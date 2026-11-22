"""Figure 1.4: the thirty parts of the framework, in the groups of Part 30."""
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
plt.rcParams.update({"font.family":"Inter","font.size":8})
BLUE="#1F5FAD"; DARK="#333333"; MID="#555555"; FILL="#F3F2EF"; EDGE="#DDDAD3"
G=[("The question","Parts 1–4","What gravity does, how it was\nexplained, and how description\ncame to stand in for mechanism"),
   ("The mechanism","Parts 5–8","The inflow; holding as throughput;\nevery force with its carrier;\nthe break, stated fairly"),
   ("The evidence","Parts 9–13","Evidence weighed and graded;\nthe four forces; the limits of\nknowledge; the Moon and life"),
   ("Foundations","Parts 14–19","The framework in one piece;\ngravitons; fields; mass;\ntime; the pathway to matter"),
   ("Order in matter","Parts 20–22","Coherence; the corridors\nflows pass along;\nmagnetism"),
   ("The numbers","Parts 23–28","Equations; units and constants;\nthe inflow to the speed of light;\norbits; force; light"),
   ("The tests","Part 29","Every result read as a medium,\nand the tests that could decide"),
   ("Conclusion","Part 30","The restoration\nof reality")]
fig,ax=plt.subplots(figsize=(8.6,4.0)); ax.set_xlim(0,4); ax.set_ylim(0,2); ax.axis("off")
for i,(t,p,d) in enumerate(G):
    c,r=i%4,1-i//4
    ax.add_patch(FancyBboxPatch((c+0.04,r+0.05),0.92,0.9,boxstyle="round,pad=0,rounding_size=0.05",fc=FILL,ec=EDGE,lw=1))
    ax.text(c+0.5,r+0.80,t,ha="center",va="center",fontsize=10,weight="bold",color=DARK)
    ax.text(c+0.5,r+0.66,p,ha="center",va="center",fontsize=9,color=BLUE)
    ax.text(c+0.5,r+0.34,d,ha="center",va="center",fontsize=7.6,color=MID,linespacing=1.4)
fig.tight_layout(pad=0.2)
for ext in ("pdf","svg","png"): fig.savefig(f"figs/fig1-4-parts-map.{ext}",dpi=200)
