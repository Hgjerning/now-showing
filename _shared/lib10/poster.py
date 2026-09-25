# -*- coding: utf-8 -*-
"""'Now Showing' hero cards for the Project 10 article series.

An original poster-style card (1080 x 1350, LinkedIn portrait): series banner, film title as the
headline, a tagline, the article's own data as the poster art, and a credits block. It uses no
real poster imagery, fonts or likenesses, only the film title as a text reference.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm

BOLD = fm.FontProperties(fname="/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed-Bold.ttf")
REG = fm.FontProperties(fname="/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed.ttf")
SERIF = fm.FontProperties(fname="/usr/share/fonts/truetype/dejavu/DejaVuSerifCondensed-Italic.ttf")
BG, INK, DIM, GOLD, LINE = "#0f1115", "#f4f1ea", "#9a978f", "#f5b301", "#2a2d33"


def poster(path, number, title, tagline, draw, credits, rated, release, accent="#3987e5", title_size=74, ax_left=0.09, kind="film"):
    """draw(ax, accent) paints the data art on a dark axes. kind='film' (Now Showing) or 'song' (Now Playing)."""
    bg = BG if kind == "film" else "#150f1c"
    fig = plt.figure(figsize=(10.8, 13.5), dpi=100, facecolor=bg)
    if kind == "song":
        import matplotlib.patches as mp
        for r, c in ((0.30, "#221a2c"), (0.27, "#1c1524"), (0.24, "#221a2c"), (0.21, "#1c1524"), (0.18, "#221a2c"), (0.06, accent), (0.012, bg)):
            fig.add_artist(mp.Ellipse((0.98, 0.93), r * 2 * 1.25, r * 2, color=c, zorder=0))
    fig.text(0.5, 0.955, f"NOW SHOWING  ·  FEATURE No. {number}" if kind == "film" else f"NOW PLAYING  ·  TRACK No. {number}", ha="center", color=GOLD, fontproperties=BOLD, fontsize=19)
    fig.text(0.5, 0.925, "A  HENRIK GJERNING  DATA  PICTURE" if kind == "film" else "A  HENRIK GJERNING  DATA  RECORD", ha="center", color=DIM, fontproperties=REG, fontsize=14)
    lines = title.split("\n")
    y = 0.865
    for ln in lines:
        fig.text(0.5, y, ln, ha="center", va="center", color=INK, fontproperties=BOLD, fontsize=title_size)
        y -= 0.075
    fig.text(0.5, y + 0.015, tagline, ha="center", va="center", color=INK, fontproperties=SERIF, fontsize=25, wrap=True)
    top = y - 0.03
    ax = fig.add_axes([ax_left, 0.25, 0.91 - ax_left, top - 0.27], facecolor=bg if kind == "film" else "none")
    for s in ax.spines.values():
        s.set_visible(False)
    ax.tick_params(colors=DIM, labelsize=13, length=0)
    ax.grid(color=LINE, lw=1); ax.set_axisbelow(True)
    draw(ax, accent)
    fig.add_artist(plt.Line2D([0.12, 0.88], [0.205, 0.205], color=LINE, lw=1.5))
    fig.text(0.5, 0.17, credits, ha="center", va="center", color=DIM, fontproperties=REG, fontsize=15, linespacing=1.6)
    fig.text(0.5, 0.095, rated, ha="center", va="center", color=bg, fontproperties=BOLD, fontsize=17,
             bbox=dict(boxstyle="square,pad=0.5", fc=GOLD, ec=GOLD))
    fig.text(0.5, 0.045, release, ha="center", va="center", color=INK, fontproperties=BOLD, fontsize=18)
    fig.savefig(path, facecolor=bg)
    plt.close(fig)
