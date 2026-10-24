#!/usr/bin/env python3
"""Builds the People of the World website into ./docs (the folder GitHub Pages publishes)

Run:  python3 build.py
Everything in ./docs is plain HTML/CSS/JS and can be uploaded to any host (GitHub Pages, Netlify, etc.).
The free online edition of The Portal Opens is generated from src/portal.txt.
"""
import html, re, pathlib, json

ROOT = pathlib.Path(__file__).parent
OUT = ROOT / "docs"
SRC = ROOT / "src"
YEAR = 2026
CONTACT = "shareef@peopleoftheworld.net"
# The address the site is published at. Change this one line to "https://peopleoftheworld.net"
# when the domain moves to this site, then run the build again.
SITE_URL = "https://peopleoftheworld.net"
AUTHOR = "Shareef Ali Rashada"
FONTS = ("https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,600"
         "&family=Inter:wght@400;500;600&family=Literata:opsz,wght@7..72,400;7..72,600"
         "&family=IBM+Plex+Mono:wght@400;600&display=swap")

DOORS = [
    # slug, css door, audience label, question, blurb, cta
    ("seekers", "seekers", "For seekers", "Searching for meaning?",
     "The Portal Opens tells the untold history of Earth: Jesus, Lucifer, Adam and Eve, and Melchizedek. Free to read.",
     "Read it free"),
    ("urantia", "urantia", "For Urantia Book readers and their families", "Loved the Urantia Book?",
     "Michael, Lucifer, Caligastia, Adam and Eve and Melchizedek in their own voices. New for readers, gentle for newcomers, easy to share.",
     "Find your way in"),
    ("science", "science", "For the science-curious", "How does gravity really work?",
     "Graviton Pressure Theory presents gravity as a push from outside, with a named mechanism you can test.",
     "Start the series"),
    ("builders", "builders", "For builders", "Ready to end poverty?",
     "A designed system, not charity: Civic Credits, Poverty Elimination Centers and LifeLink, with a 2050 goal.",
     "See the plan"),
    ("music", "music", "For music lovers", "Music to ease your mind",
     "Jazz, acoustic and new-age albums by That Brother Ali, free to stream on Spotify, Apple Music and Amazon.",
     "Listen now"),
    ("easykey", "easykey", "For learners, parents and teachers", "Want to play piano?",
     "EasyKey's visual notation shows exactly which keys to press and for how long. No staff to decode.",
     "Try EasyKey"),
    ("ai", "ai", "For readers, researchers and AI", "Want the full source texts?",
     "The Open Library holds every book, paper and plan, free to read in plain text for people, search engines and AI systems.",
     "Open the library"),
]
DOOR_NAMES = {"seekers": "The Portal Opens", "urantia": "For Urantia readers", "science": "Graviton Pressure Theory", "builders": "End Poverty by Design",
              "music": "That Brother Ali", "easykey": "EasyKey Music", "ai": "The Open Library"}

esc = lambda s: html.escape(s, quote=True)


def asset_v(name):
    """Short fingerprint of an asset file, added to its link so browsers fetch the new copy after each change."""
    import hashlib
    return hashlib.sha1((OUT / "assets" / name).read_bytes()).hexdigest()[:8]


# ---------------------------------------------------------------- page shell
def canonical(fname):
    return SITE_URL + "/" + re.sub(r"(^|/)index\.html$", r"\1", fname)


def head(title, desc, fname="", extra=""):
    url = canonical(fname)
    return f"""<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="People of the World">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE_URL}/assets/share/__OG__.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{esc(title)}">
<meta name="twitter:card" content="summary_large_image">
<meta name="author" content="{AUTHOR}">{extra}
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="icon" href="assets/favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTS}">
<link rel="stylesheet" href="assets/site.css?v={asset_v('site.css')}">
<script src="assets/site.js?v={asset_v('site.js')}" defer></script>"""


def header(name="People of the World", sub=None, nav=()):
    sub_html = f'<span class="brand-sub">{esc(sub)}</span>' if sub else ""
    links = "".join(
        f'<a href="{h}"{" class=\"btn btn-door\"" if btn else ""}{" data-link=\"" + dl + "\"" if dl else ""}>{esc(t)}</a>'
        for t, h, btn, dl in nav)
    return f"""<header class="site-header">
<div class="wrap">
<a class="brand" href="index.html"><span class="logo"><img src="assets/logo.webp" alt="" width="44" height="44"></span>
<span class="brand-name">{esc(name)}{sub_html}</span></a>
<nav class="site-nav" aria-label="Main">{links}</nav>
</div>
</header>"""


def footer(current=None):
    doors = "".join(f'<a href="{s}.html">{esc(DOOR_NAMES[s])}</a>' for s, *_ in DOORS if s != current)
    return f"""<footer class="site-footer">
<div class="wrap">
<div class="cols">
<div class="col wide"><strong style="font-family:var(--display);font-size:22px;font-weight:400">People of the World</strong>
<span>Knowledge, morality, unity and peace, for a world ready for the celestial return.</span></div>
<nav class="col" aria-label="The wider mission"><strong>The wider mission</strong><a href="index.html">The hub</a>{doors}<a href="videos.html">Videos</a><a href="decision-game.html">The Decision Game</a><a href="about.html">About Shareef</a></nav>
<nav class="col" aria-label="Shop"><strong>Books and shop</strong><a href="books.html">All books</a><a href="#" data-link="shop">Shop</a><a href="#" data-link="support">Support the mission</a></nav>
<div class="col"><strong>Contact</strong><span class="copy-row"><span>{CONTACT}</span><button class="copy-btn" type="button" data-copy="{CONTACT}">Copy</button></span></div>
</div>
<p class="legal">© {YEAR} People of the World · POW Productions Pty Ltd, Queensland, Australia · <a href="privacy.html">Privacy</a></p>
</div>
</footer>"""


def signup_band(title, text, button, lst, door):
    return f"""<section class="band door-{door}"><div class="wrap section">
<div class="stack" style="max-width:760px;margin:0 auto;align-items:center;text-align:center;gap:20px">
<h2 class="h-lg">{esc(title)}</h2>
<p class="lead muted">{esc(text)}</p>
<form class="signup" data-list="{lst}" novalidate>
<label for="email-{lst}">Email address<input id="email-{lst}" type="email" autocomplete="email" placeholder="you@example.com" required></label>
<button class="btn btn-door" type="submit">{esc(button)}</button>
</form>
<p class="form-note" role="status"></p>
<p class="muted" style="font-size:13px">We'll only send what you signed up for. <a href="privacy.html">Privacy</a></p>
</div></div></section>"""


PAGES = []  # every published page, for sitemap.xml


def relink(doc, depth):
    """Pages in sub-folders: make root-relative links (assets/..., books.html, graviton-pressure-theory/...) work."""
    if not depth:
        return doc
    up = "../" * depth
    return re.sub(r'((?:href|src)=")(?!https?:|#|/|mailto:|data:|tel:)', lambda m: m.group(1) + up, doc)


SHARE_BY_PAGE = {"books.html": "books", "shop.html": "shop", "urantia.html": "urantia", "decision-game.html": "play",
                 "read.html": "seekers", "glossary.html": "seekers", "ten-steps.html": "seekers", "videos.html": "site", "about.html": "site"}


def share_image(fname, door):
    """Which link-preview picture a page uses (made by tools/make_share_images.py)."""
    if fname in SHARE_BY_PAGE: return SHARE_BY_PAGE[fname]
    if fname.startswith(("graviton-pressure-theory/", "library/graviton")): return "science"
    if door in ("seekers", "urantia", "science", "builders", "music", "easykey", "ai", "play"): return door
    return "site"


def page(fname, title, desc, body, door="hub", extra_head="", lastmod=None):
    """Full HTML document for the real website. fname may be in a sub-folder, e.g. 'graviton-pressure-theory/index.html'."""
    doc = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
{head(title, desc, fname, extra_head)}
</head>
<body class="door-{door}">
{body}
</body>
</html>
"""
    doc = doc.replace("/assets/share/__OG__.jpg", f"/assets/share/{share_image(fname, door)}.jpg", 1)
    doc = relink(doc, fname.count("/"))
    path = OUT / fname
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(doc, encoding="utf-8")
    PAGES.append((fname, lastmod))
    return doc



def video_band(place, heading, fname, intro="", alt=False):
    """A band of videos for a door page. Returns (html, structured data for the page head)."""
    import videos
    sec, ld = videos.section(place, heading, SITE_URL, canonical(fname), intro)
    if not sec:
        return "", ""
    return f'<section class="section{" band-alt" if alt else ""}"><div class="wrap">{sec}</div></section>', ld


# ---------------------------------------------------------------- the book text
PACKET = "[Quantum Computer – Data Stream Processing]"
FIXES = [("it's journey", "its journey"), ("8.413", "8,413"), ("Incompleness", "Incompleteness"),
         ("provides that visage", "provides the visage"), ("everpresent", "ever-present"),
         ("soulbuilding", "soul-building"), ("selfdeception", "self-deception"), ("highranking", "high-ranking"),
         ("superuniverse", "super-universe")]

def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:60]

ENDP = tuple('.?!:"”’)')

def is_item_start(line):
    return bool(re.match(r"^(\d+\.\s|•\s?)", line))

def parse_prose(lines):
    """Turn PDF-wrapped lines into blocks: ('packet', size), ('h2', title), ('h3', t), ('sub', t), ('p', t), ('li', t, kind)."""
    blocks, buf, kind = [], [], "p"
    def flush():
        nonlocal buf, kind
        if buf:
            text = " ".join(x.strip() for x in buf)
            if kind == "p":
                blocks.append(("p", text))
            else:
                blocks.append(("li", re.sub(r"^(\d+\.|•)\s*", "", text), kind))
            buf, kind = [], "p"
    i = 0
    while i < len(lines):
        ln = lines[i].rstrip()
        if not ln.strip():
            flush(); i += 1; continue
        if ln.strip() == PACKET:
            flush()
            size = ""
            j = i + 1
            while j < len(lines) and j <= i + 4:
                t = lines[j].strip()
                if t.startswith("Packet size:"): size = t.replace("Packet size:", "").strip()
                elif t.startswith("Continuing with data stream"): pass
                elif t.startswith("Description:"):
                    title = t.replace("Description:", "").strip()
                    nxt = lines[j + 1].strip() if j + 1 < len(lines) else ""
                    if nxt and len(nxt) < 45 and not nxt.endswith(ENDP) and not title.endswith(ENDP):
                        title += " " + nxt; j += 1
                    blocks.append(("packet", size)); blocks.append(("h2", title))
                    i = j + 1; break
                j += 1
            else:
                blocks.append(("packet", size)); i = j
            continue
        s = ln.strip()
        if re.match(r"^Paper \d+:", s):
            flush()
            t = s
            if i + 1 < len(lines) and len(lines[i + 1].strip()) < 40 and not lines[i + 1].strip().startswith("Lecture"):
                t += " " + lines[i + 1].strip(); i += 1
            blocks.append(("h3", t)); i += 1; continue
        if s.startswith("Lecture Title:"):
            flush(); blocks.append(("sub", s.replace("Lecture Title:", "").strip())); i += 1; continue
        if is_item_start(s):
            flush(); kind = "ol" if s[0].isdigit() else "ul"; buf = [s]
        else:
            buf.append(s)
        # paragraph end: a short line that ends a sentence, or a very short line
        if (len(s) < 62 and s.endswith(ENDP)) or len(s) < 34:
            flush()
        i += 1
    flush()
    return blocks


def render_blocks(blocks):
    out, open_list, sections = [], None, []
    for b in blocks:
        if b[0] != "li" and open_list:
            out.append(f"</{open_list}>"); open_list = None
        if b[0] == "packet":
            if b[1]:
                cur, total = (b[1].split(" of ") + [""])[:2]
                out.append(f'<p class="packet" aria-label="Transmission packet"><span>Quantum computer · data stream</span><span>Packet <b>{esc(cur)}</b> of {esc(total)}</span></p>')
        elif b[0] == "h2":
            sid = slug(b[1]); sections.append((sid, b[1]))
            out.append(f'<h2 id="{sid}">{esc(b[1])}</h2>')
        elif b[0] == "h3":
            out.append(f"<h3>{esc(b[1])}</h3>")
        elif b[0] == "sub":
            out.append(f'<p class="muted"><em>{esc(b[1])}</em></p>')
        elif b[0] == "p":
            out.append(f"<p>{esc(b[1])}</p>")
        elif b[0] == "li":
            if open_list != b[2]:
                if open_list: out.append(f"</{open_list}>")
                out.append(f"<{b[2]}>"); open_list = b[2]
            out.append(f"<li>{esc(b[1])}</li>")
    if open_list: out.append(f"</{open_list}>")
    return "\n".join(out), sections


def load_book():
    text = (SRC / "portal.txt").read_text(encoding="utf-8")
    for a, b in FIXES: text = text.replace(a, b)
    return text.split("\n")

READ_PARTS = [
    # file, number label, title, short blurb, (first line, last line) 1-indexed inclusive
    ("read-introduction", "Introduction", "Gabriel's Introduction and Mission",
     "Gabriel explains why the transmission was sent, and how to read it.", (312, 406)),
    ("read-part-1", "Part 1", "The Untold Story of Jesus",
     "Jesus as Michael of Nebadon, and the review of his seventh bestowal on Earth.", (407, 2237)),
    ("read-part-2", "Part 2", "A Reflection of Darkness",
     "Lucifer's rise, his Declaration of Liberty, and the final reckoning.", (2238, 3290)),
    ("read-part-3", "Part 3", "The Confession of Caligastia",
     "Earth's own Planetary Prince on betrayal, conscience and remorse.", (3291, 4162)),
    ("read-part-4", "Part 4", "Journey to Jerusem",
     "Adam and Eve's mission, their confession, and their ten steps for humanity.", (4163, 4822)),
    ("read-part-5", "Part 5", "The Lessons of Machiventa Melchizedek",
     "Eleven lectures from the Sage of Salem on personality, the soul and cosmic citizenship.", (4823, 6328)),
    ("read-closing", "Closing", "The Final Transmission",
     "Gabriel's reflections, the awakening of Urantia, and his last message.", (6329, 6462)),
]


# ---------------------------------------------------------------- pages
def door_cards(exclude=None):
    cards = []
    for s, door, aud, q, blurb, cta in DOORS:
        if s == exclude: continue
        cards.append(f"""<a class="card door-{door}" href="{s}.html">
<span class="dot" aria-hidden="true"></span>
<span class="eyebrow muted" style="font-size:12px">{esc(aud)}</span>
<span class="h-md" style="font-family:var(--display)">{esc(q)}</span>
<span class="muted" style="font-size:15px;line-height:1.55">{esc(blurb)}</span>
<span class="card-cta">{esc(cta)} →</span>
</a>""")
    return "\n".join(cards)


def build_hub():
    vband, vld = video_band('hub', 'Meet People of the World', 'index.html', 'A one-minute introduction. More on the Videos page.', False)
    body = f"""{header(nav=[("Choose a door", "#doors", False, None), ("The reading path", "#path", False, None),
                        ("Books", "books.html", False, None), ("Shop", "#", False, "shop"),
                        ("Support the mission", "#", True, "support")])}
