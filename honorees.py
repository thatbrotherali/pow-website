"""The People of the World Honorees: the overview (honorees/), the call to serve (honorees/serve/),
and the partners and supporters page (honorees/partners/). Written so each page can be linked from an email.

Facts follow the plan Shareef approved in November 2026 (Project doc claude/people-of-the-world-honorees.md).
Nothing here promises money, tax deductions or dates beyond the published 2027 timeline.
"""
from urllib.parse import quote

B = None
esc = None
HONOURS = [("Science and Discovery", "People who ask how the world really works, seek mechanism rather than mere description, and put knowledge to the service of humanity."),
           ("Economics and Service to the Poor", "People who lift others out of poverty, whether by building better systems or by serving the hungry, the homeless and the forgotten with their own hands."),
           ("Peace and Unity", "People who bring others together across the lines that divide them: nation, faith, race, class and party."),
           ("Faith and Moral Courage", "People who do what is right when it costs them, and live their deepest convictions in the service of others, within any faith or none."),
           ("Music and the Arts", "People who use music and the arts to heal, teach, inspire and connect, and open the arts to those who were shut out of them.")]
YEAR = [("January to February", "The call goes out", "Nomination Readers and Category Judges are invited from around the world."),
        ("March", "The panel is announced", "The judges for each honour are named publicly."),
        ("April to June", "Nominations open", "Anyone may nominate someone whose life deserves to be honoured."),
        ("July to August", "Readers shortlist", "Readers check the facts of every nomination and recommend a shortlist in each area."),
        ("September", "Judges choose", "Three judges in each area choose that year's Honoree."),
        ("17 October", "Honorees announced", "On the United Nations' International Day for the Eradication of Poverty.")]


def mailto(subject, body):
    return f"mailto:{B.CONTACT}?subject={quote(subject)}&body={quote(body)}"


def timeline(rows):
    items = "".join(f'<li><span class="tl-when">{esc(w)}</span><div><strong>{esc(t)}</strong><span class="muted">{esc(d)}</span></div></li>' for w, t, d in rows)
    return f'<ol class="timeline">{items}</ol>'


def cards(rows, label=None):
    return "".join(f'<div class="card">{f"<span class=step-label>{esc(label)}</span>" if label else ""}<span class="h-md" style="font-family:var(--display)">{esc(a)}</span><span class="muted">{d}</span></div>' for a, d in rows)


def faq(rows):
    return "".join(f'<details class="card"><summary class="h-md" style="font-family:var(--display);cursor:pointer">{esc(q)}</summary><p class="muted" style="margin:10px 0 0">{a}</p></details>' for q, a in rows)


FAQ = [("Who is behind the honours?",
        "People of the World is a global movement founded by author and composer Shareef Ali Rashada, working toward a world at peace and free of poverty. It operates as a business name of POW Productions Pty Ltd. Its work includes the <a href=\"builders.html\">Plan to End Poverty</a>, <a href=\"easykey.html\">EasyKey Music</a>, and a free library of books and teachings."),
       ("Is this a religious organisation?",
        "People of the World stands openly on a spiritual foundation, <a href=\"new-morality/\">the New Morality</a>: every person carries within them a literal fragment of the Creator, and our guiding ideal is to treat others, and to act in every situation, as the God in us would treat the God in them. We belong to no church or denomination, and we ask no one to share our beliefs before taking part. The honours are open to people of every faith and of none, and the panel is drawn from all traditions."),
       ("Is it political?",
        "No. People of the World endorses no party or candidate, in any country, and the honours are never used to endorse anyone politically."),
       ("How are Honorees chosen?",
        "Anyone may nominate. Nomination Readers check the facts and shortlist, and three independent Category Judges choose each Honoree. Readers and judges agree to a code of impartiality, declare conflicts of interest and keep deliberations confidential. Partners and sponsors have no part in choosing Honorees."),
       ("How is support used?",
        "Only for what Honorees receive and for running the honours: travel not donated by partners, the recording and editing of each legacy, the annual book and its library copies, and the running of nominations. Honours money is kept in its own account, and each year we publish a statement of what was received and what it paid for."),
       ("Are you a registered charity? Is a gift tax-deductible?",
        "No. People of the World is not a registered charity, and gifts are not tax-deductible. Support from businesses is offered as a partnership in exchange for recognition; your own accountant can advise how to treat it."),
       ("What if the honours do not go ahead?",
        "For 2027, unspent gifts will be returned on request, or carried to the next year with the giver's agreement.")]


