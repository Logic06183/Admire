"""
Pipeline Fix for PM2.5 Unit Conversion Error
============================================

This file contains the corrected code segments to fix the unit conversion
error in soweto_climate_pipeline.py

PROBLEM: CAMS NRT PM2.5 data is in kg/m³ but was not converted to μg/m³
SOLUTION: Apply conversion factor of 10^9

Date: 2026-02-11
"""

# ============================================================================
# FIX 1: Replace lines 126-128 in soweto_climate_pipeline.py
# ============================================================================

# BEFORE (WRONG):
# ----------------
# def micrograms_to_micrograms(pm25: float) -> float:
#     """Pass-through for PM2.5 (already in µg/m³)."""
#     return pm25

# AFTER (CORRECT):
# ----------------
def kg_to_micrograms_per_m3(pm25_kg: float) -> float:
    """
    Convert PM2.5 from kg/m³ to μg/m³.

    CAMS NRT (Copernicus Atmosphere Monitoring Service) provides PM2.5
    concentrations in kg/m³ (kilograms per cubic meter), but standard
    air quality research and WHO guidelines use μg/m³ (micrograms per
    cubic meter).

    Conversion factor: 1 kg/m³ = 10^9 μg/m³

    Args:
        pm25_kg: PM2.5 concentration in kg/m³ from CAMS NRT

    Returns:
        PM2.5 concentration in μg/m³

    Example:
        >>> kg_to_micrograms_per_m3(1.0e-7)  # 0.0000001 kg/m³
        100.0  # 100 μg/m³
    """
    return pm25_kg * 1e9


# ============================================================================
# FIX 2: Update extract_pm25_batch method (around line 288)
# ============================================================================

# Insert this line AFTER line 287 (after date conversion, before logging)
# This ensures PM2.5 values are converted to μg/m³

# LOCATION in extract_pm25_batch method:
# Line 286: data = pd.DataFrame(data_records)
# Line 287: data['date'] = pd.to_datetime(data['date'])
# INSERT HERE: data['pm25'] = data['pm25'].apply(kg_to_micrograms_per_m3)
# Line 289: self.logger.info(f"Extracted {len(data)} PM2.5 records")

# Full corrected segment (lines 284-292):
def extract_pm25_batch_corrected_segment():
    """
    This shows the corrected segment of the extract_pm25_batch method.
    Replace lines 284-292 in the original file.
    """
    # ... (earlier code remains the same)

    # Convert to pandas DataFrame
    data_records = [feat['properties'] for feat in feature_list]
    data = pd.DataFrame(data_records)

    # Convert date
    data['date'] = pd.to_datetime(data['date'])

    # *** CRITICAL FIX: Convert PM2.5 from kg/m³ to μg/m³ ***
    data['pm25'] = data['pm25'].apply(kg_to_micrograms_per_m3)

    self.logger.info(f"Extracted {len(data)} PM2.5 records")

    return data[['date', 'pm25']]


# ============================================================================
# FIX 3: Update configuration comments (optional but recommended)
# ============================================================================

# Add to PM25_COLLECTION documentation (around line 53-55):
#
# PM25_COLLECTION = 'ECMWF/CAMS/NRT'
# PM25_BAND = 'particulate_matter_d_less_than_25_um_surface'
# PM25_SCALE = 40000  # CAMS native resolution (meters)
#
# # IMPORTANT: CAMS NRT PM2.5 data is in kg/m³ and must be converted
# # to μg/m³ using the conversion factor 10^9
# PM25_UNITS_INPUT = 'kg/m³'  # CAMS NRT native units
# PM25_UNITS_OUTPUT = 'μg/m³'  # Standard air quality units


# ============================================================================
# FIX 4: Add unit documentation to save_results method (around line 656)
# ============================================================================

# Update the CSV header comments when saving PM2.5 data:
def save_pm25_with_units_documentation(df, output_path, logger):
    """
    Save PM2.5 data with proper unit documentation in header.

    This ensures anyone reading the CSV knows the units are correct.
    """
    import pandas as pd

    # Add metadata header
    header_lines = [
        "# Soweto PM2.5 Data - ECMWF CAMS NRT",
        "# Units: μg/m³ (micrograms per cubic meter)",
        "# Source: CAMS NRT particulate_matter_d_less_than_25_um_surface",
        "# Original units (kg/m³) converted to μg/m³ using factor 10^9",
        f"# Extraction date: {pd.Timestamp.now().isoformat()}",
        "# Spatial averaging: 5km buffer around Soweto center",
        "#"
    ]

    with open(output_path, 'w') as f:
        f.write('\n'.join(header_lines) + '\n')
        df.to_csv(f, index=False)

    logger.info(f"Saved PM2.5 data with unit documentation: {output_path}")


# ============================================================================
# VERIFICATION: Test the conversion
# ============================================================================