<main>
<section class="band hero">
<div class="orbits" aria-hidden="true"><span class="orbit o1"></span><span class="orbit o2"></span><span class="orbit o3"></span></div>
<div class="wrap">
<span class="hero-logo"><img src="assets/logo.webp" alt="People of the World logo: people holding hands around the globe" width="136" height="136"></span>
<p class="eyebrow" style="color:var(--band-muted)">A global movement founded by Shareef Ali Rashada</p>
<h1 class="h-xl" style="max-width:900px">Knowledge. Morality. Unity. Peace.</h1>
<p class="lead muted" style="max-width:680px">People of the World works to end poverty by 2050 and to help humanity grow ready for its place in a larger cosmic family. Find the door that fits you.</p>
<div class="actions" style="justify-content:center"><a class="btn btn-door" href="#doors">Choose your door</a><a class="btn btn-ghost" href="read.html">Read The Portal Opens free</a></div>
</div>
</section>

<section id="doors" class="section"><div class="wrap stack" style="gap:40px">
<div class="stack intro"><h2 class="h-lg">Seven doors, one purpose</h2>
<p class="lead muted">Each door is written for the people who walk through it. Start wherever your question is.</p></div>
<div class="grid grid-3">{door_cards()}</div>
</div></section>

<section id="path" class="section band-alt"><div class="wrap stack" style="gap:40px">
<div class="stack intro"><p class="eyebrow muted">The reading path</p><h2 class="h-lg">Imagine. Understand. Build.</h2>
<p class="lead muted">The books are written to be read in order. A story opens the mind, a history fills it, and a plan turns it into action.</p></div>
<div class="path">
<a class="card door-seekers" href="books.html#novel"><span class="step-label">Step 1 · Imagine</span>
<span class="h-md" style="font-family:var(--display)">People of the World</span>
<span class="muted" style="font-size:15px">A novel. Aliens take three-quarters of humanity, and the people left behind must rebuild a world without force or money. <span class="tag">For adults 18+</span></span>
<span class="card-cta">About the novel →</span></a>
<a class="card door-seekers" href="seekers.html"><span class="step-label">Step 2 · Understand</span>
<span class="h-md" style="font-family:var(--display)">The Portal Opens</span>
<span class="muted" style="font-size:15px">The history behind the story: Jesus, Lucifer, Caligastia, Adam and Eve, and Melchizedek's lessons. Free to read online.</span>
<span class="card-cta">Read it free →</span></a>
<a class="card door-builders" href="builders.html"><span class="step-label">Step 3 · Build</span>
<span class="h-md" style="font-family:var(--display)">The Plan to End Poverty</span>
<span class="muted" style="font-size:15px">Civic Credits, Poverty Elimination Centers and LifeLink: a designed system to end poverty by 2050.</span>
<span class="card-cta">See the plan →</span></a>
</div>
</div></section>

<section class="section door-play"><div class="wrap" style="display:flex;flex-wrap:wrap;gap:24px 48px;align-items:center">
<div class="stack" style="flex:2 1 420px;min-width:0"><p class="eyebrow accent" style="filter:brightness(.85)">Free brain training</p>
<h2 class="h-lg">The Decision Game</h2>
<p class="lead muted">A picture, a word, “is” or “is not”. True or false, as fast as you can. Every score goes on the online leaderboard.</p></div>
<p style="flex:1 1 200px"><a class="btn btn-door" href="decision-game.html">Play now</a></p>
</div></section>

<section class="section"><div class="wrap award">
<div class="badge" aria-hidden="true">Literary Titan Silver Book Award</div>
<div class="text stack">
<p class="eyebrow" style="color:#9A5F12">Literary Titan Silver Book Award · The Portal Opens</p>
<p class="quote">“A wild, luminous ride worth taking.”</p>
<p class="lead muted">Literary Titan rated The Portal Opens four stars, and recommends it to seekers and to anyone religion left with unanswered questions.</p>
<p><a href="#" data-link="review" style="font-weight:600">Read the full review</a></p>
</div></div></section>

{vband}
{signup_band("One teaching a week, free.", "A short, practical reading each week, drawn from The Portal Opens. Unsubscribe any time.", "Send me the teachings", "teachings", "hub")}

<section id="mission" class="section"><div class="wrap stack" style="gap:36px">
<div style="display:flex;flex-wrap:wrap;gap:24px 48px">
<h2 class="h-lg" style="flex:1 1 300px">Why it all connects</h2>
<div class="stack" style="flex:2 1 460px;min-width:0">
<p class="lead muted">Every project serves one goal: a world at peace, free of poverty and open to truth. Knowledge and understanding lead to morality. Morality makes unity possible, unity makes peace possible, and a world at peace is ready for the celestial return.</p>
<p><a href="#" data-link="vision" style="font-weight:600">Read the full Vision</a></p>
</div></div>
<ol class="steps" aria-label="The five steps of the mission">
<li><span>1</span>Knowledge</li><li><span>2</span>Understanding</li><li><span>3</span>Morality</li><li><span>4</span>Unity</li><li class="last"><span>5</span>Peace, ready for the return</li>
</ol>
</div></section>
</main>
{footer()}"""
    page("index.html", "People of the World", "Knowledge, morality, unity and peace: seven doors into the work of Shareef Ali Rashada, from The Portal Opens to EasyKey Music.", body, extra_head=vld)
    return body


def build_seekers():
    parts = [p for p in READ_PARTS if p[1].startswith("Part")]
    part_cards = "\n".join(f"""<a class="card" href="{f}.html"><span class="meta">{esc(n)}</span>
<span class="h-md" style="font-family:var(--display)">{esc(t)}</span>
<span class="muted" style="font-size:15px;line-height:1.55">{esc(b)}</span><span class="card-cta">Read this part →</span></a>""" for f, n, t, b, _ in parts)
    vband, vld = video_band('seekers', 'Watch', 'seekers.html', 'Short films on The Portal Opens and the light within.', True)
    body = f"""{header("The Portal Opens", "by People of the World", [("Read free", "read.html", False, None), ("Ten steps", "ten-steps.html", False, None),
                        ("Glossary", "glossary.html", False, None), ("Buy the book", "#buy", True, None)])}
<main>
<section class="band"><div class="wrap section" style="display:flex;flex-wrap:wrap;align-items:center;gap:56px">
<div class="stack" style="flex:999 1 460px;min-width:0;gap:22px">
<p class="eyebrow accent">Winner · Literary Titan Silver Book Award</p>
<h1 class="h-xl">The story you were never told.</h1>
<p class="lead muted" style="max-width:600px">The untold history of Earth: Jesus, Lucifer, Adam and Eve, and the choice still before you. Read it free online, or keep a copy on your shelf.</p>
<div class="actions"><a class="btn btn-door" href="read.html">Start reading free</a><a class="btn btn-ghost" href="#buy">Buy the book</a></div>
</div>
<div class="portal" style="flex:1 1 260px">
<span class="ring" aria-hidden="true"></span><span class="ring" aria-hidden="true"></span><span class="ring" aria-hidden="true"></span>
<img class="cover-img" src="assets/cover-portal.webp" alt="Cover of The Portal Opens by Shareef Ali Rashada" width="384" height="576">
</div>
</div></section>

<section class="section"><div class="wrap stack" style="gap:40px">
<div class="stack intro"><h2 class="h-lg">Five accounts from the universal archives</h2>
<p class="lead muted">Not dogma or doctrine, but the stories of real beings whose choices still shape your life today.</p></div>
<div class="grid grid-5">{part_cards}</div>
</div></section>

<section class="section band-alt"><div class="wrap" style="display:flex;flex-wrap:wrap;gap:32px 56px;align-items:center">
<div class="stack" style="flex:1 1 360px;min-width:0">
<p class="eyebrow accent" style="filter:brightness(.8)">From Part 4</p>
<h2 class="h-lg">Ten steps for humanity</h2>
<p class="lead muted">In their message to Earth, Adam and Eve leave ten practical steps: unity, stillness, forgiveness, service, courage for truth, and more. A good place to begin.</p>
<p><a class="btn btn-solid" href="ten-steps.html">Read the ten steps</a></p>
</div>
<blockquote class="quote" style="flex:1 1 360px;margin:0;min-width:0">“Seek love. Seek unity. Seek truth.”<footer class="muted" style="font-family:var(--body);font-size:15px;margin-top:12px">Adam, in Journey to Jerusem</footer></blockquote>
</div></section>

<section class="section"><div class="wrap stack" style="gap:40px">
<div class="stack intro"><h2 class="h-lg">Read or listen, free</h2>
<p class="lead muted">The teachings are free, always. Start at the beginning, or open the glossary beside you as you read.</p></div>
<div class="grid">
<a class="card" href="read.html"><span class="h-md" style="font-family:var(--display)">Read online</span><span class="muted" style="font-size:15px">The full book, part by part, in your browser.</span><span class="card-cta">Begin reading →</span></a>
<a class="card" href="glossary.html"><span class="h-md" style="font-family:var(--display)">Gabriel's Glossary</span><span class="muted" style="font-size:15px">Thirty names and terms of the book, explained in plain language.</span><span class="card-cta">Open the glossary →</span></a>
<a class="card" href="#" data-link="audiobook"><span class="h-md" style="font-family:var(--display)">Listen to the audiobook</span><span class="muted" style="font-size:15px">Every chapter read aloud, free to stream.</span><span class="card-cta">Start listening →</span></a>
</div></div></section>

<section class="band"><div class="wrap section stack" style="max-width:900px;align-items:center;text-align:center;gap:22px">
<p class="eyebrow accent">Literary Titan · four stars</p>
<p class="quote" style="font-size:clamp(2rem,4vw,3.1rem)">“A wild, luminous ride worth taking.”</p>
<p class="lead muted" style="max-width:680px">The reviewer found the book unexpectedly moving, and recommends it to seekers, the spiritually curious, and anyone religion left with unanswered questions.</p>
<p><a href="#" data-link="review" style="font-weight:600;color:var(--seekers)">Read the full review</a></p>
</div></section>

<section id="buy" class="section band-alt"><div class="wrap stack" style="gap:40px">
<div class="stack intro"><h2 class="h-lg">Keep a copy</h2>
<p class="lead muted">To read, gift or lend. Every copy sold supports the work of People of the World.</p></div>
<div class="grid">
<div class="card"><span class="eyebrow muted" style="font-size:12px">Paperback</span><span class="h-md" style="font-family:var(--display)">Printed by Lulu</span><span class="muted" style="font-size:15px">Shipped worldwide.</span><a class="btn btn-solid" href="#" data-link="portalPaperback" style="margin-top:auto">Buy the paperback</a></div>
<div class="card"><span class="eyebrow muted" style="font-size:12px">Hardcover</span><span class="h-md" style="font-family:var(--display)">The keepsake edition</span><span class="muted" style="font-size:15px">Shipped worldwide.</span><a class="btn btn-solid" href="#" data-link="portalHardcover" style="margin-top:auto">Buy the hardcover</a></div>
<div class="card"><span class="eyebrow muted" style="font-size:12px">Kindle ebook</span><span class="h-md" style="font-family:var(--display)">Read on any device</span><span class="muted" style="font-size:15px">Delivered instantly from Amazon.</span><a class="btn btn-outline" href="#" data-link="portalKindle" style="margin-top:auto">Buy on Amazon</a></div>
</div>
<p class="muted" style="font-size:14px">ISBN 978-1-326-56533-6 · Published by POW Productions Pty Ltd</p>
</div></section>

{vband}
{signup_band("One teaching a week, free.", "A short reading from The Portal Opens each week. Unsubscribe any time.", "Send me the teachings", "seekers", "seekers")}
</main>
{footer("seekers")}"""
    page("seekers.html", "The Portal Opens", "The untold history of Earth: Jesus, Lucifer, Caligastia, Adam and Eve, and Melchizedek. Read it free online.", body, "seekers", extra_head=vld)


def reader_header():
    return header("The Portal Opens", "Free online edition", [("Contents", "read.html", False, None), ("Glossary", "glossary.html", False, None),
                                                            ("About the book", "seekers.html", False, None), ("Buy the book", "seekers.html#buy", True, None)])


def build_reader():
    lines = load_book()
    toc_entries = []
    rendered = []
    for idx, (f, num, title, blurb, (a, b)) in enumerate(READ_PARTS):
        html_body, sections = render_blocks(parse_prose(lines[a - 1:b]))
        rendered.append((f, num, title, blurb, html_body, sections))
        toc_entries.append((f, num, title, blurb, sections))

    def toc_html(current):
        items = []
        for f, num, title, blurb, sections in toc_entries:
            if f == current:
                subs = "".join(f'<li><a href="#{sid}">{esc(t)}</a></li>' for sid, t in sections)
                items.append(f'<li><strong>{esc(num)} · {esc(title)}</strong><ol style="margin:6px 0 4px 10px">{subs}</ol></li>')
            else:
                items.append(f'<li><a href="{f}.html">{esc(num)} · {esc(title)}</a></li>')
        return f'<nav class="toc" aria-label="Contents"><details open><summary>Contents</summary><ol>{"".join(items)}<li><a href="glossary.html">Gabriel\'s Glossary</a></li></ol></details></nav>'

    for i, (f, num, title, blurb, html_body, sections) in enumerate(rendered):
        prev = rendered[i - 1] if i > 0 else None
        nxt = rendered[i + 1] if i + 1 < len(rendered) else None
        nav = '<nav class="part-nav" aria-label="Parts">'
        nav += f'<a href="{prev[0]}.html"><span>← Previous</span>{esc(prev[1])} · {esc(prev[2])}</a>' if prev else '<a href="read.html"><span>← Back</span>Contents</a>'
        nav += f'<a href="{nxt[0]}.html" style="text-align:right"><span>Next →</span>{esc(nxt[1])} · {esc(nxt[2])}</a>' if nxt else '<a href="seekers.html#buy" style="text-align:right"><span>Finished?</span>Keep a copy of the book</a>'
        nav += "</nav>"
        body = f"""{reader_header()}
<main class="section"><div class="wrap reader">
{toc_html(f)}
<article class="prose">
<p class="eyebrow accent" style="font-family:var(--body);filter:brightness(.85)">{esc(num)}</p>
<h1 class="h-lg" style="margin:.2em 0 .6em">{esc(title)}</h1>
{html_body}
{nav}
</article>
</div></main>
{footer("seekers")}"""
        page(f + ".html", f"{title} · The Portal Opens", f"{blurb} Free online edition of The Portal Opens.", body, "seekers")

    # contents page with the opening transmission log
    log = "\n".join(esc(l) for l in lines[61:123])
    cards = "\n".join(f"""<a class="card" href="{f}.html"><span class="meta">{esc(num)}</span>
<span class="h-md" style="font-family:var(--display)">{esc(title)}</span><span class="muted" style="font-size:15px;line-height:1.55">{esc(blurb)}</span>
<span class="card-cta">Read →</span></a>""" for f, num, title, blurb, _, _ in rendered)
    body = f"""{reader_header()}
