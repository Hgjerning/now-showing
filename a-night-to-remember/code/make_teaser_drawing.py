# -*- coding: utf-8 -*-
"""A68 teaser drawing: a ship's log lying open, three entries, the last one still blank. Original drawing, no third-party
artwork. Writes figures/teaser_log.png."""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch, Polygon

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INK, INK2, GOLD, BG, SEA, PAPER = "#0b0b0b", "#52514e", "#c9a227", "#fcfcfb", "#3987e5", "#f4efe3"
fig, ax = plt.subplots(figsize=(4.4, 5.0), dpi=200); fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
ax.set_xlim(0, 10); ax.set_ylim(0, 12); ax.axis("off")
ax.text(5.0, 11.4, "The ship's log", ha="center", fontsize=12, fontweight="bold", color=INK)
ax.text(5.0, 10.8, "Written before the night, read after it", ha="center", fontsize=8, color=INK2)
ax.add_patch(FancyBboxPatch((0.8, 3.3), 8.4, 6.9, boxstyle="round,pad=0.02,rounding_size=0.15", fc=PAPER, ec=INK, lw=1.4))   # the open book
ax.plot([5, 5], [3.3, 10.2], color=INK2, lw=1.0)
for y in (9.3, 8.5, 7.7, 6.9, 6.1, 5.3, 4.5):
    ax.plot([1.2, 4.6], [y, y], color="#d9d2c0", lw=0.8); ax.plot([5.4, 8.8], [y, y], color="#d9d2c0", lw=0.8)
ax.text(1.3, 9.42, "6 OCT", fontsize=6.5, fontweight="bold", color=INK); ax.text(1.3, 8.62, "Is the path explosive?", fontsize=6, color=INK2, style="italic"); ax.text(1.3, 7.82, "Not explosive.", fontsize=6.3, color=INK)
ax.text(1.3, 6.2, "14 OCT", fontsize=6.5, fontweight="bold", color=INK); ax.text(1.3, 5.42, "Do past markets forecast?", fontsize=6, color=INK2, style="italic"); ax.text(1.3, 4.62, "Tested. See inside.", fontsize=6.3, color=INK)
ax.text(5.5, 9.42, "20 NOV", fontsize=6.5, fontweight="bold", color=INK)
xs = [5.5, 6.1, 6.6, 7.2, 7.7, 8.2, 8.7]; ys = [8.9, 8.75, 8.8, 8.3, 8.4, 7.7, 6.9]
ax.plot(xs, ys, color=SEA, lw=2.2, solid_capstyle="round"); ax.text(8.75, 6.55, "−11.6%", fontsize=6.3, fontweight="bold", color=SEA, ha="right")
ax.text(5.5, 6.2, "21 NOV", fontsize=6.5, fontweight="bold", color=INK); ax.text(5.5, 5.42, "Signed. Market closed.", fontsize=6.3, color=INK); ax.text(5.5, 4.55, "19 FEB 2027:  ?", fontsize=7.2, fontweight="bold", color="#b3261e")
ax.add_patch(Polygon([(7.9, 3.3), (8.5, 3.3), (8.5, 2.5), (8.2, 2.8), (7.9, 2.5)], closed=True, fc="#b3261e", ec=INK, lw=0.8))                 # ribbon
labels = [("1", "did the tests\nsee it?"), ("2", "built to\nsee what?"), ("3", "after the\nfirst 10%?")]
for i, (nm, lab) in enumerate(labels):
    xx = 0.9 + i * 3.15
    ax.add_patch(Circle((xx, 1.25), 0.32, fc=GOLD, ec=INK, lw=1.1)); ax.text(xx, 1.25, nm, ha="center", va="center", fontsize=8.5, fontweight="bold")
    ax.text(xx + 0.45, 1.25, lab, ha="left", va="center", fontsize=6.8, color=INK2, style="italic")
fig.savefig(os.path.join(ROOT, "figures", "teaser_log.png"), facecolor=BG, bbox_inches="tight", pad_inches=0.05)
print("wrote figures/teaser_log.png")