def build(b):
    global B, esc
    B, esc = b, b.esc
    build_overview()
    build_serve()
    build_partners()


def build_overview():
    receive = [("Time to rest", "A two-week stay with one of our Host Partners, places of beauty and peace, with travel provided by our Travel Partners."),
               ("Their legacy, in their own words", "A recorded interview and a piece they write themselves: the lessons they would leave. Kept permanently in a public library of the best examples of humanity."),
               ("A place in the annual book", "Each year's Honorees are published together in a book placed in libraries around the world."),
               ("Light on their work", "A profile in <em>A Deeper Look</em>, our weekly journal, and support raised in their name directed to the cause they serve.")]
    part = [("Serve on the panel", "Help choose the Honorees as a Nomination Reader or a Category Judge.", "honorees/serve/", "Answer the call"),
            ("Become a partner", "Host an Honoree, provide travel, or sponsor one of the five honours.", "honorees/partners/", "Partner with us"),
            ("Support the honours", "Help bring an Honoree to rest, record a legacy, or place the book in a library.", "honorees/partners/#give", "Ways to give"),
            ("Nominate someone", "Nominations open in April 2027. Sign up below and we will tell you when they do.", "#updates", "Tell me when")]
    part_html = "".join(f"""<div class="card"><span class="h-md" style="font-family:var(--display)">{esc(a)}</span><span class="muted">{esc(d)}</span>
<a class="btn btn-outline" style="margin-top:auto;align-self:flex-start" href="{h}">{esc(c)}</a></div>""" for a, d, h, c in part)
    honours = "".join(f'<div class="card"><span class="step-label">Honoree for</span><span class="h-md" style="font-family:var(--display)">{esc(a)}</span><span class="muted">{esc(d)}</span></div>' for a, d in HONOURS)
    body = f"""{B.header("People of the World", "The Honorees", [("All doors", "index.html#doors", False, None), ("Serve", "honorees/serve/", False, None), ("Partners", "honorees/partners/", False, None), ("Updates", "#updates", True, None)])}
<main>
<section class="band door-hub"><div class="wrap section stack" style="gap:22px">
<p class="eyebrow accent">The People of the World Honorees · from 2027</p>
<h1 class="h-xl" style="max-width:920px">Honouring the best of humanity.</h1>
<p class="lead muted" style="max-width:740px">Every day, the world's attention goes to the worst of us. Each year, the People of the World Honorees will turn it toward the best: five people whose lives show what humanity can be, in discovery, in service to the poor, in peacemaking, in moral courage, and in the arts.</p>
<div class="actions"><a class="btn btn-door" href="honorees/serve/">Serve on the panel</a><a class="btn btn-ghost" href="honorees/partners/">Become a partner</a></div>
</div></section>

<section class="section"><div class="wrap stack" style="gap:28px">
<div class="stack intro"><h2 class="h-lg">Why honour the good</h2>
<p class="lead muted" style="max-width:780px">What a society pays attention to, it grows more of. The quiet people who hold communities together are rarely seen. The Honorees may be famous, or known only to their neighbours. What they share is that they have made the world better, and that others can learn from how they did it.</p></div>
</div></section>

<section class="section band-alt"><div class="wrap stack" style="gap:28px">
<div class="stack intro"><h2 class="h-lg">The five honours</h2>
<p class="lead muted">One Honoree each year in each area. The areas are deliberately broad: what matters is the life, not the title.</p></div>
<div class="grid grid-3">{honours}</div>
</div></section>

<section class="section"><div class="wrap stack" style="gap:28px">
<div class="stack intro"><h2 class="h-lg">What Honorees receive</h2>
<p class="lead muted" style="max-width:760px">Not a cash prize, but something rarer for people who give their lives to others: rest, and a voice that lasts.</p></div>
<div class="grid grid-2">{cards(receive)}</div>
</div></section>

<section class="section band-alt"><div class="wrap stack" style="gap:28px;max-width:980px">
<div class="stack intro"><h2 class="h-lg">The year ahead</h2>
<p class="lead muted">The first Honorees are announced on 17 October 2027.</p></div>
{timeline(YEAR)}
</div></section>

<section class="section"><div class="wrap stack" style="gap:28px">
<div class="stack intro"><h2 class="h-lg">Take part</h2>
<p class="lead muted">An honour is only as meaningful as the people who make it possible.</p></div>
<div class="grid grid-2">{part_html}</div>
</div></section>

<section class="section band-alt"><div class="wrap stack" style="gap:20px;max-width:900px">
<div class="stack intro"><h2 class="h-lg">Questions</h2></div>
<div class="stack" style="gap:12px">{faq(FAQ[:4])}</div>
<p class="muted">More answers for partners and supporters on the <a href="honorees/partners/#questions">partners page</a>.</p>
</div></section>
<div id="updates"></div>
{B.signup_band("Follow the Honorees.", "An email when the panel is announced, when nominations open, and when the Honorees are named. Nothing else unless you ask.", "Keep me posted", "honorees", "hub")}
</main>
{B.footer()}"""
    B.page("honorees/index.html", "The People of the World Honorees",
           "The People of the World Honorees recognise five people each year whose lives show the best of humanity, from 2027. Serve on the panel, become a partner, or nominate someone.", body, "hub")


