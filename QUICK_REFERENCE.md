# Quick Reference Guide
## Soweto Climate Data Extraction Pipeline

---

## One-Page Cheat Sheet

### Installation (First Time)
```bash
cd "/Users/craig/Library/Mobile Documents/com~apple~CloudDocs/Admire"
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
earthengine authenticate
```

### Run Pipeline
```bash
source venv/bin/activate
python soweto_climate_pipeline.py
# OR use the convenience script:
./run_pipeline.sh
```

### Validate Results
```bash
python validate_extraction.py
```

### View Results
```bash
# Check log
cat climate_data_output/soweto_climate_extraction.log

# View quality report
cat climate_data_output/quality_report.json | python -m json.tool

# List all outputs
ls -lh climate_data_output/
```

---

## Output Files

| File | Description | Format |
|------|-------------|--------|
| `soweto_temperature_raw.csv` | Hourly temperature data | date, temperature_c |
| `soweto_pm25_raw.csv` | 3-hourly PM2.5 data | date, pm25 |
| `soweto_temp_monthly_stats.csv` | Monthly temp statistics | year, month, mean, median, IQR |
| `soweto_temp_seasonal_stats.csv` | Seasonal temp statistics | season_year, season, stats |
| `soweto_temp_annual_stats.csv` | Annual temp statistics | year, stats |
| `soweto_pm25_monthly_stats.csv` | Monthly PM2.5 statistics | year, month, mean, median, IQR |
| `soweto_pm25_seasonal_stats.csv` | Seasonal PM2.5 statistics | season_year, season, stats |
| `soweto_pm25_annual_stats.csv` | Annual PM2.5 statistics | year, stats |
| `quality_report.json` | Data quality metrics | JSON format |
| `soweto_climate_extraction.log` | Execution log | Text log |

---

## Data Sources

### Temperature: ERA5-Land
- **Collection**: `ECMWF/ERA5_LAND/HOURLY`
- **Band**: `temperature_2m`
- **Resolution**: 11km, hourly
- **Unit**: Celsius (converted from Kelvin)
- **Type**: Reanalysis (observation-assimilated)

### PM2.5: CAMS NRT
- **Collection**: `ECMWF/CAMS/NRT`
- **Band**: `particulate_matter_d_less_than_25_um_surface`
- **Resolution**: 40km, 3-hourly
- **Unit**: µg/m³
- **Type**: Atmospheric reanalysis

---

## Configuration Parameters

Edit `soweto_climate_pipeline.py` class `PipelineConfig`:

```python
# Location
SOWETO_LAT = -26.2678          # Latitude
SOWETO_LON = 27.8585           # Longitude
BUFFER_DISTANCE = 5000         # Meters (5km radius)

# Date range
START_DATE = '2014-01-01'
END_DATE = '2024-12-31'

# Processing
BATCH_SIZE_MONTHS = 6          # Reduce if memory issues
MAX_RETRIES = 3                # GEE retry attempts
RETRY_DELAY = 5                # Seconds between retries

# Output
OUTPUT_DIR = Path('...')       # Output directory path
```

---

## Common Commands

### Python Quick Tests
```python
# Test GEE connection
python -c "import ee; ee.Initialize(); print('GEE OK')"

# Check data files exist
python -c "
from pathlib import Path
d = Path('climate_data_output')
print(f'Files: {len(list(d.glob(\"*.csv\")))}')
"

# Quick data preview
python -c "
import pandas as pd
df = pd.read_csv('climate_data_output/soweto_temperature_raw.csv')
print(df.head())
print(f'Records: {len(df):,}')
"
```

### Log Analysis
```bash
# Recent errors
tail -100 climate_data_output/soweto_climate_extraction.log | grep ERROR

# Batch progress
grep "Processing.*batch" climate_data_output/soweto_climate_extraction.log

# Completion status
tail -20 climate_data_output/soweto_climate_extraction.log
```

### Data Inspection
```bash
# Temperature statistics
python -c "
import pandas as pd
df = pd.read_csv('climate_data_output/soweto_temp_annual_stats.csv')
print(df[['year', 'temperature_c_mean', 'temperature_c_median']])
"

# PM2.5 statistics
python -c "
import pandas as pd
df = pd.read_csv('climate_data_output/soweto_pm25_annual_stats.csv')
print(df[['year', 'pm25_mean', 'pm25_median']])
"
```

---

## Pipeline Workflow

```
1. Initialize
   ├── Authenticate with GEE
   ├── Setup logging
   └── Create data extractors

2. Extract Data (15-30 min)
   ├── Process 6-month batches
   ├── Temperature: ERA5-Land
   ├── PM2.5: CAMS
   └── Save raw CSV files

3. Quality Checks (<1 min)
   ├── Check completeness
   ├── Identify missing values
   ├── Detect outliers
   └── Generate quality report

4. Compute Aggregations (1-2 min)
   ├── Monthly statistics
   ├── Seasonal statistics
   └── Annual statistics

5. Save Results (<1 min)
   ├── Export all CSV files
   ├── Save quality report (JSON)
   └── Log execution summary
```

---

## Statistics Computed

For each aggregation period (monthly/seasonal/annual):

- **Mean**: Average value
- **Median**: 50th percentile
- **Q25**: 25th percentile
- **Q75**: 75th percentile
- **IQR**: Interquartile range (Q75 - Q25)
- **Count**: Number of observations

---

## Southern Hemisphere Seasons

| Season | Months | Description |
|--------|--------|-------------|
| Summer | DJF (Dec-Jan-Feb) | Warmest period |
| Autumn | MAM (Mar-Apr-May) | Cooling period |
| Winter | JJA (Jun-Jul-Aug) | Coldest period |
| Spring | SON (Sep-Oct-Nov) | Warming period |

