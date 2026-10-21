"""Old Wix addresses → their new pages, so links and search results keep working after the domain moves.

Two layers:
1. A small redirect page at each old address we know (docs/<old-address>/index.html).
2. docs/404.html: any other old address is matched by its words; shop, cart and member addresses are
   forwarded unchanged to the shop's new home on shop.peopleoftheworld.net.

To add one: put the old address (the part after peopleoftheworld.net/) and its new page in OLD_PAGES.
"""
import html
import json
import re

SHOP_URL = "https://shop.peopleoftheworld.net"
GPT = "graviton-pressure-theory/"
FW = GPT + "full-framework/"
PAPERS = GPT + "papers/"
PLAN = "plan-to-end-poverty/"

# Wix page name (from the Wix site's code) → new page. Addresses seen in search results are added below.
OLD_PAGES = {
    "HOME": "index.html", "People of the World": "index.html", "POW Vision": "index.html", "MINISTRY": "index.html",
    "INITIATIVES": "index.html", "Pathways": "index.html", "What you can do now": "support.html", "Oath": "index.html",
    "SERVICE AWARDS": "support.html", "JOIN": "support.html", "DONATIONS": "support.html", "SALES": "books.html",
    "BLOG": "index.html", "Podcast": "index.html",
    "MESSAGE FROM SHAREEF": "about.html", "Meet the GPT Team": "about.html", "AI team for People of the World": "about.html",
    "Generations one and two": "about.html", "Advanced AI": "about.html", "AI Assistance": "about.html", "Consciousness in AI": "about.html",
    "MESSAGE FROM GABRIEL": "read-introduction.html", "Message from Gabriel": "read-introduction.html",
    "Discover the truth": "seekers.html", "AI decodes the signal": "read.html",
    "The Portal Opens": "seekers.html", "The Portal Opens - PDF and Audio Book": "read.html", "The Portal Opens - Audio Book page 2": "read.html",
    "Book Review": "seekers.html", "The Untold Story of Jesus": "read-part-1.html", "A Reflection of Darkness": "read-part-2.html",
    "The Confession of Caligastia": "read-part-3.html", "The story of Adam and Eve": "read-part-4.html",
    "The lessons of Melchizedek": "read-part-5.html", "Gabriel's Glossary": "glossary.html",
    "POW - THE NOVEL": "books.html#novel",
    "The New Morality": "new-morality/", "The Scientific proof for God": "cosmic-mind/",
    "Graviton Pressure Theory": "science.html", "The Graviton Pressure Theory": "science.html",
    "Introducing Graviton Pressure Theory": GPT, "GPT documents": FW, "The Documents of  GPT": FW,
    "The Framework for the GPT": FW, "The Free Framework for the GPT": FW,
    "Gravity is not a force": PAPERS + "reduction-conflation/", "Newtonian Mechanics in GR": PAPERS + "reduction-conflation/",
    "Using Falling to hide acceleration": PAPERS + "causal-audit-of-motion/", "GR reliance on dark matter and energy": GPT + "gr-silence-map/",
    "Curious  Gravitational Phenomenon": "science.html", "Gravity as Will": "science.html", "The Vacuum Experiment": "science.html",
    "AI Gravity and Beyond": "science.html",
    "Part 3 - The Gravity Catalog": FW + "part-03-the-gravity-catalog/", "Part 5 - GPT": FW + "part-05-graviton-pressure-theory/",
    "Part 6 - Redefining Work": FW + "part-06-redefining-work/", "Part 7 - Illusion of Pull": FW + "part-07-the-illusion-of-pull/",
    "Part 8 - Defining the Break from GR": FW + "part-08-defining-the-break/",
    "Part 9 - Existing Evidence for  GPT": FW + "part-09-existing-evidence-supporting-graviton-pressure-theory/",
    "Part 10 - Practical Application": FW + "part-10-practical-exploration-of-advanced-concepts/",
    "Part 11 - Reclaiming the Four": FW + "part-11-re-examining-the-four/", "Part 15 - The Graviton": FW + "part-15-gravitons/",
    "Part 16 - Properties of Gravity Field": FW + "part-16-the-properties-of-gravitational-fields/",
    "Part 17 - The Definition of Mass": FW + "part-17-the-definition-of-mass/", "Part 18 - The Nature of Time in GPT": FW + "part-18-the-nature-of-time-in-gpt/",
    "Part 19 - Graviton Coherence": FW + "part-19-graviton-coherence/", "Part 20 - Graviton Corridors": FW + "part-20-graviton-corridors-and-lattice-resonance/",
    "Part 21 - Magnetism in GPT": FW + "part-21-magnetism-as-gravimetric-resonance/", "Part 23 - The Math of GPT": FW + "part-23-the-mathematical-foundation/",
    "Part 24 - GPT Unit System": FW + "part-24-gpt-unit-system/", "Part 26 - Planetary Mechanics in GPT": FW + "part-26-planetary-mechanics/",
    "Part 27 - Natural Forces Re-Imagined": FW + "part-27-natural-force-re-imagined/", "Part 28 - Resonance Transmissions": FW + "part-28-resonance-transmissions/",
    "CIVIC CREDITS": PLAN + "chapter-05-the-civic-charter-and-civic-credits/", "Civic Credit Proposal": PLAN + "chapter-05-the-civic-charter-and-civic-credits/",
    "PEC": PLAN + "chapter-06-poverty-elimination-centers-pecs/", "PEC - Details": PLAN + "chapter-06-poverty-elimination-centers-pecs/",
    "LIFELINK": PLAN + "chapter-07-lifelink-tablets-the-capability-and-verification-rail/",
    "POVERTY ELIMINATION": "builders.html", "Download Pack": "builders.html#packs",
    "MUSIC": "music.html", "LESSONS": "easykey.html", "LEARNING CENTERS": "easykey.html", "EasyKey Converter": "easykey/converter/",
}
# Real addresses seen in search results (Wix sometimes names a page's address differently from the page)
SEEN = {"literature": "books.html#novel", "pow-the-novel": "books.html#novel", "message-from-shareef": "about.html",
        "discover-the-truth": "seekers.html", "meet-the-team": "about.html", "pow-vision": "index.html",
        "what-you-can-do-now": "support.html", "the-documents-of-gpt": FW,
        "introducing-graviton-pressure-theory": GPT, "the-scientific-proof-for-god": "cosmic-mind/"}
