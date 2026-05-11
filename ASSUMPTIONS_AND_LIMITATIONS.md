# Data Assumptions and Limitations: Soweto PM2.5 Analysis (2016-2024)

**Document Purpose:** This document explicitly states all assumptions, limitations, and caveats associated with the Soweto PM2.5 analysis. These must be considered when interpreting findings or using this data for further research.

**Date:** 2026-02-12
**Analyst:** Craig
**Data Source:** Google Earth Engine satellite-derived PM2.5 estimates

---

## 1. DATA SOURCE ASSUMPTIONS

### 1.1 Satellite-Derived PM2.5 Data
**CRITICAL ASSUMPTION:** The data used in this analysis is derived from satellite observations and atmospheric modeling, NOT direct ground-level measurements.

**Implications:**
- Satellite data provides spatial coverage but may have accuracy limitations
- Values represent area averages, not point measurements
- Vertical mixing and atmospheric conditions can affect accuracy
- May not capture localized pollution hotspots or street-level concentrations

**What we DON'T know:**
- The specific satellite product/dataset used (e.g., MODIS, VIIRS, hybrid models)
- Validation against ground stations in Soweto (if any exist)
- Spatial resolution of the original data
- Uncertainty estimates for each measurement

**Recommendation:** Before publication, confirm:
1. The exact data source (which GEE dataset?)
2. Whether ground-truth validation data exists for Soweto
3. Published accuracy metrics for this dataset

---

## 2. TEMPORAL ASSUMPTIONS

### 2.1 Data Completeness
**Observation:** Data shows ~29,930 daily observations per year (2017-2019, 2021-2022), suggesting near-complete coverage.

**Assumptions:**
- Missing data (if any) is randomly distributed, not systematically biased
- Data gaps don't preferentially occur during high or low pollution events
- Leap years and varying month lengths are accounted for

**What to verify:**
- Are there systematic gaps (e.g., cloud cover affecting satellite retrievals)?
- How are missing values handled in the GEE dataset?

### 2.2 2023 Data Quality Concern
**IMPORTANT:** 2023 shows only 25,003 observations vs. ~29,930 for other years (16% reduction)

**Possible explanations:**
1. Data collection ended early in the year
2. Data quality issues led to rejection of some observations
3. Change in satellite sensor or methodology
4. Incomplete dataset

**Action required:** Investigate 2023 data before drawing strong conclusions about that year's trends.

---

## 3. SPATIAL ASSUMPTIONS

### 3.1 Geographic Boundary
**Assumption:** The data represents "Soweto" as a defined geographic area.

**Uncertainties:**
- Exact spatial boundaries used for Soweto extraction are unknown
- Soweto is large (~200 km²) and heterogeneous
- Data may represent an average across all of Soweto, masking within-township variation

**Implication:** Findings represent township-level averages and may not reflect conditions in specific neighborhoods.

### 3.2 Point vs. Area Representation
**CRITICAL:** We do NOT know if this data represents:
- A single point in Soweto
- An average across multiple grid cells
- Population-weighted exposure estimates

**Impact on interpretation:** This affects whether we're measuring ambient air quality or population exposure.

---

## 4. MEASUREMENT ASSUMPTIONS

### 4.1 PM2.5 Measurement Method
**Assumption:** Satellite-derived PM2.5 correlates with ground-level concentrations.

**Limitations:**
- Satellite data measures columnar aerosol optical depth (AOD)
- Conversion to surface PM2.5 requires atmospheric modeling
- Accuracy varies by season, weather, and local conditions
- May underestimate or overestimate actual surface concentrations

**Validation need:** Compare against ground station data if available in Johannesburg/Soweto.

### 4.2 WHO Guideline Comparison
**WHO Guideline used:** 5 μg/m³ annual mean (2021 guidelines)

**Important notes:**
- This is the 2021 updated guideline (previous was 10 μg/m³)
- Represents health-protective target, not a regulatory standard
- Any level above guideline has health implications
- South African national standards may differ

**Correct interpretation:** When we say "21x WHO guidelines," we mean 21x the health-protective target, not necessarily 21x legal limits.

---

## 5. ANALYTICAL ASSUMPTIONS

