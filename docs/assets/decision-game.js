/* People of the World — The Decision Game
   Picture, word, "is" or "is not": decide true or false as fast as you can.
   Scores are saved online on the Wix site (shop.peopleoftheworld.net), and every run is also kept on this device. */
(() => {
  const API = "https://shop.peopleoftheworld.net/_functions/decisionGame";
  const IMG = "https://static.wixstatic.com/media/eaef6d_";
  const ITEMS = [
    ["Ball", "7f2b9555f08e4407bcf27857bf332d3c"], ["Umbrella", "a783bbb23e2f4960a84c5946322bd1d1"], ["Pig", "12d8e64c3bbb45749e7d2328b1ea3329"],
    ["Butterfly", "87217c52f3b44756834c0cc47ddb62fc"], ["Airplane", "fd2e5d6a21154331aad70d6079dce246"], ["Car", "ce7258f9c42342c49453582be5a69c88"],
    ["Mouse", "cb46105a23d049808c595598fe7d883f"], ["Hat", "bb22e0b78d134c88bb6c67d4941ece27"], ["House", "6ece4136d1ec4dc8bf3f51c8e244766b"],
    ["Cow", "df0c98fc5b28458db695aa5cb3d414a8"], ["Bus", "64f8949a66c14145948d1cb0db7e7224"], ["Tree", "0fd2bc64878e41a299cc22c3f0a35abf"],
    ["Flower", "8cf53ea56de040f2b2ceecfe2a2619b4"], ["Bee", "8f18d62b58914a7085530ea3d3183901"], ["Cup", "633ee54b4fd9427bb9ef5a3d2e027fe3"],
    ["Ballerina", "2a8b7bce57d24700b5bd133da2da1dd1"], ["Bird", "653bf4fd82f94aff94796803666e80de"], ["Chair", "3b4a0f88dd6d4ba485ed22d103eabf2a"],
    ["Book", "f0408751e9a640d88066b46722a8ea91"], ["Cherry", "97c92754a41d489eb0bb984377487207"]
  ].map(([label, id]) => ({ label, url: `${IMG}${id}~mv2.png/v1/fit/w_480,h_480,q_85/${label.toLowerCase()}.png` }));
  const MODES = {
    practice: { label: "Practice", n: Infinity, ranked: false },
    short: { label: "Short · 10", n: 10, ranked: true },
    long: { label: "Long · 20", n: 20, ranked: true },
    infinite: { label: "Endless", n: Infinity, ranked: true }
  };
  const BOARD_MODES = ["short", "long", "infinite"];
  const LIMIT_START = 1.0, LIMIT_MIN = 0.3;            // endless mode: seconds allowed per question
  const store = {
    get(k, d) { try { const v = localStorage.getItem(k); return v ? JSON.parse(v) : d; } catch { return d; } },
    set(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch {} }
  };
  const $ = id => document.getElementById(id);
  const fmt = s => (Math.round(s * 100) / 100).toFixed(2) + "s";
  const esc = s => String(s ?? "").replace(/[&<>"']/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  const day = d => { try { return new Date(d).toLocaleDateString(undefined, { day: "numeric", month: "short", year: "numeric" }); } catch { return ""; } };

  // ---------------------------------------------------------------- player identity (kept on this device)
  let me = store.get("powDG_player", null);
  if (!me || !me.id) {
    const rnd = (crypto.randomUUID ? crypto.randomUUID() : Date.now().toString(36) + Math.random().toString(36).slice(2)).replace(/[^a-zA-Z0-9-]/g, "");
    me = { id: "p-" + rnd.replace(/-/g, "").slice(0, 24), name: "" };
    store.set("powDG_player", me);
  }
  let history = store.get("powDG_history", []);    // every ranked run on this device
  let online = null;                                 // null = unknown, 1 = original service, 2 = full service, 0 = offline

  // ---------------------------------------------------------------- sound
  let ctx = null;
  const tone = (f, d, v, type = "sine") => {
    if (!$("dg-sound").checked) return;
    try {
      ctx = ctx || new (window.AudioContext || window.webkitAudioContext)();
      const o = ctx.createOscillator(), g = ctx.createGain();
      o.type = type; o.frequency.value = f; g.gain.value = v;
      o.connect(g); g.connect(ctx.destination); o.start(); o.stop(ctx.currentTime + d);
    } catch {}
  };
  const sfx = {
    beep: i => tone(600 + i * 80, 0.15, 0.2), go: () => tone(1000, 0.22, 0.25), right: () => tone(880, 0.12, 0.22),
    wrong: () => tone(260, 0.18, 0.18, "square"), end: () => { tone(900, 0.16, 0.2); setTimeout(() => tone(700, 0.18, 0.18), 180); }
  };

  // ---------------------------------------------------------------- game state
  let mode = store.get("powDG_mode", "short");
  if (!MODES[mode]) mode = "short";
  let s = null, timers = [], tick = null, qTimeout = null;

  const ui = {
    stage: $("dg-stage"), pic: $("dg-pic"), rel: $("dg-rel"), word: $("dg-word"), start: $("dg-start"),
    yes: $("dg-true"), no: $("dg-false"), q: $("dg-q"), time: $("dg-time"), avg: $("dg-avg"), ok: $("dg-ok"), bad: $("dg-bad"),
    result: $("dg-result"), limit: $("dg-limit")
  };

  function shuffle(a) { for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; }

  function setMode(m) {
    if (s && (s.running || s.counting)) stop(true);
    mode = m; store.set("powDG_mode", m);
    document.querySelectorAll("[data-mode]").forEach(b => b.setAttribute("aria-pressed", String(b.dataset.mode === m)));
    ui.limit.hidden = m !== "infinite";
    idle();
    if (BOARD_MODES.includes(m)) showBoard(m);
  }

  function idle() {
    clearAll();
    s = null;
    ui.stage.classList.remove("is-running", "flash-ok", "flash-bad");
    ui.word.textContent = "Press Start";
    ui.rel.textContent = "is"; ui.rel.classList.remove("not");
    const it = ITEMS[Math.floor(Math.random() * ITEMS.length)];
    ui.pic.src = it.url; ui.pic.alt = it.label;
    ui.start.textContent = "Start";
    ui.yes.disabled = ui.no.disabled = true;
    const n = MODES[mode].n;
    ui.q.textContent = "0 / " + (isFinite(n) ? n : "∞");
    ui.time.textContent = ui.avg.textContent = "0.00s";
    ui.ok.textContent = ui.bad.textContent = "0";
    ui.limit.textContent = "1.0s per answer";
  }

  function clearAll() {
    timers.forEach(clearTimeout); timers = [];
    clearInterval(tick); tick = null;
    clearTimeout(qTimeout); qTimeout = null;
  }

  function begin() {
    if (s && (s.running || s.counting)) { stop(true); return; }
    ui.result.hidden = true;
    if (window.innerWidth < 900) $("play").scrollIntoView({ behavior: "smooth", block: "start" });
    const n = MODES[mode].n;
    s = { counting: true, running: false, q: 0, ok: 0, bad: 0, react: 0, t0: 0, shown: 0, answer: null, live: false,
          lastW: -1, lastP: -1, lastNot: null, streak: 0, limit: LIMIT_START,
          words: isFinite(n) ? shuffle([...ITEMS.keys()]).slice(0, n) : null };
    ui.start.textContent = "Stop";
    ui.rel.textContent = ""; ui.rel.classList.remove("not");
    ui.word.textContent = "Get ready";
    [3, 2, 1].forEach((k, i) => timers.push(setTimeout(() => { ui.word.textContent = String(k); sfx.beep(i); }, 500 + i * 1000)));
    timers.push(setTimeout(() => {
      s.counting = false; s.running = true; sfx.go();
      ui.stage.classList.add("is-running");
      ui.yes.disabled = ui.no.disabled = false;
      s.t0 = performance.now();
      tick = setInterval(paintClock, 50);
      next();
    }, 3500));
  }

  function chooseNot() {
    let not = Math.random() < 0.5;
    if (s.lastNot !== null && not === s.lastNot && s.streak >= 2) not = !not;   // never more than two of a kind in a row
    s.streak = not === s.lastNot ? s.streak + 1 : 1;
    s.lastNot = not;
    return not;
  }

  function next() {
    const n = MODES[mode].n;
    if (isFinite(n) && s.q >= n) return stop(false);
    let w, p;
    if (s.words) w = s.words[s.q];
    else do { w = Math.floor(Math.random() * ITEMS.length); } while (w === s.lastW);
    // about one question in three shows the matching picture, so "is" and "is not" are both worth reading
    if (Math.random() < 1 / 3 && w !== s.lastP) p = w;
    else do { p = Math.floor(Math.random() * ITEMS.length); } while (p === s.lastP || p === w);
    const not = chooseNot();
    ui.pic.src = ITEMS[p].url; ui.pic.alt = "Picture";
    ui.word.textContent = ITEMS[w].label;
    ui.rel.textContent = not ? "is not" : "is"; ui.rel.classList.toggle("not", not);
    s.answer = not ? w !== p : w === p;
    s.lastW = w; s.lastP = p;
    s.shown = performance.now(); s.live = true;
    ui.q.textContent = (s.q + 1) + " / " + (isFinite(n) ? n : "∞");
    if (mode === "infinite") {
      s.limit = Math.max(LIMIT_MIN, LIMIT_START - 0.1 * Math.floor(s.ok / 50));
      ui.limit.textContent = s.limit.toFixed(1) + "s per answer";
      qTimeout = setTimeout(timeout, s.limit * 1000);
    }
  }

  function flash(good) {
    ui.stage.classList.remove("flash-ok", "flash-bad"); void ui.stage.offsetWidth;
    ui.stage.classList.add(good ? "flash-ok" : "flash-bad");
  }

  function answer(said) {
    if (!s || !s.running || !s.live) return;
    clearTimeout(qTimeout);
    s.live = false;
    s.react += (performance.now() - s.shown) / 1000;
    s.q++;
    const good = said === s.answer;
    good ? (s.ok++, sfx.right()) : (s.bad++, sfx.wrong());
    flash(good);
    ui.ok.textContent = s.ok; ui.bad.textContent = s.bad;
    if (mode === "infinite" && !good) return stop(false);
    next();
  }

  function timeout() {
    if (!s || !s.running || !s.live) return;
    s.live = false; s.q++; s.bad++; s.react += s.limit;
    ui.bad.textContent = s.bad; sfx.wrong(); flash(false);
    stop(false, "Out of time");
  }

  function paintClock() {
    if (!s || !s.running) return;
    ui.time.textContent = fmt((performance.now() - s.t0) / 1000);
    ui.avg.textContent = fmt(s.q ? s.react / s.q : 0);
  }

  function stop(manual, why) {
    if (!s) return;
    const wasRunning = s.running;
    clearAll();
    if (!wasRunning) { idle(); return; }
    s.running = false;
    ui.stage.classList.remove("is-running");
    ui.yes.disabled = ui.no.disabled = true;
    ui.start.textContent = "Play again";
    const run = { mode, questions: s.q, correct: s.ok, totalTime: (performance.now() - s.t0) / 1000,
                  avgReaction: s.q ? s.react / s.q : 0, date: new Date().toISOString() };
    paintClock();
    sfx.end();
    const complete = mode === "infinite" ? run.correct > 0 : run.questions === MODES[mode].n;
    ui.word.textContent = manual ? "Stopped" : (why || "Finished");
    ui.rel.textContent = ""; ui.rel.classList.remove("not");
    if (!MODES[mode].ranked || !complete) { showResult(run, null, mode === "practice" ? "Practice runs aren't recorded." : manual ? "Run stopped early, so it isn't recorded." : "No correct answers this time, so it isn't recorded."); return; }
    record(run);
  }

  // ---------------------------------------------------------------- results and saving
  function better(a, b) {
    if (!b) return true;
    if (a.mode === "infinite") {
      if (a.correct !== b.correct) return a.correct > b.correct;
      if (a.avgReaction !== b.avgReaction) return a.avgReaction < b.avgReaction;
      return a.totalTime < b.totalTime;
    }
    const am = a.questions - a.correct, bm = b.questions - b.correct;
    if (am !== bm) return am < bm;
    if (a.totalTime !== b.totalTime) return a.totalTime < b.totalTime;
    return a.avgReaction < b.avgReaction;
  }
  const localBest = m => history.filter(r => r.mode === m).reduce((b, r) => (better(r, b) ? r : b), null);

  function record(run) {
    const prevBest = localBest(run.mode);
    const pb = better(run, prevBest);
    history.unshift(run); history = history.slice(0, 1000); store.set("powDG_history", history);
    paintMine();
    if (!me.name) { askName(() => record2(run, pb)); return; }
    record2(run, pb);
  }

  async function record2(run, pb) {
    showResult(run, pb, "Saving your score online…");
    const msg = await save(run);
    showResult(run, pb, msg);
    showBoard(run.mode, true);
  }

  async function save(run) {
    try {
      const body = JSON.stringify({ playerId: me.id, name: me.name, initials: me.name.slice(0, 3).toUpperCase(),
        mode: run.mode, correct: run.correct, questions: run.questions,
        totalTime: Math.round(run.totalTime * 1000) / 1000, avgReaction: Math.round(run.avgReaction * 1000) / 1000 });
      // sent as plain text so the browser makes a simple request (no pre-flight check)
      const r = await fetch(API + "/saveScore", { method: "POST", headers: { "Content-Type": "text/plain;charset=utf-8" }, body });
      if (!r.ok) { const j = await r.json().catch(() => ({})); return "Not saved online: " + (j.error || "the score service is unavailable") + ". It is kept on this device."; }
      return "Saved to the online leaderboard.";
    } catch { return "Couldn't reach the score service. Your run is kept on this device."; }
  }

  function showResult(run, pb, note) {
    const wrong = run.questions - run.correct;
    const head = run.mode === "infinite" ? `${run.correct} correct in a row` : `${run.correct} / ${run.questions} correct`;
    const share = `I scored ${run.mode === "infinite" ? run.correct + " in a row on Endless" : run.correct + "/" + run.questions + " in " + fmt(run.totalTime) + " on " + MODES[run.mode].label.replace(" · ", " ")} in the Decision Game. Can you beat it?`;
    ui.result.innerHTML = `
      <div class="dg-result-head">${pb ? '<span class="dg-pb">New personal best</span>' : ""}<strong>${esc(head)}</strong></div>
      <dl class="dg-facts"><div><dt>Mistakes</dt><dd>${wrong}</dd></div><div><dt>Total time</dt><dd>${fmt(run.totalTime)}</dd></div>
      <div><dt>Average answer</dt><dd>${fmt(run.avgReaction)}</dd></div></dl>
      <p class="muted dg-note" role="status">${esc(note || "")}</p>
      ${MODES[run.mode].ranked ? `<div class="dg-result-actions"><button class="btn btn-door share-btn" type="button" data-url="${location.origin + location.pathname}" data-text="${esc(share)}">Challenge a friend</button>
      <a class="btn btn-outline" href="?player=${encodeURIComponent(me.id)}#player">My scores</a></div>` : ""}`;
    ui.result.hidden = false;
    wireShare(ui.result);
  }

  function wireShare(root) {
    root.querySelectorAll(".share-btn").forEach(btn => {
      if (btn.dataset.wired) return; btn.dataset.wired = "1";
      const label = btn.textContent;
      btn.addEventListener("click", async () => {
        const url = btn.dataset.url, text = btn.dataset.text || "";
        if (navigator.share) { try { await navigator.share({ title: document.title, text, url }); return; } catch (e) { if (e && e.name === "AbortError") return; } }
        try { await navigator.clipboard.writeText(text + " " + url); btn.textContent = "Copied"; } catch { btn.textContent = "Couldn't copy"; }
        setTimeout(() => (btn.textContent = label), 2000);
      });
    });
  }

  // ---------------------------------------------------------------- name
  function askName(then) {
    const dlg = $("dg-name");
    const input = $("dg-name-input");
    input.value = me.name || "";
    dlg.hidden = false;
    setTimeout(() => input.focus(), 30);
    const done = e => {
      e && e.preventDefault();
      const v = input.value.replace(/[<>"'`\\]/g, "").replace(/\s+/g, " ").trim().slice(0, 16);
      if (v.length < 2) { $("dg-name-note").textContent = "Please use at least 2 characters."; return; }
      me.name = v; store.set("powDG_player", me);
      dlg.hidden = true; $("dg-name-form").onsubmit = null; $("dg-name-skip").onclick = null;
      paintMe();
      then && then();
    };
    $("dg-name-form").onsubmit = done;
    $("dg-name-skip").onclick = () => { dlg.hidden = true; if (then) showResult(history[0], false, "Not saved online, because no name was given. It is kept on this device."); };
  }
  function paintMe() { $("dg-me").textContent = me.name || "not set yet"; }

  // ---------------------------------------------------------------- leaderboards
  let boardMode = BOARD_MODES.includes(mode) ? mode : "short", boardView = "best";
  const cols = m => m === "infinite" ? ["Correct", "Avg", "Total"] : ["Mistakes", "Total", "Avg"];
  const cells = r => r.mode === "infinite" || boardMode === "infinite"
    ? [r.correct, fmt(r.avgReaction), fmt(r.totalTime)] : [r.questions - r.correct, fmt(r.totalTime), fmt(r.avgReaction)];

  async function getJSON(path) {
    const r = await fetch(API + path, { cache: "no-store" });
    const j = await r.json().catch(() => ({}));
    return { ok: r.ok, status: r.status, j };
  }

  async function detect() {
    if (online !== null) return online;
    try { const p = await getJSON("/ping"); online = p.ok && p.j.version >= 2 ? 2 : 1; }
    catch { online = 0; }
    document.querySelectorAll("[data-needs-v2]").forEach(e => (e.hidden = online !== 2));
    return online;
  }

  async function showBoard(m, fresh) {
    boardMode = m;
    document.querySelectorAll("[data-board]").forEach(b => b.setAttribute("aria-pressed", String(b.dataset.board === m)));
    document.querySelectorAll("[data-view]").forEach(b => b.setAttribute("aria-pressed", String(b.dataset.view === boardView)));
    const tbody = $("dg-board-body"), note = $("dg-board-note");
    $("dg-board-head").innerHTML = `<th>#</th><th>Player</th>${cols(m).map(c => `<th class="num">${c}</th>`).join("")}<th class="num">Date</th>`;
    tbody.innerHTML = `<tr><td colspan="6" class="muted">Loading…</td></tr>`;
    const v = await detect();
    if (v === 0) { tbody.innerHTML = `<tr><td colspan="6" class="muted">The online leaderboard can't be reached right now.</td></tr>`; return; }
    const view = v === 2 ? boardView : "best";
    try {
      const { ok, j } = await getJSON(view === "all" ? `/runs?mode=${m}&limit=100` : `/leaderboard?mode=${m}`);
      if (!ok) throw 0;
      const rows = j.results || [];
      if (!rows.length) { tbody.innerHTML = `<tr><td colspan="6" class="muted">No scores yet. Be the first.</td></tr>`; }
      else tbody.innerHTML = rows.map((r, i) => {
        const mine = r.playerId && r.playerId === me.id;
        const who = r.playerId && v === 2 ? `<a href="?player=${encodeURIComponent(r.playerId)}#player">${esc(r.name)}</a>` : esc(r.name || r.initials);
        return `<tr${mine ? ' class="mine"' : ""}><td>${view === "all" ? "" : (r.rank || i + 1)}</td><td>${who}${mine ? ' <span class="tag">you</span>' : ""}</td>${cells({ ...r, mode: m }).map(c => `<td class="num">${c}</td>`).join("")}<td class="num">${r.date ? day(r.date) : ""}</td></tr>`;
      }).join("");
      note.textContent = view === "all" ? "Every run, newest first." :
        m === "infinite" ? "Each player's best run. Ranked by most correct, then fastest average answer." :
        "Each player's best run. Ranked by fewest mistakes, then fastest total time.";
    } catch { tbody.innerHTML = `<tr><td colspan="6" class="muted">The leaderboard couldn't be loaded. Try again in a minute.</td></tr>`; }
  }

  // ---------------------------------------------------------------- this device and player pages
  function paintMine() {
    const list = $("dg-mine");
    const bests = BOARD_MODES.map(m => [m, localBest(m)]).filter(([, b]) => b);
    $("dg-mine-best").innerHTML = bests.length ? bests.map(([m, b]) => `<div class="card dg-best"><span class="eyebrow muted" style="font-size:12px">${MODES[m].label}</span>
      <strong class="h-md" style="font-family:var(--display)">${m === "infinite" ? b.correct + " in a row" : b.correct + " / " + b.questions}</strong>
      <span class="muted">${fmt(b.totalTime)} total · ${fmt(b.avgReaction)} average</span></div>`).join("") : `<p class="muted">Finish a Short, Long or Endless run and your best scores appear here.</p>`;
    list.innerHTML = history.slice(0, 50).map(r => `<tr><td>${MODES[r.mode].label}</td>${[r.mode === "infinite" ? r.correct + " in a row" : (r.questions - r.correct) + (r.questions - r.correct === 1 ? " mistake" : " mistakes"), fmt(r.totalTime), fmt(r.avgReaction)].map(c => `<td class="num">${c}</td>`).join("")}<td class="num">${day(r.date)}</td></tr>`).join("")
      || `<tr><td colspan="5" class="muted">No runs yet.</td></tr>`;
  }

  async function showPlayer(id) {
    const box = $("player"); box.hidden = false;
    const body = $("dg-player-body");
    body.innerHTML = `<p class="muted">Loading…</p>`;
    const v = await detect();
    if (v !== 2) { body.innerHTML = `<p class="muted">Player pages will appear once the online score service is updated.</p>`; return; }
    try {
      const { ok, j } = await getJSON(`/player?id=${encodeURIComponent(id)}`);
      if (!ok) throw 0;
      const name = j.player.name || "Player";
      $("dg-player-name").textContent = name + (id === me.id ? " (you)" : "");
      const bests = BOARD_MODES.filter(m => j.bests[m]).map(m => { const b = j.bests[m];
        return `<div class="card dg-best"><span class="eyebrow muted" style="font-size:12px">${MODES[m].label}${b.rank ? ` · rank ${b.rank} of ${b.players}` : ""}</span>
        <strong class="h-md" style="font-family:var(--display)">${m === "infinite" ? b.correct + " in a row" : b.correct + " / " + b.questions}</strong>
        <span class="muted">${fmt(b.totalTime)} total · ${fmt(b.avgReaction)} average · ${day(b.date)}</span></div>`; }).join("");
      const runs = (j.runs || []).map(r => `<tr><td>${MODES[r.mode] ? MODES[r.mode].label : r.mode}</td>${[r.mode === "infinite" ? r.correct + " in a row" : (r.questions - r.correct) + (r.questions - r.correct === 1 ? " mistake" : " mistakes"), fmt(r.totalTime), fmt(r.avgReaction)].map(c => `<td class="num">${c}</td>`).join("")}<td class="num">${day(r.date)}</td></tr>`).join("");
      body.innerHTML = `<div class="grid grid-3">${bests || '<p class="muted">No scores yet.</p>'}</div>
        <h3 class="h-md" style="margin-top:28px">Every run (${(j.runs || []).length})</h3>
        <div class="table-wrap"><table class="dg-table"><thead><tr><th>Mode</th><th class="num">Result</th><th class="num">Total</th><th class="num">Average</th><th class="num">Date</th></tr></thead><tbody>${runs || '<tr><td colspan="5" class="muted">No runs yet.</td></tr>'}</tbody></table></div>
        <div class="actions" style="margin-top:20px"><button class="btn btn-door share-btn" type="button" data-url="${location.origin + location.pathname}?player=${encodeURIComponent(id)}#player" data-text="${esc(name)}'s scores in the Decision Game">Share this page</button></div>`;
      wireShare(body);
    } catch { body.innerHTML = `<p class="muted">This player's scores couldn't be loaded.</p>`; }
  }

  // ---------------------------------------------------------------- wiring
  document.querySelectorAll("[data-mode]").forEach(b => b.addEventListener("click", () => setMode(b.dataset.mode)));
  document.querySelectorAll("[data-board]").forEach(b => b.addEventListener("click", () => showBoard(b.dataset.board)));
  document.querySelectorAll("[data-view]").forEach(b => b.addEventListener("click", () => { boardView = b.dataset.view; showBoard(boardMode); }));
  ui.start.addEventListener("click", begin);
  ui.yes.addEventListener("click", () => answer(true));
  ui.no.addEventListener("click", () => answer(false));
  $("dg-rename").addEventListener("click", () => askName(null));
  $("dg-sound").checked = store.get("powDG_sound", true);
  $("dg-sound").addEventListener("change", e => store.set("powDG_sound", e.target.checked));
  document.addEventListener("keydown", e => {
    if (!$("dg-name").hidden || e.target.closest("input, textarea")) return;
    const running = s && s.running;
    if (running && (e.key === "ArrowRight" || e.key === "j" || e.key === "J")) { e.preventDefault(); answer(true); }
    else if (running && (e.key === "ArrowLeft" || e.key === "f" || e.key === "F")) { e.preventDefault(); answer(false); }
    else if ((e.key === " " || e.key === "Enter") && e.target === document.body) { e.preventDefault(); begin(); }
  });
  // load every picture before play, so answer times measure the player, not the network
  let loaded = 0;
  ui.start.disabled = true; ui.start.textContent = "Loading pictures…";
  ITEMS.forEach(it => { const im = new Image(); im.onload = im.onerror = () => { if (++loaded === ITEMS.length) { ui.start.disabled = false; if (!s) ui.start.textContent = "Start"; } }; im.src = it.url; });

  paintMe(); paintMine(); setMode(mode);
  if (!BOARD_MODES.includes(mode)) showBoard(boardMode);
  const pid = new URLSearchParams(location.search).get("player");
  if (pid) showPlayer(pid).then(() => $("player").scrollIntoView({ block: "start" }));
})();