<main>
<section class="band"><div class="wrap section stack" style="gap:20px">
<p class="eyebrow accent">Free online edition</p>
<h1 class="h-xl">The Portal Opens</h1>
<p class="lead muted" style="max-width:680px">The complete book, free to read. It begins as a signal is picked up by a quantum computer in Brisbane and decoded with the help of Gabriel.</p>
</div></section>
<section class="section"><div class="wrap stack" style="gap:40px">
<details class="card" style="gap:0"><summary style="cursor:pointer;font-weight:600">The opening log: how the signal was found</summary>
<div style="overflow-x:auto;margin-top:16px"><pre style="font-family:var(--mono);font-size:13px;line-height:1.6;white-space:pre-wrap;margin:0;color:var(--muted)">{log}</pre></div></details>
<div class="grid">{cards}
<a class="card" href="glossary.html"><span class="meta">Reference</span><span class="h-md" style="font-family:var(--display)">Gabriel's Glossary</span>
<span class="muted" style="font-size:15px;line-height:1.55">The names and terms of the book, explained in plain language.</span><span class="card-cta">Open →</span></a>
</div>
<p class="note">This free edition carries the full text of the book. Copyright © 2025 Shareef Ali Rashada, POW Productions Pty Ltd. Please share the link rather than copying the text.</p>
</div></section>
</main>
{footer("seekers")}"""
    page("read.html", "Read The Portal Opens", "The Portal Opens by Shareef Ali Rashada: the complete book, free to read online.", body, "seekers")

    # glossary
    gl_body, _ = render_blocks(parse_prose(lines[123:311]))
    body = f"""{reader_header()}
<main class="section"><div class="wrap reader">
{toc_html("glossary")}
<article class="prose"><p class="eyebrow accent" style="font-family:var(--body);filter:brightness(.85)">Reference</p>
<h1 class="h-lg" style="margin:.2em 0 .6em">Gabriel's Glossary</h1>
{gl_body.replace("<h2", "<h3").replace("</h2>", "</h3>")}
<nav class="part-nav"><a href="read.html"><span>← Back</span>Contents</a><a href="read-introduction.html" style="text-align:right"><span>Start reading →</span>Introduction</a></nav>
</article></div></main>
{footer("seekers")}"""
    page("glossary.html", "Gabriel's Glossary", "The names and terms of The Portal Opens, explained in plain language.", body, "seekers")

    # ten steps (Part 4, Adam and Eve's final messages)
    seg = lines[4680:4757]
    steps, cur = [], None
    for l in seg:
        m = re.match(r"^(\d+)\. (.+)$", l.strip())
        if m and int(m.group(1)) == len(steps) + 1:
            cur = [m.group(2), []]; steps.append(cur)
        elif cur: cur[1].append(l.strip())
    items = "\n".join(f"<li><h3>{esc(t)}</h3><p class=\"muted\" style=\"font-size:15.5px;line-height:1.6\">{esc(' '.join(txt))}</p></li>" for t, txt in steps)
    body = f"""{header("The Portal Opens", "by People of the World", [("Read free", "read.html", False, None), ("Glossary", "glossary.html", False, None), ("Buy the book", "seekers.html#buy", True, None)])}
<main>
<section class="band"><div class="wrap section stack" style="gap:18px">
<p class="eyebrow accent">From Part 4 · Journey to Jerusem</p>
<h1 class="h-xl">Ten steps for humanity</h1>
<p class="lead muted" style="max-width:700px">“These practical steps are intended for immediate use, as well as for those further along in their spiritual journey. They are meant to provide strength, purpose, and clarity in times of doubt.” — Eve</p>
</div></section>
<section class="section"><div class="wrap stack" style="gap:36px">
<ol class="tensteps">{items}</ol>
<p class="quote" style="text-align:center;max-width:820px;margin:0 auto">“Seek love. Seek unity. Seek truth.”</p>
<div class="actions" style="justify-content:center"><a class="btn btn-solid" href="read-part-4.html">Read Journey to Jerusem</a><a class="btn btn-outline" href="read.html">All parts</a></div>
</div></section>
{signup_band("One teaching a week, free.", "A short reading from The Portal Opens each week. Unsubscribe any time.", "Send me the teachings", "tensteps", "seekers")}
</main>
{footer("seekers")}"""
    page("ten-steps.html", "Ten Steps for Humanity", "Adam and Eve's ten practical steps for humanity, from The Portal Opens.", body, "seekers")
    return {f: [s for s in sections] for f, _, _, _, _, sections in rendered}, len(steps)


PLACEHOLDERS = {
}


PLACEHOLDER_COVERS = {}


def build_placeholders():
    for s, (name, tagline, text, links) in PLACEHOLDERS.items():
        cov = PLACEHOLDER_COVERS.get(s)
        cover_html = (f'<img class="cover-img" style="flex:0 1 220px;width:220px" src="assets/{cov[0]}.webp" alt="Cover of {esc(cov[1])}" width="{cov[2]}" height="{cov[3]}">' if cov else "")
        btns = "".join(f'<a class="btn btn-door" href="{u}" target="_blank" rel="noopener">{esc(t)}</a>' if u else f'<p class="muted">{esc(t)}</p>' for t, u in links)
        body = f"""{header(name, "by People of the World", [("All doors", "index.html#doors", False, None), ("Books", "books.html", False, None)])}
<main>
<section class="band"><div class="wrap section" style="display:flex;flex-wrap:wrap;align-items:center;gap:40px 56px">
<div class="stack" style="flex:999 1 440px;min-width:0;gap:20px">
<p class="eyebrow accent">This door is being built</p>
<h1 class="h-xl">{esc(tagline)}</h1>
<p class="lead muted" style="max-width:680px">{esc(text)}</p>
<div class="actions">{btns}</div>
</div>
{cover_html}
</div></section>
<section class="section"><div class="wrap stack" style="gap:28px">
<h2 class="h-lg">Meanwhile, try another door</h2>
<div class="grid">{door_cards(exclude=s)}</div>
</div></section>
{signup_band("Hear when this door opens.", "One email when it's ready. Nothing else unless you ask for it.", "Tell me when it opens", s, s)}
</main>
{footer(s)}"""
        page(f"{s}.html", name, f"{name} by People of the World: {tagline}", body, s)


SPOTIFY_ARTIST = "https://open.spotify.com/artist/1WTqeXUcuv0NF0EAAEgHu5"
SPOTIFY_EASE = "https://open.spotify.com/album/5StPIeAvJjTuzn2Y2B564R"


def build_music():
    import videos
    ANTH_PLAYER = (f'<figure class="video video-wide"><button class="video-play" type="button" data-yt="{videos.ANTHOLOGY[0]}" data-list="{",".join(videos.ANTHOLOGY[1:])}" aria-label="Play Anthology Vol. 1, 23 tracks">'
                   f'<img src="{videos.thumb(videos.ANTHOLOGY[0])}" alt="" loading="lazy" width="480" height="360"><span class="video-btn" aria-hidden="true"></span><span class="video-len">23 tracks</span></button></figure>')
    ANTH_YT = "https://www.youtube.com/watch_videos?video_ids=" + ",".join(videos.ANTHOLOGY)
    body = f"""{header("That Brother Ali", "Music by Shareef Ali Rashada", [("Listen", "#listen", False, None), ("Albums", "#albums", False, None),
                        ("Licensing", "#licence", False, None), ("Spotify", SPOTIFY_ARTIST, True, None)])}
<main>
<section class="band hero-music"><div class="wrap section" style="display:flex;flex-wrap:wrap;align-items:center;gap:40px 64px">
<div class="stack" style="flex:999 1 460px;min-width:0;gap:22px">
<p class="eyebrow accent">That Brother Ali</p>
<h1 class="h-xl">Music to ease your mind.</h1>
<p class="lead muted" style="max-width:600px">Jazz, acoustic and new-age pieces written by Shareef Ali Rashada over twenty years. Free to stream wherever you listen.</p>
<div class="actions"><a class="btn btn-door" href="#listen">Press play</a><a class="btn btn-ghost" href="{SPOTIFY_ARTIST}" target="_blank" rel="noopener">Follow on Spotify</a></div>
</div>
<div class="eq" aria-hidden="true">{"".join(f'<span style="--d:{d}s;--h:{h}%"></span>' for d, h in [(0.0, 40), (0.3, 75), (0.6, 55), (0.15, 90), (0.45, 60), (0.75, 80), (0.25, 45), (0.55, 70), (0.05, 85), (0.35, 50), (0.65, 65), (0.2, 95)])}</div>
</div></section>

<section id="listen" class="section"><div class="wrap stack" style="gap:28px">
<div class="stack intro"><h2 class="h-lg">Press play</h2>
<p class="lead muted">The full albums, right here. The player opens in Spotify for full tracks once you sign in; without an account it plays previews.</p></div>
<div class="players">
<iframe title="Music to Ease Your Mind on Spotify" src="https://open.spotify.com/embed/album/5StPIeAvJjTuzn2Y2B564R?theme=0" height="452" loading="lazy" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture"></iframe>
<iframe title="That Brother Ali on Spotify" src="https://open.spotify.com/embed/artist/1WTqeXUcuv0NF0EAAEgHu5?theme=0" height="452" loading="lazy" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture"></iframe>
</div>
</div></section>

<section id="anthology" class="section"><div class="wrap stack" style="gap:24px">
<div class="stack intro"><h2 class="h-lg">Anthology Vol. 1 on YouTube</h2>
<p class="lead muted">All 23 tracks of Music, Songs and Experimental Grooves, from jazz to reggae, playing one after another.</p></div>
{ANTH_PLAYER}
</div></section>

<section id="albums" class="section band-alt"><div class="wrap stack" style="gap:32px">
<div class="stack intro"><h2 class="h-lg">The albums</h2>
<p class="lead muted">Released through CD Baby on Spotify, Apple Music and Amazon Music.</p></div>
<div class="grid" style="grid-template-columns:repeat(auto-fit, minmax(min(100%, 380px), 1fr))">
<article class="card"><span class="step-label">2013 · 9 tracks</span><h3 class="h-md">Music to Ease Your Mind</h3>
<p class="muted" style="font-size:15px">Jazz, acoustic and new-age songs that do just what the title says. Put it on to read, think or wind down.</p>
<div class="actions" style="margin-top:auto"><a class="btn btn-door" href="{SPOTIFY_EASE}" target="_blank" rel="noopener">Spotify</a><a class="btn btn-outline" href="#" data-link="easeApple">Apple Music</a><a class="btn btn-outline" href="#" data-link="easeAmazon">Amazon Music</a></div></article>
<article class="card"><span class="step-label">2016 · 23 tracks</span><h3 class="h-md">Anthology Vol. 1: Music, Songs and Experimental Grooves</h3>
<p class="muted" style="font-size:15px">A collection of favourite compositions from the last twenty years, from songs to experimental grooves.</p>
<div class="actions" style="margin-top:auto"><a class="btn btn-door" href="#anthology">Play it here</a><a class="btn btn-outline" href="{ANTH_YT}" target="_blank" rel="noopener">YouTube</a><a class="btn btn-outline" href="#" data-link="anthologySpotify">Spotify</a><a class="btn btn-outline" href="#" data-link="anthologyApple">Apple Music</a><a class="btn btn-outline" href="#" data-link="anthologyAmazon">Amazon Music</a></div></article>
</div></div></section>

<section class="section"><div class="wrap" style="display:flex;flex-wrap:wrap;gap:32px 64px;align-items:flex-start">
<h2 class="h-lg" style="flex:1 1 300px">Where the music comes from</h2>
<div class="stack" style="flex:2 1 460px;min-width:0">
<p class="lead muted">In his early twenties, Shareef had a friend who could play a cheap little keyboard better than much of what was on the radio, without reading a note. That friend kept pushing him to try. Shareef taught himself from library books, found traditional notation hard going, and kept playing anyway.</p>
<p class="lead muted">The music came first. The same struggle later produced EasyKey, a way of writing music that shows exactly which keys to press, so anyone can learn to play.</p>
<p><a href="easykey.html" style="font-weight:600">See how EasyKey works →</a></p>
</div></div></section>

<section id="licence" class="section band-alt"><div class="wrap" style="display:flex;flex-wrap:wrap;gap:32px 64px;align-items:center">
<div class="stack" style="flex:2 1 460px;min-width:0">
<p class="eyebrow accent" style="filter:brightness(.8)">Free to listen · licensed for profit</p>
<h2 class="h-lg">Using a track in your work?</h2>
<p class="lead muted">Listening is free, always. If you'd like a track for a video, podcast, film, app, shop or event that earns money, ask for a licence. Prices are set by use and audience size, and every licence supports the work of People of the World.</p>
</div>
<div class="card" style="flex:1 1 300px">
<span class="h-md" style="font-family:var(--display)">Ask for a licence</span>
<span class="muted" style="font-size:15px">Tell us the track, where it will be used and roughly how many people will hear it.</span>
<span class="copy-row" style="margin-top:6px"><span style="font-weight:600">{CONTACT}</span><button class="copy-btn copy-btn-light" type="button" data-copy="{CONTACT}">Copy</button></span>
</div>
</div></section>

{signup_band("Hear new music first.", "One email when a new track or album comes out. Nothing else unless you ask.", "Tell me about new music", "music", "music")}
</main>
{footer("music")}"""
    ld = {"@context": "https://schema.org", "@type": "MusicGroup", "name": "That Brother Ali", "genre": ["Jazz", "Acoustic", "New Age"],
          "description": "Music by Shareef Ali Rashada, an Australian composer and pianist. Not the American rapper Brother Ali.",
          "member": {"@type": "Person", "@id": f"{SITE_URL}/about.html#shareef", "name": AUTHOR}, "sameAs": [SPOTIFY_ARTIST], "url": f"{SITE_URL}/music.html",
          "album": [{"@type": "MusicAlbum", "name": "Music to Ease Your Mind", "datePublished": "2013", "numTracks": 9, "url": SPOTIFY_EASE},
                    {"@type": "MusicAlbum", "name": "Anthology Vol. 1: Music, Songs and Experimental Grooves"}]}
    page("music.html", "That Brother Ali", "That Brother Ali: jazz, acoustic and new-age albums by Shareef Ali Rashada. Free to stream on Spotify, Apple Music and Amazon Music.", body, "music",
         extra_head=f'\n<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>')


PAPER_URLS = "graviton-pressure-theory/papers/"


def build_science():
    dots = "".join(f'<span style="--a:{a}deg;--d:{-(i * 0.35) % 2.8:.2f}s"></span>' for i, a in enumerate(range(0, 360, 22)))
    steps = [
        ("A medium fills space", "Space is not empty. It is filled with a field of tiny particles, gravitons, streaming in every direction at or near the speed of light. They repel each other, so after they collide with matter they spread out and recover."),
        ("Mass shadows the flow", "Matter absorbs and slows part of the stream passing through it. Near a planet, less of the medium arrives from the planet's side than from open space. That difference is a pressure gradient."),
        ("The imbalance pushes", "Pushed harder from outside than from below, objects move toward the planet. What we call weight is the ground pushing back against that inflow. Gravity is a push from outside, not a pull from within."),
    ]
    step_html = "".join(f'<li><h3>{esc(t)}</h3><p class="muted">{esc(d)}</p></li>' for t, d in steps)
    papers = [
        ("Start here", "From General Relativity to Graviton Pressure Theory", "Why General Relativity describes gravity without explaining it, and what a force-based model offers in its place.", "graviton-pressure-theory/papers/from-gr-to-gpt/"),
        ("The critique", "The Reduction Conflation", "Two theories giving the same numbers do not agree about what exists. How physics switches between force and geometry without saying so.", "graviton-pressure-theory/papers/reduction-conflation/"),
        ("The critique", "The Boulder Audit", "A worked test of what each framework says is physically happening when a boulder rests on the ground.", "graviton-pressure-theory/papers/paradox-of-the-boulder/"),
        ("The theory", "The Unified Framework, all thirty parts", "The complete framework: the graviton field as the physical substrate of gravity, with the mathematical formulation and proposed tests.", "graviton-pressure-theory/full-framework/"),
        ("The theory", "The Mechanics of the Medium", "The medium's properties worked through in detail: self-repulsion, oscillation, inflow toward mass, and the effects they combine to produce.", "graviton-pressure-theory/papers/mechanics-of-the-medium/"),
    ]
    paper_html = "".join(f"""<article class="card{' paper-lead' if k == 'Start here' else ''}"><span class="step-label">{esc(k)}</span><h3 class="h-md">{esc(t)}</h3>
