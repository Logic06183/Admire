"""
Figure 2: Map showing Gauteng Province, Soweto, and CHBAH.

Two-panel composite (inset + main):
  - Inset: South Africa with Gauteng province highlighted, so an
    international reader can orient themselves.
  - Main: Gauteng province with the City of Johannesburg metropolitan
    boundary, Soweto labelled in its southwestern quadrant, and Chris
    Hani Baragwanath Academic Hospital (CHBAH) marked with a star.

Boundary data:
  - South Africa + provinces: Natural Earth 10m admin_1_states_provinces
    (public domain).
  - City of Johannesburg metropolitan boundary: geoBoundaries ZAF ADM2
    (CC-BY-4.0).
  - Soweto and CHBAH positions: OSM Nominatim / Wikipedia coordinates.

CHBAH facts (for the caption):
  - Coordinates: 26.2616 S, 27.9396 E
  - Bed count: ~3,200 (widely cited as the third-largest hospital in
    the world by bed count)
  - Sources: Chris Hani Baragwanath Academic Hospital official website
    (http://www.chrishanibaragwanathhospital.co.za) and Wikipedia
    article (https://en.wikipedia.org/wiki/Chris_Hani_Baragwanath_Hospital)

Run:
    python3 analysis/figure2_map.py
"""
from __future__ import annotations

import json
import sys
import urllib.request
from pathlib import Path

import cartopy.crs as ccrs
import cartopy.io.shapereader as shpreader
import geopandas as gpd
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch, Rectangle
from shapely.geometry import Point

REPO_ROOT = Path(__file__).resolve().parent.parent
FIG_DIR = REPO_ROOT / "figures"
CACHE_DIR = REPO_ROOT / "climate_data_output" / "_geo_cache"
FIG_DIR.mkdir(exist_ok=True)
CACHE_DIR.mkdir(parents=True, exist_ok=True)

# Lancet house style
sys.path.insert(0, str(Path(__file__).resolve().parent))
from lancet_style import (  # noqa: E402
    apply_lancet_rcparams,
    panel_letter,
    source_footer,
    COL_LANCET_RED, COL_INK, COL_PAPER,
    COL_GREY_DARK, COL_GREY_MID, COL_GREY_LIGHT, COL_GREY_FAINT,
)

apply_lancet_rcparams()

# Anchor points
SOWETO_LAT, SOWETO_LON = -26.2678, 27.8585   # study-area centroid (matches pipeline)
CHBAH_LAT, CHBAH_LON = -26.2616, 27.9396     # Chris Hani Baragwanath Academic Hospital
JOBURG_CBD_LAT, JOBURG_CBD_LON = -26.2041, 28.0473
PRETORIA_LAT, PRETORIA_LON = -25.7479, 28.2293

# Map palette — Lancet idiom: grayscale base, single red accent for the
# highlighted entities (City of Joburg, Soweto, CHBAH). Non-highlighted
# context is mid-to-light grey so the eye lands on the study area
# without conscious effort.
COL_LAND = "#ECECEC"                # other provinces
COL_LAND_BORDER = "#9E9E9E"
COL_NEIGHBOUR = "#F7F7F7"           # neighbouring countries (inset)
COL_NEIGHBOUR_BORDER = "#C9C9C9"
COL_GAUTENG = "#D9D9D9"             # province highlight — neutral grey
COL_GAUTENG_EDGE = "#444444"
COL_CITY = "#FFFFFF"                # city interior: bright contrast against grey province
COL_CITY_EDGE = COL_LANCET_RED      # red metropolitan boundary
COL_SOWETO = COL_LANCET_RED         # red hatched study-area footprint
COL_HOSPITAL = COL_LANCET_RED       # red star for CHBAH
COL_OCEAN = "#FFFFFF"


