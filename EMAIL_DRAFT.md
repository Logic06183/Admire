# Email to Admire - Soweto PM2.5 Analysis

---

**To:** Admire
**Subject:** Soweto PM2.5 Analysis Complete - Critical Findings and Validation Needed

---

Hi Admire,

I've completed the analysis of the Soweto PM2.5 data (2016-2024) and compiled a comprehensive report for you. The findings are significant and reveal some important patterns that warrant further investigation.

## Quick Summary

The data shows a **severe but time-limited air pollution crisis in Soweto during 2017-2018**, with PM2.5 levels reaching 106.7 μg/m³ (21× WHO guidelines). This was followed by a dramatic improvement starting in 2019, with levels stabilizing around 25 μg/m³ in recent years - still concerning, but an 80% reduction from the peak.

## Key Documents

I've prepared three documents for you:

1. **📊 Full Analysis Report (Word)**: `Soweto_PM25_Analysis_Report.docx`
   - Comprehensive 30+ page report with methods, results, discussion, and recommendations
   - Includes data tables, interpretations, and statistical analysis
   - Ready to share with collaborators or use as basis for publication

2. **⚠️ Assumptions & Limitations**: `ASSUMPTIONS_AND_LIMITATIONS.md`
   - Critical document outlining all caveats and data quality concerns
   - **Please read this carefully before using findings for publication**
   - Documents what we can vs. cannot conclude from this data

3. **📧 Initial Email Draft**: `email_to_admire.md`
   - My original detailed explanation of the thought process

## Critical Points Before You Use This Data

**⚠️ Important Limitations:**

1. **Data Source**: This analysis uses satellite-derived estimates, NOT ground-level measurements
   - Accuracy not validated against ground stations in Soweto
   - Need to verify the exact GEE dataset used in your extraction pipeline

2. **Data Gaps**:
   - 2016 has only half the observations of other years (may be incomplete)
   - 2023 has 16% fewer observations than typical (reason unknown)

3. **Causality**: While the temporal patterns are robust, the underlying causes are hypotheses, not proven facts
   - We don't know definitively what caused the 2017-2018 spike
   - We don't know definitively what caused the 2019-2020 improvement

4. **Verification Needed**:
   - Check the data extraction pipeline to confirm the GEE dataset name/version
   - Look for any ground-truth air quality data from SAAQIS (South African Air Quality Information System)
   - Investigate whether any methodological changes occurred during 2016-2024

## What The Data DOES Show Clearly

✓ **Robust temporal pattern**: 2017-2018 anomaly is 7-10× baseline variation
✓ **Strong seasonal pattern**: Winter (June) peaks consistent with solid fuel burning
✓ **Substantial improvement**: Sharp decline between 2019-2020
✓ **Large dataset**: ~218,000 observations provide statistical confidence

## Recommended Next Steps

1. **Immediate** (before publication):
   - Verify data source from your extraction pipeline
   - Search for ground station validation data
   - Investigate 2016 and 2023 data gaps

2. **Context research**:
   - Timeline of Soweto/Johannesburg policies 2016-2020
   - Any documented pollution events during 2017-2018
   - Economic/fuel price data for the period
   - COVID-19 lockdown impact assessment

3. **Extended analysis**:
   - Compare with other Johannesburg areas (is this Soweto-specific?)
   - Correlate with temperature data (test heating hypothesis)
   - Health impact assessment if hospital/mortality data available

## Access All Files

**GitHub Repository**: https://github.com/Logic06183/Admire

All data, analysis scripts, and documentation are in the repository. The Word report is ready to share with collaborators or supervisors.

## My Interpretation

The data tells a compelling environmental justice story: a disadvantaged community experienced a severe air pollution crisis that was somehow resolved. Understanding both the crisis and the recovery could inform interventions globally. But we need to validate the satellite data and investigate the contextual factors before we can publish or make policy recommendations with confidence.

The temporal pattern is scientifically solid - what we need now is the "why" behind it.

## Questions?

Let me know if you need:
- Clarification on any findings
- Additional analysis
- Help with the temperature data analysis
- Assistance preparing this for publication
- Support investigating the data quality concerns

I'm ready to dive deeper wherever you need.

Best,
Craig

---

**P.S.** The report includes proper cautionary language for all findings, so you can share it directly with your advisor or research team. Just make sure they also review the assumptions document.

**P.P.S.** All charts/figures referenced in the report are in your original images - we may want to regenerate them with proper formatting and captions for publication if needed.