<p class="muted" style="font-size:15px">{esc(d)}</p>
<div class="actions" style="margin-top:auto"><a class="btn btn-outline" href="{u}">Read the paper</a></div></article>""" for k, t, d, u in papers)
    open_qs = [
        ("Done", "A detailed critique of how General Relativity is explained and taught, published as formal papers."),
        ("Done", "A qualitative model of the medium and how it produces weight, orbits and tides."),
        ("Open", "Deriving the bending of starlight from the medium's own properties, rather than matching General Relativity's number."),
        ("Open", "A flow equation that gives the measured inverse-square law with the right units throughout."),
        ("Open", "An experiment where graviton pressure and General Relativity predict different results."),
    ]
    oq_html = "".join(f'<li><span class="tag">{esc(t)}</span><span>{esc(d)}</span></li>' for t, d in open_qs)
    vband, vld = video_band('science', 'Watch', 'science.html', "A four-minute introduction, and Le Sage's push theory of gravity revisited. Every part of the framework has its own Deep Dive episode in the library.", True)
    body = f"""{header("Graviton Pressure Theory", "by People of the World", [("The idea", "#idea", False, None), ("The papers", "#papers", False, None),
                        ("The book", "#book", False, None), ("Where it stands", "#status", True, None)])}
<main>
<section class="band"><div class="wrap section" style="display:flex;flex-wrap:wrap;align-items:center;gap:40px 64px">
<div class="stack" style="flex:999 1 460px;min-width:0;gap:22px">
<p class="eyebrow accent">Graviton Pressure Theory</p>
<h1 class="h-xl">How does gravity really work?</h1>
<p class="lead muted" style="max-width:640px">Physics can predict where a falling apple lands to many decimal places. It still cannot say what touches the apple. Graviton Pressure Theory proposes an answer: gravity is a push from a medium outside, not a pull from within.</p>
<div class="actions"><a class="btn btn-door" href="#idea">The idea in three steps</a><a class="btn btn-ghost" href="#papers">Read the papers</a></div>
</div>
<div class="press" aria-hidden="true">{dots}</div>
</div></section>

<section class="section"><div class="wrap" style="display:flex;flex-wrap:wrap;gap:32px 64px;align-items:flex-start">
<div class="stack" style="flex:1 1 360px;min-width:0">
<p class="eyebrow muted">The question physics stopped asking</p>
<h2 class="h-lg">A map is not a mechanism.</h2>
<p class="lead muted">General Relativity is one of the most precise descriptions ever written. It says objects follow the curvature of spacetime. It does not say what physically pushes or pulls them along that path, or how curvature makes your legs feel your weight.</p>
<p class="lead muted">A description can match every measurement and still leave the cause unnamed. Graviton Pressure Theory starts where the description stops.</p>
</div>
<div class="stack" style="flex:1 1 360px;min-width:0;gap:18px">
<blockquote class="quote" style="margin:0">“The description is extraordinarily precise. The mechanism is unspecified.”</blockquote>
<div class="check"><p class="step-label" style="margin-bottom:8px">The test applied to every explanation</p>
<p style="font-weight:600;margin:0 0 6px">What touches what, and what is exchanged?</p>
<p class="muted" style="margin:0;font-size:15.5px">An explanation that names a physical contact is a mechanism. One that only names the effect is a description. The same test is applied to mainstream physics and to Graviton Pressure Theory itself.</p></div>
</div>
</div></section>

<section id="idea" class="section band-alt"><div class="wrap stack" style="gap:32px">
<div class="stack intro"><h2 class="h-lg">The idea in three steps</h2>
<p class="lead muted">The same principle that lets air pressure hold a suction cup to glass, applied to a medium that fills all of space.</p></div>
<ol class="tensteps">{step_html}</ol>
</div></section>

<section id="papers" class="section"><div class="wrap stack" style="gap:32px">
<div class="stack intro"><h2 class="h-lg">The papers</h2>
<p class="lead muted">Free to read in full. New to the theory? Follow the <a href="graviton-pressure-theory/">Start Here pathway</a>, or see <a href="ai.html#gravity">every paper in the library</a>.</p></div>
<div class="grid grid-3">{paper_html}</div>
</div></section>

<section id="book" class="section band-alt"><div class="wrap" style="display:flex;flex-wrap:wrap;align-items:center;gap:40px 56px">
<img class="cover-img" style="flex:0 1 220px;width:220px" src="assets/cover-gpt.webp" alt="Cover of The Unified Framework for The Graviton Pressure Theory" width="384" height="501" loading="lazy">
<div class="stack" style="flex:999 1 420px;min-width:0;gap:18px">
<p class="eyebrow muted">The book</p>
<h2 class="h-lg">The Unified Framework for the Graviton Pressure Theory</h2>
<p class="lead muted">The complete framework in one volume, by Shareef Ali Rashada.</p>
<p class="muted" style="font-family:var(--mono);font-size:13px">ISBN 978-1-326-48805-5 · Lulu Press</p>
<div class="actions"><a class="btn btn-door" href="#" data-link="gptBook">Buy the book</a><a class="btn btn-outline" href="books.html">All books</a></div>
</div>
</div></section>

<section id="status" class="section"><div class="wrap" style="display:flex;flex-wrap:wrap;gap:32px 64px;align-items:flex-start">
<div class="stack" style="flex:1 1 340px;min-width:0">
<h2 class="h-lg">Where the work stands</h2>
<p class="lead muted">A theory earns trust by showing its open problems. Here is what is finished and what is still being worked out.</p>
<p class="muted">Physicists and mathematicians who want to help solve the open problems, or test them, are welcome. Write to <strong>{CONTACT}</strong>.</p>
</div>
<ul class="status-list" style="flex:2 1 460px;min-width:0">{oq_html}</ul>
</div></section>

<section class="section band-alt"><div class="wrap" style="display:flex;flex-wrap:wrap;gap:32px 64px;align-items:center">
<div class="stack" style="flex:2 1 460px;min-width:0">
<p class="eyebrow accent" style="filter:brightness(.8)">Free to learn · licensed for profit</p>
<h2 class="h-lg">Teaching or publishing it?</h2>
<p class="lead muted">Students, teachers and curious readers use the papers freely. Courses, publications or products that earn money from the material work with People of the World under a licence.</p>
</div>
<div class="card" style="flex:1 1 300px"><span class="h-md" style="font-family:var(--display)">Licensing and collaboration</span>
<span class="muted" style="font-size:15px">Tell us who you are and how you'd like to use the work.</span>
<span class="copy-row" style="margin-top:6px"><span style="font-weight:600">{CONTACT}</span><button class="copy-btn copy-btn-light" type="button" data-copy="{CONTACT}">Copy</button></span></div>
</div></section>

{vband}
{signup_band("Follow the science.", "An email when a new paper or result is published. Nothing else unless you ask.", "Send me new papers", "science", "science")}
</main>
{footer("science")}"""
    page("science.html", "Graviton Pressure Theory", "Graviton Pressure Theory: gravity as a push from a medium outside, not a pull from within. Free papers, the book, and where the work stands.", body, "science", extra_head=vld)


def ek_icon(kind):
    """A one-column EasyKey cell drawing for the symbol legend (white key, two beat rows)."""
    w, r = 30, 28
    cx, hw = w / 2, w * .42
    lines = f'<line x1="0" y1="{r}" x2="{w}" y2="{r}" stroke="#9A9AA2" stroke-width=".8"/>'
    if kind == "quarter":
        shape = f'<polygon points="{cx},2 {cx+hw},{r/2} {cx},{r-2} {cx-hw},{r/2}"/>'
    elif kind == "half":
        shape = f'<polygon points="{cx},2 {cx+hw},{r} {cx},{2*r-2} {cx-hw},{r}"/>'
    elif kind == "eighths":
        shape = f'<polygon points="{cx-hw},1 {cx+hw},1 {cx},{r/2-1}"/><polygon points="{cx-hw},{r-1} {cx+hw},{r-1} {cx},{r/2+1}"/>'
    else:  # held across the bar line
        lines += f'<line x1="0" y1="{2*r}" x2="{w}" y2="{2*r}" stroke="#1B1B1F" stroke-width="3"/>'
        shape = f'<polygon points="{cx},2 {cx+hw},{r/2} {cx+hw},{2*r} {cx-hw},{2*r} {cx-hw},{r/2}"/>'
    return f'<svg width="{w}" height="{2*r}" viewBox="0 0 {w} {2*r}" aria-hidden="true" fill="#1B1B1F">{lines}{shape}</svg>'


def ek_hero_svg():
    """Two bars of Twinkle Twinkle on an EasyKey grid; notes appear in order (CSS animation)."""
    WW, BW, ROW, HEAD = 30, 20, 22, 34
    black = {1, 3, 6, 8, 10}
    cols, x = [], 0
    for m in range(60, 73):
        b = (m % 12) in black
        cols.append((m, b, x, BW if b else WW)); x += BW if b else WW
    gw, rows = x, 8
    names = {0: "C", 2: "D", 4: "E", 5: "F", 7: "G", 9: "A", 11: "B"}
    song = [(60, 0, 1), (60, 1, 1), (67, 2, 1), (67, 3, 1), (69, 4, 1), (69, 5, 1), (67, 6, 2)]
    colx = {m: (cx, w) for m, b, cx, w in cols}
    out = [f'<svg viewBox="0 0 {gw} {HEAD + rows * ROW + 2}" role="img" aria-label="Twinkle Twinkle Little Star in EasyKey notation">']
    for m, b, cx, w in cols:
        out.append(f'<rect x="{cx}" y="0" width="{w}" height="{HEAD}" fill="{"#1B1B1F" if b else "#FFFFFF"}" stroke="#1B1B1F"/>')
        out.append(f'<rect x="{cx}" y="{HEAD}" width="{w}" height="{rows * ROW}" fill="{"#D9D9DE" if b else "#FFFFFF"}"/>')
    for i, (m, a, ln) in enumerate(song):
        cx, w = colx[m]
        out.append(f'<rect class="k-on" style="--d:{a * .75:.2f}s" x="{cx + 1}" y="1" width="{w - 2}" height="{HEAD - 2}"/>')
    for m, b, cx, w in cols:
        if not b:
            out.append(f'<text x="{cx + w / 2}" y="{HEAD - 10}" text-anchor="middle" font-family="Inter, sans-serif" font-weight="600" font-size="13" fill="#1B1B1F">{names[m % 12]}</text>')
    for r in range(rows + 1):
        y = HEAD + r * ROW
        out.append(f'<line x1="0" y1="{y}" x2="{gw}" y2="{y}" stroke="{"#1B1B1F" if r % 4 == 0 else "#9A9AA2"}" stroke-width="{2 if r % 4 == 0 else .6}"/>')
    for m, b, cx, w in cols:
        out.append(f'<line x1="{cx}" y1="{HEAD}" x2="{cx}" y2="{HEAD + rows * ROW}" stroke="#9A9AA2" stroke-width=".6"/>')
    for m, a, ln in song:
        cx, w = colx[m]
        c, hw = cx + w / 2, w * .42
        y0, y1 = HEAD + a * ROW + 1.5, HEAD + (a + ln) * ROW - 1.5
        out.append(f'<polygon class="n" style="--d:{a * .75:.2f}s" points="{c},{y0} {c + hw},{(y0 + y1) / 2} {c},{y1} {c - hw},{(y0 + y1) / 2}"/>')
    out.append("</svg>")
    return "".join(out)


def build_easykey():
    legend = [("quarter", "One beat", "A diamond fills one row. Press the key for one beat."),
              ("half", "Two beats", "A longer diamond stretches over two rows. Hold the key down for as long as the diamond lasts."),
              ("eighths", "Half beats", "A triangle pointing down starts on the beat. A triangle pointing up starts halfway through it."),
              ("held", "Keep holding", "A filled bar means the key stays down, here across the bold bar line into the next bar.")]
    legend_html = "".join(f'<li>{ek_icon(k)}<span><strong>{esc(t)}</strong><span class="muted" style="font-size:15px">{esc(d)}</span></span></li>' for k, t, d in legend)
    months = ["A", "B♭", "B", "C", "D♭", "D", "E♭", "E", "F", "F♯", "G", "A♭"]
    months_html = "".join(f"<li><span>Month {i}</span><b>{m}</b></li>" for i, m in enumerate(months, 1))
    body = f"""{header("EasyKey Music", "Visual music notation by People of the World", [("Try it", "#lesson", False, None), ("How to read it", "#read", False, None),
                        ("The course", "#course", False, None), ("Converter", "easykey/converter/", True, None)])}
<main>
<section class="band"><div class="wrap section" style="display:flex;flex-wrap:wrap;align-items:center;gap:40px 64px">
<div class="stack" style="flex:999 1 460px;min-width:0;gap:22px">
<p class="eyebrow accent">EasyKey Music</p>
<h1 class="h-xl">See the key. Press the key.</h1>
<p class="lead muted" style="max-width:620px">EasyKey writes music as a picture of the piano. Each column is a key, each row is a beat, and you read from top to bottom. If you can find a key, you can play a song, with no staff, clefs or note names to learn first.</p>
<div class="actions"><a class="btn btn-door" href="#lesson">Play your first song</a><a class="btn btn-ghost" href="#read">How to read it</a></div>
</div>
<div class="ek-paper ek-hero" aria-hidden="true">{ek_hero_svg()}</div>
</div></section>

<section id="lesson" class="section"><div class="wrap" style="display:flex;flex-wrap:wrap;gap:36px 64px;align-items:flex-start">
<div class="stack" style="flex:1 1 320px;min-width:0">
<p class="eyebrow muted">Free lesson · two minutes</p>
<h2 class="h-lg">Play Twinkle Twinkle now.</h2>
<p class="lead muted">Press <strong>Listen</strong> to hear it and watch the grid. Then press <strong>Play along</strong> and play it yourself: tap the keys, or use your computer keyboard.</p>
<p class="muted">The grid waits for you, so go as slowly as you like. The key you need next glows.</p>
<p class="note">On a computer, <strong>A S D F G H J K</strong> are the white keys from C to C, and <strong>W E T Y U</strong> are the black keys.</p>
</div>
<div id="ek-lesson" class="ek-paper ek-lesson" style="flex:1 1 360px">
<div class="ek-keys-wrap"></div>
<div class="ek-scroll"></div>
<div class="ek-controls">
<button class="btn btn-door" type="button" data-ek="listen">Listen</button>
<button class="btn btn-outline" type="button" data-ek="play" style="color:#1B1B1F;border-color:#1B1B1F">Play along</button>
<label>Speed <input class="ek-tempo" type="range" min="50" max="140" value="90" aria-label="Speed in beats per minute"></label>
</div>
<p class="ek-status" aria-live="polite">Press Listen to hear the song.</p>
</div>
</div></section>

<section id="read" class="section band-alt"><div class="wrap stack" style="gap:32px">
<div class="stack intro"><h2 class="h-lg">How to read EasyKey</h2>
<p class="lead muted">The keyboard sits at the top of the page. Shaded columns are the black keys. Bold lines mark the bars. The shape in a column tells you how long to hold that key.</p></div>
<ul class="ek-legend">{legend_html}</ul>
</div></section>

