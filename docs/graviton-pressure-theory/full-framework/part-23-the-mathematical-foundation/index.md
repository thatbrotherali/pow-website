# The Mathematical Foundation

*The Equations of the Medium, and What They Reproduce*

By Shareef Ali Rashada

*How to read the marks.* Claims about Graviton Pressure Theory are marked by status. Established claims carry no mark. **\[Argued\]** marks a conclusion this framework argues in detail; **\[Hypothesis\]** a proposal of GPT, not yet tested; **\[Open\]** a question not yet answered. On the web page and in the PDF these appear as solid, dashed and dotted underlines.

# About This Paper

This paper sets out the equations of Graviton Pressure Theory: the flow of the medium into a mass, its pressure, the motion of bodies and of light within it, the slowing of clocks, the effect of rotation, the waves the medium carries, and its scale. Each equation is checked against what is measured, and every other part of the framework cites this one set.

The central result is simple to state. A flowing medium in flat space, with light moving at $c$ through it, and with rods and clocks, which are patterns of the medium, squashed and slowed by the medium streaming through them, reproduces the predictions of General Relativity for a single mass exactly. The numbers that General Relativity calculates from the geometry of spacetime, GPT obtains from the motion of a medium. What General Relativity treats as geometry, GPT treats as what the medium’s streaming does to rods and clocks. This form of the equations is known in the physics literature as the river model,[^1] and the wider study of flows that mimic gravity as analogue gravity;[^2] GPT reads it not as an analogy but as the mechanism.

The paper states, too, what the equations do not yet contain: the derivations still owed are listed with each topic and gathered at the end. Claims are marked by their status, as the key shows.

# The Quantities

Table <a href="#tab:symbols" data-reference-type="ref" data-reference="tab:symbols">1</a> lists the quantities used throughout. All are in SI units; the medium’s pressure is in pascals.

<div id="tab:symbols">

| **Symbol**   | **Meaning**                                                    | **Value or unit**                 |
|:-------------|:---------------------------------------------------------------|:----------------------------------|
| $\mathbf{v}$ | velocity of the medium’s inflow                                | m/s                               |
| $\rho_g$     | density of the medium’s active (pressure-bearing) part         | about $10^{-26}$ kg/m$^3$         |
| $n$          | count density of gravitons (active and neutral)                | m$^{-3}$                          |
| $P$          | active pressure of the medium                                  | Pa                                |
| $P_0$        | active pressure in free space, $\tfrac12\rho_g c^2$            | about $4.5\times10^{-10}$ Pa      |
| $c$          | speed of waves in the medium (light, gravitational waves)      | $2.998\times10^{8}$ m/s           |
| $\Phi$       | Newtonian potential, $-GM/r$ for one mass                      | m$^2$/s$^2$                       |
| $\mathbf{u}$ | velocity of a body, in the frame of distant matter             | m/s                               |
| $\mathbf{w}$ | velocity of a body through the medium, $\mathbf{u}-\mathbf{v}$ | m/s                               |
| $a_0$        | acceleration at the relaxation boundary                        | about $1.2\times10^{-10}$ m/s$^2$ |

Quantities used in this paper.

</div>

# The Inflow and Its Acceleration

**\[Hypothesis: the passage that follows\]**

The medium flows into a mass $M$ along radial lines, with a speed calibrated once to Newton: $$\mathbf{v}(r) = -\sqrt{\frac{2GM}{r}}\;\hat{\mathbf{r}}.
\label{eq:inflow}$$ At the Earth’s surface this is 11.2 kilometres per second, the escape speed; at the Sun’s surface, 618 kilometres per second.

**\[End of passage\]**

The medium accelerates as it flows in, and its acceleration is exactly Newton’s gravity: **\[Argued\]** $$\mathbf{a}_{\text{medium}} = (\mathbf{v}\cdot\nabla)\mathbf{v} = v_r\,\frac{dv_r}{dr}\,\hat{\mathbf{r}} = -\frac{GM}{r^2}\,\hat{\mathbf{r}}.
\label{eq:accel}$$ Every body in the flow receives momentum from it in proportion to its own mass, at every particle at once (Part 7, Part 11), and so shares this acceleration: $$\mathbf{F} = m\,\mathbf{a}_{\text{medium}} = -\frac{GMm}{r^2}\,\hat{\mathbf{r}}.$$ Because the delivery is proportional to mass, every body falls alike, whatever it is made of; the MICROSCOPE mission found this true to about one part in $10^{15}$.[^3]

The first edition wrote the force as $\mathbf{F} = -m\nabla P_g$. That expression has the wrong units (kilograms times pascals per metre is not a newton), and it cannot be repaired by a constant, because the pressure gradient acts on the medium, not on the body. The medium’s own equation of steady flow (Euler’s equation) gives the correct link: the medium’s acceleration is set by its pressure gradient and its own density, and bodies share that acceleration. $$(\mathbf{v}\cdot\nabla)\mathbf{v} = -\frac{\nabla P}{\rho_g}.
\label{eq:euler}$$

# Pressure

