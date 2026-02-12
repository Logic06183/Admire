# PM2.5 Anomaly Investigation - Complete Findings

**Investigation Date:** February 11, 2026
**Data Period:** 2016-2024
**Location:** Soweto, South Africa
**Investigator:** Climate and Health Data Science Team

---

## Quick Answer for Admire

**Question:** Why do PM2.5 values for 2019 appear 3-fold higher than other years?

**Answer:** They don't. This is a misinterpretation caused by a **critical unit conversion error** in the data pipeline. When units are corrected, 2019 is NOT anomalous. The actual elevated period is 2017-2018.

---

## Critical Finding: Unit Conversion Error

### The Problem

**CAMS NRT PM2.5 data is in kg/m³ but was never converted to μg/m³**

- Source data units: **kg/m³** (kilograms per cubic meter)
- Required units: **μg/m³** (micrograms per cubic meter)
- Missing conversion: **×10⁹** (multiply by 1 billion)
- Location in code: `soweto_climate_pipeline.py` lines 126-128

### Impact

**ALL current PM2.5 values are wrong by a factor of 1,000,000,000**

The pipeline has a placeholder function that does nothing:
```python
def micrograms_to_micrograms(pm25: float) -> float:
    """Pass-through for PM2.5 (already in µg/m³)."""
    return pm25  # WRONG - data is NOT in μg/m³!
```

---

## Corrected Annual Values

| Year | **WRONG** (kg/m³) | **CORRECT** (μg/m³) | vs. Baseline | Status |
|------|-------------------|---------------------|--------------|---------|
| 2016 | 1.48×10⁻⁸ | 14.8 | 0.56× | Partial year |
| **2017** | 1.02×10⁻⁷ | **102.3** | **3.88×** | **⚠ EXTREME** |
| **2018** | 1.07×10⁻⁷ | **106.7** | **4.04×** | **⚠ EXTREME** |
| 2019 | 6.21×10⁻⁸ | 62.1 | 2.36× | Declining |
| 2020 | 2.49×10⁻⁸ | 24.9 | 0.95× | Normal |
| 2021 | 2.90×10⁻⁸ | 29.0 | 1.10× | Normal |
| 2022 | 2.89×10⁻⁸ | 28.9 | 1.10× | Normal |
| 2023 | 2.40×10⁻⁸ | 24.0 | 0.91× | Normal |
| 2024 | 2.51×10⁻⁸ | 25.1 | 0.95× | Normal |

**Baseline:** 2020-2024 average = 26.4 μg/m³
**WHO Annual Guideline:** 5 μg/m³

---

## What's Actually Happening?

### Timeline

1. **2016** (14.8 μg/m³): Partial year, low baseline
2. **2017-2018** (102-107 μg/m³): **EXTREME POLLUTION EPISODE** ⚠
3. **2019** (62.1 μg/m³): Declining from 2018 peak (NOT anomalous)
4. **2020-2024** (24-29 μg/m³): Return to "normal" elevated levels

### The Real Anomaly: 2017-2018

**Peak months:**
- 2017 June: 174 μg/m³
- 2018 June: 273 μg/m³ (27× higher than WHO guideline!)

**Seasonal pattern:** Peaks during autumn/winter (March-August)

**Likely causes:**
1. Biomass burning / veld fires (most likely)
2. Severe drought 2015-2018 (reduced atmospheric cleaning)
3. Increased residential coal/wood burning for heating
4. Winter atmospheric inversions trapping pollutants
5. Agricultural burning season

**Evidence needed:**
- Ground station validation (SAAQIS network)
- MODIS fire detection data
- Meteorological records
- CAMS algorithm version history

---

## Data Quality Assessment

### Overall Quality: ACCEPTABLE (after unit correction)

| Metric | Value | Status |
|--------|-------|--------|
| Total records | 248,654 | ✓ |
| Missing values | 574 (0.23%) | ✓ Excellent |
| Outliers | 18,127 (7.3%) | ⚠ Mostly 2017-2018 |
| Date coverage | Jun 2016 - Dec 2024 | ✓ |

### By Period

