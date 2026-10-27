"""End Poverty by Design: the plain-language hub (builders.html) and one page per instrument
(Civic Credits, Poverty Elimination Centers, LifeLink), each with its library of working papers.

Every figure on these pages comes from the author's documents (the 2025 edition of the Plan and the
working papers in src/library). Targets and modelled results are labelled as such.
"""
import json
import shutil

import library_pages as LP

B = None
esc = None
PLAN = LP.PLAN_URL


def cat():
    return json.loads((B.SRC / "library" / "catalog.json").read_text(encoding="utf-8"))


def stats():
    c = cat()
    plan_words = sum(d["words"] for d in c["plan"])
    work = c.get("working", [])
    return {"docs": len(c["plan"]) + len(work), "papers": len(work), "chapters": len(c["plan"]),
            "plan_words": plan_words, "words": plan_words + sum(d["words"] for d in work),
            "by_prog": {k: [d for d in work if d["programme"] == k] for k in LP.PROGRAMMES}}


def doc_library(prog, intro=""):
    """Grouped list of a programme's working papers, linking to their library pages."""
    docs = stats()["by_prog"][prog]
    groups = []
    for d in docs:
        if d["group"] not in groups:
            groups.append(d["group"])
    out = []
    for g in groups:
        items = "".join(
            f"""<li><a href="{LP.working_url(d)}"><span class="li-title">{esc(d['title'])}</span>
<span class="li-sub muted">{esc(d['subtitle'] or LP.sentences(d['lead'], 150))}</span></a>
<span class="li-meta">{LP.minutes(d['words'])} min · {d['date'][:4]}{' · PDF' if d.get('pdf') else ''}</span></li>"""
            for d in docs if d["group"] == g)
        out.append(f'<h3 class="h-md" style="margin-top:12px">{esc(g)}</h3><ol class="doclist">{items}</ol>')
    words = sum(d["words"] for d in docs)
    return f"""<section id="papers" class="section band-alt"><div class="wrap stack" style="gap:20px;max-width:980px">
<div class="stack intro"><p class="eyebrow muted">The working papers</p>
<h2 class="h-lg">Read every document</h2>
<p class="lead muted">{len(docs)} papers, about {words // 1000:,}k words, free to read in full{intro}. Each one has a plain-text copy, and most have the original PDF.</p>
<p class="muted" style="font-size:15px">These papers were written in 2024 and 2025 as the plan developed. Where one differs from <a href="{PLAN}">the 2025 edition of the Plan</a>, the 2025 edition is the current statement.</p></div>
{''.join(out)}
</div></section>"""


def flow(steps, label):
    """Numbered left-to-right flow (wraps on small screens)."""
    items = "".join(f'<li><span class="flow-n">{i}</span><strong>{esc(t)}</strong><span class="muted">{esc(d)}</span></li>'
                    for i, (t, d) in enumerate(steps, 1))
    return f'<ol class="flow" aria-label="{esc(label)}">{items}</ol>'


def timeline(rows):
    items = "".join(f'<li><span class="tl-when">{esc(w)}</span><div><strong>{esc(t)}</strong><span class="muted">{esc(d)}</span></div></li>'
                    for w, t, d in rows)
    return f'<ol class="timeline">{items}</ol>'


def qa(pairs):
    return "".join(f'<details class="card faq"><summary>{esc(q)}</summary><p class="muted">{esc(a)}</p></details>' for q, a in pairs)


def hero(eyebrow, title, lead, actions, extra=""):
    return f"""<section class="band hero-build"><div class="wrap section stack" style="gap:22px;position:relative">
<p class="crumbs"><a href="builders.html">End Poverty by Design</a></p>
<p class="eyebrow accent">{esc(eyebrow)}</p>
<h1 class="h-xl" style="max-width:900px">{esc(title)}</h1>
<p class="lead muted" style="max-width:700px">{lead}</p>
{extra}
<div class="actions">{actions}</div>
</div></section>"""


def nav_for(current):
    items = [("The plan", "builders.html", False, None), ("Civic Credits", PLAN + "civic-credits/", False, None),
             ("PECs", PLAN + "poverty-elimination-centers/", False, None), ("LifeLink", PLAN + "lifelink/", False, None),
             ("Support", "support.html", True, None)]
    return [x for x in items if x[1] != current]


def other_instruments(current):
    cards = [("civic-credits", "Civic Credits", "Pay for the work a community needs."),
             ("poverty-elimination-centers", "Poverty Elimination Centers", "A complete path from struggle to stability."),
             ("lifelink", "LifeLink", "One link to every public service.")]
    html = "".join(f"""<a class="card" href="{PLAN}{k}/"><span class="step-label">Instrument</span>
<span class="h-md" style="font-family:var(--display)">{esc(n)}</span><span class="muted">{esc(t)}</span><span class="card-cta">Explore →</span></a>"""
                   for k, n, t in cards if k != current)
    return f"""<section class="section"><div class="wrap stack" style="gap:24px">
<h2 class="h-lg">The other two instruments</h2>
<p class="lead muted">Each instrument does one job. They are designed to work together.</p>
<div class="grid grid-2">{html}
</div></div></section>"""


def end_band():
    return f"""<section class="section"><div class="wrap stack" style="max-width:820px;align-items:center;text-align:center;gap:20px">
<h2 class="h-lg">Help build it.</h2>
<p class="lead muted">The first pilots need funding, partners and people: the Civic Credits software, the first Poverty Elimination Centers, and LifeLink development.</p>
<div class="actions" style="justify-content:center"><a class="btn btn-door" href="support.html">Support the plan</a><a class="btn btn-outline" href="builders.html#partner">Partner with us</a></div>
</div></section>
{B.signup_band("Follow the plan's progress.", "Occasional updates on pilots, partners and milestones. Unsubscribe any time.", "Send me updates", "builders", "builders")}"""


def ld(name, desc, url):
    data = {"@context": "https://schema.org", "@type": "WebPage", "name": name, "description": desc, "url": f"{B.SITE_URL}/{url}",
            "author": {"@type": "Person", "name": B.AUTHOR}, "publisher": {"@type": "Organization", "name": "People of the World"},
            "isPartOf": {"@type": "Book", "name": LP.BOOK_PLAN, "url": f"{B.SITE_URL}/{PLAN}"}, "about": ["Poverty", "Economic policy", name]}
    return f'\n<script type="application/ld+json">{json.dumps(data, ensure_ascii=False)}</script>'