Integrating Equation <a href="#eq:euler" data-reference-type="eqref" data-reference="eq:euler">[eq:euler]</a> along the inflow gives Bernoulli’s relation: **\[Argued\]** $$P(r) = P_0 - \tfrac12\rho_g v^2 = P_0 - \frac{\rho_g GM}{r} = P_0 + \rho_g\,\Phi.
\label{eq:pressure}$$ The active pressure is lower near a mass, by an amount set by the Newtonian potential $\Phi$. The free-space value is $P_0 = \tfrac12\rho_g c^2$, **\[Hypothesis\]** the value at which the pressure law and the clock law of Section <a href="#sec:clocks" data-reference-type="ref" data-reference="sec:clocks">“Clocks”</a> agree. With it, $$\frac{P}{P_0} = 1 - \frac{v^2}{c^2} = 1 - \frac{2GM}{c^2 r}.
\label{eq:ratio}$$

# Continuity

A steady inflow neither piles up nor runs short only if as much medium crosses every sphere around the mass as any other. **\[Argued\]** With the inflow speed of Equation <a href="#eq:inflow" data-reference-type="eqref" data-reference="eq:inflow">[eq:inflow]</a>, that requires the count of gravitons to rise toward the mass as $r^{-3/2}$: $$4\pi r^2\, n(r)\, |v(r)| = Q = \text{constant} \quad\Longrightarrow\quad n(r) \propto r^{-3/2}.
\label{eq:continuity}$$ This is the premise the framework already holds: the count of gravitons rises toward a mass while the active pressure falls (Part 14). The two are consistent because most of the medium near a mass has passed through matter and been ejected neutral: it is counted, but it does not press.

The relation between the intake $Q$ and the mass $M$ is still owed. **\[Open\]** If $Q$ is proportional to $M$, the normalisation of $n$ must scale as $\sqrt{M}$.

# Combining Flows

**\[Hypothesis: the passage that follows\]**

Flows from several masses do not add as velocities; their pressures combine. If the pressure deficits add, $$P = P_0 + \rho_g \sum_i \Phi_i, \qquad \Phi_i = -\frac{GM_i}{|\mathbf{r}-\mathbf{r}_i|},$$ then the acceleration set up by the combined pressure is $$\mathbf{a} = -\frac{\nabla P}{\rho_g} = -\nabla\sum_i \Phi_i,$$ which is Newton’s law for any number of bodies. In a static distribution of matter of density $\rho_m$, the pressure obeys $$\nabla^2 P = 4\pi G\,\rho_g\,\rho_m,
\label{eq:poisson}$$ which is Poisson’s equation of Newtonian gravity, written for the medium’s pressure.

**\[End of passage\]**

Combining by pressure recovers Newtonian dynamics for many bodies exactly: **\[Argued\]** the orbits of the planets, the Lagrange points, the tides (Part 13). Adding the inflow velocities instead would not: at the Earth, the cross term between the Sun’s inflow and the Earth’s would be of order 40 to 70 metres per second squared, which is not observed. The direction of the velocity field around many bodies, and the full non-linear rule for strong fields, are still owed. **\[Open\]**

# Clocks

**\[Hypothesis: the passage that follows\]**

A clock is a structure of medium waves, and it ticks more slowly the faster the medium streams through it; why, and why rods are squashed by the same factor, is set out in Section <a href="#sec:rulers" data-reference-type="ref" data-reference="sec:rulers">“Rods and Clocks: What the Streaming Does”</a>. A clock moving with velocity $\mathbf{u}$ through a medium flowing at $\mathbf{v}$ moves through the medium at $\mathbf{w} = \mathbf{u} - \mathbf{v}$, and its rate is $$\frac{d\tau}{dt} = \sqrt{1 - \frac{|\mathbf{u}-\mathbf{v}|^2}{c^2}}.
\label{eq:clock}$$

**\[End of passage\]**

For a clock held still ($\mathbf{u}=0$), the medium streams past at the inflow speed, and Equations <a href="#eq:ratio" data-reference-type="eqref" data-reference="eq:ratio">[eq:ratio]</a> and <a href="#eq:clock" data-reference-type="eqref" data-reference="eq:clock">[eq:clock]</a> give $$\frac{d\tau}{dt} = \sqrt{1 - \frac{2GM}{c^2 r}} = \sqrt{\frac{P}{P_0}}.$$ Gravitational and motional time dilation are one effect: both are the speed of the medium through the clock. **\[Argued\]** Each clock’s own rate is set by its structure: a caesium clock ticks about 9.2 billion times a second and a strontium clock about 429 trillion, and a change in a clock’s order, temperature or stress changes its rate. The factor by which the medium’s speed slows that rate depends on where the clock is and how it moves, and is the same for every kind of clock compared so far: **\[Argued\]** nuclear transitions (the iron-57 gamma rays of the Pound–Rebka tower), caesium and hydrogen masers, optical clocks of strontium, ytterbium, aluminium and mercury ions, and the weak-force decay of muons. Whether a change in a clock’s internal order alters that factor has not been tested. **\[Open\]**

#### Checks.

- **Height.** Raising a clock by $h$ near the Earth speeds it by $gh/c^2$: $2.5\times10^{-15}$ over the 22.5 metres of the Pound–Rebka tower,[^4] and $3.6\times10^{-17}$ for the 33-centimetre rise measured with optical clocks.[^5]

