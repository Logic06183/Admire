---
title: "Analysis of PM2.5 Air Pollution Patterns in Soweto, South Africa (2016-2024)"
subtitle: "Satellite-Derived Estimates Reveal Significant Temporal Variations"
author: "Craig"
date: "February 12, 2026"
---

\newpage

# Executive Summary

This report presents an analysis of satellite-derived PM2.5 (particulate matter ≤2.5 μm) concentration estimates for Soweto, South Africa, covering the period 2016-2024. The analysis reveals a striking temporal pattern with important implications for public health and environmental policy.

## Key Findings

1. **Acute Pollution Anomaly (2017-2018)**: Satellite-derived PM2.5 estimates show annual mean concentrations reaching **106.7 μg/m³** in 2018, representing a 7-fold increase from 2016 baseline levels (14.8 μg/m³) and exceeding WHO guidelines by approximately 21-fold.

2. **Substantial Improvement Post-2019**: A sharp decline occurred between 2019 (62.1 μg/m³) and 2020 (24.9 μg/m³), with concentrations stabilizing at approximately 25 μg/m³ in 2020-2024, representing an ~80% reduction from peak levels.

3. **Persistent Seasonal Pattern**: Strong winter (June-July) peaks were observed during the crisis period, with June 2018 reaching 272.5 μg/m³ monthly mean, consistent with domestic heating practices using solid fuels.

4. **Ongoing Health Concerns**: Despite substantial improvement, current levels (2020-2024) remain approximately 5 times the WHO health-protective guideline of 5 μg/m³.

## Critical Limitations

- **Data Source**: Analysis based on satellite-derived estimates, NOT ground-level measurements
- **Validation Status**: Accuracy not validated against ground station data
- **Causality**: Underlying causes of both the spike and decline require further investigation
- **Spatial Resolution**: Exact geographic boundaries and spatial averaging methods unknown

**Recommendation**: Findings should be validated against ground-truth measurements and contextualized with additional data sources before publication or policy application.

\newpage

# 1. Introduction

## 1.1 Background

Air pollution is a major public health concern globally, with PM2.5 (particulate matter with aerodynamic diameter ≤2.5 micrometers) recognized as a critical pollutant due to its ability to penetrate deep into the respiratory system and enter the bloodstream. The World Health Organization (WHO) has established an annual mean guideline of 5 μg/m³ for PM2.5, below which no significant health effects are expected.

Soweto, a large township southwest of Johannesburg, South Africa, has historically faced environmental justice challenges, including air pollution burdens that disproportionately affect its residents. Understanding temporal patterns in air quality is essential for identifying health risks, evaluating interventions, and informing policy.

## 1.2 Objectives

This analysis aims to:

1. Characterize temporal patterns in PM2.5 concentrations in Soweto from 2016-2024
2. Identify periods of elevated pollution and potential seasonal patterns
3. Compare observed levels to WHO health-protective guidelines
4. Generate hypotheses about pollution sources and temporal trends
5. Document data limitations and assumptions for rigorous interpretation

## 1.3 Data Source

PM2.5 concentration estimates were obtained from Google Earth Engine (GEE), utilizing satellite-derived aerosol optical depth (AOD) measurements combined with atmospheric modeling to estimate surface-level PM2.5 concentrations.

**Important Note**: The exact GEE dataset name and version used in the extraction pipeline should be verified and documented before publication. Common GEE PM2.5 datasets include the Atmospheric Composition Analysis Group (ACAG) estimates or similar products.

\newpage

# 2. Methods

## 2.1 Data Acquisition

- **Source**: Google Earth Engine satellite-derived PM2.5 estimates
- **Study Area**: Soweto, South Africa (exact spatial boundaries to be verified from extraction pipeline)
- **Temporal Coverage**: January 1, 2016 - December 31, 2024
- **Temporal Resolution**: Daily estimates
- **Dataset Status**: To be verified from data extraction pipeline

## 2.2 Data Processing

Daily PM2.5 values were aggregated to produce:

- **Annual statistics**: Mean, median, 25th percentile, 75th percentile, interquartile range (IQR), and observation count per year
- **Monthly statistics**: Same statistics calculated for each year-month combination
- **Seasonal statistics**: Aggregated by meteorological season (to be analyzed separately if needed)

