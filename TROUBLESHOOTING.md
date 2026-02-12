# Troubleshooting Guide
## Soweto Climate Data Extraction Pipeline

---

## Quick Diagnostics

If you encounter issues, run these commands first:

```bash
# Check Python version (should be 3.8+)
python --version

# Check if GEE is authenticated
python -c "import ee; ee.Initialize(); print('GEE OK')"

# Check installed packages
pip list | grep -E 'earthengine|geemap|pandas'

# Run validation script (after pipeline completes)
python validate_extraction.py
```

---

## Common Issues and Solutions

### 1. Installation Issues

#### Problem: "ModuleNotFoundError: No module named 'ee'"

**Cause**: Google Earth Engine API not installed

**Solution**:
```bash
pip install earthengine-api
```

#### Problem: "ModuleNotFoundError: No module named 'geemap'"

**Cause**: GEEMAP not installed

**Solution**:
```bash
pip install geemap
```

#### Problem: Package conflicts or version mismatches

**Cause**: Incompatible package versions

**Solution**:
```bash
# Create fresh virtual environment
python3 -m venv venv_new
source venv_new/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

---

### 2. Authentication Issues

#### Problem: "Please authorize access to your Earth Engine account"

**Cause**: First-time authentication needed

**Solution**:
```bash
earthengine authenticate
```
Follow the browser prompts, sign in with Google Account, and paste authorization code.

#### Problem: "Invalid credentials" or "Authentication failed"

**Cause**: Expired or corrupted credentials

**Solution**:
```bash
# Remove old credentials
rm -rf ~/.config/earthengine

# Re-authenticate
earthengine authenticate
```

#### Problem: "User doesn't have Earth Engine enabled"

**Cause**: GEE access not approved

**Solution**:
1. Sign up at: https://earthengine.google.com/signup/
2. Wait for approval (usually 1-2 business days)
3. Check email for confirmation
4. Try authentication again

---

### 3. Data Extraction Issues

#### Problem: "User memory limit exceeded"

**Cause**: Trying to process too much data at once

**Solution**:

Edit `soweto_climate_pipeline.py` line 52:
```python
BATCH_SIZE_MONTHS = 3  # Reduce from 6 to 3
```

Or process shorter date ranges:
```python
START_DATE = '2020-01-01'  # Instead of 2014
END_DATE = '2023-12-31'
```

#### Problem: "Computation timed out"

**Cause**: GEE server timeout (usually temporary)

**Solution**:
- The pipeline includes automatic retry logic
- If persistent, try running during off-peak hours (US/Europe night time)
- Reduce `BATCH_SIZE_MONTHS` as shown above

#### Problem: "Too many requests" or "Rate limit exceeded"

**Cause**: GEE rate limiting

**Solution**:

The pipeline has built-in retry logic. If issues persist, increase retry delay:

Edit `soweto_climate_pipeline.py` line 55:
```python
RETRY_DELAY = 10  # Increase from 5 to 10 seconds
```

#### Problem: "No data returned for date range"

**Cause**: Data not available for specific period or location

**Solution**:
1. Check GEE Data Catalog for dataset availability
2. For CAMS PM2.5, data may be limited before 2016
3. Verify location coordinates are correct
4. Check the log file for specific error messages

#### Problem: "Image.reduceRegion: Invalid region"

**Cause**: Geometry or scale issue

**Solution**:

Check the buffer distance and scale settings:
```python
# In PipelineConfig class
BUFFER_DISTANCE = 5000  # Try smaller buffer if needed
TEMPERATURE_SCALE = 11132  # Don't change native resolution
PM25_SCALE = 40000  # Don't change native resolution
```

---

### 4. Output Issues

#### Problem: Empty CSV files

**Cause**: No data extracted or extraction failed

**Solution**:
1. Check log file: `climate_data_output/soweto_climate_extraction.log`
2. Look for error messages in console output
3. Verify GEE authentication is working
4. Check date range and location are valid
5. Run validation script to diagnose:
   ```bash
   python validate_extraction.py
   ```

#### Problem: Missing some aggregation files

**Cause**: Partial pipeline failure

**Solution**:
1. Check which stage failed in the log file
2. If raw data exists but aggregations missing, you can recompute:
   ```python
   # Use individual components
   from soweto_climate_pipeline import StatisticalAggregator, PipelineConfig
   import pandas as pd
   import logging

   config = PipelineConfig()
   logger = logging.getLogger()
   aggregator = StatisticalAggregator(config, logger)

   # Load raw data
   temp_data = pd.read_csv('climate_data_output/soweto_temperature_raw.csv')
   temp_data['date'] = pd.to_datetime(temp_data['date'])

   # Compute aggregations
   monthly = aggregator.aggregate_monthly(temp_data, 'temperature_c')
   monthly.to_csv('climate_data_output/soweto_temp_monthly_stats.csv', index=False)
   ```

#### Problem: "Permission denied" when saving files

**Cause**: No write permissions in output directory

**Solution**:
```bash
# Create output directory with proper permissions
mkdir -p "/Users/craig/Library/Mobile Documents/com~apple~CloudDocs/Admire/climate_data_output"
chmod 755 "/Users/craig/Library/Mobile Documents/com~apple~CloudDocs/Admire/climate_data_output"
```

Or change output directory to a different location:
```python
# In PipelineConfig class
OUTPUT_DIR = Path('/tmp/climate_data_output')  # Use temp directory
```

---

### 5. Performance Issues

#### Problem: Pipeline running very slowly (>1 hour)

**Cause**: Various factors

**Solution**:

1. **Check GEE server status**: https://status.earthengine.google.com/

2. **Run during off-peak hours**: GEE is heavily used during US/Europe business hours

3. **Check internet connection**: Slow connection affects performance

4. **Reduce batch size** (see "User memory limit exceeded" above)

5. **Process shorter time periods**:
   ```python
   # Process year by year if needed
   START_DATE = '2014-01-01'
   END_DATE = '2014-12-31'
   ```

6. **Check system resources**:
   ```bash
   # Monitor Python process
   top | grep python
   ```

#### Problem: Pipeline consumes too much local memory

**Cause**: Large datasets being loaded into memory

**Solution**:

The pipeline is designed to minimize local memory use, but if issues occur:

1. Process data in smaller chunks
2. Don't load raw data unnecessarily
3. Use data generators instead of loading full datasets

---

### 6. Data Quality Issues

#### Problem: Unexpected values (outliers)

**Cause**: Could be real extreme events or data quality issues

**Solution**:

Run the validation script:
```bash
python validate_extraction.py
```

Check the quality report:
```bash
cat climate_data_output/quality_report.json | python -m json.tool
```

For outlier analysis:
```python
import pandas as pd
temp_data = pd.read_csv('climate_data_output/soweto_temperature_raw.csv')

