// EasyKey Converter v0.80 — MIDI Edition
// Visual Music Notation System (VMNS) © Shareef Ali Rashada / EasyKey Music
//
// Changes from v0.55
//  1. Notes are drawn at their true start and length (off-beat and dotted notes were rounded to whole rows).
//  2. Bar lines follow every time signature in the file, and one row = one beat of the time signature.
//  3. Pickup (lead-in) support, plus automatic removal of empty bars before the first note.
//  4. Drums are left out by default and every track/channel can be switched on or off.
//  5. Firmer timing clean-up: Auto picks the best grid (1/4 or 1/3 beat) and snaps starts and ends to it.
//  Symbols now follow the book: diamonds for notes of 3/4 beat or longer (drawn to their exact length),
//  ▼ for a short note in the first half of a beat, ▲ for a short note in the second half.
//  Also: book-style keyboard header (narrow shaded black keys, white-key names), measure numbers,
//  page splitting for printing, SVG download, working debug panel.

'use strict';

const $ = id => document.getElementById(id);
const fileInput = $('fileInput'), svgWrap = $('svgWrap'), statusEl = $('status');
const tracksEl = $('tracks'), debugPanel = $('debugPanel'), titleEl = $('songTitle');
const timingSel = $('timingMode'), snapSel = $('snapGrid'), cellSel = $('cellUnit');
const pickupIn = $('pickup'), octavesChk = $('octaves'), viewSel = $('viewMode'), tripletSel = $('tripletStyle');

let song = null;          // parsed MIDI
let enabled = new Set();  // enabled track:channel groups
let showDebug = false;
let lastResult = null;

// ---------- UI wiring ----------
$('debugBtn').addEventListener('click', e => {
  showDebug = !showDebug;
  e.target.dataset.on = String(showDebug);
  e.target.textContent = `Debug (${showDebug ? 'on' : 'off'})`;
  debugPanel.hidden = !showDebug || !lastResult;
});
$('clearBtn').addEventListener('click', () => {
  song = null; lastResult = null; svgWrap.innerHTML = ''; tracksEl.hidden = true;
  titleEl.hidden = true; debugPanel.hidden = true; statusEl.textContent = 'Cleared.';
});
$('printBtn').addEventListener('click', () => { if (lastResult) window.print(); });
$('svgBtn').addEventListener('click', downloadSVG);
[timingSel, snapSel, cellSel, pickupIn, octavesChk, viewSel, tripletSel].forEach(el => el.addEventListener('change', redraw));

fileInput.addEventListener('change', async e => {
  const f = e.target.files?.[0]; if (!f) return;
  statusEl.textContent = `Loading ${f.name}…`;
  try {
    const ab = await f.arrayBuffer();
    song = parseMIDI(new DataView(ab));
    song.fileName = f.name.replace(/\.(mid|midi)$/i, '');
    enabled = new Set(song.groups.filter(g => !g.isDrum).map(g => g.key));
    pickupIn.value = 0;
    buildTrackList();
    redraw();
  } catch (err) {
    console.error(err);
    statusEl.textContent = `Could not read this MIDI file (${err.message}).`;
  }
  fileInput.value = '';
});

function buildTrackList() {
  tracksEl.innerHTML = '<strong>Parts:</strong> ';
  for (const g of song.groups) {
    const lab = document.createElement('label');
    const cb = document.createElement('input');
    cb.type = 'checkbox'; cb.checked = enabled.has(g.key);
    cb.addEventListener('change', () => { cb.checked ? enabled.add(g.key) : enabled.delete(g.key); redraw(); });
    lab.appendChild(cb);
    lab.append(` ${g.label} (${g.count})`);
    tracksEl.appendChild(lab);
  }
  tracksEl.hidden = false;
}

function redraw() {
  if (!song) return;
  const opts = {
    mode: timingSel.value,
    snap: parseInt(snapSel.value, 10),
    cell: cellSel.value,
    pickup: Math.max(0, parseFloat(pickupIn.value) || 0),
  };
  const res = convert(song, opts);
  lastResult = res;
  titleEl.textContent = song.title || song.fileName; titleEl.hidden = false;
  if (viewSel.value === 'pro') renderPro(res); else renderPages(res, { octaves: octavesChk.checked });
  statusEl.textContent = res.notes.length
    ? `${res.notes.length} notes · ${res.bars.length - 1} bars · ${res.tsText} · one row = ${res.cellName} · key ${res.keys.map(k => k.name).filter((v, i, a) => a.indexOf(v) === i).join(' → ')} (${res.keySource}) · timing: ${res.modeUsed}${res.scaled ? ` · grid enlarged ×${2 ** res.scaled} for fast notes` : ''}`
    : 'No notes in the selected parts.';
  debugPanel.textContent = res.debug;
  debugPanel.hidden = !showDebug;
}

// ---------- MIDI parsing ----------
function readVLQ(dv, i) {
  let v = 0, b;
  do { b = dv.getUint8(i++); v = (v << 7) | (b & 0x7F); } while (b & 0x80);
  return { value: v, next: i };
}

