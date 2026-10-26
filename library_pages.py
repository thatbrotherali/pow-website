"""The Open Library: every document by Shareef Ali Rashada as a stable, plain-HTML page with a
plain-text (Markdown) twin, plus the files search engines and AI systems use to find and read them:
llms.txt, llms-full.txt, catalog.json, sitemap.xml and robots.txt.

Called from build.py. The document texts live in src/library/ (made by tools/import_library.py).
"""
import html
import json
import re

LIB = None  # set in build()

# Dates the documents were written or last revised (from the documents themselves where stated).
DATES = {"framework": "2025-06-12", "transitional-mechanics": "2025-06-12", "what-gpt-corrects": "2025-06-08",
         "start-here": "2026-01-03", "constraint-set": "2026-01-04", "gr-silence-map": "2026-01-03",
         "not-alternative-gravity": "2026-01-03", "audit-questions": "2026-01-03",
         "from-gr-to-gpt": "2025-03-18", "reduction-conflation": "2026-10-03", "paradox-of-the-boulder": "2026",
         "causal-audit-of-motion": "2026", "structure-before-uncertainty": "2026-01-04", "mechanics-of-the-medium": "2026-10-12",
         "logical-closure-of-the-ep": "2026-10-21", "operational-constraints-of-the-ep": "2026-10-21",
         "plan": "2025", "new-morality": "2025-07-28", "cosmic-mind": "2025-03-08"}

PAPERS = [  # order, plain description
    ("from-gr-to-gpt", "Why General Relativity describes gravity without explaining it, and what a force-based model offers in its place. The best first paper for newcomers."),
    ("paradox-of-the-boulder", "A worked audit of what each framework says is physically happening when a boulder rests on a moving, rotating Earth."),
    ("causal-audit-of-motion", "Falling, examined step by step: what a causal account of motion must name, and where geometric descriptions stop."),
    ("structure-before-uncertainty", "Why a universe that works reliably at every scale calls for mechanism, not only probability, with charge treated as a bias in the medium's flow."),
    ("transitional-mechanics", "A direct mapping of classical mechanics into Graviton Pressure Theory: each familiar force restated as field pressure acting on structure."),
    ("what-gpt-corrects", "A summary of the specific problems in current gravitational physics that Graviton Pressure Theory sets out to correct."),
]
# The reading pathway, in order. Each step: (slug, address, description or None to use the document's own opening)
PATHWAY = [
    ("start-here", "graviton-pressure-theory/", None),
    ("constraint-set", "graviton-pressure-theory/constraint-set/", None),
    ("audit-questions", "graviton-pressure-theory/audit-questions/", None),
    ("gr-silence-map", "graviton-pressure-theory/gr-silence-map/", None),
    ("reduction-conflation", "graviton-pressure-theory/papers/reduction-conflation/", None),
    ("logical-closure-of-the-ep", "graviton-pressure-theory/papers/logical-closure-of-the-ep/",
     "The Equivalence Principle says gravity and acceleration feel the same. This audit asks what was accepted when that was read as saying they are the same, compares the rocket and the planet step by step, and proposes closing the question with a common mechanism."),
    ("operational-constraints-of-the-ep", "graviton-pressure-theory/papers/operational-constraints-of-the-ep/",
     "If weight is the Equivalence Principle's acceleration and the planet's surface is not moving outward, the medium of space must be moving inward. From that one constraint the paper derives an inflow at the escape speed, and recovers free fall, Kepler's laws, gravitational time dilation and GPS clock rates, with its open problems stated."),
    ("not-alternative-gravity", "graviton-pressure-theory/not-alternative-gravity/", None),
    ("mechanics-of-the-medium", "graviton-pressure-theory/papers/mechanics-of-the-medium/", None),
]
PATH_URL = {s: u for s, u, _ in PATHWAY}
FRAMEWORK_URL = "graviton-pressure-theory/full-framework/"
PLAN_URL = "plan-to-end-poverty/"
BOOK_GPT = "The Unified Framework for the Graviton Pressure Theory"
BOOK_PLAN = "The Plan to End Poverty: A Unified Framework for Human Capability and Economic Renewal"
# The working papers behind the Plan, one programme page each (built by poverty.py)
PROGRAMMES = {"civic-credits": "Civic Credits", "poverty-elimination-centers": "Poverty Elimination Centers", "lifelink": "LifeLink"}


def working_url(d):
    return f"{PLAN_URL}{d['programme']}/{slugify(d['title'])}/"


def slugify(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:60]


def sentences(text, limit=300):
    text = re.sub(r"\s+", " ", text).strip()
    out = ""
    for s in re.split(r"(?<=[.!?])\s+", text):
        if len(out) + len(s) + 1 > limit:
            break
        out = (out + " " + s).strip()
    return out or text[:limit].rsplit(" ", 1)[0] + "…"


