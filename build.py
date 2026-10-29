#!/usr/bin/env python3
"""Builds the People of the World website into ./docs (the folder GitHub Pages publishes)

Run:  python3 build.py
Everything in ./docs is plain HTML/CSS/JS and can be uploaded to any host (GitHub Pages, Netlify, etc.).
The free online edition of The Portal Opens is generated from src/portal.txt.
"""
import html, re, pathlib, json
import audiobook

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
     "Why we search, the voice within, and the thread through every faith. Free weekly teachings and The Portal Opens, free to read.",
     "Begin here"),
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
DOOR_NAMES = {"seekers": "The Search for Meaning", "urantia": "For Urantia readers", "science": "Graviton Pressure Theory", "builders": "End Poverty by Design",
              "music": "That Brother Ali", "easykey": "EasyKey Music", "ai": "The Open Library"}

esc = lambda s: html.escape(s, quote=True)
AWARD_IMG = "https://static.wixstatic.com/media/eaef6d_6fee9686863c430c812048ab0654fdf4~mv2.jpg/v1/fit/w_640,h_640,q_85/literary-titan-silver-book-award.jpg"


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
<script src="assets/site.js?v={asset_v('site.js')}" defer></script>
<script data-goatcounter="https://peopleoftheworld.goatcounter.com/count" async src="https://gc.zgo.at/count.js"></script>"""


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
<nav class="col" aria-label="The wider mission"><strong>The wider mission</strong><a href="index.html">The hub</a>{doors}<a href="videos.html">Videos</a><a href="play.html">Brain training games</a><a href="about.html">About Shareef</a></nav>
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
                 "read.html": "seekers", "audiobook.html": "seekers", "glossary.html": "seekers", "ten-steps.html": "seekers", "videos.html": "site", "about.html": "site"}


def share_image(fname, door):
    """Which link-preview picture a page uses (made by tools/make_share_images.py)."""
    if fname in SHARE_BY_PAGE: return SHARE_BY_PAGE[fname]
    if fname.startswith(("graviton-pressure-theory/", "library/graviton")): return "science"
    if door in ("seekers", "urantia", "science", "builders", "music", "easykey", "ai", "play"): return door
    return "site"


# ---------------------------------------------------------------- "The why": a quiet link on the pages where people reach the end of a door
WHY = {
    "seekers.html": "The voice within has a name in this work: the Thought Adjuster, a fragment of the Creator now given to every person. That is why the search never ends, and why it matters.",
    "ten-steps.html": "Each step is a way of listening more closely to the presence within. Why that presence is now in every one of us, and what it asks of us, is the heart of everything here.",
    "read-closing.html": "The story ends with a choice that is now before every person. Why that choice is open to all of us, and how it shapes everything People of the World does:",
    "urantia.html": "Since Pentecost, the Spirit of Truth has been poured out on all humanity, and every normal-minded person receives a Thought Adjuster. People of the World is built on what that means for how we live: the New Morality.",
    "builders.html": "Why end poverty? Because every person carries a portion of the Creator, and a life spent only on survival leaves little room to hear it.",
    "plan-to-end-poverty/civic-credits/index.html": "Why pay for the work a community needs? Because every person carries a portion of the Creator, and no one should be kept from it by the struggle to survive.",
    "plan-to-end-poverty/poverty-elimination-centers/index.html": "Why a complete path out of hardship? Because every person carries a portion of the Creator, and deserves the room to grow toward it.",
    "plan-to-end-poverty/lifelink/index.html": "Why connect every person? Because every person matters: each one carries a portion of the Creator.",
    "music.html": "Music to ease your mind: stillness is where the voice within is most easily heard.",
    "easykey.html": "Creating is one of the ways we grow. EasyKey exists so that anyone, at any age, can make music.",
    "easykey/centers/index.html": "Why gather a community around music? Because creating together, and serving one another, is how we grow toward unity.",
    "science.html": "People of the World seeks truth in every field, physics included. The physics papers make physical claims only; why the project exists at all is a separate question, answered here.",
    "ai.html": "The library is open to everyone, because truth belongs to everyone.",
    "support.html": "Every project you support serves one goal. Here is why.",
    "about.html": "Every project here serves one goal. Here is why.",
}
SIGNUP_MARK = '<section class="band door-'


def why_band(text):
    return f"""<section class="section why-band"><div class="wrap" style="max-width:780px">