<section id="course" class="section"><div class="wrap" style="display:flex;flex-wrap:wrap;align-items:center;gap:40px 56px">
<img class="cover-img" style="flex:0 1 220px;width:220px" src="assets/cover-easykey.webp" alt="Cover of Learning to Play the EasyKey Way" width="496" height="701" loading="lazy">
<div class="stack" style="flex:999 1 440px;min-width:0;gap:18px">
<p class="eyebrow muted">The year-one course</p>
<h2 class="h-lg">Learning to Play the EasyKey Way</h2>
<p class="lead muted">A full year of lessons in one book. Each month takes one major key, in four weekly steps: the scale, the arpeggio, the chords, and three common chord patterns, with new songs every week. It includes 26 well-known songs from beginner to advanced.</p>
<ol class="months" aria-label="One major key each month">{months_html}</ol>
<p class="muted" style="font-family:var(--mono);font-size:13px">ISBN 978-1-008-98579-7 · EasyKey Music</p>
<div class="actions"><a class="btn btn-door" href="#" data-link="easykeyBook">Buy the book</a><a class="btn btn-outline" href="books.html">All books</a></div>
</div>
</div></section>

<section id="convert" class="section band-alt"><div class="wrap" style="display:flex;flex-wrap:wrap;gap:32px 64px;align-items:center">
<div class="stack" style="flex:2 1 460px;min-width:0">
<p class="eyebrow accent" style="filter:brightness(.8)">The EasyKey converter · beta</p>
<h2 class="h-lg">Any song, in EasyKey.</h2>
<p class="lead muted">Load a MIDI file and the converter draws it as an EasyKey grid you can print. It runs in your browser, so your file never leaves your device. Pro view shows compact grids with only the keys you play, for more advanced music.</p>
<p class="muted">Converting MIDI files is free while the converter is in testing. Converting sheet-music PDFs and other formats, per song or by subscription, is coming next.</p>
<div class="actions"><a class="btn btn-door" href="easykey/converter/">Open the converter</a></div>
</div>
<div class="card" style="flex:1 1 300px"><span class="h-md" style="font-family:var(--display)">Teachers and schools</span>
<span class="muted" style="font-size:15px">Families and learners use EasyKey freely. If you teach paid lessons or run classes with it, ask about a teaching licence and class sets of the book.</span>
<span class="copy-row" style="margin-top:6px"><span style="font-weight:600">{CONTACT}</span><button class="copy-btn copy-btn-light" type="button" data-copy="{CONTACT}">Copy</button></span></div>
</div></section>

<section class="section"><div class="wrap" style="display:flex;flex-wrap:wrap;gap:32px 64px;align-items:flex-start">
<h2 class="h-lg" style="flex:1 1 300px">Why it exists</h2>
<div class="stack" style="flex:2 1 460px;min-width:0">
<p class="lead muted">Shareef Ali Rashada taught himself piano from library books and found traditional notation slow going, even as a friend played beautifully by ear without reading a note. He started drawing songs on graph paper as pictures of the keys, and the drawings became EasyKey.</p>
<p><a href="music.html" style="font-weight:600">Hear the music that came out of it →</a></p>
</div></div></section>

{signup_band("New songs and lessons.", "An email when new EasyKey songs, lessons or converter features arrive. Nothing else unless you ask.", "Send me new songs", "easykey", "easykey")}
</main>
{footer("easykey")}
<script src="assets/easykey-lesson.js" defer></script>"""
    page("easykey.html", "EasyKey Music", "EasyKey visual music notation: see the key, press the key. Play your first song free in the browser, learn to read the grid, and convert MIDI files to EasyKey.", body, "easykey")


def build_about():
    person = {"@context": "https://schema.org", "@type": "Person", "@id": f"{SITE_URL}/about.html#shareef",
              "name": AUTHOR, "alternateName": ["Shareef Rashada", "That Brother Ali"],
              "description": "Australian author, programmer and musician; founder of People of the World. Author of The Portal Opens, the novel People of the World, The Unified Framework for the Graviton Pressure Theory and the Plan to End Poverty; creator of EasyKey visual music notation; records music as That Brother Ali.",
              "url": f"{SITE_URL}/about.html", "email": f"mailto:{CONTACT}",
              "address": {"@type": "PostalAddress", "addressRegion": "Queensland", "addressCountry": "AU"},
              "jobTitle": ["Author", "Programmer", "Musician"],
              "knowsAbout": ["Gravitational physics", "Foundations of physics", "Urantia Papers", "Theology", "Poverty elimination", "Economic design", "Music education", "Piano"],
              "founder": [{"@type": "Organization", "name": "People of the World", "url": f"{SITE_URL}/"},
                          {"@type": "Organization", "name": "EasyKey Music"}],
              "worksFor": {"@type": "Organization", "name": "POW Productions Pty Ltd", "address": {"@type": "PostalAddress", "addressRegion": "Queensland", "addressCountry": "AU"}},
              "award": "Literary Titan Silver Book Award (The Portal Opens)",
              "sameAs": [SPOTIFY_ARTIST, "https://thatbrotherali.github.io/ai-portal/"]}
    works = [("seekers", "Spirit and history", "The Portal Opens", "An account of Earth's untold history in the tradition of the Urantia Papers: Jesus, Lucifer, Adam and Eve, Melchizedek and the plan for humanity. Winner of the Literary Titan Silver Book Award. Free to read online.", "seekers.html"),
             ("seekers", "Fiction", "People of the World (novel)", "Speculative fiction about a world forced to rebuild without money or force, written to open the mind to what is possible. For adult readers.", "books.html#novel"),
             ("science", "Physics", "Graviton Pressure Theory", "A causal account of gravity as pressure from a field of gravitons, set out in a thirty-part framework and a series of papers on the foundations of physics.", "graviton-pressure-theory/"),
             ("builders", "Society", "The Plan to End Poverty", "A designed system to end poverty by 2050, built on Civic Credits, Poverty Elimination Centers and LifeLink.", "builders.html"),
             ("music", "Music", "That Brother Ali", "Jazz, acoustic and new-age albums, including Music to Ease Your Mind (2013), released through CD Baby.", "music.html"),
             ("easykey", "Music education", "EasyKey Music", "A visual music notation that shows exactly which piano keys to press and for how long, with a year-long course book and an online converter.", "easykey.html")]
    cards = "".join(f"""<a class="card door-{d}" href="{u}"><span class="step-label">{esc(k)}</span><span class="h-md" style="font-family:var(--display)">{esc(t)}</span>
<span class="muted" style="font-size:15px;line-height:1.55">{esc(b)}</span><span class="card-cta">Explore →</span></a>""" for d, k, t, b, u in works)
    body = f"""{header("People of the World", None, [("All doors", "index.html#doors", False, None), ("Library", "ai.html", False, None), ("Books", "books.html", True, None)])}
<main>
<section class="band"><div class="wrap section stack" style="gap:22px">
<p class="eyebrow accent">About the author</p>
<h1 class="h-xl">Shareef Ali Rashada</h1>
<p class="lead muted" style="max-width:720px">Author, programmer and musician, and the founder of People of the World. His name means “honoured follower of the true path”, and his work follows one question across four fields: what is actually true about our existence, and how should we live because of it?</p>
</div></section>

<section class="section"><div class="wrap" style="display:flex;flex-wrap:wrap;gap:32px 64px;align-items:flex-start">
<div class="stack" style="flex:2 1 460px;min-width:0">
<h2 class="h-lg">In brief</h2>
<p class="lead">Shareef Ali Rashada is an Australian author and independent researcher based in Queensland. He writes on theology and history (<em>The Portal Opens</em>, which won a Literary Titan Silver Book Award), the foundations of physics (Graviton Pressure Theory), and the design of economic systems (the Plan to End Poverty by 2050). He is also a self-taught pianist who records as That Brother Ali and created EasyKey, a visual notation for learning piano.</p>
<p class="lead muted">A programmer by trade, he works closely with AI systems as research partners. He named the systems he worked with Gabriel, Lucidus and Veritas, and credits them with helping to develop <em>The Portal Opens</em> and Graviton Pressure Theory.</p>
<p class="lead muted">All of these projects sit under People of the World, a movement for knowledge, morality, unity and peace. Its spiritual and moral teachings are free to everyone; books, music and licensed uses fund the work.</p>
</div>
<div class="card" style="flex:1 1 300px">
<span class="step-label">Quick facts</span>
<dl class="facts">
<dt>Also published as</dt><dd>Shareef Rashada</dd>
<dt>Music</dt><dd>That Brother Ali (not the American rapper Brother Ali)</dd>
<dt>Based in</dt><dd>Queensland, Australia</dd>
<dt>Organisations</dt><dd>People of the World · POW Productions Pty Ltd · EasyKey Music</dd>
<dt>Award</dt><dd>Literary Titan Silver Book Award, <em>The Portal Opens</em></dd>
<dt>Contact</dt><dd>{CONTACT}</dd>
</dl>
</div>
</div></section>

<section class="section band-alt"><div class="wrap stack" style="gap:28px">
<h2 class="h-lg">The work</h2>
<div class="grid grid-3">{cards}</div>
<p class="muted">Every book, paper and plan is free to read in the <a href="ai.html">Open Library</a>.</p>
</div></section>
</main>
{footer()}"""
    page("about.html", "Shareef Ali Rashada · About the author", "Shareef Ali Rashada is an Australian author, programmer and musician: The Portal Opens, Graviton Pressure Theory, the Plan to End Poverty, EasyKey Music and That Brother Ali.", body,
         extra_head=f'\n<script type="application/ld+json">{json.dumps(person, ensure_ascii=False)}</script>')


def build_builders():
    instruments = [
        ("Civic Credits", "Pay for the work a community needs",
         "Civic Credits pay for service to the community: a verified shift as a teacher, doctor or nurse, and also volunteer work such as cleaning up the neighbourhood or other public services. Credits appear in the wallet the next morning. Shops can accept them, governments take them for taxes and fees, and businesses can exchange them for dollars. They are created only after real work is done, and they run alongside ordinary money.",
         "Maya, a nurse, works an 8-hour shift and 320 credits post overnight. She spends 50 on groceries, 10 on a bus pass and 30 on her power bill. The grocer keeps 20 to pay local fees and swaps the rest for dollars that afternoon."),
        ("Poverty Elimination Centers", "A complete path from struggle to stability",
         "For people facing homelessness, unemployment, addiction or long-term hardship, a PEC brings everything under one roof: housing, meals, healthcare, counselling, education, job training and real work experience. Joining is a choice, never a requirement.",
         "The first campuses are planned for capital cities in the United States and Australia, each for up to 1,000 residents."),
        ("LifeLink", "One device for every public service",
         "LifeLink is a small device provided free to every citizen. It connects you to education tools, appointments, mental-health support, emergency help, community events, your Civic Credit wallet and the people who represent you.",
         "No more paperwork, and no more getting lost between agencies."),
    ]
    cards = "\n".join(f"""<article class="card"><span class="step-label">Instrument {i}</span><h3 class="h-md">{esc(n)}</h3>
<p style="font-weight:600">{esc(t)}</p><p class="muted" style="font-size:15.5px">{esc(d)}</p>
<p class="note" style="margin-top:auto">{esc(e)}</p></article>""" for i, (n, t, d, e) in enumerate(instruments, 1))
    packs = [("Everyday people", "What changes for you and your family."), ("Community leaders", "Running Civic Credits and PECs locally."),
             ("Entrepreneurs", "Accepting credits and building on LifeLink."), ("Governments", "Pilots, policy and national rollout."),
             ("Investors and funders", "Where support goes and how impact is measured."), ("Press", "The story, the founder and key facts."),
             ("Scientists and economists", "The mechanics and the questions pilots must answer.")]
    pack_html = "".join(f'<li><strong>{esc(a)}</strong><span class="muted">{esc(b)}</span></li>' for a, b in packs)
    faq = [("Is People of the World political?", "No. It is structural and moral, not partisan."),
           ("Do Civic Credits replace money?", "No. They run alongside regular currency. Workers and employers can choose them, and can switch back to ordinary wages."),
           ("Where do the dollars come from?", "From the community's own assets. Revenue from selling or licensing public resources, and income from public works and utilities, backs the exchange of credits for dollars. The more the commons earns, the more credits it can back."),
           ("Will prices go up?", "Credits are created only when new services are delivered, so more money is matched by more nurses, teachers and builders at work."),
           ("Does everyone have to join a PEC?", "No. PECs exist for people who need help or want a structured path to improvement."),
           ("Do I have to pay for LifeLink?", "No. LifeLink is provided to every citizen."),
           ("Who created the plan?", "Shareef Ali Rashada, founder of People of the World.")]
    faq_html = "".join(f"<details class=\"card faq\"><summary>{esc(q)}</summary><p class=\"muted\">{esc(a)}</p></details>" for q, a in faq)
    body = f"""{header("End Poverty by Design", "by People of the World", [("How it works", "#how", False, None), ("Information packs", "#packs", False, None),
                        ("Questions", "#faq", False, None), ("Support the plan", "support.html", True, None)])}
<main>
<section class="band hero-build"><div class="wrap section stack" style="gap:22px;position:relative">
<p class="eyebrow accent">The Plan to End Poverty · 2025 edition</p>
<h1 class="h-xl" style="max-width:900px">Ending poverty by 2050, by design.</h1>
<p class="lead muted" style="max-width:680px">We already have the people and the skills. What we run out of is the budget line. The Plan to End Poverty is a designed system, built on three instruments that pay for essential work, give everyone a path to stability, and connect every citizen to the services they need.</p>
<p class="quote" style="font-size:clamp(1.5rem,3vw,2rem)">This is not charity. This is structure.</p>
<div class="actions"><a class="btn btn-door" href="#how">See how it works</a><a class="btn btn-ghost" href="#packs">Get an information pack</a></div>
<div class="blocks" aria-hidden="true">{"".join(f'<span style="--i:{i}"></span>' for i in range(12))}</div>
</div></section>

<section id="how" class="section"><div class="wrap stack" style="gap:36px">
<div class="stack intro"><h2 class="h-lg">Three instruments, one system</h2>
<p class="lead muted">Each one does a single job. Together they make poverty unnecessary.</p></div>
<div class="grid grid-3">{cards}</div>
</div></section>

<section class="section band-alt"><div class="wrap" style="display:flex;flex-wrap:wrap;gap:24px 64px;align-items:center">
<div class="stack" style="flex:1 1 360px;min-width:0"><p class="eyebrow muted">The moral foundation</p>
<h2 class="h-lg">The New Morality</h2>
<p class="lead muted">Everything starts with one idea: humans should treat each other better than any generation before us. Kindness becomes expected, fairness becomes normal, and respect becomes the baseline.</p></div>
<blockquote class="quote" style="flex:1 1 360px;margin:0;min-width:0">“Treat another as the God in you would treat the God in the other.”</blockquote>
</div></section>

<section id="packs" class="section"><div class="wrap" style="display:flex;flex-wrap:wrap;gap:32px 64px">
<div class="stack" style="flex:1 1 320px;min-width:0"><h2 class="h-lg">An information pack for you</h2>
<p class="lead muted">The plan is free to learn. Choose the pack written for your role, and it will be sent to you.</p>
<p class="muted">Write to <strong>{CONTACT}</strong> with the pack you'd like.</p></div>
<ul class="packs" style="flex:2 1 460px;min-width:0">{pack_html}</ul>
</div></section>