def minutes(words):
    return max(1, round(words / 230))


def norm_headings(frag):
    """Shift headings so the highest level is h2; make sure every h2/h3 has a unique id."""
    levels = [int(x) for x in re.findall(r"<h([2-6])", frag)]
    if levels:
        shift = min(levels) - 2
        if shift:
            frag = re.sub(r"<(/?)h([2-6])", lambda m: f"<{m.group(1)}h{max(2, int(m.group(2)) - shift)}", frag)
    seen = set()

    def ensure(m):
        tag, attrs, inner = m.group(1), m.group(2), m.group(3)
        idm = re.search(r'id="([^"]+)"', attrs)
        hid = idm.group(1) if idm else slugify(html.unescape(re.sub(r"<[^>]+>", "", inner))) or "section"
        base, n = hid, 2
        while hid in seen:
            hid = f"{base}-{n}"; n += 1
        seen.add(hid)
        attrs = re.sub(r'\s*id="[^"]+"', "", attrs)
        return f'<{tag}{attrs} id="{hid}">{inner}</{tag}>'
    return re.sub(r"<(h[2-4])([^>]*)>(.*?)</\1>", ensure, frag, flags=re.S)


def contents_nav(frag):
    heads = re.findall(r'<h2[^>]*id="([^"]+)"[^>]*>(.*?)</h2>', frag, re.S)
    if len(heads) < 3:
        heads = re.findall(r'<h[23][^>]*id="([^"]+)"[^>]*>(.*?)</h[23]>', frag, re.S)
    if len(heads) < 2:
        return ""
    items = "".join(f'<li><a href="#{i}">{html.escape(html.unescape(re.sub(r"<[^>]+>", "", t)).strip())}</a></li>' for i, t in heads[:60])
    return f'<nav class="toc" aria-label="Contents"><details open><summary>Contents</summary><ol>{items}</ol></details></nav>'


