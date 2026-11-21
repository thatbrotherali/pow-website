"""Figure 1.1: three accounts of the same falling apple (second edition: GPT panel shows the inflow and carrying)."""
import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Ellipse, Rectangle
plt.rcParams.update({"font.family": "Inter", "font.size": 9})
RED = "#E04848"; EARTH = "#D9D6CF"; EDGE = "#555555"; GREEN = "#1FA36A"; ORANGE = "#E07A2E"; BLUE = "#2F6FD0"; GREY = "#666666"; NAVY = "#3A4A6B"
fig = plt.figure(figsize=(9.6, 4.2))
def arrow(ax, x0, y0, x1, y1, color, lw=1.6, hw=0.22):
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0), arrowprops=dict(arrowstyle=f"-|>,head_width={hw},head_length={hw*1.6}", color=color, lw=lw))
# Newton
a = fig.add_axes([0.0, 0.0, 0.25, 0.86]); a.set_xlim(1, 9); a.set_ylim(0, 12); a.axis("off")
a.set_title("Newton:\na force, no carrier", fontsize=11)
a.text(5, 11.2, "what carries it?", ha="center", style="italic", color=GREY)
a.add_patch(Circle((5, 8.8), 0.75, color=RED))
arrow(a, 5, 7.7, 5, 3.6, "black", 1.8)
a.text(5.5, 5.6, "F = GMm/r²", fontsize=10)
a.text(2.7, 5.4, "?", fontsize=22, color=ORANGE, weight="bold", ha="center")
a.add_patch(Rectangle((1.2, 0.6), 7.6, 1.6, color=EARTH)); a.text(5, 1.15, "Earth", ha="center", color=GREY)
# GR
b = fig.add_axes([0.27, 0.0, 0.25, 0.86]); b.set_xlim(1, 9); b.set_ylim(0, 12); b.axis("off")
b.set_title("General Relativity:\ngeometry, no force", fontsize=11)
b.text(5, 11.2, "curvature described; no carrier named", ha="center", style="italic", color=GREY)
xs = np.linspace(1.3, 8.7, 11)
for y0 in np.linspace(2.0, 10.0, 9):
    yy = y0 - 1.6 * np.exp(-((xs - 5) ** 2) / 6) * (1 - (y0 - 2) / 12)
    b.plot(xs, yy, color="#DDDDDD", lw=0.8)
for x0 in xs:
    ys = np.linspace(1.6, 10.0, 30)
    b.plot(x0 + (5 - x0) * 0.08 * np.exp(-((ys - 2.4) ** 2) / 8), ys, color="#DDDDDD", lw=0.8)
b.add_patch(Circle((5, 8.6), 0.7, color=RED))
b.plot([5, 5], [7.8, 3.0], color=BLUE, lw=2, ls=(0, (3, 2)))
b.text(5.4, 5.4, "geodesic\n(unforced)", fontsize=9.5)
b.add_patch(Ellipse((5, 2.3), 4.2, 1.4, color=EARTH)); b.text(5, 2.15, "Earth", ha="center", color=GREY)
# GPT
c = fig.add_axes([0.54, 0.0, 0.46, 0.86]); c.set_xlim(0, 14.67); c.set_ylim(0, 12); c.axis("off")
c.set_title("Graviton Pressure Theory:\na medium flowing into every mass", fontsize=11)
ex, ey, R = 6.0, 3.2, 2.0
# lowered pressure: faint glow around the Earth
for k, rr in enumerate(np.linspace(6.5, 2.1, 14)):
    c.add_patch(Circle((ex, ey), rr, color=NAVY, alpha=0.018, lw=0))
# inflow arrows: speed ~ 1/sqrt(r)
rng = np.random.default_rng(3)
for rr in [3.0, 4.2, 5.6, 7.2]:
    n = int(10 + rr * 2)
    for t in np.linspace(0, 2 * np.pi, n, endpoint=False) + rr:
        x, y = ex + rr * np.cos(t), ey + rr * np.sin(t)
        if not (0.4 < x < 13.6 and 0.3 < y < 10.6): continue
        if np.hypot(x - ex, y - 9.0) < 1.5: continue
        L = 1.25 / np.sqrt(rr / 3.0); x1, y1 = x - L * np.cos(t), y - L * np.sin(t)
        def bad(px, py): return (px > 9.0 and (7.0 < py < 9.6 or 4.1 < py < 6.7)) or py < 1.0
        if bad(x, y) or bad(x1, y1): continue
        L = 1.25 / np.sqrt(rr / 3.0)
        arrow(c, x, y, x - L * np.cos(t), y - L * np.sin(t), GREEN, 1.1, 0.14)
c.add_patch(Circle((ex, ey), R, facecolor=EARTH, edgecolor=EDGE, lw=1)); c.text(ex, ey - 0.15, "Earth", ha="center", color=GREY, fontsize=10)
# the apple, carried: equal arrows on its particles
ax_, ay = ex, 9.0
c.add_patch(Circle((ax_, ay), 0.85, color=RED))
for dx, dy in [(-0.38, 0.3), (0.3, 0.35), (0, 0), (-0.35, -0.3), (0.35, -0.28)]:
    arrow(c, ax_ + dx, ay + dy + 0.12, ax_ + dx, ay + dy - 0.28, "white", 1.1, 0.12)
c.text(9.3, 8.3, "the apple is carried:\nmomentum given to\nevery particle alike", fontsize=9, color="black", va="center")
c.text(9.3, 5.4, "the medium flows in,\nfaster closer to the Earth;\nits pressure is lowered\nwhere it flows fastest", fontsize=9, color=NAVY, va="center")
c.text(ex, 0.55, "matter takes the medium in and returns it inactive", ha="center", fontsize=8.6, color=GREEN)
c.text(0.3, 11.15, "HYPOTHESIS", fontsize=9.5, color=ORANGE, weight="bold")
for ext in ("svg", "pdf", "png"):
    fig.savefig(f"fig1-1-three-apples.{ext}", dpi=170)
