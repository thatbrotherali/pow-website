"""Editorial corrections to equations in the Open Library (October 2026), made at the author's request.

The source texts in src/library stay exactly as imported from the author's files; these corrections are applied
when the site is built, and each corrected page lists what was changed in an "Editor's corrections" box.
Original PDFs are left untouched.

Each entry: slug -> {"notes": [plain-language list of changes], "edits": [(old_html, new_html), ...]}.
Every old_html must occur in the page; the build stops if one is missing, so nothing is silently skipped.
"""
import re

D = lambda tex: f'<span class="math display">\\[{tex}\\]</span>'
I = lambda tex: f'<span class="math inline">\\({tex}\\)</span>'

# One shared note: the two senses of "graviton pressure" used across the framework, and how they fit together.
BRIDGE = ("Notation used in the corrections. The framework uses “graviton pressure” in two senses: the static pressure "
          "P, which is lower on the side facing a mass and pushes bodies toward it (a = −∇P/ρ_g), and the inflow (flux) "
          "pressure Π, which is higher near a mass. For a steady inflow they are linked by P = P₀ − Π, where P₀ is the "
          "free-space pressure. Taking P₀ = ½ρ_g c² gives Π/P₀ = 2GM/rc², so the clock rate √(P/P₀) = √(1 − Π/P₀) and the "
          "refractive index n = P₀/P ≈ 1 + Π/P₀ reproduce the measured clock shifts and light deflection. Each equation "
          "below keeps the sense its own text gives it.")

CORR = {}


def fix(slug, notes, edits, bridge=True):
    CORR[slug] = {"notes": ([BRIDGE] if bridge else []) + notes, "edits": edits}


# ---------------------------------------------------------------- From General Relativity to GPT (2025)
fix("from-gr-to-gpt", [
    "Equations 4, 6–8 and 12: a pressure gradient is a force per unit volume, so it is divided by the density of the graviton medium ρ_g to give an acceleration (the form the paper itself uses in equation 21).",
    "Equations 9–11: ρ_g carried through, so the pressure field reads P_g = P₀ − ρ_g GM/r and has the units of pressure.",
    "Equations 14–17: the algebra did not follow (1 − (P₀ − GM/r)/P₀ is GM/P₀r, not 1 − GM/P₀r). With the static pressure lower near a mass, the clock rate is √(P_g/P₀); with P₀ = ½ρ_g c² this gives √(1 − 2GM/rc²), the measured rate. The plain-English note now says time slows where this pressure is lower.",
    "Equation 3: a force is a pressure difference times an area, so F = ΔP·A (pressure times mass has no physical meaning).",
    "Equation 20: the indices did not match (one free index on the left, two on the right). It now proposes a pressure tensor proportional to the stress-energy tensor, with conservation following from ∇_μT^{μν} = 0.",
    "Equations 13, 18, 19 and 23 are GR's tested results. The paper states them rather than derives them from graviton pressure; deriving them is an open task.",
], [
    (D(r"F = -\nabla P_g \tag{2}"), D(r"F = -\frac{m}{\rho_g}\nabla P_g \tag{2}")),
    (D(r"F = P\,\Delta m \tag{3}"), D(r"F = \Delta P\, A \tag{3}")),
    ("where " + I("P") + " represents external graviton pressure, and " + I(r"\Delta m") + " is the mass experiencing the pressure differential.",
     "where " + I(r"\Delta P") + " is the difference in external graviton pressure across the body, and " + I("A") + " is the area it acts on."),
    (D(r"\vec F_g = -\nabla P_g, \quad \text{where } P_g \text{ is the local graviton pressure field.} \tag{4}"),
     D(r"\vec a_g = -\frac{1}{\rho_g}\nabla P_g, \quad \text{where } P_g \text{ is the local graviton pressure and } \rho_g \text{ the density of the graviton medium.} \tag{4}")),
    (D(r"\frac{d\vec p}{dt} = -\nabla P_g \tag{6}"), D(r"\frac{d\vec p}{dt} = -\frac{m}{\rho_g}\nabla P_g \tag{6}")),
    (D(r"\vec F_g = -\nabla P_g \tag{7}"), D(r"\vec F_g = -\frac{m}{\rho_g}\nabla P_g \tag{7}")),
    (D(r"-\nabla P_g = -\frac{GM}{r^2} \tag{8}"), D(r"-\frac{1}{\rho_g}\nabla P_g = -\frac{GM}{r^2}\,\hat r \tag{8}")),
    (D(r"\frac{dP_g}{dr} = \frac{GM}{r^2} \tag{9}"), D(r"\frac{dP_g}{dr} = \frac{\rho_g GM}{r^2} \tag{9}")),
    (D(r"P_g(r) = -\frac{GM}{r} + C \tag{10}"), D(r"P_g(r) = -\frac{\rho_g GM}{r} + C \tag{10}")),
    (D(r"P_g(r) = P_0 - \frac{GM}{r} \tag{11}"), D(r"P_g(r) = P_0 - \frac{\rho_g GM}{r} \tag{11}")),
    (D(r"\vec F_g = -\nabla P_g = -\frac{GM}{r^2} \tag{12}"), D(r"\vec a_g = -\frac{1}{\rho_g}\nabla P_g = -\frac{GM}{r^2}\,\hat r \tag{12}")),
    (D(r"\frac{d\tau}{dt} = \sqrt{1 - \frac{P_g}{P_0}}, \quad \text{where } P_0 \text{ is the graviton pressure in free space.} \tag{14}"),
     D(r"\frac{d\tau}{dt} = \sqrt{\frac{P_g}{P_0}}, \quad \text{where } P_0 \text{ is the graviton pressure in free space.} \tag{14}")),
    ("time slows down in regions where graviton pressure is higher.", "time slows down where this graviton pressure is lower, that is, closer to a mass."),
    ("Substituting " + I(r"P_g(r) = P_0 - \frac{GM}{r}"), "Substituting " + I(r"P_g(r) = P_0 - \frac{\rho_g GM}{r}")),
    (D(r"\frac{d\tau}{dt} = \sqrt{1 - \frac{P_0 - GM/r}{P_0}} \tag{15}"), D(r"\frac{d\tau}{dt} = \sqrt{\frac{P_0 - \rho_g GM/r}{P_0}} \tag{15}")),
    (D(r"\frac{d\tau}{dt} = \sqrt{1 - \frac{GM}{P_0 r}} \tag{16}"), D(r"\frac{d\tau}{dt} = \sqrt{1 - \frac{\rho_g GM}{P_0\, r}} \tag{16}")),
    (D(r"\frac{d\tau}{dt} = \sqrt{1 - \frac{GM}{P_0 r}} \tag{17}"), D(r"\frac{d\tau}{dt} = \sqrt{1 - \frac{2GM}{rc^2}} \quad \text{taking } P_0 = \tfrac{1}{2}\rho_g c^2 \tag{17}")),
    (D(r"\nabla_\mu P^{\mu\nu} = 4\pi G\, T^{\mu\nu} \tag{20}"), D(r"P^{\mu\nu} = \kappa_g\, T^{\mu\nu}, \qquad \nabla_\mu P^{\mu\nu} = 0 \tag{20}")),
    (D(r"v_c^2 = \frac{1}{\rho_g}\nabla P_g\, r \tag{22}"), D(r"v_c^2 = \frac{r}{\rho_g}\left|\nabla P_g\right| \tag{22}")),
])


