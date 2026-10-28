/* People of the World — The Focus Game
   A plus sign appears: press as fast as you can. A plus inside a circle: hold back and don't press. */
(() => {
  const G = window.POWG, $ = id => document.getElementById(id), esc = G.esc, fmt = G.fmt;
  const MODES = {
    daily: { label: "Daily", trials: 30, ranked: true, daily: true },
    practice: { label: "Practice", trials: Infinity, ranked: false },
    endless: { label: "Endless", trials: Infinity, ranked: true, lives: 3 }
  };
  const NOGO = 0.25;                    // one sign in four has a circle around it
  const WAIT_MIN = 700, WAIT_MAX = 2300; // the pause before each sign, so it can't be predicted
  const WINDOW_START = 1000, WINDOW_MIN = 450;
  let mode = G.store.get("powFG_mode", "daily"); if (!MODES[mode]) mode = "daily";
  let history = G.store.get("powFG_history", []);
  let s = null, timer = null;
  const ui = { stage: $("fg-stage"), sign: $("fg-sign"), msg: $("fg-msg"), start: $("fg-start"), press: $("fg-press"),
               trial: $("fg-trial"), hits: $("fg-hits"), bad: $("fg-bad"), avg: $("fg-avg"), lives: $("fg-lives"), win: $("fg-window"), result: $("fg-result") };
  const rand = () => (s && s.R ? s.R() : Math.random());

  function setMode(m) {
    if (s && s.running) stop(true);
    mode = m; G.store.set("powFG_mode", m);
    document.querySelectorAll("[data-mode]").forEach(b => b.setAttribute("aria-pressed", String(b.dataset.mode === m)));
    idle(); showBoard(m);
  }
  function idle() {
    clearTimeout(timer); s = null;
    ui.sign.className = "fg-sign"; ui.stage.classList.remove("is-running", "flash-ok", "flash-bad");
    ui.msg.textContent = MODES[mode].daily ? `Daily Challenge #${G.dayNumber()}: 30 signs, the same for everyone today.` : mode === "endless" ? "The signs speed up. Three mistakes and the run ends." : "Practise as long as you like. Nothing is recorded.";
    ui.start.textContent = "Start"; ui.press.disabled = true; paint();
  }
  function paint() {
    ui.trial.textContent = s ? `${s.n} / ${isFinite(MODES[mode].trials) ? MODES[mode].trials : "∞"}` : `0 / ${isFinite(MODES[mode].trials) ? MODES[mode].trials : "∞"}`;
    ui.hits.textContent = s ? s.hits : 0; ui.bad.textContent = s ? s.misses + s.falseAlarms + s.early : 0;
    ui.avg.textContent = s && s.hits ? fmt(s.rt / s.hits) : "0.00s";
    ui.lives.textContent = s && MODES[mode].lives ? "♥".repeat(Math.max(0, MODES[mode].lives - (s.misses + s.falseAlarms + s.early))) : "–";
    ui.win.textContent = s ? (s.window / 1000).toFixed(2) + "s to respond" : (WINDOW_START / 1000).toFixed(2) + "s to respond";
  }
  function begin() {
    if (s && s.running) { stop(true); return; }
    ui.result.hidden = true;
    s = { running: true, n: 0, hits: 0, misses: 0, falseAlarms: 0, early: 0, rt: 0, window: WINDOW_START, phase: "wait", t0: performance.now(), marks: [],
          R: MODES[mode].daily ? G.dailyRng("focus") : null };
    ui.start.textContent = "Stop"; ui.press.disabled = false; ui.stage.classList.add("is-running");
    ui.msg.textContent = "Watch the centre.";
    paint(); wait();
  }
  function wait() {
    if (!s.running) return;
    if (s.n >= MODES[mode].trials) return stop(false);
    s.phase = "wait"; ui.sign.className = "fg-sign";
    const d = WAIT_MIN + rand() * (WAIT_MAX - WAIT_MIN);
    s.nogo = rand() < NOGO;
    timer = setTimeout(show, d);
  }
  function show() {
    s.phase = "sign"; s.shown = performance.now();
    ui.sign.className = "fg-sign is-on" + (s.nogo ? " is-nogo" : "");
    timer = setTimeout(expire, s.window);
  }
  function result(good, kind) {
    s.marks.push(good); s.n++;
    if (good) G.sfx.right(); else G.sfx.wrong();
    ui.stage.classList.remove("flash-ok", "flash-bad"); void ui.stage.offsetWidth; ui.stage.classList.add(good ? "flash-ok" : "flash-bad");
    ui.msg.textContent = { hit: "Good.", hold: "Well held.", miss: "Too slow.", false: "That one had a circle: hold back.", early: "Too soon: wait for the sign." }[kind];
    if (mode === "endless" && good && kind === "hit" && s.hits % 10 === 0) s.window = Math.max(WINDOW_MIN, s.window - 50);
    paint();
    const mistakes = s.misses + s.falseAlarms + s.early;
    if (MODES[mode].lives && mistakes >= MODES[mode].lives) { timer = setTimeout(() => stop(false, "Out of chances"), 700); return; }
    timer = setTimeout(wait, 450);
  }
  function expire() {
    if (s.phase !== "sign") return;
    s.phase = "done"; ui.sign.className = "fg-sign";
    if (s.nogo) result(true, "hold"); else { s.misses++; result(false, "miss"); }
  }
  function press() {
    if (!s || !s.running) return;
    if (s.phase === "wait") { clearTimeout(timer); s.early++; s.phase = "done"; result(false, "early"); return; }
    if (s.phase !== "sign") return;
    clearTimeout(timer); s.phase = "done"; ui.sign.className = "fg-sign";
    if (s.nogo) { s.falseAlarms++; result(false, "false"); }
    else { s.hits++; s.rt += (performance.now() - s.shown) / 1000; result(true, "hit"); }
  }
  function stop(manual, why) {
    if (!s) return;
    clearTimeout(timer); const was = s.running; s.running = false;
    ui.start.textContent = "Play again"; ui.press.disabled = true; ui.stage.classList.remove("is-running"); ui.sign.className = "fg-sign";
    if (!was) return idle();
    G.sfx.end();
    const mistakes = s.misses + s.falseAlarms + s.early;
    const run = { game: "focus", mode, board: mode, questions: s.n, correct: s.n - mistakes, hits: s.hits, misses: s.misses, falseAlarms: s.falseAlarms, early: s.early,
                  avgReaction: s.hits ? s.rt / s.hits : 0, totalTime: (performance.now() - s.t0) / 1000, date: new Date().toISOString(), marks: s.marks.slice() };
    ui.msg.textContent = manual ? "Stopped." : (why || "Finished.");
    const m = MODES[mode];
    if (!m.ranked || manual || !run.hits) return showResult(run, null, mode === "practice" ? "Practice runs aren't recorded." : manual ? "Stopped early, so it isn't recorded." : "No hits this time, so it isn't recorded.");
    if (m.daily) {
      if (G.dailyDone("focus")) { run.dailyRepeat = true; return showResult(run, null, "Today's challenge is already recorded: only your first run counts. A new one arrives tomorrow."); }
      run.day = G.today(); run.number = G.dayNumber();
      G.markDaily("focus", { correct: run.correct, questions: run.questions, avgReaction: run.avgReaction, marks: run.marks });
    }
    record(run);
  }

  // ---------------------------------------------------------------- results: daily ranks fewest mistakes then fastest; endless ranks most correct then fastest
  function better(a, b) {
    if (!b) return true;
    if (a.mode === "daily") { const am = a.questions - a.correct, bm = b.questions - b.correct; return am !== bm ? am < bm : a.avgReaction < b.avgReaction; }
    return a.correct !== b.correct ? a.correct > b.correct : a.avgReaction < b.avgReaction;
  }
  const localBest = m => history.filter(r => r.mode === m).reduce((b, r) => (better(r, b) ? r : b), null);
  function record(run) {
    const pb = better(run, localBest(run.mode));
    history.unshift(run); history = history.slice(0, 500); G.store.set("powFG_history", history); paintMine();
    const go = async () => { showResult(run, pb, "Saving your result…"); const r = await G.save(run); showResult(run, pb, r.msg); showBoard(run.mode); };
    if (!G.me().name) G.askName(go, () => showResult(run, pb, "Not saved online, because no name was given. It is kept on this device.")); else go();
  }
  function showResult(run, pb, note) {
    const mistakes = run.questions - run.correct;
    const head = run.mode === "endless" ? `${run.correct} in a row before ${MODES.endless.lives} mistakes` : `${run.correct} / ${run.questions} right`;
    const daily = run.mode === "daily" && !run.dailyRepeat ? `Focus Game #${run.number} · ${run.correct}/${run.questions} · ${fmt(run.avgReaction)} avg\n${G.grid(run.marks)}` : null;
    const text = daily || `I reached ${run.correct} in the Focus Game, averaging ${fmt(run.avgReaction)}. Can you beat it?`;
    ui.result.innerHTML = `<div class="dg-result-head">${pb ? '<span class="dg-pb">New personal best</span>' : ""}<strong>${esc(head)}</strong></div>
      <dl class="dg-facts"><div><dt>Average reaction</dt><dd>${fmt(run.avgReaction)}</dd></div><div><dt>Pressed on a circle</dt><dd>${run.falseAlarms}</dd></div>
      <div><dt>Too slow</dt><dd>${run.misses}</dd></div><div><dt>Too soon</dt><dd>${run.early}</dd></div></dl>
      ${daily ? `<pre class="g-grid">${esc(daily)}</pre><p class="muted dg-note">Streak: ${G.streak("focus")} day${G.streak("focus") === 1 ? "" : "s"}.</p>` : ""}
      <p class="muted dg-note" role="status">${esc(note || "")}</p>
      <div class="dg-result-actions">${MODES[run.mode].ranked && !run.dailyRepeat ? `<button class="btn btn-door" type="button" id="fg-share">${daily ? "Share your result" : "Challenge a friend"}</button>` : ""}<a class="btn btn-outline" href="play.html">More games</a></div>
      ${G.teaching()}`;
    ui.result.hidden = false;
    const b = $("fg-share"); if (b) b.addEventListener("click", () => G.share(text, location.origin + location.pathname, b));
    if (mistakes === 0 && run.mode === "daily") ui.msg.textContent = "A perfect round.";
  }
  async function showBoard(m) {
    const body = $("fg-board"), note = $("fg-board-note");
    if (!MODES[m].ranked) m = "daily";
    document.querySelectorAll("[data-board]").forEach(b => b.setAttribute("aria-pressed", String(b.dataset.board === m)));
    body.innerHTML = `<tr><td colspan="5" class="muted">Loading…</td></tr>`;
    const r = await G.board("focus-" + m, m === "daily" ? `&day=${G.today()}` : "");
    if (r.soon) { body.innerHTML = `<tr><td colspan="5" class="muted">The online leaderboard for the Focus Game opens soon. Your results, bests and streak are kept on this device.</td></tr>`; note.textContent = ""; return; }
    if (r.error) { body.innerHTML = `<tr><td colspan="5" class="muted">The leaderboard can't be reached right now.</td></tr>`; return; }
    body.innerHTML = r.rows.length ? r.rows.map((x, i) => `<tr${x.playerId === G.me().id ? ' class="mine"' : ""}><td>${x.rank || i + 1}</td><td>${esc(x.name || x.initials)}</td><td class="num">${x.correct}</td><td class="num">${fmt(x.avgReaction)}</td><td class="num">${G.day(x.date)}</td></tr>`).join("")
      : `<tr><td colspan="5" class="muted">No scores yet. Be the first.</td></tr>`;
    note.textContent = m === "daily" ? "Ranked by fewest mistakes, then fastest reaction." : "Ranked by most right, then fastest reaction.";
  }
  function paintMine() {
    const st = G.streak("focus"), done = G.dailyDone("focus");
    $("fg-daily-status").textContent = done ? `Today's challenge #${G.dayNumber()}: ${done.correct}/${done.questions}. Streak: ${st} day${st === 1 ? "" : "s"}.` : `Today's challenge #${G.dayNumber()} is waiting.${st ? ` Streak: ${st} day${st === 1 ? "" : "s"}.` : ""}`;
    const bests = ["daily", "endless"].map(m => [m, localBest(m)]).filter(([, b]) => b);
    $("fg-mine").innerHTML = bests.length ? bests.map(([m, b]) => `<div class="card dg-best"><span class="eyebrow muted" style="font-size:12px">Best · ${MODES[m].label}</span><strong class="h-md" style="font-family:var(--display)">${m === "endless" ? b.correct + " in a row" : b.correct + " / " + b.questions}</strong><span class="muted">${fmt(b.avgReaction)} average reaction · ${G.day(b.date)}</span></div>`).join("")
      : `<p class="muted">Finish a Daily or Endless run and your bests appear here.</p>`;
  }

  // ---------------------------------------------------------------- wiring: space bar, or the big button on a phone
  document.querySelectorAll("[data-mode]").forEach(b => b.addEventListener("click", () => setMode(b.dataset.mode)));
  document.querySelectorAll("[data-board]").forEach(b => b.addEventListener("click", () => showBoard(b.dataset.board)));
  ui.start.addEventListener("click", begin);
  ui.press.addEventListener("pointerdown", e => { e.preventDefault(); press(); });
  document.addEventListener("keydown", e => {
    if (e.target.closest("input, textarea") || !$("g-name").hidden) return;
    if (e.key === " " || e.code === "Space") { e.preventDefault(); if (s && s.running) press(); else if (e.target === document.body) begin(); }
  });
  const snd = $("g-sound"); snd.checked = G.store.get("powDG_sound", true); snd.addEventListener("change", e => G.store.set("powDG_sound", e.target.checked));
  paintMine(); setMode(mode);
})();