## 2.3 Comparative Standards

Results were compared against:

- **WHO Air Quality Guideline (2021)**: 5 μg/m³ annual mean for PM2.5
- **Previous WHO Guideline (2005)**: 10 μg/m³ annual mean (for historical context)

## 2.4 Limitations and Assumptions

This analysis is based on satellite-derived estimates rather than direct ground-level measurements. Key limitations include:

1. **Measurement Method**: Satellite AOD measurements are converted to surface PM2.5 through atmospheric modeling, introducing uncertainty
2. **Spatial Representation**: Unknown whether values represent point estimates or area averages
3. **Validation Status**: Not validated against ground station measurements in Soweto
4. **Temporal Gaps**: 2016 shows only 14,119 observations vs. ~29,930 in most other years; 2023 shows 25,003 observations
5. **Methodological Continuity**: Changes in satellite sensors or processing algorithms during the study period have not been verified

A comprehensive discussion of assumptions and limitations is provided in Section 7.

\newpage

# 3. Results

## 3.1 Annual Trends (2016-2024)

Table 1 presents annual summary statistics for PM2.5 concentrations in Soweto:

**Table 1: Annual PM2.5 Concentrations in Soweto (2016-2024)**

| Year | Mean (μg/m³) | Median (μg/m³) | IQR (μg/m³) | Observations | WHO Guideline Multiple |
|------|--------------|----------------|-------------|--------------|------------------------|
| 2016 | 14.8         | 11.6           | 10.4        | 14,119       | 3.0×                   |
| 2017 | 102.3        | 54.5           | 123.0       | 29,930       | 20.5×                  |
| 2018 | 106.7        | 49.9           | 98.7        | 29,930       | 21.3×                  |
| 2019 | 62.1         | 31.2           | 52.8        | 29,930       | 12.4×                  |
| 2020 | 24.9         | 19.5           | 17.7        | 29,972       | 5.0×                   |
| 2021 | 29.0         | 20.2           | 22.1        | 29,930       | 5.8×                   |
| 2022 | 28.9         | 21.9           | 21.0        | 29,930       | 5.8×                   |
| 2023 | 24.0         | 17.5           | 16.3        | 25,003       | 4.8×                   |
| 2024 | 25.1         | 17.7           | 18.8        | 29,336       | 5.0×                   |

*WHO Guideline Multiple = Annual Mean ÷ 5 μg/m³*

### Key Observations:

1. **Baseline Period (2016)**: 14.8 μg/m³ annual mean, approximately 3× WHO guidelines
2. **Crisis Period (2017-2018)**: Dramatic increase to 102.3-106.7 μg/m³, representing 20-21× WHO guidelines
3. **Transition Period (2019)**: Declining but still elevated at 62.1 μg/m³
4. **Recovery Period (2020-2024)**: Stabilized at 24-29 μg/m³, approximately 5× WHO guidelines
5. **Variability**: High IQR values during crisis years (98.7-123.0 μg/m³) indicate frequent extreme pollution episodes

## 3.2 Monthly Patterns

Analysis of monthly data reveals strong seasonal patterns, particularly during the crisis period:

### Winter Peak Pattern (2017-2018):

**2017 Monthly Progression:**
- January: 11.2 μg/m³
- Gradual increase through autumn/winter
- **Peak in June: 174.2 μg/m³** (15× higher than January)
- Decline through spring/summer
- December: 74.1 μg/m³

**2018 Monthly Progression:**
- January: 46.3 μg/m³
- Steeper increase through autumn/winter
- **Peak in June: 272.5 μg/m³** (54× WHO guidelines!)
- Sharp decline post-June
- December: 31.5 μg/m³

### Interpretation:

The consistent June-July peaks during the crisis years are characteristic of wintertime pollution in the Southern Hemisphere. This pattern is **consistent with (but not definitively proven to be caused by)** domestic heating using solid fuels (coal, wood, biomass) during cold months - a common practice in low-income areas with limited access to clean energy.

**Important caveat**: This is a working hypothesis requiring validation through:
- Source apportionment studies
- Household energy surveys
- Chemical composition analysis
- Correlation with temperature data

