"""For librarians: every book with its ISBNs, formats, audience and how to order, one-page sheets to print,
and a section asking readers to request the books at their own library. Called from build.py."""
import json, pathlib

B = None
esc = None

# Each book: editions are (label, isbn, note). Only facts confirmed from retailer listings or the books themselves.
BOOKS = [
    {"slug": "the-portal-opens", "title": "The Portal Opens", "sub": "A Revelation of the Cosmos", "cover": "assets/cover-portal.webp", "w": 384, "h": 576,
     "door": "seekers", "year": "2025",
     "editions": [("Paperback", "978-1-326-60989-4", "301 pages"), ("Hardcover", "978-1-326-56533-6", ""), ("Kindle ebook", "", "Amazon"), ("Audiobook", "", "AI narration, on Spotify")],
     "subjects": "Religion and spirituality · Christianity and Jesus · The Urantia Book",
     "audience": "Adult general readers; spiritual seekers; readers of The Urantia Book",
     "blurb": "The history behind the story, as transmitted by Gabriel: Jesus, Lucifer, Caligastia, Adam and Eve, and Melchizedek. Warm and accessible, it asks what we were never told, and why every faith points to a portion of the Creator within each person.",
     "why": ["Winner of the Literary Titan Silver Book Award: “A wild, luminous ride worth taking.”", "Readers of The Urantia Book ask for it by name: an audience of its own.", "Free to read online too, so a library copy reaches readers who prefer print."],
     "more": "seekers.html#book"},
    {"slug": "unified-framework", "title": "The Unified Framework for the Graviton Pressure Theory", "sub": "", "cover": "assets/cover-gpt.webp", "w": 384, "h": 501,
     "door": "science", "year": "2025",
     "editions": [("Hardcover", "978-1-326-48805-5", "")],
     "subjects": "Science · Physics · Gravity",
     "audience": "Readers of popular and alternative physics; students; researchers",
     "blurb": "Gravity as a pressure from the medium of space, with a named physical mechanism, the mathematics and proposed tests, in thirty parts. An open invitation to researchers working on space as a medium, from analogue gravity to superfluid vacuum.",
     "why": ["A complete, testable framework with its open problems stated, not hidden.", "All thirty parts are also free online, so the library copy serves readers who study in print.", "By an author and researcher based in Queensland, Australia."],
     "more": "science.html#book"},
    {"slug": "easykey", "title": "Learning to Play the EasyKey Way", "sub": "Special Library Edition", "cover": "assets/cover-easykey.webp", "w": 496, "h": 701,
     "door": "easykey", "year": "2021",
     "editions": [("Special Library Edition, paperback", "978-1-4709-4290-8", "111 pages"), ("Special Home Edition, paperback", "978-1-4717-9103-1", "")],
     "subjects": "Music · Instruction and study · Piano and keyboard",
     "audience": "Beginners of any age, children with a parent, families, music teachers",
     "blurb": "A year of piano in twelve keys, written entirely in EasyKey's visual notation: no staff to decode, just the keys you press, read from top to bottom. Scales, arpeggios, chords and chord patterns, with 26 songs from beginner to advanced.",
     "why": ["EasyKey was a 2016 finalist in the Moreton Bay Regional Council Innovation Awards.", "A written method for the way most beginners now learn: by seeing which keys to press.", "Works alone or with a whole family learning together."],
     "more": "easykey.html"},
    {"slug": "my-first-book-of-songs", "title": "My First Book of Songs", "sub": "EasyKey Visual Music Notation", "cover": "", "w": 0, "h": 0,
     "door": "easykey", "year": "2021",
     "editions": [("Paperback", "978-1-4717-9102-4", "")],
     "subjects": "Music · Songbooks · Piano and keyboard",
     "audience": "Young beginners and families; companion to Learning to Play the EasyKey Way",
     "blurb": "38 songs arranged in the EasyKey Visual Music Notation System, for beginners who want to play real songs from the first day.",
     "why": ["The natural companion to the EasyKey method book.", "Songs a child can play within the first lessons."],
     "more": "easykey.html"},
    {"slug": "people-of-the-world", "title": "People of the World", "sub": "A novel", "cover": "assets/cover-pow.webp", "w": 212, "h": 320,
     "door": "seekers", "year": "2011",
     "editions": [("Paperback", "978-1-4477-7737-3", ""), ("Kindle ebook", "", "Amazon")],
     "subjects": "Fiction · Science fiction · Visionary and metaphysical",
     "audience": "Adults only (18+): strong language, sexual content, drug use and violence",
     "blurb": "On July 11, 2012, aliens take three-quarters of humanity. The people left behind must rebuild a world where force no longer works and money loses its meaning, while a young man named Jason is shown the history of the universe.",
     "why": ["Speculative fiction about rebuilding society without force or money.", "The novel that opens the reading path to The Portal Opens."],
     "more": "books.html#novel"},
]