<p class="eyebrow muted">The why</p>
<p class="lead muted">{esc(text)}</p>
<p><a href="why.html" style="font-weight:600">Why it all connects →</a></p>
</div></section>
"""


def add_why(fname, body):
    text = WHY.get(fname)
    if not text or "why-band" in body:
        return body
    end = body.rfind("</main>")
    if end < 0:
        return body
    k = body.rfind(SIGNUP_MARK, 0, end)
    k = k if k > 0 and "signup" in body[k:end] else end
    return body[:k] + why_band(text) + body[k:]


def page(fname, title, desc, body, door="hub", extra_head="", lastmod=None):
    """Full HTML document for the real website. fname may be in a sub-folder, e.g. 'graviton-pressure-theory/index.html'."""
    body = add_why(fname, body)
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
    extra = ('<p class="muted" style="margin-top:18px">Prefer to listen? The Deep Dive is also a podcast: '
             '<a href="https://open.spotify.com/show/65h2giWS1p2cJnIKn61KsY" target="_blank" rel="noopener" style="font-weight:600">'
             'follow it on Spotify</a> or see <a href="videos.html#listen" style="font-weight:600">all episodes</a>.</p>') if place == "science" else ""
    return f'<section class="section{" band-alt" if alt else ""}"><div class="wrap">{sec}{extra}</div></section>', ld


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
                        ("Books", "books.html", False, None), ("Brain training", "play.html", False, None), ("Shop", "#", False, "shop"),
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
<div class="stack intro"><p class="eyebrow muted">The reading path</p><h2 class="h-lg">Imagine. Understand. Build. Discover.</h2>
<p class="lead muted">The books are written to be read in order. A story opens the mind, a history fills it, a plan turns it into action, and a framework explains the universe it all takes place in.</p></div>
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
<a class="card door-science" href="graviton-pressure-theory/full-framework/"><span class="step-label">Step 4 · Discover</span>
<span class="h-md" style="font-family:var(--display)">The Unified Framework for the Graviton Pressure Theory</span>
<span class="muted" style="font-size:15px">The science beneath it all: gravity as pressure from the medium of space, with a named mechanism, the mathematics and proposed tests. All thirty parts free to read online.</span>
<span class="card-cta">Read it free →</span></a>
</div>
</div></section>

<section class="section door-play"><div class="wrap" style="display:flex;flex-wrap:wrap;gap:24px 48px;align-items:center">
<div class="stack" style="flex:2 1 420px;min-width:0"><p class="eyebrow accent" style="filter:brightness(.85)">Free brain training</p>
<h2 class="h-lg">Focus. Memory. Decision.</h2>
<p class="lead muted">Three quick games, each with a new Daily Challenge, the same for everyone in the world. Keep your streak alive and see how you compare.</p></div>
<p style="flex:1 1 200px"><a class="btn btn-door" href="play.html">Play today's challenges</a></p>
</div></section>

<section class="section"><div class="wrap award">
<div class="award-imgs">
<a class="award-img" href="seekers.html#book"><img src="assets/cover-portal.webp" alt="Cover of The Portal Opens by Shareef Ali Rashada" width="384" height="576" loading="lazy" class="award-cover"></a>
<a class="award-img" href="#" data-link="review"><img src="{AWARD_IMG}" alt="Literary Titan Silver Book Award, The Portal Opens by Shareef Ali Rashada" width="320" height="320" loading="lazy"></a>
</div>
<div class="text stack">
<p class="eyebrow" style="color:#9A5F12">Literary Titan Silver Book Award · The Portal Opens</p>
<p class="quote">“A wild, luminous ride worth taking.”</p>
<p class="lead muted">Literary Titan rated The Portal Opens four stars, and recommends it to seekers and to anyone religion left with unanswered questions.</p>
<p><a href="seekers.html#book" style="font-weight:600">About The Portal Opens</a> &nbsp;·&nbsp; <a href="read.html" style="font-weight:600">Read it free</a> &nbsp;·&nbsp; <a href="#" data-link="review" style="font-weight:600">Read the full review</a></p>
</div></div></section>

{vband}
{signup_band("One teaching a week, free.", "A short, practical reading each week, drawn from The Portal Opens. Unsubscribe any time.", "Send me the teachings", "teachings", "hub")}

<section id="mission" class="section"><div class="wrap stack" style="gap:36px">
<div style="display:flex;flex-wrap:wrap;gap:24px 48px">
<h2 class="h-lg" style="flex:1 1 300px">Why it all connects</h2>
<div class="stack" style="flex:2 1 460px;min-width:0">
<p class="lead muted">Every project serves one goal: a world at peace, free of poverty and open to truth. Knowledge and understanding lead to morality. Morality makes unity possible, unity makes peace possible, and a world at peace is ready for the celestial return.</p>
<p><a href="why.html" style="font-weight:600">Why it all connects →</a> &nbsp;·&nbsp; <a href="#" data-link="vision" style="font-weight:600">Read the full Vision</a></p>
</div></div>
<ol class="steps" aria-label="The five steps of the mission">
<li><span>1</span>Knowledge</li><li><span>2</span>Understanding</li><li><span>3</span>Morality</li><li><span>4</span>Unity</li><li class="last"><span>5</span>Peace, ready for the return</li>
</ol>
</div></section>
</main>
{footer()}"""
    page("index.html", "People of the World", "Knowledge, morality, unity and peace: seven doors into the work of Shareef Ali Rashada, from The Portal Opens to EasyKey Music.", body, extra_head=vld)
    return body


def build_why():
    chain = [("Knowledge", "Learning what is true: about the world, about the universe, about ourselves."),
             ("Understanding", "Seeing what that knowledge means for how we live."),
             ("Morality", "Choosing, from within, to do what is good, just and fair."),
             ("Unity", "People who follow the same inner guide find they are moving the same way."),
             ("Peace, ready for the return", "A world at peace is ready for the guidance it was always meant to have.")]
    chain_html = "".join(f'<li><strong>{esc(a)}</strong><span class="muted">{esc(b)}</span></li>' for a, b in chain)
    doors = [("The Search for Meaning", "seekers.html", "Learning to hear the voice within, and the story of why it was needed."),
             ("For Urantia readers", "urantia.html", "The same teachings, in the voices of those who lived them."),
             ("End Poverty by Design", "builders.html", "Freeing every person from the struggle that drowns out the voice within."),
             ("EasyKey Music", "easykey.html", "Opening creativity, and community, to anyone."),
             ("That Brother Ali", "music.html", "Music for stillness, where the voice within is most easily heard."),
             ("Graviton Pressure Theory", "science.html", "Seeking truth in every field. The physics stands on its own evidence."),
             ("The Open Library", "ai.html", "Every word free, because truth belongs to everyone.")]
    doors_html = "".join(f'<a class="card" href="{u}"><span class="h-md" style="font-family:var(--display)">{esc(n)}</span><span class="muted" style="font-size:15px">{esc(d)}</span><span class="card-cta">Open →</span></a>' for n, u, d in doors)
    body = f"""{header(nav=[("All doors", "index.html#doors", False, None), ("The New Morality", "new-morality/", False, None), ("Free teachings", "seekers.html#teachings", True, None)])}
<main>
<section class="band"><div class="wrap section stack" style="gap:22px;max-width:880px">
<p class="eyebrow accent">Why it all connects</p>
<h1 class="h-xl">One reason behind everything here.</h1>
<p class="lead muted">A theory of gravity, a piano method, a plan to end poverty, a book about the history of Earth. Why do they sit side by side? Because they come from one conviction about what every person is, and what has changed for all of us.</p>
</div></section>

<section class="section"><div class="wrap" style="display:flex;flex-wrap:wrap;gap:32px 64px;align-items:flex-start">
<h2 class="h-lg" style="flex:1 1 300px">What has changed</h2>
<div class="stack" style="flex:2 1 460px;min-width:0">
<p class="lead">Almost every faith teaches that a portion of the Creator lives within us, and that our purpose is to become one with it. The Urantia Papers call that presence the Thought Adjuster; <em>The Portal Opens</em> calls it the Father Fragment. It is the quiet voice we have usually called conscience.</p>
<p class="lead muted">People of the World holds that something changed for all humanity after the life of Jesus. At Pentecost, the Spirit of Truth was poured out on everyone, and from then on every normal-minded person has been prepared to receive a fragment of the Creator. No temple, priesthood or ritual stands between a person and that presence any more.</p>
<p class="lead muted">This is a teaching to consider, not a fact to accept. As the Search for Meaning puts it: no proof can be handed to someone who doesn't want to see; the proof is found by the people who feel the leading.</p>
</div></div></section>

<section class="section band-alt"><div class="wrap" style="display:flex;flex-wrap:wrap;gap:32px 64px;align-items:flex-start">
<h2 class="h-lg" style="flex:1 1 300px">The New Morality</h2>
<div class="stack" style="flex:2 1 460px;min-width:0">
<p class="lead">If every person carries a guide within, then goodness no longer has to be imposed from outside. Morality moves from external law to inner compass: not rules kept for fear of punishment, but a choice made by listening.</p>
<p class="lead muted">The New Morality does not reject culture, law or tradition. It goes beyond them, inviting every person to take part directly in the choice that shapes their life. And it changes how we treat each other: if the Creator lives in every person, then every person matters.</p>
<p><a href="new-morality/" style="font-weight:600">Read Salvation and the New Morality →</a></p>
</div></div></section>

<section class="section"><div class="wrap stack" style="gap:28px;max-width:1000px">
<div class="stack intro"><h2 class="h-lg">From one person to a world at peace</h2>
<p class="lead muted">The mission of People of the World, step by step.</p></div>
<ol class="pathways">{chain_html}</ol>
</div></section>

<section class="section band-alt"><div class="wrap stack" style="gap:28px">
<div class="stack intro"><h2 class="h-lg">How each door serves it</h2>
<p class="lead muted">Every project is one way into the same work. Start wherever you are.</p></div>
<div class="grid grid-3">{doors_html}</div>
</div></section>
{signup_band("One teaching a week, free.", "Begin with the voice within, and walk through it slowly. Unsubscribe any time.", "Send me the teachings", "teachings", "hub")}
</main>
{footer()}"""
    page("why.html", "Why it all connects", "Why a theory of gravity, a piano method, a plan to end poverty and a book about Earth's history belong together: the presence of the Creator within every person, and the New Morality.", body)