function parseMIDI(dv) {
  let i = 0;
  const str = n => { let s = ''; for (let k = 0; k < n; k++) s += String.fromCharCode(dv.getUint8(i++)); return s; };
  const u32 = () => { const v = dv.getUint32(i); i += 4; return v; };
  const u16 = () => { const v = dv.getUint16(i); i += 2; return v; };

  if (str(4) !== 'MThd') throw new Error('not a MIDI file');
  const hdrLen = u32(), format = u16(), ntrks = u16(), division = u16();
  i += hdrLen - 6;
  // SMPTE timing has no beats; assume 120 bpm so the grid is still usable.
  const ppq = (division & 0x8000) ? ((256 - (division >> 8)) * (division & 0xFF)) / 2 : division;

  const notes = [], timeSigs = [], keySigs = [], trackNames = [];
  let title = '';

  for (let t = 0; t < ntrks && i < dv.byteLength; t++) {
    if (str(4) !== 'MTrk') throw new Error('track header missing');
    const len = u32(), end = Math.min(i + len, dv.byteLength);
    let abs = 0, running = null;
    const open = new Map(); // "ch,note" -> [start ticks] (stack for repeated notes)
    while (i < end) {
      const d = readVLQ(dv, i); i = d.next; abs += d.value;
      let status = dv.getUint8(i);
      if (status & 0x80) { i++; } else { status = running; }
      if (status === null) throw new Error('bad running status');

      if (status === 0xFF) {                 // meta event
        running = null;
        const type = dv.getUint8(i++); const l = readVLQ(dv, i); i = l.next;
        const data = new Uint8Array(dv.buffer, dv.byteOffset + i, l.value); i += l.value;
        if (type === 0x59 && data.length >= 2) keySigs.push({ tick: abs, sf: (data[0] << 24) >> 24, minor: data[1] === 1 });
        if (type === 0x58 && data.length >= 2) timeSigs.push({ tick: abs, num: data[0], den: Math.pow(2, data[1]) });
        if (type === 0x03) { const name = new TextDecoder('latin1').decode(data).trim(); trackNames[t] = name; if (t === 0 && !title) title = name; }
        if (type === 0x2F) break;
      } else if (status === 0xF0 || status === 0xF7) { // sysex
        running = null;
        const l = readVLQ(dv, i); i = l.next + l.value;
      } else {
        running = status;
        const cmd = status & 0xF0, ch = status & 0x0F;
        if (cmd === 0x90 || cmd === 0x80) {
          const note = dv.getUint8(i++), vel = dv.getUint8(i++);
          const key = ch + ',' + note;
          if (cmd === 0x90 && vel > 0) {
            if (!open.has(key)) open.set(key, []);
            open.get(key).push(abs);
          } else if (open.has(key) && open.get(key).length) {
            const st = open.get(key).shift();
            if (abs > st) notes.push({ midi: note, ch, track: t, st, en: abs });
          }
        } else {
          i += (cmd === 0xC0 || cmd === 0xD0) ? 1 : 2;
        }
      }
    }
    // close notes that never received a note-off
    for (const [key, starts] of open) for (const st of starts) {
      const [ch, note] = key.split(',').map(Number);
      if (abs > st) notes.push({ midi: note, ch, track: t, st, en: abs });
    }
    i = end;
  }

  timeSigs.sort((a, b) => a.tick - b.tick);
  if (!timeSigs.length || timeSigs[0].tick > 0) timeSigs.unshift({ tick: 0, num: 4, den: 4 });
  // keep the last signature given for any tick
  const ts = []; for (const s of timeSigs) { if (ts.length && ts[ts.length - 1].tick === s.tick) ts[ts.length - 1] = s; else ts.push(s); }

  // group notes by track + channel so each part can be switched on/off
  const gmap = new Map();
  for (const n of notes) {
    const key = n.track + ':' + n.ch;
    if (!gmap.has(key)) {
      const name = trackNames[n.track] || `Track ${n.track + 1}`;
      gmap.set(key, { key, label: n.ch === 9 ? `${name} – drums` : `${name}${format === 0 ? ` (ch ${n.ch + 1})` : ''}`, count: 0, isDrum: n.ch === 9 });
    }
    gmap.get(key).count++;
  }
  // track 0's name is usually the song title when that track holds no notes
  const titleOk = title && !notes.some(n => n.track === 0) && !/^(track|untitled)/i.test(title);
  keySigs.sort((a, b) => a.tick - b.tick);
  return { format, ppq, notes, timeSigs: ts, keySigs, groups: [...gmap.values()], title: titleOk ? title : '' };
}

// ---------- conversion to rows ----------
const NOTE_NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'];
const isBlack = m => [1, 3, 6, 8, 10].includes(((m % 12) + 12) % 12);