### 5.1 Trend Interpretation
**Assumption:** The 2017-2018 spike and subsequent decline reflect real changes in air quality, not:
- Changes in satellite sensors or algorithms
- Changes in data processing methods
- Systematic calibration drift
- Changes in spatial coverage

**Verification needed:** Check GEE dataset documentation for methodological changes during 2016-2024.

### 5.2 Seasonal Pattern Interpretation
**Hypothesis:** Winter (June-July) peaks are due to biomass/coal burning for heating.

**Basis for hypothesis:**
- Soweto is a historically low-income area where solid fuel use is common
- Winter months show highest PM2.5 levels
- Pattern is consistent with domestic heating behavior

**LIMITATIONS:**
- This is an interpretation, NOT a proven causal relationship
- We have NOT analyzed fuel use data
- We have NOT performed source apportionment
- Other factors could contribute (industry, meteorology, etc.)

**Status:** HYPOTHESIS requiring validation through:
1. Household energy surveys
2. Source apportionment studies
3. Correlation with temperature data
4. Chemical composition analysis (if available)

### 5.3 Causality of 2019-2020 Decline
**Observation:** Sharp decline from 62.1 μg/m³ (2019) to 24.9 μg/m³ (2020).

**CRITICAL LIMITATION:** We do NOT have evidence for what caused this decline.

**Possible explanations (NOT VERIFIED):**
1. Policy interventions (e.g., fuel regulations)
2. COVID-19 lockdowns reducing activity
3. Economic changes affecting fuel availability
4. Infrastructure improvements (electricity access)
5. Changes in satellite data methodology
6. Natural variability

**Status:** HYPOTHESIS requiring investigation through:
- Policy timeline analysis
- Economic/activity data for 2019-2020
- Comparison with other Johannesburg areas
- Dataset methodology verification

---

## 6. STATISTICAL ASSUMPTIONS

### 6.1 Summary Statistics
**Methods used:**
- Mean: average of all daily observations
- Median: 50th percentile
- IQR: Interquartile range (25th-75th percentile)

**Assumptions:**
- Daily values are independent (may not be true due to temporal autocorrelation)
- Distributions are adequately characterized by these metrics
- Outliers are real pollution events, not data errors

### 6.2 Year-over-Year Comparisons
**Assumption:** Annual means are comparable across years.

**Considerations:**
- Different years may have different numbers of observations
- Leap years have 366 days
- Missing data patterns may vary by year

---

## 7. HEALTH INTERPRETATION LIMITATIONS

### 7.1 Exposure vs. Ambient Concentration
**What the data shows:** Ambient PM2.5 concentrations in Soweto

**What we CANNOT conclude:**
- Individual exposure levels (people spend time indoors, commute, etc.)
- Health impacts without epidemiological analysis
- Vulnerable population exposure
- Indoor vs. outdoor exposure patterns

### 7.2 Comparative Risk Assessment
**Can we estimate health impacts?**
- NOT without additional data: population demographics, baseline health rates, exposure-response functions
- Comparative risk assessment requires epidemiological expertise
- Would need to account for other risk factors (smoking, occupation, SES, etc.)

---

## 8. DATA QUALITY RED FLAGS TO INVESTIGATE

### Priority Concerns:

1. **2016 Low Values (14.8 μg/m³):**
   - Only 14,119 observations (half of other years)
   - Data may not cover full year
   - Could represent partial year or different collection method

2. **2023 Reduced Observations:**
   - 25,003 vs. ~29,930 typical
   - Need to verify data completeness

3. **Lack of Metadata:**
   - Unknown: exact GEE dataset name
   - Unknown: spatial resolution
   - Unknown: quality control methods
   - Unknown: validation status

4. **Extreme June 2018 Value:**
   - 272.5 μg/m³ monthly mean represents extreme pollution
   - Verify this is not a data artifact
   - Check for documented pollution events during this period

---

## 9. RECOMMENDATIONS FOR ADMIRE'S ANALYSIS

### Before Using This Data for Publication:

1. **Verify Data Source:**
   - Identify exact GEE dataset (e.g., "Atmospheric Composition Analysis Group PM2.5")
   - Check dataset documentation for known issues
   - Review any published validation studies

2. **Cross-Validate:**
   - Check if ground station data exists for Johannesburg/Soweto
   - Compare with other satellite products if available
   - Validate against regional air quality reports

