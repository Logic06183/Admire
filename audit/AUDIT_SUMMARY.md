# Pipeline Audit Summary

**Date:** 2026-05-11
**Auditor:** Craig (with verification scripts in `audit/`)
**Status:** PASS with one documented caveat

## Result: 11 PASS / 1 WARN / 0 FAIL

The Soweto climate extraction pipeline (`soweto_climate_pipeline.py`) does exactly what its documentation claims. All extracted data on disk is reproducible against fresh GEE queries to within numerical noise (max drift: 3.6 × 10⁻¹⁵ K).

## What was verified

| # | Check | Result | Detail |
|---|---|---|---|
| 1 | GEE auth + dataset access | PASS | ERA5-Land hourly + CAMS NRT both return data for the same windows the pipeline claims to query |
| 2 | Native resolution vs configured scale | PASS | ERA5-Land: 11,131.9 m native vs 11,132 m configured (ratio 1.0). CAMS NRT: 44,453 m native vs 40,000 m configured (ratio 0.9). |
| 3 | Soweto coordinates inside Soweto | PASS | Configured point (−26.2678, 27.8585) is inside the OSM bounding box for Soweto, with a 5 km buffer for areal averaging |
| 4 | Temperature units (K → °C) | PASS | Raw band value 290.96 K → 17.8 °C for 2024-01-15. Conversion correct. |
| 5 | PM2.5 units (kg/m³ → µg/m³) | PASS | Raw 1.33 × 10⁻⁸ kg/m³ → 13.3 µg/m³ for 2023-06-01. Conversion correct. (Original `micrograms_to_micrograms` pass-through bug was already fixed before this audit — see `pm25_anomaly_report.md`.) |
| 6 | Independent PM2.5 reanalysis cross-check | **WARN** | CAMS EAC4 reanalysis is **not in the GEE catalog**. We cannot independently verify the 2017–2018 elevation against a second PM2.5 product without leaving GEE. See "Implication" below. |
| 7 | Reproducibility — fresh GEE pull vs saved CSV | PASS | Re-extracted 168 hourly temperature values for 2024-06-01..08 and diffed against `soweto_temperature_raw.csv` — max absolute difference 3.55 × 10⁻¹⁵ K (machine epsilon). |
| 8 | Saved CSV value-range sanity | PASS | Temperature: 96,408 rows, 0 null, −3.76 to 36.72 °C. PM2.5: 248,654 rows, 574 null, 0 to 1,281 µg/m³ (peak values during 2017–2018 elevation flagged in anomaly report). |
| extra | No synthetic/random/mock data in code | PASS | Static grep of all `.py` and `.ipynb` files turned up zero matches for `random`, `synth`, `fake`, `simulate`, `mock`, `placeholder`, `dummy`. |

## Implication of the one warning

The Copernicus CAMS EAC4 reanalysis — the product we would normally use to independently verify CAMS NRT — is not directly accessible via Google Earth Engine. To cross-check the 2017–2018 PM2.5 elevation against a second product, we have two options:

1. **MODIS MAIAC AOD** (`MODIS/061/MCD19A2_GRANULES`, available 2000-02-24 onwards). AOD is column-integrated aerosol optical depth, not a direct PM2.5 measurement, but it is an independent satellite observation that strongly correlates with surface PM2.5 over Southern Africa. If AOD also shows an elevation in 2017–2018 over Soweto, the CAMS NRT signal is corroborated by an independent product.
2. **Copernicus CDS API** (off-platform). The EAC4 reanalysis can be downloaded via the Copernicus Climate Data Store, but that requires a separate Python client and credentials. Adds setup time but gives a true second PM2.5 product.

For the manuscript background figure, **option 1 (MAIAC AOD) is the parsimonious choice**: a single AOD line plotted alongside the CAMS NRT PM2.5 series provides independent corroboration without leaving the GEE workflow.

## What this means for the figure

| Variable | Product | Time span available | Notes |
|---|---|---|---|
| Tmax / Tmin / Tmean | ERA5-Land hourly | **1950-01-01 → present (75 years)** | The earliest image in GEE is 1950-01-01 01:00 UTC. Plenty of years to demonstrate climate-change warming. ERA5-Land monthly aggregates also available, much faster to pull. |
| PM2.5 | CAMS NRT | 2016-06-22 → present (~9 years) | Honest start year. |
| AOD (corroborating) | MODIS MAIAC MCD19A2 | 2000-02-24 → present (~26 years) | 1 km native resolution, daily. Plotted as a secondary axis or second panel to show that the long-term aerosol-loading trend pre-dates the CAMS NRT record. |

## Files produced by the audit

- `audit/audit_pipeline.py` — re-runnable audit script
- `audit/audit_report.json` — structured PASS/FAIL records
- `audit/audit_log.txt` — human-readable check-by-check log
- `audit/AUDIT_SUMMARY.md` — this document
