# -*- coding: utf-8 -*-
"""A06 teaser drawing (23 Oct 2026, click teaser): three precogs' crystal balls, each holding one of the teaser's questions.
Original drawing, no third-party artwork. Writes figures/teaser_precogs.png."""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Ellipse, FancyBboxPatch, Polygon

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INK, INK2, ACC, GOLD, BG, POOL = "#0b0b0b", "#52514e", "#2a78d6", "#c9a227", "#fcfcfb", "#dfeaf6"
fig, ax = plt.subplots(figsize=(4.2, 5.0), dpi=200); fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
ax.set_xlim(0, 10); ax.set_ylim(0, 12); ax.axis("off")
ax.text(5.0, 11.2, "THE PRECOGS", ha="center", va="center", fontsize=15, fontweight="bold", color=INK, family="DejaVu Sans")
ax.add_patch(Ellipse((5.0, 2.2), 9.2, 1.6, fc=POOL, ec=INK, lw=1.4))               # the pool the precogs lie in
labels = [("1", "beat\n1993?"), ("2", "when did\nit stop?"), ("3", "pure\nnoise?")]
for i, (n, lab) in enumerate(labels):
    cx, cy = 1.9 + i * 3.1, 6.6 + (0.5 if i == 1 else 0)
    ax.add_patch(Polygon([[cx - 0.9, cy - 2.6], [cx + 0.9, cy - 2.6], [cx + 0.5, cy - 1.45], [cx - 0.5, cy - 1.45]], closed=True, fc="#3b3a38", ec=INK, lw=1.3))
    ax.add_patch(Circle((cx, cy), 1.35, fc="white", ec=INK, lw=1.6))
    ax.add_patch(Ellipse((cx - 0.45, cy + 0.6), 0.55, 0.3, angle=30, fc="#eef3fa", ec="none"))   # glint
    ax.add_patch(Circle((cx, cy + 0.8), 0.26, fc=GOLD, ec=INK, lw=1.0)); ax.text(cx, cy + 0.8, n, ha="center", va="center", fontsize=8.5, fontweight="bold", color=INK)
    ax.text(cx, cy - 0.2, lab, ha="center", va="center", fontsize=8.2, fontweight="bold", color=ACC, linespacing=1.05)
    ax.plot([cx, cx], [cy - 2.6, 2.9], color=INK2, lw=0.8, ls=(0, (2, 2)))
ax.text(5.0, 0.55, "Three questions. The answers are in the article", ha="center", va="center", fontsize=8, color=INK2)
fig.savefig(os.path.join(ROOT, "figures", "teaser_precogs.png"), facecolor=BG, bbox_inches="tight", pad_inches=0.05)
print("wrote figures/teaser_precogs.png")
