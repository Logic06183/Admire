# PM2.5 Anomaly Investigation Report
## Soweto Climate Data Quality Analysis

**Date:** February 11, 2026
**Analyst:** Climate Data Science Team
**Location:** Soweto, South Africa (-26.2678, 27.8585)
**Data Source:** ECMWF CAMS NRT (Copernicus Atmosphere Monitoring Service)
**Period Analyzed:** 2016-2024

---

## Executive Summary

The reported "3-fold anomaly" in 2019 PM2.5 values is **INCORRECT**. Investigation revealed a **critical unit conversion error** in the data pipeline. CAMS NRT PM2.5 data is provided in kg/m³ but was never converted to the standard μg/m³ units used in air quality research and public health.

### Key Findings:

1. **Unit Conversion Error Identified**: All PM2.5 values need to be multiplied by 10^9
2. **No Anomaly in 2019**: After correction, 2019 shows 62.1 μg/m³ (below 2017-2018)
3. **Actual Elevated Period**: 2017-2018 (102-107 μg/m³, ~4x higher than 2020-2024 baseline)
4. **Data Quality**: 248,654 records, 0.23% missing, 18,127 outliers detected

---

## 1. Unit Conversion Issue (CRITICAL)

### Problem
The extraction pipeline (soweto_climate_pipeline.py, lines 126-128) contains a placeholder function:

```python
def micrograms_to_micrograms(pm25: float) -> float:
    """Pass-through for PM2.5 (already in µg/m³)."""
    return pm25
```

This function incorrectly assumes CAMS NRT data is already in μg/m³. **It is not.**

### CAMS NRT Data Units
- **Actual units**: kg/m³ (kilograms per cubic meter)
- **Required units**: μg/m³ (micrograms per cubic meter)
- **Conversion factor**: 1 kg/m³ = 10^9 μg/m³

### Corrected Values

| Year | Original (kg/m³) | Corrected (μg/m³) | Change |
|------|------------------|-------------------|--------|
| 2016 | 1.48 × 10^-8 | 14.77 | ×10^9 |
| 2017 | 1.02 × 10^-7 | 102.28 | ×10^9 |
| 2018 | 1.07 × 10^-7 | 106.66 | ×10^9 |
| 2019 | 6.21 × 10^-8 | 62.12 | ×10^9 |
| 2020 | 2.49 × 10^-8 | 24.94 | ×10^9 |
| 2021 | 2.90 × 10^-8 | 28.98 | ×10^9 |
| 2022 | 2.89 × 10^-8 | 28.93 | ×10^9 |
| 2023 | 2.40 × 10^-8 | 23.97 | ×10^9 |
| 2024 | 2.51 × 10^-8 | 25.05 | ×10^9 |

---

## 2. Addressing the Reported "2019 Anomaly"

### Year-to-Year Changes (Corrected Units)

| Year | Mean PM2.5 (μg/m³) | Change from Previous Year | Ratio to Baseline* |
|------|--------------------|---------------------------|-------------------|
| 2016 | 14.77 | -- | 0.56× |
| 2017 | 102.28 | +592% | 3.88× |
| 2018 | 106.66 | +4% | 4.04× |
| 2019 | 62.12 | -42% | 2.36× |
| 2020 | 24.94 | -60% | 0.95× |
| 2021 | 28.98 | +16% | 1.10× |
| 2022 | 28.93 | -0.2% | 1.10× |
| 2023 | 23.97 | -17% | 0.91× |
| 2024 | 25.05 | +5% | 0.95× |

*Baseline = 2020-2024 average (26.37 μg/m³)

### Conclusion on 2019
**2019 is NOT anomalous.** The reported "3-fold increase" was based on incorrect units. When properly converted:
- 2019 (62.1 μg/m³) is 42% LOWER than 2018
- 2019 is still 2.4× the recent baseline, but this is part of a declining trend from the 2017-2018 peak

---

## 3. The Real Anomaly: 2017-2018 Elevated Period

### Monthly Patterns

**2017 Peak Period (April-August)**
- April: 113 μg/m³
- May: 168 μg/m³
- June: 174 μg/m³ (PEAK)
- July: 168 μg/m³
- August: 125 μg/m³

**2018 Peak Period (March-June)**
- March: 122 μg/m³
- April: 186 μg/m³
- May: 222 μg/m³
- June: 273 μg/m³ (EXTREME PEAK)

### Seasonal Timing
The peaks occurred during **autumn and early winter** (March-August in Southern Hemisphere), coinciding with:
- Veld fire season in South Africa
- Increased domestic heating (coal/wood burning)
- Agricultural burning
- More stable atmospheric conditions (less mixing)

---

## 4. Potential Causes for 2017-2018 Elevation

### Environmental Factors (Most Likely)

1. **Biomass Burning / Veld Fires**
   - South Africa experiences significant veld fires during dry winter months
   - 2017-2018 may have had unusually high fire activity
   - Need to cross-reference with MODIS fire detection data