# ---------------------------------------------------------------- The Unified Framework: Part 5
fix("gpt-part-05", [
    "Subscripts: the source wrote P\\_g with an escaped underscore, so subscripts displayed as literal underscores. They now display as subscripts.",
    "Flow-field force: the divergence of a vector field is a scalar, so it cannot equal a force vector. The flow's divergence now appears as a sink term, and the force comes from the pressure gradient over the body's volume V.",
    "Pressure from flux: pressure is a momentum flux, ρv², not ρv; and the gradient of pressure is a force per unit volume, so it is written as f.",
    "Newtonian sum: the subscripts were garbled in conversion; restored.",
    "Lensing: an angle cannot be a vector dotted with a length; it now uses the size of the density gradient across the path.",
], [
    ("\\_", "_"),
    (D(r"\vec{F}_g = - \nabla \cdot \vec{G}(\vec{r})"), D(r"\nabla \cdot \vec{G}(\vec{r}) = -s(\vec{r}), \qquad \vec{F}_g = -V\,\nabla P_G(\vec{r})")),
    (D(r"\vec{F} = -\nabla P_G(\vec{r}) = -\nabla (\rho_G \cdot v_G)"), D(r"\vec{f} = -\nabla P_G(\vec{r}) = -\nabla \left(\rho_G\, v_G^2\right)")),
    (D(r"\vec{F}*\text{total} = \vec{F}*{12} + \vec{F}*{13} + \vec{F}*{23} + \cdots"), D(r"\vec{F}_\text{total} = \vec{F}_{12} + \vec{F}_{13} + \vec{F}_{23} + \cdots")),
    (D(r"\theta \propto \nabla \rho_G \cdot \ell"), D(r"\theta \propto \left|\nabla_{\perp} \rho_G\right| \ell")),
], bridge=False)

# Part 6: work
fix("gpt-part-06", [
    "Coherence work: force × distance × time has units of joule-seconds, not energy. The integrand now uses the rate of internal adjustment, so W has units of joules.",
], [
    (D(r"W_{GPT} = \int (F_{\text{pressure}} \cdot d_{\text{coherence}})\, dt"), D(r"W_{GPT} = \int F_{\text{pressure}}\, \dot{d}_{\text{coherence}}\, dt")),
    (I(r"d_{\text{coherence}}") + " represents the internal structural adjustment", I(r"\dot{d}_{\text{coherence}}") + " represents the rate of internal structural adjustment"),
], bridge=False)

# Part 7: pressure integral
fix("gpt-part-07", [
    "Net force: a force is not a pressure, and ρv integrated over an area is a mass flow (kg/s), not a force. The force is now the momentum flux ρ(v·n̂)v of the incoming graviton flow integrated over the surface, with ρ_g a density per unit volume.",
], [
    (D(r"F = P_{\text{net}} = \int_{A} (\rho_g \cdot \vec{v_g})\, dA"), D(r"\vec{F} = \int_{A} P_{\text{net}}\,\hat{n}\, dA = \int_{A} \rho_g\, (\vec{v}_g \cdot \hat{n})\, \vec{v}_g\, dA")),
    ("is the density of incident gravitons per unit area", "is the density of the incident graviton flow per unit volume"),
], bridge=False)

# Part 8: GR versus GPT (here P_g is higher near a mass)
fix("gpt-part-08", [
    "In this part P_g is used in the sense that is higher near a mass. On that reading a body is carried toward higher P_g, so the force law and the frame-dragging law now have a plus sign and the density ρ_g that turns a pressure gradient into an acceleration.",
    "Earth and orbit clocks: the ratio was inverted, which would make the ground clock run fast. It is now √(P_orbit/P_Earth) − 1, negative like the GR expression above it.",
    "Refractive index: n ∝ √P_g would vanish far from mass; it is now n = P_g/P₀, which goes to 1 in free space and gives the full measured deflection.",
    "Frame-dragging: a curl needs a vector field; it now uses the graviton flow velocity u_g, so P_g stays a scalar.",
], [
    (D(r"F_{gpt} = -\nabla P_g"), D(r"\vec{a}_{gpt} = \frac{1}{\rho_g}\nabla P_g")),
    (D(r"\Delta t_{GPT} = t \left( \sqrt{\frac{P_{Earth}}{P_{Orbit}}} - 1 \right)"), D(r"\Delta t_{GPT} = t \left( \sqrt{\frac{P_{Orbit}}{P_{Earth}}} - 1 \right)")),
    (D(r"n_g \propto \sqrt{P_g}"), D(r"n_g = \frac{P_g}{P_0}")),
    (D(r"\vec{F}_{\text{gpt}} = -\nabla P_g + \vec{v}_r \times (\nabla \times \vec{P}_g)"), D(r"\vec{a}_{\text{gpt}} = \frac{1}{\rho_g}\nabla P_g + \vec{v}_r \times (\nabla \times \vec{u}_g)")),
    (I(r"\nabla \times \vec{P}_g") + " describes the rotational component of the graviton pressure vector field.",
     I(r"\nabla \times \vec{u}_g") + " describes the rotational component of the graviton flow velocity " + I(r"\vec{u}_g") + "."),
])

# Part 9: rotation curves, lensing (P_g highest at the centre)
fix("gpt-part-09", [
    "Orbital velocity: a pressure gradient divided by a mass is not an acceleration; it is divided by the density ρ_g of the graviton medium, giving v² = r k P₀ e^(−kr)/ρ_g. The fitted values quoted below were reported with the earlier formula and should be re-fitted.",
    "Lensing: with P_g highest at the lens centre, n = 1 + α/P_g would make the index lowest there and bend light outward. The index now rises with pressure, n = 1 + αP_g, and the gradient and delay integrals follow from it.",
], [
    (D(r"v(r) = \sqrt{\frac{r \cdot k P_0 e^{-k r}}{m}}"), D(r"v(r) = \sqrt{\frac{r \cdot k P_0 e^{-k r}}{\rho_g}}")),
    (D(r"v(r) = \sqrt{\frac{r \cdot k P_0 e^{-kr}}{m}}"), D(r"v(r) = \sqrt{\frac{r \cdot k P_0 e^{-kr}}{\rho_g}}")),
    (I("m") + ": Mass of the orbiting star (or test particle).", I(r"\rho_g") + ": density of the graviton medium (turns the pressure gradient into an acceleration)."),
    (D(r"n_g(r) = 1 + \frac{\alpha}{P_g(r)}"), D(r"n_g(r) = 1 + \alpha P_g(r)")),
    (D(r"n_g(r) = 1 + \frac{\alpha}{P_g(r)} = 1 + \frac{\alpha}{P_0 e^{-kr}} = 1 + \frac{\alpha e^{kr}}{P_0}"), D(r"n_g(r) = 1 + \alpha P_g(r) = 1 + \alpha P_0 e^{-kr}")),
    (D(r"\alpha_{GPT}(r) \approx \int \frac{d n_g(r)}{dr} dr = \int \frac{d}{dr} \left( 1 + \frac{\alpha}{P_g(r)} \right) dr"), D(r"\alpha_{GPT}(r) \approx \int \frac{d n_g(r)}{dr} dr = \int \frac{d}{dr} \left( 1 + \alpha P_g(r) \right) dr")),
    (D(r"\frac{d n_g(r)}{dr} = -\frac{\alpha}{P_g(r)^2} \cdot \frac{dP_g(r)}{dr} = \frac{\alpha k e^{2kr}}{P_0^2}"), D(r"\frac{d n_g(r)}{dr} = \alpha \frac{dP_g(r)}{dr} = -\alpha k P_0 e^{-kr}")),
    (D(r"\Delta t_{GPT} \approx \int \left( n_g(r) - 1 \right) \frac{dr}{c} = \int \frac{\alpha}{P_g(r)} \frac{dr}{c}"), D(r"\Delta t_{GPT} \approx \int \left( n_g(r) - 1 \right) \frac{dr}{c} = \int \alpha P_g(r) \frac{dr}{c}")),
    (D(r"\Delta t_{GPT} = \int \frac{\alpha}{P_0 e^{-kr}} \frac{dr}{c} = \frac{\alpha}{P_0 c} \int e^{kr} dr = \frac{\alpha}{P_0 c k} e^{kr} + C"), D(r"\Delta t_{GPT} = \int \alpha P_0 e^{-kr} \frac{dr}{c} = \frac{\alpha P_0}{c} \int e^{-kr} dr = -\frac{\alpha P_0}{c k} e^{-kr} + C")),
    ("Shows how light bends more strongly where pressure is low (field gradient is high).", "Shows how light bends more strongly where pressure and its gradient are high."),
], bridge=False)