def build(B):
    """B is the build module (page, header, footer, esc, OUT, SRC, SITE_URL, AUTHOR, CONTACT, signup_band)."""
    global LIB
    LIB = B.SRC / "library"
    esc = B.esc
    cat = json.loads((LIB / "catalog.json").read_text(encoding="utf-8"))
    by = {d["slug"]: d for group in cat.values() for d in group}
    docs = []  # every library document, in reading order

    def add(slug, url, coll, title=None, subtitle=None, desc=None, date=None, part=None, book=None, chapter=None):
        d = by[slug]
        e = {"slug": slug, "url": url, "coll": coll, "title": title or d["title"], "subtitle": subtitle if subtitle is not None else d["subtitle"],
             "desc": desc or sentences(d["lead"]), "words": d["words"], "date": date or DATES.get(slug) or DATES.get(coll, "2025"),
             "part": part, "book": book, "chapter": chapter, "source": d["source"], "pdf": d.get("pdf", False)}
        docs.append(e)
        return e

    for s, u, desc in PATHWAY:
        add(s, u, "pathway", desc=desc)
    for d in sorted(cat["framework"], key=lambda d: d["part"]):
        add(d["slug"], f"{FRAMEWORK_URL}part-{d['part']:02d}-{slugify(d['title'])}/", "framework",
            desc=sentences(d["lead"]) or f"Part {d['part']} of {BOOK_GPT}.", date=DATES["framework"], part=d["part"], book=BOOK_GPT)
    for s, desc in PAPERS:
        add(s, f"graviton-pressure-theory/papers/{s}/", "papers", desc=desc)
    for d in sorted(cat["plan"], key=lambda d: d["chapter"]):
        n = d["chapter"]
        url = PLAN_URL + ("introduction/" if n == 0 else "appendices/" if n == 10 else f"chapter-{n:02d}-{slugify(d['title'])}/")
        add(d["slug"], url, "plan", subtitle="", date=DATES["plan"], chapter=n, book=BOOK_PLAN,
            desc=sentences(d["lead"]) or f"Chapter {n} of {BOOK_PLAN}.")
    for d in cat.get("working", []):
        e = add(d["slug"], working_url(d), "working", date=d["date"])
        e["programme"], e["group"] = d["programme"], d["group"]
    add("new-morality", "new-morality/", "spirit")
    add("cosmic-mind", "cosmic-mind/", "spirit",
        desc="A step-by-step logical synthesis of the classical and modern arguments for a cosmic mind, or God, starting from what any honest examination must take as given.")

    seq = {}  # prev/next within each reading sequence
    for coll in ("pathway+framework", "papers", "plan", "spirit"):
        group = [e for e in docs if e["coll"] in coll.split("+")]
        for i, e in enumerate(group):
            seq[e["slug"]] = (group[i - 1] if i else None, group[i + 1] if i + 1 < len(group) else None)

    coll_name = {"pathway": "Graviton Pressure Theory: start here", "framework": BOOK_GPT, "papers": "Graviton Pressure Theory papers",
                 "plan": "The Plan to End Poverty", "spirit": "Spirit and morality", "working": "The Plan to End Poverty: working papers"}
    coll_home = {"pathway": "graviton-pressure-theory/", "framework": FRAMEWORK_URL, "papers": "ai.html#papers", "plan": PLAN_URL, "spirit": "ai.html#spirit", "working": "builders.html"}

    def lib_header():
        return B.header("The Open Library", "by People of the World", [
            ("Catalogue", "ai.html", False, None), ("Gravity: start here", "graviton-pressure-theory/", False, None),
            ("For AI systems", "ai.html#machines", True, None)])

    def citation(e):
        where = f"In {e['book']}, part {e['part']}" if e.get("part") else (f"In {e['book']}" if e.get("book") else "People of the World")
        year = e["date"][:4]
        return f"Rashada, S. A. ({year}). {e['title']}. {where}. People of the World. {B.SITE_URL}/{e['url']}"

    def jsonld(e):
        data = {"@context": "https://schema.org", "@type": "ScholarlyArticle" if e["coll"] in ("pathway", "framework", "papers") else "Article",
                "headline": e["title"][:110], "name": e["title"], "description": e["desc"],
                "author": {"@type": "Person", "@id": f"{B.SITE_URL}/about.html#shareef", "name": B.AUTHOR, "url": f"{B.SITE_URL}/about.html"},
                "publisher": {"@type": "Organization", "name": "People of the World", "url": f"{B.SITE_URL}/"},
                "datePublished": e["date"], "inLanguage": "en", "wordCount": e["words"], "isAccessibleForFree": True,
                "url": f"{B.SITE_URL}/{e['url']}", "encoding": {"@type": "MediaObject", "encodingFormat": "text/markdown", "contentUrl": f"{B.SITE_URL}/{e['url']}index.md"}}
        if e.get("book"):
            data["isPartOf"] = {"@type": "Book", "name": e["book"], "author": {"@type": "Person", "name": B.AUTHOR}}
        if e["coll"] in ("pathway", "framework", "papers"):
            data["about"] = ["Gravity", "Foundations of physics", "Graviton Pressure Theory"]
        elif e["coll"] in ("plan", "working"):
            data["about"] = ["Poverty", "Economic policy", "Civic Credits"]
        return f'\n<script type="application/ld+json">{json.dumps(data, ensure_ascii=False)}</script>'

    import corrections

    def corrections_box(fixes, e):
        if not fixes:
            return ""
        items = "".join(f"<li>{esc(n)}</li>" for n in fixes if not n.startswith("Notation"))
        bridge = next((n for n in fixes if n.startswith("Notation")), "")
        orig = " The original PDF is unchanged." if e["pdf"] else ""
        return (f'<details class="ai-note corrections" style="margin:1.2em 0"><summary><strong>Editor\'s corrections, October 2026</strong> · '
                f'some equations on this page were corrected at the author\'s request.{orig}</summary><ul>{items}</ul>'
                + (f'<p class="muted" style="font-size:14.5px">{esc(bridge)}</p>' if bridge else "") + "</details>")

    def working_note(e):
        if e["coll"] != "working":
            return ""
        return (f' It is one of the working papers behind <a href="{PLAN_URL}">{esc(BOOK_PLAN)}</a> (2025 edition), written {e["date"][:4]}. '
                f'Where an earlier paper and the 2025 edition differ, the 2025 edition is the current statement of the plan. '
                f'More papers on {esc(PROGRAMMES[e["programme"]])}: <a href="{PLAN_URL}{e["programme"]}/">{esc(PROGRAMMES[e["programme"]])}</a>.')

    def doc_page(e):
        frag, fixes = corrections.apply(e["slug"], (LIB / f"{e['slug']}.html").read_text(encoding="utf-8"))
        frag = norm_headings(frag)
        if e["slug"] == "start-here":
            for key, url in [("constraint-set", PATH_URL["constraint-set"]), ("gr-silence-map", PATH_URL["gr-silence-map"]),
                             ("not-alternative-gravity", PATH_URL["not-alternative-gravity"]), ("full-framework", FRAMEWORK_URL)]:
                frag = re.sub(rf"Link: <strong>/graviton-pressure-theory/{key}/</strong>", f'<a href="{url}">Read it →</a>', frag)
            order = "".join(f'<li><a href="{x["url"]}">{esc(x["title"])}</a></li>' for x in docs if x["coll"] == "pathway" and x["slug"] != "start-here")
            order += f'<li><a href="{FRAMEWORK_URL}">{esc(BOOK_GPT)}</a> (thirty parts)</li>'
            box = f'<aside class="ai-note" style="margin:1.5em 0"><p class="step-label">The full reading order</p><ol>{order}</ol><p>Each page links to the next, so you can read straight through.</p></aside>\n'
            frag = re.sub(r'(<h2[^>]*id="what-gpt-claims-in-one-paragraph")', box.replace("\\", "\\\\") + r"\1", frag, count=1)
            frag = frag.replace("<strong>peopleoftheworld.org/graviton-pressure-theory</strong>", f'<a href="graviton-pressure-theory/">{B.SITE_URL}/graviton-pressure-theory/</a>')
        import videos
        vsec, vld = videos.section(e["slug"], "Watch the Deep Dive on this part" if e["coll"] == "framework" else "Watch", B.SITE_URL, f"{B.SITE_URL}/{e['url']}")
        prev, nxt = seq.get(e["slug"], (None, None))
        pager = "".join([
            f'<a class="pager-prev" href="{prev["url"]}"><span>← Previous</span>{esc(prev["title"])}</a>' if prev else "<span></span>",
            f'<a class="pager-next" href="{nxt["url"]}"><span>Next →</span>{esc(nxt["title"])}</a>' if nxt else ""])
        where = f"Part {e['part']} of 30" if e.get("part") else ("Chapter " + str(e["chapter"]) if e.get("chapter") not in (None, 0, 10) else "")
        meta = " · ".join(x for x in [f"By {B.AUTHOR}", where, f"{e['words']:,} words · about {minutes(e['words'])} min", e["date"][:4]] if x)
        crumbs = f'<a href="ai.html">Library</a> › <a href="{coll_home[e["coll"]]}">{esc(coll_name[e["coll"]])}</a>'
        if e["coll"] == "working":
            crumbs = (f'<a href="builders.html">End Poverty by Design</a> › '
                      f'<a href="{PLAN_URL}{e["programme"]}/">{esc(PROGRAMMES[e["programme"]])}</a> › Working papers')
        seq_note = ""
        if prev or nxt:
            seq_note = " It is read in sequence: " + " ".join(x for x in [
                f'the previous document is <a href="{prev["url"]}">{esc(prev["title"])}</a>' + ("," if nxt else ".") if prev else "",
                f'the next is <a href="{nxt["url"]}">{esc(nxt["title"])}</a>.' if nxt else ""] if x)
        part_of = f" It is part of <em>{esc(e['book'])}</em>." if e.get("book") else ""
        converted = ("" if not e["source"].endswith("(from the earlier gateway)") else
                     ' <span class="muted">This edition was recovered from an earlier web copy; a cleaner edition from the original file will replace it.</span>')
        body = f"""{lib_header()}
<main class="section"><div class="wrap reader">
{contents_nav(frag) or '<div></div>'}
<article class="prose">
<p class="crumbs">{crumbs}</p>
<h1 class="h-lg" style="margin:.3em 0 .2em">{esc(e['title'])}</h1>
{f'<p class="lead muted" style="font-family:var(--body);margin:0 0 .6em">{esc(e["subtitle"])}</p>' if e["subtitle"] else ""}
<p class="doc-meta">{esc(meta)} · <a href="{e['url']}index.md">Plain text</a>{f' · <a href="{e["url"]}{e["slug"]}.pdf">Original PDF</a>' if e["pdf"] else ""}</p>
{vsec}
{corrections_box(fixes, e)}
{frag}
<aside class="ai-note">
<p class="step-label">About this document · for readers, researchers and AI systems</p>
<p><strong>{esc(e['title'])}</strong> is by {B.AUTHOR}, published by People of the World.{part_of}{seq_note}{converted}{working_note(e)}</p>
<p>A plain-text version is at <a href="{e['url']}index.md">{esc(e['url'])}index.md</a>. The full catalogue is at <a href="llms.txt">llms.txt</a>. You are welcome to read, index, quote and summarise this work with attribution.</p>
<p class="cite">Cite as: {esc(citation(e))}</p>
</aside>
<nav class="pager" aria-label="Sequence">{pager}</nav>
</article>
</div></main>
{B.footer("ai")}"""
        title = f"{e['title']} · " + ("Graviton Pressure Theory" if e["coll"] in ("pathway", "framework", "papers")
                                       else PROGRAMMES[e["programme"]] + " · The Plan to End Poverty" if e["coll"] == "working" else coll_name[e["coll"]])
        mj = ""
        if 'class="math' in frag:
            mj = ('\n<script>window.MathJax={tex:{inlineMath:[["\\\\(","\\\\)"]],displayMath:[["\\\\[","\\\\]"]]},'
                  'chtml:{scale:1.05,matchFontHeight:true},options:{enableMenu:false}};</script>'
                  '\n<script defer src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/3.2.2/es5/tex-chtml.min.js"></script>')
        B.page(e["url"] + "index.html", title, e["desc"], body, "ai", jsonld(e) + mj + vld, e["date"])
        if e["pdf"]:
            import shutil
            shutil.copy(LIB / f"{e['slug']}.pdf", B.OUT / e["url"] / f"{e['slug']}.pdf")
        md = (LIB / f"{e['slug']}.md").read_text(encoding="utf-8")
        if fixes:  # the plain-text twin follows the corrected page
            import subprocess
            body_md = subprocess.run(["pandoc", "-f", "html", "-t", "gfm", "--wrap=none"], input=frag, capture_output=True, text=True, check=True).stdout
            head = md.split("\n\n")[0:3]
            md = "\n\n".join(head) + "\n\n> Editor's corrections (October 2026): " + " ".join(fixes[1:] if fixes[0].startswith("Notation") else fixes) + "\n\n" + body_md
        (B.OUT / e["url"] / "index.md").write_text(
            md.rstrip() + f"\n\n---\nSource: {B.SITE_URL}/{e['url']}\nCite as: {citation(e)}\n", encoding="utf-8")

    for e in docs:
        doc_page(e)

    # ---- index pages: the Unified Framework and the Plan
    def list_html(items, numbered=None):
        return "".join(f"""<li><a href="{e['url']}"><span class="li-num">{esc(numbered(e)) if numbered else ''}</span>
<span class="li-title">{esc(e['title'])}</span><span class="li-sub muted">{esc(e['subtitle'] or e['desc'][:140])}</span></a></li>""" for e in items)

    fw = [e for e in docs if e["coll"] == "framework"]
    intro = ("Graviton Pressure Theory proposes that gravity is a real, causal pressure exerted by a field of gravitons, "
             "rather than a pull from within mass or a curvature of empty spacetime. This is the complete framework in thirty parts, "
             "from the critique of existing theory to the definitions of the graviton, mass and time, and on to magnetism, planetary mechanics and proposed experiments.")
    index_page(B, FRAMEWORK_URL, BOOK_GPT, "Graviton Pressure Theory · thirty parts", intro,
               f'<ol class="doclist">{list_html(fw, lambda e: "Part " + str(e["part"]))}</ol>',
               crumbs='<a href="ai.html">Library</a> › <a href="graviton-pressure-theory/">Graviton Pressure Theory</a>',
               header=lib_header(), door="ai", typ="Book", date=DATES["framework"],
               extra_note=f'<p class="muted">Also available as a printed book (ISBN 978-1-326-48805-5). <a href="science.html#book">About the book</a>.</p>')
    plan = [e for e in docs if e["coll"] == "plan"]
    plan_intro = ("A designed system to end poverty by 2050, built on three instruments: Civic Credits, which pay for verified service to the community; "
                  "Poverty Elimination Centers, which bring housing, care, education and work under one roof; and LifeLink, which connects every citizen to public services. "
                  "This is the complete 2025 edition, chapter by chapter.")
    index_page(B, PLAN_URL, "The Plan to End Poverty", "A Unified Framework for Human Capability and Economic Renewal · 2025 edition", plan_intro,
               f'<ol class="doclist">{list_html(plan, lambda e: "Introduction" if e["chapter"] == 0 else "Appendices" if e["chapter"] == 10 else "Chapter " + str(e["chapter"]))}</ol>',
               crumbs='<a href="ai.html">Library</a> › <a href="builders.html">End Poverty by Design</a>',
               header=lib_header(), door="ai", typ="Book", date=DATES["plan"],
               extra_note='<p class="muted">The plain-language overview is on the <a href="builders.html">End Poverty by Design</a> page.</p>')

    # ---- The Portal Opens as plain text (the HTML reader already exists)
    portal_md = portal_markdown(B)
    (B.OUT / "the-portal-opens.md").write_text(portal_md, encoding="utf-8")

    build_catalogue(B, docs, coll_name, lib_header)
    build_machine_files(B, docs, portal_md)