def build_serve():
    apply_body = ("Hi Shareef,\n\nI'd like to serve on the People of the World Honorees panel.\n\nRole (Nomination Reader or Category Judge):\n\n"
                  "Area (Science and Discovery / Economics and Service to the Poor / Peace and Unity / Faith and Moral Courage / Music and the Arts):\n\n"
                  "My name and country:\n\nMy experience in this area:\n\nWhy I'd like to take part:\n")
    roles = [("Nomination Reader", "Read nominations in one of the five areas, check the facts, and recommend a shortlist.", "A few hours a week, July to August 2027", "Open to anyone with relevant experience and a fair mind."),
             ("Category Judge", "Three judges in each area choose that year's Honoree from the shortlist. Judges are named publicly.", "About 10 to 15 hours in September 2027", "Chosen from the strongest applicants, alongside people we invite directly.")]
    roles_html = "".join(f"""<div class="card"><span class="step-label">{esc(t)}</span><span class="h-md" style="font-family:var(--display)">{esc(a)}</span><span class="muted">{esc(d)}</span>
<span class="muted" style="font-size:15px">{esc(w)}</span>
<a class="btn btn-door" style="margin-top:auto;align-self:flex-start" href="{esc(mailto(f'Honorees panel: application ({a})', apply_body))}">Apply as a {esc(a)}</a></div>""" for a, d, t, w in roles)
    code = [("Impartiality", "Judge each nominee on the life they have lived, not on who nominated them."),
            ("Honesty about conflicts", "Declare any personal or professional tie to a nominee, and step aside where one exists."),
            ("Confidentiality", "Keep deliberations private until the Honorees are announced."),
            ("Non-partisanship", "People of the World endorses no party or candidate, and the honours are never used to do so."),
            ("Respect", "Treat every nominee, and every faith and tradition, with respect.")]
    code_html = "".join(f'<li><strong>{esc(a)}</strong><span class="muted">{esc(d)}</span></li>' for a, d in code)
    honours = "".join(f'<li><strong>Honoree for {esc(a)}</strong><span class="muted">{esc(d)}</span></li>' for a, d in HONOURS)
    body = f"""{B.header("People of the World", "The Honorees", [("The Honorees", "honorees/", False, None), ("Partners", "honorees/partners/", False, None), ("Apply", "#apply", True, None)])}
<main>
<section class="band door-hub"><div class="wrap section stack" style="gap:22px">
<p class="crumbs"><a href="honorees/">The People of the World Honorees</a></p>
<p class="eyebrow accent">A call to serve</p>
<h1 class="h-xl" style="max-width:920px">Help us choose the People of the World Honorees for 2027.</h1>
<p class="lead muted" style="max-width:740px">An honour is only as meaningful as the people who decide it. So we are not choosing the Honorees alone. We are inviting people from around the world to help.</p>
<div class="actions"><a class="btn btn-door" href="#apply">Apply to serve</a><a class="btn btn-ghost" href="#who">Who we are</a></div>
</div></section>

<section id="who" class="section"><div class="wrap stack" style="gap:20px;max-width:900px">
<h2 class="h-lg">Who we are</h2>
<p class="lead muted">People of the World is a global movement with one aim: a world at peace, where no one lives in poverty.</p>
<p class="muted">Every nation on Earth has already promised that aim: the first of the United Nations' Sustainable Development Goals is to end poverty in all its forms, everywhere, by 2030. What has been missing is not the promise but the means, and the will to act on it together. Our <a href="builders.html">Plan to End Poverty</a> sets out practical tools any community or country can use: Poverty Elimination Centres, <a href="plan-to-end-poverty/civic-credits/">Civic Credits</a> that reward service to the community, and <a href="plan-to-end-poverty/lifelink/">LifeLink</a>, built on the rule <em>every person counted, no person tracked</em>.</p>
<p class="muted">Behind the plan stands a simple conviction, shared across every faith and tradition: that each person carries within them a sense of what is right, and that a world which listened to it would look very different from the one we have.</p>
</div></section>

<section class="section band-alt"><div class="wrap stack" style="gap:20px;max-width:900px">
<h2 class="h-lg">Why honour the good</h2>
<p class="muted">Every day, the world's attention goes to the worst of us. Conflict, scandal and cruelty fill the headlines, and the quiet people who hold communities together go unseen. Each year the Honorees will recognise people whose lives show the best of humanity. Instead of a cash prize, each receives time away to rest and be renewed, and the chance to record their legacy in their own words, kept in a public library and published each year as a book.</p>
<ol class="pathways">{honours}</ol>
</div></section>

<section id="apply" class="section"><div class="wrap stack" style="gap:28px">
<div class="stack intro"><h2 class="h-lg">Your part</h2>
<p class="lead muted">Two roles, both voluntary. Choose one, and your email opens with a short application ready to fill in.</p></div>
<div class="grid grid-2">{roles_html}</div>
<p class="muted">Or write directly to <a href="mailto:{B.CONTACT}">{B.CONTACT}</a> with your name and country, the area you would like to serve in, a few sentences about your experience, and why you would like to take part. In return, you will be part of the first year of a new tradition, named among the people who helped it begin.</p>
</div></section>

<section class="section band-alt"><div class="wrap stack" style="gap:24px;max-width:980px">
<div class="stack intro"><h2 class="h-lg">Who we are looking for</h2>
<p class="lead muted" style="max-width:800px">People with experience in one of the five areas, whether professional, in the community, or lived. A scientist, a social worker, a peacebuilder, a pastor, an imam, a music teacher and someone who has simply spent years serving others are all welcome. We want readers and judges from every continent, every faith and none, and every part of the political spectrum.</p></div>
<h3 class="h-md" style="font-family:var(--display)">Everyone who serves agrees to a short code</h3>
<ol class="pathways">{code_html}</ol>
</div></section>

<section class="section"><div class="wrap stack" style="gap:28px;max-width:980px">
<div class="stack intro"><h2 class="h-lg">The year ahead</h2></div>
{timeline(YEAR)}
<p class="muted">Not able to serve? Share this page with someone who should see it, and from April 2027, nominate someone whose life deserves to be honoured. <a href="honorees/">More about the Honorees</a>.</p>
</div></section>
{B.signup_band("Follow the Honorees.", "An email when the panel is announced, when nominations open, and when the Honorees are named. Nothing else unless you ask.", "Keep me posted", "honorees", "hub")}
</main>
{B.footer()}"""
    B.page("honorees/serve/index.html", "A Call to Serve · People of the World Honorees",
           "Help choose the People of the World Honorees for 2027. Apply to serve as a Nomination Reader or Category Judge in one of five areas.", body, "hub")


