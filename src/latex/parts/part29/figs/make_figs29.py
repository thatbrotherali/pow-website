"""Figure 29.1: the configuration weighing, sizes of what it must control, against the window where any effect would be GPT's."""
import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"font.family": "Inter", "font.size": 8})
GREY = "#8A8A8A"; DARK = "#333333"; ORANGE = "#C8650A"; BLUE = "#1F5FAD"; GREEN = "#2E7D4F"
rows = [  # label, low, high, colour, note
    ("Buoyancy in air, honeycomb vs solid", 1e-5, 1e-3, GREY, "removed in vacuum"),
    ("Water held on extra surface, per m²", 1e-7, 1e-6, GREY, "reduced by baking, equal surface area"),
    ("Centre of mass 1 cm higher", 3.1e-9, 3.1e-9, GREY, "match heights to a fraction of a millimetre"),
    ("Centre of mass 0.1 mm higher", 3.1e-11, 3.1e-11, GREY, ""),
    ("Mass comparator, 1 kg, repeatability", 1e-11, 1e-10, BLUE, "what can be resolved"),
    ("Stored energy (standard: ΔE/c²)", 1e-15, 1e-14, GREEN, "all standard physics expects"),
    ("Free fall, different materials (MICROSCOPE)", 1e-15, 1e-15, DARK, "tests falling, not holding"),
]
fig, ax = plt.subplots(figsize=(7.4, 3.6))
ax.axvspan(1e-14, 1e-10, color=ORANGE, alpha=0.10, lw=0)
ax.text(1.2e-12, len(rows) - 0.25, "window: a difference here, at matched height\nin vacuum, is beyond what standard physics expects", ha="center", va="bottom", fontsize=6.8, color=ORANGE)
for i, (lab, lo, hi, col, note) in enumerate(rows):
    y = len(rows) - 1 - i
    if lo == hi: ax.plot([lo], [y], "o", color=col, ms=5)
    else: ax.plot([lo, hi], [y, y], color=col, lw=5, solid_capstyle="butt")
    if note: ax.text(max(hi, lo) * 2.6, y, note, ha="left", va="center", fontsize=6.4, color=GREY)
ax.set_xscale("log"); ax.set_xlim(3e-16, 3e-1); ax.set_ylim(-0.6, len(rows) + 0.5)
ax.set_yticks(range(len(rows))); ax.set_yticklabels([r[0] for r in rows][::-1], fontsize=7.2); ax.tick_params(axis="y", length=0); ax.set_xlabel("fractional change in the reading of a 1 kg weighing")
for s in ("left", "right", "top"): ax.spines[s].set_visible(False)
ax.set_xticks([1e-15, 1e-13, 1e-11, 1e-9, 1e-7, 1e-5, 1e-3])
fig.tight_layout()
for ext in ("pdf", "svg", "png"): fig.savefig(f"figs/fig29-1-weighing.{ext}" if False else f"fig29-1-weighing.{ext}", dpi=200)