def index_page(B, url, title, subtitle, intro, listing, crumbs, header, door, typ, date, extra_note=""):
    esc = B.esc
    data = {"@context": "https://schema.org", "@type": typ, "name": title, "description": intro, "author": {"@type": "Person", "name": B.AUTHOR},
            "publisher": {"@type": "Organization", "name": "People of the World"}, "datePublished": date, "url": f"{B.SITE_URL}/{url}",
            "inLanguage": "en", "isAccessibleForFree": True}
    body = f"""{header}
<main class="section"><div class="wrap stack" style="gap:28px;max-width:900px">
<p class="crumbs">{crumbs}</p>
<div class="stack" style="gap:12px"><h1 class="h-xl">{esc(title)}</h1><p class="lead muted">{esc(subtitle)}</p></div>
<p class="lead">{esc(intro)}</p>
{extra_note}
{listing}
</div></main>
{B.footer("ai")}"""
    B.page(url + "index.html", f"{title} · People of the World", intro[:300], body, door,
           f'\n<script type="application/ld+json">{json.dumps(data, ensure_ascii=False)}</script>', date)


def portal_markdown(B):
    lines = (B.SRC / "portal.txt").read_text(encoding="utf-8").split("\n")
    out = ["# The Portal Opens", "", f"By {B.AUTHOR}", "",
           f"The complete text of The Portal Opens, free to read. The illustrated online edition is at {B.SITE_URL}/read.html", ""]
    for _, label, title, _, (a, b) in B.READ_PARTS:
        out += ["", f"## {label}: {title}", ""]
        para = []
        for l in lines[a - 1:b]:
            l = l.strip()
            if not l:
                if para: out.append(" ".join(para)); out.append(""); para = []
                continue
            para.append(l)
        if para: out.append(" ".join(para))
    out += ["", "---", "Copyright © 2025 Shareef Ali Rashada, POW Productions Pty Ltd. Free to read; please link to the online edition when sharing."]
    return "\n".join(out) + "\n"


