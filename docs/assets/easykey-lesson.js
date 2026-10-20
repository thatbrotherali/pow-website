/* EasyKey free lesson: an EasyKey grid you can listen to or play along with.
   Symbols follow the EasyKey book: columns are piano keys, rows are beats read top to bottom,
   and a diamond's length is the note's length. Bold lines are bar lines. */
(() => {
  const root = document.getElementById("ek-lesson");
  if (!root) return;

  // Twinkle Twinkle Little Star (traditional), key of C, 4/4, one row = one beat
  const SONG = [
    [60,1],[60,1],[67,1],[67,1], [69,1],[69,1],[67,2],
    [65,1],[65,1],[64,1],[64,1], [62,1],[62,1],[60,2],
    [67,1],[67,1],[65,1],[65,1], [64,1],[64,1],[62,2],
    [67,1],[67,1],[65,1],[65,1], [64,1],[64,1],[62,2],
    [60,1],[60,1],[67,1],[67,1], [69,1],[69,1],[67,2],
    [65,1],[65,1],[64,1],[64,1], [62,1],[62,1],[60,2],
  ];
  const WORDS = ["Twin","kle","twin","kle","lit","tle","star","how","I","won","der","what","you","are",
    "Up","a","bove","the","world","so","high","like","a","dia","mond","in","the","sky",
    "Twin","kle","twin","kle","lit","tle","star","how","I","won","der","what","you","are"];
  const notes = []; let t = 0;
  SONG.forEach(([m, len], i) => { notes.push({ m, a: t, b: t + len, w: WORDS[i] }); t += len; });
  const ROWS = t, BAR = 4;

  const LO = 60, HI = 72, NAMES = ["C","C♯","D","D♯","E","F","F♯","G","G♯","A","A♯","B"];
  const isBlack = m => [1,3,6,8,10].includes(m % 12);
  const WW = 30, BW = 20, ROW = 24, HEAD = 58;
  const cols = []; let x = 0;
  for (let m = LO; m <= HI; m++) { const b = isBlack(m); cols.push({ m, b, x, w: b ? BW : WW }); x += b ? BW : WW; }
  const GW = x, WORDW = 56, W = GW + WORDW, GH = ROWS * ROW;
  const colOf = new Map(cols.map(c => [c.m, c]));

  const NS = "http://www.w3.org/2000/svg";
  const el = (tag, attrs, parent) => { const e = document.createElementNS(NS, tag); for (const k in attrs) e.setAttribute(k, attrs[k]); if (parent) parent.appendChild(e); return e; };

  // keyboard (sticky, tappable)
  const kb = el("svg", { viewBox: `0 0 ${W} ${HEAD}`, class: "ek-keys", role: "group", "aria-label": "Piano keys from middle C to the C above. Tap a key to play it." });
  const keyEls = new Map();
  for (const c of cols) {
    const g = el("g", { class: "ek-key" + (c.b ? " is-black" : ""), "data-m": c.m, tabindex: "-1" }, kb);
    el("rect", { x: c.x + .5, y: .5, width: c.w - 1, height: HEAD - 1, rx: 3 }, g);
    if (!c.b) { const tx = el("text", { x: c.x + c.w / 2, y: HEAD - 14, "text-anchor": "middle" }, g); tx.textContent = NAMES[c.m % 12]; }
    keyEls.set(c.m, g);
  }

  // grid
  const grid = el("svg", { viewBox: `0 0 ${W} ${GH + 2}`, class: "ek-grid", role: "img", "aria-label": "Twinkle Twinkle Little Star written in EasyKey notation" });
  const body = el("g", { transform: "translate(0,1)" }, grid);
  for (const c of cols) el("rect", { x: c.x, y: 0, width: c.w, height: GH, class: c.b ? "ek-col-b" : "ek-col-w" }, body);
  for (let r = 0; r <= ROWS; r++) el("line", { x1: 0, y1: r * ROW, x2: GW, y2: r * ROW, class: r % BAR === 0 ? "ek-bar" : "ek-row" }, body);
  for (const c of cols) el("line", { x1: c.x, y1: 0, x2: c.x, y2: GH, class: "ek-row" }, body);
  el("line", { x1: GW, y1: 0, x2: GW, y2: GH, class: "ek-bar" }, body);
  const noteEls = notes.map(n => {
    const c = colOf.get(n.m), cx = c.x + c.w / 2, hw = c.w * .42, y0 = n.a * ROW + 1.5, y1 = n.b * ROW - 1.5, my = (y0 + y1) / 2;
    const p = el("polygon", { points: `${cx},${y0} ${cx + hw},${my} ${cx},${y1} ${cx - hw},${my}`, class: "ek-note" }, body);
    const tx = el("text", { x: GW + 8, y: n.a * ROW + ROW * .68, class: "ek-word" }, body); tx.textContent = n.w;
    return { p, tx };
  });
  const head = el("rect", { x: 0, y: 0, width: GW, height: ROW, class: "ek-head" }, body);

  const scroller = root.querySelector(".ek-scroll");
  scroller.append(grid);
  root.querySelector(".ek-keys-wrap").append(kb);

  // sound: a soft piano-like tone
  let ctx;
  const audio = () => (ctx ||= new (window.AudioContext || window.webkitAudioContext)());
  function tone(m, dur = .6) {
    const ac = audio(), t0 = ac.currentTime, f = 440 * 2 ** ((m - 69) / 12);
    const g = ac.createGain(); g.connect(ac.destination);
    g.gain.setValueAtTime(0, t0); g.gain.linearRampToValueAtTime(.28, t0 + .01); g.gain.exponentialRampToValueAtTime(.001, t0 + dur + .5);
    [[1, "triangle", 1], [2, "sine", .25], [3, "sine", .08]].forEach(([h, type, v]) => {
      const o = ac.createOscillator(), og = ac.createGain(); o.type = type; o.frequency.value = f * h; og.gain.value = v;
      o.connect(og); og.connect(g); o.start(t0); o.stop(t0 + dur + .6);
    });
  }
  function flash(m, cls = "is-on", ms = 260) { const k = keyEls.get(m); if (!k) return; k.classList.add(cls); setTimeout(() => k.classList.remove(cls), ms); }

  const status = root.querySelector(".ek-status");
  const tempo = root.querySelector(".ek-tempo");
  const btnListen = root.querySelector('[data-ek="listen"]'), btnPlay = root.querySelector('[data-ek="play"]');
  let mode = null, idx = 0, timer = null;

  function show(i) {
    noteEls.forEach((e, j) => { e.p.classList.toggle("is-done", j < i); e.p.classList.toggle("is-next", j === i); e.tx.classList.toggle("is-next", j === i); });
    if (i < 0) { head.style.opacity = 0; scroller.scrollTo({ top: 0 }); keyEls.forEach(k => k.classList.remove("is-hint")); return; }
    const n = notes[Math.min(i, notes.length - 1)];
    head.setAttribute("y", n.a * ROW); head.setAttribute("height", (n.b - n.a) * ROW);
    head.style.opacity = i < notes.length ? 1 : 0;
    const scale = grid.getBoundingClientRect().width / W, target = n.a * ROW * scale - scroller.clientHeight * .35;
    scroller.scrollTo({ top: Math.max(0, target), behavior: matchMedia("(prefers-reduced-motion: reduce)").matches ? "auto" : "smooth" });
    keyEls.forEach(k => k.classList.remove("is-hint"));
    if (mode === "play" && i < notes.length) keyEls.get(n.m).classList.add("is-hint");
  }
  function stop(msg) {
    clearTimeout(timer); mode = null;
    btnListen.textContent = "Listen"; btnPlay.textContent = "Play along";
    keyEls.forEach(k => k.classList.remove("is-hint"));
    if (msg) status.textContent = msg;
  }
  function beat() { return 60 / Number(tempo.value); }
  function listenStep() {
    if (idx >= notes.length) { stop("That's the whole song. Now try Play along."); idx = 0; show(-1); return; }
    const n = notes[idx]; show(idx); tone(n.m, (n.b - n.a) * beat() * .9); flash(n.m, "is-on", (n.b - n.a) * beat() * 900);
    timer = setTimeout(() => { idx++; listenStep(); }, (n.b - n.a) * beat() * 1000);
  }
  btnListen.addEventListener("click", () => {
    if (mode === "listen") return stop("Stopped.");
    stop(); audio(); mode = "listen"; idx = 0; btnListen.textContent = "Stop";
    status.textContent = "Watch the highlighted row move down the grid. Each diamond is a key to press."; listenStep();
  });
  btnPlay.addEventListener("click", () => {
    if (mode === "play") return stop("Stopped.");
    stop(); audio(); mode = "play"; idx = 0; btnPlay.textContent = "Stop";
    status.textContent = "Press the key under the next diamond. Tap it, or use your computer keys (A S D F G H J K are the white keys)."; show(0);
  });
  function press(m) {
    tone(m, .5);
    if (mode !== "play") { flash(m); return; }
    const n = notes[idx];
    if (m === n.m) {
      flash(m); idx++;
      if (idx >= notes.length) { show(notes.length); stop("You played Twinkle Twinkle Little Star. That's how EasyKey works: see the key, press the key."); idx = 0; return; }
      show(idx); status.textContent = `Note ${idx + 1} of ${notes.length}.`;
    } else { flash(m, "is-wrong", 320); status.textContent = `Not quite. Look for the column under the diamond in row ${notes[idx].a + 1}.`; }
  }
  kb.addEventListener("pointerdown", e => { const k = e.target.closest(".ek-key"); if (k) { e.preventDefault(); press(Number(k.dataset.m)); } });
  const MAP = { a: 60, w: 61, s: 62, e: 63, d: 64, f: 65, t: 66, g: 67, y: 68, h: 69, u: 70, j: 71, k: 72 };
  document.addEventListener("keydown", e => {
    if (e.repeat || e.metaKey || e.ctrlKey || e.altKey || /input|select|textarea/i.test(e.target.tagName)) return;
    const m = MAP[e.key.toLowerCase()]; if (m === undefined) return;
    const r = root.getBoundingClientRect(); if (r.bottom < 0 || r.top > innerHeight) return;
    e.preventDefault(); press(m);
  });
  show(-1); head.style.opacity = 0;
})();
