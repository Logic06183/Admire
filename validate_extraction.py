"""
Data Validation Script for Soweto Climate Extraction
====================================================

This script performs comprehensive validation of extracted climate data
to ensure quality and completeness.

Run this after the main pipeline to verify data integrity.
"""

import pandas as pd
import numpy as np
from pathlib import Path
import json
import sys
from datetime import datetime

from soweto_climate_pipeline import PipelineConfig

# Configuration
DATA_DIR = PipelineConfig().OUTPUT_DIR
EXPECTED_START = '2014-01-01'
EXPECTED_END = '2024-12-31'

# WHO Air Quality Guidelines
WHO_ANNUAL_PM25 = 15  # µg/m³
WHO_24HR_PM25 = 25    # µg/m³

# Temperature thresholds for Soweto (reasonable ranges)
TEMP_MIN_REASONABLE = -5   # °C (extreme cold)
TEMP_MAX_REASONABLE = 45   # °C (extreme heat)

class DataValidator:
    """Comprehensive data validation."""

    def __init__(self):
        self.issues = []
        self.warnings = []
        self.passed = []

    def log_issue(self, severity: str, message: str):
        """Log validation finding."""
        if severity == 'ERROR':
            self.issues.append(message)
            print(f"[ERROR] {message}")
        elif severity == 'WARNING':
            self.warnings.append(message)
            print(f"[WARNING] {message}")
        else:
            self.passed.append(message)

    def check_file_exists(self, filepath: Path, description: str) -> bool:
        """Check if required file exists."""
        if filepath.exists():
            self.log_issue('PASS', f"{description} exists: {filepath.name}")
            return True
        else:
            self.log_issue('ERROR', f"Missing file: {filepath.name}")
            return False

    def validate_date_range(self, df: pd.DataFrame, var_name: str):
        """Validate date range coverage."""
        actual_start = df['date'].min()
        actual_end = df['date'].max()
        expected_start = pd.to_datetime(EXPECTED_START)
        expected_end = pd.to_datetime(EXPECTED_END)

        if actual_start > expected_start:
            self.log_issue('WARNING',
                f"{var_name}: Data starts late ({actual_start} vs {expected_start})")
        else:
            self.log_issue('PASS', f"{var_name}: Start date coverage OK")

        if actual_end < expected_end:
            self.log_issue('WARNING',
                f"{var_name}: Data ends early ({actual_end} vs {expected_end})")
        else:
            self.log_issue('PASS', f"{var_name}: End date coverage OK")

    def validate_missing_values(self, df: pd.DataFrame, column: str, var_name: str):
        """Check for missing values."""
        missing = df[column].isna().sum()
        total = len(df)
        pct = (missing / total) * 100

        if pct == 0:
            self.log_issue('PASS', f"{var_name}: No missing values")
        elif pct < 5:
            self.log_issue('WARNING', f"{var_name}: {pct:.2f}% missing values ({missing}/{total})")
        else:
            self.log_issue('ERROR', f"{var_name}: {pct:.2f}% missing values ({missing}/{total})")

    def validate_temperature_range(self, df: pd.DataFrame):
        """Validate temperature values are reasonable."""
        temp_min = df['temperature_c'].min()
        temp_max = df['temperature_c'].max()

        if temp_min < TEMP_MIN_REASONABLE:
            self.log_issue('WARNING',
                f"Temperature: Unusually low value ({temp_min:.2f}°C)")
        if temp_max > TEMP_MAX_REASONABLE:
            self.log_issue('WARNING',
                f"Temperature: Unusually high value ({temp_max:.2f}°C)")

        if TEMP_MIN_REASONABLE <= temp_min and temp_max <= TEMP_MAX_REASONABLE:
            self.log_issue('PASS', f"Temperature: Values within reasonable range")

    def validate_pm25_range(self, df: pd.DataFrame):
        """Validate PM2.5 values are reasonable."""
        pm25_min = df['pm25'].min()
        pm25_max = df['pm25'].max()

        if pm25_min < 0:
            self.log_issue('ERROR', f"PM2.5: Negative values found ({pm25_min:.2f})")
        else:
            self.log_issue('PASS', "PM2.5: No negative values")

        if pm25_max > 500:
            self.log_issue('WARNING',
                f"PM2.5: Extremely high value found ({pm25_max:.2f} µg/m³)")
        else:
            self.log_issue('PASS', "PM2.5: Max value within expected range")

    def check_data_gaps(self, df: pd.DataFrame, var_name: str, expected_freq: str):
        """Check for significant gaps in time series."""
        df = df.sort_values('date')
        time_diff = df['date'].diff()

        if expected_freq == 'hourly':
            max_gap = pd.Timedelta(hours=6)  # More than 6 hours
        elif expected_freq == '3-hourly':
            max_gap = pd.Timedelta(hours=12)  # More than 12 hours
        else:
            max_gap = pd.Timedelta(days=3)

        gaps = time_diff[time_diff > max_gap]

        if len(gaps) == 0:
            self.log_issue('PASS', f"{var_name}: No significant time gaps")
        elif len(gaps) < 10:
            self.log_issue('WARNING',
                f"{var_name}: {len(gaps)} time gaps > {max_gap}")
        else:
            self.log_issue('ERROR',
                f"{var_name}: {len(gaps)} significant time gaps detected")

    def validate_statistics_consistency(self, df: pd.DataFrame, var_name: str):
        """Validate statistical aggregations are consistent."""
        issues_found = False

        for _, row in df.iterrows():
            prefix = var_name.split('_')[0]  # 'temperature' or 'pm25'

            q25 = row.get(f'{prefix}_q25')
            median = row.get(f'{prefix}_median')
            q75 = row.get(f'{prefix}_q75')
            mean = row.get(f'{prefix}_mean')
            iqr = row.get(f'{prefix}_iqr')

            # Check quartile ordering
            if pd.notna(q25) and pd.notna(median) and pd.notna(q75):
                if not (q25 <= median <= q75):
                    self.log_issue('ERROR',
                        f"{var_name}: Quartile ordering violation (Q25={q25}, median={median}, Q75={q75})")
                    issues_found = True

            # Check IQR calculation
            if pd.notna(q25) and pd.notna(q75) and pd.notna(iqr):
                expected_iqr = q75 - q25
                if not np.isclose(iqr, expected_iqr, rtol=0.01):
                    self.log_issue('ERROR',
                        f"{var_name}: IQR calculation error (computed={iqr}, expected={expected_iqr})")
                    issues_found = True

        if not issues_found:
            self.log_issue('PASS', f"{var_name}: Statistical consistency OK")

    def compare_with_who_guidelines(self, pm25_annual: pd.DataFrame):
        """Compare PM2.5 levels with WHO guidelines."""
        exceeding_years = (pm25_annual['pm25_mean'] > WHO_ANNUAL_PM25).sum()
        total_years = len(pm25_annual)

        if exceeding_years == 0:
            self.log_issue('PASS',
                f"PM2.5: All years meet WHO annual guideline ({WHO_ANNUAL_PM25} µg/m³)")
        else:
            self.log_issue('WARNING',
                f"PM2.5: {exceeding_years}/{total_years} years exceed WHO annual guideline")

    def run_all_validations(self):
        """Run complete validation suite."""
        print("="*80)
        print("SOWETO CLIMATE DATA VALIDATION")
        print("="*80)
        print(f"Validation date: {datetime.now()}")
        print(f"Data directory: {DATA_DIR}")
        print("="*80)
        print()

        # Check files exist
        print("1. Checking file existence...")
        files_to_check = [
            (DATA_DIR / 'soweto_temperature_raw.csv', 'Temperature raw data'),
            (DATA_DIR / 'soweto_pm25_raw.csv', 'PM2.5 raw data'),
            (DATA_DIR / 'soweto_temp_monthly_stats.csv', 'Temperature monthly stats'),
            (DATA_DIR / 'soweto_temp_seasonal_stats.csv', 'Temperature seasonal stats'),
            (DATA_DIR / 'soweto_temp_annual_stats.csv', 'Temperature annual stats'),
            (DATA_DIR / 'soweto_pm25_monthly_stats.csv', 'PM2.5 monthly stats'),
            (DATA_DIR / 'soweto_pm25_seasonal_stats.csv', 'PM2.5 seasonal stats'),
            (DATA_DIR / 'soweto_pm25_annual_stats.csv', 'PM2.5 annual stats'),
            (DATA_DIR / 'quality_report.json', 'Quality report'),
            (DATA_DIR / 'soweto_climate_extraction.log', 'Pipeline log'),
        ]

        all_files_exist = True
        for filepath, desc in files_to_check:
            if not self.check_file_exists(filepath, desc):
                all_files_exist = False

        if not all_files_exist:
            print("\n[CRITICAL] Missing required files. Cannot continue validation.")
            return self.generate_report()

        print()

        # Load data
        print("2. Loading data files...")
        try:
            temp_raw = pd.read_csv(DATA_DIR / 'soweto_temperature_raw.csv')
            temp_raw['date'] = pd.to_datetime(temp_raw['date'])

            pm25_raw = pd.read_csv(DATA_DIR / 'soweto_pm25_raw.csv')
            pm25_raw['date'] = pd.to_datetime(pm25_raw['date'])

            temp_monthly = pd.read_csv(DATA_DIR / 'soweto_temp_monthly_stats.csv')
            temp_annual = pd.read_csv(DATA_DIR / 'soweto_temp_annual_stats.csv')
            pm25_monthly = pd.read_csv(DATA_DIR / 'soweto_pm25_monthly_stats.csv')
            pm25_annual = pd.read_csv(DATA_DIR / 'soweto_pm25_annual_stats.csv')

            self.log_issue('PASS', "All data files loaded successfully")
            print()
        except Exception as e:
            self.log_issue('ERROR', f"Failed to load data: {e}")
            return self.generate_report()

        # Validate date ranges
        print("3. Validating date ranges...")
        self.validate_date_range(temp_raw, 'Temperature')
        self.validate_date_range(pm25_raw, 'PM2.5')
        print()

        # Validate missing values
        print("4. Checking for missing values...")
        self.validate_missing_values(temp_raw, 'temperature_c', 'Temperature')
        self.validate_missing_values(pm25_raw, 'pm25', 'PM2.5')
        print()

        # Validate value ranges
        print("5. Validating value ranges...")
        self.validate_temperature_range(temp_raw)
        self.validate_pm25_range(pm25_raw)
        print()

        # Check for data gaps
        print("6. Checking for time series gaps...")
        self.check_data_gaps(temp_raw, 'Temperature', 'hourly')
        self.check_data_gaps(pm25_raw, 'PM2.5', '3-hourly')
        print()

        # Validate statistical consistency
        print("7. Validating statistical computations...")
        self.validate_statistics_consistency(temp_monthly, 'temperature_c')
        self.validate_statistics_consistency(pm25_monthly, 'pm25')
        print()

        # WHO guideline comparison
        print("8. Comparing with WHO air quality guidelines...")
        self.compare_with_who_guidelines(pm25_annual)
        print()

        # Data volume checks
        print("9. Checking data volumes...")
        self.log_issue('PASS', f"Temperature records: {len(temp_raw):,}")
        self.log_issue('PASS', f"PM2.5 records: {len(pm25_raw):,}")

        # Expected record counts (approximate)
        years = 11
        expected_temp_min = years * 365 * 24 * 0.7  # 70% coverage
        expected_pm25_min = years * 365 * 8 * 0.5   # 50% coverage (3-hourly)

        if len(temp_raw) < expected_temp_min:
            self.log_issue('WARNING',
                f"Temperature: Record count lower than expected ({len(temp_raw):,} < {expected_temp_min:,.0f})")
        else:
            self.log_issue('PASS', "Temperature: Record count reasonable")

        if len(pm25_raw) < expected_pm25_min:
            self.log_issue('WARNING',
                f"PM2.5: Record count lower than expected ({len(pm25_raw):,} < {expected_pm25_min:,.0f})")
        else:
            self.log_issue('PASS', "PM2.5: Record count reasonable")
        print()

        return self.generate_report()

    def generate_report(self):
        """Generate validation report."""
        print("="*80)
        print("VALIDATION SUMMARY")
        print("="*80)
        print(f"Checks passed: {len(self.passed)}")
        print(f"Warnings: {len(self.warnings)}")
        print(f"Errors: {len(self.issues)}")
        print()

        if len(self.issues) == 0 and len(self.warnings) == 0:
            print("STATUS: ALL VALIDATIONS PASSED")
            status = "PASS"
        elif len(self.issues) == 0:
            print("STATUS: PASSED WITH WARNINGS")
            status = "WARNING"
        else:
            print("STATUS: VALIDATION FAILED")
            status = "FAIL"

        print("="*80)

        # Save report
        report = {
            'validation_date': datetime.now().isoformat(),
            'status': status,
            'summary': {
                'passed': len(self.passed),
                'warnings': len(self.warnings),
                'errors': len(self.issues)
            },
            'details': {
                'passed': self.passed,
                'warnings': self.warnings,
                'errors': self.issues
            }
        }

        report_path = DATA_DIR / 'validation_report.json'
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)

        print(f"\nDetailed report saved to: {report_path}")

        return status == "PASS"

def main():
    """Main entry point."""
    validator = DataValidator()
    success = validator.run_all_validations()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