def build_seekers():
    parts = [p for p in READ_PARTS if p[1].startswith("Part")]
    part_cards = "\n".join(f"""<a class="card" href="{f}.html"><span class="meta">{esc(n)}</span>
<span class="h-md" style="font-family:var(--display)">{esc(t)}</span>
<span class="muted" style="font-size:15px;line-height:1.55">{esc(b)}</span><span class="card-cta">Read this part →</span></a>""" for f, n, t, b, _ in parts)
    vband, vld = video_band('seekers', 'Watch', 'seekers.html', 'Short films on The Portal Opens and the light within.', True)
    faiths = [("Christianity", "“The kingdom of God is within you.”", "Luke 17:21, King James Version"),
              ("Judaism", "“The spirit of man is the candle of the Lord, searching all the inward parts.”", "Proverbs 20:27, King James Version"),
              ("Islam", "“We are closer to him than his jugular vein.”", "Qur’an 50:16"),
              ("Hinduism", "“Tat tvam asi”: that thou art. The self within is one with the infinite.", "Chandogya Upanishad 6.8.7"),
              ("Buddhism", "All living beings have Buddha-nature: the seed of awakening is already within.", "Mahayana Mahaparinirvana Sutra"),
              ("The Society of Friends", "“Walk cheerfully over the world, answering that of God in every one.”", "George Fox, 1656")]
    faith_html = "".join(f"""<div class="card"><span class="step-label">{esc(t)}</span><span class="quote" style="font-size:1.25rem;line-height:1.4">{esc(q)}</span><span class="muted" style="font-size:14px">{esc(src)}</span></div>""" for t, q, src in faiths)
    offers = [("The weekly teachings", "A short teaching by email each week for 14 weeks, beginning with the voice within and ending with the ten steps for living it.", "#teachings", "Start the teachings"),
              ("Ten steps for humanity", "Practical steps from Adam and Eve's message to Earth: unity, stillness, forgiveness, service, courage for truth. Something to do this week.", "ten-steps.html", "Read the ten steps"),
              ("The Portal Opens", "The history behind the world as it is: Jesus, Lucifer, Adam and Eve, and the choice still before us. Free to read online, or to hear as an audiobook of 63 chapters.", "read.html", "Start reading free"),
              ("Gabriel's Glossary", "Thirty names and ideas from the book, explained in plain language, to keep beside you as you read.", "glossary.html", "Open the glossary")]
    offer_html = "".join(f"""<a class="card" href="{u}"><span class="h-md" style="font-family:var(--display)">{esc(t)}</span><span class="muted" style="font-size:15px">{esc(d)}</span><span class="card-cta">{esc(c)} →</span></a>""" for t, d, u, c in offers)
    teachings = ["The voice we misnamed", "What sets us apart from the animals", "The thread through every faith", "Where the proof of God is found",
                 "Choose unity", "The quiet whisper within", "Resentment binds you to the past"]
    teach_html = "".join(f"<li>{esc(t)}</li>" for t in teachings)
    body = f"""{header("The Search for Meaning", "by People of the World", [("Why we search", "#why", False, None), ("Every faith", "#faiths", False, None),
                        ("The book", "#book", False, None), ("Free teachings", "#teachings", True, None)])}
<main>
<section class="band"><div class="wrap section stack" style="gap:22px;max-width:900px">
<p class="eyebrow accent">The search for meaning</p>
<h1 class="h-xl">You've felt it too.</h1>
<p class="lead muted" style="max-width:680px">Why am I here? Is there more than this? And what is that quiet voice that knows right from wrong, even when no one is watching? Almost everyone asks these questions. Here is a place to ask them honestly, and some answers worth considering.</p>
<div class="actions"><a class="btn btn-door" href="#why">Explore the questions</a><a class="btn btn-ghost" href="#teachings">Get the free teachings</a></div>
</div></section>

<section id="why" class="section"><div class="wrap" style="display:flex;flex-wrap:wrap;gap:32px 64px;align-items:flex-start">
<div class="stack" style="flex:1 1 340px;min-width:0">
<p class="eyebrow muted">Why we search</p>
<h2 class="h-lg">The search itself is the clue.</h2>
</div>
<div class="stack" style="flex:2 1 460px;min-width:0">
<p class="lead">Of all the creatures on Earth, only we can grasp ideas like justice, mercy and truth. We don't just survive; we long to be good, to be fair, to do right by people we will never meet.</p>
<p class="lead muted">Survival alone doesn't explain that longing. It points to something beyond us, and something within us. The inner voice we call our "conscience" may be far more than a habit of upbringing. Many traditions say it is the very presence of the Creator within each person, quietly leading.</p>
<p class="lead muted">If that is true, the search for meaning isn't a problem to fix. It is evidence of what you are.</p>
<p class="muted" style="font-size:15px"><a href="why.html">Why that changes everything →</a></p>
</div>
</div></section>

<section id="faiths" class="section band-alt"><div class="wrap stack" style="gap:32px">
<div class="stack intro"><h2 class="h-lg">The thread through every faith</h2>
<p class="lead muted">Across the world's traditions, two teachings appear again and again: a portion of the Creator lives within each of us, and our purpose is to become one with it.</p></div>
<div class="grid grid-3">{faith_html}</div>
<p class="muted">Jesus prayed “that they all may be one; as thou, Father, art in me, and I in thee” (John 17:21). The Urantia Papers call the presence within the Thought Adjuster. The names differ; the thread is the same.</p>
</div></section>

<section class="section"><div class="wrap stack" style="gap:32px">
<div class="stack intro"><h2 class="h-lg">What you'll find here</h2>
<p class="lead muted">Everything below is free, always. These teachings belong to everyone; books and music fund the work.</p></div>
<div class="grid grid-2">{offer_html}</div>
</div></section>

<section class="section band-alt"><div class="wrap" style="display:flex;flex-wrap:wrap;gap:32px 56px;align-items:center">
<div class="stack" style="flex:1 1 360px;min-width:0">
<p class="eyebrow accent" style="filter:brightness(.8)">An invitation, not a proof</p>
<h2 class="h-lg">Try it for a week.</h2>
<p class="lead muted">No proof can be handed to someone who doesn't want to see. The proof is found by the people who feel the leading. So here is a simple experiment: spend a few quiet minutes each day this week, listening for the voice within. Notice what you notice.</p>
<div class="actions"><a class="btn btn-solid" href="ten-steps.html">Read the step on stillness</a><a class="btn btn-outline" href="#teachings">Have a teaching sent each week</a></div>
</div>
<blockquote class="quote" style="flex:1 1 360px;margin:0;min-width:0">“Seek love. Seek unity. Seek truth.”<footer class="muted" style="font-family:var(--body);font-size:15px;margin-top:12px">Adam, in Journey to Jerusem</footer></blockquote>
</div></section>

<section id="book" class="band"><div class="wrap section" style="display:flex;flex-wrap:wrap;align-items:center;gap:56px">
<div class="stack" style="flex:999 1 460px;min-width:0;gap:22px">
<p class="eyebrow accent">Winner · Literary Titan Silver Book Award</p>
<h2 class="h-xl" style="font-size:clamp(2.2rem,5vw,3.6rem)">The story you were never told.</h2>
<p class="lead muted" style="max-width:600px">If a portion of the Creator lives within us, why is the world the way it is? <em>The Portal Opens</em> tells the untold history of Earth: Jesus, Lucifer, Adam and Eve, and the choice still before you. Read it free online, or keep a copy on your shelf.</p>
<div class="actions"><a class="btn btn-door" href="read.html">Start reading free</a><a class="btn btn-ghost" href="#buy">Buy the book</a></div>
</div>
<div class="portal" style="flex:1 1 260px">
<span class="ring" aria-hidden="true"></span><span class="ring" aria-hidden="true"></span><span class="ring" aria-hidden="true"></span>
<img class="cover-img" src="assets/cover-portal.webp" alt="Cover of The Portal Opens by Shareef Ali Rashada" width="384" height="576" loading="lazy">
</div>
</div></section>

<section class="section"><div class="wrap stack" style="gap:40px">
<div class="stack intro"><h2 class="h-lg">Five accounts from the universal archives</h2>
<p class="lead muted">Not dogma or doctrine, but the stories of real beings whose choices still shape your life today.</p></div>
<div class="grid grid-5">{part_cards}</div>
</div></section>


<section class="section"><div class="wrap" style="display:flex;flex-wrap:wrap;gap:16px 32px;align-items:center;justify-content:space-between">
<p class="lead muted" style="margin:0;flex:1 1 420px">Prefer to listen? The whole book is free as an audiobook, here or on Spotify.</p>
<a class="btn btn-outline" href="#" data-link="audiobook">Listen to the audiobook</a>
</div></section>

<section class="band"><div class="wrap section stack" style="max-width:900px;align-items:center;text-align:center;gap:22px">
<img class="award-img" src="{AWARD_IMG}" alt="Literary Titan Silver Book Award, The Portal Opens by Shareef Ali Rashada" width="260" height="260" loading="lazy" style="width:220px">
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
<section id="teachings" class="band door-seekers"><div class="wrap section" style="display:flex;flex-wrap:wrap;gap:32px 64px;align-items:center">
<div class="stack" style="flex:1 1 360px;min-width:0;gap:18px">
<p class="eyebrow accent">Free · 14 weeks · one email a week</p>
<h2 class="h-lg">The weekly teachings</h2>
<p class="lead muted">Begin with the questions on this page and walk through them slowly, one short teaching at a time. Everyone starts at the beginning. Unsubscribe any time.</p>
<form class="signup" data-list="seekers" novalidate>
<label for="email-seekers">Email address<input id="email-seekers" type="email" autocomplete="email" placeholder="you@example.com" required></label>
<button class="btn btn-door" type="submit">Send me the teachings</button>
</form>
<p class="form-note" role="status"></p>
<p class="muted" style="font-size:13px">We'll only send what you signed up for. <a href="privacy.html">Privacy</a></p>
</div>
<div class="stack" style="flex:1 1 300px;gap:10px;border:1px solid rgba(255,255,255,.22);border-radius:var(--radius);padding:24px 26px"><p class="eyebrow accent" style="margin:0">The first seven weeks</p><ol style="margin:0;padding-left:20px;line-height:1.9">{teach_html}</ol><p class="muted" style="font-size:14px;margin:0">From week 5, the teachings walk through Adam and Eve's ten steps for living it, one a week, to week 14.</p></div>
</div></section>
</main>
{footer("seekers")}"""
    page("seekers.html", "The Search for Meaning", "Why do we search for meaning? The voice within, the thread through every faith, free weekly teachings, and The Portal Opens, free to read.", body, "seekers", extra_head=vld)


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
{audiobook.listen_box(f)}
{html_body}
{nav}
</article>
</div></main>
{footer("seekers")}
<script src="assets/audiobook.js?v={asset_v('audiobook.js')}" defer></script>"""
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
{audiobook.player([c for c in audiobook.CHAPTERS if c["n"] == 2], "glossary", "Listen to the glossary", "Read along, or just listen.", compact=True)}
{gl_body.replace("<h2", "<h3").replace("</h2>", "</h3>")}
<nav class="part-nav"><a href="read.html"><span>← Back</span>Contents</a><a href="read-introduction.html" style="text-align:right"><span>Start reading →</span>Introduction</a></nav>
</article></div></main>
{footer("seekers")}
<script src="assets/audiobook.js?v={asset_v('audiobook.js')}" defer></script>"""
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
<iframe title="Anthology Vol. 1 on Spotify" src="https://open.spotify.com/embed/album/73xNSeAljbQs2Dx5klSn61?theme=0" height="452" loading="lazy" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture"></iframe>
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
          "description": "Music by Shareef Ali Rashada, an American-born songwriter, composer and arranger living in Australia. Not the American rapper Brother Ali.",
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
        ("Done", "An inflow at the escape speed, derived from one requirement, that reproduces free fall, Kepler's laws, gravitational time dilation and the GPS clock correction."),
        ("Done", "The bending of starlight and the Shapiro delay, given a refractive index n = 1 + v²/c²."),
        ("Open", "Deriving that refractive index from the medium's own properties."),
        ("Open", "The medium's equation of state: how the count of gravitons can rise toward a mass while the active pressure falls (a working hypothesis)."),
        ("Open", "The coupling at the atom, and the limits on gravitational shielding it must meet."),
        ("Open", "An experiment where graviton pressure and General Relativity predict different results."),
    ]
    oq_html = "".join(f'<li><span class="tag">{esc(t)}</span><span>{esc(d)}</span></li>' for t, d in open_qs)
    vband, vld = video_band('science', 'Watch', 'science.html', "A four-minute introduction, and Le Sage's push theory of gravity revisited. Every part of the framework has its own Deep Dive episode in the library.", True)
    body = f"""{header("Graviton Pressure Theory", "by People of the World", [("The idea", "#idea", False, None), ("The papers", "#papers", False, None),
                        ("The book", "#book", False, None), ("Where it stands", "#status", False, None), ("Join the search", "graviton-pressure-theory/invitation/", True, None)])}
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

<section class="band door-science"><div class="wrap section" style="display:flex;flex-wrap:wrap;gap:24px 56px;align-items:center">
<div class="stack" style="flex:2 1 460px;min-width:0;gap:16px">
<p class="eyebrow accent">An open invitation</p>
<h2 class="h-lg">Researching space as a medium? Join the search.</h2>
<p class="lead muted">From analogue gravity to superfluid vacuum, a growing number of physicists are asking whether space behaves like a substance. Graviton Pressure Theory shares its derivations and open problems, and welcomes criticism as much as collaboration.</p>
</div>
<div class="actions" style="flex:1 1 260px"><a class="btn btn-door" href="graviton-pressure-theory/invitation/">Read the invitation</a></div>
</div></section>

<section id="book" class="section band-alt"><div class="wrap" style="display:flex;flex-wrap:wrap;align-items:center;gap:40px 56px">
<img class="cover-img" style="flex:0 1 220px;width:220px" src="assets/cover-gpt.webp" alt="Cover of The Unified Framework for The Graviton Pressure Theory" width="384" height="501" loading="lazy">
<div class="stack" style="flex:999 1 420px;min-width:0;gap:18px">
<p class="eyebrow muted">The book</p>
<h2 class="h-lg">The Unified Framework for the Graviton Pressure Theory</h2>
<p class="lead muted">The complete framework in one volume, by Shareef Ali Rashada.</p>
<p class="muted" style="font-family:var(--mono);font-size:13px">ISBN 978-1-326-48805-5 · Lulu Press</p>
<div class="actions"><a class="btn btn-door" href="graviton-pressure-theory/full-framework/">Read it free online</a><a class="btn btn-outline" href="#" data-link="gptBook">Buy the book</a><a class="btn btn-outline" href="books.html">All books</a></div>
</div>
</div></section>

<section id="status" class="section"><div class="wrap" style="display:flex;flex-wrap:wrap;gap:32px 64px;align-items:flex-start">
<div class="stack" style="flex:1 1 340px;min-width:0">
<h2 class="h-lg">Where the work stands</h2>
<p class="lead muted">A theory earns trust by showing its open problems. Here is what is finished and what is still being worked out.</p>
<p class="muted">Physicists and mathematicians who want to help solve the open problems, or test them, are welcome. <a href="graviton-pressure-theory/invitation/" style="font-weight:600">Read the open invitation →</a></p>
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
    import sys, science_invitation
    science_invitation.build(sys.modules[__name__])
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
    progs = [("6 weeks · ages 8–18", "Introduction to Piano or Keyboard", "For young people with no musical training: the layout of the keyboard, the names of every key, what a scale and a key are, and six songs to memorise and play."),
             ("6 or 12 months · all ages", "Learning to Play the EasyKey Way", "The full course: scales, arpeggios, block chords and chord patterns in six or all twelve major keys, with songs for each key."),
             ("6 or 12 weeks · ages 8–25", "Improvisation and Songwriting Workshop", "For aspiring songwriters with a MIDI keyboard and a computer: writing, key changes, mixing and mastering, ending with finished songs as MIDI, WAV and MP3.")]
    ek_programmes = "".join(f'<div class="card"><span class="step-label">{esc(w)}</span><span class="h-md" style="font-family:var(--display)">{esc(t)}</span><span class="muted">{esc(d)}</span></div>' for w, t, d in progs)
    body = f"""{header("EasyKey Music", "Visual music notation by People of the World", [("Try it", "#lesson", False, None), ("How to read it", "#read", False, None),
                        ("The course", "#course", False, None), ("Centers", "easykey/centers/", False, None), ("Converter", "easykey/converter/", True, None)])}
