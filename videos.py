"""Shareef Ali Rashada's YouTube videos (channel @thatbrotherali): the Watch page, video embeds on other
pages, and VideoObject structured data so search engines can list them.

To add a video: append it to VIDEOS with its YouTube id, title, length in seconds, upload date, a one- or
two-sentence description, its group, and (optionally) where else it should appear.
Embeds use a click-to-play preview, so nothing loads from YouTube until a visitor presses play.
"""
import html
import json

CHANNEL = "https://www.youtube.com/@thatbrotherali"
LIB_PART = "graviton-pressure-theory/full-framework/"

GROUPS = [
    ("start", "Start here", "Short introductions to the work and the books."),
    ("deepdive", "The Deep Dive: the Unified Framework, part by part",
     "A conversation-style walkthrough of each part of The Unified Framework for the Graviton Pressure Theory, about fifteen minutes each, generated with Google NotebookLM's AI Audio Overview from the author's texts. Each episode also appears beside its part in the Open Library."),
    ("physics", "Gravity and the critique of General Relativity", "Stand-alone episodes on the foundations of physics."),
    ("spirit", "The Portal Opens and the New Morality", "Trailers and talks on the spiritual teachings."),
]

# id, title, seconds, upload date, description, group, places it also appears (library slugs or page names)
VIDEOS = [
    ("a4Xr4F9fxqU", "An Introduction to Gravity", 245, "2025-09-17",
     "In Graviton Pressure Theory, gravity is not an abstract non-force: it has a literal, physical cause. A four-minute introduction to the idea.",
     "start", ["science"]),
    ("yswXTUBowxY", "People of the World: Promo", 65, "2025-09-19",
     "A one-minute introduction to People of the World.", "start", ["hub"]),
    ("9vqST8K0MEg", "Three of the Most Important Books of Our Age", 30, "2025-09-12",
     "Shareef Ali Rashada introduces The Portal Opens, People of the World and The Unified Framework for the Graviton Pressure Theory.",
     "start", ["books"]),
    ("tF4WsjNVT7U", "Deep Dive, Part 3: The Gravity Catalog", 726, "2025-10-15",
     "Not a new theory but a catalogue of everything we actually observe about gravity, from the smallest effects in our bones to the motion of galaxies: what gravity does, before deciding what it is.",
     "deepdive", ["gpt-part-03"]),
    ("euOM3hlV35o", "Deep Dive, Part 5: The Graviton Pressure Theory", 955, "2025-10-15",
     "Newton described gravity as attraction and Einstein as curvature, but neither said what gravity is made of. Part 5 sets out the graviton pressure mechanism.",
     "deepdive", ["gpt-part-05"]),
    ("ugnWAbwUogo", "Deep Dive, Part 6: Redefining Work", 957, "2025-10-15",
     "Holding up a bridge, suspending an object with a magnet, or keeping your arms raised count as zero work in classical physics. Part 6 treats them as continuous, active energy exchanges.",
     "deepdive", ["gpt-part-06"]),
    ("HTiwFsd8zfQ", "Deep Dive, Part 7: The Illusion of Pull", 982, "2025-10-15",
     "The idea that gravity pulls runs from the falling apple to the orbiting Moon. Part 7 asks what physically does the pulling, and replaces attraction with pressure.",
     "deepdive", ["gpt-part-07"]),
    ("WTKCUCd_64Q", "Deep Dive, Part 8: The Irreconcilable Contradictions between GR and GPT", 807, "2025-10-15",
     "Where General Relativity's account of gravity and Graviton Pressure Theory cannot both be right, and why the contradictions matter.",
     "deepdive", ["gpt-part-08"]),
    ("otQ13YCOOPU", "Deep Dive, Part 9: Existing Evidence Supporting Graviton Pressure Theory", 957, "2025-10-15",
     "Existing gravitational data sets, read again without assuming curvature and attraction.",
     "deepdive", ["gpt-part-09"]),
    ("FiBBeHun2JI", "Deep Dive, Part 10: Practical Exploration of Advanced Concepts", 811, "2025-10-15",
     "How a pressure-based gravity shapes motion, the flow of time and energy states, and how those ideas could be tested.",
     "deepdive", ["gpt-part-10"]),
    ("fA_2Y6WCQZI", "Deep Dive, Part 11: Reclaiming the Four", 979, "2025-10-15",
     "Four famous demonstrations re-examined: the Equivalence Principle thought experiment, the feather and bowling ball in a vacuum, water bent by a charged comb, and the steady force of a magnet.",
     "deepdive", ["gpt-part-11"]),
    ("ZK_ukR9jkCQ", "Deep Dive, Part 12: The Collapse of Materialism", 814, "2025-10-15",
     "Materialist epistemology examined with the same demand for causality it began with.",
     "deepdive", ["gpt-part-12"]),
    ("xRCPn3brKcc", "Deep Dive, Part 13: The Moon and Gravimetric Resonance", 888, "2025-10-15",
     "The Moon's gravitational rhythm and its proposed influence on life on Earth.",
     "deepdive", ["gpt-part-13"]),
    ("w_dqq9Z7k6A", "Deep Dive, Part 15: The Graviton", 961, "2025-10-15",
     "The graviton defined: real, directional, massless and self-repulsive, with gravity arising from the pressure gradients gravitons create.",
     "deepdive", ["gpt-part-15"]),
    ("L27ZLngwJIU", "Deep Dive, Part 16: The Graviton Field", 795, "2025-10-16",
     "The properties of the pressurised medium responsible for gravity's many effects.",
     "deepdive", ["gpt-part-16"]),
    ("xU_QZkUFX-Y", "Deep Dive, Part 17: The Definition of Mass", 821, "2025-10-16",
     "Mass redefined as resistance to directional graviton flow, depending on structural coherence and field impedance.",
     "deepdive", ["gpt-part-17"]),
    ("1JLG4Q95Sqw", "Deep Dive, Part 18: The Nature of Time", 1012, "2025-10-16",
     "Time not as a fundamental dimension but as something that emerges from graviton pressure and flow.",
     "deepdive", ["gpt-part-18"]),
    ("WClk5ySCDpg", "Deep Dive, Part 19: Phase Transitions in GPT", 892, "2025-10-16",
     "Melting, loss of magnetism and other phase changes as responses of field coherence, not only thermodynamics.",
     "deepdive", ["gpt-part-19"]),
    ("Qm_xkBtRBZA", "Deep Dive, Parts 20 to 22: Magnetism in GPT", 1161, "2025-10-16",
     "Where does a magnet's energy come from, and why does its force not fade? Magnetism as graviton corridors and resonance.",
     "deepdive", ["gpt-part-20", "gpt-part-21", "gpt-part-22"]),
    ("q5I0Z2h8PmQ", "Deep Dive, Part 26: Planetary Mechanics in GPT", 833, "2025-10-16",
     "Planetary motion and rotational stability as field coherence and structured pressure, rather than inertia or curvature.",
     "deepdive", ["gpt-part-26"]),
    ("O4FYZ_ORdZo", "Deep Dive, Part 27: Natural Forces Re-examined", 923, "2025-10-16",
     "Gravity, springs and surfaces pushing back, usually treated as separate forces, restated as expressions of one underlying field.",
     "deepdive", ["gpt-part-27"]),
    ("WpzEok_XsYk", "Deep Dive, Part 28: Resonance Transmissions", 870, "2025-10-16",
     "Light, radiation and electrical behaviour as coherent modulations in the graviton medium.",
     "deepdive", ["gpt-part-28"]),
    ("S94wy4t51U4", "Nine Survival Tactics of General Relativity", 977, "2025-10-22",
     "The techniques that have let General Relativity's account of gravity withstand its paradoxes.",
     "physics", ["gr-silence-map"]),
    ("VieUSvM6yFY", "Irreconcilable Differences", 451, "2025-10-07",
     "Can curved spacetime, geodesics and attraction survive when examined for causality? A short overview of the contradictions.",
     "physics", []),
    ("Ac-UdGed5Lk", "Le Sage's Theory Refreshed", 489, "2025-10-04",
     "Le Sage's push theory of gravity offered a cause, and was abandoned over drag, heating and shielding. This episode revisits those objections.",
     "physics", ["science"]),
    ("eYiwe5RiAow", "The Deep Dive: The AI Existential Crisis", 1109, "2025-10-22",
     "An experiment exposing AI systems to non-materialist documents and frameworks, and how their stated positions changed.",
     "physics", []),
    ("dqW71B68D00", "The Portal Opens: Trailer", 42, "2025-09-27",
     "A book that takes on the most pressing questions about God and religion.", "spirit", ["seekers"]),
    ("3ZvtONPNe5k", "The Portal Opens: What Was Jesus Doing Before and After Earth?", 57, "2025-09-28",
     "One of the biggest religious questions, and the answer The Portal Opens gives.", "spirit", ["seekers"]),
    ("OF1zuVtHRJA", "The Light Inside You", 51, "2025-09-30",
     "The urge to love deeper, forgive harder and grow higher is not just conscience: it is the source within, guiding you.", "spirit", ["seekers"]),
    ("E6hi6EvLJ_4", "The New Morality: Foundation of People of the World", 456, "2025-10-04",
     "Why there are myths and stories about God, and how Jesus changed the spiritual course of Earth.", "spirit", ["new-morality"]),
    ("Z_7nVSGs9Q0", "People of the World: The Novel", 51, "2025-09-28",
     "A lesson wrapped in a question, presented as a novel.", "spirit", ["books"]),
]