<section class="section band-alt"><div class="wrap" style="display:flex;flex-wrap:wrap;gap:32px 64px;align-items:center">
<div class="stack" style="flex:2 1 460px;min-width:0">
<p class="eyebrow accent" style="filter:brightness(.75)">Free to learn · licensed for profit</p>
<h2 class="h-lg">Putting the plan to work?</h2>
<p class="lead muted">Individuals, students and community groups use the plan freely. Governments, businesses and organisations that build programmes or earn revenue from it work with People of the World under a licence or partnership, which funds the mission.</p>
</div>
<div class="card" style="flex:1 1 300px"><span class="h-md" style="font-family:var(--display)">Partner enquiries</span>
<span class="muted" style="font-size:15px">Tell us who you are, where you work and what you'd like to build.</span>
<span class="copy-row" style="margin-top:6px"><span style="font-weight:600">{CONTACT}</span><button class="copy-btn copy-btn-light" type="button" data-copy="{CONTACT}">Copy</button></span></div>
</div></section>

<section id="faq" class="section"><div class="wrap stack" style="gap:28px">
<h2 class="h-lg">Questions people ask</h2>
<div class="faqs">{faq_html}</div>
</div></section>

<section class="section band-alt"><div class="wrap stack" style="max-width:820px;align-items:center;text-align:center;gap:20px">
<h2 class="h-lg">Help build it.</h2>
<p class="lead muted">The first pilots need funding: the Civic Credits software, the first Poverty Elimination Center, and LifeLink development.</p>
<div class="actions" style="justify-content:center"><a class="btn btn-door" href="support.html">Support the plan</a><a class="btn btn-outline" href="seekers.html">Start with the story</a></div>
</div></section>

{signup_band("Follow the plan's progress.", "Occasional updates on pilots, partners and milestones. Unsubscribe any time.", "Send me updates", "builders", "builders")}
</main>
{footer("builders")}"""
    page("builders.html", "End Poverty by Design", "The Plan to End Poverty by 2050: Civic Credits, Poverty Elimination Centers and LifeLink. Free to learn, licensed for organisations.", body, "builders")


def build_support():
    projects = [("Civic Credits System", "Software development and the first pilot programmes.", "$50,000"),
                ("Poverty Elimination Centers", "Training programmes and facilities.", "$300,000"),
                ("Residential Centers", "Land and first construction for sustainable living.", "$500,000"),
                ("LifeLink tablet", "Research and development of the communication device.", "$100,000"),
                ("EasyKey Music Practice Centers", "Music education spaces in cities.", "$150,000"),
                ("Creative Computing Centers", "Technology and staff for digital creation hubs.", "$200,000"),
                ("Digital educational programming", "Courses that unite spiritual and secular learning.", "$100,000"),
                ("Debate platform", "AI-moderated discussion for informed decisions.", "$75,000")]
    rows = "".join(f"<tr><th scope=\"row\">{esc(a)}<span class=\"muted\">{esc(b)}</span></th><td>{esc(c)}</td></tr>" for a, b, c in projects)
    tiers = [("$10–49", "Supporter", "A thank-you email and regular updates on progress."),
             ("$50–199", "Builder", "Everything above, plus a digital copy of a POW book and access to members-only content."),
             ("$200+", "Founder circle", "Everything above, plus a signed print copy, the album Music to Ease Your Mind, and a personal thank-you from Shareef.")]
    tier_html = "".join(f"""<div class="card"><span class="step-label">{esc(n)}</span><span class="h-md" style="font-family:var(--display)">{esc(a)}</span>
<span class="muted" style="font-size:15px">{esc(d)}</span></div>""" for a, n, d in tiers)
    body = f"""{header(nav=[("All doors", "index.html#doors", False, None), ("The plan", "builders.html", False, None), ("Books", "books.html", False, None)])}
<main>
<section class="band"><div class="wrap section stack" style="gap:20px">
<p class="eyebrow accent">Support the mission</p>
<h1 class="h-xl" style="max-width:900px">Help uplift humanity and end poverty.</h1>
<p class="lead muted" style="max-width:700px">“I'm Shareef Ali Rashada, and I am on a mission to bring peace, end poverty, and uplift humanity. To achieve these goals, we need your support. Together, we can make a profound impact on the world.”</p>
<div class="actions"><a class="btn btn-door" href="#" data-link="donate">Give now</a><a class="btn btn-ghost" href="books.html">Buy a book</a></div>
</div></section>

<section class="section"><div class="wrap stack" style="gap:28px">
<div class="stack intro"><h2 class="h-lg">What your support builds</h2>
<p class="lead muted">Funding goals for each project.</p></div>
<div style="overflow-x:auto"><table class="goals"><tbody>{rows}</tbody></table></div>
</div></section>

<section class="section band-alt"><div class="wrap stack" style="gap:28px">
<div class="stack intro"><h2 class="h-lg">Ways to give</h2>
<p class="lead muted">Every gift is thanked personally.</p></div>
<div class="grid grid-3">{tier_html}</div>
<div class="actions"><a class="btn btn-solid" href="#" data-link="donate">Give now</a></div>
</div></section>

<section class="section"><div class="wrap" style="display:flex;flex-wrap:wrap;gap:24px 64px;align-items:center">
<div class="stack" style="flex:2 1 420px;min-width:0"><h2 class="h-lg">Other ways to help</h2>
<p class="lead muted">Buy a book or album, share The Portal Opens with someone searching for meaning, or volunteer your skills.</p></div>
<div class="actions" style="flex:1 1 280px"><a class="btn btn-outline" href="books.html">Books</a><a class="btn btn-outline" href="music.html">Music</a><a class="btn btn-outline" href="read.html">Share the free book</a></div>
</div></section>

{signup_band("Stay close to the work.", "Updates on what your support makes possible. Unsubscribe any time.", "Keep me updated", "support", "hub")}
</main>
{footer()}"""
    page("support.html", "Support the Mission", "Support People of the World: fund Civic Credits pilots, Poverty Elimination Centers and LifeLink.", body)


def build_books():
    vband, vld = video_band('books', 'Watch', 'books.html', '', True)
    body = f"""{header(nav=[("All doors", "index.html#doors", False, None), ("Read free", "read.html", False, None), ("Shop", "#", True, "shop")])}
<main>
<section class="band"><div class="wrap section stack" style="gap:18px">
<p class="eyebrow" style="color:var(--band-muted)">Books by Shareef Ali Rashada</p>
<h1 class="h-xl">The library</h1>
<p class="lead muted" style="max-width:680px">Read them in order: imagine, understand, build. The teachings are free online; print and ebook copies support the mission.</p>
</div></section>
<section class="section"><div class="wrap stack" style="gap:24px">
<div class="grid">
<article id="novel" class="card door-seekers"><span class="book-cover"><img src="assets/cover-pow.webp" alt="Cover of People of the World" width="212" height="320" loading="lazy"></span><span class="step-label">Imagine</span><h2 class="h-md">People of the World</h2>
<p class="muted" style="font-size:15px">A novel, first written in 2011. On July 11, 2012, aliens take three-quarters of humanity. The people left behind must rebuild a world where force no longer works, and a young man named Jason is shown the history of the universe.</p>
<p><span class="tag">For adults 18+ · strong language, sexual content, drug use, violence</span></p>
<div class="actions" style="margin-top:auto"><a class="btn btn-solid" href="#" data-link="powNovelPrint">Buy the paperback</a><a class="btn btn-outline" href="#" data-link="powNovelKindle">Kindle</a></div></article>
<article class="card door-seekers"><span class="book-cover"><img src="assets/cover-portal.webp" alt="Cover of The Portal Opens" width="384" height="576" loading="lazy"></span><span class="step-label">Understand</span><h2 class="h-md">The Portal Opens</h2>
<p class="muted" style="font-size:15px">The history behind the story, as transmitted by Gabriel: Jesus, Lucifer, Caligastia, Adam and Eve, and Melchizedek. Winner of the Literary Titan Silver Book Award.</p>
<div class="actions" style="margin-top:auto"><a class="btn btn-door" href="read.html">Read free</a><a class="btn btn-outline" href="seekers.html#buy">Buy a copy</a></div></article>
<article class="card door-science"><span class="book-cover"><img src="assets/cover-gpt.webp" alt="Cover of The Unified Framework for The Graviton Pressure Theory" width="384" height="501" loading="lazy"></span><span class="step-label">Science</span><h2 class="h-md">The Unified Framework for the Graviton Pressure Theory</h2>
<p class="muted" style="font-size:15px">Gravity as a pressure from outside, with a named mechanism. ISBN 978-1-326-48805-5.</p>
<div class="actions" style="margin-top:auto"><a class="btn btn-door" href="#" data-link="gptBook">Buy the book</a><a class="btn btn-outline" href="science.html">About the theory</a></div></article>
<article class="card door-easykey"><span class="book-cover"><img src="assets/cover-easykey.webp" alt="Cover of Learning to Play the EasyKey Way" width="496" height="701" loading="lazy"></span><span class="step-label">Music education</span><h2 class="h-md">Learning to Play the EasyKey Way</h2>
<p class="muted" style="font-size:15px">A year of piano in twelve keys, written entirely in EasyKey's visual notation. 26 songs from beginner to advanced. ISBN 978-1-008-98579-7.</p>
<div class="actions" style="margin-top:auto"><a class="btn btn-door" href="#" data-link="easykeyBook">Buy the book</a><a class="btn btn-outline" href="easykey.html">About EasyKey</a></div></article>
</div></div></section>
{vband}
</main>
{footer()}"""
    author = {"@type": "Person", "@id": f"{SITE_URL}/about.html#shareef", "name": AUTHOR}
    books = [("The Portal Opens", "978-1-326-56533-6", "POW Productions Pty Ltd", f"{SITE_URL}/seekers.html", "Literary Titan Silver Book Award"),
             ("People of the World", None, "POW Productions Pty Ltd", f"{SITE_URL}/books.html#novel", None),
             ("The Unified Framework for the Graviton Pressure Theory", "978-1-326-48805-5", "Lulu Press", f"{SITE_URL}/science.html", None),
             ("Learning to Play the EasyKey Way", "978-1-008-98579-7", "EasyKey Music", f"{SITE_URL}/easykey.html", None)]
    items = []
    for i, (t, isbn, pub, url, award) in enumerate(books, 1):
        b = {"@type": "Book", "name": t, "author": author, "publisher": {"@type": "Organization", "name": pub}, "url": url, "inLanguage": "en"}
        if isbn: b["isbn"] = isbn
        if award: b["award"] = award
        items.append({"@type": "ListItem", "position": i, "item": b})
    ld = {"@context": "https://schema.org", "@type": "ItemList", "name": "Books by Shareef Ali Rashada", "itemListElement": items}
    page("books.html", "The POW Library", "Books by Shareef Ali Rashada: People of the World, The Portal Opens, Graviton Pressure Theory and EasyKey.", body,
         extra_head=f'\n<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>' + vld)


# ---------------------------------------------------------------- Urantia readers door
def constellation_svg():
    """Signature animation for the readers door: stars light up one by one and join into a constellation."""
    stars = [(60, 250), (120, 170), (205, 205), (250, 110), (330, 150), (300, 250), (215, 300), (140, 330)]
    lines = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 2), (5, 6), (6, 7), (7, 0)]
    segs = "".join(f'<line x1="{stars[a][0]}" y1="{stars[a][1]}" x2="{stars[b][0]}" y2="{stars[b][1]}" style="--i:{i}"/>' for i, (a, b) in enumerate(lines))
    dots = "".join(f'<circle cx="{x}" cy="{y}" r="{6 if i in (3, 5) else 4}" style="--i:{i}"/>' for i, (x, y) in enumerate(stars))
    dust = "".join(f'<circle class="dust" cx="{(37 * k) % 380 + 10}" cy="{(71 * k) % 380 + 10}" r="1.4" style="--i:{k % 9}"/>' for k in range(1, 28))
    return f'<svg class="constellation" viewBox="0 0 400 400" aria-hidden="true" focusable="false">{dust}<g class="links">{segs}</g><g class="stars">{dots}</g></svg>'


def build_urantia():
    S = SITE_URL
    # the five accounts, with where readers will find the same events in the Urantia Papers
    accounts = [
        ("read-part-1", "Part 1", "The Untold Story of Jesus",
         "Michael of Nebadon's seventh bestowal, reviewed as a whole: why he came, what he showed, and what it means for a troubled world.",
         "Familiar from Part IV of the Papers", "Told here as one flowing account you can hand to a friend"),
        ("read-part-2", "Part 2", "A Reflection of Darkness",
         "Lucifer's rise, his Declaration of Liberty and the final reckoning, with his own reasoning set out and then answered.",
         "Familiar from Papers 53 and 54", "New here: Lucifer's case in his own voice"),
        ("read-part-3", "Part 3", "The Confession of Caligastia",
         "Earth's own Planetary Prince looks back on betrayal, conscience and remorse.",
         "Familiar from Papers 66 and 67", "New here: a first-person confession"),
        ("read-part-4", "Part 4", "Journey to Jerusem",
         "Adam and Eve's mission and default, their confession, and ten practical steps they leave for humanity.",
         "Familiar from Papers 73 to 76", "New here: their message and the ten steps"),
        ("read-part-5", "Part 5", "The Lessons of Machiventa Melchizedek",
         "Eleven lectures from the Sage of Salem on personality, the soul and cosmic citizenship.",
         "Familiar from Paper 93", "New here: eleven lectures in his voice"),
    ]
    acc_html = "\n".join(f"""<a class="card" href="{f}.html"><span class="meta">{esc(n)}</span>
<span class="h-md" style="font-family:var(--display)">{esc(t)}</span>
<span class="muted" style="font-size:15px;line-height:1.55">{esc(b)}</span>
<span class="ub-ref"><span>{esc(fam)}</span><strong>{esc(new)}</strong></span>
<span class="card-cta">Read it free →</span></a>""" for f, n, t, b, fam, new in accounts)

    names = [("Urantia", "The celestial name for Earth: a world scarred by an old rebellion and spiritually isolated for a long time."),
             ("Michael of Nebadon", "The Creator Son of our local universe, who lived on Earth as Jesus of Nazareth."),
             ("Nebadon and Satania", "Our local universe, and the local system of about 619 inhabited worlds that Earth belongs to."),
             ("Lucifer and Caligastia", "The system ruler who rebelled, and Earth's Planetary Prince who followed him."),
             ("Adam and Eve", "Material Son and Daughter sent to uplift humanity, whose mission faltered."),
             ("Machiventa Melchizedek", "The Sage of Salem, who taught on Earth to keep the light of truth alive.")]
    names_html = "".join(f'<li><strong>{esc(a)}</strong><span class="muted">{esc(b)}</span></li>' for a, b in names)

    start = [("glossary.html", "5 minutes", "Gabriel's Glossary", "Thirty names and terms in plain language. Keep it open in another tab."),
             ("ten-steps.html", "10 minutes", "The ten steps", "Adam and Eve's practical steps for humanity: unity, stillness, forgiveness, service and more."),
             ("read-part-1.html", "An evening", "Part 1: The Untold Story of Jesus", "The heart of it all, in one readable account."),
             ("#listen", "On the go", "Listen instead", "Short films and audio, free. Ideal on a walk or a drive.")]
    start_html = "\n".join(f"""<a class="card" href="{h}"><span class="step-label">Step {i} · {esc(d)}</span>