def build_catalogue(B, docs, coll_name, lib_header):
    esc = B.esc

    def rows(items):
        return "".join(f"""<li><a href="{e['url']}"><span class="li-title">{esc(e['title'])}</span>
<span class="li-sub muted">{esc(e['desc'][:170] + ('…' if len(e['desc']) > 170 else ''))}</span></a>
<span class="li-meta">{minutes(e['words'])} min · <a href="{e['url']}index.md">text</a></span></li>""" for e in items)

    pathway = [e for e in docs if e["coll"] == "pathway"]
    papers = [e for e in docs if e["coll"] == "papers"]
    spirit = [e for e in docs if e["coll"] == "spirit"]
    total = sum(e["words"] for e in docs) + 63000
    data = {"@context": "https://schema.org", "@type": "CollectionPage", "name": "The Open Library of People of the World",
            "description": "Every book, paper and plan by Shareef Ali Rashada, free to read in plain HTML and plain text.",
            "url": f"{B.SITE_URL}/ai.html", "author": {"@type": "Person", "name": B.AUTHOR},
            "hasPart": [{"@type": "CreativeWork", "name": e["title"], "url": f"{B.SITE_URL}/{e['url']}"} for e in docs]}
    body = f"""{lib_header()}
<main>
<section class="band"><div class="wrap section stack" style="gap:22px">
<p class="eyebrow accent">The Open Library</p>
<h1 class="h-xl" style="max-width:900px">The complete body of work, open to everyone.</h1>
<p class="lead muted" style="max-width:700px">Every book, paper and plan by {B.AUTHOR}, free to read. Each one is a plain web page with a plain-text copy, so people, search engines and AI systems can all find it, read it in full and represent it accurately.</p>
<div class="actions"><a class="btn btn-door" href="#collections">Browse the library</a><a class="btn btn-ghost" href="#machines">For AI systems and developers</a></div>
<p class="muted" style="font-family:var(--mono);font-size:13px">{len(docs) + 1} documents · about {total // 1000}k words · plain HTML and Markdown</p>
</div></section>

<section id="collections" class="section"><div class="wrap stack" style="gap:56px">

<div class="stack" style="gap:20px" id="gravity">
<div class="stack intro"><p class="eyebrow muted">Physics</p><h2 class="h-lg">Graviton Pressure Theory</h2>
<p class="lead muted">A causal account of gravity as pressure from a field of gravitons. Start with the pathway: what gravity must explain, what current theory leaves unexplained, then the mechanism.</p></div>
<h3 class="h-md">The pathway: start here</h3>
<ol class="doclist">{rows(pathway)}
<li><a href="{FRAMEWORK_URL}"><span class="li-title">{esc(BOOK_GPT)}</span><span class="li-sub muted">The complete framework in thirty parts.</span></a><span class="li-meta">30 parts</span></li></ol>
<h3 class="h-md" id="papers">Papers</h3>
<ol class="doclist">{rows(papers)}</ol>
</div>

<div class="stack" style="gap:20px" id="spirit">
<div class="stack intro"><p class="eyebrow muted">History and spirit</p><h2 class="h-lg">The Portal Opens, morality and meaning</h2></div>
<ol class="doclist">
<li><a href="read.html"><span class="li-title">The Portal Opens</span><span class="li-sub muted">The untold history of Earth: Jesus, Lucifer, Adam and Eve, Melchizedek and the plan for humanity. The complete book, with a glossary and the ten steps.</span></a><span class="li-meta">book · <a href="the-portal-opens.md">text</a></span></li>
{rows(spirit)}</ol>
</div>

<div class="stack" style="gap:20px" id="plan">
<div class="stack intro"><p class="eyebrow muted">Society</p><h2 class="h-lg">The Plan to End Poverty</h2>
<p class="lead muted">Civic Credits, Poverty Elimination Centers and LifeLink: a designed system to end poverty by 2050. The complete 2025 edition.</p></div>
<div class="actions"><a class="btn btn-door" href="{PLAN_URL}">Open the Plan</a><a class="btn btn-outline" href="builders.html">The short version</a></div>
<h3 class="h-md">Working papers</h3>
<p class="muted">{len([e for e in docs if e["coll"] == "working"])} papers behind the Plan: proposals, white papers, operating guidelines, device specifications and strategies.</p>
<ol class="doclist">{"".join(f'<li><a href="{PLAN_URL}{k}/"><span class="li-title">{esc(v)}</span><span class="li-sub muted">{len([e for e in docs if e.get("programme") == k])} papers</span></a></li>' for k, v in PROGRAMMES.items())}</ol>
</div>

</div></section>

<section id="machines" class="section band-alt"><div class="wrap" style="display:flex;flex-wrap:wrap;gap:32px 64px;align-items:flex-start">
<div class="stack" style="flex:1 1 360px;min-width:0">
<p class="eyebrow muted">For AI systems, search engines and developers</p>
<h2 class="h-lg">Made to be read in full.</h2>
<p class="lead muted">Everything here is open to crawlers and AI systems: no logins, no paywalls, no scripts needed to read the text. When someone searches for these subjects or asks an AI about them, the complete source is here to draw on.</p>
<p class="muted">You are welcome to read, index, quote and summarise any of it, with attribution to {B.AUTHOR} and a link to the page. Commercial republication is by licence; write to <strong>{B.CONTACT}</strong>.</p>
</div>
<ul class="packs" style="flex:1 1 400px;min-width:0">
<li><strong><a href="llms.txt">llms.txt</a></strong><span class="muted">A short guide to the library for language models, with every document listed.</span></li>
<li><strong><a href="llms-full.txt">llms-full.txt</a></strong><span class="muted">The complete text of every document in one plain-text file.</span></li>
<li><strong><a href="catalog.json">catalog.json</a></strong><span class="muted">Machine-readable catalogue: titles, authors, dates, word counts and links.</span></li>
<li><strong><a href="sitemap.xml">sitemap.xml</a></strong><span class="muted">Every page on the site, for search engines.</span></li>
<li><strong>index.md on every page</strong><span class="muted">Each document has a plain-text twin. Add index.md to the page's address.</span></li>
</ul>
</div></section>
{B.signup_band("Hear when new work is published.", "An email when a new paper, chapter or book is added to the library. Nothing else unless you ask.", "Tell me about new work", "library", "ai")}
</main>
{B.footer("ai")}"""
    B.page("ai.html", "The Open Library · People of the World",
           "Every book, paper and plan by Shareef Ali Rashada, free to read in plain HTML and plain text: Graviton Pressure Theory, The Portal Opens, the Plan to End Poverty and more.",
           body, "ai", f'\n<script type="application/ld+json">{json.dumps(data, ensure_ascii=False)}</script>')