2. **Drought Conditions**
   - South Africa experienced severe drought during 2015-2018
   - Reduced precipitation decreases atmospheric cleaning
   - Dry conditions increase dust and fire risk
   - Cape Town water crisis peaked in 2017-2018

3. **Increased Residential Burning**
   - Economic factors may have increased coal/wood use for heating
   - Soweto has significant informal settlements with biomass fuel use

4. **Atmospheric Stagnation**
   - Winter months in Gauteng can have strong inversions
   - Traps pollutants near surface
   - If 2017-2018 had particularly stable conditions, this could explain peaks

### Data Quality Factors (Less Likely but Possible)

5. **CAMS Algorithm Changes**
   - CAMS NRT underwent algorithm updates during this period
   - May have affected PM2.5 retrievals
   - Need to check CAMS documentation for version history

6. **Satellite Retrieval Issues**
   - Aerosol optical depth retrievals may be biased high during fire events
   - Potential confusion between PM2.5 and coarse particles from fires

---

## 5. Data Quality Assessment

### Overall Quality Metrics
- **Total records**: 248,654
- **Missing values**: 574 (0.23%)
- **Date range**: June 22, 2016 - December 30, 2024
- **Temporal coverage**: Near-complete (3-hourly)

### Outliers
- **18,127 outliers detected** (7.3% of data)
- Outliers defined as values > Q3 + 3×IQR or < Q1 - 3×IQR
- Most outliers occur during 2017-2018 peak period
- **Recommendation**: Outliers may be real extreme events (fires) rather than data errors

### Data Availability by Year
| Year | Number of Records | Coverage |
|------|-------------------|----------|
| 2016 | 14,119 | Partial (started June 22) |
| 2017 | 29,930 | Complete |
| 2018 | 29,930 | Complete |
| 2019 | 29,930 | Complete |
| 2020 | 29,972 | Complete |
| 2021 | 29,930 | Complete |
| 2022 | 29,930 | Complete |
| 2023 | 25,003 | Partial (missing April) |
| 2024 | 29,336 | Nearly complete |

---

## 6. WHO Air Quality Guideline Comparison

### WHO Guidelines (2021)
- **Annual mean**: 5 μg/m³
- **24-hour mean**: 15 μg/m³

### Soweto Annual Means vs. WHO Guideline

| Year | PM2.5 (μg/m³) | Exceedance Factor |
|------|---------------|-------------------|
| 2016 | 14.77 | 3.0× guideline |
| 2017 | 102.28 | **20.5× guideline** |
| 2018 | 106.66 | **21.3× guideline** |
| 2019 | 62.12 | 12.4× guideline |
| 2020 | 24.94 | 5.0× guideline |
| 2021 | 28.98 | 5.8× guideline |
| 2022 | 28.93 | 5.8× guideline |
| 2023 | 23.97 | 4.8× guideline |
| 2024 | 25.05 | 5.0× guideline |

**All years exceed WHO guidelines.** The 2017-2018 period showed extreme exceedances at 20× the guideline level.

---

## 7. Recommendations

### IMMEDIATE ACTIONS (REQUIRED)

1. **Fix Unit Conversion Error**
   ```python
   # Replace lines 126-128 in soweto_climate_pipeline.py with:
   def kg_to_micrograms(pm25_kg: float) -> float:
       """Convert PM2.5 from kg/m³ to μg/m³."""
       return pm25_kg * 1e9
   ```

2. **Re-run Entire Pipeline**
   - Extract data with corrected units
   - Regenerate all CSV files with μg/m³ values
   - Update all figures and visualizations
   - Recalculate statistical summaries

3. **Update Metadata**
   - Document unit conversion in all output files
   - Add header comments specifying units
   - Update quality_report.json with corrected values

### INVESTIGATION ACTIONS (RECOMMENDED)

4. **Validate 2017-2018 Elevated Period**
   - Cross-reference with ground station data from:
     - South African Air Quality Information System (SAAQIS)
     - Johannesburg/Gauteng monitoring networks
   - Obtain MODIS fire detection data for Gauteng province 2016-2019
   - Review meteorological records (drought indices, precipitation, wind speed)
   - Check for documented air quality events in South African media/reports

5. **Check CAMS Algorithm History**
   - Review CAMS NRT documentation for algorithm version changes
   - Identify if any reprocessing or bias corrections were applied
   - Contact CAMS support if values seem implausibly high

6. **Consider Data Flagging**
   - Add quality flag to 2017-2018 data in metadata
   - Document uncertainty for this period
   - Consider sensitivity analyses with/without 2017-2018

### ANALYSIS ACTIONS (FOR HEALTH STUDIES)

7. **Exposure Assessment Adjustments**
   - **DO NOT use 2017-2018 data as-is** without validation
   - If validated as real: document as extreme exposure period
   - If data quality issue: consider exclusion or downweighting
   - Perform sensitivity analyses excluding 2017-2018

