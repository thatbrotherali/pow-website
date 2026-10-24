"""The Portal Opens audiobook: 63 chapters streamed from the Wix Music album on shop.peopleoftheworld.net.

Builds the audiobook page, the "Listen" player on each part of the free online edition,
and an audiobook feed (audiobook.xml) for Apple Podcasts, Spotify and other podcast apps.
"""
import html, json

BASE = "https://music.wixstatic.com/preview/eaef6d_"
ALBUM_COVER = "https://static.wixstatic.com/media/eaef6d_3fca3780afcc4598987553973bbb8e43~mv2.jpg"
RAW = """01|Opening|29ba90e4fb734a92975622c571f76100|02:15|808137
02|Gabriel's Glossary|7988b571de904125b2f294951bb9d5bc|15:02|5413482
03|Gabriel's Introduction and Mission|d4e9e22bbc7a47648306514dc6d16fc9|07:12|2592744
04|The Untold Story of Jesus|0d84e7d9b2b843a0a3ced9c6d71d83e2|08:26|3038489
05|The Review of the Seventh Bestowal|38668a2706e84b0ea6abcc856540f367|08:53|3198207
06|The Crisis Before the Bestowal|a6578c92e122411f8410ac32e9a1a287|04:37|1661737
07|The Mandate of the Seventh Bestowal|f6b5efb8f0534554b098305030189d68|07:47|2799945
08|Research of a World Operating Normally|72cac4e297b746819af74b156b254725|11:35|4172791
09|The Intimate Talk with the Trinity|52e037dc66c642d7bdf9a566940afaf4|09:14|3322345
10|The Trinity Inquires About Super-universe Guidance|50ce3cd32b5f436184946e3ee93a871b|08:27|3044158
11|The Trinity Inquires About Local Universe Guidance|81226245afc74f85bc517452144b7a92|08:32|3075348
12|Celestial Strategy and Divine Fundamentals|4399bb84e23047289ef728f1c9518bd6|08:29|3052300
13|The Consequences of Isolation|5ae9f0c428b04695be37b0e09876a47e|08:40|3122347
14|The Mechanics of Bestowal and the Trinity's Role in Life|0033ce31bafe4dbabf0bf46bff97d43b|10:20|3722511
15|The Trinity's Response: Acknowledging Sovereignty|d1258d127e6c4d289f2c7ef66c49ce3a|09:12|3314521
16|The Benefits of the Seventh Bestowal|fb4f1c0ac5784e038cd3ae4b9d22b609|08:39|3114043
17|The Simulations and Reality|c9cc12292b2248e2b3f9bc3dd377b12a|08:22|3010280
18|The Father's Revelation and Confirmation|493c76c990ea4a45af249eee15a87e01|08:51|3187089
19|Epilogue|66eb50a552d94edca03048a97e1afd3c|05:39|2036782
20|A Reflection of Darkness|a09097df68034f3db78315c3f0764002|08:40|3121872
21|The Judgement of Lucifer|04e6621ae5094ed4b3ff5c9548729d2e|08:25|3030809
22|The Rise of Lucifer|0006bab5293347c6ac39e19b33987ee0|05:48|2087105
23|A Conversation with Michael|950f159da6d74bfe9ec5034fee1471d8|06:06|2196200
24|The First Whisperings of Rebellion|c3620a0b5211414db9ca290e6b1c8667|07:13|2598388
25|The Declaration Unveiled|6cf26a107bce4607ac68e4a795bf5a20|09:16|3334404
26|The Seeds of Turmoil on Urantia|f48fc732567245beac8fe2c7c2363448|08:37|3105422
27|Visions Within the Reflectivity Crystal|e2c313d876e54861b7110d30d6816415|09:52|3553378
28|The Final Reckoning|28a3b81a5763430c8339565dcf58708b|07:25|2670001
29|Gabriel's Reflections on Lucifer's Imprisonment|41e543f0fa384a19a4513353d0cd4fdd|06:35|2370821
30|The Confession of Caligastia: The Fall of a Prince|a484227bfd564f48a335e304e1c12f95|04:19|1554395
31|The Introduction to the Court|7dc7bd3309524bf1ac82a5828aa410d9|05:39|2033825
32|The Role of a Planetary Prince|01eab88c231040579a1155d7ffc5ca3c|06:35|2372843
33|Caligastia's Reckoning|67be8aa1d2df4766b20f2a55bc2ea050|07:11|2585994
34|Caligastia's Contributions|4671fd4d9b424669bed406583acd0e83|10:59|6595005
35|Caligastia's Betrayal|483355d7c96347ed9e67379b50f1e8ee|05:28|1968615
36|The Intertwining Paths of Rebellion and Redemption|203dcd77a61b4854a9790f543e620184|06:30|2342300
37|The Ripple Effect and Personal Reflections|50a28482e4fd487394cc39278e33a9cc|06:27|2320349
38|A Reunion of Fallen Beings|598900a2d83a4b86b0990b90a8e083df|02:32|912855
39|Building a Bridge to Urantia|89b67ccb54f645fbb67e3e5fefbe1fae|02:57|1060188
40|Epilogue: The Light of Truth|f1246811e21c40d0823b634e789817c6|06:48|2449641
41|Journey to Jerusem|bb0fc821723f457b91db630b53ec5d29|06:43|2417657
42|Adam and Eve's Message to Humanity|ca6903e580db4f908a7798a86c3a2407|06:06|2196676
43|Adam and Eve: Origin Story|47d98d6c795a44df89c0a0c4d070bbee|07:24|2665619
44|Adam and Eve's Confession|fdae424818e945a1b5c71ac2cd413cb0|08:59|3236914
45|The Legacy of Adam and Eve|dd6bf3cf42ea4e08b4bb77048fd3f325|06:57|2503869
46|Adam and Eve's Final Messages|f120ab4785cb465daee85e3d417c2499|08:45|3148678
47|Final Message from Gabriel|50790f56632f48adb1d77b2637defec6|03:46|1355317
48|Melchizedek: Introduction|2c4c2d81a99f48aab6d0d12b111b8a19|02:15|813170
49|Introduction to Melchizedek: Origins, Mission and Relevance|eb6111564cc440e0b0e57aa31bcc1dca|08:22|3010625
50|The Nature of Personality|522d0648272e47548c2783c5e8937003|08:36|3097109
51|The Seven Adjutant Mind-Spirits|c91eed46ea734a64b7c44734fb707e51|09:34|3443029
52|The Seven Psychic Circles|f48089871b684592842ffa98a6b180ad|09:14|3326882
53|The Spirit of Truth|f65a6afc62ec4aa8ac4e4423679d7104|08:41|3127039
54|The Energy Spectrum|f0f082a72cdc459fbbc52b803a35747a|08:12|2954318
55|Personality Survival|bb7f0602eb994181b8f1d9ae8a0c5644|07:16|2617809
56|Soul Building|5c610fe385a84eabbccb2c43102aed43|08:42|3130952
57|Cosmic Context|a2d92cc646da4a1a85fd85d3f71471e1|06:56|2494140
58|Morontial Incompleteness|089db65cd4f648ef81865295233ca0cb|08:28|3045699
59|The Final Integration|d4079bf48d964bc8bb09346e8f5b06d6|06:55|2492893
60|Final Thoughts on the Lessons of Machiventa Melchizedek|c1a9e161ef1842e384dccd06e54800c2|06:32|2352806
61|Reflections on the Transmission|e0c706823c9b45599f0ad04bb9cd3871|04:12|1512684
62|The Awakening of Urantia|f756ffb445014df8b4833123be00a194|02:24|866303
63|Final Transmission from Gabriel|e0c3b585739849c6ae3ad50a3a6d0b03|02:46|998751"""

