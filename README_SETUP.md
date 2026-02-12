# Soweto Climate Data Extraction Pipeline
## Setup and Execution Guide

---

## Overview

This pipeline extracts real observational and reanalysis climate data for Soweto, South Africa (2014-2024) using Google Earth Engine (GEE) and GEEMAP.

**Data Sources:**
- **Temperature**: ERA5-Land hourly reanalysis (2m air temperature)
  - Resolution: ~11km
  - Temporal: Hourly observations
  - Source: ECMWF ERA5-Land reanalysis (assimilates observations)

- **PM2.5**: Copernicus Atmosphere Monitoring Service (CAMS) Near Real-Time
  - Resolution: ~40km
  - Temporal: 3-hourly observations
  - Source: ECMWF CAMS global atmospheric composition reanalysis

**Location**: Soweto, South Africa (-26.2678°, 27.8585°)
- Spatial averaging: 5km buffer around center point
- Covers all Soweto districts

---

## Prerequisites

1. **Python 3.8 or higher**
2. **Google Account** (for GEE authentication)
3. **Google Earth Engine Access**
   - Sign up at: https://earthengine.google.com/signup/
   - Approval usually takes 1-2 business days

---

## Installation

### Step 1: Clone or Download the Pipeline

Ensure you have the following files in your working directory:
```
/Users/craig/Library/Mobile Documents/com~apple~CloudDocs/Admire/
├── soweto_climate_pipeline.py
├── requirements.txt
└── README_SETUP.md
```

### Step 2: Create Virtual Environment (Recommended)

```bash
# Navigate to project directory
cd "/Users/craig/Library/Mobile Documents/com~apple~CloudDocs/Admire"

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
# venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

This will install:
- `earthengine-api`: Google Earth Engine Python API
- `geemap`: Geospatial analysis library for GEE
- `pandas`: Data manipulation
- `numpy`: Numerical computing

---

## Google Earth Engine Authentication

### First-Time Setup

The pipeline will prompt you to authenticate with GEE on first run. Follow these steps:

1. **Run the authentication command** (or the pipeline will do this automatically):
   ```bash
   earthengine authenticate
   ```

2. **Browser window will open**:
   - Sign in with your Google Account
   - Grant permissions to Earth Engine
   - Copy the authorization code

3. **Paste the code** in the terminal when prompted

4. **Credentials saved**: Future runs won't require re-authentication

### Alternative: Service Account (for production/automated runs)

For production environments, use a GEE service account:

1. Create a service account in Google Cloud Console
2. Download the JSON key file
3. Set environment variable:
   ```bash
   export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service-account-key.json"
   ```

---

## Pipeline Execution

### Quick Start

```bash
# Activate virtual environment (if not already active)
source venv/bin/activate

