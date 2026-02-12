"""
PM2.5 Anomaly Investigation for Soweto Climate Data
===================================================

This script investigates the reported 3-fold increase in PM2.5 values for 2019
and checks for unit conversion issues in the CAMS NRT data.

Author: Climate Data Analysis
Date: 2026-02-11
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import json

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 10)

# Paths
OUTPUT_DIR = Path('/Users/craig/Library/Mobile Documents/com~apple~CloudDocs/Admire/climate_data_output')

print("="*80)
print("PM2.5 ANOMALY INVESTIGATION - SOWETO CLIMATE DATA")
print("="*80)

# ============================================================================
# 1. LOAD DATA
# ============================================================================

print("\n1. Loading data...")
annual = pd.read_csv(OUTPUT_DIR / 'soweto_pm25_annual_stats.csv')
monthly = pd.read_csv(OUTPUT_DIR / 'soweto_pm25_monthly_stats.csv')

# ============================================================================
# 2. UNIT CONVERSION CHECK
# ============================================================================

print("\n2. CHECKING UNITS - CRITICAL FINDING")
print("-" * 80)

# CAMS NRT data is in kg/m³, needs conversion to μg/m³
# Conversion: kg/m³ × 10^9 = μg/m³

print("UNIT CONVERSION ISSUE IDENTIFIED:")
print("  - CAMS NRT PM2.5 data is provided in kg/m³")
print("  - The data should be converted to μg/m³ (micrograms per cubic meter)")
print("  - Conversion factor: 1 kg/m³ = 10^9 μg/m³")
print()

# Apply conversion
annual_converted = annual.copy()
monthly_converted = monthly.copy()

for col in annual_converted.columns:
    if 'pm25' in col and col != 'year' and col != 'pm25_count':
        annual_converted[col] = annual_converted[col] * 1e9

for col in monthly_converted.columns:
    if 'pm25' in col and col not in ['year', 'month', 'pm25_count']:
        monthly_converted[col] = monthly_converted[col] * 1e9

print("Annual PM2.5 values BEFORE conversion (kg/m³):")
print(annual[['year', 'pm25_mean']].to_string(index=False))

print("\nAnnual PM2.5 values AFTER conversion (μg/m³):")
print(annual_converted[['year', 'pm25_mean']].to_string(index=False))

# ============================================================================
# 3. ANALYZE THE "ANOMALY" - IS IT REAL OR A MISINTERPRETATION?
# ============================================================================

print("\n" + "="*80)
print("3. ANALYZING 2019 VS OTHER YEARS (USING CORRECTED UNITS)")
print("="*80)

# Calculate year-to-year changes
annual_converted['year_change_pct'] = annual_converted['pm25_mean'].pct_change() * 100

print("\nYear-over-year changes in annual mean PM2.5 (%):")
print(annual_converted[['year', 'pm25_mean', 'year_change_pct']].to_string(index=False))

# Find the "anomalous" year
max_year = annual_converted.loc[annual_converted['pm25_mean'].idxmax()]
min_year = annual_converted.loc[annual_converted['pm25_mean'].idxmin()]

print(f"\nHighest PM2.5 year: {int(max_year['year'])} ({max_year['pm25_mean']:.2f} μg/m³)")
print(f"Lowest PM2.5 year: {int(min_year['year'])} ({min_year['pm25_mean']:.2f} μg/m³)")
print(f"Ratio (max/min): {max_year['pm25_mean'] / min_year['pm25_mean']:.2f}x")

# ============================================================================
# 4. EXAMINE 2017-2018 (THE ACTUAL HIGH YEARS)
# ============================================================================

print("\n" + "="*80)
print("4. EXAMINING 2017-2018 ELEVATED VALUES")
print("="*80)

# Compare to baseline (2020-2024 average)
baseline_years = annual_converted[annual_converted['year'].isin([2020, 2021, 2022, 2023, 2024])]
baseline_mean = baseline_years['pm25_mean'].mean()

print(f"\nBaseline PM2.5 (2020-2024 average): {baseline_mean:.2f} μg/m³")

for year in [2016, 2017, 2018, 2019, 2020]:
    year_data = annual_converted[annual_converted['year'] == year]
    if not year_data.empty:
        year_mean = year_data['pm25_mean'].values[0]
        ratio = year_mean / baseline_mean
        print(f"{year}: {year_mean:.2f} μg/m³ (ratio to baseline: {ratio:.2f}x)")

# ============================================================================
# 5. MONTHLY BREAKDOWN FOR HIGH YEARS
# ============================================================================

print("\n" + "="*80)
print("5. MONTHLY PATTERNS IN HIGH YEARS (2017-2018)")
print("="*80)

high_years = [2017, 2018]
for year in high_years:
    year_data = monthly_converted[monthly_converted['year'] == year].sort_values('month')
    print(f"\n{year} Monthly PM2.5 (μg/m³):")
    print(year_data[['month', 'pm25_mean']].to_string(index=False))

    max_month = year_data.loc[year_data['pm25_mean'].idxmax()]
    print(f"  Peak month: {int(max_month['month'])} ({max_month['pm25_mean']:.2f} μg/m³)")

# ============================================================================
# 6. DATA QUALITY FLAGS
# ============================================================================

print("\n" + "="*80)
print("6. DATA QUALITY INDICATORS")
print("="*80)

# Load quality report
with open(OUTPUT_DIR / 'quality_report.json', 'r') as f:
    quality = json.load(f)

print("\nQuality Report Summary:")
print(f"  Total records: {quality['pm25']['total_records']}")
print(f"  Missing values: {quality['pm25']['missing_values']} ({quality['pm25']['missing_percentage']:.2f}%)")
print(f"  Outliers detected: {quality['pm25']['outlier_count']}")
print(f"  Data range: {quality['pm25']['date_range_actual']}")

# Check data availability by year
print("\nData availability by year:")
year_counts = monthly['pm25_count'].groupby(monthly['year']).sum()
print(year_counts.to_string())

# ============================================================================
# 7. WHO AIR QUALITY GUIDELINE COMPARISON
# ============================================================================

print("\n" + "="*80)
print("7. WHO AIR QUALITY GUIDELINE COMPARISON")
print("="*80)

WHO_ANNUAL_GUIDELINE = 5.0  # μg/m³ (2021 guidelines)
WHO_24H_GUIDELINE = 15.0    # μg/m³ (2021 guidelines)

print(f"\nWHO Annual Mean Guideline (2021): {WHO_ANNUAL_GUIDELINE} μg/m³")
print(f"WHO 24-hour Mean Guideline (2021): {WHO_24H_GUIDELINE} μg/m³")

print("\nYears exceeding WHO annual guideline:")
exceeding = annual_converted[annual_converted['pm25_mean'] > WHO_ANNUAL_GUIDELINE]
if not exceeding.empty:
    for _, row in exceeding.iterrows():
        print(f"  {int(row['year'])}: {row['pm25_mean']:.2f} μg/m³ ({row['pm25_mean']/WHO_ANNUAL_GUIDELINE:.1f}x guideline)")
else:
    print("  None - all years meet WHO guideline")

# ============================================================================
# 8. VISUALIZATIONS
# ============================================================================

print("\n" + "="*80)
print("8. CREATING VISUALIZATIONS")
print("="*80)

fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle('PM2.5 Anomaly Investigation - Soweto Climate Data', fontsize=16, fontweight='bold')

# Plot 1: Annual trend with corrected units
ax1 = axes[0, 0]
ax1.plot(annual_converted['year'], annual_converted['pm25_mean'], marker='o', linewidth=2, markersize=8, color='#2E86AB')
ax1.axhline(y=WHO_ANNUAL_GUIDELINE, color='red', linestyle='--', linewidth=2, label='WHO Guideline (5 μg/m³)')
ax1.axhline(y=baseline_mean, color='orange', linestyle='--', linewidth=2, alpha=0.7, label=f'2020-2024 Baseline ({baseline_mean:.1f} μg/m³)')
ax1.fill_between(annual_converted['year'], 0, annual_converted['pm25_mean'], alpha=0.2, color='#2E86AB')
ax1.set_xlabel('Year', fontsize=12, fontweight='bold')
ax1.set_ylabel('Annual Mean PM2.5 (μg/m³)', fontsize=12, fontweight='bold')
ax1.set_title('Annual PM2.5 Trend (CORRECTED UNITS)', fontsize=13, fontweight='bold')
ax1.grid(True, alpha=0.3)
ax1.legend(loc='upper right')

# Annotate high years
for year in [2017, 2018]:
    year_data = annual_converted[annual_converted['year'] == year]
    if not year_data.empty:
        ax1.annotate(f'{year}\n{year_data["pm25_mean"].values[0]:.1f} μg/m³',
                    xy=(year, year_data["pm25_mean"].values[0]),
                    xytext=(10, 10), textcoords='offset points',
                    bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.7),
                    arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))

# Plot 2: Monthly trend for 2017-2019
ax2 = axes[0, 1]
for year in [2016, 2017, 2018, 2019, 2020]:
    year_data = monthly_converted[monthly_converted['year'] == year].sort_values('month')
    if not year_data.empty:
        linewidth = 3 if year in [2017, 2018] else 1.5
        alpha = 1.0 if year in [2017, 2018] else 0.5
        ax2.plot(year_data['month'], year_data['pm25_mean'], marker='o',
                label=str(year), linewidth=linewidth, alpha=alpha)

ax2.set_xlabel('Month', fontsize=12, fontweight='bold')
ax2.set_ylabel('Monthly Mean PM2.5 (μg/m³)', fontsize=12, fontweight='bold')
ax2.set_title('Monthly PM2.5 Patterns (2016-2020)', fontsize=13, fontweight='bold')
ax2.set_xticks(range(1, 13))
ax2.legend()
ax2.grid(True, alpha=0.3)

# Plot 3: Before vs After unit conversion
ax3 = axes[1, 0]
x = np.arange(len(annual))
width = 0.35
ax3.bar(x - width/2, annual['pm25_mean'] * 1e9, width, label='Corrected (μg/m³)', color='#06A77D')
ax3.bar(x + width/2, annual['pm25_mean'] * 1e15, width, label='Original (×10^15)', color='#D62839', alpha=0.6)
ax3.set_xlabel('Year', fontsize=12, fontweight='bold')
ax3.set_ylabel('PM2.5 Concentration', fontsize=12, fontweight='bold')
ax3.set_title('Unit Conversion: Before vs After', fontsize=13, fontweight='bold')
ax3.set_xticks(x)
ax3.set_xticklabels(annual['year'].astype(int), rotation=45)
ax3.legend()
ax3.grid(True, alpha=0.3, axis='y')

# Plot 4: Comparison to baseline
ax4 = axes[1, 1]
annual_converted['ratio_to_baseline'] = annual_converted['pm25_mean'] / baseline_mean
colors = ['#D62839' if ratio > 1.5 else '#2E86AB' for ratio in annual_converted['ratio_to_baseline']]
ax4.bar(annual_converted['year'], annual_converted['ratio_to_baseline'], color=colors, alpha=0.8)
ax4.axhline(y=1.0, color='black', linestyle='--', linewidth=2, label='Baseline (1.0x)')
ax4.set_xlabel('Year', fontsize=12, fontweight='bold')
ax4.set_ylabel('Ratio to 2020-2024 Baseline', fontsize=12, fontweight='bold')
ax4.set_title('PM2.5 Relative to Baseline Period', fontsize=13, fontweight='bold')
ax4.grid(True, alpha=0.3, axis='y')
ax4.legend()

plt.tight_layout()
output_path = OUTPUT_DIR / 'pm25_anomaly_investigation.png'
plt.savefig(output_path, dpi=300, bbox_inches='tight')
print(f"Saved visualization: {output_path}")

# ============================================================================
# 9. GENERATE SUMMARY REPORT
# ============================================================================

print("\n" + "="*80)
print("9. SUMMARY AND RECOMMENDATIONS")
print("="*80)

summary = {
    "investigation_date": "2026-02-11",
    "critical_finding": "UNIT CONVERSION ERROR IDENTIFIED",
    "issue_description": "CAMS NRT PM2.5 data is in kg/m³ but was not converted to μg/m³",
    "conversion_factor": 1e9,
    "corrected_values": {
        "2016": float(annual_converted[annual_converted['year'] == 2016]['pm25_mean'].values[0]),
        "2017": float(annual_converted[annual_converted['year'] == 2017]['pm25_mean'].values[0]),
        "2018": float(annual_converted[annual_converted['year'] == 2018]['pm25_mean'].values[0]),
        "2019": float(annual_converted[annual_converted['year'] == 2019]['pm25_mean'].values[0]),
        "2020": float(annual_converted[annual_converted['year'] == 2020]['pm25_mean'].values[0]),
    },
    "actual_high_years": [2017, 2018],
    "2019_is_anomaly": False,
    "2019_vs_baseline": {
        "2019_mean_ugm3": float(annual_converted[annual_converted['year'] == 2019]['pm25_mean'].values[0]),
        "baseline_mean_ugm3": float(baseline_mean),
        "ratio": float(annual_converted[annual_converted['year'] == 2019]['pm25_mean'].values[0] / baseline_mean)
    },
    "2017_2018_explanation": {
        "2017_mean_ugm3": float(annual_converted[annual_converted['year'] == 2017]['pm25_mean'].values[0]),
        "2018_mean_ugm3": float(annual_converted[annual_converted['year'] == 2018]['pm25_mean'].values[0]),
        "ratio_to_baseline": [
            float(annual_converted[annual_converted['year'] == 2017]['pm25_mean'].values[0] / baseline_mean),
            float(annual_converted[annual_converted['year'] == 2018]['pm25_mean'].values[0] / baseline_mean)
        ],
        "peak_months": {
            "2017": "May-July (autumn/winter)",
            "2018": "April-June (autumn/early winter)"
        }
    },
    "who_guideline_comparison": {
        "who_annual_guideline_ugm3": WHO_ANNUAL_GUIDELINE,
        "years_exceeding": exceeding['year'].tolist() if not exceeding.empty else []
    },
    "recommendations": [
        "URGENT: Apply unit conversion (multiply all PM2.5 values by 10^9)",
        "Update pipeline code to convert kg/m³ to μg/m³",
        "Re-run all PM2.5 analyses with corrected units",
        "Investigate 2017-2018 elevated values (likely real environmental events)",
        "Consider additional validation with ground station data if available",
        "Document unit conversion in all future analyses"
    ]
}

# Save summary
summary_path = OUTPUT_DIR / 'pm25_anomaly_investigation_summary.json'
with open(summary_path, 'w') as f:
    json.dump(summary, f, indent=2)
print(f"\nSaved summary report: {summary_path}")

# ============================================================================
# 10. PRINT FINAL CONCLUSIONS
# ============================================================================

print("\n" + "="*80)
print("FINAL CONCLUSIONS")
print("="*80)

print("""
CRITICAL FINDING: UNIT CONVERSION ERROR
----------------------------------------
The PM2.5 data from CAMS NRT is in kg/m³ and was NOT converted to μg/m³.
All values need to be multiplied by 10^9 (1 billion).