def ed_rows(b):
    return "".join(f'<tr><td>{esc(lbl)}</td><td class="mono">{esc(isbn) if isbn else "—"}</td><td>{esc(note)}</td></tr>' for lbl, isbn, note in b["editions"])


def cover(b, width=180):
    if b["cover"]:
        return f'<img class="cover-img" src="{b["cover"]}" alt="Cover of {esc(b["title"])}" width="{b["w"]}" height="{b["h"]}" loading="lazy" style="width:{width}px">'
    return (f'<div class="cover-img" role="img" aria-label="{esc(b["title"])}" style="width:{width}px;aspect-ratio:2/3;display:grid;place-items:center;text-align:center;'
            f'padding:16px;background:var(--navy);color:var(--band-fg);font-family:var(--display);font-size:20px;line-height:1.2;border-radius:10px">{esc(b["title"])}</div>')


def book_card(b):
    why = "".join(f"<li>{esc(w)}</li>" for w in b["why"])
    return f"""<article id="{b['slug']}" class="card door-{b['door']}" style="gap:18px">
<div style="display:flex;flex-wrap:wrap;gap:24px;align-items:flex-start">
<div style="flex:0 0 auto">{cover(b, 150)}</div>
<div class="stack" style="flex:1 1 320px;min-width:0;gap:10px">
<h3 class="h-md">{esc(b['title'])}</h3>{f'<p class="muted" style="margin-top:-6px">{esc(b["sub"])}</p>' if b['sub'] else ''}
<p class="muted" style="font-size:15px">By {esc(B.AUTHOR)} · Lulu · {b['year']}</p>
<p>{esc(b['blurb'])}</p>
<p style="font-size:15px"><strong>Subjects:</strong> {esc(b['subjects'])}<br><strong>Audience:</strong> {esc(b['audience'])}</p>
</div></div>
<div class="table-wrap"><table class="dg-table" style="font-size:15px"><thead><tr><th>Edition</th><th>ISBN</th><th>Notes</th></tr></thead><tbody>{ed_rows(b)}</tbody></table></div>
<div><strong style="font-size:15px">Why readers borrow it</strong><ul style="margin:6px 0 0;padding-left:20px;font-size:15px">{why}</ul></div>
<div class="actions"><a class="btn btn-outline" href="assets/librarians/{b['slug']}.pdf">One-page sheet (PDF)</a><a class="btn btn-ghost" href="{b['more']}">About the book</a></div>
</article>"""