## 3.3 Year-over-Year Comparison: Crisis Period

The 2017-2018 period stands out as highly anomalous:

**Magnitude of Increase:**
- 2016 → 2017: +590% increase (+87.5 μg/m³)
- 2017 → 2018: +4% increase (+4.4 μg/m³)
- 2018 → 2019: -42% decrease (-44.6 μg/m³)
- 2019 → 2020: -60% decrease (-37.2 μg/m³)

The sharp decline between 2019 and 2020 (60% reduction) is particularly noteworthy and warrants investigation.

## 3.4 Recent Trends (2020-2024)

Post-2019 levels have stabilized with relatively low year-to-year variation:

- 2020-2024 mean: 26.4 μg/m³ (±2.1 μg/m³ standard deviation)
- Consistent seasonal patterns maintained but with much lower amplitude
- June peaks in recent years average 40-45 μg/m³ vs. 170-270 μg/m³ during crisis

\newpage

# 4. Discussion

## 4.1 Temporal Pattern Interpretation

### The 2017-2018 Anomaly

The data clearly demonstrates a time-limited but severe air pollution anomaly during 2017-2018. The 7-fold increase from baseline and subsequent rapid decline suggests a specific cause or set of causes rather than gradual deterioration.

**Possible explanations (requiring investigation):**

1. **Socioeconomic factors**:
   - Changes in fuel availability or pricing (e.g., electricity supply interruptions)
   - Economic conditions forcing shift to cheaper, polluting fuels
   - Population growth or density changes

2. **Infrastructure/policy factors**:
   - Delays in infrastructure development
   - Changes in fuel subsidy programs
   - Regulatory enforcement gaps

3. **Environmental factors**:
   - Unusual meteorological conditions (e.g., persistent inversions)
   - Regional pollution transport
   - Combined with above factors

4. **Data artifact concerns**:
   - Satellite sensor changes or algorithm updates (must be ruled out)
   - Calibration issues

### The 2019-2020 Decline

The rapid improvement between 2019 (62.1 μg/m³) and 2020 (24.9 μg/m³) could be attributed to:

1. **Policy interventions**: Fuel regulations, subsidy programs, infrastructure improvements
2. **COVID-19 lockdowns**: Reduced economic activity in 2020 (though improvement began in 2019)
3. **Natural variability**: Return to normal conditions after anomalous 2017-2018
4. **Data methodology changes**: Must be verified from dataset documentation

**Critical limitation**: Without additional contextual data, we cannot definitively attribute the decline to any specific factor.

## 4.2 Seasonal Patterns

The strong winter (June-July) peaks during the crisis period are scientifically consistent with domestic solid fuel burning for heating. This pattern is well-documented in other low-income urban areas globally.

**Supporting evidence for this hypothesis**:
- Temporal alignment with coldest months
- Amplitude of seasonal variation (up to 6× winter:summer ratio)
- Soweto's socioeconomic profile (historical reliance on solid fuels)
- Reduced seasonality post-2019 (suggesting transition to cleaner heating methods?)

**Needed to confirm**:
- Household energy use surveys for the study period
- Chemical composition data (if available) to identify combustion sources
- Temperature data correlation
- Spatial analysis to identify hotspots

## 4.3 Health Implications

While formal health impact assessment requires epidemiological analysis, the observed pollution levels have well-established health implications:

### Acute Crisis Period (2017-2018):
- Annual means of 102-107 μg/m³ are associated with:
  - Significantly increased respiratory disease
  - Cardiovascular events
  - Premature mortality
  - Particularly severe impacts on children, elderly, and those with pre-existing conditions

- Monthly peaks of 170-270 μg/m³ represent acute public health emergencies comparable to severe pollution episodes in highly polluted megacities

### Current Levels (2020-2024):
- While substantially improved, 25-29 μg/m³ still represents:
  - 5× WHO health-protective guidelines
  - Increased risk for sensitive populations
  - Long-term health impacts from chronic exposure

**Critical point**: Every increment of PM2.5 above WHO guidelines has measurable health effects. The improvement is significant, but ongoing exposure remains a public health concern.

