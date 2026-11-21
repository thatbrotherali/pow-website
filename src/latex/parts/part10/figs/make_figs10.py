"""Figures for Part 10."""
import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"font.family": "Inter", "font.size": 8})
BLUE = "#1F5FAD"; ORANGE = "#C8650A"; GREY = "#8A8A8A"; DARK = "#333333"
def save(name):
    for ext in ("pdf", "svg"): plt.savefig(f"{name}.{ext}")
    plt.savefig(f"{name}.png", dpi=200); plt.close()

# Figure 10.1: rays through a graded index n = 1 + k/r (strength exaggerated)
k = 0.06
def n(x, y): return 1 + k / np.hypot(x, y)
def grad(x, y):
    r = np.hypot(x, y); return -k * x / r**3, -k * y / r**3
fig, ax = plt.subplots(figsize=(7.0, 3.6))
X, Y = np.meshgrid(np.linspace(-6, 10, 400), np.linspace(-3.2, 3.2, 200))
ax.imshow(np.log(n(X, Y) - 1), extent=(-6, 10, -3.2, 3.2), origin="lower", cmap="Blues", alpha=0.55, aspect="auto")
for b in [0.6, 0.9, 1.3, 1.8, 2.5, -0.6, -0.9, -1.3, -1.8, -2.5]:
    x, y = -6.0, b; px, py = n(x, y), 0.0   # optical momentum n*direction
    xs, ys = [x], [y]; ds = 0.01
    while x < 10 and abs(y) < 3.2 and np.hypot(x, y) > 0.3:
        gx, gy = grad(x, y); px += gx * ds; py += gy * ds
        nn = n(x, y); x += px / nn * ds * nn / np.hypot(px, py) ; y += py / nn * ds * nn / np.hypot(px, py)
        xs.append(x); ys.append(y)
    ax.plot(xs, ys, color=ORANGE, lw=1.1)
ax.plot(0, 0, "o", color=DARK, ms=9)
ax.text(0.35, -0.55, "mass", fontsize=7.5, color=DARK)
ax.text(-5.8, 2.75, "light enters in parallel", fontsize=7, color=ORANGE)
ax.text(4.2, 2.75, "the index is higher near the mass (darker):\nlight slows and turns toward it, as in a lens", fontsize=7, color=DARK)
ax.set_xlim(-6, 10); ax.set_ylim(-3.2, 3.2); ax.set_xticks([]); ax.set_yticks([])
ax.set_title("Refraction in a graded medium (strength exaggerated)", fontsize=8.5)
plt.tight_layout(); save("fig10-1-refraction")

# Figure 10.2: clock offset of a Galileo satellite in its eccentric orbit
GM = 3.986004418e14; c = 299792458.0; a = 27977.6e3; e = 0.162
T = 2 * np.pi * np.sqrt(a**3 / GM)
M = np.linspace(0, 4 * np.pi, 2000); E = M.copy()
for _ in range(60): E = M + e * np.sin(E)
dt = -2 * np.sqrt(GM * a) / c**2 * e * np.sin(E)      # clock minus steady time: periodic part, seconds
t = M / (2 * np.pi) * T / 3600
fig, ax = plt.subplots(figsize=(7.0, 2.8))
ax.plot(t, dt * 1e9, color=BLUE, lw=1.8)
for kk in range(3):
    ax.axvline(kk * T / 3600, color=GREY, lw=0.6, ls=":")
ax.text(0.3, 150, "around closest approach\nthe clock loses time", fontsize=7, color=DARK)
ax.text(T / 3600 / 2 + 0.4, -250, "around the farthest point\nit gains time", fontsize=7, color=DARK)
ax.set_xlabel("hours"); ax.set_ylabel("clock offset (nanoseconds)")
ax.set_title(f"An eccentric Galileo satellite: the clock's rate follows its distance (amplitude {2*np.sqrt(GM*a)/c**2*e*1e9:.0f} ns)", fontsize=8)
for s in ("top", "right"): ax.spines[s].set_visible(False)
plt.tight_layout(); save("fig10-2-galileo")
print("galileo amplitude ns", 2 * np.sqrt(GM * a) / c**2 * e * 1e9, "period h", T / 3600)

# Figure 10.3: gravity signal at c arrives before seismic waves
d = np.linspace(0, 3000, 100)
fig, ax = plt.subplots(figsize=(6.6, 3.0))
ax.plot(d, d * 1e3 / c, color=ORANGE, lw=2, label="change in gravity: at the speed of light (1000 km in 3 ms)")
ax.plot(d, d / 8.0, color=BLUE, lw=1.8, label="first seismic waves (P waves): about 8 km/s")
ax.fill_between(d, d * 1e3 / c, d / 8.0, color=ORANGE, alpha=0.12)
ax.text(1900, 120, "the window in which the gravity signal\nwas recorded before the ground shook", fontsize=7, color=DARK)
ax.axvspan(500, 3000, color=GREY, alpha=0.07)
ax.text(1700, 20, "range of the stations that recorded it\n(2011 Tohoku earthquake)", fontsize=6.8, color=GREY)
ax.set_xlabel("distance from the earthquake (km)"); ax.set_ylabel("arrival time (seconds)")
ax.legend(frameon=False, fontsize=7, loc="upper left"); ax.set_ylim(-5, 420)
for s in ("top", "right"): ax.spines[s].set_visible(False)
plt.tight_layout(); save("fig10-3-pegs")