def build(b):
    global B, esc
    B, esc = b, b.esc
    cards = "\n".join(book_card(x) for x in BOOKS)
    isbn_list = "\n".join(f"{x['title']} ({lbl}): ISBN {isbn}" for x in BOOKS for lbl, isbn, _ in x["editions"] if isbn)
    request_text = ("Hello, I'd like to suggest a book for the library: The Portal Opens by Shareef Ali Rashada "
                    "(paperback, ISBN 978-1-326-60989-4), winner of the Literary Titan Silver Book Award. "
                    "It's distributed worldwide through Ingram. Thank you!")
    body = f"""{B.header("People of the World", "For librarians", [("The books", "#books", False, None), ("Ordering", "#ordering", False, None), ("Ask your library", "#ask", True, None)])}
<main>
<section class="band"><div class="wrap section stack" style="gap:18px;max-width:900px">
<p class="eyebrow" style="color:var(--band-muted)">For librarians and library suppliers</p>
<h1 class="h-xl">Books by Shareef Ali Rashada</h1>
<p class="lead muted">Five books, from a visual way to learn piano to a new account of gravity. Every ISBN, edition and ordering route is on this page, with a one-page sheet for each book.</p>
<div class="actions"><a class="btn btn-door" href="#books">See the books</a><a class="btn btn-ghost" href="mailto:{B.CONTACT}?subject=Library%20enquiry">Ask for a review copy</a></div>
</div></section>

<section id="books" class="section"><div class="wrap stack" style="gap:28px;max-width:1000px">
{cards}
</div></section>

<section id="ordering" class="section band-alt"><div class="wrap stack" style="gap:20px;max-width:900px">
<h2 class="h-lg">Ordering</h2>
<ul class="pathways">
<li><strong>Print, worldwide</strong><span class="muted">Every print edition is distributed through Ingram (Lulu Global Distribution). Order by ISBN from Ingram Library Services or your usual supplier.</span></li>
<li><strong>Australia and New Zealand</strong><span class="muted">Ask your supplier to source the title by ISBN. If they can't, write to us and we'll arrange supply directly.</span></li>
<li><strong>Ebooks and audiobooks for libraries</strong><span class="muted">Library editions for OverDrive, hoopla, BorrowBox and cloudLibrary are in preparation. Until then, The Portal Opens and People of the World are available as Kindle ebooks, and The Portal Opens audiobook is on Spotify.</span></li>
<li><strong>Review copies, author talks and EasyKey sessions</strong><span class="muted">For review copies, or a talk or a hands-on EasyKey music session at your library (South East Queensland, or online anywhere), write to <a href="mailto:{B.CONTACT}">{B.CONTACT}</a>.</span></li>
</ul>
<details class="card"><summary style="cursor:pointer;font-weight:600">All ISBNs as plain text</summary><pre class="mono" style="white-space:pre-wrap;margin:12px 0 0;font-size:14px">{esc(isbn_list)}</pre></details>
</div></section>

<section id="ask" class="section"><div class="wrap stack" style="gap:20px;max-width:900px">
<p class="eyebrow muted">For readers</p>
<h2 class="h-lg">Ask your library to stock these books</h2>
<p class="lead muted">Libraries buy the books their members ask for. One request from you can put a book on the shelf for everyone in your town, free to borrow.</p>
<ol class="pathways">
<li><strong>Find “Suggest a purchase”</strong><span class="muted">It's on most library websites, often under Services or your account, or just ask at the desk.</span></li>
<li><strong>Give the title, author and ISBN</strong><span class="muted">The ISBNs are listed above. Ask for the paperback if you're not sure.</span></li>
<li><strong>Use the library apps too</strong><span class="muted">If your library uses Libby, hoopla or BorrowBox, look for the books there once the library ebook editions are out, and tap Notify me or Suggest.</span></li>
</ol>
<div class="card"><strong>Words you can copy</strong><p id="ask-text" style="font-size:15px">{esc(request_text)}</p>
<p><button class="copy-btn" type="button" data-copy="{esc(request_text)}">Copy</button></p></div>
</div></section>
{B.signup_band("Hear when new editions reach libraries.", "Occasional updates on the books and where to find them. Unsubscribe any time.", "Keep me updated", "support", "hub")}
</main>
{B.footer()}"""
    items = [{"@type": "Book", "name": x["title"], "author": {"@type": "Person", "name": B.AUTHOR}, "isbn": isbn, "bookFormat": "https://schema.org/" + ("Hardcover" if "Hardcover" in lbl else "Paperback"),
              "publisher": {"@type": "Organization", "name": "Lulu Press"}} for x in BOOKS for lbl, isbn, _ in x["editions"] if isbn]
    ld = {"@context": "https://schema.org", "@type": "ItemList", "name": "Books by Shareef Ali Rashada for libraries",
          "itemListElement": [{"@type": "ListItem", "position": i + 1, "item": it} for i, it in enumerate(items)]}
    B.page("librarians.html", "For Librarians · Books by Shareef Ali Rashada",
           "ISBNs, editions, subjects and ordering for every book by Shareef Ali Rashada, with one-page sheets, and how readers can ask their library to stock them.", body,
           extra_head=f'\n<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>')
    write_sheets()