- **GPS.** A GPS satellite’s clock runs faster by 45.7 microseconds a day, because the medium streams more slowly past it at altitude, and slower by 7.2 microseconds a day because of its orbital speed: a net 38.5 microseconds a day, which the system corrects for.

- **The Earth’s surface.** With the medium streaming past at 11.2 kilometres per second, a clock on the ground runs slow by $1-\sqrt{1-v^2/c^2} = 6.96\times10^{-10}$, exactly $GM/c^2R$.

- **Fast muons.** Muons circulating at $\gamma \approx 29.3$ in a storage ring, under accelerations of about $10^{18}\,g$, lived $\gamma$ times longer and no more: the rate depends on speed through the medium, not on acceleration.[^6]

# Rods and Clocks: What the Streaming Does

**\[Hypothesis: the passage that follows\]**

A rod and a clock are patterns of the medium, held together by bonds, and a bond is kept up by exchanges that cross it at $c$ through the medium. When the medium streams through a pattern at speed $w$, those exchanges take longer, and longer along the flow than across it. Across a bond of length $L$, the round trip takes $$t_\perp = \frac{2L}{\sqrt{c^2-w^2}} = \frac{2L}{c}\,\gamma ;$$ along the flow, against it and then with it, a bond of length $L_\parallel$ takes $$t_\parallel = \frac{L_\parallel}{c-w} + \frac{L_\parallel}{c+w} = \frac{2L_\parallel}{c}\,\gamma^2 ,
\qquad \gamma = \frac{1}{\sqrt{1-w^2/c^2}} .$$ At rest, a pattern settles where its exchanges balance in every direction. In the stream it settles again where they balance, and that is where $t_\parallel = t_\perp$: $$L_\parallel = \frac{L}{\gamma} .
\label{eq:squash}$$ The pattern is squashed along the flow, and only along it. Every exchange in it now takes $\gamma$ times as long, so every cycle in it runs slower by the same factor: Equation <a href="#eq:clock" data-reference-type="eqref" data-reference="eq:clock">[eq:clock]</a>. One mechanism gives both effects, which is why the factor that slows clocks and the factor that squashes rods are always equal.

**\[End of passage\]**

This is FitzGerald’s and Lorentz’s proposal, that motion through the medium changes the forces that hold a body together, given its carrier: the exchanges of the medium itself. Bell showed the same result for a single atom: as it moves, its electron’s orbit flattens along the motion and its period lengthens, both from the atom’s own dynamics.[^7][^8]

#### The same for every material.

Every bond is a pattern of the same medium, kept up by exchanges at the same speed, so every material is squashed alike. That is required by measurement. If the medium is at rest relative to the cosmic background radiation, the Earth streams through it at about 370 kilometres per second, and its laboratories are squashed along that direction by about 8 parts in $10^7$; that squash is exactly what makes light’s round trips come out the same in every direction. Were it a strain that depended on how stiff a material is, cavities of different materials would disagree. Cavities of glass-ceramic and of sapphire crystal find light’s round trip the same in every direction to about one part in $10^{17}$.[^9][^10] The squash is in the bonds’ own balance, not a load pressing on them.

#### Nothing across the flow.

Experiments with arms of unequal length, which would show any change of a body’s overall size with its speed, find none: the size across the flow is unchanged.[^11] Why the exchanges across the flow keep their length is still owed. **\[Open\]**

#### Stress while the streaming changes.

A body whose speed through the medium changes is out of balance until its bonds re-settle: for that time it is under stress, and then it holds its new shape without any. The re-settling takes a time set by the medium’s response, the same relaxation time Part 14 predicts for clocks. **\[Hypothesis\]**

#### Two kinds of squashing.

A body squashed by a load is a different thing. A support pushing on a body compresses it by an amount set by the load and the material’s stiffness: a column shortens under its own weight, and an astronaut’s spine lengthens by several centimetres when the load is gone (Part 11). That depends on $g$ and on the material. Squashing by streaming depends on the medium’s speed through the body, $w$, and is the same for every material. A rod held still at the Earth’s surface has the medium streaming through it at 11.2 kilometres per second along the vertical, and is squashed along the vertical by $1-\sqrt{1-v^2/c^2} = 7.0\times10^{-10}$, the same fraction that slows a clock there.

#### Why General Relativity says space is stretched.

Around a mass, the distance between two spherical shells, measured with rods held still, comes out larger than flat geometry gives. General Relativity reads this as space stretched. In GPT space is flat; the held rods are squashed along the flow, so more of them fit into the same gap.

Clocks slowed and rods squashed by the streaming, in a flat space through which the medium flows at Equation <a href="#eq:inflow" data-reference-type="eqref" data-reference="eq:inflow">[eq:inflow]</a>, are described together by one expression: **\[Argued\]** $$c^2 d\tau^2 = c^2 dt^2 - \left|\,d\mathbf{x} - \mathbf{v}\,dt\,\right|^2 .
\label{eq:pg}$$ This is the Schwarzschild solution of General Relativity, in the form Painlevé and Gullstrand found in 1921 and 1922.[^12][^13] Every prediction General Relativity makes for a single non-rotating mass therefore follows from GPT unchanged. General Relativity reads Equation <a href="#eq:pg" data-reference-type="eqref" data-reference="eq:pg">[eq:pg]</a> as the geometry of spacetime; in GPT it is the record of what the streaming does to rods and clocks. The numbers are the same; the mechanism is named.