function convert(s, opts) {
  const first = s.timeSigs[0];
  // quarter notes per row
  let cellQ;
  if (opts._cellQ) cellQ = opts._cellQ;
  else if (opts.cell === 'auto') cellQ = first.den >= 4 ? 4 / first.den : 1;
  else cellQ = parseFloat(opts.cell);
  const cellName = cellQ === 1 ? 'quarter note' : cellQ === 0.5 ? 'eighth note' : cellQ === 2 ? 'half note' : cellQ === 0.25 ? 'sixteenth note' : `${cellQ} quarter notes`;

  const toRows = tick => tick / s.ppq / cellQ;
  let raw = s.notes.filter(n => enabled.has(n.track + ':' + n.ch))
                   .map(n => ({ midi: n.midi, a: toRows(n.st), b: toRows(n.en) }));

  // --- timing clean-up ---
  const residual = (vals, div) => {
    if (!vals.length) return 0;
    let sum = 0; for (const v of vals) sum += Math.abs(v - Math.round(v * div) / div);
    return (sum / vals.length) * div; // as a fraction of one grid step
  };
  const starts = raw.map(n => n.a);
  let grid = 0, modeUsed = opts.mode, detail = '';
  if (opts.mode === 'quantized') {
    grid = opts.snap; modeUsed = `quantized to 1/${grid} beat`;
  } else if (opts.mode === 'auto') {
    const r4 = residual(starts, 4), r3 = residual(starts, 3), r96 = residual(starts, 96);
    // notation-made files land (almost) exactly on 1/4 or 1/3 beat; played files do not
    if (r96 < 0.05) { grid = 96; modeUsed = 'auto (notation file, exact)'; }
    else if (r3 < r4 * 0.6) { grid = 3; modeUsed = 'auto (played, snapped to 1/3 beat)'; }
    else { grid = 4; modeUsed = 'auto (played, snapped to 1/4 beat)'; }
    detail = `residuals: 1/4=${r4.toFixed(3)} 1/3=${r3.toFixed(3)} 1/96=${r96.toFixed(3)}`;
  } else { modeUsed = 'expressive (no snapping)'; }

  if (grid) {
    const q = v => Math.round(v * grid) / grid;
    raw = raw.map(n => { const a = q(n.a); let b = q(n.b); if (b <= a) b = a + 1 / grid; return { midi: n.midi, a, b }; });
    // remove duplicates created by snapping (same key, same start)
    const seen = new Set();
    raw = raw.filter(n => { const k = n.midi + '@' + n.a; if (seen.has(k)) return false; seen.add(k); return true; });
  }
  raw.sort((x, y) => x.a - y.a || x.midi - y.midi);

  // Scalable grid: if any note is faster than a sixteenth of a row, give each row a smaller note value
  // (up to twice) so every note is at least a quarter of a row and stays readable.
  if (opts.cell === 'auto' && (opts._depth || 0) < 2 && raw.some(n => n.b - n.a < 0.25 - 1e-6)) {
    return convert(s, { ...opts, _cellQ: cellQ / 2, _depth: (opts._depth || 0) + 1, pickup: opts.pickup * 2 });
  }

  // --- time signatures in rows ---
  const sigs = s.timeSigs.map(t => ({ row: toRows(t.tick), num: t.num, den: t.den, len: t.num * (4 / t.den) / cellQ }));
  const sigAt = row => { let cur = sigs[0]; for (const t of sigs) if (t.row <= row + 1e-9) cur = t; return cur; };

  // --- remove empty whole bars before the first note ---
  let shift = 0;
  if (raw.length) {
    const firstRow = raw[0].a, barLen = sigs[0].len;
    const emptyBars = Math.floor((firstRow + 1e-9) / barLen);
    if (emptyBars > 0 && sigs.every(t => t.row === 0 || t.row >= emptyBars * barLen)) shift = emptyBars * barLen;
  }
  // a file that starts with rests for most of bar 1 usually holds a pickup: trim the rests and treat the rest as a pickup
  let autoPickup = 0;
  if (raw.length && opts.pickup === 0) {
    const barLen = sigs[0].len, lead = raw[0].a - shift;
    if (lead >= barLen / 2 - 1e-9 && lead < barLen - 1e-9 && sigs.every(t => t.row === 0 || t.row >= shift + barLen)) {
      autoPickup = barLen - lead; shift += lead;
    }
  }
  if (shift) { raw.forEach(n => { n.a -= shift; n.b -= shift; }); sigs.forEach(t => { t.row = Math.max(0, t.row - shift); }); }
  if (autoPickup) opts = { ...opts, pickup: autoPickup };

  // --- bar lines ---
  const lastRow = raw.reduce((m, n) => Math.max(m, n.b), 0);
  const bars = [0];
  let cur = opts.pickup > 0 ? opts.pickup : sigAt(0).len;
  bars.push(cur);
  while (cur < lastRow - 1e-9) { cur += sigAt(cur).len; bars.push(cur); }
  const totalRows = Math.max(bars[bars.length - 1], 1);

  // --- key range, widened to start and end on white keys ---
  let lo = Infinity, hi = -Infinity;
  for (const n of raw) { lo = Math.min(lo, n.midi); hi = Math.max(hi, n.midi); }
  if (!isFinite(lo)) { lo = 60; hi = 72; }
  if (isBlack(lo)) lo--; if (isBlack(hi)) hi++;
  while (hi - lo < 11) { hi++; if (isBlack(hi)) hi++; }

  // --- key: from the file's key signatures, otherwise estimated from the notes ---
  let keys, keySource;
  const ksInFile = s.keySigs.filter(k => k.sf >= -7 && k.sf <= 7);
  if (ksInFile.length) {
    keys = ksInFile.map(k => ({ row: Math.max(0, toRows(k.tick) - shift), sf: k.sf, name: keyName(k.sf, k.minor) }));
    if (keys[0].row > 0) keys.unshift({ row: 0, sf: keys[0].sf, name: keys[0].name });
    keySource = 'from file';
  } else {
    const est = estimateKey(raw);
    keys = [{ row: 0, sf: est.sf, name: est.name }];
    keySource = 'estimated';
  }
  const keyAt = row => { let k = keys[0]; for (const x of keys) if (x.row <= row + 1e-9) k = x; return k; };

  // --- tuplets (triplets etc.): notes that sit on a 1/3, 1/5, 1/6 or 1/7 grid inside a beat ---
  markTuplets(raw);

  const tsText = sigs.map(t => `${t.num}/${t.den}`).filter((v, i, a) => a.indexOf(v) === i).join(', ');
  const debug = [
    `File: ${s.fileName}  format ${s.format}  ticks/quarter ${s.ppq}`,
    `Key: ${keys.map(k => `${k.name} @row ${k.row}`).join('; ')} (${keySource})`,
    `Tuplet notes: ${raw.filter(n => n.tup).length}`,
    `Time signatures: ${s.timeSigs.map(t => `${t.num}/${t.den} @tick ${t.tick}`).join('; ')}`,
    `One row = ${cellName} (${cellQ} quarter)  bar length (first) = ${sigs[0].len} rows`,
    `Timing: ${modeUsed}  ${detail}`,
    `Grid enlarged: ×${2 ** (opts._depth || 0)}\nEmpty rows removed at start: ${shift}   pickup rows: ${opts.pickup}`,
    `Parts on: ${[...enabled].join(', ')}`,
    `Notes drawn: ${raw.length}   key range: ${midiName(lo)}–${midiName(hi)}   rows: ${totalRows}`,
    '', 'First 40 notes (row start → end):',
    ...raw.slice(0, 40).map(n => `  ${midiName(n.midi).padEnd(4)} ${n.a.toFixed(3)} → ${n.b.toFixed(3)}  (${(n.b - n.a).toFixed(3)} rows)`),
  ].join('\n');

  return { notes: raw, bars, totalRows, lo, hi, tsText, cellName, modeUsed, debug, pickup: opts.pickup, scaled: opts._depth || 0, keys, keyAt, keySource };
}

