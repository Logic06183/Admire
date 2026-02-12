#!/usr/bin/env python3
"""
Quick test script to verify Google Earth Engine connection
"""
import ee

def test_gee_connection():
    """Test GEE authentication and basic access"""
    try:
        # Initialize Earth Engine
        ee.Initialize()
        print("✓ Earth Engine initialized successfully!")

        # Test a simple operation
        point = ee.Geometry.Point([27.8585, -26.2678])  # Soweto coordinates
        print(f"✓ Created test point: {point.getInfo()}")

        # Test accessing a dataset
        dataset = ee.ImageCollection('ECMWF/ERA5_LAND/HOURLY')
        count = dataset.filterDate('2024-01-01', '2024-01-02').size().getInfo()
        print(f"✓ Successfully accessed ERA5-Land dataset: {count} images found")

        print("\n✅ GEE Connection Test PASSED - Ready to run pipeline!")
        return True

    except ee.EEException as e:
        print(f"❌ Earth Engine Error: {e}")
        print("\nTroubleshooting:")
        print("1. Run: earthengine authenticate")
        print("2. Follow the browser authentication flow")
        print("3. Make sure you have Earth Engine access at:")
        print("   https://code.earthengine.google.com/")
        return False
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
        return False

if __name__ == "__main__":
    test_gee_connection()
