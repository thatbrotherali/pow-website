/* People of the World — audiobook player.
   Plays a list of chapters one after another, with speed control, and remembers where you stopped (in this browser). */
(() => {
  const store = {
    get(k) { try { return JSON.parse(localStorage.getItem(k) || "null"); } catch { return null; } },
    set(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch {} }
  };
  const mmss = t => { t = Math.max(0, Math.floor(t || 0)); return Math.floor(t / 60) + ":" + String(t % 60).padStart(2, "0"); };
  let speed = store.get("powAB_speed") || 1;

  document.querySelectorAll(".ab").forEach(box => {
    const tracks = JSON.parse(box.dataset.tracks || "[]");
    if (!tracks.length) return;
    const key = "powAB_" + box.dataset.key;
    const audio = box.querySelector(".ab-audio"), now = box.querySelector(".ab-now");
    const links = [...box.querySelectorAll(".ab-ch")], resume = box.querySelector(".ab-resume");
    const sel = box.querySelector(".ab-speed select");
    let i = 0, pendingSeek = 0, lastSave = 0;

    function load(n, at, play) {
      i = Math.max(0, Math.min(tracks.length - 1, n));
      const t = tracks[i];
      audio.src = t.u; pendingSeek = at || 0;
      audio.playbackRate = speed;
      now.textContent = t.n + ". " + t.t;
      links.forEach((a, k) => { a.classList.toggle("is-current", k === i); if (k === i) a.setAttribute("aria-current", "true"); else a.removeAttribute("aria-current"); });
      if (play) audio.play().catch(() => {});
    }
    audio.addEventListener("loadedmetadata", () => { if (pendingSeek) { audio.currentTime = pendingSeek; pendingSeek = 0; } audio.playbackRate = speed; });
    audio.addEventListener("play", () => {
      resume.hidden = true;
      document.querySelectorAll(".ab-audio").forEach(o => { if (o !== audio) o.pause(); });   // one player at a time
    });
    audio.addEventListener("timeupdate", () => {
      const tnow = Date.now();
      if (tnow - lastSave > 4000) { lastSave = tnow; store.set(key, { i, t: audio.currentTime }); }
    });
    audio.addEventListener("ended", () => {
      if (i + 1 < tracks.length) load(i + 1, 0, true);
      else store.set(key, { i: 0, t: 0 });
    });
    links.forEach((a, k) => a.addEventListener("click", e => { e.preventDefault(); load(k, 0, true); }));
    box.querySelector(".ab-prev").addEventListener("click", () => load(audio.currentTime > 5 ? i : i - 1, 0, true));
    box.querySelector(".ab-next").addEventListener("click", () => load(i + 1, 0, true));
    sel.value = String(speed);
    sel.addEventListener("change", () => {
      speed = parseFloat(sel.value) || 1; store.set("powAB_speed", speed);
      document.querySelectorAll(".ab-audio").forEach(o => (o.playbackRate = speed));
      document.querySelectorAll(".ab-speed select").forEach(o => (o.value = sel.value));
    });

    const saved = store.get(key);
    if (saved && (saved.i > 0 || saved.t > 10) && tracks[saved.i]) {
      load(saved.i, saved.t, false);
      resume.hidden = false;
      resume.textContent = "Picks up where you left off: chapter " + tracks[saved.i].n + " at " + mmss(saved.t);
    } else load(0, 0, false);
  });
})();