# ======================================================================= the hub
def build_hub():
    s = stats()
    instruments = [
        ("civic-credits", "Civic Credits", "Pay for the work a community needs",
         "A public unit of value created only after verified work for the community: a nurse's shift, a teacher's lesson, a crew restoring a park. Credits arrive in the worker's wallet the next morning and spend like money at shops, landlords and utilities.",
         f"{len(s['by_prog']['civic-credits'])} papers"),
        ("poverty-elimination-centers", "Poverty Elimination Centers", "A complete path from struggle to stability",
         "Campuses that bring housing, meals, healthcare, counselling, education, job training and real paid work under one roof, for anyone facing homelessness, unemployment or long-term hardship. Joining is a choice.",
         f"{len(s['by_prog']['poverty-elimination-centers'])} papers"),
        ("lifelink", "LifeLink", "One link to every public service",
         "A secure digital identity and wallet on a free tablet, app or wearable. It connects each person to their Civic Credits, learning, healthcare, emergency help and a direct voice in government.",
         f"{len(s['by_prog']['lifelink'])} papers"),
    ]
    cards = "\n".join(f"""<a class="card" href="{PLAN}{k}/"><span class="step-label">Instrument {i} · {esc(n_docs)}</span><h3 class="h-md">{esc(n)}</h3>
<p style="font-weight:600">{esc(t)}</p><p class="muted" style="font-size:15.5px">{esc(d)}</p><span class="card-cta" style="margin-top:auto">Explore {esc(n)} →</span></a>"""
                      for i, (k, n, t, d, n_docs) in enumerate(instruments, 1))

    system = f"""<div class="system" role="img" aria-label="How the three instruments connect: LifeLink gives each person an identity and wallet; Civic Credits pay for verified work into that wallet; Poverty Elimination Centers verify work, train people and accept credits for housing, food, care and learning.">
<div class="sys-node sys-ll"><span class="step-label">Identity and access</span><strong>LifeLink</strong><span>Who you are, your wallet, your services</span></div>
<div class="sys-edge"><span>verifies every person and transaction</span></div>
<div class="sys-node sys-cc"><span class="step-label">Value</span><strong>Civic Credits</strong><span>Paid for verified work, spent anywhere</span></div>
<div class="sys-edge"><span>funds the centres and pays their participants</span></div>
<div class="sys-node sys-pec"><span class="step-label">Place</span><strong>Poverty Elimination Centers</strong><span>Housing, care, training and work</span></div>
<div class="sys-edge sys-back"><span>train people for the work that earns credits</span></div>
</div>"""

    day = [("A nurse, evening shift", "Six hours at a PEC clinic and two hours of community triage, verified by her supervisor. Credits arrive overnight at the full billed value of nursing work, and she uses them at the supermarket, for childcare and for transit."),
           ("A teacher, after-school literacy", "Three afternoons a week. Credits are paid weekly after verification, and rent is paid straight from her wallet, with the landlord settled automatically."),
           ("A city horticulture worker", "A full-time civic role keeping parks planted and streets clean. It is work cities once called too expensive; now it is paid in credits that cover food, housing and utilities."),
           ("A solar-installer apprentice", "On-the-job hours are verified by a licensed mentor. He earns at the apprentice rate, eats at the PEC cafeteria, and his transit pass is covered.")]
    day_html = "".join(f'<div class="card"><span class="step-label">A day in the life</span><span class="h-md" style="font-family:var(--display)">{esc(t)}</span><span class="muted" style="font-size:15.5px">{esc(d)}</span></div>' for t, d in day)

    road = timeline([
        ("2026–2030", "Pilot and validation", "Pilots in 6 to 8 early-adopter countries; 100 Poverty Elimination Centers; 2 million LifeLink tablets and 5 million wearables; Civic Credits for health, education and local infrastructure; independent evaluations published. Review gate in 2030."),
        ("2031–2035", "National scale-up", "Full national coverage in the first-wave countries; 10,000 new centres; 100 million devices made locally; Civic Credits connected to national payment systems; 1 billion people enrolled. Review gate in 2035."),
        ("2036–2040", "Regional integration", "Regional councils align credit values, LifeLink ID and centre standards, so education and health credentials transfer across borders; 3 billion people on connected networks by 2039."),
        ("2041–2047", "Global interconnection", "A universal Civic Credit standard and an exchange for international value transfer, connected to global aid, trade and environmental systems. Review gate in 2045."),
        ("2048–2050", "Institutional maturity", "Governance made permanent and independent; the framework self-sustaining; poverty ended as a structural condition."),
    ])

    proven = [("Paying for public work", "India has guaranteed rural households paid public work since 2005: 100 days a year under MGNREGA, raised to 125 days by the law that replaced it in December 2025.", "Civic employment can run alongside private jobs, at national scale.", "vbg"),
              ("Sharing resource wealth", "The Alaska Permanent Fund has paid eligible residents a yearly dividend from oil revenue since 1982. University of Alaska researchers estimate it lifted about 25,000 Alaskans out of poverty in 2015, about a third of the poverty that would otherwise have existed.", "Public ownership of natural wealth can fund people directly.", "iser"),
              ("A parallel currency", "Switzerland's WIR has let small and medium businesses trade in their own complementary currency since 1934; more than 60,000 firms took part by the 2010s. Research finds its use rises when unemployment rises, steadying the economy in downturns.", "A second currency can circulate alongside national money, and help most when times are hard.", "levy"),
              ("Money on a phone", "A study in Science found Kenya's M-Pesa mobile money lifted about 194,000 households, 2% of the country, out of extreme poverty from 2008, with the largest gains in households headed by women.", "Digital wallets can reach everyone, and change lives when they do.", "mit"),
              ("Rewarding verified effort", "Brazil's Bolsa Família pays families who keep children in school and attend health check-ups. By 2013 it reached about 50 million people for around 0.6% of GDP, and Brazil's IPEA found it cut extreme poverty by about a quarter.", "Payments tied to verified actions change lives at national scale, cheaply.", "ipea")]
    sources = {"vbg": ("Viksit Bharat–G RAM G Act, 2025", "https://en.wikipedia.org/wiki/Viksit_Bharat%E2%80%93Guarantee_for_Rozgar_and_Ajeevika_Mission_(Gramin)_Act,_2025"),
               "iser": ("University of Alaska Anchorage, ISER: how PFDs reduce poverty", "https://www.uaa.alaska.edu/news/archive/2017/01/iser-research-matters-how-pfds-reduce-poverty-alaska"),
               "levy": ("Levy Economics Institute, Policy Note 2016/1 (citing Stodder, 2009)", "https://levyweb.bard.edu/wp-content/uploads/2024/02/pn_16_1.pdf"),
               "mit": ("MIT News: mobile money lifted Kenyans out of poverty (Suri and Jack, Science, 2016)", "https://news.mit.edu/2016/mobile-money-kenyans-out-poverty-1208"),
               "ipea": ("World Bank: Bolsa Família, Brazil's quiet revolution", "https://www.worldbank.org/en/news/opinion/2013/11/04/bolsa-familia-Brazil-quiet-revolution"),
               "ipea2": ("IPEA study, 2001–2017, reported by Money Times (Portuguese)", "https://www.moneytimes.com.br/bolsa-familia-reduziu-25-da-taxa-de-extrema-pobreza-aponta-ipea/")}
    proven_html = "".join(f'<li><strong>{esc(a)}</strong><span>{esc(b)}</span><span class="muted">What it shows: {esc(c)}</span></li>' for a, b, c, _ in proven)
    sources_html = "".join(f'<li><a href="{u}" rel="noopener">{esc(t)}</a></li>' for t, u in sources.values())

    packs = [("Everyday people", "What changes for you and your family."), ("Community leaders", "Running Civic Credits and PECs locally."),
             ("Entrepreneurs", "Accepting credits and building on LifeLink."), ("Governments", "Pilots, policy and national rollout."),
             ("Investors and funders", "Where support goes and how impact is measured."), ("Press", "The story, the founder and key facts."),
             ("Scientists and economists", "The mechanics and the questions pilots must answer.")]
    pack_html = "".join(f'<li><strong>{esc(a)}</strong><span class="muted">{esc(b)}</span></li>' for a, b in packs)
    faq = [("Is People of the World political?", "No. It is structural and moral, not partisan. The plan is written so that any government, of any party, could pilot it."),
           ("Do Civic Credits replace money?", "No. They run alongside national currency at one-to-one parity, on the same card terminals and online payment systems. Choosing to work for credits is voluntary for workers and employers, and either can switch back to ordinary wages."),
           ("Do businesses have to accept them?", "Using credits is a choice; being able to spend them is built in. Governments take credits for taxes, fees and public services, payment networks carry them beside cards, and a national rollout has registered businesses accept them at parity, so a credit always spends."),
           ("Isn't this just printing money?", "No. A credit is created only after real work has been verified, so new spending power appears at the same moment as new services: more nurses at work, more teachers in classrooms, more homes repaired."),
           ("Where does the value come from?", "From three anchors: the work already done, governments accepting credits for taxes and fees, and merchants being able to exchange credits for dollars at parity."),
           ("Who pays for it?", "No single source. Credits are created against work, so they need no upfront budget; what needs funding is the reserve behind the cash-out guarantee and the centres themselves. The plan draws on several layers: revenue from natural resources and public utilities, the taxes and fees paid in credits, the centres' own enterprises, public and development-bank investment, and partners. Each country sets its mix, and it adjusts as conditions change."),
           ("Does everyone have to join a PEC?", "No. PECs are for people who need help or want a structured path forward."),
           ("Do I have to pay for LifeLink?", "No. LifeLink is provided to every citizen, as an app on a phone you already have or as a free device."),
           ("Has it been tried?", "Not as a whole system yet; that is what the pilots are for. Each of its parts has precedents that already work, from public employment guarantees to resource dividends and mobile money."),
           ("Who created the plan?", "Shareef Ali Rashada, founder of People of the World.")]

    lib_rows = "".join(f"""<li><a href="{PLAN}{k}/#papers"><span class="li-title">{esc(v)}: working papers</span>
<span class="li-sub muted">{len(s['by_prog'][k])} documents</span></a><span class="li-meta">{sum(d['words'] for d in s['by_prog'][k]) // 1000}k words</span></li>"""
                       for k, v in LP.PROGRAMMES.items())

    body = f"""{B.header("End Poverty by Design", "by People of the World", [("How it works", "#how", False, None), ("The road to 2050", "#road", False, None),
                        ("Is it possible?", "#possible", False, None), ("Read it all", "#library", False, None), ("Support the plan", "support.html", True, None)])}
<main>
<section class="band hero-build"><div class="wrap section stack" style="gap:22px;position:relative">
<p class="eyebrow accent">The Plan to End Poverty · 2025 edition</p>
<h1 class="h-xl" style="max-width:900px">Ending poverty by 2050, by design.</h1>
<p class="lead muted" style="max-width:680px">We already have the people and the skills. What we run out of is the budget line. The Plan to End Poverty is a designed system, built on three instruments that pay for essential work, give everyone a path to stability, and connect every citizen to the services they need.</p>
<p class="quote" style="font-size:clamp(1.5rem,3vw,2rem)">This is not charity. This is structure.</p>
<div class="actions"><a class="btn btn-door" href="#how">See how it works</a><a class="btn btn-ghost" href="#library">Read the full plan</a></div>
<ul class="stats" aria-label="The plan in numbers">
<li><strong>{s['docs']}</strong><span>documents</span></li>
<li><strong>{s['words'] // 1000:,}k</strong><span>words, all free to read</span></li>
<li><strong>3</strong><span>instruments, one system</span></li>
<li><strong>2050</strong><span>the year poverty ends</span></li></ul>
<div class="blocks" aria-hidden="true">{"".join(f'<span style="--i:{i}"></span>' for i in range(12))}</div>
</div></section>

<section id="how" class="section"><div class="wrap stack" style="gap:36px">
<div class="stack intro"><h2 class="h-lg">Three instruments, one system</h2>
<p class="lead muted">Each one does a single job. Together they make poverty unnecessary.</p></div>
<div class="grid grid-3">{cards}</div>
</div></section>

<section class="section band-alt"><div class="wrap stack" style="gap:28px">
<div class="stack intro"><h2 class="h-lg">How they work together</h2>
<p class="lead muted">Take any one away and the others weaken. Together they close the loop between work, pay and opportunity.</p></div>
{system}
</div></section>

<section class="section"><div class="wrap stack" style="gap:28px">
<div class="stack intro"><h2 class="h-lg">What it looks like on an ordinary day</h2>
<p class="lead muted">From the plan's public lecture, <a href="{LP.working_url({'programme': 'civic-credits', 'title': 'Ending Poverty by 2050: Civic Credits, Explained'})}">Ending Poverty by 2050</a>.</p></div>
<div class="grid grid-2">{day_html}</div>
</div></section>

<section id="road" class="section band-alt"><div class="wrap stack" style="gap:28px;max-width:980px">
<div class="stack intro"><p class="eyebrow muted">Implementation roadmap</p><h2 class="h-lg">The road to 2050</h2>
<p class="lead muted">Five phases with three review gates, so each step is audited before the next begins. These are the targets set in the 2025 edition.</p></div>
{road}
<p class="muted" style="font-size:15px">The full roadmap, with country selection and participation pathways, is in <a href="{PLAN}chapter-09-implementation/">Chapter 9: Implementation</a>.</p>
</div></section>

<section id="possible" class="section"><div class="wrap" style="display:flex;flex-wrap:wrap;gap:32px 64px;align-items:flex-start">
<div class="stack" style="flex:1 1 340px;min-width:0">
<p class="eyebrow muted">Is it possible?</p>
<h2 class="h-lg">Every part already works somewhere.</h2>
<p class="lead muted">Nothing in the plan needs a technology or an institution the world has never seen. What is new is putting the proven parts together, under one set of rules, aimed at one goal.</p>
<p class="muted">The design also keeps the risks small. Credits exist only after work is done. They run on the payment systems shops already use. The pilots start with one or two sectors in a region, publish their results, and pass a review gate before anything grows.</p>
<p class="muted">What isn't proven yet is the whole system working as one. That is exactly what the pilots are for.</p>
</div>
<div class="stack" style="flex:1.4 1 460px;min-width:0;gap:14px"><ul class="proof">{proven_html}</ul>
<details class="sources"><summary>Sources</summary><ul>{sources_html}</ul></details></div>
</div></section>

<section id="library" class="section band-alt"><div class="wrap stack" style="gap:24px;max-width:980px">
<div class="stack intro"><p class="eyebrow muted">Read it all</p><h2 class="h-lg">The complete plan, open to everyone</h2>
<p class="lead muted">Nothing is held back. The full 2025 edition and every working paper behind it are free to read, as web pages, plain text and original PDFs.</p></div>
<ol class="doclist">
<li><a href="{PLAN}"><span class="li-title">{esc(LP.BOOK_PLAN)}</span><span class="li-sub muted">The complete 2025 edition: the economics, the Civic Charter, the centres, LifeLink, the global treasury, implementation and appendices.</span></a><span class="li-meta">{s['chapters']} chapters · {s['plan_words'] // 1000}k words</span></li>
{lib_rows}</ol>
</div></section>

<section class="section"><div class="wrap" style="display:flex;flex-wrap:wrap;gap:24px 64px;align-items:center">
<div class="stack" style="flex:1 1 360px;min-width:0"><p class="eyebrow muted">The moral foundation</p>
<h2 class="h-lg">The New Morality</h2>
<p class="lead muted">Everything starts with one idea: humans should treat each other better than any generation before us. Kindness becomes expected, fairness becomes normal, and respect becomes the baseline.</p>
<p><a href="new-morality/" style="font-weight:600">Read the New Morality →</a></p></div>
<blockquote class="quote" style="flex:1 1 360px;margin:0;min-width:0">“Treat another as the God in you would treat the God in the other.”</blockquote>
</div></section>

<section id="packs" class="section band-alt"><div class="wrap" style="display:flex;flex-wrap:wrap;gap:32px 64px">
<div class="stack" style="flex:1 1 320px;min-width:0"><h2 class="h-lg">An information pack for you</h2>
<p class="lead muted">The plan is free to learn. Choose the pack written for your role, and it will be sent to you.</p>
<p class="muted">Write to <strong>{B.CONTACT}</strong> with the pack you'd like.</p></div>
<ul class="packs" style="flex:2 1 460px;min-width:0">{pack_html}</ul>
</div></section>

<section id="partner" class="section"><div class="wrap" style="display:flex;flex-wrap:wrap;gap:32px 64px;align-items:center">
<div class="stack" style="flex:2 1 460px;min-width:0">
<p class="eyebrow accent" style="filter:brightness(.75)">Free to learn · licensed for profit</p>
<h2 class="h-lg">Putting the plan to work?</h2>
<p class="lead muted">Individuals, students and community groups use the plan freely. Governments, businesses and organisations that build programmes or earn revenue from it work with People of the World under a licence or partnership, which funds the mission.</p>
</div>
<div class="card" style="flex:1 1 300px"><span class="h-md" style="font-family:var(--display)">Partner enquiries</span>
<span class="muted" style="font-size:15px">Tell us who you are, where you work and what you'd like to build.</span>
<span class="copy-row" style="margin-top:6px"><span style="font-weight:600">{B.CONTACT}</span><button class="copy-btn copy-btn-light" type="button" data-copy="{B.CONTACT}">Copy</button></span></div>
</div></section>

<section id="faq" class="section band-alt"><div class="wrap stack" style="gap:28px">
<h2 class="h-lg">Questions people ask</h2>
<div class="faqs">{qa(faq)}</div>
</div></section>
{end_band()}
</main>
{B.footer("builders")}"""
    B.page("builders.html", "End Poverty by Design",
           "The Plan to End Poverty by 2050: Civic Credits, Poverty Elimination Centers and LifeLink, with the full 2025 edition and every working paper free to read.",
           body, "builders", ld("End Poverty by Design", "The Plan to End Poverty by 2050, in plain language.", "builders.html"))


