# Manuscript Figures — Admire Background Section

**Prepared by:** Craig
**Date:** 2026-05-11
**Manuscript:** *"Trends in preterm birth and stillbirth across months and seasons in Soweto, South Africa: Analysis of birth register data"*
**Branch:** `feat/admire-background-figures`

---

## Files in this directory

| File | Format | Purpose |
|---|---|---|
| `figure1_climate_trends.svg` | SVG | Editable source (Figma / Illustrator / Inkscape) |
| `figure1_climate_trends.pdf` | PDF | Vector, fonts embedded, manuscript-ready |
| `figure1_climate_trends.png` | PNG (300 dpi) | Raster preview |
| `figure2_gauteng_map.svg` | SVG | Editable source |
| `figure2_gauteng_map.pdf` | PDF | Manuscript-ready |
| `figure2_gauteng_map.png` | PNG (300 dpi) | Raster preview |

All SVGs preserve text as text (`svg.fonttype = "none"`), so labels remain editable rather than being converted to outline paths.

---

## Figure 1 — Caption draft

**Figure 1.** *Climate and air-quality trends in Soweto, South Africa.* **(A)** Annual mean of daily maximum and minimum 2-metre air temperature, 2014–2024, derived from ERA5-Land hourly reanalysis at the Soweto centroid (−26.27 °S, 27.86 °E) averaged across a 5 km buffer. Trend lines (dashed) with 95 % confidence bands show that recent-decade temperature trends are not statistically significant given an 11-year record (Tmax: −0.39 ± 1.66 °C/decade, p = 0.65; Tmin: +0.06 ± 0.86 °C/decade, p = 0.90). **(B)** Annual mean temperature anomaly relative to the 1991–2020 climatology, 1980–2024, from the ERA5-Land monthly aggregated product. Linear trend +0.32 ± 0.14 °C/decade (p = 3.2 × 10⁻⁵); LOESS smoother in dotted black. 2024 was the warmest year on record at +1.49 °C above the 1991–2020 baseline. **(C)** Monthly mean PM₂.₅ concentration from Copernicus CAMS NRT reanalysis, 2016–2024, plotted on a logarithmic axis. The shaded vertical band marks 2017–2018, during which CAMS NRT shows elevation that is not corroborated by the independent MODIS MAIAC aerosol observations (Panel D); the elevation likely reflects a CAMS NRT product transition rather than a real environmental event. The WHO 2021 annual air-quality guideline (5 µg/m³) is shown for reference. **(D)** Monthly mean MODIS MAIAC aerosol optical depth at 550 nm, 2003–2024, with a 12-month rolling mean (black). AOD is column-integrated aerosol loading rather than a direct surface-PM₂.₅ measurement, but provides an independent satellite observation against which the CAMS NRT series can be cross-checked. The 2017–2018 elevation in CAMS NRT (Panel C) does not appear in this independent product.

**Data sources for citation:**
- ERA5-Land hourly: Muñoz Sabater, J. (2019). ERA5-Land hourly data from 1950 to present. Copernicus Climate Change Service (C3S) Climate Data Store (CDS). doi:10.24381/cds.e2161bac
- ERA5-Land monthly: Muñoz Sabater, J. (2019). ERA5-Land monthly averaged data from 1950 to present. C3S CDS. doi:10.24381/cds.68d2bb30
- CAMS NRT: Copernicus Atmosphere Monitoring Service Near-Real-Time global forecast (`ECMWF/CAMS/NRT` in Google Earth Engine)
- MODIS MAIAC AOD: Lyapustin, A. and Wang, Y. (2022). MODIS/Terra+Aqua Land Aerosol Optical Depth MAIAC Daily L2G Global 1km SIN Grid V061 (`MODIS/061/MCD19A2_GRANULES`). NASA EOSDIS LP DAAC.

---

## Figure 2 — Caption draft

**Figure 2.** *Study location.* Main panel: Gauteng Province, South Africa, showing the City of Johannesburg metropolitan boundary (red outline) and the approximate extent of Soweto (purple hatched area) in its south-western quadrant. Chris Hani Baragwanath Academic Hospital (CHBAH; red star) is located in central Soweto at −26.262 °S, 27.940 °E. Inset: South Africa with Gauteng Province highlighted, for orientation. Boundary data: South African provincial boundaries from Natural Earth (1:10 m, public domain); City of Johannesburg metropolitan boundary from geoBoundaries ADM2 release for ZAF (CC-BY 4.0); the Soweto extent is approximate and shown for orientation rather than as an authoritative administrative boundary (Soweto is a collection of townships within City of Johannesburg rather than a single administrative unit). Chris Hani Baragwanath Academic Hospital is widely cited as the third-largest hospital in the world by bed count, with approximately 3,200 beds.¹,²

**References for the caption:**
1. Chris Hani Baragwanath Academic Hospital. *About the Hospital*. http://www.chrishanibaragwanathhospital.co.za/about.php (accessed 2026-05-11).
2. *Chris Hani Baragwanath Hospital*. Wikipedia. https://en.wikipedia.org/wiki/Chris_Hani_Baragwanath_Hospital (accessed 2026-05-11).

---

## Assumptions and limitations