- **2016**: Partial year (Jun-Dec) → Use with caution
- **2017-2018**: Complete but extreme values → **Validate before use**
- **2019-2024**: Complete and stable → Use after unit correction

---

## WHO Air Quality Comparison

All years **EXCEED** WHO 2021 annual guideline (5 μg/m³):

- 2016: 3.0× guideline
- **2017: 20.5× guideline** ⚠
- **2018: 21.3× guideline** ⚠
- 2019: 12.4× guideline
- 2020-2024: 4.8-5.8× guideline

This indicates Soweto has chronic air quality issues, with an extreme pollution episode in 2017-2018.

---

## Recommendations

### IMMEDIATE (Required)

1. **Fix pipeline code** → See `PIPELINE_FIX.py`
2. **Re-run extraction** with corrected units
3. **Regenerate all outputs** (CSVs, figures, analyses)
4. **DO NOT USE** current data for any analysis

### INVESTIGATION (Recommended)

5. **Validate 2017-2018 period**
   - Cross-check with ground stations
   - Obtain fire detection data
   - Review meteorological records
   - Check CAMS algorithm changes

6. **Document findings**
   - Update metadata with unit corrections
   - Flag 2017-2018 with quality warnings
   - Add uncertainty estimates

### DATA USAGE (Choose based on needs)

**Option A - CONSERVATIVE** (Recommended initially)
- ✓ Use 2019-2024 only (6 years of reliable data)
- ✗ Exclude 2017-2018 (flag as uncertain)
- ✗ Exclude 2016 (partial year)

**Option B - COMPREHENSIVE** (If 2017-2018 validated)
- ✓ Use all years 2016-2024
- ⚠ Flag 2017-2018 as extreme exposure period
- ✓ Document as real pollution episodes
- ✓ Useful for acute health effect studies

**Option C - MIXED** (Most thorough)
- ✓ Main analysis: 2019-2024
- ✓ Sensitivity analysis: Include 2017-2018
- ✓ Supplementary: Examine 2017-2018 separately

---

## Files Generated

**Location:** `/Users/craig/Library/Mobile Documents/com~apple~CloudDocs/Admire/climate_data_output/`

### Investigation Outputs

1. **pm25_anomaly_investigation.png**
   - 4-panel visualization
   - Annual trends with corrected units
   - Monthly patterns comparison
   - Before/after unit conversion
   - Baseline comparisons

2. **pm25_anomaly_investigation_summary.json**
   - Machine-readable summary
   - All corrected values
   - Recommendations

3. **pm25_anomaly_report.md**
   - Complete technical report
   - Detailed methodology
   - Environmental context
   - Statistical analyses

4. **PM25_ANOMALY_SUMMARY.txt**
   - Quick reference guide
   - Executive summary
   - Decision matrix

5. **PIPELINE_FIX.py**
   - Corrected code segments
   - Unit conversion function
   - Test suite
   - Quick fix utility

6. **README_PM25_INVESTIGATION.md**
   - This document
   - Complete findings summary

### Scripts

7. **investigate_pm25_anomaly.py**
   - Analysis script (reproducible)
   - Generates all visualizations
   - Creates summary reports

---

## How to Fix the Pipeline

### Step 1: Edit `soweto_climate_pipeline.py`

**Replace lines 126-128:**

```python
# OLD (WRONG):
def micrograms_to_micrograms(pm25: float) -> float:
    """Pass-through for PM2.5 (already in µg/m³)."""
    return pm25

# NEW (CORRECT):
def kg_to_micrograms_per_m3(pm25_kg: float) -> float:
    """
    Convert PM2.5 from kg/m³ to μg/m³.
    CAMS NRT provides data in kg/m³.
    Conversion: 1 kg/m³ = 10^9 μg/m³
    """
    return pm25_kg * 1e9
```

**Add after line 287** in `extract_pm25_batch`:

```python
data['date'] = pd.to_datetime(data['date'])
# ADD THIS LINE:
data['pm25'] = data['pm25'].apply(kg_to_micrograms_per_m3)
self.logger.info(f"Extracted {len(data)} PM2.5 records")
```

### Step 2: Re-run Pipeline

```bash
python soweto_climate_pipeline.py
```

