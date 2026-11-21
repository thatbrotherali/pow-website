"""Figure 8.1: one set of numbers, read as curved geometry and as a medium flowing in."""
import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"font.family": "Inter", "font.size": 8})
BLUE = "#1F5FAD"; ORANGE = "#C8650A"; GREY = "#8A8A8A"; DARK = "#333333"
fig = plt.figure(figsize=(7.4, 3.9))
# left: Flamm's paraboloid, the curved-space picture of the region outside a mass
ax = fig.add_subplot(1, 2, 1, projection="3d")
r = np.linspace(1.02, 6, 40); th = np.linspace(0, 2 * np.pi, 60)
R, TH = np.meshgrid(r, th)
Z = 2 * np.sqrt(R - 1)
ax.plot_wireframe(R * np.cos(TH), R * np.sin(TH), Z, color=BLUE, lw=0.4, rstride=3, cstride=3)
ax.set_axis_off(); ax.view_init(elev=24, azim=-60)
ax.set_title("Read as geometry:\nspace curved around the mass", fontsize=8.5, pad=-4)
# right: flat space with the medium flowing in at the escape speed
ax2 = fig.add_subplot(1, 2, 2)
xs, ys, us, vs = [], [], [], []
for rr in [1.6, 2.3, 3.1, 4.1, 5.3]:
    for a in np.linspace(0, 2 * np.pi, 12, endpoint=False) + 0.25 * rr:
        sp = 1 / np.sqrt(rr)
        xs.append(rr * np.cos(a)); ys.append(rr * np.sin(a)); us.append(-sp * np.cos(a)); vs.append(-sp * np.sin(a))
ax2.quiver(xs, ys, us, vs, color=ORANGE, angles="xy", scale_units="xy", scale=0.9, width=0.006, headwidth=4)
ax2.text(4.0, -5.8, "longer arrow: faster inflow", fontsize=7, color=ORANGE, ha="center")
ax2.add_patch(plt.Circle((0, 0), 1, color=DARK))
ax2.set_xlim(-6, 6); ax2.set_ylim(-6, 6); ax2.set_aspect("equal"); ax2.axis("off")
ax2.set_title("Read as a medium:\nflat space, the medium flowing in at $\\sqrt{2GM/r}$", fontsize=8.5)
fig.text(0.5, 0.04, "The same numbers either way: clocks slowed by $\\sqrt{1-2GM/rc^2}$; light bent 1.75″ at the Sun's edge; "
         "Mercury's orbit turned 43″ a century.", ha="center", fontsize=7.6, color=DARK)
plt.subplots_adjust(left=0.01, right=0.99, top=0.86, bottom=0.12, wspace=0.05)
for ext in ("pdf", "svg"): plt.savefig(f"fig08-1-two-readings.{ext}")
plt.savefig("fig08-1-two-readings.png", dpi=200)