def write_sheets():
    """One printable A4 page per book (HTML), turned into PDFs by tools/sheets.cjs."""
    root = pathlib.Path(__file__).parent
    out = root / "build" / "sheets"
    out.mkdir(parents=True, exist_ok=True)
    fonts = root / "apps" / "lifelink" / "node_modules" / "@fontsource-variable"
    face = (f"@font-face{{font-family:Fraunces;src:url('{(fonts / 'fraunces/files/fraunces-latin-wght-normal.woff2').as_uri()}')}}"
            f"@font-face{{font-family:Inter;src:url('{(fonts / 'inter/files/inter-latin-wght-normal.woff2').as_uri()}')}}")
    for x in BOOKS:
        why = "".join(f"<li>{esc(w)}</li>" for w in x["why"])
        img = f'<img src="{(B.OUT / x["cover"]).as_uri()}" style="width:150px;border-radius:8px;box-shadow:0 6px 18px rgba(0,0,0,.18)">' if x["cover"] else \
              f'<div style="width:150px;aspect-ratio:2/3;background:#10304D;color:#F5F9FC;display:grid;place-items:center;text-align:center;padding:12px;font-family:Fraunces,Georgia,serif;font-size:18px;border-radius:8px">{esc(x["title"])}</div>'
        html = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><title>{esc(x['title'])} · for librarians</title>
<style>{face}@page{{size:A4;margin:16mm}}body{{font-family:Inter,system-ui,sans-serif;color:#0F2236;font-size:11pt;line-height:1.45;margin:0}}
h1{{font-family:Fraunces,Georgia,serif;font-weight:400;font-size:24pt;line-height:1.1;margin:0}}.sub{{color:#44566A;margin:4px 0 0}}
.top{{display:flex;gap:22px;align-items:flex-start}}.eyebrow{{font-size:8.5pt;letter-spacing:.12em;text-transform:uppercase;color:#44566A;margin:0 0 8px}}
table{{border-collapse:collapse;width:100%;margin:14px 0;font-size:10pt}}th,td{{text-align:left;padding:6px 8px;border-bottom:1px solid #D3E0EA}}th{{background:#E4EEF4}}
.mono{{font-family:'IBM Plex Mono',ui-monospace,monospace}}h2{{font-family:Fraunces,Georgia,serif;font-weight:400;font-size:13pt;margin:16px 0 6px}}
ul{{margin:0;padding-left:18px}}.foot{{margin-top:18px;padding-top:10px;border-top:2px solid #10304D;font-size:9.5pt;color:#44566A}}</style></head><body>
<p class="eyebrow">For librarians · People of the World</p>
<div class="top">{img}<div><h1>{esc(x['title'])}</h1>{f'<p class="sub">{esc(x["sub"])}</p>' if x['sub'] else ''}
<p class="sub">By {esc(B.AUTHOR)} · Lulu · {x['year']}</p><p style="margin-top:12px">{esc(x['blurb'])}</p></div></div>
<table><thead><tr><th>Edition</th><th>ISBN</th><th>Notes</th></tr></thead><tbody>{ed_rows(x)}</tbody></table>
<p><strong>Subjects:</strong> {esc(x['subjects'])}<br><strong>Audience:</strong> {esc(x['audience'])}</p>
<h2>Why readers borrow it</h2><ul>{why}</ul>
<h2>Ordering</h2><p>Print editions are distributed worldwide through Ingram (Lulu Global Distribution): order by ISBN from Ingram Library Services or your usual supplier. Australian and New Zealand libraries: ask your supplier to source by ISBN, or contact us for direct supply.</p>
<div class="foot">Review copies, author talks and EasyKey sessions: {B.CONTACT} · peopleoftheworld.net/librarians.html</div>
</body></html>"""
        (out / f"{x['slug']}.html").write_text(html, encoding="utf-8")