# which chapters belong to which page of the free online edition
PARTS = [
    ("read-introduction", "Introduction", "Gabriel's Introduction and Mission", (1, 3)),
    ("read-part-1", "Part 1", "The Untold Story of Jesus", (4, 19)),
    ("read-part-2", "Part 2", "A Reflection of Darkness", (20, 29)),
    ("read-part-3", "Part 3", "The Confession of Caligastia", (30, 40)),
    ("read-part-4", "Part 4", "Journey to Jerusem", (41, 47)),
    ("read-part-5", "Part 5", "The Lessons of Machiventa Melchizedek", (48, 60)),
    ("read-closing", "Closing", "The Final Transmission", (61, 63)),
]


def secs(mmss):
    m, s = mmss.split(":")
    return int(m) * 60 + int(s)


CHAPTERS = []
for line in RAW.splitlines():
    n, title, fid, dur, size = line.split("|")
    CHAPTERS.append({"n": int(n), "t": title, "u": f"{BASE}{fid}-128.mp3", "d": dur, "s": secs(dur), "b": int(size)})
TOTAL = sum(c["s"] for c in CHAPTERS)


def part_of(n):
    for f, num, title, (a, b) in PARTS:
        if a <= n <= b: return f, num, title
    return None


def hm(total):
    h, m = divmod(round(total / 60), 60)
    return f"{h} h {m} min" if h else f"{m} min"