<main>
<section class="band"><div class="wrap section" style="display:flex;flex-wrap:wrap;align-items:center;gap:40px 64px">
<div class="stack" style="flex:999 1 460px;min-width:0;gap:22px">
<p class="eyebrow accent">EasyKey Music</p>
<h1 class="h-xl">See the key. Press the key.</h1>
<p class="lead muted" style="max-width:620px">EasyKey writes music as a picture of the piano. Each column is a key, each row is a beat, and you read from top to bottom. If you can find a key, you can play a song, with no staff, clefs or note names to learn first.</p>
<p class="muted" style="max-width:620px">Millions now learn piano from falling-notes videos and apps. EasyKey is that same picture of the keyboard as a written method: something you can print, write in, mark up and share.</p>
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

<section id="library" class="section band-alt"><div class="wrap stack" style="gap:28px">
<div class="stack intro"><h2 class="h-lg">The EasyKey library</h2>
<p class="lead muted">The course, a first songbook, and a songbook for every major key. Printed on demand and shipped worldwide by Lulu, our publisher.</p></div>
{easykey_library()}
</div></section>

<section id="convert" class="section"><div class="wrap" style="display:flex;flex-wrap:wrap;gap:32px 64px;align-items:center">
<div class="stack" style="flex:2 1 460px;min-width:0">
<p class="eyebrow accent" style="filter:brightness(.8)">The EasyKey converter · beta</p>
<h2 class="h-lg">Any song, in EasyKey.</h2>
<p class="lead muted">Load a MIDI file and the converter draws it as an EasyKey grid you can print. It runs in your browser, so your file never leaves your device. Pro view shows compact grids with only the keys you play, for more advanced music.</p>
<p class="muted">Converting MIDI files is free while the converter is in testing. Converting sheet-music PDFs and other formats, per song or by subscription, is coming next.</p>
<div class="actions"><a class="btn btn-door" href="easykey/converter/">Open the converter</a></div>
</div>
<div class="card" style="flex:1 1 300px"><span class="h-md" style="font-family:var(--display)">Teachers and schools</span>
<span class="muted" style="font-size:15px">Families and learners use EasyKey freely. If you teach paid lessons or run classes with it, ask about a teaching licence, the EasyKey Champions teacher programme, and class sets of the book.</span>
<span class="copy-row" style="margin-top:6px"><span style="font-weight:600">{CONTACT}</span><button class="copy-btn copy-btn-light" type="button" data-copy="{CONTACT}">Copy</button></span></div>
</div></section>