# Part 10: light, time (P_g rises toward the mass)
fix("gpt-part-10", [
    "Lensing integral: for a radially varying index the deflection is −2b∫(dn/dr) dr / (r√(r²−b²)); the factor 2b/r was missing.",
], [
    (D(r"\Theta \approx \int_{r_0}^{r_f} \frac{\partial n_g(r)}{\partial r} \cdot \frac{dr}{\sqrt{r^2 - b^2}}"), D(r"\Theta \approx -2b\int_{r_0}^{r_f} \frac{\partial n_g(r)}{\partial r} \, \frac{dr}{r\sqrt{r^2 - b^2}}")),
], bridge=False)

# Part 15
fix("gpt-part-15", [
    "Graviton pressure: pressure is a momentum flux, ρ_g v_g², as this part itself writes later (ΔP_g = ρ_g v_g²); ρ_g v_g alone is a momentum density.",
], [
    (D(r"a = -\frac{\nabla P_g}{\rho_{\text{imp}}}, \quad P_g = \rho_g \cdot v_g,"), D(r"a = -\frac{\nabla P_g}{\rho_{\text{imp}}}, \quad P_g = \rho_g \cdot v_g^2,")),
], bridge=False)

# Part 19
fix("gpt-part-19", [
    "Units: a change of 5–10 micro-g would be about 10⁻⁴ m/s². The figure in brackets, about 10⁻⁸ m/s², corresponds to microgals, so the unit now reads μGal.",
], [
    (D(r"\Delta g \approx 5 - 10 \, \mu g \quad (\sim 10^{-8} \, \mathrm{m/s^2})"), D(r"\Delta g \approx 5 - 10 \, \mu\mathrm{Gal} \quad (\sim 5\text{–}10 \times 10^{-8} \, \mathrm{m/s^2})")),
], bridge=False)

# Part 21
fix("gpt-part-21", [
    "Induced voltage: integrating a pressure gradient along a path gives a pressure difference (pascals), not volts, so a coupling constant κ_V (volts per pascal) is needed.",
], [
    (D(r"V = \int_{0}^{\ell} \nabla P_g \cdot d\vec{r}"), D(r"V = \kappa_V \int_{0}^{\ell} \nabla P_g \cdot d\vec{r} = \kappa_V\, \Delta P_g")),
    ("This expression quantifies electromagnetic induction", "Here " + I(r"\kappa_V") + " is a coupling constant (volts per pascal). This expression quantifies electromagnetic induction"),
], bridge=False)

# Part 23: the mathematical foundation (static pressure: bodies move toward lower P_g)
fix("gpt-part-23", [
    "Force law: m∇P_g has units of kg·N/m³, not newtons. A pressure gradient is a force per unit volume, so the acceleration is a = −∇P_g/ρ_g and the force F = −(m/ρ_g)∇P_g. The orbital and dimensional statements now follow this.",
    "Clock rate: in this part bodies move toward lower P_g, so P_g is lower near a mass and the clock rate is √(P_g/P₀); written as √(1 − P_g/P₀) clocks would run fastest in free space. The exponential form gave e⁻¹ in free space instead of 1; it now matches.",
    "Redshift: Δλ/λ₀ = √(P_g/P₀) would give a 100% shift with no field. It is now √(P₀/P_g) − 1, which is zero without a field and positive for light climbing out.",
    "Light deflection: dividing by photon energy gave the wrong units, and the gradient along the path does not bend a ray. The deflection now uses the gradient across the path of the index n = P₀/P_g.",
], [
    (D(r"\vec{F} = -m \cdot \nabla P_g"), D(r"\vec{F} = -\frac{m}{\rho_g} \nabla P_g")),
    (D(r"m \cdot a = -m \cdot \nabla P_g \quad \Rightarrow \quad a = -\nabla P_g"), D(r"m \cdot a = -\frac{m}{\rho_g} \nabla P_g \quad \Rightarrow \quad a = -\frac{1}{\rho_g}\nabla P_g")),
    (D(r"\frac{v^2}{r} = \left| \nabla P_g \right|"), D(r"\frac{v^2}{r} = \frac{1}{\rho_g}\left| \nabla P_g \right|")),
    (D(r"d\tau = dt \cdot \sqrt{1 - \frac{P_g}{P_0}}"), D(r"d\tau = dt \cdot \sqrt{\frac{P_g}{P_0}}")),
    (D(r"d\tau = dt \cdot \sqrt{1 - \frac{P_g(t)}{P_0}}"), D(r"d\tau = dt \cdot \sqrt{\frac{P_g(t)}{P_0}}")),
    (D(r"\frac{d\tau}{dt} = \exp\left(-\frac{P_g}{P_0}\right)"), D(r"\frac{d\tau}{dt} = \sqrt{\frac{P_g}{P_0}} \approx \exp\left(-\frac{P_0 - P_g}{2P_0}\right)")),
    (D(r"\frac{\Delta \lambda}{\lambda_0} = \sqrt{\frac{P_g}{P_0}}"), D(r"\frac{\Delta \lambda}{\lambda_0} = \sqrt{\frac{P_0}{P_g}} - 1")),
    (D(r"\Delta \theta = \int \frac{1}{E} \left( \nabla P_g \cdot \hat{n} \right) \, ds"), D(r"\Delta \theta = \int \left| \nabla_{\perp}\, \frac{P_0}{P_g} \right| ds")),
    ("<li><p>" + I("E") + " = photon energy</p></li>", "<li><p>" + I(r"\nabla_{\perp}") + " = gradient across the photon's path (the index is " + I(r"n = P_0/P_g") + ")</p></li>"),
    (D(r"\vec{k}_{\text{new}} = \vec{k}_{\text{initial}} + \int \frac{1}{E} \left( \nabla P_g \times \vec{v}_{\gamma} \right) ds"), D(r"\vec{k}_{\text{new}} = \vec{k}_{\text{initial}} + \left|\vec{k}\right| \int \nabla_{\perp}\!\left(\frac{P_0}{P_g}\right) ds")),
    ("and the cross product reflects lateral redirection due to structured anisotropy.", "and the perpendicular gradient of the index turns the wave vector sideways."),
    ("and the force vector " + I(r"\vec{F} = -m \cdot \nabla P_g") + " thus has units of N, as expected.",
     "the acceleration " + I(r"a = -\nabla P_g/\rho_g") + " has units of m/s² (with " + I(r"\rho_g") + " in kg/m³), and the force " + I(r"\vec{F} = -(m/\rho_g)\nabla P_g") + " has units of N, as expected."),
])

