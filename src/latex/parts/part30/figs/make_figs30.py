"""Figure 30.1: one medium, one inflow, and what it reproduces, predicts and still owes."""
import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle
plt.rcParams.update({"font.family": "Inter", "font.size": 8})
GREY="#8A8A8A"; DARK="#333333"; ORANGE="#C8650A"; BLUE="#1F5FAD"; GREEN="#2E7D4F"
items=[ # text, colour, angle(deg)
 ("Every body falls alike\n1 part in 10$^{15}$", BLUE, 90),
 ("Clocks: GPS gains\n38.5 µs a day", BLUE, 58),
 ("Light bent 1.75″\nat the Sun's edge", BLUE, 28),
 ("Mercury turned\n43″ a century", BLUE, 0),
 ("Gyroscopes turned\n37 mas a year", BLUE, -28),
 ("Waves at the\nspeed of light", BLUE, -58),
 ("Horizon where the\ninflow reaches c", BLUE, -90),
 ("Galaxies: one\nscale, a$_0$", GREEN, -122),
 ("Held weight and\nstructure", ORANGE, -152),
 ("Star pairs sorted\nby direction", ORANGE, 180),
 ("A spinning body's\nimprint", ORANGE, 152),
 ("Clusters, the third\npeak: owed", GREY, 122),
]
fig,ax=plt.subplots(figsize=(6.6,6.0)); ax.set_xlim(-1.62,1.62); ax.set_ylim(-1.42,1.42); ax.set_aspect("equal"); ax.axis("off")
R=1.08
for t,c,a in items:
    x,y=R*np.cos(np.radians(a)),R*np.sin(np.radians(a))
    ax.plot([0.43*x/R, x*0.78],[0.43*y/R, y*0.78],color=c,lw=1.1,alpha=0.7,ls="-" if c in (BLUE,GREEN) else "--")
    ax.text(x,y,t,ha="center",va="center",fontsize=7.4,color=c if c!=BLUE else DARK,
            bbox=dict(boxstyle="round,pad=0.45",fc="white",ec=c,lw=1.0))
ax.add_patch(Circle((0,0),0.42,fc="#EEF3FA",ec=BLUE,lw=1.4))
ax.text(0,0.13,"One medium",ha="center",va="center",fontsize=11,weight="bold",color=DARK)
ax.text(0,-0.04,"one inflow",ha="center",va="center",fontsize=9,color=DARK)
ax.text(0,-0.19,r"$v=\sqrt{2GM/r}$",ha="center",va="center",fontsize=9.5,color=BLUE)
# legend
lx=-1.6; ly=-1.36
for i,(lab,c) in enumerate([("measured, reproduced",BLUE),("measured, supports",GREEN),("predicted, untested",ORANGE),("owed",GREY)]):
    ax.plot([lx+i*0.82,lx+i*0.82+0.12],[ly,ly],color=c,lw=2)
    ax.text(lx+i*0.82+0.16,ly,lab,va="center",fontsize=6.8,color=DARK)
fig.tight_layout()
for ext in ("pdf","svg","png"): fig.savefig(f"figs/fig30-1-one-medium.{ext}",dpi=200)
