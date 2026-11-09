# -*- coding: utf-8 -*-
"""A07 teaser drawing (23 Oct 2026, click teaser): three pressure gauges, each needle pointing at one of the teaser's
three questions. Original drawing, no third-party artwork. Writes figures/teaser_gauges.png."""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch, Wedge, Rectangle

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INK, INK2, ACC, GOLD, RED, BG = "#0b0b0b", "#52514e", "#2a78d6", "#c9a227", "#b3261e", "#fcfcfb"
fig, ax = plt.subplots(figsize=(4.2, 5.0), dpi=200); fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
ax.set_xlim(0, 10); ax.set_ylim(0, 12); ax.axis("off")
ax.text(5.0, 11.6, "PRESSURE CHECK", ha="center", va="center", fontsize=14, fontweight="bold", color=INK, family="DejaVu Sans")
# a pipe running behind the gauges
ax.add_patch(Rectangle((0.3, 2.35), 9.4, 0.5, fc="#d9d6cc", ec=INK, lw=1.2))
specs = [(2.0, 7.6, "1", "add\nanything?", 150), (5.0, 5.4, "2", "which\nlist?", 95), (8.0, 7.6, "3", "fair\ntest?", 40)]
for cx, cy, n, lab, ang in specs:
    ax.plot([cx, cx], [2.85, cy - 1.45], color=INK, lw=3)                                   # stem to the pipe
    ax.add_patch(Circle((cx, cy), 1.45, fc="white", ec=INK, lw=2.2))
    ax.add_patch(Wedge((cx, cy), 1.25, 0, 30, width=0.22, fc=RED, ec="none"))                # red zone
    ax.add_patch(Wedge((cx, cy), 1.25, 30, 180, width=0.22, fc="#ecebe6", ec="none"))
    for t in np.linspace(0, 180, 7):
        r = np.radians(t); ax.plot([cx + 1.0 * np.cos(r), cx + 1.22 * np.cos(r)], [cy + 1.0 * np.sin(r), cy + 1.22 * np.sin(r)], color=INK2, lw=1)
    r = np.radians(ang); ax.plot([cx, cx + 0.95 * np.cos(r)], [cy, cy + 0.95 * np.sin(r)], color=INK, lw=2.4, solid_capstyle="round")
    ax.add_patch(Circle((cx, cy), 0.13, fc=INK, ec=INK))
    ax.add_patch(Circle((cx, cy - 0.62), 0.27, fc=GOLD, ec=INK, lw=1.1)); ax.text(cx, cy - 0.62, n, ha="center", va="center", fontsize=9, fontweight="bold", color=INK)
    ax.text(cx, cy + 1.95, lab, ha="center", va="center", fontsize=8.2, color=ACC, fontweight="bold", linespacing=1.05)
ax.text(5.0, 0.9, "Three questions. The readings are in the article", ha="center", va="center", fontsize=8, color=INK2)
fig.savefig(os.path.join(ROOT, "figures", "teaser_gauges.png"), facecolor=BG, bbox_inches="tight", pad_inches=0.05)
print("wrote figures/teaser_gauges.png")