def player(chapters, key, heading, sub="", compact=False):
    """A playlist player. Works without JavaScript too: every chapter is a plain audio link."""
    esc = lambda s: html.escape(str(s), quote=True)
    data = json.dumps([{"n": c["n"], "t": c["t"], "u": c["u"], "d": c["d"]} for c in chapters], ensure_ascii=False)
    total = hm(sum(c["s"] for c in chapters))
    items = "".join(f'<li><a class="ab-ch" href="{esc(c["u"])}" data-i="{i}"><span class="ab-n">{c["n"]}</span>'
                    f'<span class="ab-t">{esc(c["t"])}</span><span class="ab-d">{c["d"]}</span></a></li>' for i, c in enumerate(chapters))
    return f"""<section class="ab card{' ab-compact' if compact else ''}" data-key="{esc(key)}" data-tracks='{esc(data)}' aria-label="{esc(heading)}">
<div class="ab-head"><div class="stack" style="gap:2px"><span class="eyebrow muted" style="font-size:12px">{esc(heading)}</span>
<strong class="ab-now">{esc(chapters[0]["n"])}. {esc(chapters[0]["t"])}</strong>{f'<span class="muted" style="font-size:14px">{esc(sub)}</span>' if sub else ''}</div>
<span class="ab-total muted">{len(chapters)} chapter{'s' if len(chapters) != 1 else ''} · {total}</span></div>
<audio class="ab-audio" controls preload="none" src="{esc(chapters[0]["u"])}"></audio>
<div class="ab-tools"><button type="button" class="ab-prev" aria-label="Previous chapter">⏮ Previous</button><button type="button" class="ab-next" aria-label="Next chapter">Next ⏭</button>
<label class="ab-speed">Speed <select><option>0.8</option><option selected>1</option><option>1.25</option><option>1.5</option><option>1.75</option><option>2</option></select></label>
<span class="ab-resume" hidden></span></div>
<details class="ab-list"{' open' if not compact else ''}><summary>Chapters</summary><ol>{items}</ol></details>
</section>"""


def listen_box(part_file):
    for f, num, title, (a, b) in PARTS:
        if f == part_file:
            chs = [c for c in CHAPTERS if a <= c["n"] <= b]
            return player(chs, f"part:{f}", f"Listen to {num.lower() if num != 'Introduction' else 'the introduction'}",
                          "Read along, or just listen. The audiobook is free.", compact=True)
    return ""


def jsonld(site_url):
    return json.dumps({"@context": "https://schema.org", "@type": "Audiobook", "name": "The Portal Opens (Audiobook)",
                       "author": {"@type": "Person", "name": "Shareef Ali Rashada", "@id": f"{site_url}/about.html#shareef"},
                       "inLanguage": "en", "isAccessibleForFree": True,
                       "duration": f"PT{TOTAL // 3600}H{TOTAL % 3600 // 60}M", "url": f"{site_url}/audiobook.html",
                       "image": f"{site_url}/assets/audiobook-cover.jpg", "isbn": "9781326565336",
                       "hasPart": [{"@type": "AudioObject", "name": f'{c["n"]}. {c["t"]}', "contentUrl": c["u"],
                                    "encodingFormat": "audio/mpeg", "duration": f'PT{c["s"] // 60}M{c["s"] % 60}S'} for c in CHAPTERS]},
                      ensure_ascii=False)


def feed(site_url):
    from email.utils import format_datetime
    from datetime import datetime, timedelta, timezone
    esc = lambda s: html.escape(s, quote=False)
    start = datetime(2025, 9, 15, 12, tzinfo=timezone.utc)
    items = []
    for c in CHAPTERS:
        p = part_of(c["n"])
        link = f"{site_url}/{p[0]}.html" if p else f"{site_url}/audiobook.html"
        where = f"{p[1]}: {p[2]}. " if p else ""
        items.append(f"""<item>
<title>{c["n"]}. {esc(c["t"])}</title>
<description>{esc(where)}Chapter {c["n"]} of 63 of The Portal Opens by Shareef Ali Rashada, narrated with an AI voice (ElevenLabs). Read along free at {link}</description>
<enclosure url="{c["u"]}" length="{c["b"]}" type="audio/mpeg"/>
<guid isPermaLink="false">portal-opens-audiobook-{c["n"]:02d}</guid>
<pubDate>{format_datetime(start + timedelta(minutes=c["n"]))}</pubDate>
<link>{link}</link>
<itunes:duration>{c["s"]}</itunes:duration>
<itunes:episode>{c["n"]}</itunes:episode>
<itunes:episodeType>full</itunes:episodeType>
<itunes:explicit>false</itunes:explicit>
</item>""")
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd" xmlns:atom="http://www.w3.org/2005/Atom">
<channel>
<title>The Portal Opens: The Audiobook</title>
<link>{site_url}/audiobook.html</link>
<atom:link href="{site_url}/audiobook.xml" rel="self" type="application/rss+xml"/>
<language>en</language>
<copyright>© 2025 Shareef Ali Rashada, POW Productions Pty Ltd</copyright>
<description>The complete audiobook of The Portal Opens by Shareef Ali Rashada, in 63 chapters: the untold story of Jesus, Lucifer's rebellion, the confession of Caligastia, Adam and Eve's message to humanity, and the lessons of Machiventa Melchizedek. Winner of the Literary Titan Silver Book Award. Narrated with an AI voice (ElevenLabs); the text is by Shareef Ali Rashada. Read along free at {site_url}/read.html</description>
<itunes:author>Shareef Ali Rashada</itunes:author>
<itunes:owner><itunes:name>Shareef Ali Rashada</itunes:name><itunes:email>shareef@peopleoftheworld.net</itunes:email></itunes:owner>
<itunes:image href="{site_url}/assets/audiobook-cover.jpg"/>
<image><url>{site_url}/assets/audiobook-cover.jpg</url><title>The Portal Opens: The Audiobook</title><link>{site_url}/audiobook.html</link></image>
<itunes:category text="Religion &amp; Spirituality"><itunes:category text="Spirituality"/></itunes:category>
<itunes:category text="Arts"><itunes:category text="Books"/></itunes:category>
<itunes:explicit>false</itunes:explicit>
<itunes:type>serial</itunes:type>
{''.join(items)}
</channel>
</rss>
"""


def build(B):
    esc = lambda s: html.escape(str(s), quote=True)
    groups = []
    for f, num, title, (a, b) in PARTS:
        chs = [c for c in CHAPTERS if a <= c["n"] <= b]
        groups.append(f"""<a class="card" href="{f}.html"><span class="meta">{esc(num)} · chapters {a}–{b}</span>