# Part 24: units
fix("gpt-part-24", [
    "Units of graviton torque: a torque is a force times a distance (N·m = kg·m²/s²), which is pressure times volume, not pressure times length.",
    "Units of the resonance feedback coefficient: kg·m²/s is pressure × time × volume; pressure × time × distance would be kg/s.",
    "Still open: Cres is given units of pressure per volume here but defined as gp/ρ_coh (which would make it a volume), and Part 28 treats it as a pressure. One definition needs to be chosen across Parts 24 and 28.",
], [
    (D(r"= gp \cdot \text{length} = \frac{\text{kg} \cdot \text{m}^2}{\text{s}^2}"), D(r"= gp \cdot \text{volume} = \frac{\text{kg} \cdot \text{m}^2}{\text{s}^2}")),
    (D(r"= gp \cdot \text{time} \cdot \text{distance} = \frac{\text{kg} \cdot \text{m}^2}{\text{s}}"), D(r"= gp \cdot \text{time} \cdot \text{volume} = \frac{\text{kg} \cdot \text{m}^2}{\text{s}}")),
], bridge=False)

# Part 25
fix("gpt-part-25", [
    "Field equation: the left side has units of pressure per area, so the source cannot be a density alone. With P_g in the sense that is higher near a mass, the Newtonian limit requires ∇²P_g = −4πG ρ_g ρ_m, where ρ_m is the mass density and ρ_g the density of the graviton medium. The units of α become m²/N.",
    "Unit conversion: P₀/κ_g has units of N/m when κ_g is in m⁻¹, so it cannot be in N/m². The GPT pressure unit is now P₀ itself.",
], [
    (D(r"\nabla^2 P_g + \alpha \left( \nabla P_g \cdot \nabla P_g \right) = -\rho_g"), D(r"\nabla^2 P_g + \alpha \left( \nabla P_g \cdot \nabla P_g \right) = -4\pi G\, \rho_g\, \rho_m")),
    (I(r"\rho_g") + ' is local mass <a href="#fn2" class="footnote-ref" id="fnref2" role="doc-noteref"><sup>2</sup></a>-coherence density',
     I(r"\rho_m") + ' is the local mass <a href="#fn2" class="footnote-ref" id="fnref2" role="doc-noteref"><sup>2</sup></a>-coherence density and ' + I(r"\rho_g") + " the density of the graviton medium"),
    ("Governs field reinforcement curvature, units: m" + I("^3") + "/N", "Governs field reinforcement curvature, units: m" + I("^2") + "/N"),
    (I("10^{-7}") + " m" + I("^3") + "/N in resonance-sensitive materials", I("10^{-7}") + " m" + I("^2") + "/N in resonance-sensitive materials"),
    (D(r"1\ \text{GPT-pressure unit} = \frac{P_0}{\kappa_g} \quad \text{(in N/m$^2$)}"), D(r"1\ \text{GPT-pressure unit} = P_0 \quad \text{(in N/m}^2\text{)}")),
], bridge=False)

# Part 26: orbits (P_g highest at the centre; bodies are carried toward higher P_g)
fix("gpt-part-26", [
    "Orbits: a pressure gradient is a force per unit volume, so dividing by the density ρ_g of the graviton medium gives the acceleration; equating it to mv²/r mixed a force density with a force. The orbital velocity is now v = √(r k P₀ e^(−kr)/ρ_g), directed toward the centre where P_g is highest.",
    "Escape: the integral of a pressure over distance is not an energy. The escape condition now integrates the acceleration: ½v² ≥ (P₀/ρ_g) e^(−kr).",
    "Refractive index: with P_g highest near the mass, n = 1 + α/P_g would be lowest there; it is now n = 1 + αP_g.",
    "Spin–orbit ratio: C_rΩ has units of velocity, not angular momentum. With C_r read as the radius of gyration, I = mC_r², so L_f = mC_r²Ω and κ = C_r²Ω/(vr), which is dimensionless.",
], [
    (D(r"n_g(r) = 1 + \frac{\alpha}{P_g(r)}"), D(r"n_g(r) = 1 + \alpha P_g(r)")),
    (D(r"a(r) = -\nabla P_g(r) = k P_0 e^{-k r}"), D(r"a(r) = \frac{1}{\rho_g}\left|\nabla P_g(r)\right| = \frac{k P_0 e^{-k r}}{\rho_g} \quad (\text{toward the centre})")),
    (D(r"L_f = C_r \cdot \Omega"), D(r"L_f = m\, C_r^2\, \Omega")),
    (D(r"\nabla P_g(r) = k P_0 e^{-k r} = \frac{m v^2}{r}"), D(r"\frac{1}{\rho_g}\left|\nabla P_g(r)\right| = \frac{k P_0 e^{-k r}}{\rho_g} = \frac{v^2}{r}")),
    ("and " + I("m") + " is the orbiting body’s mass.", "and " + I(r"\rho_g") + " is the density of the graviton medium."),
    (D(r"\kappa = \frac{L_s}{L_o} = \frac{I \omega}{m v r} = \frac{C_r \Omega}{m v r}"), D(r"\kappa = \frac{L_s}{L_o} = \frac{I \omega}{m v r} = \frac{C_r^2 \Omega}{v r}")),
    (D(r"F_{\text{orb}} = -\nabla P_g(r) = k P_0 e^{-k r}"), D(r"a_{\text{orb}} = \frac{1}{\rho_g}\left|\nabla P_g(r)\right| = \frac{k P_0 e^{-k r}}{\rho_g}")),
    (D(r"ma = \frac{mv^2}{r} = k P_0 e^{-k r}"), D(r"a = \frac{v^2}{r} = \frac{k P_0 e^{-k r}}{\rho_g}")),
    (D(r"v(r) = \sqrt{r \cdot k P_0 e^{-k r} / m}"), D(r"v(r) = \sqrt{r \cdot k P_0 e^{-k r} / \rho_g}")),
    (D(r"E_k = \frac{1}{2} m v^2 \geq \int_{r}^{\infty} P_g(r) \, dr = \frac{P_0}{k} e^{-k r}"), D(r"\frac{1}{2} v^2 \geq \int_{r}^{\infty} a(r') \, dr' = \frac{P_0}{\rho_g} e^{-k r}")),
    (D(r"v_{\text{escape}}(r) = \sqrt{\frac{2P_0}{k m} e^{-k r}}"), D(r"v_{\text{escape}}(r) = \sqrt{\frac{2P_0}{\rho_g} e^{-k r}}")),
], bridge=False)


# Part 27 and Transitional Mechanics (same mechanics section)
_mech_notes = [
    "Contact force: A·∇P_g/ρ does not have units of force. A pressure acting on a body gives a force equal to the pressure difference across it times the area, or equivalently the volume times the gradient: F = A·ΔP_g = V|∇P_g|.",
]
_mech_edits = [
    (D(r"P_g = \frac{F_{\text{net}}}{A} \rightarrow F_{\text{GPT}} = A \cdot P_g = A \cdot \frac{\nabla P_g}{\rho}"), D(r"P_g = \frac{F_{\text{net}}}{A} \rightarrow F_{\text{GPT}} = A \cdot \Delta P_g = V \left|\nabla P_g\right|")),
    ("<li><p>" + I(r"\rho") + " is local graviton permeability (inverse coherence density)</p></li>", "<li><p>" + I("V") + " is the volume of the body and " + I(r"\Delta P_g") + " the pressure difference across it</p></li>"),
]
fix("transitional-mechanics", _mech_notes, _mech_edits, bridge=False)
fix("gpt-part-27", _mech_notes + [
    "Friction, tension and work: a pressure gradient times a dimensionless factor is not a force, and the integral of a gradient over distance is a pressure, not an energy. Each now includes the volume or length the gradient acts over.",
], _mech_edits + [
    (D(r"F_{\text{friction}} = \mu \cdot \nabla_{\parallel} P_g"), D(r"F_{\text{friction}} = \mu \, V_c \, \nabla_{\parallel} P_g")),
    ("is the local coherence-interference factor along the contact plane, and", "is the local coherence-interference factor along the contact plane, " + I("V_c") + " is the volume of the contact layer, and"),
    (D(r"F_{\text{tension}} = -\frac{\partial P_g}{\partial r} \cdot A"), D(r"F_{\text{tension}} = -\frac{\partial P_g}{\partial r} \cdot A\, \ell")),
    ("is the cross-sectional area of the strand, and", "is the cross-sectional area of the strand, " + I(r"\ell") + " its length, and"),
    (D(r"W = \int F \cdot dx = \int \nabla P_g \cdot dx"), D(r"W = \int F \cdot dx = \int V\, \nabla P_g \cdot dx")),
], bridge=False)