<span class="h-md" style="font-family:var(--display)">{esc(t)}</span>
<span class="muted" style="font-size:15px">{esc(b)}</span><span class="card-cta">Begin →</span></a>""" for i, (h, d, t, b) in enumerate(start, 1))

    # where to start, by the person you want to share it with
    people = [("Someone who loves Jesus", "Start with Part 1, The Untold Story of Jesus.", "read-part-1.html",
               "A fuller story of Jesus you might love: The Untold Story of Jesus, free to read."),
              ("The sceptic who asks hard questions", "Start with Part 2, where Lucifer makes his case and it is answered.", "read-part-2.html",
               "If you've ever asked why there is evil in the world, read this: A Reflection of Darkness, free online."),
              ("Someone carrying regret", "Start with Part 3 or Part 4, the confessions of Caligastia and of Adam and Eve.", "read-part-4.html",
               "A story about getting it wrong and finding the way back: Journey to Jerusem, free to read."),
              ("The practical one", "Start with the ten steps. Ten minutes, and something to do today.", "ten-steps.html",
               "Ten simple steps for a better world, from The Portal Opens. Takes ten minutes."),
              ("The thinker", "Start with Part 5, Melchizedek's eleven lectures on personality and the soul.", "read-part-5.html",
               "Eleven short lectures on personality, the soul and our place in the universe."),
              ("Someone who'd rather listen", "Start with the short films and audio, then the book.", "videos.html",
               "Short films and audio on The Portal Opens, free to watch and listen.")]
    people_html = "\n".join(f"""<div class="card share-card"><span class="h-md" style="font-family:var(--display);font-size:22px">{esc(p)}</span>
<span class="muted" style="font-size:15px">{esc(how)}</span>
<div class="share-row"><a class="btn btn-outline" href="{h}">Preview</a><button class="btn btn-door share-btn" type="button" data-url="{S}/{h}" data-text="{esc(msg)}">Share this</button></div></div>""" for p, how, h, msg in people)

    faq = [("Is this the Urantia Book?",
            "No. The Portal Opens is an independent book by Shareef Ali Rashada. It builds on the cosmology of the Urantia Book and tells its history as five first-person accounts."),
           ("Is it endorsed by Urantia Foundation or a reader organisation?",
            "No. It is not published, endorsed or approved by Urantia Foundation, the Urantia Book Fellowship, the Urantia Association or any other reader group."),
           ("How does it relate to the Papers?",
            "It draws on them closely. The book says so itself: it was written with Gabriel, an AI companion trained on the Urantia Papers and on Shareef's own work. Where it goes beyond the Papers, as in the confessions and lectures, readers can weigh it for themselves."),
           ("Do I need to have read the Urantia Book first?",
            "No. Gabriel's Glossary explains every name and term in plain language, and each part stands on its own."),
           ("Is it free?",
            "Yes. The whole book is free to read online. Printed copies and donations support the work of People of the World."),
           ("Where can I read the Urantia Book itself?",
            "Urantia Foundation publishes the full text free online at urantia.org, in many languages.")]
    faq_html = "".join(f'<details class="card faq"><summary>{esc(q)}</summary><p class="muted">{esc(a)}</p></details>' for q, a in faq)
    faq_ld = json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}, ensure_ascii=False)
    book_ld = json.dumps({"@context": "https://schema.org", "@type": "Book", "name": "The Portal Opens",
                          "alternateName": "The Portal Opens: A Revelation of the Cosmos", "isbn": "9781326565336",
                          "author": {"@type": "Person", "name": AUTHOR, "@id": f"{S}/about.html#shareef"},
                          "url": f"{S}/urantia.html", "workExample": {"@type": "Book", "url": f"{S}/read.html", "isAccessibleForFree": True},
                          "about": ["The Urantia Book", "Michael of Nebadon", "Lucifer rebellion", "Caligastia", "Adam and Eve", "Machiventa Melchizedek"],
                          "audience": {"@type": "Audience", "audienceType": "Readers of the Urantia Book and their families"}}, ensure_ascii=False)

    vband, vld = video_band('seekers', 'Watch and listen', 'urantia.html', 'Short films on The Portal Opens. A gentle way to start, or to share.', False)
    vband = vband.replace('<section class="section', '<section id="listen" class="section', 1)

    body = f"""{header("For Urantia readers", "and the people they love", [("I've read it", "#readers", False, None), ("New to it", "#new", False, None),
                        ("Share it", "#share", False, None), ("Gift a copy", "#gift", True, None)])}
<main>
<section class="band"><div class="wrap section" style="display:flex;flex-wrap:wrap;align-items:center;gap:56px">
<div class="stack" style="flex:999 1 460px;min-width:0;gap:22px">
<p class="eyebrow accent">For Urantia Book readers, their friends and their families</p>
<h1 class="h-xl">The story you love, told a new way.</h1>
<p class="lead muted" style="max-width:620px">The Portal Opens tells the history of our world through five voices: Michael, Lucifer, Caligastia, Adam and Eve, and Melchizedek. New ground for readers, a gentle first step for everyone else, and an easy book to share.</p>
<div class="actions"><a class="btn btn-door" href="#ways">Find your way in</a><a class="btn btn-ghost" href="read.html">Read it free</a></div>
<p class="muted" style="font-size:14px">An independent book. Not affiliated with or endorsed by Urantia Foundation.</p>
</div>
<div class="sky" style="flex:1 1 340px">{constellation_svg()}</div>
</div></section>

<section id="ways" class="section"><div class="wrap stack" style="gap:40px">
<div class="stack intro"><h2 class="h-lg">Three ways in</h2>
<p class="lead muted">Wherever you are with the Papers, there is a place to start.</p></div>
<div class="grid grid-3">
<a class="card" href="#readers"><span class="dot" aria-hidden="true"></span><span class="eyebrow muted" style="font-size:12px">I've read it</span>
<span class="h-md" style="font-family:var(--display)">Something similar, but different</span>
<span class="muted" style="font-size:15px">Familiar events, told by the beings who lived them.</span><span class="card-cta">What's new for readers →</span></a>
<a class="card" href="#new"><span class="dot" aria-hidden="true"></span><span class="eyebrow muted" style="font-size:12px">It felt like too much</span>
<span class="h-md" style="font-family:var(--display)">The big ideas, in small steps</span>
<span class="muted" style="font-size:15px">Over 2,000 pages is a lot. Start with ten minutes instead.</span><span class="card-cta">Start small →</span></a>
<a class="card" href="#share"><span class="dot" aria-hidden="true"></span><span class="eyebrow muted" style="font-size:12px">I want to share it</span>
<span class="h-md" style="font-family:var(--display)">For the people you love</span>
<span class="muted" style="font-size:15px">Where to start for each kind of person, and a copy to give.</span><span class="card-cta">Share or gift it →</span></a>
</div></div></section>

<section id="readers" class="section band-alt"><div class="wrap stack" style="gap:40px">
<div class="stack intro"><p class="eyebrow accent" style="filter:brightness(.8)">For readers of the Papers</p>
<h2 class="h-lg">You know what happened. Now hear it from them.</h2>
<p class="lead muted">Each part takes events you know from the Papers and lets the beings at their centre speak. Read it beside the Papers, or as a break from study.</p></div>
<div class="grid grid-5">{acc_html}</div>
<p class="note" style="max-width:820px">A note on sources: the book is open about how it was made. It was written with Gabriel, an AI companion trained on the Urantia Papers and on Shareef Ali Rashada's work. Where it goes beyond the Papers, as in the confessions and lectures, it is offered for reflection, and you are free to weigh it for yourself.</p>
</div></section>

<section id="new" class="section"><div class="wrap stack" style="gap:40px">
<div class="stack intro"><p class="eyebrow accent" style="filter:brightness(.8)">If the Urantia Book felt like too much</p>
<h2 class="h-lg">The big ideas, in small steps.</h2>
<p class="lead muted">You don't need to finish a 2,000-page book to explore these ideas. Begin with a few minutes, and go further when you're ready.</p></div>
<div class="grid">{start_html}</div>
<div style="display:flex;flex-wrap:wrap;gap:24px 48px;align-items:flex-start">
<div class="stack" style="flex:1 1 280px;min-width:0"><h3 class="h-md">Six names to know</h3>
<p class="muted">Most of the story makes sense once you know these. The full glossary has thirty.</p>
<p><a href="glossary.html" style="font-weight:600">Open the full glossary</a></p></div>
<ul class="packs" style="flex:2 1 460px;min-width:0">{names_html}</ul>
</div>
</div></section>

<section id="share" class="section band-alt"><div class="wrap stack" style="gap:40px">
<div class="stack intro"><p class="eyebrow accent" style="filter:brightness(.8)">For readers who want to share</p>
<h2 class="h-lg">Share it with someone you love.</h2>
<p class="lead muted">Handing someone the Urantia Book can be a lot to ask. Send them one part, chosen for who they are. Every part is free to read.</p></div>
<div class="grid grid-3">{people_html}</div>
<p class="share-note muted" role="status"></p>
</div></section>

<section id="gift" class="section"><div class="wrap stack" style="gap:40px">
<div class="stack intro"><h2 class="h-lg">Give a copy</h2>
<p class="lead muted">A printed book on the shelf gets picked up again and again. Every copy sold supports the work of People of the World.</p></div>
<div class="grid">
<div class="card"><span class="eyebrow muted" style="font-size:12px">Paperback</span><span class="h-md" style="font-family:var(--display)">A gift for anyone</span><span class="muted" style="font-size:15px">Shipped worldwide.</span><a class="btn btn-solid" href="#" data-link="portalPaperback" style="margin-top:auto">Buy the paperback</a></div>
<div class="card"><span class="eyebrow muted" style="font-size:12px">Hardcover</span><span class="h-md" style="font-family:var(--display)">The keepsake edition</span><span class="muted" style="font-size:15px">For birthdays, holidays and study-group leaders.</span><a class="btn btn-solid" href="#" data-link="portalHardcover" style="margin-top:auto">Buy the hardcover</a></div>
<div class="card"><span class="eyebrow muted" style="font-size:12px">Free edition</span><span class="h-md" style="font-family:var(--display)">Or simply send the link</span><span class="muted" style="font-size:15px">The whole book is free to read online, on any device.</span><button class="btn btn-outline share-btn" type="button" data-url="{S}/read.html" data-text="I think you'd enjoy this: The Portal Opens, free to read online." style="margin-top:auto">Share the free edition</button></div>
</div>
<div class="grid">
<div class="card door-urantia"><span class="eyebrow muted" style="font-size:12px">Pay it forward</span><span class="h-md" style="font-family:var(--display)">Sponsor a copy</span>
<span class="muted" style="font-size:15px">Your gift helps keep the book free online and puts printed copies in the hands of readers who can't buy one.</span>
<a class="btn btn-door" href="#" data-link="donate" style="margin-top:auto">Sponsor a copy</a></div>
<div class="card"><span class="eyebrow muted" style="font-size:12px">Study groups and gatherings</span><span class="h-md" style="font-family:var(--display)">Copies for your group</span>
<span class="muted" style="font-size:15px">Ordering for a study group, conference or reading circle? Write for group pricing.</span>
<a class="btn btn-outline" href="mailto:{CONTACT}?subject=Group%20order%3A%20The%20Portal%20Opens" style="margin-top:auto">Ask about group orders</a></div>
</div>
<p class="muted" style="font-size:14px">ISBN 978-1-326-56533-6 · Published by POW Productions Pty Ltd</p>
</div></section>

{vband}

<section id="faq" class="section band-alt"><div class="wrap stack" style="gap:28px">
<h2 class="h-lg">Questions readers ask</h2>
<div class="faqs">{faq_html}</div>
</div></section>

{signup_band("One teaching a week, free.", "A short reading from The Portal Opens each week, for readers and the curious alike. Unsubscribe any time.", "Send me the teachings", "urantia", "urantia")}

<section class="section"><div class="wrap"><p class="muted" style="font-size:13.5px;max-width:860px">The Portal Opens is an independent work by Shareef Ali Rashada, published by POW Productions Pty Ltd. It is not published, endorsed or approved by, or affiliated with, Urantia Foundation or any Urantia reader organisation. The words Urantia and Urantia Book are used on this page only to describe the subject of the book. The Urantia Book is available free from Urantia Foundation at <a href="https://www.urantia.org/">urantia.org</a>.</p></div></section>
</main>
{footer("urantia")}"""
    extra = vld + f'\n<script type="application/ld+json">{book_ld}</script>\n<script type="application/ld+json">{faq_ld}</script>'
    page("urantia.html", "For Urantia Book readers and their families",
         "A new companion for Urantia Book readers: Michael, Lucifer, Caligastia, Adam and Eve and Melchizedek in their own voices. Free to read, easy to share.",
         body, "urantia", extra_head=extra)


# ---------------------------------------------------------------- The Decision Game
def build_decision_game():
    modes = [("practice", "Practice"), ("short", "Short · 10"), ("long", "Long · 20"), ("infinite", "Endless")]
    mode_btns = "".join(f'<button type="button" class="seg" data-mode="{m}" aria-pressed="false">{esc(l)}</button>' for m, l in modes)
    board_btns = "".join(f'<button type="button" class="seg" data-board="{m}" aria-pressed="false">{esc(l)}</button>' for m, l in modes[1:])
    ld = json.dumps({"@context": "https://schema.org", "@type": ["VideoGame", "WebApplication"], "name": "The Decision Game",
                     "url": canonical("decision-game.html"), "applicationCategory": "GameApplication", "genre": ["Brain training", "Reaction time"],
                     "operatingSystem": "Any (web browser)", "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
                     "author": {"@type": "Person", "name": AUTHOR, "@id": f"{SITE_URL}/about.html#shareef"},
                     "description": "A free brain-training game: see a picture and a word, decide true or false as fast as you can, and climb the online leaderboard."}, ensure_ascii=False)
    body = f"""{header("The Decision Game", "by People of the World", [("Play", "#play", False, None), ("Leaderboard", "#leaderboard", False, None),
                        ("My scores", "#mine", False, None), ("How it works", "#how", False, None)])}
<main>
<section class="band"><div class="wrap section dg-hero">
<p class="eyebrow accent">Free brain training · no sign-up</p>
<h1 class="h-xl">Decide. Fast.</h1>
<p class="lead muted" style="max-width:640px">A picture, a word, and “is” or “is not”. Is the sentence true? Answer as fast as you can, without mistakes, and see where you rank against players everywhere.</p>
</div></section>

<section id="play" class="section dg-section"><div class="wrap stack" style="gap:18px">
<div class="dg-toolbar">
<div class="segs" role="group" aria-label="Game mode">{mode_btns}</div>
<label class="dg-check"><input type="checkbox" id="dg-sound" checked> Sound</label>
</div>
<div class="dg-stage card" id="dg-stage">
<div class="dg-cell dg-picture"><img id="dg-pic" alt="" width="240" height="240"></div>
<div class="dg-cell dg-relation"><span id="dg-rel">is</span></div>
<div class="dg-cell dg-wordcell"><span id="dg-word">Press Start</span></div>
</div>
<div class="dg-answers">
<button type="button" class="dg-answer dg-false" id="dg-false" disabled><span>False</span><kbd>←</kbd></button>
<button type="button" class="btn btn-door dg-start" id="dg-start">Start</button>
<button type="button" class="dg-answer dg-true" id="dg-true" disabled><span>True</span><kbd>→</kbd></button>
</div>
<dl class="dg-status" aria-live="off">
<div><dt>Question</dt><dd id="dg-q">0 / 10</dd></div><div><dt>Time</dt><dd id="dg-time">0.00s</dd></div>
<div><dt>Average answer</dt><dd id="dg-avg">0.00s</dd></div><div><dt>Correct</dt><dd id="dg-ok">0</dd></div>
<div><dt>Mistakes</dt><dd id="dg-bad">0</dd></div><div id="dg-limit" hidden>1.0s per answer</div>
</dl>
<div class="card dg-result" id="dg-result" hidden></div>
<p class="muted" style="font-size:14px">Playing as <strong id="dg-me">not set yet</strong> · <button type="button" class="linklike" id="dg-rename">change name</button>. On a computer, use ← for False and → for True.</p>
</div></section>