<span class="h-md" style="font-family:var(--display)">{esc(title)}</span>
<span class="muted" style="font-size:15px">{hm(sum(c["s"] for c in chs))} · read along with the text</span><span class="card-cta">Read and listen →</span></a>""")
    body = f"""{B.reader_header()}
<main>
<section class="band"><div class="wrap section" style="display:flex;flex-wrap:wrap;align-items:center;gap:40px 56px;padding-bottom:48px">
<div class="stack" style="flex:999 1 440px;min-width:0;gap:18px">
<p class="eyebrow accent">Free audiobook</p>
<h1 class="h-xl">Listen to The Portal Opens.</h1>
<p class="lead muted" style="max-width:620px">The complete book in 63 chapters, {hm(TOTAL)} in all. Press play and it carries on from chapter to chapter, and remembers where you stopped.</p>
<p class="muted" style="font-size:14px">Narrated with an AI voice (ElevenLabs).</p>
<div class="actions"><a class="btn btn-door" href="#player">Start listening</a><a class="btn btn-ghost" href="read.html">Read along</a></div>
</div>
<img class="ab-cover" src="assets/cover-portal.webp" alt="Cover of The Portal Opens" width="200" height="300" style="flex:0 0 auto;width:200px;height:auto;border-radius:10px;box-shadow:0 18px 50px rgba(0,0,0,.35)">
</div></section>
<section id="player" class="section"><div class="wrap stack" style="gap:28px">
{player(CHAPTERS, "audiobook", "The Portal Opens · complete audiobook")}
<p class="muted" style="font-size:14.5px">Prefer a podcast app? Add the audiobook feed to any podcast player: <code>{B.SITE_URL}/audiobook.xml</code></p>
</div></section>
<section class="section band-alt"><div class="wrap stack" style="gap:28px">
<div class="stack intro"><h2 class="h-lg">Read and listen, part by part</h2>
<p class="lead muted">Every part of the free online edition has its chapters ready to play at the top of the page.</p></div>
<div class="grid">{''.join(groups)}</div>
</div></section>
<section id="buy" class="section"><div class="wrap" style="display:flex;flex-wrap:wrap;gap:20px 48px;align-items:center">
<div class="stack" style="flex:2 1 420px;min-width:0"><h2 class="h-lg">Keep a copy on your shelf</h2>
<p class="lead muted">The paperback, hardcover and Kindle editions support the work of People of the World.</p></div>
<p style="flex:1 1 200px"><a class="btn btn-door" href="seekers.html#buy">Buy the book</a></p>
</div></section>
</main>
{B.footer("seekers")}
<script src="assets/audiobook.js?v={B.asset_v('audiobook.js')}" defer></script>"""
    B.page("audiobook.html", "The Portal Opens audiobook (free)",
           f"Listen free to the complete audiobook of The Portal Opens by Shareef Ali Rashada: 63 chapters, {hm(TOTAL)}.",
           body, "seekers", extra_head=f'<script type="application/ld+json">{jsonld(B.SITE_URL)}</script>')
    (B.OUT / "audiobook.xml").write_text(feed(B.SITE_URL), encoding="utf-8")
