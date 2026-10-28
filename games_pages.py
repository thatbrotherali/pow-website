"""The brain-training suite: a games hub (play.html), the Memory Game and the Focus Game.
The Decision Game lives in build.py. Shared code: docs/assets/games-common.js."""
import json

B = None
esc = None


def name_modal():
    return """<div class="dg-modal" id="g-name" hidden><form class="card dg-name-card" id="g-name-form">
<h2 class="h-md">Your name for the leaderboard</h2>
<p class="muted">Shown next to your scores in every game. 2 to 16 characters. Your scores stay linked to this device.</p>
<label for="g-name-input">Name<input id="g-name-input" maxlength="16" autocomplete="nickname" required></label>
<p class="form-note" id="g-name-note"></p>
<div class="actions"><button class="btn btn-door" type="submit">Save my score</button><button class="btn btn-outline" type="button" id="g-name-skip">Not now</button></div>
</form></div>"""


def segs(items, attr, label):
    return f'<div class="segs" role="group" aria-label="{esc(label)}">' + "".join(
        f'<button type="button" class="seg" data-{attr}="{k}" aria-pressed="false">{esc(v)}</button>' for k, v in items) + "</div>"


def board_section(prefix, cols):
    return f"""<section id="leaderboard" class="section band-alt"><div class="wrap stack" style="gap:20px">
<div class="stack intro"><h2 class="h-lg">Leaderboard</h2><p class="lead muted">Today's Daily Challenge, and the best Endless runs of all time.</p></div>
<div class="dg-toolbar">{segs([("daily", "Today's Daily"), ("endless", "Endless")], "board", "Leaderboard")}</div>
<div class="table-wrap card" style="padding:0"><table class="dg-table"><thead><tr><th>#</th><th>Player</th>{''.join(f'<th class="num">{c}</th>' for c in cols)}<th class="num">Date</th></tr></thead><tbody id="{prefix}-board"></tbody></table></div>
<p class="muted" id="{prefix}-board-note" style="font-size:14px"></p>
</div></section>

<section id="mine" class="section"><div class="wrap stack" style="gap:20px">
<div class="stack intro"><h2 class="h-lg">My bests</h2><p class="lead muted" id="{prefix}-daily-status"></p></div>
<div class="grid grid-3" id="{prefix}-mine"></div>
<p class="muted" style="font-size:14px">Playing as <strong data-g-me>not set yet</strong> · <button type="button" class="linklike" data-g-rename>change name</button></p>
</div></section>"""


def ld(name, url, desc, genre):
    return json.dumps({"@context": "https://schema.org", "@type": ["VideoGame", "WebApplication"], "name": name, "url": B.canonical(url),
                       "applicationCategory": "GameApplication", "genre": genre, "operatingSystem": "Any (web browser)",
                       "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
                       "author": {"@type": "Person", "name": B.AUTHOR, "@id": f"{B.SITE_URL}/about.html#shareef"}, "description": desc}, ensure_ascii=False)


def nav(current):
    items = [("All games", "play.html", False, None), ("Decision", "decision-game.html", False, None), ("Memory", "memory-game.html", False, None),
             ("Focus", "focus-game.html", False, None)]
    return [x for x in items if x[1] != current]


def scripts(name):
    return f"""<script src="assets/games-common.js?v={B.asset_v('games-common.js')}" defer></script>
<script src="assets/{name}?v={B.asset_v(name)}" defer></script>"""