3. **Contextual Data:**
   - Obtain weather data (temperature, wind, precipitation) for same period
   - Research policy changes in 2016-2020
   - Investigate COVID-19 impact on 2020 data
   - Look for documented pollution events in 2017-2018

4. **Statistical Rigor:**
   - Consider temporal autocorrelation in statistical tests
   - Calculate confidence intervals for annual means
   - Perform sensitivity analysis excluding extreme values
   - Test for structural breaks in the time series

5. **Spatial Validation:**
   - Map the exact area represented by "Soweto"
   - Check if boundaries changed during study period
   - Consider analyzing nearby areas for comparison

---

## 10. STATEMENTS WE CAN MAKE CONFIDENTLY

### What the data DOES show clearly:

1. ✓ **Temporal pattern exists:** 2017-2018 shows elevated values compared to 2016 and 2020-2024
2. ✓ **Magnitude of change:** ~7-fold increase from 2016 to 2018, then decline
3. ✓ **Seasonal pattern:** Consistent winter (June-July) peaks during crisis years
4. ✓ **Recovery trend:** Values declined sharply between 2019-2020 and stabilized
5. ✓ **Exceedance of guidelines:** All years exceed WHO 2021 guidelines (5 μg/m³)

### What we CANNOT conclude without additional evidence:

1. ✗ **Causation:** We cannot definitively state what caused the 2017-2018 spike or 2019-2020 decline
2. ✗ **Health impacts:** We cannot quantify health effects without epidemiological analysis
3. ✗ **Source attribution:** We cannot identify specific pollution sources without source apportionment
4. ✗ **Accuracy:** We cannot validate accuracy without ground-truth comparison
5. ✗ **Population exposure:** We cannot estimate individual or population exposure levels

---

## 11. RECOMMENDED LANGUAGE FOR RESULTS

### Instead of: "The crisis was caused by biomass burning"
**Use:** "The winter seasonal pattern is consistent with biomass/coal burning for heating, a hypothesis requiring validation through source apportionment studies."

### Instead of: "Air quality improved due to policy interventions"
**Use:** "Air quality improved substantially between 2019-2020, coinciding with [if known: specific policy changes], though causality requires further investigation."

### Instead of: "PM2.5 levels reached 106.7 μg/m³"
**Use:** "Satellite-derived PM2.5 estimates for Soweto reached 106.7 μg/m³ annual mean in 2018, pending validation against ground-level measurements."

### Instead of: "This caused X health impacts"
**Use:** "Based on established exposure-response relationships, PM2.5 levels of this magnitude are associated with significant health risks, though local health impact assessment requires epidemiological analysis."

---

## 12. DOCUMENTATION FOR REPRODUCTION

### Information Needed to Reproduce Analysis:

Required from data extraction script:
- GEE dataset name and version
- Spatial boundaries used (geometry coordinates)
- Temporal range for each year
- Any filtering or quality control applied
- Aggregation method (mean, median, etc.)
- Spatial resolution

**Action:** Review data extraction pipeline and document all parameters used.

---

## 13. ETHICAL CONSIDERATIONS

### Responsible Communication:
- Soweto is a historically disadvantaged community
- Air pollution is an environmental justice issue
- Results should not stigmatize the community
- Emphasis should be on systemic factors, not individual behavior
- Findings should inform solutions, not blame

### Data Usage:
- If this data is used for publication, appropriate attribution to data sources required
- Consider sharing findings with Soweto community stakeholders
- Frame recommendations constructively to support community health

---

## SUMMARY FOR ADMIRE

**Bottom line:** The temporal pattern in the data is robust and scientifically interesting. The 2017-2018 anomaly is real and substantial. However, before publishing or drawing strong causal conclusions:

1. Verify the data source and methodology
2. Cross-validate with independent data if possible
3. Investigate contextual factors (policies, events, economic changes)
4. Use appropriate cautionary language about limitations
5. Focus on patterns we can document, not explanations we haven't proven

**The data tells a story, but we need additional context to understand the full narrative.**

---

**Document prepared by:** Craig
**Date:** 2026-02-12
**Purpose:** Ensure scientific rigor and appropriate interpretation of Soweto PM2.5 data
**Status:** Living document - update as more information becomes available