// ---------- keys and spelling ----------
const SHARP_NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'];
const FLAT_NAMES = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B'];
const NEUTRAL_NAMES = ['C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'Ab', 'A', 'Bb', 'B']; // C major / A minor
const MAJOR_BY_SF = { '-7': 'Cb', '-6': 'Gb', '-5': 'Db', '-4': 'Ab', '-3': 'Eb', '-2': 'Bb', '-1': 'F', '0': 'C', '1': 'G', '2': 'D', '3': 'A', '4': 'E', '5': 'B', '6': 'F#', '7': 'C#' };
const MINOR_BY_SF = { '-7': 'Ab', '-6': 'Eb', '-5': 'Bb', '-4': 'F', '-3': 'C', '-2': 'G', '-1': 'D', '0': 'A', '1': 'E', '2': 'B', '3': 'F#', '4': 'C#', '5': 'G#', '6': 'D#', '7': 'A#' };
function keyName(sf, minor) { return minor ? `${MINOR_BY_SF[sf]} minor` : `${MAJOR_BY_SF[sf]} major`; }

function spell(m, sf) {
  const pc = ((m % 12) + 12) % 12;
  if (sf >= 6 && pc === 5) return 'E#';
  if (sf >= 7 && pc === 0) return 'B#';
  if (sf <= -6 && pc === 11) return 'Cb';
  if (sf <= -7 && pc === 4) return 'Fb';
  return (sf > 0 ? SHARP_NAMES : sf < 0 ? FLAT_NAMES : NEUTRAL_NAMES)[pc];
}
function spelledOctave(m, sf) {
  const pc = ((m % 12) + 12) % 12, oct = Math.floor(m / 12) - 1;
  if (sf >= 7 && pc === 0) return oct - 1; // B#3 is the same key as C4
  if (sf <= -6 && pc === 11) return oct + 1; // Cb5 is the same key as B4
  return oct;
}

// Krumhansl–Schmuckler key finding: compare how long each pitch class sounds with the
// typical major and minor profiles, in all 12 keys, and keep the best match.
function estimateKey(notes) {
  const MAJ = [6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88];
  const MIN = [6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17];
  const dur = new Array(12).fill(0);
  for (const n of notes) dur[((n.midi % 12) + 12) % 12] += n.b - n.a;
  if (!dur.some(v => v > 0)) return { sf: 0, name: 'C major' };
  const corr = (x, y) => { const mx = x.reduce((s, v) => s + v, 0) / 12, my = y.reduce((s, v) => s + v, 0) / 12;
    let n = 0, dx = 0, dy = 0; for (let i = 0; i < 12; i++) { n += (x[i] - mx) * (y[i] - my); dx += (x[i] - mx) ** 2; dy += (y[i] - my) ** 2; } return n / Math.sqrt(dx * dy || 1); };
  let best = { r: -2 };
  for (let t = 0; t < 12; t++) for (const [prof, minor] of [[MAJ, false], [MIN, true]]) {
    const rot = Array.from({ length: 12 }, (_, i) => prof[(i - t + 12) % 12]);
    const r = corr(dur, rot); if (r > best.r) best = { r, t, minor };
  }
  const majorTonic = best.minor ? (best.t + 3) % 12 : best.t;
  // circle of fifths position of the major key; prefer flats for Db/Gb, sharps for B/F#
  const SF_OF = { 0: 0, 7: 1, 2: 2, 9: 3, 4: 4, 11: 5, 6: 6, 1: -5, 8: -4, 3: -3, 10: -2, 5: -1 };
  const sf = SF_OF[majorTonic];
  return { sf, name: keyName(sf, best.minor) };
}

// Mark notes that belong to tuplets (3, 5, 6 or 7 notes in the space of a beat or two)
function markTuplets(notes) {
  const near = (v, n) => Math.abs(v * n - Math.round(v * n)) < 0.02;
  for (const n of notes) {
    const len = n.b - n.a, frac = n.a - Math.floor(n.a + 1e-9);
    if (len >= 1.0 - 1e-9) continue;
    if (near(frac, 4) && near(len, 4)) continue;           // ordinary eighths/sixteenths
    for (const k of [3, 6, 5, 7]) {
      if (near(frac, k) && near(len, k)) { n.tup = { k, frac, slot: Math.round(frac * k) }; break; }
    }
  }
  // group: tuplet notes of the same kind in the same beat share the group's starting point
  const groups = new Map();
  for (const n of notes) if (n.tup) {
    const key = Math.floor(n.a + 1e-9) + ':' + n.tup.k;
    groups.set(key, Math.min(groups.has(key) ? groups.get(key) : 1, n.tup.frac));
  }
  for (const n of notes) if (n.tup) n.tup.groupStart = groups.get(Math.floor(n.a + 1e-9) + ':' + n.tup.k);
}

function midiName(m) { return NOTE_NAMES[m % 12] + (Math.floor(m / 12) - 1); }

// ---------- drawing ----------
const C = { white: '#ffffff', blackCol: '#d3d3d3', key: '#000000', grid: '#8c8c8c', bar: '#000000', ink: '#000000', label: '#000000' };
const WW = 30, BW = 20, ROW = 28, HEAD = 44, NUMW = 30, PAD = 12;

function columns(lo, hi) {
  const cols = []; let x = 0;
  for (let m = lo; m <= hi; m++) { const b = isBlack(m); const w = b ? BW : WW; cols.push({ midi: m, black: b, x, w }); x += w; }
  return { cols, width: x };
}

function splitPages(bars, maxRows = 28) {
  const pages = []; let startIdx = 0;
  while (startIdx < bars.length - 1) {
    let endIdx = startIdx + 1;
    while (endIdx + 1 < bars.length && bars[endIdx + 1] - bars[startIdx] <= maxRows) endIdx++;
    pages.push({ from: bars[startIdx], to: bars[endIdx], barIdx: [startIdx, endIdx] });
    startIdx = endIdx;
  }
  return pages;
}

function renderPages(res, view) {
  svgWrap.innerHTML = '';
  const pages = splitPages(res.bars);
  pages.forEach((p, i) => {
    const holder = document.createElement('div'); holder.className = 'page';
    const cap = document.createElement('div'); cap.className = 'page-cap';
    cap.textContent = `${titleEl.textContent} – Page ${i + 1}${pages.length > 1 ? ' of ' + pages.length : ''}`;
    holder.appendChild(cap);
    holder.appendChild(buildSVG(res, view, p.from, p.to, p.barIdx));
    svgWrap.appendChild(holder);
  });
}

function buildSVG(res, view, fromRow, toRow, barIdx) {
  const NS = 'http://www.w3.org/2000/svg';
  const { cols, width: gw } = columns(res.lo, res.hi);
  const rows = toRow - fromRow, gh = rows * ROW;
  const W = PAD + gw + NUMW + PAD, H = PAD + HEAD + gh + PAD;
  const svg = document.createElementNS(NS, 'svg');
  svg.setAttribute('xmlns', NS);
  svg.setAttribute('width', W); svg.setAttribute('height', H); svg.setAttribute('viewBox', `0 0 ${W} ${H}`);
  const el = (tag, attrs, parent = svg) => { const e = document.createElementNS(NS, tag); for (const k in attrs) e.setAttribute(k, attrs[k]); parent.appendChild(e); return e; };
  el('rect', { x: 0, y: 0, width: W, height: H, fill: '#ffffff' });

  const g = el('g', { transform: `translate(${PAD},${PAD})` });
  // keyboard header: white keys named, black keys solid black
  for (const c of cols) {
    el('rect', { x: c.x, y: 0, width: c.w, height: HEAD, fill: c.black ? C.key : C.white, stroke: C.key, 'stroke-width': 1 }, g);
    if (!c.black) {
      const t = el('text', { x: c.x + c.w / 2, y: view.octaves ? 20 : 27, 'text-anchor': 'middle', 'font-family': 'Georgia, serif', 'font-weight': 'bold', 'font-size': 18, fill: C.label }, g);
      t.textContent = NOTE_NAMES[c.midi % 12];
      if (view.octaves) { const o = el('text', { x: c.x + c.w / 2, y: 37, 'text-anchor': 'middle', 'font-family': 'Arial, sans-serif', 'font-size': 10, fill: C.label }, g); o.textContent = String(Math.floor(c.midi / 12) - 1); }
    }
  }
  const body = el('g', { transform: `translate(0,${HEAD})` }, g);
  // column shading
  for (const c of cols) el('rect', { x: c.x, y: 0, width: c.w, height: gh, fill: c.black ? C.blackCol : C.white }, body);
  // row lines
  for (let r = 0; r <= Math.ceil(rows - 1e-9); r++) {
    const y = Math.min(r, rows) * ROW;
    el('line', { x1: 0, y1: y, x2: gw, y2: y, stroke: C.grid, 'stroke-width': 1 }, body);
  }
  // column lines
  for (const c of cols) el('line', { x1: c.x, y1: 0, x2: c.x, y2: gh, stroke: C.grid, 'stroke-width': 1 }, body);
  el('line', { x1: gw, y1: 0, x2: gw, y2: gh, stroke: C.bar, 'stroke-width': 2 }, body);
  el('line', { x1: 0, y1: 0, x2: 0, y2: gh, stroke: C.bar, 'stroke-width': 2 }, body);
  // bar lines + measure numbers (right side)
  const hasPickup = res.pickup > 0;
  for (let bi = barIdx[0]; bi <= barIdx[1]; bi++) {
    const y = (res.bars[bi] - fromRow) * ROW;
    el('line', { x1: 0, y1: y, x2: gw, y2: y, stroke: C.bar, 'stroke-width': 2 }, body);
    if (bi < res.bars.length - 1 && bi < barIdx[1]) {
      const num = hasPickup ? bi : bi + 1;
      if (num > 0) { const t = el('text', { x: gw + 6, y: y + 14, 'font-family': 'Arial, sans-serif', 'font-size': 11, fill: '#555' }, body); t.textContent = num; }
    }
  }

  // notes
  const ink = el('g', {}, body);
  const colOf = new Map(cols.map(c => [c.midi, c]));
  for (const n of res.notes) {
    const c = colOf.get(n.midi); if (c) drawNote(el, ink, c, n, fromRow, toRow, ROW);
  }
  return svg;
}

// Draws one note in column c, clipped to rows [fromRow, toRow). Row height = rowH px.
function drawNote(el, parent, c, n, fromRow, toRow, rowH) {
  if (n.b <= fromRow + 1e-9 || n.a >= toRow - 1e-9) return;
  const a = Math.max(n.a, fromRow), b = Math.min(n.b, toRow);
  const y0 = (a - fromRow) * rowH, y1 = (b - fromRow) * rowH;
  const cx = c.x + c.w / 2, hw = c.w * 0.42;
  const len = n.b - n.a;
  const before = n.a < fromRow - 1e-9, after = n.b > toRow + 1e-9;
  if (before || after) {
    // Shareef's held-key symbol: a diamond point marks where the note starts or ends,
    // a filled square/bar means the key stays down across the bar line.
    const span = y1 - y0, taper = Math.min(rowH * 0.5, span * 0.5);
    const top = before ? [[cx - hw, y0], [cx + hw, y0]] : [[cx, y0], [cx + hw, y0 + taper]];
    const bot = after ? [[cx + hw, y1], [cx - hw, y1]] : [[cx + hw, y1 - taper], [cx, y1]];
    const left = before ? [] : [[cx - hw, y0 + taper]];
    const pts = [...top, ...bot, ...(after ? [] : [[cx - hw, y1 - taper]]), ...left];
    el('polygon', { points: pts.map(p => p.join(',')).join(' '), fill: C.ink }, parent);
  } else if (n.tup) {
    // tuplets: stacked triangles, one per note, each filling its share of the beat
    const style = tripletSel ? tripletSel.value : 'group';
    let down;
    if (style === 'group') down = n.tup.groupStart < 0.5 - 1e-9;       // whole group points the way its first note does
    else if (style === 'half') down = n.tup.frac < 0.5 - 1e-9;          // same rule as eighths: ▼ first half, ▲ second half
    else down = n.tup.slot % 2 === 0;                                    // alternate ▼▲▼
    if (down) el('polygon', { points: `${cx - hw},${y0} ${cx + hw},${y0} ${cx},${y1}`, fill: C.ink }, parent);
    else el('polygon', { points: `${cx - hw},${y1} ${cx + hw},${y1} ${cx},${y0}`, fill: C.ink }, parent);
  } else if (len >= 0.75 - 1e-9) {
    // diamond drawn to the note's exact length
    const my = (y0 + y1) / 2;
    el('polygon', { points: `${cx},${y0} ${cx + hw},${my} ${cx},${y1} ${cx - hw},${my}`, fill: C.ink }, parent);
  } else if (len < 0.375 - 1e-9) {
    // sixteenth: thin diamond from one corner of the row to its centre, clockwise from top-left
    const within = n.a - Math.floor(n.a + 1e-9);
    const slot = Math.max(0, Math.min(3, Math.floor(within * 4 + 1e-6)));
    const rowTop = (Math.floor(n.a + 1e-9) - fromRow) * rowH;
    const corners = [[c.x, rowTop], [c.x + c.w, rowTop], [c.x + c.w, rowTop + rowH], [c.x, rowTop + rowH]];
    const [px, py] = corners[slot];
    const ccx = c.x + c.w / 2, ccy = rowTop + rowH / 2;
    const vx = ccx - px, vy = ccy - py, L = Math.hypot(vx, vy) || 1, nx = -vy / L, ny = vx / L;
    const t = Math.min(c.w, rowH) * 0.16, mx = (px + ccx) / 2, my = (py + ccy) / 2;
    el('polygon', { points: `${px},${py} ${mx + nx * t},${my + ny * t} ${ccx},${ccy} ${mx - nx * t},${my - ny * t}`, fill: C.ink }, parent);
  } else {
    // short note: ▼ when it starts in the first half of the beat, ▲ when in the second half
    const within = n.a - Math.floor(n.a + 1e-9);
    if (within < 0.5 - 1e-9) el('polygon', { points: `${cx - hw},${y0} ${cx + hw},${y0} ${cx},${y1}`, fill: C.ink }, parent);
    else el('polygon', { points: `${cx - hw},${y1} ${cx + hw},${y1} ${cx},${y0}`, fill: C.ink }, parent);
  }
}

// ---------- Pro Mode ----------
// One small grid per measure. Columns cover groupings of played keys: gaps of up to 3 unused keys are kept,
// wider jumps start a new grouping with a thick divider and an octave subscript. Hands split into two blocks when unused keys in
// the span outnumber the used ones. Measures run down the page, then continue in a new column.
const MAX_GAP = 3; // unused keys allowed inside a grouping
const PRO = { WW: 26, BW: 20, ROW: 22, HEAD: 30, NUMH: 16, GAP: 12, COLGAP: 28, PAGE_W: 720, PAGE_H: 960 };

function proMeasures(res) {
  const out = [];
  for (let i = 0; i < res.bars.length - 1; i++) {
    const from = res.bars[i], to = res.bars[i + 1];
    const notes = res.notes.filter(n => n.b > from + 1e-9 && n.a < to - 1e-9);
    const pitches = [...new Set(notes.map(n => n.midi))].sort((x, y) => x - y);
    let groups = [pitches];
    if (pitches.length >= 2) {
      const span = pitches[pitches.length - 1] - pitches[0] + 1, used = pitches.length;
      if (span - used > used) {
        let k = 0, best = -1;
        for (let j = 0; j < pitches.length - 1; j++) { const g = pitches[j + 1] - pitches[j]; if (g > best) { best = g; k = j; } }
        groups = [pitches.slice(0, k + 1), pitches.slice(k + 1)];
      }
    }
    const blocks = groups.map(ps => {
      // key groupings: keys played less than 4 keys apart stay together with the keys between them shown;
      // a wider jump starts a new grouping (thick divider + octave subscript)
      let x = 0; const cols = [];
      ps.forEach((m, j) => {
        const prev = j > 0 ? ps[j - 1] : null;
        const startGroup = prev === null || m - prev - 1 > MAX_GAP;
        const keys = startGroup ? [m] : Array.from({ length: m - prev }, (_, k) => prev + 1 + k);
        keys.forEach((k, idx) => {
          const w = isBlack(k) ? PRO.BW : PRO.WW;
          const first = startGroup && idx === 0;
          cols.push({ midi: k, black: isBlack(k), x, w, sub: first, jump: first && j > 0 });
          x += w;
        });
      });
      if (!cols.length) cols.push({ midi: null, black: false, x: 0, w: PRO.WW, sub: false }), x = PRO.WW; // a bar of rests
      return { cols, width: x };
    });
    const width = blocks.reduce((s, b) => s + b.width, 0) + PRO.GAP * (blocks.length - 1);
    const height = PRO.NUMH + PRO.HEAD + (to - from) * PRO.ROW;
    const num = res.pickup > 0 ? i : i + 1;
    out.push({ from, to, notes, blocks, width, height, num });
  }
  return out;
}

function layoutPro(measures) {
  const pages = []; let page = null, colX = 0, y = 0, colW = 0;
  const newPage = () => { page = { items: [], width: 0, height: 0 }; pages.push(page); colX = 0; y = 0; colW = 0; };
  newPage();
  for (const m of measures) {
    if (y > 0 && y + m.height > PRO.PAGE_H) { colX += colW + PRO.COLGAP; y = 0; colW = 0; }        // new column
    if (colX > 0 && colX + m.width > PRO.PAGE_W) newPage();                                           // new page
    page.items.push({ m, x: colX, y });
    y += m.height + 10; colW = Math.max(colW, m.width);
    page.width = Math.max(page.width, colX + m.width); page.height = Math.max(page.height, y);
  }
  return pages;
}

function buildProPage(page, res) {
  const NS = 'http://www.w3.org/2000/svg', P = 12;
  const W = page.width + 2 * P, H = page.height + 2 * P;
  const svg = document.createElementNS(NS, 'svg');
  svg.setAttribute('xmlns', NS); svg.setAttribute('width', W); svg.setAttribute('height', H); svg.setAttribute('viewBox', `0 0 ${W} ${H}`);
  const el = (tag, attrs, parent = svg) => { const e = document.createElementNS(NS, tag); for (const k in attrs) e.setAttribute(k, attrs[k]); parent.appendChild(e); return e; };
  el('rect', { x: 0, y: 0, width: W, height: H, fill: '#ffffff' });
  for (const { m, x, y } of page.items) {
    const g = el('g', { transform: `translate(${P + x},${P + y})` });
    const t = el('text', { x: 0, y: 11, 'font-family': 'Arial, sans-serif', 'font-size': 11, fill: '#555' }, g);
    t.textContent = m.num > 0 ? `${m.num}` : 'pickup';
    const rows = m.to - m.from, gh = rows * PRO.ROW;
    let bx = 0;
    for (const b of m.blocks) {
      const bg = el('g', { transform: `translate(${bx},${PRO.NUMH})` }, g);
      // header: every column named (no keyboard context in Pro Mode), octave as subscript where needed
      for (const c of b.cols) {
        el('rect', { x: c.x, y: 0, width: c.w, height: PRO.HEAD, fill: c.black ? '#000000' : '#ffffff', stroke: '#000', 'stroke-width': 1 }, bg);
        if (c.midi === null) continue;
        const lab = el('text', { x: c.x + c.w / 2, y: 19, 'text-anchor': 'middle', 'font-family': 'Georgia, serif', 'font-weight': 'bold', 'font-size': c.black ? 11 : 14, fill: c.black ? '#ffffff' : '#000000' }, bg);
        lab.textContent = spell(c.midi, res.keyAt(m.from).sf);
        if (c.sub) { const s = el('tspan', { 'font-size': 9, dy: 4, 'font-weight': 'normal' }, lab); s.textContent = String(spelledOctave(c.midi, res.keyAt(m.from).sf)); }
      }
      const body = el('g', { transform: `translate(0,${PRO.HEAD})` }, bg);
      for (const c of b.cols) el('rect', { x: c.x, y: 0, width: c.w, height: gh, fill: c.black ? C.blackCol : C.white }, body);
      for (let r = 0; r <= Math.ceil(rows - 1e-9); r++) { const yy = Math.min(r, rows) * PRO.ROW; el('line', { x1: 0, y1: yy, x2: b.width, y2: yy, stroke: C.grid, 'stroke-width': 1 }, body); }
      for (const c of b.cols) el('line', { x1: c.x, y1: 0, x2: c.x, y2: gh, stroke: c.jump ? '#000' : C.grid, 'stroke-width': c.jump ? 2.5 : 1 }, body);
      el('rect', { x: 0, y: 0, width: b.width, height: gh, fill: 'none', stroke: '#000', 'stroke-width': 2 }, body);
      const colOf = new Map(b.cols.map(c => [c.midi, c]));
      for (const n of m.notes) { const c = colOf.get(n.midi); if (c) drawNote(el, body, c, n, m.from, m.to, PRO.ROW); }
      bx += b.width + PRO.GAP;
    }
  }
  return svg;
}

function renderPro(res) {
  svgWrap.innerHTML = '';
  const pages = layoutPro(proMeasures(res));
  pages.forEach((p, i) => {
    const holder = document.createElement('div'); holder.className = 'page';
    const cap = document.createElement('div'); cap.className = 'page-cap';
    cap.textContent = `${titleEl.textContent} – Pro – Page ${i + 1}${pages.length > 1 ? ' of ' + pages.length : ''}`;
    holder.appendChild(cap); holder.appendChild(buildProPage(p, res)); svgWrap.appendChild(holder);
  });
  return pages;
}

// stack Pro pages vertically into one page for the SVG download
function mergePages(a, b) {
  const off = a.height + 30;
  return { items: [...a.items, ...b.items.map(it => ({ ...it, y: it.y + off }))], width: Math.max(a.width, b.width), height: off + b.height };
}

function downloadSVG() {
  if (!lastResult) return;
  const res = lastResult;
  const svg = viewSel.value === 'pro'
    ? buildProPage(layoutPro(proMeasures(res)).reduce((all, p) => all ? mergePages(all, p) : p, null), res)
    : buildSVG(res, { octaves: octavesChk.checked }, 0, res.totalRows, [0, res.bars.length - 1]);
  const blob = new Blob(['<?xml version="1.0" encoding="UTF-8"?>\n' + new XMLSerializer().serializeToString(svg)], { type: 'image/svg+xml' });
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob); a.download = `${(titleEl.textContent || 'easykey').replace(/[^\w\- ]+/g, '')} - EasyKey.svg`;
  document.body.appendChild(a); a.click(); a.remove();
  setTimeout(() => URL.revokeObjectURL(a.href), 1000);
}
