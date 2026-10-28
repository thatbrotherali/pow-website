/* People of the World — shared pieces for the brain-training games:
   one player name across games, daily challenges (the same puzzle for everyone each day), streaks,
   sharing, the online score service, and a short line from the teachings after each round. */
window.POWG = (() => {
  const API = "https://shop.peopleoftheworld.net/_functions/decisionGame";
  const store = {
    get(k, d) { try { const v = localStorage.getItem(k); return v ? JSON.parse(v) : d; } catch { return d; } },
    set(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch {} }
  };
  const esc = s => String(s ?? "").replace(/[&<>"']/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  const fmt = s => (Math.round(s * 100) / 100).toFixed(2) + "s";
  const day = d => { try { return new Date(d).toLocaleDateString(undefined, { day: "numeric", month: "short", year: "numeric" }); } catch { return ""; } };

  // ---------------------------------------------------------------- one player across every game (shared with the Decision Game)
  let me = store.get("powDG_player", null);
  if (!me || !me.id) {
    const rnd = (crypto.randomUUID ? crypto.randomUUID() : Date.now().toString(36) + Math.random().toString(36).slice(2)).replace(/[^a-zA-Z0-9]/g, "");
    me = { id: "p-" + rnd.slice(0, 24), name: "" };
    store.set("powDG_player", me);
  }
  const setName = n => { me.name = n; store.set("powDG_player", me); };

  // ---------------------------------------------------------------- daily challenge: the same puzzle for everyone, chosen by the date
  const pad = n => String(n).padStart(2, "0");
  const today = () => { const d = new Date(); return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}`; };
  const EPOCH = Date.UTC(2026, 9, 28);   // challenge #1 is 28 October 2026, the day the suite opened
  const dayNumber = (iso = today()) => { const [y, m, d] = iso.split("-").map(Number); return Math.floor((Date.UTC(y, m - 1, d) - EPOCH) / 864e5) + 1; };
  function hash(str) { let h = 1779033703 ^ str.length; for (let i = 0; i < str.length; i++) { h = Math.imul(h ^ str.charCodeAt(i), 3432918353); h = (h << 13) | (h >>> 19); } return h >>> 0; }
  function rng(seed) {   // mulberry32: a small, repeatable random generator
    let a = typeof seed === "number" ? seed : hash(seed);
    return () => { a |= 0; a = (a + 0x6D2B79F5) | 0; let t = Math.imul(a ^ (a >>> 15), 1 | a); t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; };
  }
  const dailyRng = game => rng(`pow-${game}-${today()}`);

  // a day's result is kept so the daily counts once; streaks are consecutive days with a daily played
  const dailyKey = game => `powG_daily_${game}`;
  const dailyDone = game => (store.get(dailyKey(game), {})[today()] || null);
  function markDaily(game, result) {
    const all = store.get(dailyKey(game), {});
    if (!all[today()]) { all[today()] = result; store.set(dailyKey(game), all); }
    const any = store.get("powG_days", {}); any[today()] = true; store.set("powG_days", any);
  }
  function streakFrom(days) {
    let n = 0; const d = new Date();
    const key = x => `${x.getFullYear()}-${pad(x.getMonth() + 1)}-${pad(x.getDate())}`;
    if (!days[key(d)]) d.setDate(d.getDate() - 1);   // today not played yet: the streak is still alive from yesterday
    while (days[key(d)]) { n++; d.setDate(d.getDate() - 1); }
    return n;
  }
  const streak = game => streakFrom(game ? store.get(dailyKey(game), {}) : store.get("powG_days", {}));

  // ---------------------------------------------------------------- a line from the teachings, one for each day
  const LINES = [
    ["The voice we call conscience may be far more than habit. Listen for it.", "seekers.html#why", "The Search for Meaning"],
    ["Seek love. Seek unity. Seek truth.", "ten-steps.html", "Ten steps for humanity"],
    ["Stillness is where the voice within is most easily heard.", "ten-steps.html", "Ten steps for humanity"],
    ["Growth must be intentional.", "ten-steps.html", "Ten steps for humanity"],
    ["Resentment binds you to the past. Forgiveness sets you free to move.", "ten-steps.html", "Ten steps for humanity"],
    ["Serving others is not a burden but a privilege.", "ten-steps.html", "Ten steps for humanity"],
    ["It takes courage to question what we were told, and courage to seek what is true.", "ten-steps.html", "Ten steps for humanity"],
    ["Almost every faith says a portion of the Creator lives within us.", "seekers.html#faiths", "The thread through every faith"],
    ["You are not alone. Help is always available to those who seek it.", "seekers.html#teachings", "The weekly teachings"],
    ["Every person counted, no person left behind.", "builders.html", "End Poverty by Design"],
    ["A clear mind makes better choices. Better choices make a better world.", "why.html", "Why it all connects"],
    ["Choose unity: it begins with how you treat the next person you meet.", "ten-steps.html", "Ten steps for humanity"]
  ];
  function teaching() {
    const [t, href, label] = LINES[((dayNumber() % LINES.length) + LINES.length) % LINES.length];
    return `<div class="g-thought"><p class="g-thought-text">“${esc(t)}”</p><p class="muted" style="margin:0;font-size:14px"><a href="${href}">${esc(label)} →</a></p></div>`;
  }

  // ---------------------------------------------------------------- sharing
  async function share(text, url, btn) {
    if (navigator.share) { try { await navigator.share({ title: document.title, text, url }); return; } catch (e) { if (e && e.name === "AbortError") return; } }
    const label = btn && btn.textContent;
    try { await navigator.clipboard.writeText(text + "\n" + url); if (btn) btn.textContent = "Copied"; } catch { if (btn) btn.textContent = "Couldn't copy"; }
    if (btn) setTimeout(() => (btn.textContent = label), 2000);
  }
  const grid = marks => marks.map(m => (m ? "🟩" : "🟥")).join("");

  // ---------------------------------------------------------------- online scores (the score service on the Wix site)
  // Games other than the Decision Game, and daily challenges, are saved online once the score service accepts them;
  // until then they are kept on this device, and the page says so.
  async function save(run) {
    try {
      const body = JSON.stringify({ playerId: me.id, name: me.name, initials: me.name.slice(0, 3).toUpperCase(), game: run.game || "decision",
        mode: run.board, day: run.day || null, correct: run.correct, questions: run.questions,
        totalTime: Math.round(run.totalTime * 1000) / 1000, avgReaction: Math.round(run.avgReaction * 1000) / 1000 });
      const r = await fetch(API + "/saveScore", { method: "POST", headers: { "Content-Type": "text/plain;charset=utf-8" }, body });
      if (r.ok) return { ok: true, msg: "Saved to the online leaderboard." };
      if (r.status === 400) return { ok: false, soon: true, msg: "The online leaderboard for this challenge opens soon. Your result is kept on this device." };
      return { ok: false, msg: "Not saved online: the score service is unavailable. It is kept on this device." };
    } catch { return { ok: false, msg: "Couldn't reach the score service. Your result is kept on this device." }; }
  }
  async function board(mode, extra = "") {
    try {
      const r = await fetch(`${API}/leaderboard?mode=${encodeURIComponent(mode)}${extra}`, { cache: "no-store" });
      const j = await r.json().catch(() => ({}));
      if (r.status === 400) return { soon: true, rows: [] };
      if (!r.ok) return { error: true, rows: [] };
      return { rows: j.results || [] };
    } catch { return { error: true, rows: [] }; }
  }

  // ---------------------------------------------------------------- the name prompt (markup: #g-name dialog on each game page)
  function askName(then, skip) {
    const dlg = document.getElementById("g-name"), input = document.getElementById("g-name-input"), note = document.getElementById("g-name-note");
    if (!dlg) { then && then(); return; }
    input.value = me.name || ""; note.textContent = ""; dlg.hidden = false; setTimeout(() => input.focus(), 30);
    document.getElementById("g-name-form").onsubmit = e => {
      e.preventDefault();
      const v = input.value.replace(/[<>"'`\\]/g, "").replace(/\s+/g, " ").trim().slice(0, 16);
      if (v.length < 2) { note.textContent = "Please use at least 2 characters."; return; }
      setName(v); dlg.hidden = true; paintName(); then && then();
    };
    document.getElementById("g-name-skip").onclick = () => { dlg.hidden = true; skip && skip(); };
  }
  function paintName() { document.querySelectorAll("[data-g-me]").forEach(e => (e.textContent = me.name || "not set yet")); }
  document.addEventListener("DOMContentLoaded", () => {
    paintName();
    document.querySelectorAll("[data-g-rename]").forEach(b => b.addEventListener("click", () => askName(null)));
  });

  // ---------------------------------------------------------------- sound
  let ctx = null;
  function tone(f, d, v, type = "sine") {
    const box = document.getElementById("g-sound");
    if (box && !box.checked) return;
    try {
      ctx = ctx || new (window.AudioContext || window.webkitAudioContext)();
      const o = ctx.createOscillator(), g = ctx.createGain();
      o.type = type; o.frequency.value = f; g.gain.value = v; o.connect(g); g.connect(ctx.destination); o.start(); o.stop(ctx.currentTime + d);
    } catch {}
  }
  const sfx = { beep: i => tone(600 + i * 80, 0.15, 0.2), go: () => tone(1000, 0.22, 0.25), right: () => tone(880, 0.12, 0.22),
                wrong: () => tone(260, 0.18, 0.18, "square"), end: () => { tone(900, 0.16, 0.2); setTimeout(() => tone(700, 0.18, 0.18), 180); } };

  return { API, store, esc, fmt, day, me: () => me, setName, askName, today, dayNumber, rng, dailyRng, dailyDone, markDaily, streak,
           teaching, share, grid, save, board, sfx };
})();
