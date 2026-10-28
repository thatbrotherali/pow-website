"""An open invitation to researchers exploring space as a medium (graviton-pressure-theory/invitation/).

The research cited here is real and linked; none of it is claimed as support for Graviton Pressure Theory,
and the page says so. Open problems match the papers' own lists.
"""
from urllib.parse import quote

B = None
esc = None
URL = "graviton-pressure-theory/invitation/"
P = "graviton-pressure-theory/papers/"


def mailto(role):
    subject = f"The medium: count me in ({role})"
    body = ("Hi Shareef,\n\nI'd like to take part in the search for the medium.\n\n"
            f"Who I am ({role}):\n\nWhat I'd like to work on or ask about:\n\nBest way to reach me:\n")
    return f"mailto:{B.CONTACT}?subject={quote(subject)}&body={quote(body)}"


def build(b):
    global B, esc
    B, esc = b, b.esc
    S = B.SITE_URL

    field = [
        ("Analogue gravity", "Since William Unruh's 1981 paper, physicists have shown that sound in a flowing fluid obeys the same equations as light near a black hole. In 2016 Jeff Steinhauer reported the quantum analogue of Hawking radiation in a flowing Bose–Einstein condensate.",
         [("Barceló, Liberati and Visser, Analogue Gravity, Living Reviews in Relativity 14, 3 (2011)", "https://www.maths.tcd.ie/EMIS/journals/LRG/Articles/lrr-2011-3/")]),
        ("The universe in a helium droplet", "Grigory Volovik has shown how features of particle physics and gravity emerge in superfluid helium-3, treating the vacuum itself as a kind of quantum liquid.",
         [("G. E. Volovik, The Universe in a Helium Droplet (Oxford University Press, 2003)", "https://academic.oup.com/book/11557")]),
        ("Is spacetime a superfluid?", "Stefano Liberati and Luca Maccione tested whether spacetime could behave as a fluid by checking whether high-energy light from the Crab Nebula loses energy on its way to us. Their answer: if it is a fluid, it must be an almost frictionless superfluid.",
         [("Scientific American: If spacetime were a superfluid…", "https://www.scientificamerican.com/article/superfluid-spacetime-relativity-quantum-physics/")]),
        ("Superfluid dark matter", "Lasha Berezhiani and Justin Khoury propose that dark matter forms a superfluid inside galaxies, whose sound waves produce the extra pull usually attributed to unseen mass.",
         [("Berezhiani and Khoury, Theory of Dark Matter Superfluidity, Physical Review D 92, 103510 (2015)", "https://arxiv.org/abs/1507.01019")]),
        ("The river model", "Andrew Hamilton and Jason Lisle showed that the geometry around a black hole can be pictured exactly as space flowing inward like a river, at the escape speed at every radius.",
         [("Hamilton and Lisle, The river model of black holes, American Journal of Physics 76, 519 (2008)", "https://arxiv.org/abs/gr-qc/0411060")]),
    ]
    field_html = "".join(
        f"""<div class="card"><span class="h-md" style="font-family:var(--display)">{esc(t)}</span><span class="muted">{esc(d)}</span>
<span style="font-size:14px">{' · '.join(f'<a href="{u}" rel="noopener">{esc(n)}</a>' for n, u in refs)}</span></div>""" for t, d, refs in field)

    shared = [("Space is physical", "The vacuum has properties: pressure, a speed limit for waves, the ability to flow. It is not nothing."),
              ("Geometry as a fluid description", "General Relativity's equations can be read as describing how a medium flows, the way the equations of fluid dynamics describe water without naming its molecules."),
              ("The inflow is already in the mathematics", "The Gullstrand–Painlevé form of the Schwarzschild solution, the river model, is an inward flow at the escape speed. Graviton Pressure Theory derives the same flow from one requirement and treats it as real.")]
    adds = [("What touches what", "Every explanation is asked to name its physical interface: what is in contact, and what is exchanged. That question is applied to mainstream physics and to Graviton Pressure Theory alike."),
            ("A mechanism at the atom", "Matter takes in gravitons, sorts them and ejects them in a neutralized state. That cycle is proposed as the interface for weight and for inertia: one coupling, counted twice, which is why the two masses are equal."),
            ("Weight as a push", "The inflow presses matter toward the mass, and the ground pushes back. The Equivalence Principle becomes a consequence: in a rocket and on a planet, the same relative acceleration between matter and medium is at work.")]
    col = lambda rows: "".join(f'<li><strong>{esc(a)}</strong><span class="muted">{esc(c)}</span></li>' for a, c in rows)

    derived = [("Inflow at the escape speed", "v = √(2GM/r) follows from requiring the medium to carry a stationary observer into the floor at g."),
               ("Free fall and Kepler's laws", "Universality of free fall follows from one coupling for weight and inertia; circular orbits and T² ∝ r³ follow from the inflow."),
               ("Clock rates", "A clock's speed through the medium gives General Relativity's gravitational time dilation exactly, and the GPS satellites' net gain of about 38 microseconds a day."),
               ("Light", "Given a refractive index n = 1 + v²/c², the bending of starlight (1.75″ at the Sun) and the Shapiro delay follow, the same for radio and visible light.")]
    derived_html = "".join(f'<li><span class="tag">Derived</span><span><strong>{esc(a)}.</strong> {esc(c)}</span></li>' for a, c in derived)

    problems = [
        ("The medium's equation of state", "Working hypothesis: the count of gravitons rises toward a mass while the active pressure falls, because the inflow mixes with neutralized gravitons that exert no pressure. Needed: an equation of state that produces this, and the background pressure it requires.", P + "operational-constraints-of-the-ep/"),
        ("The coupling at the atom", "The momentum exchanged per second, per unit of impedance, in the intake–sorting–ejection cycle. This is where the mechanism names its interface, and where it can be tested most directly.", P + "operational-constraints-of-the-ep/"),
        ("The refractive index", "Derive n = 1 + v²/c² from the medium's properties, rather than adopt it because it matches observation.", P + "operational-constraints-of-the-ep/"),
        ("Lorentz invariance", "Show that the exchange between matter and medium produces exactly the relativistic contraction and time dilation that hide steady motion through it, in the tradition of Lorentz's own account.", P + "logical-closure-of-the-ep/"),
        ("Shielding", "If matter absorbs part of the flux, it should cast a gravitational shadow. Lunar laser ranging limits any such absorption to about 10⁻²² m²/kg. Show the mechanism stays below that, or produces no shadow.", P + "logical-closure-of-the-ep/"),
        ("Field equations for a moving medium", "Rotation, frame dragging and gravitational waves, written as the dynamics of the medium.", P + "operational-constraints-of-the-ep/"),
        ("An experiment that tells the theories apart", "Every reinterpretation of a known result fits both pictures. The search is for a measurement where they predict different numbers.", "science.html#status"),
    ]
    prob_html = "".join(f"""<li><strong>{esc(t)}</strong><span class="muted">{esc(d)} <a href="{u}">Where it stands →</a></span></li>""" for t, d, u in problems)

    roles = [("Physicist or researcher", "Critique a derivation, or take on one of the open problems."),
             ("Mathematician", "Help turn the mechanism into equations that can be solved and checked."),
             ("Experimentalist", "Design or run a test where the predictions differ."),
             ("Student", "Work through the papers, check the steps, and ask hard questions."),
             ("Science writer or podcaster", "Help people find the conversation about what space is made of.")]
    roles_html = "".join(f"""<div class="card"><span class="h-md" style="font-family:var(--display)">{esc(a)}</span><span class="muted">{esc(d)}</span>
<a class="btn btn-outline" style="margin-top:auto;align-self:flex-start" href="{esc(mailto(a))}">Count me in</a></div>""" for a, d in roles)

    terms = [("Open access", "Every paper is free to read in full, with plain-text copies for people and AI tools. LaTeX sources are available on request."),
             ("Credit where it's due", "Contributions are credited by name, and joint work is co-authored."),
             ("Errors corrected in public", "When a mistake is found, the correction is published with the paper, in an editor's note, so the record stays honest."),
             ("Physics kept separate", "The physics papers make physical claims only. People of the World's philosophical and spiritual writing lives in its own place.")]
    terms_html = "".join(f'<div class="card"><span class="h-md" style="font-family:var(--display)">{esc(a)}</span><span class="muted">{esc(d)}</span></div>' for a, d in terms)

    share_msg = "An open invitation to everyone researching space as a physical medium, from analogue gravity to superfluid vacuum: Graviton Pressure Theory's papers and open problems."
    body = f"""{B.header("Graviton Pressure Theory", "An open invitation", [("Graviton Pressure Theory", "science.html", False, None), ("Start here", "graviton-pressure-theory/", False, None), ("Count me in", "#join", True, None)])}
<main>
<section class="band door-science"><div class="wrap section stack" style="gap:22px">
<p class="crumbs"><a href="science.html">Graviton Pressure Theory</a></p>
<p class="eyebrow accent">An open invitation</p>
<h1 class="h-xl" style="max-width:920px">Is space a medium? Let's find out together.</h1>
<p class="lead muted" style="max-width:720px">A growing number of physicists are asking whether the vacuum behaves like a substance: a fluid, even a superfluid. Graviton Pressure Theory comes to the same question from another direction, by asking what physically touches a falling body. This is an invitation to everyone working on the question to share what we've found, test it hard, and help find the answer.</p>
<div class="actions"><a class="btn btn-door" href="#join">Count me in</a><a class="btn btn-ghost" href="#problems">The open problems</a><button class="btn btn-ghost share-btn" type="button" data-url="{S}/{URL}" data-text="{esc(share_msg)}">Share this invitation</button></div>
<p class="share-note muted" role="status"></p>
</div></section>

<section class="section"><div class="wrap stack" style="gap:28px">
<div class="stack intro"><h2 class="h-lg">You're not alone in asking</h2>
<p class="lead muted">The idea that space is a physical medium is being taken seriously in several fields of mainstream research.</p></div>
<div class="grid grid-2">{field_html}</div>
<p class="muted" style="font-size:15px">These researchers work within their own frameworks. They are listed to show the breadth of the question, not to suggest they support Graviton Pressure Theory.</p>
</div></section>

<section class="section band-alt"><div class="wrap stack" style="gap:28px">
<div class="stack intro"><h2 class="h-lg">Where Graviton Pressure Theory fits</h2>
<p class="lead muted">Common ground first, then what this framework adds to the conversation.</p></div>
<div class="grid grid-2">
<div class="stack" style="gap:14px"><h3 class="h-md">What we share</h3><ol class="pathways">{col(shared)}</ol></div>
<div class="stack" style="gap:14px"><h3 class="h-md">What it adds</h3><ol class="pathways">{col(adds)}</ol></div>
</div>
</div></section>

<section class="section"><div class="wrap" style="display:flex;flex-wrap:wrap;gap:32px 64px;align-items:flex-start">
<div class="stack" style="flex:1 1 340px;min-width:0">
<h2 class="h-lg">What's already worked out</h2>
<p class="lead muted">From one requirement, that the medium carries a stationary observer into the floor at g, the inflow reproduces these results.</p>
<p><a href="{P}operational-constraints-of-the-ep/" style="font-weight:600">Read the derivations →</a></p>
</div>
<ul class="status-list" style="flex:2 1 460px;min-width:0">{derived_html}</ul>
</div></section>

<section id="problems" class="section band-alt"><div class="wrap stack" style="gap:24px;max-width:1000px">
<div class="stack intro"><h2 class="h-lg">The problems we'd like help with</h2>
<p class="lead muted">These are the places where the work goes next. Each one is stated in the papers, with what has been tried.</p></div>
<ol class="pathways">{prob_html}</ol>
</div></section>

<section class="section"><div class="wrap stack" style="gap:28px">
<div class="stack intro"><h2 class="h-lg">How we work</h2></div>
<div class="grid grid-2">{terms_html}</div>
</div></section>

<section id="join" class="section band-alt"><div class="wrap stack" style="gap:28px">
<div class="stack intro"><h2 class="h-lg">Join the search</h2>
<p class="lead muted">Choose how you'd like to take part, and your email opens with a short note ready to send. Criticism is as welcome as collaboration.</p></div>
<div class="grid grid-3">{roles_html}</div>
<p class="muted">Or write directly: <a href="mailto:{B.CONTACT}">{B.CONTACT}</a>. New to the theory? <a href="graviton-pressure-theory/">Start here</a>.</p>
</div></section>
{B.signup_band("Follow the research.", "An email when a new paper, derivation or result is published. Nothing else unless you ask.", "Send me new papers", "science", "science")}
</main>
{B.footer("science")}"""
    desc = "An open invitation to researchers exploring space as a medium, from analogue gravity to superfluid vacuum: what Graviton Pressure Theory has derived, the open problems, and how to take part."
    B.page(URL + "index.html", "An open invitation · Graviton Pressure Theory", desc, body, "science")