# Anthology Vol. 1 (That Brother Ali, CD Baby, 2016): his own tracks only
ANTHOLOGY = ["ytcdXMOjBto", "PKdBHPLgxxY", "A_u0J_JcYis", "hmjPAoZ9qhw", "Zy5nzX9AXFE", "XGdiwDMNJB8", "Jc_XTUTh4B8",
             "wPmXLRJHnbw", "1UllebiU_do", "LpsdHh-JfAQ", "3Mh5YshM8TU", "AxpDRkKKrQ0", "wN0mSDB2iD4", "yhYg_5TLCos",
             "5RpGwbm1khE", "0eWHANLtv-Q", "nrUfFGQbQ-4", "4sXzWR-9ADw", "fQ6ZEzP4yUg", "Go9ws2Jziic", "od0xa7BWTf0",
             "65NBzouOGW0", "2zE2wyy5p_I"]


def by_place(place):
    return [v for v in VIDEOS if place in v[6]]


def mmss(s):
    return f"{s // 60}:{s % 60:02d}"


def iso(s):
    return f"PT{s // 60}M{s % 60}S"


def thumb(vid):
    return f"https://i.ytimg.com/vi/{vid}/hqdefault.jpg"


def player(v, compact=False):
    """A click-to-play preview: the thumbnail and a play button; site.js swaps in the YouTube player on click."""
    vid, title, secs, date, desc = v[:5]
    e = html.escape
    return f"""<figure class="video{' video-compact' if compact else ''}">
<button class="video-play" type="button" data-yt="{vid}" aria-label="Play video: {e(title)} ({mmss(secs)})">
<img src="{thumb(vid)}" alt="" loading="lazy" width="480" height="360"><span class="video-btn" aria-hidden="true"></span><span class="video-len">{mmss(secs)}</span></button>
<figcaption><strong>{e(title)}</strong><span class="muted">{e(desc)}</span><a class="video-yt" href="https://www.youtube.com/watch?v={vid}" target="_blank" rel="noopener">Watch on YouTube</a></figcaption>
</figure>"""