# Part 28
fix("gpt-part-28", [
    "Units of the electric field: if E = −∇gp, its units are those of a pressure gradient, kg/(m²·s²), not of a pressure.",
    "Still open: the unit table in this part (resistance, capacitance, EM velocity, impedance) depends on how Cres and R_field are defined, and those definitions differ from Part 24. A single set of definitions is needed before the derived units can be checked.",
], [
    (I(r"[E] = \text{kg} / (\text{m} \cdot \text{s}^2)"), I(r"[E] = \text{kg} / (\text{m}^2 \cdot \text{s}^2)")),
    ('<td style="text-align: left;">' + I(r"-\nabla gp") + '</td>\n<td style="text-align: left;">' + I(r"\text{kg} / (\text{m} \cdot \text{s}^2)") + "</td>",
     '<td style="text-align: left;">' + I(r"-\nabla gp") + '</td>\n<td style="text-align: left;">' + I(r"\text{kg} / (\text{m}^2 \cdot \text{s}^2)") + "</td>"),
], bridge=False)


# Structure Before Uncertainty: equations pasted as rendered text (three copies run together); restored as typeset maths
SBU_TEX = [r"\mathcal{U} = \frac{\kappa}{2}\,|\nabla \psi|^2", r"U = \int \mathcal{U}\,dV", r"U_{12}(r)\propto \frac{q_1q_2}{r}",
           r"F(r) = -\frac{dU_{12}}{dr}\propto \frac{q_1q_2}{r^2}", r"\sigma_q(\mathbf{x},t)",
           r"\frac{\partial \psi}{\partial t} + \mathbf{V}\cdot \nabla \psi = D\nabla^2 \psi - \alpha\,\sigma_q", r"\mathbf{A}",
           r"\nabla^2 \mathbf{A} = -\beta\,\mathbf{J}_q", r"\mathbf{J}_q = \sigma_q\mathbf{v}", r"\beta", r"\mathbf{b} \equiv \nabla \times \mathbf{A}",
           r"\mathbf{b}", r"\mathbf{F} \propto q(\mathbf{e} + \mathbf{v}\times \mathbf{b})", "q = q(s)", r"V(s)=a(s^2-s_0^2)^2", r"s=\pm s_0", r"q=\pm q_0",
           r"V_{\text{int}} = -\lambda\,s\,\psi(\mathbf{x}_\text{obj})", r"\epsilon_0", r"\mu_0", r"\psi", r"-\nabla\psi"]
fix("structure-before-uncertainty", [
    "Several equations had been pasted as rendered text, so each appeared three times run together. They are now typeset once. The equations themselves were sound.",
    "Flux constancy: the divergence theorem over a ball containing the exchanger would not give zero. Over the shell between r₀ and r it gives Φ(r) − Φ(r₀) = 0, which is what makes the flux constant, as the next sentence says.",
], [
    ("0 = ∫_V ∇·(ρ_g u) dV = ∫_S ρ_g u · dA = Φ(r)", "0 = ∫_V ∇·(ρ_g u) dV = Φ(r) − Φ(r₀), where V is the shell between r₀ and r"),
    ("@katex", SBU_TEX),
    ("For two bias sources q1q_1q1\u200b and q2q_2q2\u200b, the cross term in UUU", "For two bias sources " + I("q_1") + " and " + I("q_2") + ", the cross term in " + I("U")),
    ("order parameter sss (", "order parameter " + I("s") + " ("),
    ("If q1q2&lt;0q_1q_2&lt;0q1\u200bq2\u200b&lt;0, UUU decreases as rrr decreases", "If " + I("q_1q_2&lt;0") + ", " + I("U") + " decreases as " + I("r") + " decreases"),
    ("If q1q2&gt;0q_1q_2&gt;0q1\u200bq2\u200b&gt;0, UUU increases as rrr decreases", "If " + I("q_1q_2&gt;0") + ", " + I("U") + " increases as " + I("r") + " decreases"),
], bridge=False)


# ---------------------------------------------------------------- The Reduction Conflation
fix("reduction-conflation", [
    "Spinal load (Newtonian ontology, Claim 3 and the composite stress): ∫ρg dz over height is already a pressure, so it is not a force, and dividing it by the area again gave pascals per square metre. The load is now F(z) = ∫ρ(z′) g A(z′) dz′ and the stress σ(z) = F(z)/A(z). Cosmetic: the argument is unchanged.",
    "Metabolic cost: integrating force over time gives a total energy, not a rate, so the left side is now E_metabolic(T) rather than Ė. Cosmetic.",
    "Vacuum energy: the Planck cutoff is a wavenumber, k_max = 1/ℓ_P, not a mass, and the zero-point sum is of order the Planck density c⁵/ħG² (about 5 × 10⁹³ g/cm³); c³/ħG² is not a density. The '120 orders of magnitude' discrepancy stands.",
    "Two logic displays contradicted their sentences. After “It does NOT show:” the display now reads Derive(GR → N) ⟹ O_GR ∼ O_N (the inference that is not shown). After “the Reduction Conflation converts this … into an ontological equivalence”, the display now shows that equivalence (≡), labelled as the unlicensed step. The argument is unchanged.",
], [
    (r"&amp;F_{\text{compressive}}(z) = \int_z^H \rho(z&#39;) g \, dz&#39; \quad",
     r"&amp;F_{\text{compressive}}(z) = \int_z^H \rho(z&#39;)\, g\, A(z&#39;) \, dz&#39; \quad"),
    (r"\sigma(z) = \frac{1}{A(z)}\int_z^H \rho(z&#39;)g\,dz&#39; \quad",
     r"\sigma(z) = \frac{1}{A(z)}\int_z^H \rho(z&#39;)\,g\,A(z&#39;)\,dz&#39; \quad"),
    (r"\sigma_{\text{comp}}(z) = \frac{1}{A(z)} \int_z^H \rho(z&#39;)\,g(z&#39;) \,dz&#39;",
     r"\sigma_{\text{comp}}(z) = \frac{1}{A(z)} \int_z^H \rho(z&#39;)\,g(z&#39;)\,A(z&#39;) \,dz&#39;"),
    (r"\dot{E}_{\text{metabolic}} = k_{\text{metabolic}} \int_0^T", r"E_{\text{metabolic}}(T) = k_{\text{metabolic}} \int_0^T"),
    (I(r"k_{\text{max}} = M_{\text{Planck}}"), I(r"k_{\text{max}} = 1/\ell_{\text{P}}")),
    (r"\approx \frac{c^3}{\hbar G^2} \approx 10^{92}\,\text{g/cm}^3", r"\sim \frac{c^5}{\hbar G^2} \approx 5\times 10^{93}\,\text{g/cm}^3"),
    (r"\text{Derive}(\text{GR} \to \text{N}) \kern-0.8em\not\implies \mathcal{O}_{\text{GR}} \sim \mathcal{O}_{\text{N}}",
     r"\text{Derive}(\text{GR} \to \text{N}) \implies \mathcal{O}_{\text{GR}} \sim \mathcal{O}_{\text{N}}"),
    (r"\text{Full Causal Chain}\vert_{\text{Scenario A}} \kern-0.8em\not\equiv \text{Full Causal Chain}",
     r"\text{Full Causal Chain}\vert_{\text{Scenario A}} \equiv \text{Full Causal Chain}"),
], bridge=False)