The first edition’s form, in which rulers shrank equally in every direction, gave the wrong advance of Mercury’s perihelion (57$''$ per century instead of 43$''$). Squashing along the flow only gives the right one.

# Light

**\[Hypothesis: the passage that follows\]**

Light is a transverse wave of the medium and moves at $c$ relative to the medium. A wave with wave vector $\mathbf{k}$ in a medium moving at $\mathbf{v}$ has frequency $$\omega = c\,|\mathbf{k}| + \mathbf{k}\cdot\mathbf{v}.
\label{eq:light}$$

**\[End of passage\]**

Measured locally, by rods and clocks that are themselves in the medium, its speed is always $c$. Tracing rays with Equation <a href="#eq:light" data-reference-type="eqref" data-reference="eq:light">[eq:light]</a> past a mass gives:

- **Bending**: $\Delta\theta = 4GM/c^2 b$ for a ray passing at distance $b$, which is 1.75$''$ at the Sun’s edge. **\[Argued\]** The traced rays give $\Delta\theta\, b\,c^2/GM = 4.016$, $4.002$ and $4.0005$ for $b = 10^3$, $10^4$ and $10^5$ times $GM/c^2$, approaching 4 as the path lengthens.

- **Delay**: a signal passing the Sun is delayed by $(2GM/c^3)\ln(4r_1r_2/b^2)$ each way, **\[Argued\]** as Shapiro predicted and radar and spacecraft measured; the Cassini spacecraft confirmed it to about one part in $10^5$.[^14][^15]

- **Redshift**: a signal climbing from a lower to a higher clock is received by a faster clock, so it appears redder by $\Delta\Phi/c^2$, as in Section <a href="#sec:clocks" data-reference-type="ref" data-reference="sec:clocks">“Clocks”</a>.

In the language of refraction, the medium near a mass acts on light with an index $n \approx 1 + 2GM/c^2 r$. From Equation <a href="#eq:ratio" data-reference-type="eqref" data-reference="eq:ratio">[eq:ratio]</a>, that is $$n \approx 2 - \frac{P}{P_0}:$$ the lower the active pressure, the higher the index, and the slower light travels as measured from far away. The first edition had the sign reversed, with light slowing where the pressure was higher.

#### No colour in the bending.

Because light moves at $c$ through the medium whatever its frequency, the bending is the same for radio and for visible light. It is: radio and optical measurements agree to a few parts in a thousand, and radio interferometry fixes the bending to about one part in $10^4$. The first edition’s suggestion of colour-dependent lensing is withdrawn.

# Motion

**\[Hypothesis: the passage that follows\]**

A body moving through the medium at $\mathbf{w}$ takes in the medium faster at its leading face than at its trailing face, by the factor $$k = \sqrt{\frac{1+w/c}{1-w/c}}.$$ The imbalance is its momentum, the path it carves (Part 11).

**\[End of passage\]**

The arithmetic is exact. **\[Argued\]** Half the sum of the front and back rates, $\tfrac12(k + 1/k)$, is $\gamma = 1/\sqrt{1-w^2/c^2}$; half the difference, $\tfrac12(k - 1/k)$, is $\gamma w/c$. So the body’s energy and momentum are $$E = \gamma m c^2, \qquad \mathbf{p} = \gamma m \mathbf{w}.$$ Their shared rate, the geometric mean $\sqrt{k \cdot 1/k} = 1$, is the rest rate that runs the body’s internal cycles, which is why a moving clock slows by $1/\gamma$; the excess $\gamma - 1$ is its kinetic energy. A force along the motion changes the speed at a cost $\gamma^3$ times that at rest, and a force across it at a cost $\gamma$. Approaching $c$, the front rate grows without bound, and so does the energy needed.

The path of a body moving freely in the medium follows from Equation <a href="#eq:pg" data-reference-type="eqref" data-reference="eq:pg">[eq:pg]</a>: **\[Argued\]** it is the path General Relativity calls a geodesic. For an orbit, it gives Kepler’s ellipses with a slow advance of the perihelion, $$\Delta\varpi = \frac{6\pi GM}{c^2 a (1-e^2)} \ \text{per orbit},$$ which is 43.0$''$ per century for Mercury, as observed after the pull of the other planets (532$''$ per century) is removed.[^16]

Matter and light differ in one respect. Matter is a standing pattern of the medium, with both a leading and a trailing exchange, and so a rest rate: a mass. Light is a travelling wave of the medium, with only a front, so its rest rate is zero: it has energy and momentum, $E = pc$, but no mass.

# Rotation

**\[Hypothesis: the passage that follows\]**

A rotating mass gives the medium flowing into it a swirl, as a spinning drain gives swirl to the water entering it. Far from a body with angular momentum $J$, the swirl turns at $$\omega(r) \approx \frac{2GJ}{c^2 r^3},$$ and a gyroscope carried in the medium is turned with it.

**\[End of passage\]**