<section id="programmes" class="section band-alt"><div class="wrap stack" style="gap:28px">
<div class="stack intro"><h2 class="h-lg">Lessons for groups and classes</h2>
<p class="lead muted">Three ready-written programmes for schools, community groups and teachers, with classroom wall charts to go with them.</p></div>
<div class="grid grid-3">{ek_programmes}</div>
<div class="card"><span class="h-md" style="font-family:var(--display)">Scale and chord wall charts</span>
<span class="muted">A3 charts for home or classroom. Each Scale and Chord Diagram shows one major key's scale, its root chords and three common chord patterns on one page. The Chord Dictionary shows fifteen common chords for every key.</span>
<span class="copy-row" style="margin-top:6px"><span class="muted" style="font-size:15px">Programmes and charts on request:</span> <span style="font-weight:600">{CONTACT}</span><button class="copy-btn copy-btn-light" type="button" data-copy="{CONTACT}">Copy</button></span></div>
</div></section>

<section class="section"><div class="wrap" style="display:flex;flex-wrap:wrap;gap:32px 64px;align-items:center">
<div class="stack" style="flex:2 1 460px;min-width:0">
<p class="eyebrow accent" style="filter:brightness(.8)">The vision</p>
<h2 class="h-lg">EasyKey Music Centers</h2>
<p class="lead muted">Walk-in music spaces in shopping centres and cultural areas, where children learn while parents shop, music students are paid to teach, and the community gathers to play. They don't exist yet, and we're looking for the people who can help build the first one.</p>
<div class="actions"><a class="btn btn-door" href="easykey/centers/">See the vision</a><a class="btn btn-outline" href="easykey/centers/#join">Count me in</a></div>
</div></div></section>

