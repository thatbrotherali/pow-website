"""Figure 27.1: why surfaces in step grip and surfaces out of step glide (a model of Dienwiebel et al. 2004)."""
import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"font.family": "Inter", "font.size": 8})
BLUE = "#1F5FAD"; ORANGE = "#C8650A"; GREY = "#8A8A8A"

N = 12                       # atoms in the rigid layer
cases = [("Layers in step", 1.0, BLUE, "one rigid layer: every atom over a hollow,\nso all must climb out together",
          "large, regular peaks: high friction"),
         ("Layers out of step", 0.72, ORANGE, "one rigid layer, different spacing: some atoms\nover hollows, some over crests; the pushes cancel",
          "nearly flat: almost no friction")]
fig, ax = plt.subplots(2, 2, figsize=(7.4, 4.4), gridspec_kw={"height_ratios": [1, 1.15]})
fig.suptitle("A MODEL of a measured effect: graphite flakes turned out of step with the surface beneath slide almost freely (Dienwiebel et al., 2004)",
             fontsize=6.5, color="#555555", x=0.02, ha="left")
xs = np.linspace(-0.5, 12.5, 1200)
d = np.linspace(0, 3, 600)
for col, (title, a, c, note, verdict) in enumerate(cases):
    t = ax[0, col]
    surf = 0.35 * np.cos(2 * np.pi * xs)              # crests at whole numbers, hollows at half-integers
    t.fill_between(xs, -1.2, surf, color="#EEF0F2", lw=0)
    t.plot(xs, surf, color=GREY, lw=1.0)
    atoms = 0.5 + a * np.arange(N) + (12 - a * (N - 1) - 1) / 2 * (a != 1)
    t.plot(atoms, np.full(N, 0.75), "o", color=c, ms=5)
    t.plot([atoms[0], atoms[-1]], [0.75, 0.75], color=c, lw=1.2)
    for xa in atoms:
        t.plot([xa, xa], [0.75, 0.35 * np.cos(2 * np.pi * xa)], color=c, lw=0.6, ls=":")
    t.text(12.6, -0.75, "surface\nbelow", fontsize=6.5, color="#555555")
    t.set_title(title, fontsize=8.5)
    t.text(6, 1.25, note, ha="center", fontsize=6.5, color="#333333")
    t.set_xlim(-0.6, 13.8); t.set_ylim(-1.2, 1.9); t.axis("off")
    # resistance to sliding per atom: the average of each atom's sideways push
    f = np.mean([np.sin(2 * np.pi * (d + 0.5 + a * j)) for j in range(N)], axis=0)
    f = f / 1.0
    b = ax[1, col]
    b.axhline(0, color=GREY, lw=0.6)
    b.plot(d, f, color=c, lw=1.6)
    b.set_ylim(-1.15, 1.15); b.set_xlim(-0.05, 3.05)
    b.set_title(verdict, fontsize=7)
    b.set_xlabel("distance slid (atomic spacings)", fontsize=7)
    if col == 0: b.set_ylabel("resistance to sliding\n(per atom)", fontsize=7)
    for s in ("top", "right"): b.spines[s].set_visible(False)
    b.tick_params(labelsize=6.5)
plt.tight_layout(rect=(0, 0, 1, 0.95))
for ext in ("pdf", "svg"):
    plt.savefig(f"fig27-1-friction.{ext}")
plt.savefig("fig27-1-friction.png", dpi=200)
print("ok", np.abs(np.mean([np.sin(2*np.pi*(d+0.5+0.72*j)) for j in range(N)],axis=0)).max())
