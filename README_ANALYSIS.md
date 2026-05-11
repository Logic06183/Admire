# Soweto PM2.5 Analysis - Quick Reference Guide

**Analysis Date**: February 12, 2026
**Analyst**: Craig
**Status**: Preliminary findings pending data verification

---

## 📁 Files Created

### Main Report
- **`Soweto_PM25_Analysis_Report.docx`** (26 KB)
  - Comprehensive Word document with full analysis
  - Ready to share with collaborators/advisors
  - Includes: methods, results, discussion, limitations, recommendations
  - Has table of contents and numbered sections

### Supporting Documentation
- **`ASSUMPTIONS_AND_LIMITATIONS.md`**
  - Critical document outlining all caveats
  - **READ THIS BEFORE PUBLICATION**
  - Documents what we can vs. cannot conclude

- **`email_to_admire.md`**
  - Initial detailed explanation
  - Shows thought process and analysis approach

- **`EMAIL_DRAFT.md`**
  - Ready-to-send email summarizing findings
  - Links to GitHub repository
  - Highlights key points and limitations

---

## 🔑 Key Findings (30-Second Summary)

1. **Crisis Period (2017-2018)**
   - PM2.5 reached 106.7 μg/m³ (21× WHO guidelines)
   - June 2018 peak: 272.5 μg/m³ monthly mean
   - Comparable to worst pollution in Delhi/Beijing

2. **Recovery (2019-2020)**
   - Sharp 60% decline from 2019 to 2020
   - Stabilized at ~25 μg/m³ (still 5× WHO guidelines)
   - 80% improvement from peak

3. **Seasonal Pattern**
   - Winter (June) peaks during crisis
   - Consistent with solid fuel burning for heating
   - Hypothesis requiring validation

---

## ⚠️ Critical Limitations

- Based on **satellite estimates**, not ground measurements
- Data gaps in 2016 and 2023
- Causes of spike and decline are hypotheses, not proven
- Needs validation before publication

---

## 📊 Data Location

**GitHub Repository**: https://github.com/Logic06183/Admire

**Raw Data**:
- `climate_data_output/soweto_pm25_raw.csv` (daily values)
- `climate_data_output/soweto_pm25_annual_stats.csv`
- `climate_data_output/soweto_pm25_monthly_stats.csv`

---

## ✅ Before Publishing

1. Verify GEE dataset source from extraction pipeline
2. Search for ground station validation data (SAAQIS)
3. Investigate 2016/2023 data gaps
4. Research policy timeline 2016-2020
5. Review `ASSUMPTIONS_AND_LIMITATIONS.md`

---

## 📈 Comparison to WHO Guidelines

| Year | PM2.5 (μg/m³) | × WHO Guideline |
|------|---------------|-----------------|
| 2016 | 14.8 | 3.0× |
| 2017 | 102.3 | 20.5× |
| **2018** | **106.7** | **21.3×** |
| 2019 | 62.1 | 12.4× |
| 2020 | 24.9 | 5.0× |
| 2021 | 29.0 | 5.8× |
| 2022 | 28.9 | 5.8× |
| 2023 | 24.0 | 4.8× |
| 2024 | 25.1 | 5.0× |

*WHO Guideline: 5 μg/m³ annual mean*

---

## 🎯 Next Steps

### Priority 1: Validation
- [ ] Confirm data source and methodology
- [ ] Find ground-truth comparison data
- [ ] Verify dataset continuity

### Priority 2: Context
- [ ] Policy timeline research
- [ ] Economic/fuel price data
- [ ] Temperature correlation analysis

### Priority 3: Extension
- [ ] Compare other Johannesburg areas
- [ ] Health impact assessment
- [ ] Source apportionment if data available

---

## 💡 Research Questions Generated

1. What caused the 2017-2018 spike?
2. What intervention led to 2019-2020 improvement?
3. Why does seasonality disappear post-2019?
4. What are current persistent sources?
5. What were the health impacts?
6. Is this Soweto-specific or city-wide?

---

## 📞 Contact

For questions about this analysis:
- GitHub Issues: https://github.com/Logic06183/Admire/issues

---

**Last Updated**: February 12, 2026