This is the frame-dragging of General Relativity: **\[Argued\]** the river model of a rotating black hole contains exactly this swirl.[^17] Gravity Probe B measured the dragging of its gyroscopes around the Earth at $37.2 \pm 7.2$ milliarcseconds a year, against 39.2 predicted, and the precession of their spin axes by the inflow itself at $6602 \pm 18$ milliarcseconds a year, against 6606.[^18] The orbits of the LAGEOS satellites are dragged as predicted, to about ten per cent.[^19]

# Waves in the Medium

**\[Hypothesis: the passage that follows\]**

The medium carries stress as well as pressure, and so it carries transverse waves. Light is one; gravitational waves, the medium’s response to masses accelerating, are another. Both move at $c$.

**\[End of passage\]**

What is measured fixes the form of these waves: **\[Argued\]**

- **Speed.** Gravitational waves and light from the neutron-star merger of August 2017 arrived within two seconds of each other after travelling 130 million years: their speeds agree to about one part in $10^{15}$.[^20] In GPT this is expected, since both are waves of the same medium.

- **Polarisation.** With three detectors, the pattern of stretching fitted the two transverse, tensor polarisations better than scalar or vector patterns.[^21] The waves are not pressure waves of the medium; a pressure wave would be a single, breathing polarisation.

- **Energy carried.** The orbit of the binary pulsar PSR B1913+16 shrinks exactly as the energy carried away by gravitational waves requires: the measured rate is $0.9983 \pm 0.0016$ times the predicted one.[^22]

How one medium carries two kinds of transverse wave, vector waves for light and tensor waves for gravity, at the same speed, is still owed. **\[Open\]** The elastic models of the luminiferous medium in the nineteenth century are the precedent to study. The first edition’s scalar wave equation for the pressure, with a speed that might exceed $c$, is withdrawn: it gives the wrong polarisation and the wrong speed.

# The Medium’s Scale

Only the inflow speed enters the motion of planets, clocks and light; the medium’s density and free-space pressure do not. They cannot be measured from orbits or from the bending of light. They are fixed instead by what the medium may deliver as heat.

If matter absorbed the medium flowing into it and kept its energy as heat, the intake $4\pi R^2 \rho_g v_{\text{esc}}$, times $c^2$, would heat every planet and star. **\[Argued\]** At $P_0 \approx 4.5\times10^{-10}$ pascals, $\rho_g \approx 1.0\times10^{-26}$ kilograms per cubic metre:

- the Earth would absorb $5.1\times10^{9}$ watts, one ten-thousandth of its measured heat flow of 47 terawatts;

- the Sun would absorb $3.4\times10^{15}$ watts, a hundred-billionth of its output.

Both pass. The first edition’s higher values, $10^{10}$ to $10^{12}$ pascals in Part 19 and $10^{-6}$ to $10^{-4}$ pascals in Part 25, are retired as the medium’s free-space pressure: the first would heat the Earth beyond its measured heat flow by fifteen orders of magnitude and more. The $10^{10}$ to $10^{11}$ pascals of Part 19 survives as a different quantity, the energy density of the bonds that hold matter together (iron’s cohesive energy is about $5.8\times10^{10}$ joules per cubic metre).

The scale has a coincidence worth noting: $\tfrac12\rho_c c^2$, for the critical density of the universe, is $3.8\times10^{-10}$ pascals, and the pressure attributed to dark energy has a magnitude of $5.3\times10^{-10}$ pascals. **\[Hypothesis\]** In General Relativity the dark-energy pressure is negative, and the medium’s is positive; any link must come through a different route, the expansion of a self-repelling medium that is not confined, and must be derived (Part 14).

The medium’s equation of state, and the range and law of its self-repulsion, are still owed. **\[Open\]** One constraint is already clear: if the pressure were simply proportional to the density, compression waves would travel at $c/\sqrt2$, so light and gravitational waves cannot be compression waves. That agrees with Section <a href="#sec:waves" data-reference-type="ref" data-reference="sec:waves">“Waves in the Medium”</a>. The first edition’s inverse-square repulsion between gravitons is superseded by the phase account of Part 15: gravitons in phase push one another, and neutral ones do not, so the law cannot be one inverse square over all pairs.

# The Relaxation Boundary

Galaxies rotate as though held by more matter than they contain, and the departure from Newton follows a single pattern. Across 153 galaxies of every size, the acceleration observed at each radius is fixed by the acceleration expected from the visible matter alone, with a scatter of about 0.13 dex, by the relation[^23] $$g_{\text{obs}} = \frac{g_{\text{bar}}}{1 - e^{-\sqrt{g_{\text{bar}}/a_0}}}, \qquad a_0 \approx 1.2\times10^{-10}\ \text{m/s}^2.
\label{eq:rar}$$ Where $g_{\text{bar}}$ is large, $g_{\text{obs}} = g_{\text{bar}}$: Newton holds. Where it is small, $g_{\text{obs}} \to \sqrt{g_{\text{bar}}\,a_0}$, and a star orbiting at a large radius moves at a speed that no longer falls with distance, $v^4 = GMa_0$ (Figure <a href="#fig:rar" data-reference-type="ref" data-reference="fig:rar">1</a>).

**\[Hypothesis: the passage that follows\]**

