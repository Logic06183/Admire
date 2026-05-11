"""
Figure 1: Soweto climate and air quality trends for the manuscript
background section.

Four-panel composite (SVG / PDF / PNG):

  A. Annual daily Tmax and Tmin, 2014-2024 (derived from ERA5-Land hourly).
     Shows recent climate baseline for the study period; trend lines with
     95% CI for context (trends are not statistically significant at 11
     years — that is itself a useful caveat for the manuscript).

  B. Annual mean-temperature anomaly relative to 1991-2020 climatology,
     1980-2024 (ERA5-Land monthly). LOESS smoother + linear trend with
     95% CI. This is the climate-change panel: +0.32 +/- 0.14 C/decade,
     p = 3e-5.

  C. PM2.5 monthly mean for Soweto, 2016-2024 (CAMS NRT). WHO 2021
     annual guideline (5 ug/m3) shown as reference line. The 2017-2018
     elevation is left visible; not smoothed away.

  D. MODIS MAIAC AOD 550 nm, 2003-2024, monthly mean (if available).
     Independent satellite measurement of column aerosol loading,
     providing historical context for the air-pollution narrative
     before the CAMS NRT record begins. AOD is not PM2.5 but it
     correlates with surface aerosol loading.

Run:
    python3 analysis/figure1_climate_trends.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.lines import Line2D
from scipy import stats

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = REPO_ROOT / "climate_data_output"
FIG_DIR = REPO_ROOT / "figures"
FIG_DIR.mkdir(exist_ok=True)

# Lancet house style: muted palette + Lancet red as the emphasis colour,
# bold panel letters in the top-left, italic data-source footer below.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from lancet_style import (  # noqa: E402
    apply_lancet_rcparams,
    panel_letter,
    source_footer,
    COL_LANCET_RED, COL_LANCET_BLUE, COL_INK,
    COL_GREY_DARK, COL_GREY_MID, COL_GREY_LIGHT, COL_GREY_FAINT,
    COL_PM25, COL_AOD,
)

apply_lancet_rcparams()

# Series-specific colour assignments (mapped to the Lancet palette)
COL_TMAX = COL_LANCET_RED
COL_TMIN = COL_LANCET_BLUE
COL_MEAN = COL_INK
COL_WHO = COL_GREY_DARK
COL_BAND = COL_GREY_MID


def loess_1d(x, y, frac: float = 0.4):
    """Simple LOWESS via statsmodels (if available) else a moving mean."""
    try:
        from statsmodels.nonparametric.smoothers_lowess import lowess
        z = lowess(y, x, frac=frac, it=2, return_sorted=True)
        return z[:, 0], z[:, 1]
    except Exception:
        order = np.argsort(x)
        xs = np.asarray(x)[order]
        ys = np.asarray(y)[order]
        window = max(3, int(len(xs) * frac))
        smoothed = pd.Series(ys).rolling(window, center=True, min_periods=1).mean().values
        return xs, smoothed


def fit_linear_with_ci(x, y, ci: float = 0.95):
    """Return (slope, intercept, slope_lo, slope_hi, slope_se, p, fit_line, ci_band).

    `fit_line` is y_hat at x. `ci_band` is the half-width of the CI on the
    mean prediction at each x (used to draw a band around the trend line).
    """
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    n = len(x)
    res = stats.linregress(x, y)
    fit = res.intercept + res.slope * x

    # CI on the mean prediction at each x_i
    t_crit = stats.t.ppf(0.5 + ci / 2, df=n - 2)
    s_yx = np.sqrt(np.sum((y - fit) ** 2) / (n - 2))
    x_mean = np.mean(x)
    sxx = np.sum((x - x_mean) ** 2)
    band = t_crit * s_yx * np.sqrt(1.0 / n + (x - x_mean) ** 2 / sxx)

    slope_ci = t_crit * res.stderr
    return {
        "slope": res.slope,
        "intercept": res.intercept,
        "slope_ci_half": slope_ci,
        "p": res.pvalue,
        "r2": res.rvalue ** 2,
        "fit": fit,
        "band_half": band,
    }


# ============================================================================
# Panel A — Annual Tmax / Tmin 2014-2024
# ============================================================================
def panel_a(ax):
    daily = pd.read_csv(DATA_DIR / "soweto_temp_daily.csv")
    daily["date"] = pd.to_datetime(daily["date"])
    annual = (
        daily.assign(year=daily["date"].dt.year)
        .groupby("year")
        .agg(tmax=("tmax", "mean"), tmin=("tmin", "mean"))
        .reset_index()
    )

    ax.plot(annual["year"], annual["tmax"], "o-", color=COL_TMAX, label="Annual mean of daily $T_{max}$")
    ax.plot(annual["year"], annual["tmin"], "s-", color=COL_TMIN, label="Annual mean of daily $T_{min}$")

    trend_lines = []
    for col, c, label in [("tmax", COL_TMAX, "Tmax"), ("tmin", COL_TMIN, "Tmin")]:
        f = fit_linear_with_ci(annual["year"], annual[col])
        ax.plot(annual["year"], f["fit"], "--", color=c, lw=0.9, alpha=0.7)
        ax.fill_between(
            annual["year"], f["fit"] - f["band_half"], f["fit"] + f["band_half"],
            color=c, alpha=0.10, linewidth=0,
        )
        slope = f["slope"] * 10
        ci = f["slope_ci_half"] * 10
        sig = "n.s." if f["p"] > 0.05 else ("p<0.05" if f["p"] > 0.01 else "p<0.01")
        trend_lines.append((c, f"{label}: {slope:+.2f} ± {ci:.2f} °C/decade ({sig})"))

    ax.set_xlabel("Year")
    ax.set_ylabel("Temperature (°C)")
    ax.set_title("Annual mean of daily $T_{max}$ and $T_{min}$, 2014–2024",
                 loc="left", pad=10)
    ax.legend(loc="center left", frameon=False)
    ax.set_xlim(2013.5, 2024.5)
    panel_letter(ax, "A")

    # Trend annotation as a coloured text block — sits in the white space
    # between the Tmax and Tmin clusters
    for i, (c, txt) in enumerate(trend_lines):
        ax.text(
            0.97, 0.50 - i * 0.06, txt, transform=ax.transAxes,
            ha="right", color=c, fontsize=7,
        )


# ============================================================================
# Panel B — Long-term anomaly 1980-2024
# ============================================================================
def panel_b(ax):
    monthly = pd.read_csv(DATA_DIR / "soweto_temp_monthly_1980_2024.csv")
    annual = monthly.groupby("year")["t2m_c_mean"].mean().reset_index()
    baseline = annual.loc[
        (annual["year"] >= 1991) & (annual["year"] <= 2020), "t2m_c_mean"
    ].mean()
    annual["anomaly"] = annual["t2m_c_mean"] - baseline

    # Bars for the anomaly
    colors = [COL_LANCET_RED if a > 0 else COL_LANCET_BLUE for a in annual["anomaly"]]
    ax.bar(annual["year"], annual["anomaly"], color=colors, alpha=0.7, width=0.85,
           edgecolor="none")

    # Linear trend + 95% CI band
    f = fit_linear_with_ci(annual["year"], annual["anomaly"])
    ax.plot(annual["year"], f["fit"], "-", color=COL_INK, lw=1.4,
            label=f"Linear trend: {f['slope']*10:+.2f} ± {f['slope_ci_half']*10:.2f} °C/decade")
    ax.fill_between(
        annual["year"], f["fit"] - f["band_half"], f["fit"] + f["band_half"],
        color=COL_INK, alpha=0.12, linewidth=0,
    )

    # LOESS for visual narrative
    xs, ys = loess_1d(annual["year"].values, annual["anomaly"].values, frac=0.35)
    ax.plot(xs, ys, ":", color=COL_INK, lw=1.0, alpha=0.7, label="LOESS smoother")

    ax.axhline(0, color=COL_INK, lw=0.5)
    ax.set_xlabel("Year")
    ax.set_ylabel("Anomaly vs 1991–2020 (°C)")
    ax.set_title("Annual mean temperature anomaly, 1980–2024",
                 loc="left", pad=10)
    # Add significance text
    p = f["p"]
    p_text = f"p = {p:.1e}" if p < 0.001 else f"p = {p:.3f}"
    ax.text(0.98, 0.05, p_text, transform=ax.transAxes, ha="right",
            fontsize=7.5, color=COL_INK)
    ax.legend(loc="upper left", frameon=False)
    panel_letter(ax, "B")


# ============================================================================
# Panel C — PM2.5 monthly 2016-2024
# ============================================================================
def panel_c(ax):
    pm = pd.read_csv(DATA_DIR / "soweto_pm25_monthly_stats.csv")
    # Build a datetime column for x-axis
    pm["date"] = pd.to_datetime(
        pm["year"].astype(str) + "-" + pm["month"].astype(str).str.zfill(2) + "-01"
    )
    pm = pm.sort_values("date").reset_index(drop=True)

    # Shade the 2017-2018 suspect-data window
    suspect_start = pd.Timestamp("2017-01-01")
    suspect_end = pd.Timestamp("2019-01-01")
    ax.axvspan(suspect_start, suspect_end, color=COL_GREY_LIGHT, alpha=0.35,
               linewidth=0)
    ax.text(pd.Timestamp("2018-01-01"), 300,
            "CAMS NRT elevation\nnot corroborated\nby MAIAC AOD (Panel D)",
            ha="center", va="top", fontsize=7, color=COL_GREY_DARK, style="italic")

    ax.plot(pm["date"], pm["pm25_mean"], "-", color=COL_PM25, lw=1.2)
    ax.fill_between(pm["date"], pm["pm25_q25"], pm["pm25_q75"], color=COL_PM25,
                    alpha=0.18, linewidth=0, label="Interquartile range")

    # WHO 2021 annual guideline reference (5 ug/m3)
    ax.axhline(5, color=COL_WHO, lw=1.0, linestyle="--",
               label="WHO 2021 annual guideline (5 µg/m³)")

    ax.set_xlabel("Year")
    ax.set_ylabel("PM$_{2.5}$ (µg/m³)")
    ax.set_title("Monthly mean PM$_{2.5}$, 2016–2024",
                 loc="left", pad=10)
    ax.legend(loc="upper right", frameon=False)
    # Use a log scale because the 2017-18 elevation dwarfs the rest
    ax.set_yscale("log")
    ax.set_ylim(1, 500)
    panel_letter(ax, "C")


# ============================================================================
# Panel D — MODIS MAIAC AOD 2003-2024 (only if file exists)
# ============================================================================
def panel_d(ax):
    path = DATA_DIR / "soweto_aod_monthly_2003_2024.csv"
    if not path.exists():
        ax.text(0.5, 0.5,
                "MODIS MAIAC AOD pull in progress —\n"
                "panel will be added once data is on disk.",
                ha="center", va="center", transform=ax.transAxes,
                fontsize=10, color=COL_BAND, style="italic")
        ax.set_xticks([])
        ax.set_yticks([])
        ax.spines["bottom"].set_visible(False)
        ax.spines["left"].set_visible(False)
        ax.set_title("D. MODIS MAIAC AOD 550 nm, 2003–2024 (pending)",
                     loc="left")
        return

    aod = pd.read_csv(path)
    aod["date"] = pd.to_datetime(aod["date"])
    aod = aod.sort_values("date").reset_index(drop=True)

    # Shade the same 2017-2018 window so panels C and D line up visually
    ax.axvspan(pd.Timestamp("2017-01-01"), pd.Timestamp("2019-01-01"),
               color=COL_GREY_LIGHT, alpha=0.35, linewidth=0)

    ax.plot(aod["date"], aod["aod_550_mean"], "-", color=COL_AOD, lw=1.0,
            alpha=0.5, label="Monthly mean")

    # 12-month rolling mean for trend visibility
    aod["rolling_12"] = aod["aod_550_mean"].rolling(12, center=True).mean()
    ax.plot(aod["date"], aod["rolling_12"], "-", color=COL_INK, lw=1.6,
            label="12-month rolling mean")

    # Annotate the absence of a 2017-2018 spike
    ax.text(pd.Timestamp("2018-01-01"), 0.31,
            "No comparable elevation\nin independent product",
            ha="center", va="top", fontsize=7, color=COL_GREY_DARK, style="italic")

    ax.set_xlabel("Year")
    ax.set_ylabel("Aerosol optical depth (550 nm)")
    ax.set_title("MODIS MAIAC AOD 550 nm, 2003–2024 (independent corroboration)",
                 loc="left", pad=10)
    ax.legend(loc="upper right", frameon=False)
    ax.set_ylim(0, 0.35)
    panel_letter(ax, "D")


# ============================================================================
# Main
# ============================================================================
def main() -> int:
    fig = plt.figure(figsize=(11.0, 9.0))
    gs = fig.add_gridspec(2, 2, hspace=0.45, wspace=0.24,
                          left=0.08, right=0.96, top=0.92, bottom=0.10)
    axA = fig.add_subplot(gs[0, 0])
    axB = fig.add_subplot(gs[0, 1])
    axC = fig.add_subplot(gs[1, 0])
    axD = fig.add_subplot(gs[1, 1])

    panel_a(axA)
    panel_b(axB)
    panel_c(axC)
    panel_d(axD)

    fig.suptitle(
        "Climate and air-quality trends, Soweto, South Africa",
        fontsize=11.5, fontweight="bold", y=0.965, x=0.08, ha="left",
        color=COL_INK,
    )

    # Data-source footer in the Lancet idiom: two short italic lines below
    # the plot area, full attribution so the figure is publication-defensible
    # without leaning on the caption.
    source_footer(
        fig,
        "Data sources  A–B: ERA5-Land reanalysis (Copernicus C3S/ECMWF).  "
        "C: CAMS NRT global forecast (Copernicus Atmosphere Monitoring Service).  "
        "D: MODIS MCD19A2 MAIAC AOD v6.1 (NASA LP DAAC).",
        y=0.040,
    )
    source_footer(
        fig,
        "Extracted at Soweto −26.27 °S, 27.86 °E with a 5 km buffer. "
        "Figure prepared 2026-05-11. See MANUSCRIPT_FIGURES.md for assumptions and limitations.",
        y=0.015,
    )

    out_svg = FIG_DIR / "figure1_climate_trends.svg"
    out_pdf = FIG_DIR / "figure1_climate_trends.pdf"
    out_png = FIG_DIR / "figure1_climate_trends.png"
    fig.savefig(out_svg)
    fig.savefig(out_pdf)
    fig.savefig(out_png, dpi=300)
    print(f"Wrote {out_svg}")
    print(f"Wrote {out_pdf}")
    print(f"Wrote {out_png}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