# ======================================================================= Civic Credits
def build_civic_credits():
    url = PLAN + "civic-credits/"
    steps = flow([("Do the work", "A verified shift in health, education, care, housing, food or community services."),
                  ("Verified that evening", "Supervisor sign-off, with time records and random audits."),
                  ("Paid by morning", "The clearinghouse issues credits equal to the day's wage into your wallet."),
                  ("Spend like money", "Tap to pay for groceries, rent, transport and utilities."),
                  ("Back to the public", "Credits return through taxes, fees and public services, and are retired or reissued.")],
                 "The life of a Civic Credit")
    anchors = [("The work is already done", "Every new credit matches a service that now exists: a patient cared for, a class taught, a home repaired."),
               ("Governments accept it", "Taxes, licences, fees, public transit and utilities take credits at parity. That alone gives a currency value."),
               ("Shops can cash out", "Merchants can exchange credits for dollars at the clearinghouse, one for one, from a stabilisation reserve.")]
    anchors_html = "".join(f'<div class="card"><span class="step-label">Anchor {i}</span><span class="h-md" style="font-family:var(--display)">{esc(t)}</span><span class="muted">{esc(d)}</span></div>'
                           for i, (t, d) in enumerate(anchors, 1))
    domains = [("Care and health", "Nurses, paramedics, mental-health and disability support workers, home-care aides."),
               ("Education", "Early-childhood educators, teachers, tutors, vocational instructors, adult-literacy coaches."),
               ("Infrastructure and environment", "Clean-water and recycling crews, solar and efficiency installers, transit operators, reforestation teams."),
               ("Community safety", "Mediators, restorative-justice facilitators, emergency-response volunteers, elder-care coordinators."),
               ("Food and housing", "Urban farms, food distribution, kitchens, affordable-housing construction and repair."),
               ("Digital and civic", "LifeLink technicians, accessibility designers, translators, community tech support, public-interest media.")]
    dom_html = "".join(f'<li><strong>{esc(a)}</strong><span class="muted">{esc(b)}</span></li>' for a, b in domains)
    safeguards = [("No credit before the work", "Credits are never issued in advance."),
                  ("More than one signature", "Supervisor sign-off, random peer checks, and time and location proof where appropriate."),
                  ("Audits that respect privacy", "System-wide anomaly detection and targeted audits, with personal data kept off the public ledger."),
                  ("Rewards for whistleblowers", "Confirmed reports of fraud earn a credit bonus."),
                  ("Real penalties", "Restitution, suspension or removal; serious cases are prosecuted as theft from the commons."),
                  ("Everything published", "Daily totals by sector and region, redemption volumes and reserve coverage, reviewed by independent auditors and citizen committees.")]
    safe_html = "".join(f'<li><strong>{esc(a)}</strong><span class="muted">{esc(b)}</span></li>' for a, b in safeguards)
    objections = [("Isn't this just printing money?", "No. New credits exist only after verifiable work is done, so spending power rises with output. The mismatch that drives inflation is absent by design."),
                  ("Won't prices for essentials go up?", "Capacity rises with spending: when more nurses work, waiting times fall; when more builders repair homes, backlogs shrink. Prices for essentials bought with credits follow no-profit-on-necessities rules: true cost plus a fair margin."),
                  ("Will it push out ordinary wages?", "Taking part is contractual and voluntary. The first sectors are the understaffed ones where dollar budgets never meet the need."),
                  ("What if every shop cashes out straight away?", "That's expected at first, and it's why the stabilisation reserve exists. As governments accept credits for taxes and suppliers price some inputs in credits, natural uses for them reduce the pressure to cash out."),
                  ("What stops employers abusing it?", "Employers can't create credits; issuance is independent and happens only after verification. Wage rates are set from market data and reviewed in public, and disputes go to an independent tribunal."),
                  ("What happens in a downturn?", "Issuance is capped by sector and prioritises essential services. Because credits aren't debt, there is no debt spiral to unwind."),
                  ("Is it a second-class currency?", "No. It has full parity and public acceptance; it is a purpose-built way to settle essential work, used alongside national currency.")]
    rollout = timeline([("Launch", "One or two sectors per region", "For example nursing aides and home repairs, with strict parity and instant redemption for merchants."),
                        ("Prove", "Publish weekly results", "Staffing up, waiting times down, redemption stable: the evidence that builds trust."),
                        ("Grow", "Expand acceptance and sectors", "More public-sector acceptance points first, then more sectors as the data supports it.")])
    layers = [("Work-backed issuance", "Credits are created only against verified work and return through taxes, fees and public services. The value is the work itself.", "No budget needed for the credit"),
              ("The commons dividend", "Revenue from natural resources and public utilities, logged in plain units (kilowatt-hours, litres, tonnes, gigabytes) and converted on a published schedule. The funding paper's split: 60% to the workers who run those systems, 20% to maintenance and infrastructure, 20% to a community dividend for the centres, healthcare and education.", "Backs the reserve and the centres"),
              ("Resource and licence fees", "Fees on companies that extract or use public resources, higher for finite resources like minerals and oil than for renewable ones like timber.", "Feeds the stabilisation reserve"),
              ("The stabilisation reserve", "Guarantees that any merchant can exchange credits for dollars at parity, with its coverage published daily. As more taxes and supplier bills are paid in credits, the pressure to cash out falls.", "Keeps the peg credible"),
              ("Centre enterprises", "Each centre's own goods and services, surplus renewable energy, training contracts, public-works contracts and recycling. The 2025 edition targets 80–100% of a centre's running costs from these by year 10.", "Makes the centres self-sustaining"),
              ("Investment and partners", "Public budgets for education, health and labour; development banks through results-based loans and social bonds; philanthropy paid out only when credits for verified work are issued; and licence fees from organisations that build on the plan.", "Builds the first centres and systems")]
    layers_html = "".join(f'<li><span class="step-label">{esc(c)}</span><strong>{esc(a)}</strong><span class="muted">{esc(b)}</span></li>' for a, b, c in layers)
    part = [("Workers", "Choose roles paid in credits, or stay on ordinary wages. They can switch back."),
            ("Employers", "Opt in by signing a standard addendum; their timekeeping and quality checks stay the same."),
            ("Governments", "Accept credits for taxes, licences, fees, transit and utilities: the first and strongest guarantee of value."),
            ("Payment networks", "Carry a Civic Credit lane beside debit and credit, with a software update to existing terminals."),
            ("Businesses", "In a national rollout, registered merchants accept credits at parity. They can keep them to pay taxes and suppliers, or cash them out."),
            ("Citizens in need", "Joining a Poverty Elimination Center is always a choice, never a condition.")]
    part_html = "".join(f'<li><strong>{esc(a)}</strong><span class="muted">{esc(b)}</span></li>' for a, b in part)
    lecture = LP.working_url({"programme": "civic-credits", "title": "Ending Poverty by 2050: Civic Credits, Explained"})
    guide = LP.working_url({"programme": "civic-credits", "title": "Civic Credits, Simply"})
    paper = LP.working_url({"programme": "civic-credits", "title": "Civic Credits: A Debt-Free Employment and Settlement System for Essential Work"})
    charter = LP.working_url({"programme": "civic-credits", "title": "Civic Charter for Resources"})
    body = f"""{B.header("End Poverty by Design", "Civic Credits", nav_for(url))}
<main>
{hero("Instrument 1 of 3 · Civic Credits", "Pay for the work a community needs.",
      "Civic Credits are a public unit of value created only after verified work for the community. They are not borrowed into existence and carry no debt. They run alongside national money at one-to-one, on the same card terminals and apps people already use. If the work needs doing and people are ready to do it, society can afford it.",
      f'<a class="btn btn-door" href="#how">How a credit is made</a><a class="btn btn-ghost" href="{guide}">The two-page version</a><a class="btn btn-ghost" href="#papers">All papers</a>')}

<section id="how" class="section"><div class="wrap stack" style="gap:28px">
<div class="stack intro"><h2 class="h-lg">How a credit is made</h2>
<p class="lead muted">The workflow stays familiar. Only the money changes.</p></div>
{steps}
</div></section>

<section class="section band-alt"><div class="wrap" style="display:flex;flex-wrap:wrap;gap:28px 64px;align-items:center">
<div class="stack" style="flex:1 1 340px;min-width:0"><p class="eyebrow muted">Worked example</p>
<h2 class="h-lg">A nurse's day</h2>
<p class="lead muted">From the <a href="{paper}">technical white paper</a>.</p></div>
<ol class="receipt" style="flex:1.2 1 420px;min-width:0">
<li><span>Contracted at 40 credits an hour, she completes a 10-hour shift</span><strong>+400</strong></li>
<li><span>Her employer's system sends the verified completion; overnight the credits appear</span><strong>400</strong></li>
<li><span>Groceries</span><strong>−40</strong></li>
<li><span>Transport</span><strong>−10</strong></li>
<li><span>Utilities that accept credits</span><strong>−50</strong></li>
<li class="receipt-note"><span>The grocer keeps 20 credits to pay local fees and exchanges 20 for dollars at the clearinghouse. Those 20 credits are retired later, when a citizen pays tax with them.</span></li>
</ol>
</div></section>

<section class="section"><div class="wrap stack" style="gap:28px">
<div class="stack intro"><h2 class="h-lg">Why a credit holds its value</h2>
<p class="lead muted">Three anchors work together.</p></div>
<div class="grid grid-3">{anchors_html}</div>
</div></section>

<section id="funding" class="section band-alt"><div class="wrap stack" style="gap:28px">
<div class="stack intro"><p class="eyebrow muted">Who pays?</p>
<h2 class="h-lg">No single source, and no new debt.</h2>
<p class="lead muted">A credit is created against work already done, so the credit itself needs no budget. What needs funding is the reserve that lets shops cash credits out at parity, and the centres and systems that run the plan. These rest on several layers, so no one source can bring the system down. Each country sets its own mix and adjusts it as conditions change.</p></div>
<ol class="layers">{layers_html}</ol>
<p class="muted" style="font-size:15px">The foundation is the <a href="{charter}">Civic Charter for Resources</a>: no one created the land, the water, the minerals or the air, so the value they produce belongs to everyone and flows back as Civic Credits. Alaska has paid a resource dividend to its residents since 1982; see <a href="builders.html#possible">what already works</a>.</p>
</div></section>

<section id="pay" class="section"><div class="wrap" style="display:flex;flex-wrap:wrap;gap:32px 64px">
<div class="stack" style="flex:1 1 340px;min-width:0"><p class="eyebrow muted">What a credit pays</p>
<h2 class="h-lg">Every role has a published rate.</h2>
<p class="lead muted">A Role Standards Board defines each role and its rate from current market data, reviews the rates every quarter, and publishes them for public comment.</p>
<p class="muted">Pilots start at today's going rate, so nothing is disrupted on day one. Reviews then move each rate toward the full value society already pays for the work: where a contractor bills $40 an hour for a technician it pays $20, the work is worth $40. Disputes go to an independent tribunal.</p>
<p class="muted">Communities can propose new roles. If the work has a measurable public benefit and can be verified, it can be added.</p></div>
<div class="stack" style="flex:1 1 340px;min-width:0"><p class="eyebrow muted">What work earns credits</p>
<ul class="packs" style="grid-template-columns:1fr">{dom_html}</ul></div>
</div></section>

<section id="participation" class="section band-alt"><div class="wrap stack" style="gap:28px">
<div class="stack intro"><p class="eyebrow muted">Who takes part</p>
<h2 class="h-lg">Choosing credits is voluntary. Spending them is guaranteed.</h2>
<p class="lead muted">No one is made to work for credits, and no one is made to join a centre. But a credit is only useful if it spends everywhere, so acceptance is built into the system.</p></div>
<ul class="packs">{part_html}</ul>
</div></section>

<section class="section"><div class="wrap stack" style="gap:28px">
<div class="stack intro"><h2 class="h-lg">Built so it can't be gamed</h2>
<p class="lead muted">Trust, but verify: at every step.</p></div>
<ul class="packs">{safe_html}</ul>
</div></section>

<section class="section band-alt"><div class="wrap stack" style="gap:28px;max-width:980px">
<div class="stack intro"><h2 class="h-lg">Starting small</h2>
<p class="lead muted">The rollout is designed to earn confidence before it grows.</p></div>
{rollout}
</div></section>

<section class="section"><div class="wrap stack" style="gap:28px">
<h2 class="h-lg">The hard questions, answered</h2>
<div class="faqs">{qa(objections)}</div>
<p class="muted">More in the <a href="{lecture}">complete public lecture</a> and in <a href="{PLAN}chapter-05-the-civic-charter-and-civic-credits/">Chapter 5 of the Plan</a>, which adds the economic modelling, legal integration and international compatibility.</p>
</div></section>
{doc_library("civic-credits")}
{other_instruments("civic-credits")}
{end_band()}
</main>
{B.footer("builders")}"""
    desc = "Civic Credits: a debt-free public unit of value created only after verified community work, spent like money, backed by the commons. How they work, why they hold value, and every paper."
    B.page(url + "index.html", "Civic Credits · End Poverty by Design", desc, body, "builders", ld("Civic Credits", desc, url))


