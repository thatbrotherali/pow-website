"""Figure 5.1: the medium around the Earth: one inflow, three bodies in it, and its numbers with height."""
import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, FancyArrowPatch
plt.rcParams.update({"font.family": "Inter", "font.size": 8})
BLUE = "#1F5FAD"; ORANGE = "#C8650A"; GREY = "#8A8A8A"; DARK = "#333333"; GREEN = "#2E7D4F"
GM = 3.986004e14; R = 6.371e6; c = 2.99792458e8
fig = plt.figure(figsize=(7.4, 3.9))
# (a) the inflow and three bodies in it
ax = fig.add_axes([0.0, 0.02, 0.5, 0.9])
ax.add_patch(Circle((0, -6.0), 4.2, color="#6B8FB5", zorder=1))
ax.text(0, -2.75, "Earth", color="white", ha="center", fontsize=9, zorder=2)
for x in np.linspace(-3.9, 3.9, 9):
    for y in [3.0, 1.3, -0.4]:
        if np.hypot(x - (-2.4), y - 1.2) < 1.4 or np.hypot(x - 2.4, y - 0.2) < 1.4 or (abs(x - 2.4) < 0.6 and y < 0) or (abs(x + 2.4) < 1.3 and y < 0.2) or (x > 2 and y < 0): continue
        d = np.hypot(x, y + 6.0); sp = 2.2 / np.sqrt(d)
        ux, uy = -x / d, -(y + 6.0) / d
        ax.annotate("", xy=(x + 0.9 * sp * ux, y + 0.9 * sp * uy), xytext=(x, y),
                    arrowprops=dict(arrowstyle="-|>", color=ORANGE, lw=0.9, alpha=0.75), zorder=1)
# falling ball: delivery to every particle, equal arrows
fx, fy = -2.4, 1.2
ax.add_patch(Circle((fx, fy), 0.55, facecolor="white", edgecolor=DARK, lw=1, zorder=3))
for dx, dy in [(-0.25, 0.2), (0.2, 0.25), (-0.2, -0.2), (0.22, -0.18), (0, 0)]:
    ax.annotate("", xy=(fx + dx, fy + dy - 0.28), xytext=(fx + dx, fy + dy),
                arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=1), zorder=4)
ax.text(fx, fy + 0.8, "Let go: carried", ha="center", fontsize=8, color=DARK, weight="bold")
ax.text(fx, fy - 1.35, "momentum $mg$ each second\nto every particle alike;\nnothing is compressed", ha="center", fontsize=6.8, color=DARK)
# held ball on a stand: same delivery relayed into the support
hx, hy = 2.4, 0.2
ax.add_patch(Rectangle((hx - 0.15, -2.0), 0.3, hy - 0.55 + 2.0, color=GREY, zorder=2))
ax.add_patch(Circle((hx, hy), 0.55, facecolor="white", edgecolor=DARK, lw=1, zorder=3))
for dx, dy in [(-0.25, 0.2), (0.2, 0.25), (0, 0)]:
    ax.annotate("", xy=(hx + dx, hy + dy - 0.28), xytext=(hx + dx, hy + dy),
                arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=1), zorder=4)
ax.annotate("", xy=(hx, -1.8), xytext=(hx, hy - 0.6), arrowprops=dict(arrowstyle="-|>", color=GREEN, lw=2), zorder=5)
ax.text(hx, hy + 0.8, "Held: the same current", ha="center", fontsize=8, color=DARK, weight="bold")
ax.text(hx + 0.35, -0.9, "relayed into\nthe support;\na scale reads\nits rate", ha="left", fontsize=6.8, color=GREEN)
# clock
ax.text(0, 4.15, "Everywhere: the medium streams through every body at the inflow speed,\n11.2 km/s at the ground, slowing every clock by $\\sqrt{P/P_0}$",
        ha="center", fontsize=7, color=ORANGE)
ax.set_xlim(-4.3, 4.3); ax.set_ylim(-3.2, 4.8); ax.set_aspect("equal"); ax.axis("off")
ax.set_title("(a) One inflow, two destinations", fontsize=8.5, loc="left", x=0.04)
# (b) the inflow speed and the clock rate with height
ax2 = fig.add_axes([0.57, 0.16, 0.34, 0.68])
h = np.linspace(0, 40000e3, 400); r = R + h
v = np.sqrt(2 * GM / r)
ax2.plot(h / 1e3, v / 1e3, color=ORANGE, lw=1.6)
ax2.set_xlabel("height above the ground (km)"); ax2.set_ylabel("inflow speed (km/s)", color=ORANGE)
ax2.tick_params(axis="y", colors=ORANGE); ax2.set_ylim(0, 12)
ax3 = ax2.twinx()
loss = 0.5 * (2 * GM / r) / c**2 * 86400e6
ax3.plot(h / 1e3, loss, color=BLUE, lw=1.2, ls="--")
ax3.set_ylabel("clock slowing (μs per day)", color=BLUE); ax3.tick_params(axis="y", colors=BLUE); ax3.set_ylim(0, 65)
hg = 20200e3; vg = np.sqrt(2 * GM / (R + hg))
ax2.axvline(hg / 1e3, color=GREY, lw=0.6, ls=":")
ax2.text(hg / 1e3 + 600, 11.2, "GPS orbit", fontsize=7, color=GREY)
d_g = 0.5 * (2 * GM / R - 2 * GM / (R + hg)) / c**2 * 86400e6
d_m = 0.5 * (GM / (R + hg)) / c**2 * 86400e6
ax2.text(4500, 0.4, f"GPS clock, slower stream: +{d_g:.1f} μs/day\nits own motion: −{d_m:.1f} μs/day\nnet: +{d_g - d_m:.1f} μs/day", fontsize=6.6, color=DARK)
for s in ["top"]: ax2.spines[s].set_visible(False); ax3.spines[s].set_visible(False)
ax2.set_title("(b) The inflow and clocks with height", fontsize=8.5, loc="left")
for ext in ["pdf", "svg", "png"]:
    fig.savefig(f"fig05-1-inflow.{ext}", dpi=200)
print(d_g, d_m, d_g - d_m, np.sqrt(2 * GM / R))