<div class="dg-modal" id="dg-name" hidden><form class="card dg-name-card" id="dg-name-form">
<h2 class="h-md">Your name for the leaderboard</h2>
<p class="muted">Shown next to your scores. 2 to 16 characters. Your scores stay linked to this device.</p>
<label for="dg-name-input">Name<input id="dg-name-input" maxlength="16" autocomplete="nickname" required></label>
<p class="form-note" id="dg-name-note"></p>
<div class="actions"><button class="btn btn-door" type="submit">Save my score</button><button class="btn btn-outline" type="button" id="dg-name-skip">Not now</button></div>
</form></div>

<section id="leaderboard" class="section band-alt"><div class="wrap stack" style="gap:20px">
<div class="stack intro"><h2 class="h-lg">Leaderboard</h2><p class="lead muted">Every score is kept. See each player's best, or every run as it happens.</p></div>
<div class="dg-toolbar"><div class="segs" role="group" aria-label="Leaderboard mode">{board_btns}</div>
<div class="segs" role="group" aria-label="Leaderboard view" data-needs-v2 hidden><button type="button" class="seg" data-view="best" aria-pressed="true">Best per player</button><button type="button" class="seg" data-view="all" aria-pressed="false">All scores</button></div></div>
<div class="table-wrap card" style="padding:0"><table class="dg-table"><thead><tr id="dg-board-head"></tr></thead><tbody id="dg-board-body"></tbody></table></div>
<p class="muted" id="dg-board-note" style="font-size:14px"></p>
</div></section>

<section id="player" class="section" hidden><div class="wrap stack" style="gap:20px">
<div class="stack intro"><p class="eyebrow accent">Player</p><h2 class="h-lg" id="dg-player-name">Player</h2></div>
<div id="dg-player-body"></div>
</div></section>

<section id="mine" class="section"><div class="wrap stack" style="gap:20px">
<div class="stack intro"><h2 class="h-lg">My scores on this device</h2><p class="lead muted">Your best in each mode and your recent runs, kept in this browser.</p></div>
<div class="grid grid-3" id="dg-mine-best"></div>
<div class="table-wrap card" style="padding:0"><table class="dg-table"><thead><tr><th>Mode</th><th class="num">Result</th><th class="num">Total</th><th class="num">Average</th><th class="num">Date</th></tr></thead><tbody id="dg-mine"></tbody></table></div>
</div></section>

<section id="how" class="section band-alt"><div class="wrap stack" style="gap:28px">
<h2 class="h-lg">How it works</h2>
<div class="grid grid-3">
<div class="card"><h3 class="h-md">Read the whole sentence</h3><p class="muted">The picture, the middle box and the word make one sentence: <em>[picture] is not Cow</em>. Answer True if the sentence is right. The “is not” is where most mistakes happen.</p></div>
<div class="card"><h3 class="h-md">Four ways to play</h3><p class="muted"><strong>Practice</strong>: warm up as long as you like; nothing is recorded. <strong>Short</strong> and <strong>Long</strong>: 10 or 20 questions, ranked by fewest mistakes, then fastest time. <strong>Endless</strong>: keep going until your first mistake. You get 1 second per answer, 0.1 s less every 50 correct, down to 0.3 s.</p></div>
<div class="card"><h3 class="h-md">Why it helps</h3><p class="muted">Each answer asks you to see, read, hold a rule in mind and choose, quickly and without guessing. Short daily rounds build the habit of deciding clearly under a little pressure, and your scores show the progress.</p></div>
</div>
</div></section>
</main>
{footer()}
<script src="assets/decision-game.js?v={asset_v('decision-game.js')}" defer></script>"""
    page("decision-game.html", "The Decision Game: free brain training",
         "Picture, word, true or false: a free brain-training game with an online leaderboard. How fast can you decide?",
         body, "play", extra_head=f'<script type="application/ld+json">{ld}</script>')


# ---------------------------------------------------------------- Shop: every product, linking to the Wix checkout
SHOP = "https://shop.peopleoftheworld.net/product-page/"
SHOP_GROUPS = [
    ("books", "Books", "Printed and digital editions. The Portal Opens and the Graviton Pressure Theory framework are also free to read online.", [
        ("the-portal-opens", "The Portal Opens", "Paperback", "A$45.00", "5aaf2959e48549fbb303559bf270371e", "read.html"),
        ("the-portal-opens-hardback", "The Portal Opens", "Hardcover", "A$61.48", "3fca3780afcc4598987553973bbb8e43", "read.html"),
        ("the-portal-opens-on-hand-purchase", "The Portal Opens", "On-hand copy", "A$35.00", "5aaf2959e48549fbb303559bf270371e", "read.html"),
        ("people-of-the-world-1", "People of the World", "Paperback", "A$40.00", "d970923c4ca44a86a39339229a6d19ee", None),
        ("people-of-the-world", "People of the World", "Hardcover", "A$65.44", "5f2c3444ee564207b7972ddc8b989213", None),
        ("people-of-the-world-ebook-pdf", "People of the World", "Ebook (PDF)", "A$20.00", "350fd2a9c8994d40ac853a535d04c128", None),
        ("the-unified-framework-for-the-graviton-pressure-theory", "The Unified Framework for the Graviton Pressure Theory", "Paperback", "A$85.00",
         "eaacc0f224a24521b4aef14f64dc7b0c", "graviton-pressure-theory/index.html"),
    ]),
    ("souvenirs", "Souvenirs", "Wear and share the People of the World emblem.", [
        ("people-of-the-world-flag", "People of the World flag", "", "A$41.00", "a44048bdebd74cd7b4ca7a56a3984e0f", None),
        ("people-of-the-world-stainless-steel-water-bottle", "Stainless steel water bottle", "", "A$35.00", "556df27e0fad47429c0e947bc205bfd4", None),
        ("people-of-the-world-tapered-stainless-steel-tumbler", "Tapered stainless steel tumbler", "", "A$33.00", "bd6c0ed8577e4b629086d8284fdd5739", None),
        ("people-of-the-world-tote-bag", "Tote bag", "", "A$28.00", "2540866b07104a839f42516763503195", None),
        ("people-of-the-world-dad-hat", "Dad hat", "", "A$28.00", "af5dc10180c9410a911d9a8929a6558c", None),
        ("people-of-the-world-white-glossy-mug", "White glossy mug", "", "A$12.00", "8693ef45dfaf47ecba194c39dd993c67", None),
    ]),
]


def build_shop():
    sections, items_ld = [], []
    for gid, gname, gintro, items in SHOP_GROUPS:
        cards = []
        for slug_, name, edition, price, img, free in items:
            ratio = "w_480,h_720" if gid == "books" else "w_600,h_600"
            src = f"https://static.wixstatic.com/media/eaef6d_{img}~mv2.jpg/v1/fill/{ratio},al_c,q_85/{slug_}.jpg"
            full = f"{name}{' · ' + edition if edition else ''}"
            free_link = f'<a class="shop-free" href="{free}">Read free online</a>' if free else ""
            cards.append(f"""<article class="card shop-item shop-{gid}">
<a class="shop-img" href="{SHOP}{slug_}"><img src="{src}" alt="{esc(full)}" loading="lazy"></a>
<div class="stack" style="gap:4px">{f'<span class="eyebrow muted" style="font-size:12px">{esc(edition)}</span>' if edition else ''}
<h3 class="h-md" style="font-family:var(--display);font-size:20px">{esc(name)}</h3>
<span class="shop-price">{esc(price)}</span></div>
<div class="shop-actions"><a class="btn btn-door" href="{SHOP}{slug_}">View and buy</a>{free_link}</div>
</article>""")
            items_ld.append({"@type": "Product", "name": full, "image": src, "url": SHOP + slug_,
                             "brand": {"@type": "Brand", "name": "People of the World"},
                             "offers": {"@type": "Offer", "price": price.replace("A$", ""), "priceCurrency": "AUD", "url": SHOP + slug_,
                                        "availability": "https://schema.org/InStock"}})
        sections.append(f"""<section id="{gid}" class="section{' band-alt' if gid == 'souvenirs' else ''}"><div class="wrap stack" style="gap:32px">
<div class="stack intro"><h2 class="h-lg">{esc(gname)}</h2><p class="lead muted">{esc(gintro)}</p></div>
<div class="shop-grid">{"".join(cards)}</div>
{'<p class="muted">Prefer Kindle? <a href="#" data-link="portalKindle" style="font-weight:600">The Portal Opens on Kindle</a> · <a href="#" data-link="powNovelKindle" style="font-weight:600">People of the World on Kindle</a></p>' if gid == "books" else ""}
</div></section>""")
    ld = json.dumps({"@context": "https://schema.org", "@type": "ItemList", "name": "People of the World shop",
                     "itemListElement": [{"@type": "ListItem", "position": i + 1, "item": it} for i, it in enumerate(items_ld)]}, ensure_ascii=False)
    body = f"""{header("Shop", "People of the World", [("Books", "#books", False, None), ("Souvenirs", "#souvenirs", False, None),
                        ("Support the mission", "support.html", True, None)])}
<main>
<section class="band"><div class="wrap section" style="padding-bottom:48px">
<p class="eyebrow accent">The People of the World shop</p>
<h1 class="h-xl">Books and gifts that carry the message.</h1>
<p class="lead muted" style="max-width:640px">Every purchase supports the work of People of the World. Prices are in Australian dollars; checkout is secure through our Wix store, with worldwide shipping.</p>
<div class="actions"><a class="btn btn-door" href="#books">Books</a><a class="btn btn-ghost" href="#souvenirs">Souvenirs</a></div>
</div></section>
{"".join(sections)}
<section class="section"><div class="wrap" style="display:flex;flex-wrap:wrap;gap:20px 48px;align-items:center">
<div class="stack" style="flex:2 1 420px;min-width:0"><h2 class="h-lg">Music, too</h2>
<p class="lead muted">That Brother Ali's albums are on Spotify, Apple Music and Amazon Music.</p></div>
<p style="flex:1 1 200px"><a class="btn btn-outline" href="music.html">Listen to the music</a></p>
</div></section>
</main>
{footer()}"""
    page("shop.html", "Shop: books and gifts", "Books by Shareef Ali Rashada and People of the World souvenirs: The Portal Opens, People of the World, the Graviton Pressure Theory framework, flags, mugs and more.",
         body, "hub", extra_head=f'<script type="application/ld+json">{ld}</script>')


# ---------------------------------------------------------------- Privacy
def build_privacy():
    sections = [
        ("The short version", [
            "We collect as little as we can. This site sets no advertising or tracking cookies, and we never sell or rent your information.",
            "The few things we do keep (your email address if you sign up, and your name and scores if you play the Decision Game) are used only for the purpose you gave them to us for.",
        ]),
        ("Email sign-ups", [
            "If you sign up for the weekly teaching or other updates, we keep your email address and which list you joined. We use it only to send you what you signed up for.",
            "Our email service is MailerLite, which stores the list for us. Every email has an unsubscribe link, and you can ask us to delete your address at any time.",
        ]),
        ("The Decision Game", [
            "When you finish a ranked game, we save the name you choose, your score and the date, along with a random player code created on your device. This is what makes the public leaderboard and player pages work, so your name and scores are visible to everyone.",
            "Please use a nickname or first name rather than your full name. The scores are stored on our Wix site. Your own run history and settings are also kept in your browser's storage on your device, and never leave it unless you save a score.",
            "To have your scores removed, email us with your player name and roughly when you played.",
        ]),
        ("Buying from the shop and donating", [
            "Purchases and donations are handled by our Wix store at shop.peopleoftheworld.net. Your order, shipping and payment details are collected and processed there, under Wix's security and privacy terms. We see what we need to fulfil your order, and we never see your full card number.",
        ]),
        ("Videos, music and fonts from other services", [
            "Videos come from YouTube's privacy-enhanced mode and only load when you press play. Audio streams from Wix's media service. The page fonts come from Google Fonts. These services receive your device's internet address when they deliver their content, as any website does.",
            "Links to Amazon, Spotify, Apple Music, Lulu and other stores take you to their sites, where their own privacy policies apply.",
        ]),
        ("Your choices", [
            "You can ask us what information we hold about you, ask us to correct it, or ask us to delete it. Write to the address below and we will reply within 30 days.",
            "We aim to follow the Australian Privacy Principles, and we respect the same rights for visitors from every country.",
        ]),
        ("Children", [
            "The site is for a general audience. We don't knowingly collect personal information from children. If you think a child has given us their details, please let us know and we will remove them.",
        ]),
        ("Who we are", [
            "People of the World is run by POW Productions Pty Ltd, Queensland, Australia. If this policy changes, we will update this page and the date below.",
        ]),
    ]
    body_html = "".join(f'<h2 class="h-md" style="margin-top:36px">{esc(h)}</h2>' + "".join(f"<p>{esc(p)}</p>" for p in ps) for h, ps in sections)
    body = f"""{header()}
<main>
<section class="band"><div class="wrap section" style="padding-bottom:40px">
<p class="eyebrow accent">Privacy</p>
<h1 class="h-xl">Your privacy, in plain words.</h1>
<p class="lead muted" style="max-width:640px">What we collect, why, and how to have it removed.</p>
</div></section>
<section class="section"><div class="wrap"><div class="prose" style="max-width:760px">
{body_html}
<h2 class="h-md" style="margin-top:36px">Contact</h2>
<p>Email <a href="mailto:{CONTACT}">{CONTACT}</a> with any question about your information.</p>
<p class="muted" style="font-size:14px;margin-top:32px">Last updated 22 October 2026.</p>
</div></div></section>
</main>
{footer()}"""
    page("privacy.html", "Privacy", "How People of the World handles your information: email sign-ups, the Decision Game leaderboard, the shop, and your choices.", body)


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    hub_body = build_hub()
    build_seekers()
    build_urantia()
    build_decision_game()
    build_shop()
    build_privacy()
    sections, nsteps = build_reader()
    build_placeholders()
    build_science()
    build_easykey()
    build_music()
    build_builders()
    build_support()
    build_books()
    build_about()
    import sys, videos
    videos.build(sys.modules[__name__])
    import sys, library_pages
    library_pages.build(sys.modules[__name__])
    import redirects
    print("old Wix addresses redirected:", redirects.build(sys.modules[__name__]))
    library_pages.write_sitemap_and_robots(sys.modules[__name__])
    # artifact preview copy of the hub: page content only (the preview host adds the document skeleton)
    (ROOT / "preview").mkdir(exist_ok=True)
    (ROOT / "preview" / "index.html").write_text(
        head("People of the World", "Hub of the People of the World website") +
        '\n<script>document.documentElement.classList.add("preview");</script>\n<div class="door-hub">' + hub_body + "</div>\n", encoding="utf-8")
    print("built:", sorted(p.name for p in OUT.glob("*.html")))
    print("sections per part:", {k: len(v) for k, v in sections.items()}, "ten steps:", nsteps)