### Temperature (Figure 1A, 1B)
1. **Spatial averaging.** Temperature is the 5 km-buffer area-mean around the Soweto centroid (−26.2678, 27.8585). ERA5-Land's native pixel is ~11 km, so the buffer covers roughly one grid cell — the value is effectively a point estimate at the Soweto study location, not a spatial average across all of Soweto.
2. **Reanalysis vs observations.** ERA5-Land is a reanalysis product (model fields constrained by observations) rather than a station record. For Highveld South Africa, ERA5-Land typically agrees with station data to within ~1 °C at the daily scale.
3. **2014–2024 trend non-significance (Panel A).** The 11-year record is too short for trend separation from interannual variability — this is a well-known property of climate records, not a flaw of the data. Panel B (45 years) is where the warming signal is statistically resolvable.
4. **Daily Tmax/Tmin construction.** Daily extremes are computed from the hourly ERA5-Land file. Days with fewer than 20 hourly observations were excluded to prevent biased daily extremes.

### Air pollution (Figure 1C, 1D)
5. **CAMS NRT is a near-real-time reanalysis-style product**, not a direct ground measurement. Its resolution (~44 km) is coarser than the Soweto buffer, so the value at the Soweto pixel is regionally representative of the Highveld rather than specifically of Soweto street-level exposure.
6. **CAMS NRT 2017–2018 elevation.** As described in Panel C and corroborated by Panel D, the 2017–2018 PM₂.₅ elevation in CAMS NRT is **not** reproduced by the independent MODIS MAIAC AOD observations. We recommend the manuscript either restricts the PM₂.₅ analysis to 2019–2024 or visibly flags 2017–2018 as suspect data; we have done the latter in the figure.
7. **CAMS NRT record start.** The first CAMS NRT image in Google Earth Engine is 2016-06-22, so the PM₂.₅ panel cannot extend before mid-2016 in this product. MODIS MAIAC AOD (Panel D, 2003 onwards) is the longer-record independent context.
8. **AOD ≠ PM₂.₅.** Aerosol optical depth is column-integrated aerosol loading and is sensitive to all aerosol layers in the atmosphere, not just surface-level fine particulate matter. Over Southern Africa, AOD and surface PM₂.₅ correlate well but do not have a fixed scaling relationship — AOD is presented as a qualitative cross-check rather than as a quantitative PM₂.₅ surrogate.
9. **MAIAC cloud and quality filtering.** No additional QA flag filtering was applied to the MAIAC granules beyond what the GEE collection provides. For a fully publication-grade air-quality analysis, additional MAIAC QA bit-mask filtering would be advisable.

### Map (Figure 2)
10. **Soweto extent is approximate.** Soweto does not exist as a single administrative polygon in either Natural Earth or geoBoundaries (or in OpenStreetMap for South Africa). The hatched rectangle on the map shows the approximate extent of the historic Soweto townships within City of Johannesburg and is labelled accordingly in the legend.
11. **CHBAH coordinates** are from OpenStreetMap and the hospital's official website; precision is approximately ±100 m, which is well within the visual resolution of the figure.

---

## Reproducibility

Every panel can be regenerated from clean inputs. The pipeline is laid out as:

```
soweto_climate_pipeline.py             # main hourly ERA5-Land + CAMS NRT extractor
audit/audit_pipeline.py                # 8-check pipeline audit (run before any pull)
extract_era5_monthly_1980.py           # adds 1980-2024 ERA5-Land monthly to data dir
extract_modis_aod_2003.py              # adds 2003-2024 MODIS MAIAC AOD to data dir
derive_daily_tmaxmin.py                # daily Tmax/Tmin from hourly data
analysis/figure1_climate_trends.py     # builds Figure 1 (SVG/PDF/PNG)
analysis/figure2_map.py                # builds Figure 2 (SVG/PDF/PNG)
climate_data_output/                   # all extracted data + cached boundaries
figures/                               # SVG/PDF/PNG outputs
```

To regenerate from scratch:

```bash
# 1. Verify pipeline integrity (catches any GEE collection drift)
python3 audit/audit_pipeline.py

# 2. (Optional) Re-pull data — only if the extracted CSVs are missing
python3 extract_era5_monthly_1980.py
python3 extract_modis_aod_2003.py
python3 derive_daily_tmaxmin.py

# 3. Rebuild figures
python3 analysis/figure1_climate_trends.py
python3 analysis/figure2_map.py
```

The audit script (`audit/audit_pipeline.py`) is the single most important reproducibility artifact: it verifies that fresh GEE pulls match the saved CSVs to within numerical noise (most recent run: max abs difference 3.55 × 10⁻¹⁵ K). It also re-confirms band names, unit conversions, and Soweto coordinates against live Earth Engine before any new pull.

## Headline numbers for the manuscript text

- **1980–2024 warming trend** at Soweto: **+0.32 ± 0.14 °C/decade** (annual mean temperature anomaly vs 1991–2020 baseline, p = 3.2 × 10⁻⁵, ERA5-Land monthly).
- **Pre-/post-2000 trend split**: 1980–1999 +0.14 °C/decade (p = 0.51, n.s.); **2000–2024 +0.62 °C/decade (p = 0.002)** — i.e. warming has accelerated.
- **2024 warmest year on record** in the 1980–2024 ERA5-Land series at +1.49 °C above the 1991–2020 baseline.
- **Recent (2014–2024) Tmax/Tmin trends** are statistically not significant (p > 0.6 for both), illustrating that climate-change signal requires a multi-decadal record to detect at this latitude.
- **PM₂.₅ 2019–2024 mean** at Soweto: ~26 µg/m³ — **5× the WHO 2021 annual guideline** (5 µg/m³). All years 2019–2024 exceed the guideline.
- **2017–2018 CAMS NRT PM₂.₅ elevation is not corroborated** by MODIS MAIAC AOD (PM ratio 3.7× vs AOD ratio 1.06×) and is recommended to be flagged or excluded.