GPT places a boundary around every mass where its inflow’s acceleration falls to $a_0$: $$r_{a_0} = \sqrt{\frac{GM}{a_0}}.$$ Beyond it, the medium ejected neutral by the mass is recharged, and gravity changes its form. For the Sun, $r_{a_0} \approx 7{,}000$ astronomical units, far beyond the planets, so the solar system’s tracking is untouched. For the Milky Way, with $6\times10^{10}$ to $10^{11}$ solar masses of stars and gas, it is 8 to 11 kiloparsecs, where the rotation curve flattens.

**\[End of passage\]**

<figure id="fig:rar">
<img src="assets/figures/fig23-1-rar.svg" />
<figcaption>What the relaxation boundary must reproduce: the acceleration observed in galaxies against the acceleration expected from their visible matter, in the fitted form of the measured relation (Equation <a href="#eq:rar" data-reference-type="ref" data-reference="eq:rar">[eq:rar]</a>). Above <span class="math inline"><em>a</em><sub>0</sub></span>, Newton holds; below it, the observed acceleration approaches <span class="math inline">$\sqrt{g_{\text{bar}}a_0}$</span>, and rotation curves flatten. GPT places the change at the boundary where each mass’s inflow falls to <span class="math inline"><em>a</em><sub>0</sub></span>. (Hypothesis)</figcaption>
</figure>

The law of the boundary, from which Equation <a href="#eq:rar" data-reference-type="eqref" data-reference="eq:rar">[eq:rar]</a> must follow, is still owed. **\[Open\]** It is GPT’s central distinctive prediction (Part 14). Tests at the scale of the Sun’s boundary already exist: wide binary stars separated by thousands of astronomical units, whose orbits are currently disputed in both directions.[^24][^25]

# Summary

<div id="tab:summary">

| **Effect**  | **GPT**                                                                                                         | **Measured**                         |
|:------------|:----------------------------------------------------------------------------------------------------------------|:-------------------------------------|
| Falling     | medium’s acceleration $GM/r^2$, shared in proportion to mass                                                    | same for all bodies to $10^{-15}$    |
| Many bodies | pressures combine; $\mathbf{a} = -\nabla\sum\Phi_i$                                                             | planetary motion, tides              |
| Clocks      | $\sqrt{1-|\mathbf{u}-\mathbf{v}|^2/c^2}$                                                                        | Pound–Rebka; 33 cm; GPS; muons       |
| Light       | $c$ through the medium; $4GM/c^2b$                                                                              | 1.75$''$; Shapiro delay to $10^{-5}$ |
| Orbits      | Equation <a href="#eq:pg" data-reference-type="eqref" data-reference="eq:pg">[eq:pg]</a>; $6\pi GM/c^2a(1-e^2)$ | Mercury 43$''$ per century           |
| Rotation    | swirl $2GJ/c^2r^3$                                                                                              | Gravity Probe B; LAGEOS              |
| Waves       | transverse, at $c$                                                                                              | GW170817; tensor; binary pulsar      |
| Scale       | $P_0 \approx 4.5\times10^{-10}$ Pa                                                                              | within the heat budget               |
| Galaxies    | boundary at $\sqrt{GM/a_0}$                                                                                     | radial acceleration relation         |

The equations of the medium and the measurements they meet.

</div>

Table <a href="#tab:summary" data-reference-type="ref" data-reference="tab:summary">2</a> gathers the results. Every measurement that General Relativity passes for a single mass, GPT passes with the same numbers, because it contains the same equations; what it adds is the cause, a medium flowing through flat space, and a single prediction of its own at the scale of galaxies.

The derivations still owed are: the relation between intake and mass (Section <a href="#sec:continuity" data-reference-type="ref" data-reference="sec:continuity">“Continuity”</a>); the full rule for combining flows in strong fields (Section <a href="#sec:combining" data-reference-type="ref" data-reference="sec:combining">“Combining Flows”</a>); the two transverse waves of one medium (Section <a href="#sec:waves" data-reference-type="ref" data-reference="sec:waves">“Waves in the Medium”</a>); the equation of state (Section <a href="#sec:scale" data-reference-type="ref" data-reference="sec:scale">“The Medium’s Scale”</a>); and the law of the relaxation boundary (Section <a href="#sec:boundary" data-reference-type="ref" data-reference="sec:boundary">“The Relaxation Boundary”</a>).

The path ahead is not curved. It is pressurised. And it is measurable.

# Changes in the Second Edition

This list records what changed from the first edition (12 June 2025) and why. Changes to the argument alter what the paper claims or how it supports a claim; clarifications improve wording, sources or presentation and leave the argument as it was.

## Changes to the argument

- The equations are replaced by the agreed account: the inflow calibrated to Newton, its acceleration, Bernoulli’s pressure, continuity, combining by pressure, one clock law, rulers shortened along the flow, light at $c$ through the medium, motion as the carved path, rotation as swirl, transverse waves, the scale and the relaxation boundary. Together they reproduce the Schwarzschild solution exactly, in Painlevé–Gullstrand form.

- $\mathbf{F} = -m\nabla P_g$ and $a = -\nabla P_g$ are withdrawn: their units do not balance, and the pressure gradient acts on the medium, which bodies share by delivery in proportion to mass.

