# -*- coding: utf-8 -*-
"""A05 teaser drawing (23 Oct 2026, click teaser): a police line-up whose three suspects hold the teaser's three questions.
Original drawing, no third-party artwork. Writes figures/teaser_lineup.png."""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch, Rectangle

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INK, INK2, ACC, GOLD, BG, WALL = "#0b0b0b", "#52514e", "#2a78d6", "#c9a227", "#fcfcfb", "#ecebe6"
fig, ax = plt.subplots(figsize=(4.2, 5.0), dpi=200); fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
ax.set_xlim(0, 10); ax.set_ylim(0, 12); ax.axis("off")
# wall with height lines
ax.add_patch(Rectangle((0.3, 1.2), 9.4, 10.2, fc=WALL, ec=INK, lw=1.8))
for k, yy in enumerate([2.5, 4.0, 5.5, 7.0, 8.5, 10.0]):
    ax.plot([0.3, 9.7], [yy, yy], color=INK2, lw=0.6, alpha=0.5)
    ax.text(0.45, yy + 0.12, f"{k + 4}'", fontsize=6.5, color=INK2)
ax.text(5.0, 10.75, "LINE-UP", ha="center", va="center", fontsize=15, fontweight="bold", color=INK, family="DejaVu Sans")
# three suspects: body, head, hat, placard with a question number
labels = [("1", "what's\nleft?"), ("2", "is five\na lot?"), ("3", "the 7th\nsuspect?")]
heights = [7.9, 8.4, 7.6]
for i, ((n, lab), top) in enumerate(zip(labels, heights)):
    cx = 2.0 + i * 3.0
    ax.add_patch(FancyBboxPatch((cx - 0.95, 1.2), 1.9, top - 2.25, boxstyle="round,pad=0.02,rounding_size=0.5", fc="#3b3a38", ec=INK, lw=1.4))
    ax.add_patch(Circle((cx, top - 0.55), 0.62, fc="#e9dcc8", ec=INK, lw=1.4))
    ax.add_patch(Rectangle((cx - 0.75, top - 0.05), 1.5, 0.16, fc=INK, ec=INK))            # hat brim
    ax.add_patch(Rectangle((cx - 0.5, top + 0.1), 1.0, 0.55, fc=INK, ec=INK))              # hat crown
    ax.plot([cx - 0.25, cx - 0.05], [top - 0.5, top - 0.5], color=INK, lw=1.6); ax.plot([cx + 0.05, cx + 0.25], [top - 0.5, top - 0.5], color=INK, lw=1.6)
    ax.add_patch(FancyBboxPatch((cx - 1.15, 2.6), 2.3, 2.3, boxstyle="round,pad=0.02,rounding_size=0.15", fc="white", ec=INK, lw=1.5))
    ax.add_patch(Circle((cx, 4.45), 0.28, fc=GOLD, ec=INK, lw=1.1)); ax.text(cx, 4.45, n, ha="center", va="center", fontsize=9, fontweight="bold", color=INK)
    ax.text(cx, 3.35, lab, ha="center", va="center", fontsize=8.2, color=ACC, fontweight="bold", linespacing=1.05)
ax.text(5.0, 0.55, "Which one did it? The answers are in the article", ha="center", va="center", fontsize=8, color=INK2)
fig.savefig(os.path.join(ROOT, "figures", "teaser_lineup.png"), facecolor=BG, bbox_inches="tight", pad_inches=0.05)
print("wrote figures/teaser_lineup.png")