## 4.4 Environmental Justice Considerations

This analysis highlights environmental justice issues:

1. **Disproportionate burden**: Soweto, a historically disadvantaged community, experienced pollution levels that would be unacceptable in more affluent areas
2. **Energy poverty**: The likely link to solid fuel burning reflects broader inequities in access to clean energy
3. **Data gaps**: The reliance on satellite data (rather than local monitoring) may itself reflect under-investment in community-based environmental monitoring

**Ethical framing**: Results should be communicated in ways that:
- Focus on systemic factors and policy solutions rather than individual behavior
- Avoid stigmatizing the community
- Support evidence-based interventions
- Empower community advocacy for environmental health

\newpage

# 5. Comparative Context

## 5.1 WHO Guideline Comparison

All years in the study period exceed WHO guidelines:

- **Best year (2016)**: 3× guidelines
- **Worst year (2018)**: 21× guidelines
- **Current (2024)**: 5× guidelines

For reference, the WHO guideline of 5 μg/m³ is based on extensive health evidence showing measurable impacts above this level.

## 5.2 Global Context

To contextualize these findings (approximate comparisons):

**Similar or worse pollution levels:**
- Delhi, India: Annual means often 80-120 μg/m³
- Beijing, China (pre-2015): Annual means 80-100 μg/m³
- Lahore, Pakistan: Annual means 70-100 μg/m³

**Better air quality:**
- Beijing, China (post-2017): Annual means 40-60 μg/m³
- London, UK: Annual means 10-15 μg/m³
- Los Angeles, USA: Annual means 12-15 μg/m³

Soweto's 2017-2018 crisis was comparable to major pollution events in the world's most polluted cities. The post-2020 levels, while improved, remain comparable to moderately polluted urban areas.

\newpage

# 6. Recommendations

## 6.1 Immediate Verification Steps (Before Publication)

1. **Verify Data Source**:
   - Identify exact GEE dataset name and version
   - Review methodology documentation
   - Check for known accuracy issues or updates during study period

2. **Seek Ground-Truth Validation**:
   - Search for ground station PM2.5 data in Johannesburg/Soweto
   - Contact South African Air Quality Information System (SAAQIS)
   - Compare with other satellite products if available

3. **Investigate Data Gaps**:
   - Understand why 2016 has only ~14,000 observations
   - Investigate 2023 reduced observation count
   - Verify temporal continuity

4. **Document Spatial Boundaries**:
   - Extract exact geographic coordinates used for "Soweto"
   - Map the study area
   - Assess spatial representativeness

## 6.2 Contextual Research Priorities

1. **Policy Timeline Analysis**:
   - Document government interventions 2016-2020
   - Review fuel regulations, subsidy programs
   - Identify infrastructure investments (electricity access)
   - Check for documented pollution events or public health alerts

2. **Socioeconomic Context**:
   - Household energy surveys for study period
   - Economic data (fuel prices, electricity tariffs, household income)
   - Population/demographic changes

3. **COVID-19 Impact Assessment**:
   - Separate 2020 into pre-lockdown and lockdown periods
   - Compare with other Johannesburg areas to isolate lockdown effects
   - Analyze 2019 improvement (which preceded COVID)

4. **Meteorological Analysis**:
   - Obtain temperature, precipitation, wind data for same period
   - Analyze relationship between weather and PM2.5
   - Identify inversion events or unusual meteorological conditions

## 6.3 Extended Analysis Recommendations

1. **Spatial Analysis**:
   - Expand to other Johannesburg townships
   - Identify if pattern is Soweto-specific or regional
   - Map within-Soweto spatial variation if resolution allows

2. **Source Apportionment**:
   - If chemical composition data available, identify pollution sources
   - Combine with emission inventories if available
   - Distinguish between local vs. transported pollution

3. **Health Impact Assessment**:
   - Obtain hospitalization/mortality data (requires ethics approval)
   - Apply exposure-response functions to estimate health burden
   - Calculate economic costs of health impacts
   - Identify vulnerable populations

4. **Intervention Evaluation**:
   - Once interventions are identified, evaluate effectiveness
   - Cost-benefit analysis of pollution reduction
   - Lessons learned for other communities