# ======================================================================= PECs
def build_pecs():
    url = PLAN + "poverty-elimination-centers/"
    programmes = [("Education", "From early childhood to advanced degrees, joining practical skills with academic learning, with classes for parents too."),
                  ("Vocational training", "Trades, agriculture, horticulture, physical health, arts and entertainment, with hands-on work that runs the campus itself."),
                  ("Health", "An on-site teaching hospital and health centres: preventive care, mental health and rehabilitation."),
                  ("Housing", "Dormitories at first, then independent apartments, for singles, families and people with special needs."),
                  ("Food", "A cafeteria run by the hospitality school, serving meals planned and cooked by culinary students."),
                  ("Work and enterprise", "Job placement with local employers, and support to start a business.")]
    prog_html = "".join(f'<div class="card"><span class="h-md" style="font-family:var(--display)">{esc(a)}</span><span class="muted">{esc(b)}</span></div>' for a, b in programmes)
    pathways = [("Indigent or displaced", "No housing, health or income", "Full residential care, a health assessment and a LifeLink ID; then rehabilitation, literacy and wellness."),
                ("Homeless, healthy, unskilled", "Able to work but lacking skills", "Food, shelter and a training stipend in credits; vocational training in cooking, maintenance or public works; then a job."),
                ("Homeless but skilled", "Skilled but displaced or unverified", "Temporary housing and digital onboarding; skills verified and certified; a contract or enterprise within about three months."),
                ("Unemployed or informal worker", "Seeking regular work", "Identity verification, counselling and credit-funded training; apprenticeships, digital work or enterprise support."),
                ("Existing public employee", "Teachers, medical and maintenance staff", "Kept in their role, with a credit supplement added to their wage for verified service.")]
    path_html = "".join(f'<li><strong>{esc(a)}</strong><span class="step-label">{esc(b)}</span><span class="muted">{esc(c)}</span></li>' for a, b, c in pathways)
    kinds = [("Urban flagship", "25,000–40,000 m²", "About 5,000 participants a day. The anchor for five to eight satellites, with the local credit node and data centre."),
             ("Peri-urban satellite", "8,000–15,000 m²", "1,500–2,000 participants a day. Vocational and agricultural training, renewable energy, cooperative manufacturing."),
             ("Rural micro-hub", "1,000–3,000 m²", "300–600 participants a day. Literacy, telehealth and repair training, in solar-powered modular pods."),
             ("Mobile unit", "Containers and vehicles", "Labs and fleets with satellite internet, for outreach and emergencies in climate- or conflict-affected regions.")]
    kinds_html = "".join(f'<div class="card"><span class="step-label">{esc(b)}</span><span class="h-md" style="font-family:var(--display)">{esc(a)}</span><span class="muted">{esc(c)}</span></div>' for a, b, c in kinds)
    cycle = flow([("Proposal", "Local authorities, citizens or institutions propose civic tasks."),
                  ("Validation", "Each proposal is checked for public benefit and feasibility."),
                  ("Execution", "Participants do the work under PEC supervision."),
                  ("Verification and reward", "Completion triggers Civic Credits through LifeLink.")], "The civic work cycle")
    proposal = LP.working_url({"programme": "poverty-elimination-centers", "title": "Poverty Elimination Centers"})
    body = f"""{B.header("End Poverty by Design", "Poverty Elimination Centers", nav_for(url))}
<main>
{hero("Instrument 2 of 3 · Poverty Elimination Centers", "A complete path from struggle to stability.",
      "A Poverty Elimination Center (PEC) brings everything a person needs to rebuild a life under one roof: a home, meals, healthcare, counselling, education, job training and real paid work. It is for anyone facing homelessness, unemployment, addiction or long-term hardship. Joining is a choice, never a requirement.",
      f'<a class="btn btn-door" href="#campus">What\'s on a campus</a><a class="btn btn-ghost" href="#pathways">Who it serves</a><a class="btn btn-ghost" href="#papers">All papers</a>')}

<section id="campus" class="section"><div class="wrap stack" style="gap:28px">
<div class="stack intro"><h2 class="h-lg">Everything under one roof</h2>
<p class="lead muted">No more getting lost between agencies. Each campus runs six programmes side by side.</p></div>
<div class="grid grid-3">{prog_html}</div>
<p class="muted">Campuses are designed to sustain themselves: solar and wind power, hydroponics alongside traditional farming, and waste recycling, with the aim of financial independence within a decade. (<a href="{proposal}">The PEC proposal</a>)</p>
</div></section>

<section id="pathways" class="section band-alt"><div class="wrap stack" style="gap:28px;max-width:1040px">
<div class="stack intro"><h2 class="h-lg">A way in for everyone</h2>
<p class="lead muted">People arrive from very different places. The plan maps a pathway for each, from first contact to standing on their own feet.</p></div>
<ol class="pathways">{path_html}</ol>
<p class="muted" style="font-size:15px">From the participation roadmap in <a href="{PLAN}chapter-06-poverty-elimination-centers-pecs/">Chapter 6 of the Plan</a>.</p>
</div></section>

<section class="section"><div class="wrap stack" style="gap:28px">
<div class="stack intro"><h2 class="h-lg">How work is paid</h2>
<p class="lead muted">Every centre is a node in the Civic Credit network. Useful work becomes verified, paid work.</p></div>
{cycle}
<p class="muted">Each centre is run by a three-part council: elected local representatives, trained administrators and educators, and independent auditors. All financial and performance data is published.</p>
</div></section>

<section class="section band-alt"><div class="wrap stack" style="gap:28px">
<div class="stack intro"><h2 class="h-lg">Four kinds of centre</h2>
<p class="lead muted">From megacities to remote villages, so everyone lives within reach of one.</p></div>
<div class="grid grid-2">{kinds_html}</div>
</div></section>

<section class="section"><div class="wrap" style="display:flex;flex-wrap:wrap;gap:32px 64px;align-items:center">
<div class="stack" style="flex:1 1 360px;min-width:0"><p class="eyebrow muted">The first step</p>
<h2 class="h-lg">The pilot</h2>
<p class="lead muted">The first campuses are planned for capital cities in the United States and Australia.</p>
<p class="muted">The 2025 edition sizes the first pilot phase at two flagship centres and six satellites across urban, peri-urban and rural sites, serving 25,000 people on a budget of USD 50 million, with the first campuses built within 12 months. Worldwide, the plan's first phase (2026–2030) calls for 100 centres in 6 to 8 countries.</p></div>
<ul class="stats stats-card" style="flex:1 1 360px;min-width:0">
<li><strong>2 + 6</strong><span>flagships and satellites in the pilot</span></li>
<li><strong>25,000</strong><span>people served in the pilot</span></li>
<li><strong>100</strong><span>centres by 2030</span></li>
<li><strong>10,000</strong><span>new centres by 2035</span></li></ul>
</div></section>
{doc_library("poverty-elimination-centers", ", from the original proposal to the operating guidelines and project charter")}
{other_instruments("poverty-elimination-centers")}
{end_band()}
</main>
{B.footer("builders")}"""
    desc = "Poverty Elimination Centers: housing, meals, healthcare, education, training and paid work under one roof, with a pathway for everyone. Campus design, the pilot, and every paper."
    B.page(url + "index.html", "Poverty Elimination Centers · End Poverty by Design", desc, body, "builders", ld("Poverty Elimination Centers", desc, url))