def fetch_geoboundaries(level: str = "ADM2") -> gpd.GeoDataFrame:
    """Fetch ZAF geoBoundaries ADM2 (or other) and cache locally."""
    cache = CACHE_DIR / f"geoBoundaries-ZAF-{level}.geojson"
    if not cache.exists():
        api_url = f"https://www.geoboundaries.org/api/current/gbOpen/ZAF/{level}/"
        with urllib.request.urlopen(api_url, timeout=30) as r:
            meta = json.loads(r.read())
        gj_url = meta["gjDownloadURL"]
        print(f"  downloading {gj_url}")
        with urllib.request.urlopen(gj_url, timeout=120) as r:
            cache.write_bytes(r.read())
    return gpd.read_file(cache)


def load_natural_earth_provinces() -> gpd.GeoDataFrame:
    """Load Natural Earth 10m provinces and filter to South Africa."""
    shp = shpreader.natural_earth(
        resolution="10m", category="cultural", name="admin_1_states_provinces"
    )
    g = gpd.read_file(shp)
    return g[g["admin"] == "South Africa"].copy()


def load_natural_earth_countries() -> gpd.GeoDataFrame:
    """Load Natural Earth 50m countries."""
    shp = shpreader.natural_earth(
        resolution="50m", category="cultural", name="admin_0_countries"
    )
    return gpd.read_file(shp)