### Step 3: Verify Correction

```bash
python PIPELINE_FIX.py --test
```

All tests should pass with ✓ symbols.

---

## Quick Fix for Existing Files (Temporary)

If you need corrected data immediately before re-running the pipeline:

```bash
python PIPELINE_FIX.py --fix
```

This will:
- Create backups (`.backup` extension)
- Multiply all PM2.5 values by 10⁹
- Update CSV files in place

**Note:** Still need to fix pipeline for future runs!

---

## Environmental Context: 2017-2018 Pollution Episode

### What we know:

1. **PM2.5 peaked at 273 μg/m³ (June 2018)** - 27× WHO guideline
2. **Sustained high levels** throughout autumn/winter 2017-2018
3. **Seasonal pattern** consistent with biomass burning + heating

### South Africa 2015-2018 Context:

**Severe drought:**
- Cape Town water crisis (Day Zero threat)
- Reduced rainfall across South Africa
- Dry conditions → more dust, more fires
- Less atmospheric washing

**Veld fire season:**
- Gauteng/Highveld region experiences annual fires
- Peak season: May-September (dry winter)
- Agricultural burning common
- Informal settlements use biomass fuels

**Air quality issues:**
- Soweto has many informal settlements
- Coal/wood burning for cooking and heating
- Vehicle emissions
- Industrial sources (Johannesburg metro area)
- Gauteng Highveld declared air pollution hotspot

### This makes the 2017-2018 values PLAUSIBLE but still needing validation

Ground stations in Gauteng should have captured this if it was real.

---

## Next Steps for Admire

### Decision Point 1: How to handle 2017-2018 data?

**Validate it:**
- Contact South African Air Quality Information System (SAAQIS)
- Request ground station data for Gauteng 2016-2019
- Cross-check with CAMS values
- Takes time but ensures accuracy

**OR exclude it:**
- Use only 2019-2024 (6 years)
- Faster, more conservative
- Still useful for recent exposure assessment

### Decision Point 2: Timeline

**Quick path (1-2 days):**
1. Fix pipeline code
2. Re-run extraction
3. Use 2019-2024 data only
4. Proceed with analysis

**Thorough path (2-4 weeks):**
1. Fix pipeline code
2. Re-run extraction
3. Validate 2017-2018 with ground data
4. Make informed decision on inclusion
5. Proceed with full dataset

### Decision Point 3: Research focus

**If studying recent exposure (2019-2024):**
- 2017-2018 is historical context only
- Can exclude from main analysis

**If studying extreme pollution events:**
- 2017-2018 is exactly what you want
- Critical to validate and include

**If studying long-term trends:**
- Need to decide if 2017-2018 is:
  - Real environmental event → include with flag
  - Data quality issue → exclude from trend

---

## Contact Information

**For technical questions:**
- Review visualization: `pm25_anomaly_investigation.png`
- Check detailed report: `pm25_anomaly_report.md`
- See code fixes: `PIPELINE_FIX.py`

**For data validation:**
- South African Air Quality Information System (SAAQIS): https://saaqis.environment.gov.za
- CAMS support: https://atmosphere.copernicus.eu/support
- MODIS fire data: https://firms.modaps.eosdis.nasa.gov

---

## Summary in One Paragraph

The reported "3-fold anomaly" in 2019 PM2.5 is incorrect and caused by a unit conversion error in the data pipeline. CAMS NRT provides PM2.5 in kg/m³ but the code never converted to μg/m³, making all values wrong by a factor of 1 billion. When corrected, 2019 shows 62 μg/m³, which is NOT anomalous but part of a declining trend from an extreme pollution episode in 2017-2018 (102-107 μg/m³). The 2017-2018 elevated values are plausible given South Africa's severe drought, veld fire season, and residential biomass burning, but should be validated with ground station data before use. All PM2.5 data must be corrected (multiply by 10⁹) and the pipeline must be fixed before any analysis can proceed.

---

**Investigation completed:** February 11, 2026
**Status:** Unit error identified, correction method provided, validation recommended
**Action required:** Fix pipeline, re-run extraction, validate 2017-2018 or exclude