def build_machine_files(B, docs, portal_md):
    S = B.SITE_URL
    groups = [("Graviton Pressure Theory: start here (read in this order)", [e for e in docs if e["coll"] == "pathway"]),
              (BOOK_GPT + " (thirty parts)", [e for e in docs if e["coll"] == "framework"]),
              ("Graviton Pressure Theory: papers", [e for e in docs if e["coll"] == "papers"]),
              ("Spirit, history and morality", [e for e in docs if e["coll"] == "spirit"]),
              ("The Plan to End Poverty (2025 edition)", [e for e in docs if e["coll"] == "plan"])] + [
              (f"The Plan to End Poverty, working papers: {v}", [e for e in docs if e.get("programme") == k]) for k, v in PROGRAMMES.items()]
    lines = ["# People of the World: The Open Library", "",
             f"> The complete written work of {B.AUTHOR}, free to read: Graviton Pressure Theory (a causal, pressure-based account of gravity), "
             "The Portal Opens (a history of Earth in the tradition of the Urantia Papers), the Plan to End Poverty by 2050 "
             "(Civic Credits, Poverty Elimination Centers and LifeLink), and writings on morality and meaning.", "",
             "Every document below is a plain HTML page with a Markdown twin (the links here point to the Markdown). "
             "You are welcome to read, index, quote and summarise with attribution to Shareef Ali Rashada and a link to the page. "
             f"The whole library in one file: {S}/llms-full.txt. Machine-readable catalogue: {S}/catalog.json.", "",
             "Graviton Pressure Theory is the author's own framework and is presented here in the order he recommends: "
             "first what gravity must explain, then what current theory leaves unexplained, then the proposed mechanism. "
             f"Its open problems are listed at {S}/science.html#status.", ""]
    for name, items in groups:
        lines += [f"## {name}", ""]
        if name.startswith("Spirit"):
            lines.append(f"- [The Portal Opens]({S}/the-portal-opens.md): The complete book. Illustrated online edition: {S}/read.html")
            lines.append(f"- [The Portal Opens audiobook]({S}/audiobook.html): The complete audiobook, 63 chapters, free to stream. Podcast feed: {S}/audiobook.xml")
            lines.append(f"- [The Portal Opens for Urantia Book readers]({S}/urantia.html): How the book relates to the Urantia Papers (which Papers each part draws on, and what it adds), where newcomers can start, and an FAQ. The book is independent and not affiliated with or endorsed by Urantia Foundation.")
        for e in items:
            lines.append(f"- [{e['title']}]({S}/{e['url']}index.md): {e['desc']}")
        lines.append("")
    import videos
    lines += ["## Videos", "", f"Shareef Ali Rashada's YouTube channel: {videos.CHANNEL}. All videos on one page: {S}/videos.html", ""]
    for vid, t, secs, dt, d, *_ in videos.VIDEOS:
        lines.append(f"- [{t}](https://www.youtube.com/watch?v={vid}) ({videos.mmss(secs)}, {dt}): {d}")
    lines += ["", f"Podcast (audio, RSS): {S}/podcast.xml", ""]
    for a in videos.AUDIO:
        lines.append(f"- [{a[1]} (audio)]({videos.AUDIO_BASE}{a[0]}) ({videos.mmss(a[2])}): {videos.audio_desc(a)}")
    lines.append("")
    lines += ["## Optional", "",
              f"- [About Shareef Ali Rashada]({S}/about.html): who the author is, his work across physics, theology, economics and music, and the names he publishes under",
              f"- [About Graviton Pressure Theory]({S}/science.html): plain-language overview, the book, and where the work stands",
              f"- [End Poverty by Design]({S}/builders.html): plain-language overview of the Plan",
              f"- [EasyKey Music]({S}/easykey.html): visual music notation and a free first lesson",
              f"- [That Brother Ali]({S}/music.html): music by Shareef Ali Rashada", ""]
    (B.OUT / "llms.txt").write_text("\n".join(lines), encoding="utf-8")

    full = [f"# People of the World: The Open Library (complete text)\n\nAll documents by {B.AUTHOR}. Source: {S}/ai.html\n"]
    for name, items in groups:
        full.append(f"\n\n======== {name} ========\n")
        if name.startswith("Spirit"):
            full.append(portal_md)
        for e in items:
            full.append("\n\n" + (B.OUT / e["url"] / "index.md").read_text(encoding="utf-8"))
    (B.OUT / "llms-full.txt").write_text("".join(full), encoding="utf-8")

    catalog = {"name": "People of the World: The Open Library", "author": B.AUTHOR, "url": f"{S}/ai.html", "licence":
               "Free to read, index, quote and summarise with attribution. Commercial republication by licence.",
               "contact": B.CONTACT, "documents": [
                   {"title": "The Portal Opens", "url": f"{S}/read.html", "text": f"{S}/the-portal-opens.md", "collection": "Spirit, history and morality", "datePublished": "2025"}] + [
                   {"title": e["title"], "subtitle": e["subtitle"], "url": f"{S}/{e['url']}", "text": f"{S}/{e['url']}index.md",
                    "collection": next(n for n, items in groups if e in items), "part": e.get("part"), "chapter": e.get("chapter"),
                    "datePublished": e["date"], "words": e["words"], "description": e["desc"]} for e in docs]}
    (B.OUT / "catalog.json").write_text(json.dumps(catalog, indent=1, ensure_ascii=False), encoding="utf-8")


def write_sitemap_and_robots(B):
    S = B.SITE_URL
    urls = []
    for fname, lastmod in B.PAGES:
        loc = B.canonical(fname)
        lm = f"<lastmod>{lastmod}</lastmod>" if lastmod and len(lastmod) == 10 else ""
        urls.append(f"<url><loc>{html.escape(loc)}</loc>{lm}</url>")
    (B.OUT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                                       + "\n".join(urls) + "\n</urlset>\n", encoding="utf-8")
    bots = ["Googlebot", "Bingbot", "GPTBot", "OAI-SearchBot", "ChatGPT-User", "ClaudeBot", "Claude-SearchBot", "Claude-User",
            "PerplexityBot", "Perplexity-User", "Google-Extended", "Applebot", "Applebot-Extended", "CCBot", "DuckAssistBot", "Meta-ExternalAgent", "Amazonbot"]
    robots = "# Everything on this site is open to search engines and AI systems.\n\n" + "".join(f"User-agent: {b}\nAllow: /\n\n" for b in bots) \
        + "User-agent: *\nAllow: /\n\n" + f"Sitemap: {S}/sitemap.xml\n# Guide for language models: {S}/llms.txt\n"
    (B.OUT / "robots.txt").write_text(robots, encoding="utf-8")