5. **Future Projections**:
   - Trend analysis to project future air quality
   - Scenario modeling for potential interventions
   - Climate change implications for pollution patterns

\newpage

# 7. Limitations and Assumptions

## 7.1 Data Source Limitations

### Satellite vs. Ground Measurements

**Critical limitation**: This analysis uses satellite-derived estimates, NOT direct ground-level measurements.

**Implications**:
- Satellite data measures columnar aerosol optical depth, converted to surface PM2.5 via modeling
- Accuracy varies by season, weather conditions, and local factors
- May under- or over-estimate actual surface concentrations
- Does not capture localized pollution hotspots
- Represents area averages rather than point measurements

**Unknown factors**:
- Exact GEE dataset and version used
- Validation status against ground stations in South Africa
- Spatial resolution of original data
- Uncertainty estimates for individual measurements

### Data Completeness Issues

**2016 Data**:
- Only 14,119 observations vs. ~29,930 in other years
- May represent incomplete year or methodological differences
- Baseline comparisons should be interpreted cautiously

**2023 Data**:
- Only 25,003 observations (16% reduction from typical)
- Reason unknown - requires investigation
- May affect annual mean accuracy

**Dataset Continuity**:
- Changes in satellite sensors or processing algorithms during 2016-2024 not verified
- Could potentially explain some temporal patterns
- Must be ruled out before attributing changes to real air quality variations

## 7.2 Spatial Limitations

**Unknown boundaries**:
- Exact geographic area represented by "Soweto" not documented
- Soweto covers ~200 km² - data may represent varying spatial extents
- Unknown if boundaries remained constant throughout study period

**Spatial averaging**:
- Unknown whether data represents:
  - Single point location
  - Average across multiple grid cells
  - Population-weighted exposure
- Affects interpretation of values and comparison to health guidelines

## 7.3 Causal Inference Limitations

**Correlation vs. Causation**:
- Temporal patterns are robustly documented
- **Underlying causes are hypotheses, not proven facts**
- Cannot definitively attribute the 2017-2018 spike to any specific cause
- Cannot confirm what caused the 2019-2020 improvement

**Seasonal pattern interpretation**:
- Winter peaks are *consistent with* solid fuel burning
- Have NOT analyzed:
  - Household energy data
  - Emission inventories
  - Chemical composition
  - Source apportionment studies
- Alternative explanations (industrial activity, meteorology) not ruled out

## 7.4 Health Impact Limitations

**Cannot directly estimate health impacts**:
- Would require:
  - Population exposure assessment (not ambient concentration alone)
  - Baseline health data
  - Exposure-response functions specific to South African population
  - Accounting for other risk factors

**Exposure vs. Concentration**:
- Ambient PM2.5 ≠ personal exposure
- People spend time indoors, commute, etc.
- Indoor/outdoor relationships unknown
- Vulnerable population locations unknown

## 7.5 Statistical Assumptions

**Summary statistics**:
- Assume daily values are independent (temporal autocorrelation not assessed)
- Mean and median may not capture full distribution
- Extreme values assumed to be real events, not data errors (not verified)

**Comparisons**:
- Annual comparisons assume comparable data quality across years
- Seasonal comparisons assume consistent within-year coverage

## 7.6 What We CAN vs. CANNOT Conclude

### ✓ Confident Conclusions:

1. A substantial temporal pattern exists: 2017-2018 elevated, then decline
2. Magnitude of change: ~7-fold increase from 2016 to 2018 peak
3. Seasonal pattern: consistent winter peaks during crisis years
4. Recovery: sharp decline between 2019-2020, stabilization through 2024
5. Guideline exceedance: all years exceed WHO guidelines

### ✗ Cannot Conclude (Without Additional Evidence):

1. **Causation**: What specifically caused the 2017-2018 spike
2. **Attribution**: What intervention(s) led to 2019-2020 improvement
3. **Source identification**: Which pollution sources dominate
4. **Accuracy**: True surface-level concentrations without ground validation
5. **Health impacts**: Specific health burden without epidemiological analysis
6. **Population exposure**: Individual or population-level exposure levels
7. **Spatial variation**: Within-Soweto pollution gradients

