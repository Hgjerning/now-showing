# -*- coding: utf-8 -*-
"""A04 teaser drawing (21 Oct 2026): a one-armed bandit whose three reels are the teaser's three questions.
Original drawing, no third-party artwork. Writes figures/teaser_slots.png."""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle, Rectangle

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INK, INK2, ACC, GOLD, RED, BG = "#0b0b0b", "#52514e", "#2a78d6", "#c9a227", "#b3261e", "#fcfcfb"
fig, ax = plt.subplots(figsize=(4.2, 5.0), dpi=200); fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
ax.set_xlim(0, 10); ax.set_ylim(0, 12); ax.axis("off")
# cabinet
ax.add_patch(FancyBboxPatch((0.8, 1.0), 7.6, 9.6, boxstyle="round,pad=0.02,rounding_size=0.6", fc="#f3efe3", ec=INK, lw=2.2))
ax.add_patch(FancyBboxPatch((1.3, 9.0), 6.6, 1.2, boxstyle="round,pad=0.02,rounding_size=0.3", fc=RED, ec=INK, lw=1.6))
ax.text(4.6, 9.6, "JACKPOT?", ha="center", va="center", fontsize=17, fontweight="bold", color="white", family="DejaVu Sans")
# reels
labels = [("1", "risk?"), ("2", "flaw?"), ("3", "20 months?")]
for i, (n, lab) in enumerate(labels):
    x = 1.45 + i * 2.2
    ax.add_patch(FancyBboxPatch((x, 4.6), 1.9, 3.6, boxstyle="round,pad=0.02,rounding_size=0.25", fc="white", ec=INK, lw=1.8))
    ax.text(x + 0.95, 6.75, "?", ha="center", va="center", fontsize=40, fontweight="bold", color=ACC)
    ax.text(x + 0.95, 5.25, lab, ha="center", va="center", fontsize=9.5 if len(lab) < 8 else 7.0, color=INK2, style="italic")
    ax.add_patch(Circle((x + 0.95, 8.55), 0.24, fc=GOLD, ec=INK, lw=1.2)); ax.text(x + 0.95, 8.55, n, ha="center", va="center", fontsize=8.5, fontweight="bold", color=INK)
# win line
ax.plot([1.2, 8.0], [6.75, 6.75], color=RED, lw=1.0, ls=(0, (4, 3)), alpha=0.7, zorder=0)
# coin tray and slot
ax.add_patch(FancyBboxPatch((2.2, 1.5), 4.8, 1.3, boxstyle="round,pad=0.02,rounding_size=0.3", fc="#e2dccb", ec=INK, lw=1.6))
for k, cx in enumerate([3.2, 4.0, 4.9, 5.7]):
    ax.add_patch(Circle((cx, 2.1 + 0.12 * (k % 2)), 0.32, fc=GOLD, ec=INK, lw=1.0))
ax.add_patch(Rectangle((4.2, 3.6), 0.8, 0.18, fc=INK, ec=INK))
ax.text(4.6, 3.25, "insert beta", ha="center", va="center", fontsize=7.5, color=INK2)
# lever
ax.plot([8.4, 9.3], [6.2, 6.2], color=INK, lw=3); ax.plot([9.3, 9.3], [6.2, 9.6], color=INK, lw=3)
ax.add_patch(Circle((9.3, 9.9), 0.42, fc=RED, ec=INK, lw=1.5))
ax.text(4.6, 0.35, "Pull the lever: the answers are in the article", ha="center", va="center", fontsize=8, color=INK2)
fig.savefig(os.path.join(ROOT, "figures", "teaser_slots.png"), facecolor=BG, bbox_inches="tight", pad_inches=0.05)
print("wrote figures/teaser_slots.png")
