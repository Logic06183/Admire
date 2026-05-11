"""
Extract ERA5-Land MONTHLY_AGGR for Soweto 1980-01 through 2024-12.

Uses the same Soweto point + 5 km buffer + spatial mean as the main
pipeline, so values for 2014-2024 should be consistent with the existing
hourly-derived monthly means in soweto_temp_monthly_stats.csv.

Output:
    climate_data_output/soweto_temp_monthly_1980_2024.csv
        Columns: year, month, date, t2m_c_mean (and t2m_min/t2m_max if
        available in the monthly aggregate).
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

import ee
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(REPO_ROOT))

from soweto_climate_pipeline import PipelineConfig, kelvin_to_celsius

OUT_PATH = REPO_ROOT / "climate_data_output" / "soweto_temp_monthly_1980_2024.csv"


def main() -> int:
    cfg = PipelineConfig()
    ee.Initialize()

    point = ee.Geometry.Point([cfg.SOWETO_LON, cfg.SOWETO_LAT])
    region = point.buffer(cfg.BUFFER_DISTANCE)

    coll_id = "ECMWF/ERA5_LAND/MONTHLY_AGGR"
    # Probe the bands available on this collection
    sample = ee.ImageCollection(coll_id).first()
    band_names = sample.bandNames().getInfo()
    print(f"Available bands ({len(band_names)}): {band_names[:10]}...")

    # We want temperature_2m (monthly mean), and the daily min/max aggregates
    # if present (temperature_2m_min, temperature_2m_max)
    wanted = [b for b in ("temperature_2m", "temperature_2m_min", "temperature_2m_max") if b in band_names]
    print(f"Extracting bands: {wanted}")
    if "temperature_2m" not in wanted:
        print("ERROR: temperature_2m not in collection — aborting")
        return 1

    coll = (
        ee.ImageCollection(coll_id)
        .filterDate("1980-01-01", "2025-01-01")
        .select(wanted)
    )

    n = coll.size().getInfo()
    print(f"Filtered to {n} monthly images")

    def per_image(image):
        stats = image.reduceRegion(
            reducer=ee.Reducer.mean(),
            geometry=region,
            scale=cfg.TEMPERATURE_SCALE,
            maxPixels=1e9,
        )
        out = {"timestamp": image.get("system:time_start")}
        for band in wanted:
            out[band] = stats.get(band)
        return ee.Feature(None, out)

    print("Mapping reducer over collection...")
    start = time.time()
    fc = coll.map(per_image)
    feature_list = fc.getInfo()["features"]
    print(f"  done in {time.time() - start:.1f}s — {len(feature_list)} features")

    rows = []
    for feat in feature_list:
        p = feat["properties"]
        if p.get("temperature_2m") is None:
            continue
        ts = p["timestamp"]
        dt = pd.to_datetime(ts, unit="ms")
        row = {
            "year": dt.year,
            "month": dt.month,
            "date": dt.strftime("%Y-%m"),
            "t2m_c_mean": kelvin_to_celsius(p["temperature_2m"]),
        }
        if "temperature_2m_min" in p and p["temperature_2m_min"] is not None:
            row["t2m_c_daily_min_mean"] = kelvin_to_celsius(p["temperature_2m_min"])
        if "temperature_2m_max" in p and p["temperature_2m_max"] is not None:
            row["t2m_c_daily_max_mean"] = kelvin_to_celsius(p["temperature_2m_max"])
        rows.append(row)

    df = pd.DataFrame(rows).sort_values(["year", "month"]).reset_index(drop=True)
    OUT_PATH.parent.mkdir(exist_ok=True, parents=True)
    df.to_csv(OUT_PATH, index=False)
    print(f"\nWrote {len(df):,} rows to {OUT_PATH}")
    print(f"Date range: {df['date'].iloc[0]} to {df['date'].iloc[-1]}")
    print(f"Mean temperature: {df['t2m_c_mean'].mean():.2f} C")
    print(f"Min monthly mean: {df['t2m_c_mean'].min():.2f} C")
    print(f"Max monthly mean: {df['t2m_c_mean'].max():.2f} C")

    return 0


if __name__ == "__main__":
    sys.exit(main())