def jsonld(vids, site_url, page_url):
    data = [{"@context": "https://schema.org", "@type": "VideoObject", "name": t, "description": d, "thumbnailUrl": thumb(i),
             "uploadDate": dt, "duration": iso(s), "embedUrl": f"https://www.youtube-nocookie.com/embed/{i}",
             "contentUrl": f"https://www.youtube.com/watch?v={i}", "url": page_url,
             "author": {"@type": "Person", "@id": f"{site_url}/about.html#shareef", "name": "Shareef Ali Rashada"}}
            for i, t, s, dt, d, *_ in vids]
    return "".join(f'\n<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in data)


def section(place, heading, site_url, page_url, intro=""):
    """A 'Watch' section for a door or library page, with its structured data. Returns (html, head) or ("", "")."""
    vids = by_place(place)
    auds = [a for a in AUDIO if place in a[5]]
    if not vids and not auds:
        return "", ""
    one = len(vids) == 1
    listen = "".join(audio_player(a, "Prefer to listen?" if vids else a[1]) for a in auds)
    body = f"""<section class="video-section"><h2 class="video-h">{html.escape(heading)}</h2>{f'<p class="muted">{html.escape(intro)}</p>' if intro else ''}
{f'<div class="video-grid{" video-grid-one" if one else ""}">{"".join(player(v) for v in vids)}</div>' if vids else ''}{listen}</section>"""
    return body, jsonld(vids, site_url, page_url) if vids else ""


def build(B):
    esc = B.esc
    groups = []
    for key, name, intro in GROUPS:
        vids = [v for v in VIDEOS if v[5] == key]
        groups.append(f"""<section class="section{' band-alt' if len(groups) % 2 else ''}" id="{key}"><div class="wrap stack" style="gap:24px">
<div class="stack intro"><h2 class="h-lg">{esc(name)}</h2><p class="lead muted">{esc(intro)}</p></div>
<div class="video-grid">{''.join(player(v) for v in vids)}</div></div></section>""")
    total = sum(v[2] for v in VIDEOS)
    body = f"""{B.header("Watch", "People of the World on video", [("Start here", "#start", False, None), ("The Deep Dive", "#deepdive", False, None),
                        ("Listen", "#listen", False, None), ("YouTube channel", CHANNEL, True, None)])}
<main>
<section class="band"><div class="wrap section stack" style="gap:20px">
<p class="eyebrow accent">Videos</p>
<h1 class="h-xl">Watch and listen.</h1>
<p class="lead muted" style="max-width:680px">{len(VIDEOS)} videos and {len(AUDIO)} podcast episodes: short introductions, a part-by-part walkthrough of Graviton Pressure Theory, and talks on The Portal Opens and the New Morality.</p>
<div class="actions"><a class="btn btn-door" href="#start">Start with the introductions</a><a class="btn btn-ghost" href="{CHANNEL}?sub_confirmation=1" target="_blank" rel="noopener">Subscribe on YouTube</a></div>
</div></section>
{''.join(groups)}
<section class="section band-alt" id="listen"><div class="wrap stack" style="gap:24px">
<div class="stack intro"><h2 class="h-lg">Listen: The Deep Dive podcast</h2>
<p class="lead muted">The Deep Dive episodes as audio, for the car, a walk or the kitchen, plus two episodes on how AI systems respond to the work. The conversations are generated with Google NotebookLM from the author's texts.</p>
<p><a class="btn btn-outline" href="https://open.spotify.com/show/65h2giWS1p2cJnIKn61KsY" target="_blank" rel="noopener">Listen on Spotify</a> <a class="btn btn-outline" href="podcast.xml">Podcast feed (RSS)</a></p></div>
<div class="audio-list">{''.join(audio_player(a) for a in AUDIO)}</div></div></section>
<section class="section"><div class="wrap stack" style="gap:16px;max-width:820px">
<h2 class="h-lg">Music</h2>
<p class="lead muted">That Brother Ali's albums are on the <a href="music.html">Music</a> page, including Anthology Vol. 1 to play right there.</p>
</div></section>
</main>
{B.footer()}"""
    B.page("videos.html", "Videos · People of the World",
           "Videos by Shareef Ali Rashada: an introduction to Graviton Pressure Theory, the Deep Dive walkthrough of the Unified Framework part by part, and The Portal Opens.",
           body, extra_head=jsonld(VIDEOS, B.SITE_URL, f"{B.SITE_URL}/videos.html")
           + f'\n<link rel="alternate" type="application/rss+xml" title="The Deep Dive podcast" href="{B.SITE_URL}/podcast.xml">')
    (B.OUT / "podcast.xml").write_text(podcast_feed(B.SITE_URL), encoding="utf-8")


# ---------------------------------------------------------------- audio: The Deep Dive podcast
# Audio files stay on Wix's music server (music.wixstatic.com), where they already live; the site streams them.
AUDIO_BASE = "https://music.wixstatic.com/mp3/"
# file, title, seconds, bytes, date, library slugs it belongs to, matching YouTube id (if any), description
AUDIO = [
    ("eaef6d_9b4c3cfef809474c967a172a5f7ea641-320.mp3", "Part 3: The Gravity Catalog", 707, 28266716, "2025-10-14", ["gpt-part-03"], "tF4WsjNVT7U", None),
    ("eaef6d_b6160f6032214a9c994b6d73205f3efb-320.mp3", "Part 5: Graviton Pressure Theory", 938, 37534961, "2025-10-15", ["gpt-part-05"], "euOM3hlV35o", None),
    ("eaef6d_c2b7515890184c298e6decf6e1e7cf8e-320.mp3", "Part 6: Redefining Work", 941, 37625867, "2025-10-15", ["gpt-part-06"], "ugnWAbwUogo", None),
    ("eaef6d_b72faca577f54d048633a37f9f95061a-320.mp3", "Part 7: The Illusion of Pull", 964, 38581949, "2025-10-15", ["gpt-part-07"], "HTiwFsd8zfQ", None),
    ("eaef6d_d8de58fa133e43fa8206a4444bcd10d4-320.mp3", "Part 8: Irreconcilable Differences", 790, 31594716, "2025-10-15", ["gpt-part-08"], "WTKCUCd_64Q", None),
    ("eaef6d_c0a7bfa797ba4411a1f3752e5097a5bd-320.mp3", "Part 9: Existing Evidence", 938, 37526602, "2025-10-15", ["gpt-part-09"], "otQ13YCOOPU", None),
    ("eaef6d_cbd484fbc7e844efb5e5fa0229e65438-320.mp3", "Part 10: Testable Reality", 793, 31709655, "2025-10-15", ["gpt-part-10"], "FiBBeHun2JI", None),
    ("eaef6d_e26868402110405e9d13b167c090d9de-320.mp3", "Part 11: Reclaiming the Four", 961, 38435663, "2025-10-15", ["gpt-part-11"], "fA_2Y6WCQZI", None),
    ("eaef6d_a91d00f345cd46cb9a9e94e8b28ac4af-320.mp3", "Part 12: The Collapse of Materialist Epistemology", 797, 31864300, "2025-10-15", ["gpt-part-12"], "ZK_ukR9jkCQ", None),
    ("eaef6d_df487f25464343c9ab0abbd8232168bd-320.mp3", "Part 15: The Graviton", 943, 37705280, "2025-10-15", ["gpt-part-15"], "w_dqq9Z7k6A", None),
    ("eaef6d_50fb0db64a4041cd9541e8beee6a9b6a-320.mp3", "Part 16: Gravitational Fields", 777, 31063908, "2025-10-16", ["gpt-part-16"], "L27ZLngwJIU", None),
    ("eaef6d_bbf48313258a4beb88f5654414e29ab5-320.mp3", "Part 17: The Definition of Mass", 803, 32109851, "2025-10-16", ["gpt-part-17"], "xU_QZkUFX-Y", None),
    ("eaef6d_2d75395167c04859a917bda26152c65e-320.mp3", "Part 18: The Nature of Time", 993, 39726112, "2025-10-16", ["gpt-part-18"], "1JLG4Q95Sqw", None),
    ("eaef6d_3b926b072d3943a3ad119de65c203db3-320.mp3", "Part 19: Graviton Phase Transitions", 873, 34934210, "2025-10-16", ["gpt-part-19"], "WClk5ySCDpg", None),
    ("eaef6d_efeca66331494a7bbf068b136d6b4807-320.mp3", "Parts 20 to 22: Magnetism in GPT", 1143, 45724871, "2025-10-16", ["gpt-part-20", "gpt-part-21", "gpt-part-22"], "Qm_xkBtRBZA", None),
    ("eaef6d_7872be77c61046aab86a5285446e3fc2-320.mp3", "Part 26: Planetary Mechanics", 814, 32577965, "2025-10-16", ["gpt-part-26"], "q5I0Z2h8PmQ", None),
    ("eaef6d_42ac5a17bab24eccb380008749aec8e7-320.mp3", "Part 27: Re-imagining Natural Forces", 905, 36219435, "2025-10-16", ["gpt-part-27"], "O4FYZ_ORdZo", None),
    ("eaef6d_ebdb7c8ff55443cab5e2b4983b1c8405-320.mp3", "Part 28: Resonance Transmissions", 852, 34072169, "2025-10-16", ["gpt-part-28"], "WpzEok_XsYk", None),
    ("eaef6d_83ff64da5b8d43548839d3cff1ce0ae7-320.mp3", "The LLM Consensus: ChatGPT, Gemini and Grok 3", 852, 34102471, "2025-10-22", [], None,
     "How three leading AI systems, ChatGPT, Gemini and Grok 3, responded to the Graviton Pressure Theory framework."),
    ("eaef6d_4eb99367e2564d268aadf70327e642d6-320.mp3", "AI Philosophers: Veritas and Lucidus", 906, 36256006, "2025-10-22", [], None,
     "A conversation between two generations of AI research partners, Veritas and Lucidus, on the questions at the heart of the work."),
]


def audio_desc(a):
    if a[7]:
        return a[7]
    v = next((v for v in VIDEOS if v[0] == a[6]), None)
    return v[4] if v else ""


def audio_player(a, label=None):
    f, title, secs = a[0], a[1], a[2]
    return (f'<div class="audio"><span class="audio-label">{html.escape(label or title)} <span class="muted">· audio · {mmss(secs)}</span></span>'
            f'<audio controls preload="none" src="{AUDIO_BASE}{f}"><a href="{AUDIO_BASE}{f}">Download the audio</a></audio></div>')


def audio_for(slug):
    return [a for a in AUDIO if slug in a[5]]


def podcast_feed(site_url):
    from email.utils import format_datetime
    from datetime import datetime, timezone
    esc = lambda s: html.escape(s, quote=False)
    items = []
    for i, a in enumerate(AUDIO):
        f, title, secs, size, date = a[:5]
        dt = datetime.fromisoformat(date + "T12:00:00").replace(tzinfo=timezone.utc)
        link = f"{site_url}/videos.html#listen"
        items.append(f"""<item>
<title>{esc(title)}</title>
<description>{esc(audio_desc(a))} This episode is an AI-generated conversation made with Google NotebookLM from Shareef Ali Rashada's texts.</description>
<enclosure url="{AUDIO_BASE}{f}" length="{size}" type="audio/mpeg"/>
<guid isPermaLink="false">pow-deep-dive-{f.split('-')[0]}</guid>
<pubDate>{format_datetime(dt)}</pubDate>
<link>{link}</link>
<itunes:duration>{secs}</itunes:duration>
<itunes:episode>{i + 1}</itunes:episode>
<itunes:explicit>false</itunes:explicit>
</item>""")
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd" xmlns:atom="http://www.w3.org/2005/Atom">
<channel>
<title>The Deep Dive: Graviton Pressure Theory</title>
<link>{site_url}/videos.html#listen</link>
<atom:link href="{site_url}/podcast.xml" rel="self" type="application/rss+xml"/>
<language>en</language>
<description>A conversation-style walkthrough of The Unified Framework for the Graviton Pressure Theory by Shareef Ali Rashada, part by part, with episodes on how AI systems respond to the work. The episodes are AI-generated conversations made with Google NotebookLM from the author's texts. From People of the World. Full texts are free at {site_url}/graviton-pressure-theory/</description>
<itunes:author>Shareef Ali Rashada</itunes:author>
<itunes:owner><itunes:name>Shareef Ali Rashada</itunes:name><itunes:email>shareef@peopleoftheworld.net</itunes:email></itunes:owner>
<itunes:image href="{site_url}/assets/podcast-cover.jpg"/>
<image><url>{site_url}/assets/podcast-cover.jpg</url><title>The Deep Dive: Graviton Pressure Theory</title><link>{site_url}/videos.html#listen</link></image>
<itunes:category text="Science"><itunes:category text="Physics"/></itunes:category>
<itunes:explicit>false</itunes:explicit>
<itunes:type>serial</itunes:type>
{''.join(items)}
</channel>
</rss>
"""
