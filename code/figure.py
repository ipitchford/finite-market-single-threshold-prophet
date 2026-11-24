#!/usr/bin/env python3
"""Rebuild figures/frontier.pdf from the finite-market formulas; requires matplotlib."""
from pathlib import Path
from math import sqrt
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from check_extensions import U, Q, tagged, root, finite_gap

plt.rcParams.update({"font.family":"DejaVu Sans","font.size":8.5,"axes.spines.top":False,
                     "axes.spines.right":False,"pdf.fonttype":42,"axes.labelcolor":"#302f36",
                     "xtick.color":"#393840","ytick.color":"#393840"})
fig,(left,right)=plt.subplots(1,2,figsize=(6.45,2.53),layout="constrained")
teal,plum,ochre="#12686a","#763e69","#a4631b"
qs=[.22+i*.72/180 for i in range(181)]
base=lambda q: U(3,root(lambda p: Q(3,p,2)-q),2)
tag=lambda q: 1-q/3
qstar=root(lambda q: base(q)-tag(q))
left.plot(qs,[base(q) for q in qs],color=teal,label="Utilisation")
left.plot(qs,[tag(q) for q in qs],color=plum,label="Tagged acceptance")
left.plot(qstar,tag(qstar),'o',color="#233438",ms=4.5)
left.annotate("Best target",xy=(qstar,tag(qstar)),xytext=(.32,.82),fontsize=7.4,
              arrowprops={"arrowstyle":"-","color":"#555","lw":.8})
left.set(xlabel="Probability of filling both places",ylabel="Guaranteed fraction",
         ylim=(.49,.99),xlim=(.2,.95))
left.legend(loc="lower right",frameon=False,fontsize=7.2)
left.set_title("Three applicants, two places",loc="left",fontsize=9.4,fontweight="bold")
ns=[5,6,8,10,15,20,30,50,100,200,500]
for k,col,label in [(2,teal,"Two places"),(3,ochre,"Three places")]:
    vals=[n*n*finite_gap(n,k,k) for n in ns]
    right.plot(ns,vals,'o-',color=col,ms=2.6,lw=1.3,label=label)
    from math import exp,factorial
    masses=[exp(-k)*k**j/factorial(j) for j in range(k+1)]
    c=1-masses[k]
    limit=.5*sum((k-1-j)*masses[j] for j in range(k-1))*(1-sum(masses))/c
    right.axhline(limit,ls=":",color=col,lw=1)
right.set(xscale="log",xlabel="Number of applicants",ylabel="Guarantee difference × n²")
right.set_xticks([5,10,50,100,500],labels=["5","10","50","100","500"])
right.tick_params(which="minor",bottom=False)
right.set_title("Cost of a fixed stockout target",loc="left",fontsize=9.4,fontweight="bold")
right.legend(loc="upper right",frameon=False,fontsize=7.2)
for ax in (left,right): ax.grid(axis="y",color="#dedbdb",lw=.55)
fig.savefig(Path(__file__).resolve().parent.parent / "figures" / "frontier.pdf")