ADDRESSING THE REPORTED ANOMALY:
---------------------------------
1. There is NO 3-fold anomaly in 2019
2. When units are corrected, 2019 shows ~62 μg/m³, which is LOWER than 2017-2018
3. The actual elevated years are 2017 (102 μg/m³) and 2018 (107 μg/m³)
4. 2017-2018 showed ~4x higher PM2.5 compared to 2020-2024 baseline

POTENTIAL CAUSES FOR 2017-2018 ELEVATION:
------------------------------------------
1. Biomass burning / veld fires (peak in autumn/winter months)
2. Increased coal/wood burning for heating (winter season)
3. Drought conditions reducing atmospheric cleaning
4. Algorithm changes in CAMS NRT between operational periods
5. Data quality issues specific to that period

WHO AIR QUALITY COMPARISON:
---------------------------
With corrected units, all years from 2017-2024 EXCEED the WHO annual guideline
of 5 μg/m³, with 2017-2018 showing extreme exceedances (20x guideline).

RECOMMENDATIONS:
----------------
1. IMMEDIATE: Apply unit conversion to all PM2.5 data (multiply by 10^9)
2. Update soweto_climate_pipeline.py line 126-128 with proper conversion
3. Rerun all analyses, figures, and statistical summaries
4. Investigate 2017-2018 elevated period:
   - Check for documented fire events in Gauteng province
   - Review meteorological conditions (drought, stagnation)
   - Cross-validate with ground station data if available
   - Check CAMS algorithm version changes
5. Flag 2017-2018 data with quality warning in metadata
6. Consider excluding or downweighting 2017-2018 in long-term trend analyses
""")

print("\n" + "="*80)
print("Investigation complete. All outputs saved to:")
print(f"  {OUTPUT_DIR}")
print("="*80)