def build_partners():
    def talk(kind):
        body = (f"Hi Shareef,\n\nI'm interested in becoming a {kind} of the People of the World Honorees.\n\n"
                "Organisation (if any):\n\nWhat we could offer:\n\nWhere we're based:\n\nBest way to reach me:\n")
        return esc(mailto(f"Honorees: {kind}", body))
    host = [("What we ask", "A two-week stay for one Honoree, and optionally one companion, at a time of year that suits you, between November and the following September. You choose what the stay includes."),
            ("What you receive", "Named as a Host Partner on our website, in announcements and in the annual book placed in libraries; a profile in <em>A Deeper Look</em>; and, with the Honoree's consent, their reflections and photographs from the stay for your own use."),
            ("The practical side", "Honorees are your guests under your usual terms. Any publicity is agreed with you in advance, and the Honoree's privacy comes first. A cancellation carries no penalty on either side; we will work with you to find another date or Honoree.")]
    travel = [("What we ask", "Return travel for one Honoree, and optionally one companion, to their Host Partner each year. Airlines may offer flights; travel companies may offer flights, transfers or a whole itinerary."),
              ("What you receive", "Named as a Travel Partner on our website, in announcements and in the annual book; a profile in <em>A Deeper Look</em>; with the Honoree's consent, their story and photographs from the journey; and the option to be named with one honour: \"brought to rest by\" your company.")]
    sponsor = [("What it covers", "One honour for one year: the Honoree's travel when not donated, the recording of their legacy, their place in the annual book, and the library copies."),
               ("How you are recognised", "The honour is announced as \"the Honoree for [Category], supported by\" your organisation: in the announcement, on the website, in <em>A Deeper Look</em> and in the annual book. One sponsor per honour each year; renew three years running to be recognised as a Founding Sponsor."),
               ("Independence", "Sponsors have no part in nominations, shortlisting or judging, and may not nominate for the honour they sponsor. That protects the honour, and protects you from any suggestion that it can be bought."),
               ("Reporting", "A short report after the announcement: the Honoree's story, how your support was used, and where the honour was seen, with a copy of the annual book.")]
    give = [("Sponsor a legacy", "The recording and editing of one Honoree's interview and lessons."),
            ("Bring an Honoree to rest", "Travel to their donated stay, where a Travel Partner has not provided it."),
            ("Place the book in a library", "A copy of the annual book of Honorees for a public or university library."),
            ("Any amount", "Wherever the honours need it most.")]
    give_body = ("Hi Shareef,\n\nI'd like to support the People of the World Honorees.\n\nWhat I'd like my gift to go towards:\n\n"
                 "Should my name appear among the supporters in the annual book? (yes / no / anonymous)\n")
    body = f"""{B.header("People of the World", "The Honorees", [("The Honorees", "honorees/", False, None), ("Serve", "honorees/serve/", False, None), ("Questions", "#questions", True, None)])}
<main>
<section class="band door-hub"><div class="wrap section stack" style="gap:22px">
<p class="crumbs"><a href="honorees/">The People of the World Honorees</a></p>
<p class="eyebrow accent">Partners and supporters</p>
<h1 class="h-xl" style="max-width:920px">Give the best of humanity a place to rest.</h1>
<p class="lead muted" style="max-width:740px">The Honorees receive what money rarely buys: two weeks of rest, and the chance to record the lessons of their lives. That is made possible by partners who give a stay, a journey or the means to record a legacy.</p>
<div class="actions"><a class="btn btn-door" href="#hosts">Host an Honoree</a><a class="btn btn-ghost" href="#sponsors">Sponsor an honour</a><a class="btn btn-ghost" href="#give">Give</a></div>
</div></section>

<section id="hosts" class="section"><div class="wrap stack" style="gap:28px">
<div class="stack intro"><p class="eyebrow accent">Host Partners</p><h2 class="h-lg">Host an Honoree</h2>
<p class="lead muted" style="max-width:760px">For retreat centres, eco-lodges and places of real beauty and peace. An Honoree's time with you becomes part of their recorded legacy.</p></div>
<div class="grid grid-3">{cards(host)}</div>
<div class="actions"><a class="btn btn-solid" href="{talk('Host Partner')}">Talk to us about hosting</a></div>
</div></section>

<section id="travel" class="section band-alt"><div class="wrap stack" style="gap:28px">
<div class="stack intro"><p class="eyebrow accent">Travel Partners</p><h2 class="h-lg">Bring an Honoree to rest</h2>
<p class="lead muted" style="max-width:760px">For airlines and travel companies. We offer this as a partnership: your support in exchange for recognition.</p></div>
<div class="grid grid-2">{cards(travel)}</div>
<div class="actions"><a class="btn btn-solid" href="{talk('Travel Partner')}">Talk to us about travel</a></div>
</div></section>

<section id="sponsors" class="section"><div class="wrap stack" style="gap:28px">
<div class="stack intro"><p class="eyebrow accent">Category sponsors</p><h2 class="h-lg">Sponsor one of the five honours</h2>
<p class="lead muted" style="max-width:760px">For organisations whose work matches one of the honours: Science and Discovery; Economics and Service to the Poor; Peace and Unity; Faith and Moral Courage; or Music and the Arts.</p></div>
<div class="grid grid-2">{cards(sponsor)}</div>
<div class="actions"><a class="btn btn-solid" href="{talk('Category Sponsor')}">Talk to us about sponsorship</a></div>
</div></section>

<section id="give" class="section band-alt"><div class="wrap stack" style="gap:28px">
<div class="stack intro"><p class="eyebrow accent">Individual supporters</p><h2 class="h-lg">Help us honour the best of humanity</h2>
<p class="lead muted" style="max-width:760px">Choose a gift that means something to you. Every gift is acknowledged and, if you wish, your name appears among the supporters in that year's book.</p></div>
<div class="grid grid-2">{cards(give)}</div>
<p class="muted">Online giving is being set up. Until it opens, write to us and we will reply with the ways to give: <a href="{esc(mailto('Honorees: I would like to give', give_body))}">{B.CONTACT}</a>. Gifts are not tax-deductible.</p>
</div></section>

<section id="questions" class="section"><div class="wrap stack" style="gap:20px;max-width:900px">
<div class="stack intro"><h2 class="h-lg">Questions partners ask</h2></div>
<div class="stack" style="gap:12px">{faq(FAQ)}</div>
<p class="muted">Anything else? Write to <a href="mailto:{B.CONTACT}">{B.CONTACT}</a>.</p>
</div></section>
{B.signup_band("Follow the Honorees.", "An email when the panel is announced, when nominations open, and when the Honorees are named. Nothing else unless you ask.", "Keep me posted", "honorees", "hub")}
</main>
{B.footer()}"""
    B.page("honorees/partners/index.html", "Partners and Supporters · People of the World Honorees",
           "Host an Honoree, provide travel, sponsor one of the five People of the World Honours, or give. What partners give, what they receive, and answers to common questions.", body, "hub")