<section class="section band-alt"><div class="wrap" style="display:flex;flex-wrap:wrap;gap:32px 64px;align-items:flex-start">
<h2 class="h-lg" style="flex:1 1 300px">Why it exists</h2>
<div class="stack" style="flex:2 1 460px;min-width:0">
<p class="lead muted">Shareef Ali Rashada taught himself piano from library books and found traditional notation slow going, even as a friend played beautifully by ear without reading a note. He started drawing songs on graph paper as pictures of the keys, and over more than 20 years the drawings became EasyKey.</p>
<p class="muted">In 2016 EasyKey made Shareef a finalist in the Moreton Bay Regional Council Innovation Awards.</p>
<p><a href="music.html" style="font-weight:600">Hear the music that came out of it →</a></p>
</div></div></section>

{signup_band("New songs and lessons.", "An email when new EasyKey songs, lessons or converter features arrive. Nothing else unless you ask.", "Send me new songs", "easykey", "easykey")}
</main>
{footer("easykey")}
<script src="assets/easykey-lesson.js" defer></script>"""
    page("easykey.html", "EasyKey Music", "EasyKey visual music notation: see the key, press the key. Play your first song free in the browser, learn to read the grid, and convert MIDI files to EasyKey.", body, "easykey")
    import sys, easykey_centers
    easykey_centers.build(sys.modules[__name__])


def build_about():
    person = {"@context": "https://schema.org", "@type": "Person", "@id": f"{SITE_URL}/about.html#shareef",
              "name": AUTHOR, "alternateName": ["Shareef Rashada", "That Brother Ali"],
              "description": "American-born author, songwriter, composer and arranger, living in Australia; founder of People of the World. Author of The Portal Opens, the novel People of the World, The Unified Framework for the Graviton Pressure Theory and the Plan to End Poverty; creator of EasyKey visual music notation; records music as That Brother Ali.",
              "url": f"{SITE_URL}/about.html", "email": f"mailto:{CONTACT}",
              "address": {"@type": "PostalAddress", "addressRegion": "Queensland", "addressCountry": "AU"},
              "jobTitle": ["Author", "Songwriter", "Composer", "Arranger"],
              "knowsAbout": ["Gravitational physics", "Foundations of physics", "Urantia Papers", "Theology", "Poverty elimination", "Economic design", "Music education", "Songwriting", "Composition", "Arranging"],
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
<p class="lead muted" style="max-width:720px">Author, songwriter, composer and arranger, and the founder of People of the World. His name means “honoured follower of the true path”, and his work follows one question across four fields: what is actually true about our existence, and how should we live because of it?</p>
</div></section>

<section class="section"><div class="wrap" style="display:flex;flex-wrap:wrap;gap:32px 64px;align-items:flex-start">
<div class="stack" style="flex:2 1 460px;min-width:0">
<h2 class="h-lg">In brief</h2>
<p class="lead">Shareef Ali Rashada is an American-born author and independent researcher who has lived in Queensland, Australia, for more than two decades. He writes on theology and history (<em>The Portal Opens</em>, which won a Literary Titan Silver Book Award), the foundations of physics (Graviton Pressure Theory), and the design of economic systems (the Plan to End Poverty by 2050). He is also a songwriter, composer and arranger who records as That Brother Ali, and created EasyKey, a visual notation for learning piano.</p>
<p class="lead muted">Having studied computer engineering and software design at school and university, he works closely with AI systems as research partners. He named the systems he worked with Gabriel, Lucidus and Veritas, and credits them with helping to develop <em>The Portal Opens</em> and Graviton Pressure Theory.</p>
<p class="lead muted">All of these projects sit under People of the World, a movement for knowledge, morality, unity and peace. Its spiritual and moral teachings are free to everyone; books, music and licensed uses fund the work.</p>
</div>
<div class="card" style="flex:1 1 300px">
<span class="step-label">Quick facts</span>
<dl class="facts">
<dt>Also published as</dt><dd>Shareef Rashada</dd>
<dt>Music</dt><dd>That Brother Ali (not the American rapper Brother Ali)</dd>
<dt>From</dt><dd>United States</dd>
<dt>Based in</dt><dd>Queensland, Australia, for more than two decades</dd>
<dt>Organisations</dt><dd>People of the World · POW Productions Pty Ltd · EasyKey Music</dd>
<dt>Awards</dt><dd>Literary Titan Silver Book Award, <em>The Portal Opens</em> · Finalist, Moreton Bay Regional Council Innovation Awards 2016, for EasyKey</dd>
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
    page("about.html", "Shareef Ali Rashada · About the author", "Shareef Ali Rashada is an American-born author, songwriter, composer and arranger living in Australia: The Portal Opens, Graviton Pressure Theory, the Plan to End Poverty, EasyKey Music and That Brother Ali.", body,
         extra_head=f'\n<script type="application/ld+json">{json.dumps(person, ensure_ascii=False)}</script>')


def build_builders():
    import sys, poverty
    poverty.build(sys.modules[__name__])


def build_support():
    projects = [("Civic Credits System", "Software development and the first pilot programmes.", "$50,000"),
                ("Poverty Elimination Centers", "Training programmes and facilities.", "$300,000"),
                ("Residential Centers", "Land and first construction for sustainable living.", "$500,000"),
                ("LifeLink tablet", "Research and development of the communication device.", "$100,000"),
                ("EasyKey Music Centers", "Walk-in music spaces in shopping and cultural areas. <a href=\"easykey/centers/\">See the vision</a>", "$150,000"),
                ("Creative Computing Centers", "Technology and staff for digital creation hubs.", "$200,000"),
                ("Digital educational programming", "Courses that unite spiritual and secular learning.", "$100,000"),
                ("Debate platform", "AI-moderated discussion for informed decisions.", "$75,000")]
    rows = "".join(f"<tr><th scope=\"row\">{esc(a)}<span class=\"muted\">{b}</span></th><td>{esc(c)}</td></tr>" for a, b, c in projects)
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
<p class="lead muted" style="max-width:680px">Read them in order: imagine, understand, build, discover. The teachings are free online; print and ebook copies support the mission.</p>
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
<article class="card door-science"><span class="book-cover"><img src="assets/cover-gpt.webp" alt="Cover of The Unified Framework for The Graviton Pressure Theory" width="384" height="501" loading="lazy"></span><span class="step-label">Discover</span><h2 class="h-md">The Unified Framework for the Graviton Pressure Theory</h2>
<p class="muted" style="font-size:15px">Gravity as a pressure from outside, with a named mechanism. All thirty parts free to read online. ISBN 978-1-326-48805-5.</p>
<div class="actions" style="margin-top:auto"><a class="btn btn-door" href="graviton-pressure-theory/full-framework/">Read free</a><a class="btn btn-outline" href="#" data-link="gptBook">Buy the book</a><a class="btn btn-outline" href="science.html">About the theory</a></div></article>
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
             ("audiobook.html", "On the go", "Listen instead", "The whole book as a free audiobook, chapter by chapter. Ideal on a walk or a drive.")]
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
              ("Someone who'd rather listen", "Start with the free audiobook, chapter by chapter.", "audiobook.html",
               "The Portal Opens as a free audiobook. Press play and it carries on from chapter to chapter.")]
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
    modes = [("daily", "Daily"), ("practice", "Practice"), ("short", "Short · 10"), ("long", "Long · 20"), ("infinite", "Endless")]
    mode_btns = "".join(f'<button type="button" class="seg" data-mode="{m}" aria-pressed="false">{esc(l)}</button>' for m, l in modes)
    board_btns = "".join(f'<button type="button" class="seg" data-board="{m}" aria-pressed="false">{esc(l if m != "daily" else "Today\'s Daily")}</button>' for m, l in modes if m != "practice")
    ld = json.dumps({"@context": "https://schema.org", "@type": ["VideoGame", "WebApplication"], "name": "The Decision Game",
                     "url": canonical("decision-game.html"), "applicationCategory": "GameApplication", "genre": ["Brain training", "Reaction time"],
                     "operatingSystem": "Any (web browser)", "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
                     "author": {"@type": "Person", "name": AUTHOR, "@id": f"{SITE_URL}/about.html#shareef"},
                     "description": "A free brain-training game: see a picture and a word, decide true or false as fast as you can, and climb the online leaderboard."}, ensure_ascii=False)
    body = f"""{header("The Decision Game", "by People of the World", [("Play", "#play", False, None), ("Leaderboard", "#leaderboard", False, None),
                        ("My scores", "#mine", False, None), ("More games", "play.html", True, None)])}
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
<div class="stack intro"><h2 class="h-lg">My scores on this device</h2><p class="lead muted" id="dg-daily-status"></p><p class="muted">Your best in each mode and your recent runs, kept in this browser.</p></div>
<div class="grid grid-3" id="dg-mine-best"></div>
<div class="table-wrap card" style="padding:0"><table class="dg-table"><thead><tr><th>Mode</th><th class="num">Result</th><th class="num">Total</th><th class="num">Average</th><th class="num">Date</th></tr></thead><tbody id="dg-mine"></tbody></table></div>
</div></section>