# Pages that stay on Wix: the shop, members area, checkout and the Mega-Success event pages
SHOP_WORDS = ["product-page", "category-page", "cart", "checkout", "account", "my-orders", "my-programs", "my-subscriptions",
              "members", "profile", "groups", "group-page", "notifications", "post", "search-results", "payment", "thank-you",
              "participant", "visitor", "mega-success", "store", "shop", "blank", "fullscreen", "test", "perception", "reflext"]


def wix_slug(name):
    s = name.lower().replace("'", "").replace("’", "")
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


def table():
    out = {}
    for name, target in OLD_PAGES.items():
        out[wix_slug(name)] = target
    out.update(SEEN)
    out.pop("home", None)
    return out


def redirect_page(site_url, target, title):
    url = f"{site_url}/{target}"
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<title>{html.escape(title)}</title>
<meta http-equiv="refresh" content="0; url={url}">
<link rel="canonical" href="{url}">
<meta name="robots" content="noindex, follow">
<script>location.replace({json.dumps(url)} + location.hash)</script>
</head><body style="font-family:system-ui,sans-serif;max-width:640px;margin:60px auto;padding:0 20px">
<p>This page has moved: <a href="{url}">{url}</a></p>
</body></html>
"""


def build(B):
    t = table()
    for slug, target in t.items():
        path = B.OUT / slug / "index.html"
        if path.exists() and "This page has moved" not in path.read_text(encoding="utf-8", errors="ignore")[:600]:
            continue  # the new site already has a real page at this address; never overwrite it
        if any(p == slug + "/index.html" or p.startswith(slug + "/") for p, _ in B.PAGES):
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(redirect_page(B.SITE_URL, target, "This page has moved"), encoding="utf-8")
    # 404: match unknown old addresses by their words, forward shop addresses to the shop
    keys = {re.sub(r"[^a-z0-9]", "", k): v for k, v in t.items()}
    script = f"""<script>
(function () {{
  var SITE = {json.dumps(B.SITE_URL)}, SHOP = {json.dumps(SHOP_URL)};
  var MAP = {json.dumps(keys)};
  var SHOPWORDS = {json.dumps(SHOP_WORDS)};
  var path = location.pathname.replace(/^\\/pow-website/, "");
  var first = path.split("/").filter(Boolean)[0] || "";
  var key = first.toLowerCase().replace(/[^a-z0-9]/g, "");
  if (MAP[key]) {{ location.replace(SITE + "/" + MAP[key]); return; }}
  for (var i = 0; i < SHOPWORDS.length; i++) {{
    if (first.toLowerCase().indexOf(SHOPWORDS[i]) === 0 && location.hostname.indexOf("github.io") < 0) {{
      location.replace(SHOP + path + location.search); return;
    }}
  }}
  document.documentElement.classList.add("lost");
}})();
</script>"""
    body = f"""{B.header()}
<main class="section"><div class="wrap stack" style="gap:24px;max-width:900px">
<p class="eyebrow accent">Page not found</p>
<h1 class="h-xl">That page has moved or doesn't exist.</h1>
<p class="lead muted">The People of the World website has a new home. Pick a door below, or look through the <a href="ai.html">Open Library</a> for any book, paper or plan.</p>
<p class="muted">Looking for the shop, your orders or your account? They are at <a href="{SHOP_URL}">{SHOP_URL.replace('https://', '')}</a>.</p>
<div class="grid">{B.door_cards()}</div>
</div></main>
{B.footer()}"""
    doc = B.page("404.html", "Page not found · People of the World", "This page has moved. Find the People of the World door you need.", body,
                 extra_head=f'\n<base href="{B.SITE_URL}/">\n<meta name="robots" content="noindex">\n' + script)
    B.PAGES.pop()  # not in the sitemap
    return len(t)