# Find outliers
q1 = temp_data['temperature_c'].quantile(0.25)
q3 = temp_data['temperature_c'].quantile(0.75)
iqr = q3 - q1
outliers = temp_data[
    (temp_data['temperature_c'] < q1 - 3*iqr) |
    (temp_data['temperature_c'] > q3 + 3*iqr)
]
print(outliers)
```

#### Problem: Missing data for certain periods

**Cause**: Gaps in source datasets or GEE availability

**Solution**:

1. Check data availability in GEE Data Catalog
2. Review quality report for specific gaps
3. Consider using alternative data sources for gap-filling
4. Document gaps in your analysis

#### Problem: PM2.5 data missing for 2014-2015

**Cause**: CAMS NRT dataset may have limited early coverage

**Solution**:

For historical PM2.5, consider alternative datasets:
- CAMS global reanalysis (EAC4) - longer historical record
- Satellite-derived PM2.5 products (e.g., from NASA)
- Ground station data if available

To change PM2.5 source, edit the pipeline:
```python
# In PipelineConfig class
PM25_COLLECTION = 'alternative/collection/id'
PM25_BAND = 'alternative_band_name'
```

---

### 7. Log File Analysis

#### Where to find logs

Main log file:
```
climate_data_output/soweto_climate_extraction.log
```

#### What to look for

**Errors**:
```bash
grep ERROR climate_data_output/soweto_climate_extraction.log
```

**Warnings**:
```bash
grep WARNING climate_data_output/soweto_climate_extraction.log
```

**Batch progress**:
```bash
grep "Processing.*batch" climate_data_output/soweto_climate_extraction.log
```

**Completion status**:
```bash
tail -20 climate_data_output/soweto_climate_extraction.log
```

#### Common log patterns and meanings

**"GEE authentication successful"**: Authentication OK

**"Extracted N records"**: Data extraction succeeded for batch

**"No data returned for [date range]"**: No data available for period

**"Retrying in Xs..."**: Temporary error, automatic retry in progress

**"Failed to process batch"**: Batch failed after all retries

---

### 8. Jupyter Notebook Issues

#### Problem: Notebook kernel crashes

**Cause**: Memory issues or package conflicts

**Solution**:
```bash
# Install notebook dependencies
pip install jupyter ipykernel matplotlib seaborn

# Register kernel
python -m ipykernel install --user --name=climate_venv

