import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Rectangle, Circle
plt.rcParams.update({"font.family":"DejaVu Sans","font.size":9})
BLUE="#1F5FAD"; ORANGE="#C8650A"; GREY="#555555"; RED="#B03A2E"

# ---------- Figure 28.1: where a wave's energy is ----------
x=np.linspace(0,2,600); k=2*np.pi
fig,ax=plt.subplots(2,2,figsize=(7.2,4.6),sharex=True,gridspec_kw={"height_ratios":[1,1]})
# travelling: snapshot
y=np.sin(k*x); vel=-np.cos(k*x)  # dy/dt for y=sin(kx-wt) at t=0 (scaled)
slope=np.cos(k*x)
ax[0,0].plot(x,y,color="black",lw=1.6); ax[0,0].axhline(0,color=GREY,lw=0.5,ls=":")
ax[0,0].set_title("Travelling wave: one moment",fontsize=9.5,fontweight="bold")
ax[0,0].annotate("crest: flat and still",xy=(0.25,1),xytext=(0.42,1.35),fontsize=8,arrowprops=dict(arrowstyle="-",color=GREY,lw=0.6))
ax[0,0].annotate("crossing: steepest\nand fastest",xy=(1.0,0),xytext=(1.15,-1.55),fontsize=8,arrowprops=dict(arrowstyle="-",color=GREY,lw=0.6))
ax[0,0].set_ylim(-1.8,1.8); ax[0,0].set_yticks([]); ax[0,0].set_ylabel("string")
ax[1,0].fill_between(x,vel**2,color=BLUE,alpha=0.35,lw=0,label="motion energy")
ax[1,0].plot(x,slope**2,color=ORANGE,lw=1.6,ls="--",label="stretch energy")
ax[1,0].set_ylim(0,1.75); ax[1,0].set_yticks([]); ax[1,0].set_ylabel("energy along\nthe string")
ax[1,0].legend(loc="upper right",bbox_to_anchor=(1,0.86),fontsize=7.5,frameon=False,ncol=2)
ax[1,0].text(0.02,1.58,"Together, everywhere: energy is handed on",fontsize=7.8,color="black")
# standing: two instants
ys=np.sin(k*x/2*2)  # shape
ax[0,1].plot(x,np.sin(k*x),color="black",lw=1.6,label="most bent")
ax[0,1].plot(x,0*x,color=GREY,lw=1.6,ls="-",alpha=0.6,label="a quarter-cycle later: flat")
ax[0,1].set_title("Standing wave: two moments",fontsize=9.5,fontweight="bold")
ax[0,1].legend(loc="lower right",fontsize=7.2,frameon=False)
ax[0,1].set_ylim(-1.8,1.8); ax[0,1].set_yticks([])
for n in [0,0.5,1,1.5,2]: ax[0,1].plot(n,0,"o",ms=3,color=RED)
ax[0,1].text(0.52,0.12,"nodes",color=RED,fontsize=7.5)
ax[1,1].plot(x,np.cos(k*x)**2,color=ORANGE,lw=1.6,ls="--",label="most bent: all stretch")
ax[1,1].fill_between(x,np.sin(k*x)**2,color=BLUE,alpha=0.35,lw=0,label="flat: all motion")
ax[1,1].set_ylim(0,1.75); ax[1,1].set_yticks([])
ax[1,1].legend(loc="upper right",bbox_to_anchor=(1,0.86),fontsize=7.2,frameon=False,ncol=2)
ax[1,1].text(0.02,1.58,"They swap: energy stays and sloshes",fontsize=7.8)
for a in ax.flat:
    for s in ["top","right"]: a.spines[s].set_visible(False)
    a.set_xticks([])
plt.tight_layout(); plt.savefig("fig28-1-energy.pdf"); plt.savefig("fig28-1-energy.png",dpi=200)

# ---------- Figure 28.2: where a circuit's energy travels ----------
fig,ax=plt.subplots(figsize=(7.0,3.6)); ax.set_xlim(0,10); ax.set_ylim(0,5); ax.axis("off")
# wires
ax.plot([1.3,8.6],[4.0,4.0],color="#8C6D3F",lw=4,solid_capstyle="butt")
ax.plot([1.3,8.6],[1.0,1.0],color="#8C6D3F",lw=4,solid_capstyle="butt")
# battery
ax.add_patch(Rectangle((0.7,1.0),0.6,3.0,fc="#DDDDDD",ec="black"))
ax.text(1.0,2.5,"battery",rotation=90,ha="center",va="center",fontsize=8.5)
ax.text(1.5,4.25,"+",fontsize=11); ax.text(1.5,0.55,"−",fontsize=12)
# lamp / resistor
ax.add_patch(Rectangle((8.6,1.6),0.55,1.8,fc="#F6E3B4",ec="black"))
ax.plot([8.875,8.875],[1.0,1.6],color="#8C6D3F",lw=4); ax.plot([8.875,8.875],[3.4,4.0],color="#8C6D3F",lw=4)
ax.text(9.35,2.5,"lamp",rotation=90,ha="center",va="center",fontsize=8.5)
# energy arrows through space between wires
for xx in [2.4,3.8,5.2,6.6]:
    for yy in [1.8,2.5,3.2]:
        ax.add_patch(FancyArrowPatch((xx,yy),(xx+0.9,yy),arrowstyle="-|>",mutation_scale=11,color=BLUE,lw=1.4))
for yy in [1.9,2.5,3.1]:
    ax.add_patch(FancyArrowPatch((7.8,yy),(8.55,yy),arrowstyle="-|>",mutation_scale=11,color=BLUE,lw=1.6))
ax.text(4.9,4.55,"Energy travels through the space around the wires, from battery to lamp,\nand enters the lamp from the side (Poynting, 1884)",ha="center",fontsize=8.3,color=BLUE)
# electrons drifting slowly in wire
for xx in np.linspace(2.2,7.6,7):
    ax.add_patch(Circle((xx,1.0),0.07,color=ORANGE,zorder=5))
    ax.add_patch(FancyArrowPatch((xx-0.15,0.72),(xx+0.15,0.72),arrowstyle="-|>",mutation_scale=7,color=ORANGE,lw=0.9))
ax.text(4.9,0.15,"Electrons in the wire drift at about 0.07 mm/s (1 A in 1 mm² of copper);\nswitched on, the lamp lights at once, because the energy does not ride on them",ha="center",fontsize=8.3,color=ORANGE)
plt.tight_layout(); plt.savefig("fig28-2-circuit.pdf"); plt.savefig("fig28-2-circuit.png",dpi=200)
print("ok")