- The pressure “field tension” $G_{ij} = \partial_i P^j - \partial_j P^i$, which treated a scalar pressure as a vector, is withdrawn; the medium’s stress and the swirl of its flow take its place.

- The lensing formula $\Delta\theta = \int (1/E)(\nabla P_g\cdot\hat n)\,ds$, whose units do not give an angle, is replaced by ray tracing with Equation <a href="#eq:light" data-reference-type="eqref" data-reference="eq:light">[eq:light]</a>.

- Three different clock laws ($\sqrt{1-P_g/P_0}$, $\exp(-P_g/P_0)$, and $\Delta\lambda/\lambda_0 = \sqrt{P_g/P_0}$ for redshift), each with time slowing where the pressure was higher, are replaced by one law, with the active pressure lower near a mass.

- Redshift as energy lost by light to the pressure of the medium is replaced by the slower clocks below.

- The scalar wave equation for the pressure, with a speed that might exceed $c$, and the predicted dispersion, echoes and non-tensor waves, are withdrawn: the measured speed, polarisation and absence of dispersion rule them out.

- The frame-dragging force $\mathbf{F} = m(\mathbf{v}_g\times\boldsymbol\omega)$ is replaced by the swirl of the inflow, which gives the measured rate.

- The proposed tests of particle lifetimes underground and at altitude are moved to Part 29: the predicted differences are about one part in $10^{12}$ per ten kilometres of height, the same as in General Relativity. The proposals for detectors, biological sensor arrays, chronobiology in space and accelerator tests are likewise moved to Part 29, where they are set beside the framework’s distinctive predictions.

- Section <a href="#sec:rulers" data-reference-type="ref" data-reference="sec:rulers">“Rods and Clocks: What the Streaming Does”</a> (rewritten 9 November): rods and clocks are given their mechanism. The medium streaming through a pattern lengthens the exchanges that keep up its bonds, more along the flow than across it; the pattern re-settles where they balance, squashed along the flow by $1/\gamma$, and every cycle in it slows by $\gamma$. The section separates squashing by streaming (the same for every material) from squashing by load (set by stiffness), and explains General Relativity’s “stretched space” as more squashed rods fitting into the same gap. The first edition’s inverse-square self-repulsion is now described as superseded by the phase account of Part 15, not withdrawn on grounds of equilibrium.

## Clarifications

- Section on clocks (corrected 9 November): each clock’s own rate is set by its structure; what is the same for every kind of clock is the factor by which the medium’s speed slows it. An earlier wording of this edition said the rate does not depend on what the clock is made of. Whether a change of internal order alters the factor is marked open.

- The subtitle changes from *Empirical Foundation of Graviton Pressure Theory* to *The Equations of the Medium, and What They Reproduce*.

- A table of quantities, a summary table, a figure of the radial acceleration relation, status marks and this list are added; sources are given for every measurement.

<div id="refs" class="references csl-bib-body hanging-indent">

<div id="ref-abbott2017speed" class="csl-entry">

Abbott, B. P. et al. 2017a. “Gravitational Waves and Gamma-Rays from a Binary Neutron Star Merger: GW170817 and GRB 170817A.” *The Astrophysical Journal Letters* 848: L13.

</div>

<div id="ref-abbott2017gw170814" class="csl-entry">

——— et al. 2017b. “GW170814: A Three-Detector Observation of Gravitational Waves from a Binary Black Hole Coalescence.” *Physical Review Letters* 119: 141101.

</div>

<div id="ref-bailey1977" class="csl-entry">

Bailey, J. et al. 1977. “Measurements of Relativistic Time Dilatation for Positive and Negative Muons in a Circular Orbit.” *Nature* 268: 301–5.

</div>

<div id="ref-banik2024" class="csl-entry">

Banik, Indranil et al. 2024. “Strong Constraints on the Gravitational Law from Gaia DR3 Wide Binaries.” *Monthly Notices of the Royal Astronomical Society* 527: 4573–4615.

</div>

<div id="ref-barcelo2011" class="csl-entry">

Barceló, Carlos, Stefano Liberati, and Matt Visser. 2011. “Analogue Gravity.” *Living Reviews in Relativity* 14: 3.

</div>

<div id="ref-bell1976" class="csl-entry">

Bell, John S. 1987. “How to Teach Special Relativity.” In *Speakable and Unspeakable in Quantum Mechanics*. Cambridge University Press.

</div>

<div id="ref-bertotti2003" class="csl-entry">

Bertotti, B., L. Iess, and P. Tortora. 2003. “A Test of General Relativity Using Radio Links with the Cassini Spacecraft.” *Nature* 425: 374–76.

</div>

<div id="ref-brown2005" class="csl-entry">

Brown, Harvey R. 2005. *Physical Relativity: Space-Time Structure from a Dynamical Perspective*. Oxford University Press.

</div>

<div id="ref-chae2023" class="csl-entry">

Chae, Kyu-Hyun. 2023. “Breakdown of the Newton–Einstein Standard Gravity at Low Acceleration in Internal Dynamics of Wide Binary Stars.” *The Astrophysical Journal* 952: 128.

</div>