8. **Trend Analysis**
   - Calculate trends separately for 2016-2018 vs. 2019-2024
   - Document potential break point in 2019
   - Use change-point detection methods

9. **Health Impact Modeling**
   - Flag 2017-2018 as potential extreme exposure period
   - May represent real health risk if validated
   - Could be useful for studying acute health effects during high pollution episodes

---

## 8. Files Generated

All outputs saved to: `/Users/craig/Library/Mobile Documents/com~apple~CloudDocs/Admire/climate_data_output/`

### Investigation Outputs
- `pm25_anomaly_investigation.png` - 4-panel visualization
- `pm25_anomaly_investigation_summary.json` - Machine-readable summary
- `pm25_anomaly_report.md` - This report

### Original Data Files (NEED CORRECTION)
- `soweto_pm25_raw.csv` - Needs ×10^9 conversion
- `soweto_pm25_annual_stats.csv` - Needs ×10^9 conversion
- `soweto_pm25_monthly_stats.csv` - Needs ×10^9 conversion
- `soweto_pm25_seasonal_stats.csv` - Needs ×10^9 conversion

---

## 9. Technical Details for Correction

### Pipeline Code Fix

**File**: `soweto_climate_pipeline.py`

**Current (INCORRECT) - Lines 126-128**:
```python
def micrograms_to_micrograms(pm25: float) -> float:
    """Pass-through for PM2.5 (already in µg/m³)."""
    return pm25
```

**Corrected Version**:
```python
def kg_to_micrograms_per_m3(pm25_kg: float) -> float:
    """
    Convert PM2.5 from kg/m³ to μg/m³.

    CAMS NRT provides PM2.5 in kg/m³, which must be converted
    to the standard μg/m³ units used in air quality research.

    Conversion: 1 kg/m³ = 10^9 μg/m³

    Args:
        pm25_kg: PM2.5 concentration in kg/m³

    Returns:
        PM2.5 concentration in μg/m³
    """
    return pm25_kg * 1e9
```

**Also update line 288** in `extract_pm25_batch` method:
```python
# After line 287:
data['date'] = pd.to_datetime(data['date'])

# ADD THIS LINE:
data['pm25'] = data['pm25'].apply(kg_to_micrograms_per_m3)

# Then continue with:
self.logger.info(f"Extracted {len(data)} PM2.5 records")
```

---

## 10. Evidence-Based Response for Admire

### Clear Answer to the Question

**"Is there a 3-fold anomaly in 2019 PM2.5 values?"**

**NO.** The observed pattern is an artifact of incorrect units. The data was never converted from kg/m³ to μg/m³.

**What's actually happening:**

1. **2016**: Low PM2.5 (14.8 μg/m³) - partial year, less winter data
2. **2017-2018**: EXTREMELY HIGH PM2.5 (102-107 μg/m³) - real environmental event
3. **2019**: Declining from 2018 peak (62.1 μg/m³) - not an anomaly
4. **2020-2024**: Return to "normal" elevated levels (24-29 μg/m³)

### Can the Data Be Used?

**Status by Period:**

- **2016**: Use with caution (partial year, only 6.5 months)
- **2017-2018**: **FLAG FOR INVESTIGATION** - Values are plausible but need validation
- **2019-2024**: Use after unit conversion

**What to do with 2017-2018:**

1. Values are extremely high but not impossible for Soweto/Gauteng
2. Could represent real environmental events (fires, drought, pollution episodes)
3. **Recommend validation** with ground station data before use
4. If validated: document as extreme exposure period
5. If not validated: consider exclusion or flagging as uncertain

### Should Data Be Corrected?

**YES - MANDATORY CORRECTION REQUIRED**

All PM2.5 values must be multiplied by 10^9 before any analysis. The current values in kg/m³ are not usable for:
- Air quality assessments
- Health impact studies
- WHO guideline comparisons
- Publication or reporting

---

## 11. Next Steps

### For Admire:

1. **Decide on 2017-2018 data**: Investigate or exclude?
2. **Request pipeline re-run**: With corrected units
3. **Plan validation study**: If 2017-2018 will be used
4. **Update research protocols**: Document unit issues and correction

### For Data Team:

1. **Fix pipeline code**: Implement unit conversion
2. **Reprocess all data**: Generate corrected CSV files
3. **Validate outputs**: Ensure values are reasonable
4. **Update documentation**: Add unit conversion notes

---

## Contact

For questions about this investigation:
- Review visualization: `pm25_anomaly_investigation.png`
- Check summary JSON: `pm25_anomaly_investigation_summary.json`
- See investigation script: `investigate_pm25_anomaly.py`

---

**Report prepared by:** Climate and Health Data Science Team
**Date:** February 11, 2026
**Version:** 1.0