def build_memory():
    modes = segs([("daily", "Daily"), ("practice", "Practice"), ("endless", "Endless")], "mode", "Game mode")
    desc = "A free memory game: study a growing set of letters, numbers and shapes, then spot what's missing or what's new. A Daily Challenge and an Endless climb."
    body = f"""{B.header("The Memory Game", "Brain training by People of the World", nav("memory-game.html"))}
<main>
<section class="band"><div class="wrap section dg-hero">
<p class="eyebrow accent">Free brain training · no sign-up</p>
<h1 class="h-xl">Remember. Then spot the change.</h1>
<p class="lead muted" style="max-width:660px">Study a set of letters for a moment. Then one is gone, or a new one has slipped in: which? The sets grow, numbers join the letters, then shapes join them both.</p>
</div></section>

<section id="play" class="section dg-section"><div class="wrap stack" style="gap:18px">
<div class="dg-toolbar">{modes}<label class="dg-check"><input type="checkbox" id="g-sound" checked> Sound</label></div>
<div class="card mg-stage" id="mg-stage">
<p class="mg-msg" id="mg-msg" aria-live="polite"></p>
<div class="mg-items" id="mg-items"></div>
<div class="mg-choices" id="mg-choices"></div>
</div>
<div class="actions" style="justify-content:center"><button type="button" class="btn btn-door dg-start" id="mg-start">Start</button></div>
<dl class="dg-status"><div><dt>Level</dt><dd id="mg-level">1</dd></div><div><dt>Lives</dt><dd id="mg-lives">–</dd></div>
<div><dt>Correct</dt><dd id="mg-ok">0</dd></div><div><dt>Mistakes</dt><dd id="mg-bad">0</dd></div></dl>
<div class="card dg-result" id="mg-result" hidden></div>
</div></section>
{name_modal()}
{board_section("mg", ["Correct", "Avg answer"])}

<section class="section band-alt"><div class="wrap stack" style="gap:28px">
<h2 class="h-lg">How it works</h2>
<div class="grid grid-3">
<div class="card"><h3 class="h-md">Study, then answer</h3><p class="muted">The set shows for a few seconds, longer for bigger sets. Then either one is missing (pick it from four) or one is new (tap the newcomer).</p></div>
<div class="card"><h3 class="h-md">Three ways to play</h3><p class="muted"><strong>Daily</strong>: ten rounds, climbing a level each round, the same for everyone today; only your first run counts. <strong>Endless</strong>: climb a level each time you're right; three lives. <strong>Practice</strong>: nothing recorded.</p></div>
<div class="card"><h3 class="h-md">Letters, numbers, shapes</h3><p class="muted">Levels 1 to 4 use letters, 5 to 8 add numbers, and from level 9 shapes join in. Look-alikes such as O and 0 are left out, so every mistake is a memory slip, not a trick.</p></div>
</div></div></section>
</main>
{B.footer()}
{scripts("memory-game.js")}"""
    B.page("memory-game.html", "The Memory Game: free brain training", desc, body, "play",
           extra_head=f'<script type="application/ld+json">{ld("The Memory Game", "memory-game.html", desc, ["Brain training", "Memory"])}</script>')


def build_focus():
    modes = segs([("daily", "Daily"), ("practice", "Practice"), ("endless", "Endless")], "mode", "Game mode")
    desc = "A free focus game: press the moment a plus sign appears, but hold back when it has a circle around it. A Daily Challenge and an Endless run."
    body = f"""{B.header("The Focus Game", "Brain training by People of the World", nav("focus-game.html"))}
<main>
<section class="band"><div class="wrap section dg-hero">
<p class="eyebrow accent">Free brain training · no sign-up</p>
<h1 class="h-xl">Press. Or hold back.</h1>
<p class="lead muted" style="max-width:660px">Watch the centre. When a plus sign appears, press as fast as you can. When the plus has a circle around it, don't press at all. Speed matters; so does self-control.</p>
</div></section>

<section id="play" class="section dg-section"><div class="wrap stack" style="gap:18px">
<div class="dg-toolbar">{modes}<label class="dg-check"><input type="checkbox" id="g-sound" checked> Sound</label></div>
<div class="card fg-stage" id="fg-stage">
<div class="fg-sign" id="fg-sign" aria-hidden="true"><span class="fg-plus"></span></div>
<p class="mg-msg" id="fg-msg" aria-live="polite"></p>
</div>
<div class="fg-controls"><button type="button" class="btn btn-door dg-start" id="fg-start">Start</button>
<button type="button" class="fg-press" id="fg-press" disabled>Press<kbd>Space</kbd></button></div>
<dl class="dg-status"><div><dt>Sign</dt><dd id="fg-trial">0 / 30</dd></div><div><dt>Hits</dt><dd id="fg-hits">0</dd></div>
<div><dt>Mistakes</dt><dd id="fg-bad">0</dd></div><div><dt>Average reaction</dt><dd id="fg-avg">0.00s</dd></div>
<div><dt>Chances</dt><dd id="fg-lives">–</dd></div><div id="fg-window" class="fg-window"></div></dl>
<div class="card dg-result" id="fg-result" hidden></div>
</div></section>
{name_modal()}
{board_section("fg", ["Right", "Avg reaction"])}

<section class="section band-alt"><div class="wrap stack" style="gap:28px">
<h2 class="h-lg">How it works</h2>
<div class="grid grid-3">
<div class="card"><h3 class="h-md">Three kinds of mistake</h3><p class="muted"><strong>Too soon</strong>: pressing before any sign. <strong>Too slow</strong>: missing a plain plus. <strong>Pressed on a circle</strong>: not holding back. About one sign in four has a circle.</p></div>
<div class="card"><h3 class="h-md">Three ways to play</h3><p class="muted"><strong>Daily</strong>: thirty signs, the same for everyone today; only your first run counts. <strong>Endless</strong>: the time to respond shrinks as you go; three mistakes end the run. <strong>Practice</strong>: nothing recorded.</p></div>
<div class="card"><h3 class="h-md">On a phone or a computer</h3><p class="muted">Press the space bar, or tap the big Press button. Keep your finger ready, and your eyes on the centre.</p></div>
</div></div></section>
</main>
{B.footer()}
{scripts("focus-game.js")}"""
    B.page("focus-game.html", "The Focus Game: free brain training", desc, body, "play",
           extra_head=f'<script type="application/ld+json">{ld("The Focus Game", "focus-game.html", desc, ["Brain training", "Reaction time", "Attention"])}</script>')