# Start Jupyter
jupyter notebook soweto_climate_analysis.ipynb
```

#### Problem: "No module named 'matplotlib'"

**Cause**: Visualization packages not installed

**Solution**:
```bash
pip install matplotlib seaborn
```

#### Problem: Plots not displaying

**Cause**: Backend or inline magic missing

**Solution**:

Add to first notebook cell:
```python
%matplotlib inline
import matplotlib.pyplot as plt
plt.rcParams['figure.dpi'] = 100
```

---

### 9. Specific Error Messages

#### "EEException: Invalid JSON"

**Cause**: Malformed GEE request

**Solution**:
- Usually transient, retry will work
- If persistent, check that coordinate values are valid numbers

#### "HttpError 429: Too Many Requests"

**Cause**: Rate limiting

**Solution**:
- Pipeline will automatically retry
- Wait a few minutes between manual runs

#### "HttpError 500: Internal Server Error"

**Cause**: GEE server issue

**Solution**:
- Temporary GEE server problem
- Wait and retry
- Check GEE status: https://status.earthengine.google.com/

#### "ValueError: could not convert string to float"

**Cause**: Data type issue in downloaded data

**Solution**:
- Check for null/missing values in raw data
- May indicate upstream data quality issue
- Review specific records causing the error

---

### 10. Validation Failures

After running `validate_extraction.py`:

#### "Missing file" errors

**Solution**: Pipeline didn't complete successfully. Re-run main pipeline.

#### "Quartile ordering violation"

**Cause**: Statistical computation error

**Solution**:
- This shouldn't happen with the provided code
- If it does, there may be data corruption
- Re-run extraction for affected periods

#### "Record count lower than expected"

**Cause**: Data gaps or limited availability

**Solution**:
- Check quality report for specific gaps
- Verify date range in source datasets
- May be normal for certain datasets/periods

---

## Getting More Help

### 1. Check the log file first
```bash
cat climate_data_output/soweto_climate_extraction.log
```

### 2. Run validation script
```bash
python validate_extraction.py
```

### 3. Check GEE status
Visit: https://status.earthengine.google.com/

### 4. Test GEE connection
```bash
python -c "
import ee
ee.Initialize()
print('Testing GEE...')
point = ee.Geometry.Point([27.8585, -26.2678])
print(f'Point created: {point.getInfo()}')
print('GEE connection OK')
"
```

### 5. Check Python environment
```bash
python --version
pip list
which python
```

### 6. Search GEE forums
Google Earth Engine Developers: https://groups.google.com/g/google-earth-engine-developers

### 7. Review GEE documentation
- API Reference: https://developers.google.com/earth-engine
- Data Catalog: https://developers.google.com/earth-engine/datasets

---

## Prevention Tips

### Before running the pipeline

1. Verify GEE authentication: `earthengine authenticate`
2. Test internet connection
3. Check available disk space (need ~500MB for outputs)
4. Verify Python environment is activated
5. Review configuration settings for your use case

### During execution

1. Don't interrupt the pipeline unnecessarily
2. Monitor log file for errors: `tail -f climate_data_output/soweto_climate_extraction.log`
3. Be patient - full extraction takes 15-30 minutes

### After completion

1. Run validation script
2. Review quality report
3. Check all expected files are present
4. Verify data ranges are reasonable

---

## Emergency Recovery

### If pipeline fails mid-execution

The pipeline is designed to be resumable, but if you need to restart:

1. **Check what data was extracted**:
   ```bash
   ls -lh climate_data_output/
   ```

2. **Review log to find failure point**:
   ```bash
   grep -A 5 ERROR climate_data_output/soweto_climate_extraction.log | tail -20
   ```

3. **If raw data exists but aggregations missing**, you can recompute aggregations without re-extracting raw data (see "Missing some aggregation files" above)

4. **For complete re-run**:
   ```bash
   # Backup existing data
   mv climate_data_output climate_data_output_backup_$(date +%Y%m%d)

   # Re-run pipeline
   python soweto_climate_pipeline.py
   ```

---

## Performance Benchmarks

Expected performance on typical hardware:

| Operation | Time | Records |
|-----------|------|---------|
| Authentication | 10-30s | - |
| Single batch (6 months temp) | 30-90s | ~4,400 |
| Single batch (6 months PM2.5) | 20-60s | ~1,500 |
| Full extraction (11 years) | 15-30 min | ~100,000 |
| Aggregations | 1-2 min | - |
| Quality checks | <1 min | - |

Factors affecting performance:
- GEE server load (time of day)
- Internet connection speed
- Region/location (distance to GEE servers)
- Concurrent GEE users

---

## Advanced Debugging

### Enable verbose logging

Edit pipeline to add debug logging:
```python
logging.basicConfig(
    level=logging.DEBUG,  # Change from INFO to DEBUG
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_path),
        logging.StreamHandler()
    ]
)
```

### Test individual components

```python
# Test authentication only
from soweto_climate_pipeline import GEEAuthenticator
import logging
logger = logging.getLogger()
auth = GEEAuthenticator()
success = auth.authenticate(logger)
print(f"Auth success: {success}")

# Test data extractor initialization
from soweto_climate_pipeline import ClimateDataExtractor, PipelineConfig
config = PipelineConfig()
extractor = ClimateDataExtractor(config, logger)
print(f"Extractor point: {extractor.point.getInfo()}")

# Test small extraction
temp_data = extractor.extract_temperature_batch('2020-01-01', '2020-01-07')
print(f"Records extracted: {len(temp_data)}")
```

### Profile performance

```bash
# Run with profiling
python -m cProfile -o profile.stats soweto_climate_pipeline.py

# View results
python -c "
import pstats
p = pstats.Stats('profile.stats')
p.sort_stats('cumulative')
p.print_stats(20)
"
```

---

## Contact and Support

For issues with:
- **Pipeline code**: Check this guide and logs
- **GEE platform**: Visit https://developers.google.com/earth-engine/support
- **Data availability**: Consult GEE Data Catalog
- **Research questions**: Refer to data source documentation (ERA5, CAMS)

---

**Last Updated**: 2026-02-09
**Pipeline Version**: 1.0.0