# ---------------------------------------------------------------- The Mechanics of the Medium
fix("mechanics-of-the-medium", [
    "Surface condition (Section 10): a draft line offering two guesses with a question mark is now shown as the naive guess g ≟ v²/R, which the next paragraph corrects.",
    "Coupling k: the inflow slows with distance, so dv/dr = −k/r with k > 0 (k has units of speed), and a = −v dv/dr = kv/r is positive inward. Since v = √(2GM/r), k = v/2 at each radius rather than a single constant; at the surface this gives the paper's k = √(gR/2).",
    "Velocity profile: for an inward acceleration GM/r², v dv/dr = −GM/r², which integrates to ½v² = GM/r + C. With the original sign ½v² = −GM/r, so v² would be negative; the result v = √(2GM/r) is unchanged.",
    "Pressure from flow (Section 11): with P ∝ ρv² the pressure would be highest near the mass and the force −V∇P would push outward. The text itself says pressure increases with distance, which is the static (Bernoulli) pressure P_g = P₀ − ½ρ_g v². Its gradient is ρ_g GM/r² outward, so the force −V_eff∇P_g points inward and κ = 1/ρ_g. This changes how the force is derived, not the result.",
    "Still open: the paper also says the medium's density rises near a mass and that pressure rises with density (the equation of state). Both cannot hold with a static pressure that falls near the mass. The density perturbation 2GM/c²r used for light and clocks matches the inflow pressure ratio Π/P₀ = v²/c² in the notation note below; one consistent choice is needed.",
    "Light deflection (Sections 14 and 23): the deflection is −∫(dn/dr)(b/r) dx/n; the extra factor 2 would give 8GM/c²b, twice the measured value. The minus sign makes the angle positive (toward the mass). The 1.75″ result stands.",
    "Clock rate from matter waves (Section 25): τ = τ₀ n gives 1 + 2GM/c²r, twice the measured shift, as the text acknowledged. It is now τ = τ₀√n ≈ τ₀(1 + GM/c²r), the same factor as Section 16 and the notation note (clock rate √(P/P₀)).",
    "Charge (Sections 17–18): the energy of two charges' interaction is the cross term κ∫∇ψ₁·∇ψ₂ dV, not the whole field energy (which includes each charge's self-energy). In the Gauss's-law step, 4πr²·C/r² is +4πC, so C = −αq/4π; the final ψ = αq/4πr is unchanged.",
    "Waves (Section 22): the vector-potential equation had the source with the wrong sign relative to Section 19; it is now ∇²A = −βJ + (1/c²)∂²A/∂t². And 1/(ε₀μ₀) is 1 over the product of compressibility and stiffness, not their ratio.",
    "Laplace resonance: Io, Europa and Ganymede orbit with frequencies in the ratio 4 : 2 : 1 (their periods are 1 : 2 : 4).",
    "Lensing (Section 24): for a circularly symmetric lens the deflection is 4GM(<ξ)/c²ξ, using the mass inside ξ, not an integral of M/ξ. Shear comes from the second derivatives of the lensing potential ψ_L ∝ ∫(n − 1) dz, not from its gradient.",
    "Cosmology (Section 27): acceleration needs P_g < −⅓ρ_g c²; at exactly −⅓ρ_g c² the expansion coasts. Λ has units of 1/m², so (1/c²)∇·u (units s/m²) cannot be Λ; the dimensionally consistent form is Λ_eff = (∇·u)²/3c² = 3H²/c², the de Sitter relation. This changes the number the paper compares with the observed Λ.",
    "Appendix B: the cross-section κ/(m_atom c²) has units of 1/J, not area, and later steps changed κ from 3 to 2 and γ to 3. With a dimensionless κ the cross-section is σ = κ(ħ/m_atom c)². Because v² = 2gR is used as an input, the condition does not predict g: it fixes σ = m_atom/(2γρ₀R), about 9 × 10⁻⁹ m² for Earth (κ ≈ 2 × 10²³), and that σ depends on the body's radius. A body-independent cross-section is still needed. This changes the appendix's conclusion.",
    "Appendix C: r × (−∇P_g) has units of pressure; a torque needs the volume the gradient acts on, T = r × (−V_eff∇P_g), in N·m (gp·m³).",
    "Appendix F: with coupling terms −ασψ and βJ·A the variations gave ∇²ψ = −(α/ε₀)σ, which with α = 1/ε₀ is not Section 19's equation; the couplings are now −σψ + J·A. The wave term in the Ampère-like equation had the wrong sign (the original is not a wave equation); the electric energy now includes ∂A/∂t so it follows from the Lagrangian.",
    "Cosmetic: the graviton flux is written Φ_flux so it is not confused with the potential Φ, and the order term on ρ_g is placed inside the bracket.",
], [
    (D(r"g = \frac{v(R)^2}{R} \quad \text{or} \quad g = \frac{v(R)^2}{kR} ?"), D(r"g \stackrel{?}{=} \frac{v(R)^2}{R}")),
    (D(r"\frac{dv}{dr} = \frac{k}{r}"), D(r"\frac{dv}{dr} = -\frac{k}{r}, \qquad k > 0")),
    (D(r"a = -v \cdot \frac{k}{r} = -\frac{k v}{r}"), D(r"a = -v \cdot \left(-\frac{k}{r}\right) = \frac{k v}{r}")),
    (D(r"v \frac{dv}{dr} = \frac{GM}{r^2}"), D(r"v \frac{dv}{dr} = -\frac{GM}{r^2}")),
    (D(r"\int v \, dv = GM \int \frac{dr}{r^2} \quad \Rightarrow \quad \frac{1}{2} v^2 = -\frac{GM}{r} + C"),
     D(r"\int v \, dv = -GM \int \frac{dr}{r^2} \quad \Rightarrow \quad \frac{1}{2} v^2 = \frac{GM}{r} + C")),
    ("but the product " + I(r"r^2 v(r)") + " tends to a constant.", "but the product " + I(r"r^2 v(r)") + " would have to tend to a constant."),
    (D(r"\rho_g(r) = \rho_0 \left(1 + \frac{2GM}{c^2 r}\right) + \mathcal{O}\left(\frac{GM}{c^2 r}\right)^2"),
     D(r"\rho_g(r) = \rho_0 \left(1 + \frac{2GM}{c^2 r} + \mathcal{O}\left(\frac{GM}{c^2 r}\right)^2\right)")),
    (D(r"P_g \propto \rho_g v^2 + P_{\text{self}}"), D(r"P_g \approx P_0 - \tfrac{1}{2}\rho_g v^2 = P_0 - \frac{\rho_g GM}{r}")),
    ("where " + I(r"P_{\text{self}}") + " is the contribution from graviton-graviton self-repulsion.",
     "where " + I("P_0") + " is the free-space pressure maintained by graviton–graviton self-repulsion, and the inflow lowers it by " + I(r"\tfrac{1}{2}\rho_g v^2") + " (Bernoulli)."),
    (D(r"\nabla P_g = \frac{dP_g}{dr} \hat{\mathbf{r}} \propto \frac{GM}{r^2} \hat{\mathbf{r}}"), D(r"\nabla P_g = \frac{dP_g}{dr} \hat{\mathbf{r}} = \frac{\rho_g GM}{r^2} \hat{\mathbf{r}}")),
    ("The gradient points radially inward—pressure increases", "The gradient points radially outward—pressure increases"),
    (D(r"\nabla \Phi = \kappa \nabla P_g"), D(r"\nabla \Phi = \kappa \nabla P_g, \qquad \kappa = \frac{1}{\rho_g}")),
    (D(r"\Phi = 4\pi r^2 \rho_g v(r)"), D(r"\Phi_{\text{flux}} = 4\pi r^2 \rho_g v(r)")),
    (r"\omega_1 : \omega_2 : \omega_3 = 1 : 2 : 4 \quad", r"\omega_{\text{Io}} : \omega_{\text{Europa}} : \omega_{\text{Ganymede}} = 4 : 2 : 1 \quad"),
    (D(r"\alpha = 2 \int_{-\infty}^{\infty} \frac{1}{n} \frac{dn}{dr} \frac{b}{r} \, dx"), D(r"\alpha = -\int_{-\infty}^{\infty} \frac{1}{n} \frac{dn}{dr} \frac{b}{r} \, dx")),
    (D(r"\alpha = 2 \int_{-\infty}^{\infty} \frac{1}{1 + 2GM/(c^2 r)} \cdot \frac{-2GM}{c^2 r^2} \cdot \frac{b}{r} \, dx"),
     D(r"\alpha = -\int_{-\infty}^{\infty} \frac{1}{1 + 2GM/(c^2 r)} \cdot \frac{-2GM}{c^2 r^2} \cdot \frac{b}{r} \, dx")),
    (D(r"U_{12}(r) = \int \frac{\kappa}{2} |\nabla \psi|^2 dV = \frac{1}{4\pi\epsilon_0} \frac{q_1 q_2}{r}"),
     D(r"U_{12}(r) = \kappa \int \nabla \psi_1 \cdot \nabla \psi_2 \, dV = \frac{1}{4\pi\epsilon_0} \frac{q_1 q_2}{r}")),
    (D(r"\oint \nabla \psi \cdot d\mathbf{A} = 4\pi r^2 \frac{d\psi}{dr} = -4\pi C = -\alpha q"), D(r"\oint \nabla \psi \cdot d\mathbf{A} = 4\pi r^2 \frac{d\psi}{dr} = 4\pi C = -\alpha q")),
    ("Thus " + I(r"C = \alpha q/(4\pi)") + ", and:", "Thus " + I(r"C = -\alpha q/(4\pi)") + ", and:"),
    (D(r"\nabla^2 \mathbf{A} = \beta \mathbf{J}_q + \frac{1}{c^2} \frac{\partial^2 \mathbf{A}}{\partial t^2}"), D(r"\nabla^2 \mathbf{A} = -\beta \mathbf{J}_q + \frac{1}{c^2} \frac{\partial^2 \mathbf{A}}{\partial t^2}")),
    (r"= \frac{\text{transverse curl stiffness}}{\text{bias compressibility}}", r"= \frac{1}{(\text{bias compressibility}) \times (\text{transverse curl stiffness})}"),
    (r"\hat{\alpha}(\xi) = \frac{4G}{c^2} \int_0^{\xi} \frac{M(\xi&#39;)}{\xi&#39;} \, d\xi&#39; + \hat{\alpha}_{\text{medium}}(\xi)",
     r"\hat{\alpha}(\xi) = \frac{4G\,M(\xi)}{c^2\,\xi} + \hat{\alpha}_{\text{medium}}(\xi), \qquad M(\xi) = \text{mass within projected radius } \xi"),
    (D(r"\gamma = \frac{1}{2} \int \nabla_\perp n \, dz"),
     D(r"\gamma_1 = \tfrac{1}{2}\left(\partial_1^2 - \partial_2^2\right)\psi_L, \quad \gamma_2 = \partial_1 \partial_2 \psi_L, \qquad \psi_L(\boldsymbol{\theta}) = \frac{D_{ls}}{D_d D_s} \int (n - 1)\, dz")),
    (D(r"\tau(r) = \tau_0 \cdot n(r) \approx \tau_0 \left(1 + \frac{2GM}{c^2 r}\right)"), D(r"\tau(r) = \tau_0 \sqrt{n(r)} \approx \tau_0 \left(1 + \frac{GM}{c^2 r}\right)")),
    (" — the factor of 2 difference is resolved by noting that " + I("n(r)") + " applies to phase velocity, while clock rate depends on group velocity; the detailed derivation yields the correct " + I(r"GM/(c^2 r)") + " coefficient).", ")."),
    (D(r"P_g \approx -\frac{1}{3} \rho_g c^2"), D(r"P_g < -\frac{1}{3} \rho_g c^2")),
    ("This gives " + I(r"\rho_g + 3P_g/c^2 \approx 0") + ", and acceleration emerges from higher-order terms.",
     "This makes " + I(r"\rho_g + 3P_g/c^2 < 0") + ", so " + I(r"\ddot{a} > 0") + ": the expansion accelerates. (At exactly " + I(r"-\tfrac{1}{3}\rho_g c^2") + " it would coast.)"),
    (D(r"\Lambda_{\text{eff}} = \frac{1}{c^2} \nabla \cdot \mathbf{u}_{\text{cosmological}}"), D(r"\Lambda_{\text{eff}} = \frac{\left(\nabla \cdot \mathbf{u}_{\text{cosmological}}\right)^2}{3c^2}")),
    (D(r"\Lambda_{\text{eff}}(t) = \frac{3H(t)}{c^2}"), D(r"\Lambda_{\text{eff}}(t) = \frac{3H(t)^2}{c^2}")),
    (D(r"\sigma = \frac{\kappa}{m_{\text{atom}}} \cdot \frac{1}{c^2}"), D(r"\sigma = \kappa \left(\frac{\hbar}{m_{\text{atom}}\, c}\right)^2")),
    ("The factor " + I(r"1/m_{\text{atom}}") + " ensures that heavier atoms (more nucleons) have larger cross-section.",
     "(" + I(r"\hbar/m_{\text{atom}}c") + " is the atom's reduced Compton wavelength, the only length that can be formed from " + I(r"\hbar") + ", " + I(r"m_{\text{atom}}") + " and " + I("c") + ".)"),
    (D(r"g = \gamma \rho_0 v(R)^2 \frac{1}{m_{\text{atom}}} \cdot \frac{\kappa}{m_{\text{atom}} c^2}"), D(r"g = \gamma \rho_0 v(R)^2 \, \frac{\kappa \hbar^2}{m_{\text{atom}}^3 c^2}")),
    (D(r"\kappa \approx 3"), D(r"\kappa = \frac{m_{\text{atom}}^3 c^2}{2\gamma \rho_0 R \hbar^2} \approx 2 \times 10^{23}")),
    (D(r"\sigma = \frac{3}{m_{\text{atom}} c^2}"), D(r"\sigma = \frac{m_{\text{atom}}}{2\gamma \rho_0 R} \approx 9 \times 10^{-9}\ \text{m}^2")),
    (D(r"g = \gamma \rho_0 v(R)^2 \cdot \frac{3}{m_{\text{atom}}^2 c^2}"), D(r"g = \gamma \rho_0 v(R)^2 \, \frac{\kappa \hbar^2}{m_{\text{atom}}^3 c^2}")),
    (D(r"g = \gamma \rho_0 (2gR) \cdot \frac{3}{m_{\text{atom}}^2 c^2}"), D(r"g = \gamma \rho_0 (2gR) \, \frac{\kappa \hbar^2}{m_{\text{atom}}^3 c^2}")),
    (D(r"1 = \frac{6\gamma \rho_0 R}{m_{\text{atom}}^2 c^2}"), D(r"1 = \frac{2\gamma \kappa \rho_0 R \hbar^2}{m_{\text{atom}}^3 c^2}")),
    ("the equation is satisfied with " + I(r"\gamma \kappa \approx 3") + ". Taking " + I(r"\gamma = 3/2") + " gives " + I(r"\kappa = 2") + ".",
     "the equation is satisfied with " + I(r"\gamma \kappa \approx 3 \times 10^{23}") + ". Taking " + I(r"\gamma = 3/2") + " gives " + I(r"\kappa \approx 2 \times 10^{23}") + "."),
    (D(r"\sigma = \frac{2}{m_{\text{atom}} c^2}"), D(r"\sigma = \frac{m_{\text{atom}}}{2\gamma \rho_0 R} = \frac{m_{\text{atom}}}{3 \rho_0 R} \approx 9 \times 10^{-9}\ \text{m}^2")),
    (D(r"g = \frac{3\rho_0 v^2}{m_{\text{atom}}} \cdot \frac{2}{m_{\text{atom}} c^2} = \frac{6 \rho_0 v^2}{m_{\text{atom}}^2 c^2}"),
     D(r"g = \frac{3}{2}\rho_0 v^2 \, \frac{\sigma}{m_{\text{atom}}} = \frac{v^2}{2R}")),
    ("The key result is the proportionality: " + I(r"g \propto \rho_0 / m_{\text{atom}}^2") + ". For fixed atomic composition, surface gravity is determined by vacuum density.",
     "Because " + I("v^2 = 2gR") + " was used as an input, this is a consistency condition rather than an independent prediction of " + I("g") + ": it fixes the cross-section per atom, " + I(r"\sigma = m_{\text{atom}}/(3\rho_0 R)") + ", which as written depends on the body's radius. A cross-section that is the same for every body is still needed before this appendix can predict " + I("g") + " from " + I(r"\rho_0") + "."),
    (r"T_{gp} = \vec{r} \times (-\nabla P_g) \quad [\text{gp} \cdot \text{m}]", r"T_{gp} = \vec{r} \times (-V_{\text{eff}}\nabla P_g) \quad [\text{N} \cdot \text{m} = \text{gp} \cdot \text{m}^3]"),
    (r"+ \frac{\epsilon_0}{2} (\nabla \psi)^2 - \frac{1}{2\mu_0} (\nabla \times \mathbf{A})^2 - \alpha \sigma_q \psi + \beta \mathbf{J}_q \cdot \mathbf{A}",
     r"+ \frac{\epsilon_0}{2} \left(\nabla \psi + \frac{\partial \mathbf{A}}{\partial t}\right)^2 - \frac{1}{2\mu_0} (\nabla \times \mathbf{A})^2 - \sigma_q \psi + \mathbf{J}_q \cdot \mathbf{A}"),
    (D(r"\nabla^2 \psi = -\frac{\alpha}{\epsilon_0} \sigma_q"), D(r"\nabla^2 \psi = -\frac{\sigma_q}{\epsilon_0} = -\alpha\, \sigma_q \quad \text{(Coulomb gauge)}")),
    (D(r"\nabla \times (\nabla \times \mathbf{A}) - \frac{1}{c^2} \frac{\partial^2 \mathbf{A}}{\partial t^2} = \mu_0 \mathbf{J}_q"),
     D(r"\nabla \times (\nabla \times \mathbf{A}) + \frac{1}{c^2} \frac{\partial^2 \mathbf{A}}{\partial t^2} = \mu_0 \mathbf{J}_q - \frac{1}{c^2}\frac{\partial}{\partial t}\nabla\psi")),
    (D(r"\nabla^2 \mathbf{A} = -\mu_0 \mathbf{J}_q"), D(r"\nabla^2 \mathbf{A} - \frac{1}{c^2} \frac{\partial^2 \mathbf{A}}{\partial t^2} = -\mu_0 \mathbf{J}_{q,\perp} \quad \text{(transverse part of the current; static limit } \nabla^2 \mathbf{A} = -\mu_0 \mathbf{J}_q \text{)}")),
])