def build_hub():
    games = [("decision", "decision-game.html", "Decision", "The Decision Game", "A picture, a word, “is” or “is not”: true or false? Read the whole sentence and decide, fast."),
             ("memory", "memory-game.html", "Memory", "The Memory Game", "Study a set of letters, numbers and shapes. Then spot what's missing, or what's new."),
             ("focus", "focus-game.html", "Focus", "The Focus Game", "Press the instant a plus appears. Hold back when it's circled. Speed and self-control.")]
    cards = "".join(f"""<article class="card g-card"><span class="step-label">{esc(k)}</span><h2 class="h-md">{esc(t)}</h2><p class="muted">{esc(d)}</p>
<p class="g-today muted" data-game="{g}"></p>
<div class="actions" style="margin-top:auto"><a class="btn btn-door" href="{u}">Play</a></div></article>""" for g, u, k, t, d in games)
    desc = "Free brain-training games for focus, memory and decision-making: a new Daily Challenge every day, the same for everyone, with streaks and leaderboards."
    body = f"""{B.header("Brain training", "by People of the World", [("The games", "#games", False, None), ("Why play", "#why-play", False, None)])}
<main>
<section class="band"><div class="wrap section stack" style="gap:22px;max-width:900px">
<p class="eyebrow accent">Free · no sign-up · a few minutes a day</p>
<h1 class="h-xl">Focus. Memory. Decision.</h1>
<p class="lead muted" style="max-width:660px">Three quick games, each with a new Daily Challenge, the same for everyone in the world. Play all three in five minutes, keep your streak alive, and see how you compare.</p>
<p class="g-streak" id="g-streak"></p>
</div></section>

<section id="games" class="section"><div class="wrap stack" style="gap:28px">
<div class="grid grid-3">{cards}</div>
</div></section>

<section id="why-play" class="section band-alt"><div class="wrap" style="display:flex;flex-wrap:wrap;gap:32px 64px;align-items:flex-start">
<h2 class="h-lg" style="flex:1 1 300px">Why play</h2>
<div class="stack" style="flex:2 1 460px;min-width:0">
<p class="lead">Each game asks for something we use all day: noticing, remembering, and choosing well under a little pressure. A few minutes of practice, every day, is a good habit, and it's fun to see your own numbers move.</p>
<p class="lead muted">We make no medical claims: these are games for practice and enjoyment, not treatments. Play for the challenge, the streak, and the friendly competition.</p>
</div></div></section>
</main>
{B.footer()}
<script src="assets/games-common.js?v={B.asset_v('games-common.js')}" defer></script>
<script>
document.addEventListener("DOMContentLoaded", () => {{
  const G = window.POWG, n = G.dayNumber();
  document.querySelectorAll(".g-today").forEach(p => {{
    const g = p.dataset.game, d = G.dailyDone(g), st = G.streak(g);
    p.textContent = d ? `Today's #${{n}} done: ${{d.correct}}/${{d.questions}}${{st > 1 ? ` · ${{st}}-day streak` : ""}}` : `Today's challenge #${{n}} is waiting${{st ? ` · ${{st}}-day streak` : ""}}`;
  }});
  const all = G.streak(), el = document.getElementById("g-streak");
  if (all) el.textContent = `Your streak: ${{all}} day${{all === 1 ? "" : "s"}} in a row.`;
}});
</script>"""
    B.page("play.html", "Brain training: focus, memory and decision games", desc, body, "play")


def build(b):
    global B, esc
    B, esc = b, b.esc
    build_hub()
    build_memory()
    build_focus()
