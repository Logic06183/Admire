"""
Lancet-style figure styling.

The Lancet has a recognisable visual idiom for figures:
  - Sans-serif throughout (Frutiger / Helvetica / Arial fallback chain),
    7-9 pt axis text, 9-10 pt titles, bold black panel letters (A, B,
    C, D) tucked into each subplot's top-left corner.
  - Subdued, mostly-greyscale palette with a single saturated emphasis
    colour ("Lancet red") used to draw the eye to the headline series
    or the highlighted feature.
  - No grid by default. Tick marks point outward. Spines kept on the
    bottom and left only.
  - Data-source attribution sits as a small italic line below the
    figure, never inside the plot area.

Importing this module applies the rcParams globally. Use the COL_*
constants for colour selection so the palette stays consistent
between figures.

Reference for the approximate palette: The Lancet's published
brand colours and recent figures (e.g. Lancet Global Health and
Lancet Planetary Health 2023-2024 issues).
"""
from __future__ import annotations

import matplotlib as mpl
import matplotlib.pyplot as plt

# --- Palette --------------------------------------------------------------
# Lancet's signature red — used for the primary / emphasis series.
COL_LANCET_RED = "#C8102E"
# Cool counter-accent for paired series (e.g. Tmin against Tmax) — desaturated
# dark blue rather than a vibrant primary.
COL_LANCET_BLUE = "#2A5B86"
# Neutral primary line / text colour.
COL_INK = "#222222"
# Subtle grey for context / background fills.
COL_PAPER = "#F5F4F1"
COL_GREY_DARK = "#555555"
COL_GREY_MID = "#888888"
COL_GREY_LIGHT = "#BFBFBF"
COL_GREY_FAINT = "#E5E5E5"

# Air-quality / aerosol palette (still in the Lancet idiom but
# distinguishable from temperature reds/blues)
COL_PM25 = "#8C1515"       # dark crimson — pollution emphasis
COL_AOD = "#2D5F3F"        # dark teal-green for the independent product

# Map fills
COL_LAND = "#EFEDE8"
COL_GAUTENG_FILL = "#E8DCC4"   # warm neutral
COL_GAUTENG_EDGE = "#777777"
COL_CITY_FILL = "#F6E0D1"
COL_CITY_EDGE = COL_LANCET_RED
COL_SOWETO_FILL = COL_LANCET_RED
COL_OCEAN = "#FFFFFF"


def apply_lancet_rcparams() -> None:
    """Apply the global rcParams for a Lancet-styled figure."""
    mpl.rcParams.update({
        # Typography
        "font.family": "sans-serif",
        "font.sans-serif": ["Frutiger", "Helvetica", "Arial", "DejaVu Sans"],
        "font.size": 8.5,
        "axes.titlesize": 9.5,
        "axes.titleweight": "regular",
        "axes.labelsize": 8.5,
        "axes.labelcolor": COL_INK,
        "xtick.labelsize": 7.5,
        "ytick.labelsize": 7.5,
        "xtick.color": COL_INK,
        "ytick.color": COL_INK,
        "legend.fontsize": 7.5,

        # Spines and ticks
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.spines.left": True,
        "axes.spines.bottom": True,
        "axes.edgecolor": COL_INK,
        "axes.linewidth": 0.7,
        "xtick.direction": "out",
        "ytick.direction": "out",
        "xtick.major.width": 0.7,
        "ytick.major.width": 0.7,
        "xtick.major.size": 3.0,
        "ytick.major.size": 3.0,

        # Lines
        "lines.linewidth": 1.3,
        "lines.solid_capstyle": "round",

        # Legend
        "legend.frameon": False,

        # SVG output: keep text as text so it round-trips into Figma
        "svg.fonttype": "none",

        # Default colour cycle
        "axes.prop_cycle": mpl.cycler(color=[
            COL_LANCET_RED, COL_LANCET_BLUE, COL_INK,
            COL_GREY_DARK, COL_PM25, COL_AOD,
        ]),

        # Grid off by default
        "axes.grid": False,
    })


def panel_letter(ax, letter: str, x: float = -0.10, y: float = 1.05) -> None:
    """Place a bold, slightly-oversized panel letter (A, B, C, D) in the
    top-left corner of the subplot — the Lancet convention."""
    ax.text(
        x, y, letter,
        transform=ax.transAxes,
        fontsize=12, fontweight="bold", color=COL_INK,
        ha="left", va="bottom",
    )


def source_footer(fig, text: str, y: float = 0.015, x: float = 0.04) -> None:
    """Italic 'Data: ...' attribution line below the figure body, in the
    Lancet style."""
    fig.text(
        x, y, text,
        fontsize=7.0, color=COL_GREY_DARK, style="italic",
        ha="left", va="bottom",
    )
