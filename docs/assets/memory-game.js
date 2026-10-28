/* People of the World — The Memory Game
   Study a set of letters, then numbers, then shapes. Then say which one is missing, or which one is new. */
(() => {
  const G = window.POWG, $ = id => document.getElementById(id), esc = G.esc, fmt = G.fmt;
  const LETTERS = "ABCDEFGHJKLMNPRSTUVWXYZ".split("");          // no I, O or Q: too easy to confuse with 1, 0
  const DIGITS = "23456789".split("");                          // no 0 or 1, for the same reason
  const SHAPES = ["circle", "triangle", "square", "diamond", "star", "cross", "hexagon", "heart"];
  const SHAPE_NAMES = { circle: "circle", triangle: "triangle", square: "square", diamond: "diamond", star: "star", cross: "cross", hexagon: "hexagon", heart: "heart" };
  const MODES = {
    daily: { label: "Daily", rounds: 10, lives: Infinity, ranked: true, daily: true },
    practice: { label: "Practice", rounds: Infinity, lives: Infinity, ranked: false },
    endless: { label: "Endless", rounds: Infinity, lives: 3, ranked: true }
  };
  let mode = G.store.get("powMG_mode", "daily"); if (!MODES[mode]) mode = "daily";
  let history = G.store.get("powMG_history", []);
  let s = null, timers = [];
  const ui = { stage: $("mg-stage"), msg: $("mg-msg"), items: $("mg-items"), choices: $("mg-choices"), start: $("mg-start"),
               level: $("mg-level"), lives: $("mg-lives"), ok: $("mg-ok"), bad: $("mg-bad"), result: $("mg-result") };

  // ---------------------------------------------------------------- what a level looks like
  // levels 1–4 letters, 5–8 letters and numbers, 9 and up letters, numbers and shapes; the set grows by one every two levels
  const sizeFor = level => Math.min(3 + Math.floor((level - 1) / 2), 12);
  const poolFor = level => level <= 4 ? LETTERS : level <= 8 ? LETTERS.concat(DIGITS) : LETTERS.concat(DIGITS, SHAPES.map(x => "#" + x));
  const studyMs = n => 900 + n * 650;
  const shapeSVG = name => {
    const p = { circle: '<circle cx="20" cy="20" r="15"/>', triangle: '<path d="M20 4 37 34H3z"/>', square: '<rect x="6" y="6" width="28" height="28"/>',
                diamond: '<path d="M20 3 37 20 20 37 3 20z"/>', star: '<path d="M20 3l5 11 12 1-9 8 3 12-11-6-11 6 3-12-9-8 12-1z"/>',
                cross: '<path d="M15 4h10v11h11v10H25v11H15V25H4V15h11z"/>', hexagon: '<path d="M11 4h18l9 16-9 16H11L2 20z"/>',
                heart: '<path d="M20 35S4 25 4 14a8 8 0 0 1 16-3 8 8 0 0 1 16 3c0 11-16 21-16 21z"/>' }[name];
    return `<svg viewBox="0 0 40 40" width="40" height="40" aria-hidden="true" fill="currentColor">${p}</svg>`;
  };
  const label = x => x.startsWith("#") ? SHAPE_NAMES[x.slice(1)] : x;
  const tile = (x, extra = "") => `<span class="mg-tile${x.startsWith("#") ? " mg-shape" : ""}"${extra} aria-label="${esc(label(x))}">${x.startsWith("#") ? shapeSVG(x.slice(1)) : esc(x)}</span>`;
  const rand = () => (s && s.R ? s.R() : Math.random());
  const pick = (arr, n, not = []) => { const a = arr.filter(x => !not.includes(x)); for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(rand() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a.slice(0, n); };

  // ---------------------------------------------------------------- flow
  function setMode(m) {
    if (s && s.running) stop(true);
    mode = m; G.store.set("powMG_mode", m);
    document.querySelectorAll("[data-mode]").forEach(b => b.setAttribute("aria-pressed", String(b.dataset.mode === m)));
    idle(); showBoard(m);
  }
  function clear() { timers.forEach(clearTimeout); timers = []; }
  function idle() {
    clear(); s = null;
    ui.items.innerHTML = ""; ui.choices.innerHTML = "";
    ui.msg.textContent = MODES[mode].daily ? `Daily Challenge #${G.dayNumber()}: ten rounds, the same for everyone today.` : mode === "endless" ? "Climb as high as you can. Three lives." : "Practise as long as you like. Nothing is recorded.";
    ui.start.textContent = "Start"; paintStatus();
  }
  function paintStatus() {
    ui.level.textContent = s ? s.level : 1;
    ui.lives.textContent = s && isFinite(MODES[mode].lives) ? "♥".repeat(s.lives) : "–";
    ui.ok.textContent = s ? s.ok : 0; ui.bad.textContent = s ? s.bad : 0;
  }
  function begin() {
    if (s && s.running) { stop(true); return; }
    ui.result.hidden = true;
    s = { running: true, level: 1, round: 0, ok: 0, bad: 0, lives: MODES[mode].lives, react: 0, t0: performance.now(), marks: [],
          R: MODES[mode].daily ? G.dailyRng("memory") : null };
    ui.start.textContent = "Stop";
    round();
  }
  function round() {
    if (!s.running) return;
    const m = MODES[mode];
    if (s.round >= m.rounds) return stop(false);
    if (m.daily) s.level = s.round + 1;                                 // the daily climbs one level a round, so everyone sees the same sets
    const n = sizeFor(s.level), pool = poolFor(s.level);
    const set = pick(pool, n);
    const missing = rand() < 0.5;                                     // half the rounds: what's missing? the other half: what's new?
    s.q = { set, missing };
    ui.choices.innerHTML = "";
    ui.msg.textContent = `Level ${s.level}: remember these ${n}.`;
    ui.items.innerHTML = set.map(x => tile(x)).join("");
    ui.stage.classList.add("is-study");
    paintStatus();
    timers.push(setTimeout(() => {
      ui.items.innerHTML = ""; ui.msg.textContent = "…";
      timers.push(setTimeout(ask, 700));
    }, studyMs(n)));
  }
  function ask() {
    ui.stage.classList.remove("is-study");
    const { set, missing } = s.q, pool = poolFor(s.level);
    if (missing) {
      const gone = set[Math.floor(rand() * set.length)];
      const rest = pick(set.filter(x => x !== gone), set.length - 1);
      const options = pick([gone, ...pick(pool, 3, set)], 4);
      s.q.answer = gone;
      ui.msg.textContent = "Which one is missing?";
      ui.items.innerHTML = rest.map(x => tile(x)).join("");
      ui.choices.innerHTML = options.map(x => `<button type="button" class="mg-choice" data-v="${esc(x)}">${tile(x)}</button>`).join("");
    } else {
      const extra = pick(pool, 1, set)[0];
      const shown = pick([...set, extra], set.length + 1);
      s.q.answer = extra;
      ui.msg.textContent = "Which one is new?";
      ui.items.innerHTML = "";
      ui.choices.innerHTML = shown.map(x => `<button type="button" class="mg-choice" data-v="${esc(x)}">${tile(x)}</button>`).join("");
    }
    s.shown = performance.now(); s.live = true;
    ui.choices.querySelectorAll(".mg-choice").forEach(b => b.addEventListener("click", () => choose(b.dataset.v, b)));
  }
  function choose(v, btn) {
    if (!s || !s.live) return;
    s.live = false; s.round++;
    s.react += (performance.now() - s.shown) / 1000;
    const good = v === s.q.answer;
    s.marks.push(good);
    ui.choices.querySelectorAll(".mg-choice").forEach(b => { b.disabled = true; if (b.dataset.v === s.q.answer) b.classList.add("is-answer"); });
    if (good) { s.ok++; if (!MODES[mode].daily) s.level++; G.sfx.right(); btn.classList.add("is-right"); ui.msg.textContent = "Right."; }
    else { s.bad++; s.lives--; G.sfx.wrong(); btn.classList.add("is-wrong"); ui.msg.textContent = `It was ${label(s.q.answer)}.`; }
    paintStatus();
    if (isFinite(MODES[mode].lives) && s.lives <= 0) { timers.push(setTimeout(() => stop(false, "Out of lives"), 900)); return; }
    timers.push(setTimeout(round, 1100));
  }
  function stop(manual, why) {
    if (!s) return;
    clear(); const was = s.running; s.running = false; s.live = false;
    ui.start.textContent = "Play again";
    if (!was) return idle();
    G.sfx.end();
    const run = { game: "memory", mode, board: mode, questions: s.round, correct: s.ok, totalTime: (performance.now() - s.t0) / 1000,
                  avgReaction: s.round ? s.react / s.round : 0, date: new Date().toISOString(), marks: s.marks.slice() };
    ui.msg.textContent = manual ? "Stopped." : (why || "Finished.");
    const m = MODES[mode];
    if (!m.ranked || manual || !run.correct) return showResult(run, null, mode === "practice" ? "Practice runs aren't recorded." : manual ? "Stopped early, so it isn't recorded." : "No correct answers this time, so it isn't recorded.");
    if (m.daily) {
      if (G.dailyDone("memory")) { run.dailyRepeat = true; return showResult(run, null, "Today's challenge is already recorded: only your first run counts. A new one arrives tomorrow."); }
      run.day = G.today(); run.number = G.dayNumber();
      G.markDaily("memory", { correct: run.correct, questions: run.questions, totalTime: run.totalTime, marks: run.marks });
    }
    record(run);
  }

  // ---------------------------------------------------------------- results
  const better = (a, b) => !b || a.correct > b.correct || (a.correct === b.correct && a.avgReaction < b.avgReaction);
  const localBest = m => history.filter(r => r.mode === m).reduce((b, r) => (better(r, b) ? r : b), null);
  function record(run) {
    const pb = better(run, localBest(run.mode));
    history.unshift(run); history = history.slice(0, 500); G.store.set("powMG_history", history); paintMine();
    const go = async () => { showResult(run, pb, "Saving your result…"); const r = await G.save(run); showResult(run, pb, r.msg); showBoard(run.mode); };
    if (!G.me().name) G.askName(go, () => showResult(run, pb, "Not saved online, because no name was given. It is kept on this device.")); else go();
  }
  function showResult(run, pb, note) {
    const head = run.mode === "endless" ? `Reached level ${run.correct + 1}` : `${run.correct} / ${run.questions} correct`;
    const daily = run.mode === "daily" && !run.dailyRepeat ? `Memory Game #${run.number} · ${run.correct}/${run.questions} · ${fmt(run.avgReaction)} avg\n${G.grid(run.marks)}` : null;
    const text = daily || (run.mode === "endless" ? `I reached level ${run.correct + 1} in the Memory Game. How far can you go?` : "Try the Memory Game.");
    ui.result.innerHTML = `<div class="dg-result-head">${pb ? '<span class="dg-pb">New personal best</span>' : ""}<strong>${esc(head)}</strong></div>
      <dl class="dg-facts"><div><dt>Correct</dt><dd>${run.correct}</dd></div><div><dt>Mistakes</dt><dd>${run.questions - run.correct}</dd></div><div><dt>Average answer</dt><dd>${fmt(run.avgReaction)}</dd></div></dl>
      ${daily ? `<pre class="g-grid">${esc(daily)}</pre><p class="muted dg-note">Streak: ${G.streak("memory")} day${G.streak("memory") === 1 ? "" : "s"}.</p>` : ""}
      <p class="muted dg-note" role="status">${esc(note || "")}</p>
      <div class="dg-result-actions">${MODES[run.mode].ranked && !run.dailyRepeat ? `<button class="btn btn-door" type="button" id="mg-share">${daily ? "Share your result" : "Challenge a friend"}</button>` : ""}<a class="btn btn-outline" href="play.html">More games</a></div>
      ${G.teaching()}`;
    ui.result.hidden = false;
    const b = $("mg-share"); if (b) b.addEventListener("click", () => G.share(text, location.origin + location.pathname, b));
  }
  async function showBoard(m) {
    const body = $("mg-board"), note = $("mg-board-note");
    if (!MODES[m].ranked) m = "daily";
    document.querySelectorAll("[data-board]").forEach(b => b.setAttribute("aria-pressed", String(b.dataset.board === m)));
    body.innerHTML = `<tr><td colspan="5" class="muted">Loading…</td></tr>`;
    const r = await G.board("memory-" + m, m === "daily" ? `&day=${G.today()}` : "");
    if (r.soon) { body.innerHTML = `<tr><td colspan="5" class="muted">The online leaderboard for the Memory Game opens soon. Your results, bests and streak are kept on this device.</td></tr>`; note.textContent = ""; return; }
    if (r.error) { body.innerHTML = `<tr><td colspan="5" class="muted">The leaderboard can't be reached right now.</td></tr>`; return; }
    body.innerHTML = r.rows.length ? r.rows.map((x, i) => `<tr${x.playerId === G.me().id ? ' class="mine"' : ""}><td>${x.rank || i + 1}</td><td>${esc(x.name || x.initials)}</td><td class="num">${x.correct}</td><td class="num">${fmt(x.avgReaction)}</td><td class="num">${G.day(x.date)}</td></tr>`).join("")
      : `<tr><td colspan="5" class="muted">No scores yet. Be the first.</td></tr>`;
    note.textContent = "Ranked by most correct, then fastest average answer.";
  }
  function paintMine() {
    const st = G.streak("memory"), done = G.dailyDone("memory");
    $("mg-daily-status").textContent = done ? `Today's challenge #${G.dayNumber()}: ${done.correct}/${done.questions}. Streak: ${st} day${st === 1 ? "" : "s"}.` : `Today's challenge #${G.dayNumber()} is waiting.${st ? ` Streak: ${st} day${st === 1 ? "" : "s"}.` : ""}`;
    const bests = ["daily", "endless"].map(m => [m, localBest(m)]).filter(([, b]) => b);
    $("mg-mine").innerHTML = bests.length ? bests.map(([m, b]) => `<div class="card dg-best"><span class="eyebrow muted" style="font-size:12px">Best · ${MODES[m].label}</span><strong class="h-md" style="font-family:var(--display)">${m === "endless" ? "Level " + (b.correct + 1) : b.correct + " / " + b.questions}</strong><span class="muted">${fmt(b.avgReaction)} average · ${G.day(b.date)}</span></div>`).join("")
      : `<p class="muted">Finish a Daily or Endless run and your bests appear here.</p>`;
  }

  // ---------------------------------------------------------------- wiring
  document.querySelectorAll("[data-mode]").forEach(b => b.addEventListener("click", () => setMode(b.dataset.mode)));
  document.querySelectorAll("[data-board]").forEach(b => b.addEventListener("click", () => showBoard(b.dataset.board)));
  ui.start.addEventListener("click", begin);
  const snd = $("g-sound"); snd.checked = G.store.get("powDG_sound", true); snd.addEventListener("change", e => G.store.set("powDG_sound", e.target.checked));
  paintMine(); setMode(mode);
})();