# ======================================================================= LifeLink
DEVICES = [("ll-look-smart-glasses", "glasses", "Look Smart Glasses", "Hands-free access with augmented-reality guidance, identity verification and payments."),
           ("ll-hear-buds", "hear-buds", "Hear Buds", "Voice access to every service, with real-time translation and sound enhancement."),
           ("ll-smartwatch", "smartwatch", "Smartwatch", "Health monitoring, emergency SOS, Civic Credit payments and alerts on the wrist."),
           ("ll-touch-smart-ring", "ring", "Touch Smart Ring", "A biometric key: tap to pay, sign in securely, or double-tap for silent SOS.")]


def build_lifelink():
    url = PLAN + "lifelink/"
    works = {d["slug"]: d for d in stats()["by_prog"]["lifelink"]}
    features = [("Identity", "A secure digital ID, verified by fingerprint, face or iris, that works offline and can't be lost like paper documents."),
                ("Wallet", "Earn, hold and spend Civic Credits; pay bills automatically; see exactly where public money goes."),
                ("Learning", "An AI teacher from basic literacy to career training, with automatic certification and job matching."),
                ("Health", "Telemedicine, mental-health support, preventive guidance and an emergency button that calls for help."),
                ("Voice", "Vote, petition and follow legislation; join town halls; speak directly to the people who represent you."),
                ("Creativity", "The Social, Arts and Creative hub, where artists, musicians and writers earn credits for their work.")]
    feat_html = "".join(f'<div class="card"><span class="h-md" style="font-family:var(--display)">{esc(a)}</span><span class="muted">{esc(b)}</span></div>' for a, b in features)
    dev_html = "".join(f"""<a class="device" href="{LP.working_url(works[s])}"><img src="assets/lifelink/{img}.jpg" alt="Concept rendering of the LifeLink {esc(n)}" width="320" height="320" loading="lazy">
<strong>{esc(n)}</strong><span class="muted">{esc(d)}</span></a>""" for s, img, n, d in DEVICES)
    safeguards = [("You own your data", "Opt out, delete or move your records at any time; personal and health data kept out of public ledgers."),
                  ("AI that assists, never rules", "Every AI decision must be explainable, publicly auditable, reversible and under human oversight."),
                  ("Three bodies of oversight", "An Ethical and Security Council for privacy and AI, a Public Assembly for citizens' say, and an Economic and Development Board for finances."),
                  ("Works when systems fail", "Offline ID, peer-to-peer mesh networking, solar-powered devices and satellite access in emergencies."),
                  ("Built to privacy law", "Designed to meet GDPR, CCPA and ISO security standards, with encryption designed to resist future quantum attacks."),
                  ("For people without papers", "Digital identity for refugees and displaced people, so no one is shut out of help.")]
    safe_html = "".join(f'<li><strong>{esc(a)}</strong><span class="muted">{esc(b)}</span></li>' for a, b in safeguards)
    day = flow([("Morning", "Sign in with a fingerprint; today's credits, bills and health check at a glance."),
                ("Work", "Job matching, certifications from the AI teacher, and secure remote work."),
                ("Learning", "A lesson plan built around your goals, from literacy to law."),
                ("Community", "Local projects that earn credits, events, and fact-checked news."),
                ("Evening", "Family connections, a reading list, and a quiet check-in on your wellbeing.")], "A day with LifeLink")
    roadmap = timeline([("Years 1–2", "Launch the core services", "The creative hub, AI teacher, civic hub, safety and health modules, on phones and certified devices; partnerships with device makers."),
                        ("Years 2–3", "Economy and governance", "LifeLink recognised as official digital ID in early-adopting nations; Civic Credits and PEC systems connected."),
                        ("Years 3–5", "Global standard", "Cross-border Civic Credit recognition, participatory-democracy tools, and PEC infrastructure worldwide."),
                        ("By 2030", "Devices in hand", "The 2025 edition's first-phase target: 2 million LifeLink tablets and 5 million wearables.")])
    body = f"""{B.header("End Poverty by Design", "LifeLink", nav_for(url))}
<main>
{hero("Instrument 3 of 3 · LifeLink", "One link to every public service.",
      "LifeLink gives every citizen a secure digital identity and wallet, free, on a phone they already own, a LifeLink tablet or a wearable. Through it people receive their Civic Credits, learn, see a doctor, call for help, and take part in government. No more paperwork, and no more getting lost between agencies.",
      f'<a class="btn btn-door" href="#what">What it does</a><a class="btn btn-ghost" href="#devices">The devices</a><a class="btn btn-ghost" href="#papers">All papers</a>')}

<section id="what" class="section"><div class="wrap stack" style="gap:28px">
<div class="stack intro"><h2 class="h-lg">What it does</h2>
<p class="lead muted">Six services, one secure identity.</p></div>
<div class="grid grid-3">{feat_html}</div>
</div></section>

<section class="section band-alt"><div class="wrap stack" style="gap:28px">
<div class="stack intro"><h2 class="h-lg">A day with LifeLink</h2>
<p class="lead muted">From <a href="{LP.working_url(works['ll-daily-implementation'])}">LifeLink Daily Implementation</a>.</p></div>
{day}
</div></section>

<section id="devices" class="section"><div class="wrap stack" style="gap:28px">
<div class="stack intro"><h2 class="h-lg">The LifeLink family</h2>
<p class="lead muted">LifeLink starts as an app and on <a href="{LP.working_url(works['ll-tablet'])}">the LifeLink Tablet</a> ("The Link"), then grows into a family of wearables, each with its own technical specification.</p></div>
<div class="devices">{dev_html}</div>
<p class="muted" style="font-size:14px">The pictures are AI-generated concept renderings; final products may differ.</p>
</div></section>

<section class="section band-alt"><div class="wrap stack" style="gap:28px">
<div class="stack intro"><h2 class="h-lg">Safeguards first</h2>
<p class="lead muted">A system this close to people's lives has to earn their trust. These rules are written into the design.</p></div>
<ul class="packs">{safe_html}</ul>
<p class="muted" style="font-size:15px">Detailed in the <a href="{LP.working_url(works['ll-ethical-ai-and-data-privacy-framework'])}">Ethical AI and Data Privacy Framework</a>, the <a href="{LP.working_url(works['ll-legal-and-ethical-safeguards-framework'])}">Legal and Ethical Safeguards Framework</a> and the <a href="{LP.working_url(works['ll-design-specification'])}">Core Specification</a>.</p>
</div></section>

<section class="section"><div class="wrap stack" style="gap:28px;max-width:980px">
<div class="stack intro"><h2 class="h-lg">The roadmap</h2>
<p class="lead muted">Phased, so each layer proves itself before the next is added.</p></div>
{roadmap}
</div></section>
{doc_library("lifelink", ", including 23 strategies covering everything from funding and hardware to health, education, governance and crisis response" + (f'. The complete <a href="{url}lifelink-master-plan.pdf">LifeLink Master Plan</a> (PDF) gathers them in one volume' if (B.SRC / "lifelink" / "lifelink-master-plan.pdf").exists() else ""))}
{other_instruments("lifelink")}
{end_band()}
</main>
{B.footer("builders")}"""
    desc = "LifeLink: a free, secure digital identity and wallet that connects every citizen to Civic Credits, learning, healthcare, safety and government. Devices, safeguards, roadmap and every paper."
    B.page(url + "index.html", "LifeLink · End Poverty by Design", desc, body, "builders", ld("LifeLink", desc, url))
    if (B.SRC / "lifelink" / "lifelink-master-plan.pdf").exists():
        shutil.copy(B.SRC / "lifelink" / "lifelink-master-plan.pdf", B.OUT / url / "lifelink-master-plan.pdf")


def build(b):
    global B, esc
    B, esc = b, b.esc
    img_src = B.SRC / "lifelink"
    (B.OUT / "assets" / "lifelink").mkdir(parents=True, exist_ok=True)
    for _, img, *_ in DEVICES:
        shutil.copy(img_src / f"{img}.jpg", B.OUT / "assets" / "lifelink" / f"{img}.jpg")
    build_hub()
    build_civic_credits()
    build_pecs()
    build_lifelink()