# Run the pipeline
python soweto_climate_pipeline.py
```

### What Happens During Execution

The pipeline will:

1. **Initialize** (30 seconds - 1 minute)
   - Authenticate with GEE
   - Setup logging
   - Initialize data extractors

2. **Extract Data** (10-30 minutes depending on GEE server load)
   - Process data in 6-month batches
   - Extract temperature from ERA5-Land
   - Extract PM2.5 from CAMS
   - Automatic retry on failures
   - Progress logged to console and file

3. **Quality Checks** (< 1 minute)
   - Check data completeness
   - Identify missing values
   - Detect outliers
   - Generate quality report

4. **Compute Aggregations** (< 2 minutes)
   - Monthly statistics (mean, median, IQR)
   - Seasonal statistics (DJF, MAM, JJA, SON)
   - Annual statistics

5. **Save Results** (< 1 minute)
   - Export CSV files
   - Save quality report (JSON)
   - Log summary

### Expected Outputs

All outputs saved to:
```
/Users/craig/Library/Mobile Documents/com~apple~CloudDocs/Admire/climate_data_output/
```

**Raw Data Files:**
- `soweto_temperature_raw.csv`: Hourly temperature data (°C)
- `soweto_pm25_raw.csv`: 3-hourly PM2.5 data (µg/m³)

**Aggregated Statistics:**
- `soweto_temp_monthly_stats.csv`: Monthly temperature statistics
- `soweto_temp_seasonal_stats.csv`: Seasonal temperature statistics
- `soweto_temp_annual_stats.csv`: Annual temperature statistics
- `soweto_pm25_monthly_stats.csv`: Monthly PM2.5 statistics
- `soweto_pm25_seasonal_stats.csv`: Seasonal PM2.5 statistics
- `soweto_pm25_annual_stats.csv`: Annual PM2.5 statistics

**Quality & Metadata:**
- `quality_report.json`: Data quality metrics and pipeline metadata
- `soweto_climate_extraction.log`: Detailed execution log

---

## Understanding the Outputs

### Raw Data Format

**Temperature CSV:**
```csv
date,temperature_c
2014-01-01 00:00:00,22.5
2014-01-01 01:00:00,21.8
...
```

**PM2.5 CSV:**
```csv
date,pm25
2014-01-01 00:00:00,15.3
2014-01-01 03:00:00,14.9
...
```

### Aggregated Statistics Format

Each aggregation file contains:
- `*_mean`: Mean value
- `*_median`: Median value
- `*_q25`: 25th percentile
- `*_q75`: 75th percentile
- `*_iqr`: Interquartile range (Q75 - Q25)
- `*_count`: Number of observations

**Example - Monthly Statistics:**
```csv
year,month,temperature_c_mean,temperature_c_median,temperature_c_q25,temperature_c_q75,temperature_c_iqr,temperature_c_count
2014,1,23.5,23.2,21.5,25.3,3.8,744
```

**Example - Seasonal Statistics:**
```csv
season_year,season,temperature_c_mean,temperature_c_median,...
2014,Summer,24.5,24.2,...
2014,Autumn,18.3,18.1,...
```

### Quality Report (JSON)

Contains:
- Data completeness metrics
- Missing value counts
- Outlier detection results
- Date range coverage
- Pipeline execution metadata
- Data source information

---

## Troubleshooting

### Common Issues

#### 1. Authentication Fails
```
Error: Failed to authenticate with GEE
```
**Solution:**
- Ensure you have GEE access approved
- Run `earthengine authenticate` manually
- Check internet connection

#### 2. Memory Errors
```
Error: User memory limit exceeded
```
**Solution:**
- Pipeline already uses batching to avoid this
- If it occurs, reduce `BATCH_SIZE_MONTHS` in config (line 52)
- Default is 6 months; try 3 months

#### 3. Rate Limiting
```
Error: Too many requests
```
**Solution:**
- Pipeline includes automatic retry with exponential backoff
- Increase `RETRY_DELAY` in config if needed
- Wait a few minutes and re-run

#### 4. No PM2.5 Data for Early Years
```
Warning: No PM2.5 data returned for [date range]
```
**Solution:**
- CAMS NRT data availability varies
- Check GEE data catalog for exact date ranges
- Consider alternative PM2.5 products for earlier periods

#### 5. Slow Execution
```
Pipeline taking > 1 hour
```
**Solution:**
- Normal for large date ranges (11 years)
- GEE server load varies by time of day
- Consider running during off-peak hours (US/Europe night time)
- Check logs for specific slow batches

---

## Configuration Customization

To modify pipeline behavior, edit the `PipelineConfig` class in `soweto_climate_pipeline.py`:

### Change Date Range
```python
START_DATE = '2018-01-01'  # Change start year
END_DATE = '2023-12-31'    # Change end year
```

### Change Location
```python
SOWETO_LAT = -26.2678     # Your latitude
SOWETO_LON = 27.8585      # Your longitude
BUFFER_DISTANCE = 10000   # 10km buffer instead of 5km
```

### Change Batch Size
```python
BATCH_SIZE_MONTHS = 3     # Smaller batches for memory constraints
```

### Change Output Directory
```python
OUTPUT_DIR = Path('/your/custom/path')
```

---

## Data Source Details

### ERA5-Land Temperature

**About:**
- Global reanalysis produced by ECMWF
- Assimilates observations from weather stations, satellites, etc.
- 2m air temperature (standard meteorological height)
- Validated against ground observations globally

**Technical Details:**
- Collection: `ECMWF/ERA5_LAND/HOURLY`
- Band: `temperature_2m`
- Native resolution: 0.1° (~11km)
- Temporal resolution: Hourly
- Unit: Kelvin (converted to Celsius in pipeline)

**Citation:**
Muñoz Sabater, J., (2019): ERA5-Land hourly data from 1950 to present. Copernicus Climate Change Service (C3S) Climate Data Store (CDS).

### CAMS PM2.5

**About:**
- Global atmospheric composition reanalysis
- Combines model simulations with satellite observations
- Surface particulate matter < 2.5µm
- Validated against ground monitoring networks

**Technical Details:**
- Collection: `ECMWF/CAMS/NRT`
- Band: `particulate_matter_d_less_than_25_um_surface`
- Native resolution: 0.4° (~40km)
- Temporal resolution: 3-hourly
- Unit: µg/m³

**Citation:**
Copernicus Atmosphere Monitoring Service (2023). CAMS global reanalysis (EAC4). ECMWF.

**Data Availability Note:**
- CAMS NRT: 2016-present (full coverage)
- 2014-2015: May have limited coverage
- Check quality report for actual data availability

---

## Pipeline Architecture

### Design Principles

1. **Batch Processing**: Data extracted in 6-month chunks to respect GEE memory limits
2. **Retry Logic**: Automatic retry with exponential backoff for transient failures
3. **Spatial Aggregation**: 5km buffer averaging reduces noise and represents district-level conditions
4. **Quality Assurance**: Automated checks for completeness, outliers, and coverage
5. **Reproducibility**: All parameters logged; fixed random seeds not needed (deterministic data)
6. **Scalability**: Easy to extend to multiple locations or additional variables

### Component Overview

```
ClimatePipeline (Main Orchestrator)
├── GEEAuthenticator: Handle authentication
├── ClimateDataExtractor: GEE data extraction
├── BatchProcessor: Manage date range batching
├── StatisticalAggregator: Compute temporal statistics
└── DataQualityChecker: Validate outputs
```

### Error Handling

- **Network failures**: Automatic retry (3 attempts)
- **GEE quota limits**: Exponential backoff
- **Missing data**: Logged and reported in quality report
- **Invalid data**: Outlier detection and flagging

---

## Performance Optimization

The pipeline is optimized for:

1. **Server-side processing**: All computations done on GEE servers
2. **Minimal data transfer**: Only final aggregated values downloaded
3. **Efficient reducers**: Uses `ee.Reducer.mean()` for spatial averaging
4. **Lazy evaluation**: GEE's lazy execution model maximized
5. **Appropriate scales**: Uses native resolution of each dataset

### Expected Performance

- **Small date range** (1 year): ~5-10 minutes
- **Full range** (11 years): ~15-30 minutes
- **Depends on**: GEE server load, network speed, time of day

---

## Advanced Usage

### Running Specific Components

You can import and use individual components:

```python
from soweto_climate_pipeline import (
    PipelineConfig,
    ClimateDataExtractor,
    StatisticalAggregator
)

