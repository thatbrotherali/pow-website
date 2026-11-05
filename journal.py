"""A Deeper Look: the weekly journal (journal/ and journal/<date>/).

Each edition is one file in src/journal/, named by its week-ending date:

    src/journal/2026-11-08.html
    title: The lead story's headline
    summary: One or two sentences for the archive and for link previews.
    ---
    <section>...the edition as HTML...</section>

In the text, mark a statement's status with one of these (the key is added by the build):
    <span class="st st-e">Established</span>  <span class="st st-a">Argued</span>
    <span class="st st-h">Hypothesis</span>   <span class="st st-o">Open</span>
Pictures go in docs/assets/journal/<date>/ and are referenced as assets/journal/<date>/name.jpg.
Styles: docs/assets/journal.css. The rules for writing an edition are in the Project's journal guide.
Links to the journal appear around the site only once the first edition exists.
"""
import datetime, html, json, re

NAME = "A Deeper Look"
TAGLINE = "The week's news, and what it shows about the world."
KEY = [("e", "Established", "measured or documented."), ("a", "Argued", "our reasoning."),
       ("h", "Hypothesis", "a proposal from People of the World's frameworks."), ("o", "Open", "not yet known.")]
WHY = "Why read the news this way? Because every person carries a portion of the Creator, and the events of each week are people learning, slowly, to live as one family."


def editions(root):
    """Published editions, newest first."""
    found = []
    for path in (root / "src" / "journal").glob("*.html"):
        text = path.read_text(encoding="utf-8")
        meta, _, body = text.partition("\n---\n")
        fields = dict(line.split(": ", 1) for line in meta.splitlines() if ": " in line)
        date = datetime.date.fromisoformat(path.stem)
        found.append({"slug": path.stem, "date": date, "title": fields["title"], "summary": fields["summary"], "body": body})
    return sorted(found, key=lambda e: e["date"], reverse=True)


def has_editions(root):
    return any((root / "src" / "journal").glob("*.html"))


def long_date(d):
    return f"{d.day} {d.strftime('%B %Y')}"


def key_html():
    items = "".join(f'<li><span class="st st-{k}"><strong>{name}</strong></span>: {text}</li>' for k, name, text in KEY)
    return f"""<aside class="journal-key" aria-label="Key to the status colours"><h2 class="h-md">Key: how close each statement is to verified</h2>
<p class="muted">Coloured statements go beyond the reported news. From closest to verified to furthest:</p><ul>{items}</ul></aside>"""


def nav():
    return [("All editions", "journal/index.html", False, None), ("The hub", "index.html", False, None), ("Books", "books.html", False, None)]


def css(b):
    return f'\n<link rel="stylesheet" href="assets/journal.css?v={b.asset_v("journal.css")}">'


def ld(b, e, url):
    return json.dumps({"@context": "https://schema.org", "@type": "Article", "headline": e["title"], "description": e["summary"],
                       "datePublished": e["slug"], "url": b.canonical(url), "inLanguage": "en", "isPartOf": {"@type": "Periodical", "name": NAME},
                       "author": {"@type": "Person", "name": b.AUTHOR, "@id": f"{b.SITE_URL}/about.html#shareef"},
                       "publisher": {"@type": "Organization", "name": "People of the World", "url": b.SITE_URL}}, ensure_ascii=False)


def build_edition(b, e, newer, older):
    fname = f"journal/{e['slug']}/index.html"
    links = ""
    if older:
        links += f'<a class="pager-prev" href="journal/{older["slug"]}/index.html"><span>Previous edition</span>{b.esc(older["title"])}</a>'
    if newer:
        links += f'<a class="pager-next" href="journal/{newer["slug"]}/index.html"><span>Next edition</span>{b.esc(newer["title"])}</a>'
    body = f"""{b.header(NAME, "The journal of People of the World", nav())}
<main>
<section class="band"><div class="wrap section dg-hero">
<p class="eyebrow accent">Week ending {long_date(e["date"])}</p>
<h1 class="h-xl">{NAME}</h1>
<p class="lead muted" style="max-width:700px;margin-top:16px">{b.esc(e["summary"])}</p>
</div></section>
<section class="section"><div class="wrap"><article class="prose journal">
{e["body"]}
{key_html()}
</article>
<nav class="pager" aria-label="Other editions" style="max-width:68ch">{links}</nav>
</div></section>
{b.why_band(WHY)}</main>
{b.footer()}"""
    extra = css(b) + f'\n<script type="application/ld+json">{ld(b, e, fname)}</script>'
    b.page(fname, f"{e['title']} | {NAME}", e["summary"], body, extra_head=extra, lastmod=e["slug"])


def build_index(b, all_editions):
    if all_editions:
        items = "".join(f"""<li><a href="journal/{e["slug"]}/index.html"><span class="li-num">Week ending {long_date(e["date"])}</span>
<span class="li-title">{b.esc(e["title"])}</span><span class="li-sub muted">{b.esc(e["summary"])}</span></a></li>""" for e in all_editions)
        content = f'<h2 class="h-lg" style="margin-bottom:20px">Editions</h2><ul class="doclist">{items}</ul>'
    else:
        content = '<p class="lead muted">The first edition is on its way.</p>'
    body = f"""{b.header(NAME, "The journal of People of the World", [("The hub", "index.html", False, None), ("Books", "books.html", False, None)])}
<main>
<section class="band"><div class="wrap section dg-hero">
<p class="eyebrow accent">The journal of People of the World</p>
<h1 class="h-xl">{NAME}</h1>
<p class="lead muted" style="max-width:680px;margin-top:16px">{TAGLINE} Each week: science, economics, culture and politics, faith, and AI, read for how things actually work and for what brings humanity closer together.</p>
</div></section>
<section class="section"><div class="wrap" style="max-width:860px">{content}</div></section>
</main>
{b.footer()}"""
    extra = css(b) + ("" if all_editions else '\n<meta name="robots" content="noindex">')
    b.page("journal/index.html", f"{NAME}: the journal of People of the World", f"{TAGLINE} A weekly journal from People of the World.", body, extra_head=extra)
    if not all_editions:
        b.PAGES.pop()  # stays out of the sitemap until there is something to read


def build(b):
    all_editions = editions(b.ROOT)
    build_index(b, all_editions)
    for i, e in enumerate(all_editions):
        newer = all_editions[i - 1] if i else None
        older = all_editions[i + 1] if i + 1 < len(all_editions) else None
        build_edition(b, e, newer, older)