<section id="how" class="section band-alt"><div class="wrap stack" style="gap:28px">
<h2 class="h-lg">How it works</h2>
<div class="grid grid-3">
<div class="card"><h3 class="h-md">Read the whole sentence</h3><p class="muted">The picture, the middle box and the word make one sentence: <em>[picture] is not Cow</em>. Answer True if the sentence is right. The “is not” is where most mistakes happen.</p></div>
<div class="card"><h3 class="h-md">Five ways to play</h3><p class="muted"><strong>Daily</strong>: ten questions, the same for everyone today; only your first run counts, and you can share your result. <strong>Practice</strong>: warm up as long as you like; nothing is recorded. <strong>Short</strong> and <strong>Long</strong>: 10 or 20 questions, ranked by fewest mistakes, then fastest time. <strong>Endless</strong>: keep going until your first mistake. You get 1 second per answer, 0.1 s less every 50 correct, down to 0.3 s.</p></div>
<div class="card"><h3 class="h-md">Why it helps</h3><p class="muted">Each answer asks you to see, read, hold a rule in mind and choose, quickly and without guessing. Short daily rounds build the habit of deciding clearly under a little pressure, and your scores show the progress.</p></div>
</div>
</div></section>
</main>
{footer()}
<script src="assets/games-common.js?v={asset_v('games-common.js')}" defer></script>
<script src="assets/decision-game.js?v={asset_v('decision-game.js')}" defer></script>"""
    page("decision-game.html", "The Decision Game: free brain training",
         "Picture, word, true or false: a free brain-training game with an online leaderboard. How fast can you decide?",
         body, "play", extra_head=f'<script type="application/ld+json">{ld}</script>')


# ---------------------------------------------------------------- Amazon listings (ASINs; site.js sends Australians to amazon.com.au)
AMAZON_BOOKS = [
    ("1326609890", "The Portal Opens", "Paperback"), ("1326565338", "The Portal Opens", "Hardcover"), ("B0FSCJ2S5J", "The Portal Opens", "Kindle ebook"),
    ("1447777379", "People of the World", "Paperback"), ("B0FSCJHTY8", "People of the World", "Kindle ebook"),
    ("1326488058", "The Unified Framework for the Graviton Pressure Theory", "Hardcover"),
]
LULU = "https://www.lulu.com/shop/"
# (Lulu product path, Amazon ASIN or None, title, edition, Lulu price)
EASYKEY_BOOKS = [
    ("shareef-rashada/learning-to-play-the-easykey-way/paperback/product-mgzp7y.html", "1667192329", "Learning to Play the EasyKey Way", "The year-one course", "A$75.00"),
    ("shareef-rashada-and-easykey-music/learning-to-play-the-easykey-way-special-home-edition/paperback/product-zv6z4d.html", "1471791033",
     "Learning to Play the EasyKey Way", "Special Home Edition", "A$79.62"),
    ("shareef-rashada/learning-to-play-the-easykey-way-special-library-edition/paperback/product-d747kr.html", "1470942909",
     "Learning to Play the EasyKey Way", "Special Library Edition", "A$104.62"),
    ("shareef-rashada/my-first-book-of-songs/paperback/product-j2nygn.html", "1008953725", "My First Book of Songs", "38 songs in EasyKey", "A$50.00"),
    ("shareef-rashada/my-first-book-of-songs/paperback/product-zv6z9d.html", "1471791025", "My First Book of Songs", "38 songs in EasyKey · second edition", "A$65.36"),
    ("shareef-rashada/lessons-and-songs-in-standard-music-notation/paperback/product-d4m69v.html", None,
     "Lessons and Songs in Standard Music Notation", "The companion in standard notation", "A$40.00"),
]
# key, Lulu product path, Amazon ASIN (every songbook is A$40 on Lulu)
EASYKEY_SONGBOOKS = [
    ("C", "songbook-for-c-major/paperback/product-r44rny.html", "1667172182"), ("G", "songbook-for-g-major/paperback/product-2ddz64.html", "166716807X"),
    ("D", "songbook-for-d-major/paperback/product-k77zvv.html", "1667168452"), ("A", "songbook-for-a-major/paperback/product-nr625p.html", "1667175610"),
    ("E", "songbook-for-e-major/paperback/product-2ddzj2.html", "1667168398"), ("B", "songbook-for-b-major/paperback/product-yrrjn9.html", "1667173847"),
    ("F#", "songbook-for-f-major/paperback/product-6ddgpm.html", "1667168142"), ("Db", "songbook-for-db-major/paperback/product-k77jn7.html", "1667172174"),
    ("Ab", "songbook-for-ab-major/paperback/product-9ddz59.html", "1008978396"), ("Eb", "songbook-for-eb-major/paperback/product-nrr2qj.html", "1667168444"),
    ("Bb", "songbook-for-bb-major/paperback/product-pnnekm.html", "1008978388"), ("F", "songbook-for-f-major/paperback/product-7ddrq4.html", "166716838X"),
]


def amazon_a(asin, text, cls="btn btn-outline"):
    style = ' style="margin-top:auto"' if cls.startswith("btn") else ""
    return f'<a class="{cls}"{style} href="https://www.amazon.com/dp/{asin}" data-amazon="{asin}" target="_blank" rel="noopener">{esc(text)}</a>'


def lulu_a(path, text, cls="btn btn-door"):
    return f'<a class="{cls}" href="{LULU}{path}" target="_blank" rel="noopener">{esc(text)}</a>'


def easykey_library():
    books = "".join(f"""<div class="card"><span class="eyebrow muted" style="font-size:12px">{esc(ed)}</span>