# ---------------------------------------------------------------- Operational Constraints of the EP (re-check)
fix("operational-constraints-of-the-ep", [
    "Light deflection: ∂n/∂b is negative (the index falls away from the mass), so a minus sign makes the bending angle positive, toward the mass. The 4GM/c²b result is unchanged. The rest of the paper's equations check out.",
], [
    (r"\alpha = \int_{-\infty}^{\infty} \frac{\partial n}{\partial b}\, dz", r"\alpha = -\int_{-\infty}^{\infty} \frac{\partial n}{\partial b}\, dz"),
], bridge=False)


def untriple(html, texs):
    """Text pasted from a rendered page reads RENDERED + LaTeX + RENDERED (with zero-width spaces). Keep only the LaTeX, typeset.
    Longest LaTeX first, so short symbols do not match inside longer formulas."""
    for tex in sorted(texs, key=len, reverse=True):
        out, pos = [], 0
        while True:
            i = html.find(tex, pos)
            if i < 0:
                break
            pre, post = html[:i], html[i + len(tex):]
            best = 0
            for L in range(1, min(60, len(post)) + 1):
                tail = post[:L]
                if "<" in tail:
                    break
                cand = tail.replace("\u200b", "").replace("\u2009", "").replace(" ", "")
                prev = re.sub(r"[\u200b\u2009 ]", "", pre[-(L + 40):])
                nxt = post[L:L + 1]
                if cand and prev.endswith(cand) and (nxt in ("", " ", ",", ".", "<", "-", ")", ";", ":")):
                    best = L
            if not best:
                pos = i + len(tex)
                continue
            tail = post[:best]
            cand = tail.replace("\u200b", "").replace("\u2009", "").replace(" ", "")
            # walk back over the rendered prefix, ignoring thin and zero-width spaces
            j, k = i, len(cand)
            while k > 0 and j > 0:
                ch = html[j - 1]
                if ch in "\u200b\u2009 ":
                    j -= 1
                    continue
                if ch != cand[k - 1]:
                    break
                j -= 1; k -= 1
            display = html[:j].endswith("<p>") and post[best:].lstrip(" ").startswith("</p>")
            span = D(tex) if display else I(tex)
            html = html[:j] + span + post[best:]
            pos = j + len(span)
    # whole-paragraph formulas whose rendered copies are reordered (fractions): keep only the LaTeX
    for tex in texs:
        html = re.sub(r"<p>[^<]*?" + re.escape(tex) + r"[^<]*</p>", lambda m: "<p>" + D(tex) + "</p>", html)
    return html


def apply(slug, html):
    """Return (corrected html, notes). Raises if an expected passage is missing."""
    c = CORR.get(slug)
    if not c:
        return html, []
    for old, new in c["edits"]:
        if old == "@katex":
            html = untriple(html, new)
            continue
        n = html.count(old)
        if n == 0:
            raise ValueError(f"corrections: {slug}: passage not found: {old[:90]}")
        html = html.replace(old, new)
    return html, c["notes"]