---

## Error Handling

The pipeline includes:

- **Automatic retry**: 3 attempts with exponential backoff
- **Batch processing**: Prevents memory overflow
- **Error logging**: All errors logged to file
- **Graceful degradation**: Continues on non-critical errors

---

## Troubleshooting Quick Fixes

| Problem | Quick Fix |
|---------|-----------|
| "No module named 'ee'" | `pip install earthengine-api` |
| "Authentication failed" | `earthengine authenticate` |
| "Memory limit exceeded" | Reduce `BATCH_SIZE_MONTHS` to 3 |
| "Too many requests" | Wait 5 minutes, then retry |
| Empty CSV files | Check log for errors, verify GEE auth |
| Slow performance | Run during off-peak hours |

---

## Data Quality Guidelines

### Temperature (Soweto)
- **Normal range**: 5°C to 35°C
- **Mean annual**: ~15-17°C
- **Extreme cold**: <0°C (rare)
- **Extreme heat**: >40°C (rare)

### PM2.5
- **WHO guideline**: 15 µg/m³ annual mean
- **Typical urban**: 10-30 µg/m³
- **Poor quality**: >50 µg/m³
- **Extreme**: >100 µg/m³

---

## Integration Examples

### Load Data in Python
```python
import pandas as pd

# Load raw data
temp = pd.read_csv('climate_data_output/soweto_temperature_raw.csv')
temp['date'] = pd.to_datetime(temp['date'])

pm25 = pd.read_csv('climate_data_output/soweto_pm25_raw.csv')
pm25['date'] = pd.to_datetime(pm25['date'])

# Load aggregated data
temp_annual = pd.read_csv('climate_data_output/soweto_temp_annual_stats.csv')
```

### Load Data in R
```r
# Load raw data
temp <- read.csv('climate_data_output/soweto_temperature_raw.csv')
temp$date <- as.POSIXct(temp$date)

pm25 <- read.csv('climate_data_output/soweto_pm25_raw.csv')
pm25$date <- as.POSIXct(pm25$date)

# Load aggregated data
temp_annual <- read.csv('climate_data_output/soweto_temp_annual_stats.csv')
```

### Quick Visualization (Python)
```python
import matplotlib.pyplot as plt

# Annual trends
temp_annual = pd.read_csv('climate_data_output/soweto_temp_annual_stats.csv')

plt.figure(figsize=(12, 5))
plt.plot(temp_annual['year'], temp_annual['temperature_c_mean'], marker='o')
plt.xlabel('Year')
plt.ylabel('Temperature (°C)')
plt.title('Annual Temperature Trend - Soweto')
plt.grid(True)
plt.savefig('temp_trend.png')
```

---

## File Paths Reference

### Input Files
```
/Users/craig/Library/Mobile Documents/com~apple~CloudDocs/Admire/
├── soweto_climate_pipeline.py    # Main pipeline
├── validate_extraction.py        # Validation script
├── requirements.txt               # Dependencies
├── README_SETUP.md               # Setup guide
├── TROUBLESHOOTING.md            # Troubleshooting
└── run_pipeline.sh               # Convenience script
```

### Output Files
```
/Users/craig/Library/Mobile Documents/com~apple~CloudDocs/Admire/climate_data_output/
├── soweto_temperature_raw.csv
├── soweto_pm25_raw.csv
├── soweto_temp_monthly_stats.csv
├── soweto_temp_seasonal_stats.csv
├── soweto_temp_annual_stats.csv
├── soweto_pm25_monthly_stats.csv
├── soweto_pm25_seasonal_stats.csv
├── soweto_pm25_annual_stats.csv
├── quality_report.json
├── validation_report.json
└── soweto_climate_extraction.log
```

---

## Performance Tips

1. **Run during off-peak hours** (US/Europe night time)
2. **Stable internet connection** required
3. **Don't interrupt** mid-batch
4. **Monitor logs** for progress
5. **Reduce batch size** if memory issues occur

---

## Citation Information

### Pipeline
```
Soweto Climate Data Extraction Pipeline (2026).
Google Earth Engine and GEEMAP-based climate data processing system.
```

### Data Sources

**ERA5-Land**:
```
Muñoz Sabater, J., (2019): ERA5-Land hourly data from 1950 to present.
Copernicus Climate Change Service (C3S) Climate Data Store (CDS).
DOI: 10.24381/cds.e2161bac
```

**CAMS**:
```
Copernicus Atmosphere Monitoring Service (2023).
CAMS global reanalysis (EAC4). ECMWF.
```

---

## Support Resources

- **GEE Documentation**: https://developers.google.com/earth-engine
- **GEE Data Catalog**: https://developers.google.com/earth-engine/datasets
- **GEEMAP Docs**: https://geemap.org/
- **GEE Forum**: https://groups.google.com/g/google-earth-engine-developers
- **GEE Status**: https://status.earthengine.google.com/

---

## Version Information

- **Pipeline Version**: 1.0.0
- **Created**: 2026-02-09
- **Python Requirement**: 3.8+
- **GEE API Version**: 0.1.384+
- **GEEMAP Version**: 0.30.0+

---

## Quick Start (Complete Workflow)

```bash
# 1. Setup (first time only)
cd "/Users/craig/Library/Mobile Documents/com~apple~CloudDocs/Admire"
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
earthengine authenticate

# 2. Run extraction
python soweto_climate_pipeline.py

# 3. Validate results
python validate_extraction.py

# 4. Analyze data (optional)
jupyter notebook soweto_climate_analysis.ipynb
```

That's it! Results will be in `climate_data_output/`.

---

**For detailed information, see:**
- `README_SETUP.md` - Complete setup instructions
- `TROUBLESHOOTING.md` - Detailed troubleshooting guide
