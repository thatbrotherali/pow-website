"""Figures for Part 9 from the public SPARC tables."""
import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import sparc
plt.rcParams.update({"font.family": "Inter", "font.size": 8})
BLUE = "#1F5FAD"; ORANGE = "#C8650A"; GREY = "#8A8A8A"; DARK = "#333333"
G = 6.674e-11; MSUN = 1.989e30

def save(name):
    for ext in ("pdf", "svg"): plt.savefig(f"{name}.{ext}")
    plt.savefig(f"{name}.png", dpi=200); plt.close()

# ---- Figure 9.1: the radial acceleration relation
d = sparc.rar(); gb = np.array([x[1] for x in d]); go = np.array([x[2] for x in d])
a0, res = sparc.fit_a0(gb, go)
fig, (ax, rx) = plt.subplots(2, 1, figsize=(6.4, 6.0), gridspec_kw={"height_ratios": [3, 1]}, sharex=True)
ax.scatter(np.log10(gb), np.log10(go), s=2.5, color=BLUE, alpha=0.35, lw=0)
x = np.linspace(-12.6, -8.3, 300); g = 10 ** x
ax.plot(x, x, color=GREY, ls="--", lw=1)
ax.plot(x, np.log10(g / (1 - np.exp(-np.sqrt(g / a0)))), color=ORANGE, lw=1.8)
ax.axvline(np.log10(a0), color=DARK, lw=0.7, ls=":")
ax.text(np.log10(a0) + 0.05, -8.55, f"a$_0$ = {a0/1e-10:.2f}×10$^{{-10}}$ m/s²", fontsize=7, color=DARK)
ax.text(-11.05, -11.55, "Newton from the visible\nmatter alone", color=GREY, fontsize=7)
ax.text(-12.45, -10.05, "one curve for every galaxy", color=ORANGE, fontsize=7.5)
ax.set_ylabel("measured acceleration, log$_{10}$ (m/s²)")
ax.set_xlim(-12.6, -8.3); ax.set_ylim(-12.0, -8.3)
ax.set_title(f"{len(go):,} points in {len({x[0] for x in d})} galaxies (SPARC)", fontsize=8)
rx.scatter(np.log10(gb), res, s=2.5, color=BLUE, alpha=0.35, lw=0); rx.axhline(0, color=ORANGE, lw=1.2)
rx.set_ylim(-0.7, 0.7); rx.set_ylabel("residual (dex)")
rx.text(-12.5, 0.48, f"scatter {res.std():.2f} dex", fontsize=7, color=DARK)
rx.set_xlabel("acceleration expected from the visible matter, log$_{10}$ (m/s²)")
for a in (ax, rx):
    for s in ("top", "right"): a.spines[s].set_visible(False)
plt.tight_layout(); save("fig09-1-rar")

# ---- Figure 9.2: baryonic Tully-Fisher relation
gal = sparc.table1()
pts = [(k, 0.5 * v["L"] + 1.33 * v["MHI"], v["Vflat"], v["eVflat"]) for k, v in gal.items() if v["Vflat"] > 0 and v["Q"] < 3 and v["inc"] >= 30]
M = np.array([p[1] for p in pts]); V = np.array([p[2] for p in pts])
slope, icpt = np.polyfit(np.log10(V), np.log10(M), 1)
fig, ax = plt.subplots(figsize=(6.4, 4.0))
ax.scatter(np.log10(V), np.log10(M), s=10, color=BLUE, alpha=0.6, lw=0)
v = np.linspace(1.3, 2.6, 50); Vms = 10 ** v * 1e3
ax.plot(v, np.log10(Vms ** 4 / (G * a0) / MSUN), color=ORANGE, lw=1.8, label="$M = v^4/(G\\,a_0)$: no free parameter")
for name, lab in (("NGC3198", "NGC 3198"), ("UGC02885", "UGC 2885")):
    g_ = gal[name]; m_ = 0.5 * g_["L"] + 1.33 * g_["MHI"]
    ax.plot(np.log10(g_["Vflat"]), np.log10(m_), "o", mfc="none", mec=DARK, ms=8)
    ax.annotate(lab, (np.log10(g_["Vflat"]), np.log10(m_)), xytext=(-48, 8), textcoords="offset points", fontsize=7, color=DARK)
ax.set_xlabel("flat rotation speed, log$_{10}$ (km/s)"); ax.set_ylabel("visible mass, log$_{10}$ (solar masses)")
ax.legend(frameon=False, fontsize=7, loc="upper left")
ax.text(2.0, 7.4, f"{len(pts)} galaxies (SPARC)", fontsize=7, color=DARK)
for s in ("top", "right"): ax.spines[s].set_visible(False)
plt.tight_layout(); save("fig09-2-btfr")
# ---- Figure 9.3: the GPS clock budget as the medium streaming past each clock
GM = 3.986004418e14; c = 299792458.0; day = 86400.0; rg = 6378137.0; om = 7.2921150e-5; rs = 26561.75e3
f = lambda w2: w2 / (2 * c * c) * day * 1e6            # microseconds lost per day
parts = {"Ground clock": (f(2 * GM / rg), f((om * rg) ** 2)), "GPS satellite clock": (f(2 * GM / rs), f(GM / rs))}
fig, ax = plt.subplots(figsize=(6.6, 2.6))
for i, (lab, (a, b)) in enumerate(parts.items()):
    ax.barh(i, a, color=BLUE, height=0.5); ax.barh(i, b, left=a, color=ORANGE, height=0.5)
    ax.text(a + b + 0.8, i, f"{a + b:.2f} µs a day", va="center", fontsize=7.5)
ax.set_yticks([0, 1]); ax.set_yticklabels(list(parts)); ax.invert_yaxis()
ax.set_xlabel("slowing of the clock by the medium streaming past it (microseconds a day)")
from matplotlib.patches import Patch
ax.legend(handles=[Patch(color=BLUE, label="the inflow streaming down past the clock"),
                   Patch(color=ORANGE, label="the clock's own motion through the medium")],
          frameon=False, fontsize=7, loc="upper right", bbox_to_anchor=(1.0, 0.72))
g_, s_ = sum(parts["Ground clock"]), sum(parts["GPS satellite clock"])
ax.annotate("", xy=(s_, 1.42), xytext=(g_, 1.42), arrowprops=dict(arrowstyle="<->", color=DARK, lw=0.8))
ax.text((g_ + s_) / 2, 1.62, f"difference {g_ - s_:.2f} µs a day: the satellite clock runs fast", ha="center", fontsize=7, color=DARK)
ax.set_xlim(0, 75); ax.set_ylim(1.95, -0.5)
for sp in ("top", "right"): ax.spines[sp].set_visible(False)
plt.tight_layout(); save("fig09-3-gps")
print("gps", {k: [round(x, 2) for x in v] for k, v in parts.items()}, round(g_ - s_, 2))
res_b = np.log10(M) - np.log10((V * 1e3) ** 4 / (G * a0) / MSUN)
print(f"a0={a0:.3e} rar_n={len(go)} scatter={res.std():.3f}; btfr n={len(pts)} slope={slope:.2f} scatter_vs_line={res_b.std():.2f} mean={res_b.mean():+.2f}")
for name in ("NGC3198", "UGC02885"):
    g_ = gal[name]; m_ = 0.5 * g_["L"] + 1.33 * g_["MHI"]; vp = (G * m_ * MSUN * a0) ** 0.25 / 1e3
    print(name, f"Mb={m_:.3g} Vflat={g_['Vflat']} predicted v={vp:.0f}")
