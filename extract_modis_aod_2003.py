"""
Extract MODIS MAIAC AOD (550 nm) for Soweto 2003-01 through 2024-12.

Collection: MODIS/061/MCD19A2_GRANULES (1 km, daily granules)
Band:       Optical_Depth_055 (AOD at 550 nm, scale factor 0.001)

AOD is column-integrated aerosol optical depth, NOT a direct PM2.5 measurement.
It is an independent satellite observation that correlates with surface PM2.5
loading over Southern Africa, providing historical context for the
CAMS NRT PM2.5 series (which only goes back to 2016-06-22).

Strategy: build a server-side ImageCollection of monthly mean composites,
then pull all 264 monthly values (22 years x 12 months) in one getInfo()
call. Much faster than client-side year-by-year iteration.

Output:
    climate_data_output/soweto_aod_monthly_2003_2024.csv
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

import ee
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(REPO_ROOT))

from soweto_climate_pipeline import PipelineConfig

OUT_MONTHLY = REPO_ROOT / "climate_data_output" / "soweto_aod_monthly_2003_2024.csv"


def main() -> int:
    cfg = PipelineConfig()
    ee.Initialize()

    point = ee.Geometry.Point([cfg.SOWETO_LON, cfg.SOWETO_LAT])
    region = point.buffer(cfg.BUFFER_DISTANCE)

    coll_full = (
        ee.ImageCollection("MODIS/061/MCD19A2_GRANULES")
        .filterDate("2003-01-01", "2025-01-01")
        .select("Optical_Depth_055")
    )

    n_total = coll_full.size().getInfo()
    print(f"Total granules 2003-2024: {n_total:,}")
    print(f"Soweto region: point ({cfg.SOWETO_LAT}, {cfg.SOWETO_LON}) "
          f"with {cfg.BUFFER_DISTANCE}m buffer")

    # Chunk the request into 3-year batches to stay under GEE's
    # per-request compute budget.
    def batch_features(start_year: int, end_year: int):
        n_months = (end_year - start_year) * 12
        months = ee.List.sequence(0, n_months - 1)

        def month_mean_feature(i):
            i = ee.Number(i)
            year = ee.Number(start_year).add(i.divide(12).floor())
            month = i.mod(12).add(1)
            start = ee.Date.fromYMD(year, month, 1)
            end = start.advance(1, "month")

            monthly_imgs = coll_full.filterDate(start, end)
            monthly_mean_img = monthly_imgs.mean()

            stats = monthly_mean_img.reduceRegion(
                reducer=ee.Reducer.mean(),
                geometry=region,
                scale=1000,
                maxPixels=1e9,
            )
            return ee.Feature(None, {
                "year": year,
                "month": month,
                "n_granules": monthly_imgs.size(),
                "aod_550_scaled": stats.get("Optical_Depth_055"),
            })

        return ee.FeatureCollection(months.map(month_mean_feature))

    rows = []
    for y in range(2003, 2025, 3):
        y_end = min(y + 3, 2025)
        print(f"  fetching {y}-{y_end - 1}...", end="", flush=True)
        t0 = time.time()
        info = batch_features(y, y_end).getInfo()
        print(f" {time.time() - t0:.1f}s ({len(info['features'])} months)")
        for feat in info["features"]:
            p = feat["properties"]
            if p.get("aod_550_scaled") is None:
                continue
            rows.append({
                "year": int(p["year"]),
                "month": int(p["month"]),
                "n_granules": int(p["n_granules"]),
                "aod_550_mean": p["aod_550_scaled"] * 0.001,
            })

    df = pd.DataFrame(rows).sort_values(["year", "month"]).reset_index(drop=True)
    df["date"] = pd.to_datetime(
        df["year"].astype(str) + "-" + df["month"].astype(str).str.zfill(2) + "-01"
    )
    df.to_csv(OUT_MONTHLY, index=False)
    print(f"\nWrote {len(df):,} monthly rows to {OUT_MONTHLY}")
    print(f"Date range: {df['date'].min()} to {df['date'].max()}")
    print(f"AOD 550 mean: {df['aod_550_mean'].mean():.3f}, "
          f"range {df['aod_550_mean'].min():.3f}-{df['aod_550_mean'].max():.3f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