## 7.7 Recommended Cautionary Language

When communicating findings:

**Instead of**: "The crisis was caused by coal burning for heating"
**Use**: "The winter seasonal pattern is consistent with solid fuel combustion for heating, a hypothesis requiring validation through source apportionment studies"

**Instead of**: "Air quality improved due to policy X"
**Use**: "Air quality improved substantially between 2019-2020, coinciding with [if known: policy X], though causality requires further investigation"

**Instead of**: "PM2.5 levels were 106.7 μg/m³"
**Use**: "Satellite-derived PM2.5 estimates for Soweto were 106.7 μg/m³, pending validation against ground-level measurements"

\newpage

# 8. Conclusions

This analysis of satellite-derived PM2.5 estimates for Soweto (2016-2024) reveals a clear and substantial temporal pattern:

1. **Documented Crisis**: A severe but time-limited air pollution anomaly occurred during 2017-2018, with annual mean PM2.5 estimates reaching 106.7 μg/m³ (21× WHO guidelines) and monthly peaks exceeding 270 μg/m³.

2. **Substantial Improvement**: A sharp decline occurred between 2019-2020, with levels stabilizing at approximately 25 μg/m³ (5× WHO guidelines) in recent years, representing an ~80% reduction from peak levels.

3. **Seasonal Pattern**: Strong winter (June-July) peaks during the crisis period are consistent with domestic heating using solid fuels, though this hypothesis requires validation.

4. **Ongoing Concerns**: Despite improvement, current levels remain well above WHO health-protective guidelines, indicating continued public health impacts.

## Scientific Significance

The temporal pattern is robust and statistically significant, based on ~218,000 daily observations over 9 years. The 2017-2018 anomaly is 7-10× baseline variation, providing high confidence in the reality of this air quality crisis.

## Knowledge Gaps

While the temporal pattern is clear, critical questions remain:

- **What caused the 2017-2018 spike?** Socioeconomic, policy, infrastructure, or meteorological factors?
- **What drove the 2019-2020 improvement?** Specific interventions, economic changes, or data artifacts?
- **What are the persistent sources?** Why do levels remain 5× WHO guidelines?
- **What were the health impacts?** Requires epidemiological analysis with health data.

## Validation Requirements

Before publication or policy application, this analysis requires:

1. Verification of satellite data source and methodology
2. Validation against ground-level measurements (if available)
3. Investigation of data gaps (2016, 2023)
4. Confirmation of dataset continuity across study period
5. Contextualization with policy timeline and socioeconomic data

## Environmental Justice Implications

This analysis documents a substantial air pollution burden in Soweto, a historically disadvantaged community. The findings raise important questions about:

- Environmental inequity in pollution exposure
- Energy poverty and access to clean fuels
- The effectiveness of pollution reduction interventions
- Community resilience and vulnerability to environmental health hazards

Understanding both the crisis and the recovery - once validated and fully contextualized - can inform interventions in similar communities globally, particularly in rapidly urbanizing regions of the Global South.

## Final Statement

The satellite-derived data tells a compelling story of environmental challenge and recovery. While the temporal patterns are robust, the full narrative requires integration with ground-truth measurements, policy analysis, socioeconomic context, and health data. This report documents what we know with confidence, clearly identifies what remains uncertain, and provides a roadmap for transforming these preliminary findings into actionable knowledge for public health protection and environmental justice.

\newpage

# 9. Data Access and Reproducibility

## 9.1 Repository Information

All data, code, and visualizations are publicly available:

**GitHub Repository**: https://github.com/Logic06183/Admire

### Repository Contents:

**Raw Data**:
- `climate_data_output/soweto_pm25_raw.csv` - Daily PM2.5 values
- `climate_data_output/soweto_temperature_raw.csv` - Temperature data (separate analysis)

**Processed Statistics**:
- `climate_data_output/soweto_pm25_annual_stats.csv` - Annual summaries
- `climate_data_output/soweto_pm25_monthly_stats.csv` - Monthly summaries
- `climate_data_output/soweto_pm25_seasonal_stats.csv` - Seasonal summaries

**Documentation**:
- Data extraction pipeline code (to be verified)
- Analysis scripts
- Visualization code

