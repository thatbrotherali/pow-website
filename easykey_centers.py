"""EasyKey Music Centers: the vision page (easykey/centers/), written to invite partners.

Nothing here exists yet; the page says so plainly. Legal points are stated as the operating rules
the centres will follow (lessons, not childcare; screening by role; partner professionals).
"""
from urllib.parse import quote

B = None
esc = None
URL = "easykey/centers/"
NEC = "https://www5.austlii.edu.au/au/legis/nsw/consol_act/cacsnl443/s5.html"


def mailto(role):
    subject = f"EasyKey Music Centers: count me in ({role})"
    body = ("Hi Shareef,\n\nI'd like to help build the EasyKey Music Centers.\n\n"
            f"How I can help ({role}):\n\nWhere I'm based:\n\nBest way to reach me:\n")
    return f"mailto:{B.CONTACT}?subject={quote(subject)}&body={quote(body)}"


def build(b):
    global B, esc
    B, esc = b, b.esc
    day = [("Morning", "Community sessions", "Seniors meet for a weekly social piano session, led by a partner professional trained in EasyKey."),
           ("After school", "Children learning their first song", "A group of eight-year-olds play Twinkle together while their parents do the shopping next door."),
           ("Late afternoon", "Practice that matches school", "A teenager rehearses the piece her school band is learning this term, with a tutor who knows the curriculum."),
           ("Evening", "Rehearsal and recording", "A local band books the rehearsal room and records its first demo.")]
    day_html = B_timeline(day)
    acts = [("Drop-in lessons", "Children, while parents shop or run errands", "Structured 30–60 minute group lessons with a set start and finish, booked or walk-in."),
            ("After-school programme", "School-age students", "Group classes and supervised practice, aligned with what their school is teaching."),
            ("Lessons and practice rooms", "All ages", "Private lessons with tutors, and keyboard rooms hired by the hour."),
            ("Rehearsal and recording", "Bands, choirs, songwriters", "Rooms and a small recording setup, scheduled in adult-only time blocks."),
            ("Community sessions", "Seniors, people with disability, new arrivals, youth groups, carers", "Group piano for wellbeing, social connection and learning, delivered with partner professionals."),
            ("School partnerships", "Local primary and secondary schools", "Schools share their music curriculum, so practice and rehearsal at the centre matches classwork and exams."),
            ("Workshops", "Ages 8–25", "Songwriting and improvisation, from first idea to a finished MIDI, WAV or MP3, plus holiday programmes.")]
    acts_html = "".join(f'<div class="card"><span class="step-label">{esc(w)}</span><span class="h-md" style="font-family:var(--display)">{esc(a)}</span><span class="muted">{esc(d)}</span></div>'
                        for a, w, d in acts)
    why = [("Work for musicians", "University music education students need teaching experience, and graduates need paid work. A centre offers both, and can become an approved placement site."),
           ("Music for every family", "Group lessons in EasyKey cost far less per child than private lessons, and nobody needs a piano at home to start."),
           ("A place to gather", "Seniors, new arrivals, young people and carers share one welcoming space, built around making music together."),
           ("A first home for Civic Credits", "With paid staff, regular families and local shops around it, a centre is a natural place for a small, voluntary credits trial: tutors could take part of their pay in credits, families could pay for lessons with them, and nearby businesses could accept them."),
           ("A testing ground for LifeLink", "Tablets used for lessons, bookings and practice tracking give real users and real feedback before any wider rollout.")]
    why_html = "".join(f'<div class="card"><span class="h-md" style="font-family:var(--display)">{esc(a)}</span><span class="muted">{esc(d)}</span></div>' for a, d in why)
    rules = [("Lessons, not childcare", f'Every centre, in Australia and everywhere else, runs as a music instruction service. Drop-off is always a booked lesson with a set start and finish, a named tutor, and sign-in and sign-out. In Australia, a service "principally conducted to provide instruction in a particular activity", music included, sits outside childcare regulation (<a href="{NEC}">Education and Care Services National Law, s 5</a>). Each new country gets its own legal check first.'),
             ("Screening by role and by time", "Everyone who works with children holds a Blue Card in Queensland, or the local equivalent. Adult-only sessions such as rehearsal and recording are timetabled separately, and the booking system shows who is in the building at any time."),
             ("Partner professionals, trained in EasyKey", "Music therapists, aged-care and disability workers, school music teachers and community leaders work alongside EasyKey staff. They bring their expertise and registrations; EasyKey brings the method, the space and the materials. Sessions are called therapy only when a registered music therapist leads them."),
             ("Smart local sites", "Each site is chosen for space, access and price. All options are open: shopping-centre tenancies, short-term leases on empty shops, council and cultural buildings, libraries, schools after hours, community halls, and spaces shared with music retailers."),
             ("A mixed funding base", "Lesson fees, practice and rehearsal room hire, recording sessions, school partnerships, council and arts grants, funding through partner professionals, and sponsorship.")]
    rules_html = "".join(f'<li><strong>{esc(a)}</strong><span class="muted">{d}</span></li>' for a, d in rules)
    roles = [("Music educator or university department", "Teaching placements and paid work for your students and graduates."),
             ("Therapist, care or youth worker", "Bring EasyKey into your work as a trained partner."),
             ("School", "Share your music curriculum and send students to practise and rehearse."),
             ("Space provider", "Shopping centres, councils, cultural venues and halls with room to offer."),
             ("Music retailer or maker", "Supply keyboards, or sponsor a room."),
             ("Funder or philanthropist", "Back a community music space with a clear social return."),
             ("Volunteer or organiser", "Help build it, wherever you are.")]
    roles_html = "".join(f"""<div class="card"><span class="h-md" style="font-family:var(--display)">{esc(a)}</span><span class="muted">{esc(d)}</span>
<a class="btn btn-outline" style="margin-top:auto;align-self:flex-start" href="{esc(mailto(a))}">Count me in</a></div>""" for a, d in roles)
    path = B_timeline([("Step 1", "A pilot centre in Moreton Bay", "The first centre, in the region where EasyKey was a 2016 innovation awards finalist. It runs for 6 to 12 months and publishes its results."),
                       ("Step 2", "A second site", "Opened from the same operating manual, with what the pilot taught us."),
                       ("Step 3", "Civic Credits and LifeLink trials", "Small, voluntary trials begin once a centre is steady and trusted."),
                       ("Then", "Centres around the world", "Each adapted to local law, in shopping and cultural areas wherever People of the World takes root.")])
    body = f"""{B.header("EasyKey Music", "EasyKey Music Centers", [("EasyKey", "easykey.html", False, None), ("The plan", "builders.html", False, None), ("Count me in", "#join", True, None)])}
<main>
<section class="band door-easykey"><div class="wrap section stack" style="gap:22px">
<p class="crumbs"><a href="easykey.html">EasyKey Music</a></p>
<p class="eyebrow accent">The vision · EasyKey Music Centers</p>
<h1 class="h-xl" style="max-width:900px">Music in the middle of everyday life.</h1>
<p class="lead muted" style="max-width:720px">Walk-in EasyKey music spaces in shopping centres and cultural precincts, where children learn while parents shop, local musicians are paid to teach, and the whole community has a reason to gather.</p>
<p class="note" style="max-width:720px">This is a plan, not something that exists yet. It's here to invite the people who can help build it.</p>
<div class="actions"><a class="btn btn-door" href="#join">Count me in</a><a class="btn btn-ghost" href="#inside">What happens inside</a></div>
</div></section>

<section class="section"><div class="wrap stack" style="gap:28px;max-width:980px">
<div class="stack intro"><h2 class="h-lg">A day in a centre</h2>
<p class="lead muted">One space, used all day by different parts of the community.</p></div>
{day_html}
</div></section>

<section id="inside" class="section band-alt"><div class="wrap stack" style="gap:28px">
<div class="stack intro"><h2 class="h-lg">What happens inside</h2>
<p class="lead muted">Every centre teaches with EasyKey, the written method that shows exactly which keys to press and for how long.</p></div>
<div class="grid grid-3">{acts_html}</div>
</div></section>

<section class="section"><div class="wrap stack" style="gap:28px">
<div class="stack intro"><h2 class="h-lg">Part of something bigger</h2>
<p class="lead muted">The centres are where EasyKey becomes part of <a href="builders.html">the Plan to End Poverty</a>: meaningful work, open access and a trusted local base for its new instruments.</p></div>
<div class="grid grid-2">{why_html}</div>
<p class="muted">Read more about <a href="plan-to-end-poverty/civic-credits/">Civic Credits</a> and <a href="plan-to-end-poverty/lifelink/">LifeLink</a>.</p>
</div></section>

<section class="section band-alt"><div class="wrap stack" style="gap:24px;max-width:980px">
<div class="stack intro"><h2 class="h-lg">How every centre runs</h2>
<p class="lead muted">The same ground rules, wherever a centre opens.</p></div>
<ol class="pathways">{rules_html}</ol>
</div></section>

<section class="section"><div class="wrap stack" style="gap:28px;max-width:980px">
<div class="stack intro"><h2 class="h-lg">How it could begin</h2></div>
{path}
</div></section>

<section id="join" class="section band-alt"><div class="wrap stack" style="gap:28px">
<div class="stack intro"><h2 class="h-lg">Help build the first centre</h2>
<p class="lead muted">No one builds this alone. Choose how you'd like to help, and your email opens with a short note ready to send.</p></div>
<div class="grid grid-3">{roles_html}</div>
<p class="muted">Or write directly: <a href="mailto:{B.CONTACT}">{B.CONTACT}</a>. To give towards the centres, see <a href="support.html">Support the mission</a>.</p>
</div></section>
{B.signup_band("Follow the centres as they grow.", "Occasional news on the pilot, partners and milestones. Unsubscribe any time.", "Send me updates", "easykey-centers", "easykey")}
</main>
{B.footer("easykey")}"""
    desc = "The vision for EasyKey Music Centers: walk-in music spaces in shopping and cultural areas, with lessons, practice, community sessions and paid work for musicians. Help build the first one."
    B.page(URL + "index.html", "EasyKey Music Centers · The vision", desc, body, "easykey")


def B_timeline(rows):
    items = "".join(f'<li><span class="tl-when">{esc(w)}</span><div><strong>{esc(t)}</strong><span class="muted">{esc(d)}</span></div></li>'
                    for w, t, d in rows)
    return f'<ol class="timeline">{items}</ol>'