# Custom configuration
config = PipelineConfig()
config.START_DATE = '2020-01-01'
config.END_DATE = '2020-12-31'

# Initialize extractor
extractor = ClimateDataExtractor(config, logger)

# Extract specific variable
temp_data = extractor.extract_temperature_batch('2020-01-01', '2020-12-31')
```

### Extending to Multiple Locations

```python
locations = [
    {'name': 'Soweto', 'lat': -26.2678, 'lon': 27.8585},
    {'name': 'Johannesburg', 'lat': -26.2041, 'lon': 28.0473},
    # ... more locations
]

for loc in locations:
    config.SOWETO_LAT = loc['lat']
    config.SOWETO_LON = loc['lon']
    # Run pipeline for each location
```

### Adding Additional Variables

To add new climate variables:

1. Find GEE collection in Earth Engine Data Catalog
2. Add collection ID and band name to config
3. Create extraction method in `ClimateDataExtractor`
4. Add batch processing call in `extract_all_data()`

---

## Support and Resources

### Google Earth Engine Resources

- **Data Catalog**: https://developers.google.com/earth-engine/datasets
- **Documentation**: https://developers.google.com/earth-engine
- **Code Editor**: https://code.earthengine.google.com/
- **Community Forum**: https://groups.google.com/g/google-earth-engine-developers

### GEEMAP Resources

- **Documentation**: https://geemap.org/
- **GitHub**: https://github.com/gee-community/geemap
- **Tutorials**: https://geemap.org/tutorials/

### Data Source Information

- **ERA5-Land**: https://cds.climate.copernicus.eu/cdsapp#!/dataset/reanalysis-era5-land
- **CAMS**: https://atmosphere.copernicus.eu/

---

## Citation

If you use this pipeline in research, please cite:

**Pipeline:**
```
Soweto Climate Data Extraction Pipeline (2026).
Google Earth Engine and GEEMAP-based climate data processing system.
```

**Data Sources:**
- See "Data Source Details" section above for proper data citations

---

## License

This pipeline is provided as-is for research and analysis purposes.

**Data Licensing:**
- ERA5-Land: Copernicus License (free and open)
- CAMS: Copernicus License (free and open)

---

## Contact and Issues

For issues with:
- **Pipeline code**: Check logs in `climate_data_output/soweto_climate_extraction.log`
- **GEE authentication**: Refer to GEE documentation
- **Data availability**: Check GEE data catalog for product-specific information

---

## Version History

**v1.0.0** (2026-02-09)
- Initial release
- ERA5-Land temperature extraction
- CAMS PM2.5 extraction
- Monthly, seasonal, annual aggregations
- Quality assurance checks
- Batch processing implementation

---

## Acknowledgments

Data provided by:
- European Centre for Medium-Range Weather Forecasts (ECMWF)
- Copernicus Climate Change Service (C3S)
- Copernicus Atmosphere Monitoring Service (CAMS)
- Google Earth Engine platform