<div id="ref-chou2010" class="csl-entry">

Chou, C. W., D. B. Hume, T. Rosenband, and D. J. Wineland. 2010. “Optical Clocks and Relativity.” *Science* 329: 1630–33.

</div>

<div id="ref-ciufolini2004" class="csl-entry">

Ciufolini, I., and E. C. Pavlis. 2004. “A Confirmation of the General Relativistic Prediction of the Lense–Thirring Effect.” *Nature* 431: 958–60.

</div>

<div id="ref-eisele2009" class="csl-entry">

Eisele, Ch., A. Yu. Nevsky, and S. Schiller. 2009. “Laboratory Test of the Isotropy of Light Propagation at the $10^{-17}$ Level.” *Physical Review Letters* 103: 090401.

</div>

<div id="ref-everitt2011" class="csl-entry">

Everitt, C. W. F. et al. 2011. “Gravity Probe b: Final Results of a Space Experiment to Test General Relativity.” *Physical Review Letters* 106: 221101.

</div>

<div id="ref-gullstrand1922" class="csl-entry">

Gullstrand, Allvar. 1922. “Allgemeine lösung Des Statischen Einkörperproblems in Der Einsteinschen Gravitationstheorie.” *Arkiv för Matematik, Astronomi Och Fysik* 16 (8): 1–15.

</div>

<div id="ref-hamilton2008" class="csl-entry">

Hamilton, Andrew J. S., and Jason P. Lisle. 2008. “The River Model of Black Holes.” *American Journal of Physics* 76: 519–32.

</div>

<div id="ref-kennedy1932" class="csl-entry">

Kennedy, Roy J., and Edward M. Thorndike. 1932. “Experimental Establishment of the Relativity of Time.” *Physical Review* 42: 400–418.

</div>

<div id="ref-mcgaugh2016" class="csl-entry">

McGaugh, Stacy S., Federico Lelli, and James M. Schombert. 2016. “Radial Acceleration Relation in Rotationally Supported Galaxies.” *Physical Review Letters* 117: 201101.

</div>

<div id="ref-nagel2015" class="csl-entry">

Nagel, Moritz et al. 2015. “Direct Terrestrial Test of Lorentz Symmetry in Electrodynamics to $10^{-18}$.” *Nature Communications* 6: 8174.

</div>

<div id="ref-painleve1921" class="csl-entry">

Painlevé, Paul. 1921. “La mécanique Classique Et La Théorie de La Relativité.” *Comptes Rendus de l’Académie Des Sciences* 173: 677–80.

</div>

<div id="ref-pound1960" class="csl-entry">

Pound, R. V., and G. A. Rebka. 1960. “Apparent Weight of Photons.” *Physical Review Letters* 4: 337–41.

</div>

<div id="ref-shapiro1964" class="csl-entry">

Shapiro, Irwin I. 1964. “Fourth Test of General Relativity.” *Physical Review Letters* 13: 789–91.

</div>

<div id="ref-touboul2022" class="csl-entry">

Touboul, Pierre et al. 2022. “MICROSCOPE Mission: Final Results of the Test of the Equivalence Principle.” *Physical Review Letters* 129: 121102.

</div>

<div id="ref-weisberg2016" class="csl-entry">

Weisberg, J. M., and Y. Huang. 2016. “Relativistic Measurements from Timing the Binary Pulsar PSR B1913+16.” *The Astrophysical Journal* 829: 55.

</div>

<div id="ref-will2014" class="csl-entry">

Will, Clifford M. 2014. “The Confrontation Between General Relativity and Experiment.” *Living Reviews in Relativity* 17: 4.

</div>

</div>

[^1]: (Hamilton and Lisle 2008).

[^2]: (Barceló, Liberati, and Visser 2011).

[^3]: (Touboul et al. 2022).

[^4]: (Pound and Rebka 1960).

[^5]: (Chou et al. 2010).

[^6]: (Bailey et al. 1977).

[^7]: (Bell 1987).

[^8]: (Brown 2005).

[^9]: (Eisele, Nevsky, and Schiller 2009).

[^10]: (Nagel et al. 2015).

[^11]: (Kennedy and Thorndike 1932).

[^12]: (Painlevé 1921).

[^13]: (Gullstrand 1922).

[^14]: (Shapiro 1964).

[^15]: (Bertotti, Iess, and Tortora 2003).

[^16]: (Will 2014).

[^17]: (Hamilton and Lisle 2008).

[^18]: (Everitt et al. 2011).

[^19]: (Ciufolini and Pavlis 2004).

[^20]: (Abbott et al. 2017a).

[^21]: (Abbott et al. 2017b).

[^22]: (Weisberg and Huang 2016).

[^23]: (McGaugh, Lelli, and Schombert 2016).

[^24]: (Chae 2023).

[^25]: (Banik et al. 2024).

---
Source: https://peopleoftheworld.net/graviton-pressure-theory/full-framework/part-23-the-mathematical-foundation/
Cite as: Rashada, S. A. (2026). The Mathematical Foundation. In The Unified Framework for the Graviton Pressure Theory, part 23. People of the World. https://peopleoftheworld.net/graviton-pressure-theory/full-framework/part-23-the-mathematical-foundation/