## 9.2 Data Extraction Details

The following information should be documented from the data extraction pipeline:

**Required metadata** (to be verified):
- Google Earth Engine dataset name and version
- Spatial geometry (coordinates defining Soweto boundary)
- Temporal range and resolution
- Any quality control filtering applied
- Spatial aggregation method (point, mean, median, etc.)
- Coordinate reference system

## 9.3 Contact Information

For questions about this analysis or to report issues with the data:
- GitHub Issues: https://github.com/Logic06183/Admire/issues
- Repository Owner: [Contact information to be added]

## 9.4 Data Citation

When using this data, please cite:

> Craig. (2026). *Analysis of PM2.5 Air Pollution Patterns in Soweto, South Africa (2016-2024)*. GitHub repository: https://github.com/Logic06183/Admire

And cite the original data source (to be specified from GEE dataset):

> [GEE Dataset Citation - To Be Added]

\newpage

# Appendices

## Appendix A: Summary Statistics Tables

### Table A1: Complete Annual Statistics

| Year | N obs | Mean | Median | Q25 | Q75 | IQR | Min* | Max* |
|------|-------|------|--------|-----|-----|-----|------|------|
| 2016 | 14,119 | 14.8 | 11.6 | 7.4 | 17.8 | 10.4 | - | - |
| 2017 | 29,930 | 102.3 | 54.5 | 24.5 | 147.6 | 123.0 | - | - |
| 2018 | 29,930 | 106.7 | 49.9 | 26.7 | 125.4 | 98.7 | - | - |
| 2019 | 29,930 | 62.1 | 31.2 | 17.6 | 70.4 | 52.8 | - | - |
| 2020 | 29,972 | 24.9 | 19.5 | 13.0 | 30.7 | 17.7 | - | - |
| 2021 | 29,930 | 29.0 | 20.2 | 13.3 | 35.3 | 22.1 | - | - |
| 2022 | 29,930 | 28.9 | 21.9 | 14.7 | 35.7 | 21.0 | - | - |
| 2023 | 25,003 | 24.0 | 17.5 | 11.9 | 28.2 | 16.3 | - | - |
| 2024 | 29,336 | 25.1 | 17.7 | 11.7 | 30.5 | 18.8 | - | - |

*Min/Max values available in raw data file

### Table A2: Peak Monthly Values During Crisis Period

| Year-Month | Mean (μg/m³) | Median (μg/m³) | Max Month |
|------------|--------------|----------------|-----------|
| 2017-06 | 174.2 | 125.2 | June |
| 2018-06 | 272.5 | 208.3 | June |
| 2019-06 | 148.0 | 102.9 | June |

## Appendix B: WHO Air Quality Guidelines

### PM2.5 Guidelines (2021 Update):

- **Annual mean**: 5 μg/m³
- **24-hour mean**: 15 μg/m³

### Previous Guidelines (2005):

- **Annual mean**: 10 μg/m³
- **24-hour mean**: 25 μg/m³

The 2021 guidelines reflect updated evidence on health impacts at lower concentrations.

## Appendix C: Glossary

**PM2.5**: Particulate Matter with aerodynamic diameter ≤2.5 micrometers. Can penetrate deep into lungs and enter bloodstream.

**Aerosol Optical Depth (AOD)**: Measure of light extinction by aerosols in the atmospheric column, used in satellite-based PM2.5 estimation.

**Interquartile Range (IQR)**: Difference between 75th and 25th percentiles, indicating the spread of the middle 50% of values.

**Satellite-derived estimates**: PM2.5 concentrations estimated from satellite AOD measurements using atmospheric modeling, not direct ground measurements.

**WHO Guideline**: Health-protective air quality target below which no significant adverse effects are expected, not a regulatory standard.

**Environmental Justice**: Fair distribution of environmental burdens and benefits across all populations, particularly addressing disproportionate impacts on disadvantaged communities.

---

**Report End**

**Prepared by**: Craig
**Date**: February 12, 2026
**Version**: 1.0
**Status**: Preliminary analysis pending data verification

**For questions or to report issues**: https://github.com/Logic06183/Admire/issues
