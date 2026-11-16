# -*- coding: utf-8 -*-
"""A08 teaser drawing (23 Oct 2026, click teaser): an old valve radio whose three tuning dials hold the teaser's three
questions. Original drawing, no third-party artwork. Writes figures/teaser_radio.png."""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch, Rectangle

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INK, INK2, ACC, GOLD, WOOD, BG = "#0b0b0b", "#52514e", "#2a78d6", "#c9a227", "#b07a45", "#fcfcfb"
fig, ax = plt.subplots(figsize=(4.2, 5.0), dpi=200); fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
ax.set_xlim(0, 10); ax.set_ylim(0, 12); ax.axis("off")
ax.text(5.0, 11.5, "NOW PLAYING?", ha="center", va="center", fontsize=14, fontweight="bold", color=INK, family="DejaVu Sans")
# cabinet with a rounded top
ax.add_patch(FancyBboxPatch((0.7, 1.4), 8.6, 8.8, boxstyle="round,pad=0.02,rounding_size=1.6", fc=WOOD, ec=INK, lw=2.2))
# speaker cloth with a few grille slats
ax.add_patch(FancyBboxPatch((1.6, 6.0), 6.8, 3.4, boxstyle="round,pad=0.02,rounding_size=0.6", fc="#e9dcc8", ec=INK, lw=1.6))
for x in np.linspace(2.3, 7.7, 8):
    ax.plot([x, x], [6.25, 9.15], color="#c9b79c", lw=2.2)
# frequency band
ax.add_patch(Rectangle((1.6, 5.15), 6.8, 0.55, fc="#f6f1e4", ec=INK, lw=1.2))
for x in np.linspace(1.9, 8.1, 14):
    ax.plot([x, x], [5.2, 5.45], color=INK2, lw=0.8)
ax.plot([6.1, 6.1], [5.15, 5.7], color="#b3261e", lw=2)
# three dials holding the questions
for cx, n, lab in [(2.4, "1", "paper or\ncalendar?"), (5.0, "2", "who\nfaded?"), (7.6, "3", "worth\npaying?")]:
    ax.add_patch(Circle((cx, 3.4), 0.95, fc="#2f2a25", ec=INK, lw=1.8))
    ax.add_patch(Circle((cx, 3.4), 0.62, fc="#4a423a", ec=INK, lw=1.0))
    ax.plot([cx, cx + 0.5], [3.4, 3.75], color="#f6f1e4", lw=2.2, solid_capstyle="round")
    ax.add_patch(Circle((cx, 4.62), 0.24, fc=GOLD, ec=INK, lw=1.0)); ax.text(cx, 4.62, n, ha="center", va="center", fontsize=8.5, fontweight="bold", color=INK)
    ax.text(cx, 1.95, lab, ha="center", va="center", fontsize=8.0, color="#f6f1e4", fontweight="bold", linespacing=1.05)
ax.text(5.0, 0.7, "Three questions. The answers are in the article", ha="center", va="center", fontsize=8, color=INK2)
fig.savefig(os.path.join(ROOT, "figures", "teaser_radio.png"), facecolor=BG, bbox_inches="tight", pad_inches=0.05)
print("wrote figures/teaser_radio.png")
