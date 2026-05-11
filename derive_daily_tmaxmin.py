"""
Derive daily Tmax / Tmin / Tmean for Soweto 2014-2024 from the existing
hourly ERA5-Land extract.

Reads:  climate_data_output/soweto_temperature_raw.csv (hourly)
Writes: climate_data_output/soweto_temp_daily.csv (daily Tmax/Tmin/Tmean)
        climate_data_output/soweto_temp_annual_tmaxmin.csv (annual means
        of daily Tmax/Tmin/Tmean + linear trend stats)
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

REPO_ROOT = Path(__file__).resolve().parent
DATA_DIR = REPO_ROOT / "climate_data_output"
HOURLY = DATA_DIR / "soweto_temperature_raw.csv"
DAILY_OUT = DATA_DIR / "soweto_temp_daily.csv"
ANNUAL_OUT = DATA_DIR / "soweto_temp_annual_tmaxmin.csv"


def main() -> int:
    if not HOURLY.exists():
        print(f"ERROR: {HOURLY} not found")
        return 1

    df = pd.read_csv(HOURLY)
    df["date"] = pd.to_datetime(df["date"])
    df["day"] = df["date"].dt.normalize()
    print(f"Read {len(df):,} hourly records, {df['date'].min()} → {df['date'].max()}")

    # Drop days with fewer than 20 hours of data (incomplete days bias daily extremes)
    counts = df.groupby("day")["temperature_c"].count()
    keep_days = counts[counts >= 20].index
    daily = (
        df[df["day"].isin(keep_days)]
        .groupby("day")["temperature_c"]
        .agg(tmax="max", tmin="min", tmean="mean", n_hours="count")
        .reset_index()
        .rename(columns={"day": "date"})
    )
    daily["diurnal_range"] = daily["tmax"] - daily["tmin"]
    print(f"Daily rows (>=20 hr complete): {len(daily):,}")

    daily.to_csv(DAILY_OUT, index=False)
    print(f"Wrote {DAILY_OUT}")

    # Annual aggregates + linear trend
    annual = (
        daily.assign(year=daily["date"].dt.year)
        .groupby("year")
        .agg(
            tmax_annual=("tmax", "mean"),
            tmin_annual=("tmin", "mean"),
            tmean_annual=("tmean", "mean"),
            diurnal_range_annual=("diurnal_range", "mean"),
            n_days=("date", "count"),
        )
        .reset_index()
    )
    annual.to_csv(ANNUAL_OUT, index=False)
    print(f"Wrote {ANNUAL_OUT}")

    # Linear trends with 95% CIs (for the figure)
    print("\nLinear trends (2014-2024):")
    for col in ["tmax_annual", "tmin_annual", "tmean_annual"]:
        x = annual["year"].astype(float).values
        y = annual[col].astype(float).values
        res = stats.linregress(x, y)
        slope_per_decade = res.slope * 10
        # 95% CI on slope from stderr
        ci95 = 1.96 * res.stderr * 10
        print(
            f"  {col}: {slope_per_decade:+.3f} ± {ci95:.3f} °C/decade "
            f"(r²={res.rvalue ** 2:.3f}, p={res.pvalue:.3f})"
        )

    return 0


if __name__ == "__main__":
    sys.exit(main())
