"""Figures for Part 25, The Medium at Its Limits."""
import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
plt.rcParams.update({"font.family": "Inter", "font.size": 8})
BLUE = "#1F5FAD"; ORANGE = "#C8650A"; GREY = "#8A8A8A"; DARK = "#333333"

def save(name):
    for ext in ("pdf", "svg"):
        plt.savefig(f"{name}.{ext}")
    plt.savefig(f"{name}.png", dpi=200); plt.close()

# Figure 25.2: light in the inflow
x = np.linspace(0.35, 5, 600)                      # radius in units of the horizon radius
v = np.sqrt(1 / x)                                 # inflow speed / c
fig, (top, ax) = plt.subplots(2, 1, figsize=(7.2, 4.6), gridspec_kw={"height_ratios": [0.9, 2]}, sharex=True)
# top strip: the inflow, arrows pointing inward with length set by the inflow speed
for xa in [0.55, 0.85, 1.25, 1.7, 2.2, 2.9, 3.7, 4.6]:
    L = 0.3 * np.sqrt(1 / xa)
    top.add_patch(FancyArrowPatch((xa + L / 2, 0.55), (xa - L / 2, 0.55), arrowstyle="-|>", mutation_scale=9, color=GREY, lw=1.4))
    top.add_patch(FancyArrowPatch((xa - 0.12, 0.12), (xa + 0.12, 0.12), arrowstyle="-|>", mutation_scale=8, color=ORANGE, lw=1.4))
top.axvline(1, color=DARK, lw=1)
top.text(1.08, 0.88, "the inflow (grey): faster toward the centre", fontsize=7, color=GREY)
top.text(1.08, -0.12, "light sent outward (orange): always at c through the medium around it", fontsize=7, color=ORANGE)
top.set_ylim(-0.25, 1.05); top.axis("off")
# bottom: net outward progress of that light, c - v, as seen from far away
net = 1 - v
ax.fill_between(x, 0, net, where=net >= 0, color=BLUE, alpha=0.15, lw=0)
ax.fill_between(x, 0, net, where=net < 0, color=ORANGE, alpha=0.15, lw=0)
ax.plot(x, net, color=BLUE, lw=1.8)
ax.axhline(0, color=GREY, lw=0.7); ax.axvline(1, color=DARK, lw=1)
ax.text(2.6, 0.22, "light makes headway outward", color=BLUE, fontsize=7.5)
ax.text(0.4, 0.12, "light carried\ninward", color=ORANGE, fontsize=7.5)
ax.annotate("horizon: the inflow equals c;\nlight sent outward stands still", xy=(1, 0), xytext=(1.25, -0.55), fontsize=7,
            arrowprops=dict(arrowstyle="-", color=DARK, lw=0.6))
ax.set_ylabel("outward progress of light\n(fraction of c, seen from far away)", fontsize=7)
ax.set_xlabel("distance from the centre (horizon radii)")
ax.set_xlim(0.35, 5); ax.set_ylim(-0.75, 0.6)
for s in ("top", "right"): ax.spines[s].set_visible(False)
plt.tight_layout(); save("fig25-2-light")

# Figure 25.1: the sideways hold, weakened by the pressure ratio
x = np.linspace(1.05, 12, 1500)
fig, (ax, al) = plt.subplots(1, 2, figsize=(7.4, 3.6), gridspec_kw={"width_ratios": [2.2, 1]})
for l2, col, lab in [(4.0, BLUE, "more sideways motion: a hollow (stable orbit)\nand a crest"),
                     (3.0, DARK, "the last stable orbit: hollow and crest\nmerge at 3 horizon radii"),
                     (2.4, GREY, "less sideways motion: no hollow;\nno orbit holds")]:
    ax.plot(x, (1 - 1 / x) * (1 + l2 / x**2), color=col, lw=1.7, label=lab)
ax.plot([3], [(1 - 1 / 3) * (1 + 3 / 9)], "o", color=DARK, ms=4)
xm = 2 * (1 + np.sqrt(1 - 3 / 4)) ; xm = (4 + np.sqrt(16 - 12)) / 1  # hollow of l2=4 at x = l2(1+sqrt(1-3/l2))
xm = 4 * (1 + np.sqrt(1 - 3 / 4)); ax.plot([xm], [(1 - 1 / xm) * (1 + 4 / xm**2)], "o", color=BLUE, ms=4)
ax.set_xlabel("distance from the centre (horizon radii)")
ax.set_ylabel("pressure ratio \u00d7 (1 + sideways term)", fontsize=7.5)
ax.set_xlim(1, 12); ax.set_ylim(0.55, 1.12)
ax.legend(fontsize=6.6, frameon=False, loc="lower right")
ax.text(5.2, 1.04, "far out the curves level toward 1: Newton's orbits,\nwith the slow precession of Mercury", fontsize=6.6, color=DARK)
ax.set_title("A body with sideways motion", fontsize=8.5)
xl = np.linspace(1.0, 6, 400); Vl = (1 - 1 / xl) / xl**2
al.plot(xl, Vl / Vl.max(), color=ORANGE, lw=1.7); al.axvline(1.5, color=ORANGE, lw=0.7, ls="--")
al.text(3.0, 0.88, "one crest, at 1.5 horizon\nradii: light can circle\nthere, but not stay", fontsize=6.6, color=ORANGE)
al.set_title("Light", fontsize=8.5); al.set_yticks([]); al.set_xlabel("horizon radii"); al.set_ylim(0, 1.1)
for a_ in (ax, al):
    for s_ in ("top", "right"): a_.spines[s_].set_visible(False)
plt.tight_layout(); save("fig25-1-hold")
print("ok")