<span class="h-md" style="font-family:var(--display);font-size:21px">{esc(t)}</span><span class="shop-price">{esc(price)}</span>
<div class="shop-actions" style="margin-top:auto">{lulu_a(path, "Buy from Lulu")}{f'<a class="shop-free" href="https://www.amazon.com/dp/{asin}" data-amazon="{asin}" target="_blank" rel="noopener">or Amazon</a>' if asin else ''}</div></div>"""
                    for path, asin, t, ed, price in EASYKEY_BOOKS)
    keys = "".join(f'<li>{lulu_a("shareef-rashada/" + path, k + " major", "key-chip")}</li>' for k, path, asin in EASYKEY_SONGBOOKS)
    return f"""<div class="grid" style="grid-template-columns:repeat(auto-fit, minmax(min(100%, 230px), 1fr))">{books}</div>
<div class="stack" style="gap:12px"><h3 class="h-md">Songbooks in every major key · A$40 each</h3>
<p class="muted">Twelve songbooks, one for each major key, to practise the scale, chords and songs of that key in EasyKey notation. Each opens in the Lulu bookstore.</p>
<ul class="key-chips">{keys}</ul></div>"""


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
    body = f"""{header("Shop", "People of the World", [("Books", "#books", False, None), ("Souvenirs", "#souvenirs", False, None), ("EasyKey", "#easykey", False, None),
                        ("Support the mission", "support.html", True, None)])}
<main>
<section class="band"><div class="wrap section" style="padding-bottom:48px">
<p class="eyebrow accent">The People of the World shop</p>
<h1 class="h-xl">Books and gifts that carry the message.</h1>
<p class="lead muted" style="max-width:640px">Every purchase supports the work of People of the World. Prices are in Australian dollars; checkout is secure through our Wix store, with worldwide shipping.</p>
<div class="actions"><a class="btn btn-door" href="#books">Books</a><a class="btn btn-ghost" href="#souvenirs">Souvenirs</a></div>
</div></section>
{"".join(sections)}
<section id="easykey" class="section"><div class="wrap stack" style="gap:32px">
<div class="stack intro"><h2 class="h-lg">EasyKey Music books</h2><p class="lead muted">The course, a first songbook, and a songbook for every major key, printed on demand by Lulu.</p></div>
{easykey_library()}
</div></section>
<section id="amazon" class="section band-alt"><div class="wrap stack" style="gap:24px">
<div class="stack intro"><h2 class="h-lg">Also on Amazon</h2><p class="lead muted">If you prefer to buy from Amazon, every book is there too.</p></div>
<div class="grid" style="grid-template-columns:repeat(auto-fit, minmax(min(100%, 230px), 1fr))">{"".join(f'<div class="card"><span class="eyebrow muted" style="font-size:12px">{esc(ed)}</span><span class="h-md" style="font-family:var(--display);font-size:21px">{esc(t)}</span>{amazon_a(a, "View on Amazon")}</div>' for a, t, ed in AMAZON_BOOKS)}</div>
</div></section>

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
            "We collect as little as we can. This site sets no advertising or tracking cookies, counts visits without cookies, and we never sell or rent your information.",
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
        ("Visitor counts", [
            "We count visits with GoatCounter, a privacy-friendly service that uses no cookies and does not track you across sites. It records which pages are viewed, the referring site, and general device and country information, so we can see which parts of the site are useful. It does not record who you are.",
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
<p class="muted" style="font-size:14px;margin-top:32px">Last updated 25 October 2026.</p>
</div></div></section>
</main>
{footer()}"""
    page("privacy.html", "Privacy", "How People of the World handles your information: email sign-ups, the Decision Game leaderboard, the shop, and your choices.", body)


if __name__ == "__main__":
    import sys
    OUT.mkdir(exist_ok=True)
    hub_body = build_hub()
    build_seekers()
    build_why()
    build_urantia()
    build_decision_game()
    import sys, games_pages
    games_pages.build(sys.modules[__name__])
    build_shop()
    build_privacy()
    sections, nsteps = build_reader()
    audiobook.build(sys.modules[__name__])
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