def test_unit_conversion():
    """
    Test that unit conversion is working correctly.
    Run this after applying fixes to verify correct behavior.
    """
    import numpy as np

    print("Testing PM2.5 unit conversion...")
    print("="*60)

    # Test cases from actual Soweto data
    test_cases = [
        (1.48e-8, 14.77, "2016 annual mean"),
        (1.02e-7, 102.28, "2017 annual mean (high)"),
        (1.07e-7, 106.66, "2018 annual mean (peak)"),
        (6.21e-8, 62.12, "2019 annual mean"),
        (2.49e-8, 24.94, "2020 annual mean"),
        (1.0e-9, 1.0, "1 nanogram/m³"),
        (5.0e-9, 5.0, "WHO guideline level"),
    ]

    all_passed = True

    for kg_value, expected_ug, description in test_cases:
        result = kg_to_micrograms_per_m3(kg_value)
        passed = np.isclose(result, expected_ug, rtol=0.01)
        status = "✓ PASS" if passed else "✗ FAIL"

        print(f"{status} | {description}")
        print(f"  Input:    {kg_value:.2e} kg/m³")
        print(f"  Expected: {expected_ug:.2f} μg/m³")
        print(f"  Got:      {result:.2f} μg/m³")
        print()

        if not passed:
            all_passed = False

    if all_passed:
        print("="*60)
        print("✓ All tests passed! Unit conversion is correct.")
        print("="*60)
    else:
        print("="*60)
        print("✗ Some tests failed! Check implementation.")
        print("="*60)

    return all_passed


# ============================================================================
# QUICK CORRECTION SCRIPT (for existing CSV files)
# ============================================================================

def correct_existing_csv_files(data_dir):
    """
    Quick fix to correct units in existing CSV files.

    WARNING: This modifies files in place. Make backups first!

    Args:
        data_dir: Path to climate_data_output directory
    """
    from pathlib import Path
    import pandas as pd
    import shutil

    data_dir = Path(data_dir)

    # Files that need correction (all PM2.5 files)
    pm25_files = [
        'soweto_pm25_raw.csv',
        'soweto_pm25_annual_stats.csv',
        'soweto_pm25_monthly_stats.csv',
        'soweto_pm25_seasonal_stats.csv'
    ]

    print("Correcting PM2.5 units in existing CSV files...")
    print("="*60)

    for filename in pm25_files:
        filepath = data_dir / filename

        if not filepath.exists():
            print(f"⚠ Skipping {filename} (not found)")
            continue

        # Create backup
        backup_path = filepath.with_suffix('.csv.backup')
        shutil.copy2(filepath, backup_path)
        print(f"✓ Created backup: {backup_path.name}")

        # Read CSV
        df = pd.read_csv(filepath)

        # Identify PM2.5 columns (exclude year, month, count, etc.)
        pm25_cols = [col for col in df.columns
                     if 'pm25' in col.lower()
                     and col not in ['year', 'month', 'season', 'season_year', 'pm25_count']]

        # Apply conversion
        for col in pm25_cols:
            df[col] = df[col] * 1e9

        # Save corrected file
        df.to_csv(filepath, index=False)
        print(f"✓ Corrected: {filename} ({len(pm25_cols)} columns)")

    print("="*60)
    print("✓ Correction complete!")
    print("  Original files backed up with .backup extension")


# ============================================================================
# USAGE INSTRUCTIONS
# ============================================================================

if __name__ == "__main__":
    print(__doc__)
    print("\nUSAGE INSTRUCTIONS")
    print("="*60)
    print()
    print("OPTION 1: Fix pipeline and re-run (RECOMMENDED)")
    print("-" * 60)
    print("1. Edit soweto_climate_pipeline.py:")
    print("   - Replace lines 126-128 with kg_to_micrograms_per_m3 function")
    print("   - Add unit conversion in extract_pm25_batch (after line 287)")
    print()
    print("2. Re-run the pipeline:")
    print("   python soweto_climate_pipeline.py")
    print()
    print("3. Verify results with test:")
    print("   python PIPELINE_FIX.py --test")
    print()
    print()
    print("OPTION 2: Quick fix existing files (TEMPORARY)")
    print("-" * 60)
    print("1. Run this script with --fix flag:")
    print("   python PIPELINE_FIX.py --fix")
    print()
    print("2. This will multiply all PM2.5 values by 10^9 in existing CSVs")
    print("   (Creates backups with .backup extension)")
    print()
    print("3. Note: Still need to fix pipeline for future runs!")
    print()
    print("="*60)
    print()

    # Command line interface
    import sys

    if '--test' in sys.argv:
        print("\nRunning unit conversion tests...\n")
        test_unit_conversion()

    elif '--fix' in sys.argv:
        data_dir = '/Users/craig/Library/Mobile Documents/com~apple~CloudDocs/Admire/climate_data_output'
        print(f"\nApplying quick fix to files in:\n{data_dir}\n")

        response = input("This will modify CSV files. Backups will be created. Continue? (yes/no): ")
        if response.lower() == 'yes':
            correct_existing_csv_files(data_dir)
        else:
            print("Cancelled.")

    else:
        print("Run with --test to verify conversion or --fix to correct existing files")