# ============================================================================
# Main figure
# ============================================================================
def main() -> int:
    print("Loading boundary data...")
    sa_provs = load_natural_earth_provinces()
    print(f"  South African provinces: {len(sa_provs)}")
    gauteng = sa_provs[sa_provs["name"] == "Gauteng"]
    if gauteng.empty:
        print("  ERROR: 'Gauteng' not found in Natural Earth provinces")
        return 1

    countries = load_natural_earth_countries()

    print("Fetching City of Joburg from geoBoundaries ADM2...")
    adm2 = fetch_geoboundaries("ADM2")
    # ADM2 names — City of Johannesburg metropolitan municipality
    joburg_mask = adm2["shapeName"].str.contains("Johannesburg", case=False, na=False)
    joburg = adm2[joburg_mask]
    print(f"  found {len(joburg)} ADM2 match(es) for Johannesburg")

    # Map projection: equal-area for Gauteng (Albers conic with local origin)
    proj = ccrs.AlbersEqualArea(
        central_longitude=28.0, central_latitude=-26.0,
        standard_parallels=(-25.0, -27.0),
    )
    geo = ccrs.PlateCarree()

    fig = plt.figure(figsize=(11.0, 7.5))
    gs = fig.add_gridspec(1, 2, width_ratios=[2.0, 1.0], wspace=0.05,
                          left=0.04, right=0.97, top=0.88, bottom=0.12)
    ax_main = fig.add_subplot(gs[0], projection=proj)
    ax_inset = fig.add_subplot(gs[1], projection=ccrs.PlateCarree())

    # ---------- Inset: South Africa with Gauteng highlighted ----------
    sa_geom = countries[countries["ADMIN"] == "South Africa"]
    ax_inset.add_geometries(
        sa_geom.geometry, crs=geo,
        facecolor=COL_LAND, edgecolor=COL_LAND_BORDER, linewidth=0.7,
    )
    # Gauteng filled in Lancet red on the inset — small enough that a strong
    # accent reads clearly at thumbnail size.
    ax_inset.add_geometries(
        gauteng.geometry, crs=geo,
        facecolor=COL_LANCET_RED, edgecolor=COL_LANCET_RED, linewidth=0.9, alpha=0.85,
    )

    # Neighbouring countries for context
    neighbours = countries[countries["ADMIN"].isin(
        ["Namibia", "Botswana", "Zimbabwe", "Mozambique", "Eswatini", "Lesotho"]
    )]
    ax_inset.add_geometries(
        neighbours.geometry, crs=geo,
        facecolor=COL_NEIGHBOUR, edgecolor=COL_NEIGHBOUR_BORDER, linewidth=0.4,
    )

    ax_inset.set_extent([15, 35, -36, -22], crs=geo)
    ax_inset.set_facecolor(COL_OCEAN)

    # Label Gauteng (no arrow needed — the red fill is unambiguous)
    g_centroid = gauteng.geometry.iloc[0].centroid
    ax_inset.annotate(
        "Gauteng", xy=(g_centroid.x, g_centroid.y), xycoords=geo._as_mpl_transform(ax_inset),
        xytext=(10, 10), textcoords="offset points",
        fontsize=8, color=COL_LANCET_RED, fontweight="bold",
    )
    ax_inset.text(
        0.02, 0.97, "B", transform=ax_inset.transAxes,
        fontsize=14, fontweight="bold", color=COL_INK, va="top", ha="left",
        zorder=10,
    )

    # ---------- Main: Gauteng with City of Joburg + Soweto + CHBAH ----------
    # Neighbouring provinces (drawn first so Gauteng sits on top)
    other_provs = sa_provs[sa_provs["name"] != "Gauteng"]
    ax_main.add_geometries(
        other_provs.geometry, crs=geo,
        facecolor=COL_LAND, edgecolor=COL_LAND_BORDER, linewidth=0.5,
    )

    # Gauteng (greyscale highlight — the eye is drawn instead to the red
    # city + red Soweto + red star)
    ax_main.add_geometries(
        gauteng.geometry, crs=geo,
        facecolor=COL_GAUTENG, edgecolor=COL_GAUTENG_EDGE, linewidth=1.0,
    )

    # City of Joburg — white interior, red border (the focus boundary)
    if not joburg.empty:
        ax_main.add_geometries(
            joburg.geometry, crs=geo,
            facecolor=COL_CITY, edgecolor=COL_CITY_EDGE, linewidth=1.4, alpha=1.0,
        )

    # Soweto highlight — approximate footprint of the townships.
    # Clearly labelled in the legend as "approximate extent" rather than
    # an authoritative boundary (Soweto is not a single admin unit).
    soweto_bbox = Rectangle(
        (27.80, -26.30), 0.13, 0.10,
        transform=geo, fill=True,
        facecolor=COL_SOWETO, alpha=0.22,
        edgecolor=COL_SOWETO, linewidth=1.2,
        zorder=4,
    )
    ax_main.add_patch(soweto_bbox)

    # CHBAH star marker
    ax_main.plot(
        CHBAH_LON, CHBAH_LAT, "*",
        markersize=20, color=COL_HOSPITAL,
        markeredgecolor=COL_INK, markeredgewidth=0.7,
        transform=geo, zorder=5,
    )

    # Pretoria and Joburg CBD for orientation — small grey markers
    for lon, lat, name, off in [
        (PRETORIA_LON, PRETORIA_LAT, "Pretoria", (7, 5)),
        (JOBURG_CBD_LON, JOBURG_CBD_LAT, "Johannesburg CBD", (8, 8)),
    ]:
        ax_main.plot(lon, lat, "o", markersize=4.0, color=COL_INK,
                     transform=geo, zorder=5)
        ax_main.annotate(
            name, xy=(lon, lat), xycoords=geo._as_mpl_transform(ax_main),
            xytext=off, textcoords="offset points",
            fontsize=8, color=COL_INK,
        )

    # Soweto label (pushed below the hatched area to clear CHBAH)
    ax_main.annotate(
        "Soweto",
        xy=(27.85, -26.28), xycoords=geo._as_mpl_transform(ax_main),
        xytext=(-65, -25), textcoords="offset points",
        fontsize=10.5, fontweight="bold", color=COL_LANCET_RED,
        arrowprops=dict(arrowstyle="-", color=COL_LANCET_RED, lw=0.7),
    )

    # CHBAH label — placed lower-right of marker, clear of CBD label
    ax_main.annotate(
        "Chris Hani Baragwanath\nAcademic Hospital (CHBAH)",
        xy=(CHBAH_LON, CHBAH_LAT), xycoords=geo._as_mpl_transform(ax_main),
        xytext=(48, -20), textcoords="offset points",
        fontsize=9, color=COL_LANCET_RED, fontweight="bold",
        arrowprops=dict(arrowstyle="->", color=COL_LANCET_RED, lw=0.9),
    )

    # Extent: tight around Gauteng with a little buffer
    gx0, gy0, gx1, gy1 = gauteng.total_bounds
    pad = 0.05
    ax_main.set_extent(
        [gx0 - pad, gx1 + pad, gy0 - pad, gy1 + pad], crs=geo
    )
    ax_main.set_facecolor(COL_OCEAN)
    # No subplot title — figure-level suptitle covers it. Panel letter
    # placed inside the top-left corner (just inside the frame), not above.
    ax_main.text(
        0.02, 0.97, "A", transform=ax_main.transAxes,
        fontsize=14, fontweight="bold", color=COL_INK, va="top", ha="left",
        zorder=10,
    )

    # Legend
    legend_handles = [
        Patch(facecolor=COL_GAUTENG, edgecolor=COL_GAUTENG_EDGE, label="Gauteng Province"),
        Patch(facecolor=COL_CITY, edgecolor=COL_CITY_EDGE,
              label="City of Johannesburg metro"),
        Patch(facecolor=COL_SOWETO, alpha=0.30, edgecolor=COL_SOWETO,
              label="Soweto (approximate extent)"),
        Line2D([0], [0], marker="*", color="none", markerfacecolor=COL_HOSPITAL,
               markeredgecolor=COL_INK, markersize=13, label="CHBAH"),
    ]
    ax_main.legend(handles=legend_handles, loc="lower left", frameon=True,
                   facecolor="white", edgecolor=COL_GREY_MID, fontsize=8)

    # Scale bar — 20 km at the lower right
    bar_x = gx1 - 0.30
    bar_y = gy0 + 0.04
    ax_main.plot([bar_x, bar_x + 20 / 111.0], [bar_y, bar_y],
                 color=COL_INK, lw=2.0, transform=geo)
    ax_main.text(bar_x + 10 / 111.0, bar_y + 0.015, "20 km",
                 ha="center", va="bottom", fontsize=8, color=COL_INK, transform=geo)

    # North arrow
    arrow_x = gx0 + 0.06
    arrow_y = gy1 - 0.10
    ax_main.annotate("N", xy=(arrow_x, arrow_y), xycoords=geo._as_mpl_transform(ax_main),
                     xytext=(arrow_x, arrow_y - 0.05),
                     textcoords=geo._as_mpl_transform(ax_main),
                     fontsize=11, ha="center", fontweight="bold", color=COL_INK,
                     arrowprops=dict(facecolor=COL_INK, width=2, headwidth=8))

    # Figure title above + data-source footer below (Lancet idiom)
    fig.suptitle(
        "Study location: Gauteng Province, Soweto and CHBAH",
        fontsize=12, fontweight="bold", y=0.955, x=0.04, ha="left", color=COL_INK,
    )
    fig.text(
        0.04, 0.918,
        "(A) Gauteng Province (grey) with the City of Johannesburg metropolitan area outlined in red, "
        "Soweto highlighted, and CHBAH marked with a star. (B) South Africa locator showing Gauteng in red.",
        fontsize=8.5, color=COL_GREY_DARK, ha="left", va="top",
    )
    source_footer(
        fig,
        "Boundaries  Provinces: Natural Earth 10 m (public domain).  "
        "City of Johannesburg: geoBoundaries ZAF ADM2 (CC-BY 4.0).  "
        "CHBAH and Soweto: OpenStreetMap.",
        y=0.055,
    )
    source_footer(
        fig,
        "CHBAH is widely cited as one of the world's largest hospitals "
        "(~3,200 beds; CHBAH official website and Wikipedia, accessed 2026-05-11).",
        y=0.033,
    )
    source_footer(
        fig,
        "Soweto is shown as an approximate extent rather than a single "
        "administrative boundary; see MANUSCRIPT_FIGURES.md for full assumptions.",
        y=0.012,
    )

    out_svg = FIG_DIR / "figure2_gauteng_map.svg"
    out_pdf = FIG_DIR / "figure2_gauteng_map.pdf"
    out_png = FIG_DIR / "figure2_gauteng_map.png"
    fig.savefig(out_svg)
    fig.savefig(out_pdf)
    fig.savefig(out_png, dpi=300)
    print(f"Wrote {out_svg}")
    print(f"Wrote {out_pdf}")
    print(f"Wrote {out_png}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
