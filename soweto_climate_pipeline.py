"""
Soweto Climate Data Extraction Pipeline
========================================

This pipeline extracts real observational/reanalysis climate data for Soweto, South Africa
using Google Earth Engine and GEEMAP.

Data Sources:
- Temperature: ERA5-Land hourly reanalysis (2m temperature)
- PM2.5: Copernicus Atmosphere Monitoring Service (CAMS) Global Reanalysis

Author: Climate Data Engineering Pipeline
Date: 2026-02-09
Version: 1.0.0
"""

import ee
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import logging
import json
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import time
from functools import wraps
from dataclasses import dataclass, field

# ============================================================================
# CONFIGURATION
# ============================================================================

@dataclass(frozen=True)
class PipelineConfig:
    """Centralized configuration for the climate data pipeline."""

    # Location Configuration
    SOWETO_LAT: float = -26.2678
    SOWETO_LON: float = 27.8585
    BUFFER_DISTANCE: int = 5000  # meters

    # Temporal Configuration
    START_DATE: str = '2014-01-01'
    END_DATE: str = '2024-12-31'

    # Data Source Configuration
    TEMPERATURE_COLLECTION: str = 'ECMWF/ERA5_LAND/HOURLY'
    TEMPERATURE_BAND: str = 'temperature_2m'
    TEMPERATURE_SCALE: int = 11132

    # PM2.5 Configuration (CAMS Global Reanalysis)
    PM25_COLLECTION: str = 'ECMWF/CAMS/NRT'
    PM25_BAND: str = 'particulate_matter_d_less_than_25_um_surface'
    PM25_SCALE: int = 40000

    # Processing Configuration
    BATCH_SIZE_MONTHS: int = 6
    PM25_BATCH_SIZE_MONTHS: int = 2
    MAX_RETRIES: int = 3
    RETRY_DELAY: int = 5

    # Output Configuration
    OUTPUT_DIR: Path = field(
        default_factory=lambda: Path(__file__).resolve().parent / 'climate_data_output'
    )
    LOG_FILE: str = 'soweto_climate_extraction.log'

    # Seasonal Definitions (Southern Hemisphere)
    SEASONS: Dict[str, List[int]] = field(default_factory=lambda: {
        'Summer': [12, 1, 2],
        'Autumn': [3, 4, 5],
        'Winter': [6, 7, 8],
        'Spring': [9, 10, 11]
    })

    # Verification windows to ensure the pipeline talks to live GEE datasets
    DATASET_VERIFICATION_WINDOWS: Dict[str, Tuple[str, str]] = field(default_factory=lambda: {
        'temperature': ('2014-01-01', '2014-01-07'),
        # CAMS NRT has reliable coverage later in the record
        'pm25': ('2018-01-01', '2018-01-07')
    })

# ============================================================================
# LOGGING SETUP
# ============================================================================

def setup_logging(config: PipelineConfig) -> logging.Logger:
    """Configure logging with both file and console handlers."""
    config.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    log_path = config.OUTPUT_DIR / config.LOG_FILE

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_path),
            logging.StreamHandler()
        ]
    )

    logger = logging.getLogger('SowetoClimatePipeline')
    logger.info("="*80)
    logger.info("Soweto Climate Data Extraction Pipeline Initialized")
    logger.info("="*80)

    return logger

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def retry_on_ee_error(max_retries: int = 3, delay: int = 5):
    """Decorator for retrying GEE operations with exponential backoff."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except ee.EEException as e:
                    if attempt == max_retries - 1:
                        raise
                    wait_time = delay * (2 ** attempt)
                    logging.warning(f"GEE error in {func.__name__}: {e}. Retrying in {wait_time}s...")
                    time.sleep(wait_time)
        return wrapper
    return decorator

def kelvin_to_celsius(temp_k: float) -> float:
    """Convert temperature from Kelvin to Celsius."""
    return temp_k - 273.15

def kg_to_micrograms_per_m3(pm25_kg: float) -> float:
    """
    Convert PM2.5 from kg/m³ to μg/m³.

    CAMS NRT (Copernicus Atmosphere Monitoring Service) provides PM2.5
    concentrations in kg/m³, but standard air quality research and WHO
    guidelines use μg/m³.

    Conversion factor: 1 kg/m³ = 10^9 μg/m³

    Args:
        pm25_kg: PM2.5 concentration in kg/m³ from CAMS NRT

    Returns:
        PM2.5 concentration in μg/m³

    Example:
        >>> kg_to_micrograms_per_m3(1.0e-7)
        100.0  # 100 μg/m³
    """
    return pm25_kg * 1e9

# ============================================================================
# GEE AUTHENTICATION
# ============================================================================

class GEEAuthenticator:
    """Handle Google Earth Engine authentication."""

    @staticmethod
    def authenticate(logger: logging.Logger) -> bool:
        """
        Authenticate with Google Earth Engine.

        Returns:
            bool: True if authentication successful
        """
        try:
            # Try to initialize with existing credentials
            ee.Initialize()
            logger.info("GEE authentication successful (using existing credentials)")
            return True
        except Exception as e:
            logger.warning(f"Existing credentials failed: {e}")
            try:
                # Trigger authentication flow
                ee.Authenticate()
                ee.Initialize()
                logger.info("GEE authentication successful (new credentials)")
                return True
            except Exception as auth_error:
                logger.error(f"GEE authentication failed: {auth_error}")
                return False

    @staticmethod
    def verify_collection_access(
        collection_id: str,
        start: str,
        end: str,
        logger: logging.Logger
    ) -> bool:
        """Ensure a target collection returns live data within a sample window."""
        try:
            collection = ee.ImageCollection(collection_id).filterDate(start, end)
            image_count = collection.size().getInfo()

            if image_count == 0:
                logger.error(
                    f"Verification failed for {collection_id}: no imagery between {start} and {end}"
                )
                return False

            logger.info(
                f"Verified {collection_id} contains {image_count} images between {start} and {end}"
            )
            return True
        except ee.EEException as e:
            logger.error(f"Failed to verify collection {collection_id}: {e}")
            return False

# ============================================================================
# DATA EXTRACTION
# ============================================================================

class ClimateDataExtractor:
    """Extract climate data from Google Earth Engine."""

    def __init__(self, config: PipelineConfig, logger: logging.Logger):
        self.config = config
        self.logger = logger
        self.point = ee.Geometry.Point([config.SOWETO_LON, config.SOWETO_LAT])
        self.region = self.point.buffer(config.BUFFER_DISTANCE)

    @retry_on_ee_error(max_retries=3, delay=5)
    def extract_temperature_batch(self, start_date: str, end_date: str) -> pd.DataFrame:
        """
        Extract temperature data for a specific date range.

        Args:
            start_date: Start date in 'YYYY-MM-DD' format
            end_date: End date in 'YYYY-MM-DD' format

        Returns:
            DataFrame with temperature data
        """
        self.logger.info(f"Extracting temperature: {start_date} to {end_date}")

        # Load ERA5-Land collection
        collection = ee.ImageCollection(self.config.TEMPERATURE_COLLECTION) \
            .filterDate(start_date, end_date) \
            .select(self.config.TEMPERATURE_BAND)

        # Define reduction function for spatial averaging
        def extract_temperature(image):
            # Calculate mean temperature over the region
            stats = image.reduceRegion(
                reducer=ee.Reducer.mean(),
                geometry=self.region,
                scale=self.config.TEMPERATURE_SCALE,
                maxPixels=1e9
            )

            # Get timestamp
            timestamp = image.get('system:time_start')

            return ee.Feature(None, {
                'timestamp': timestamp,
                'date': ee.Date(timestamp).format('YYYY-MM-dd HH:mm:ss'),
                'temperature_k': stats.get(self.config.TEMPERATURE_BAND)
            })

        # Extract data
        features = collection.map(extract_temperature)

        # Convert to pandas DataFrame using Earth Engine's getInfo()
        feature_list = features.getInfo()['features']

        if not feature_list:
            self.logger.warning(f"No temperature data returned for {start_date} to {end_date}")
            return pd.DataFrame()

        # Convert to pandas DataFrame
        data_records = [feat['properties'] for feat in feature_list]
        data = pd.DataFrame(data_records)

        # Convert Kelvin to Celsius
        data['temperature_c'] = data['temperature_k'].apply(kelvin_to_celsius)
        data['date'] = pd.to_datetime(data['date'])

        self.logger.info(f"Extracted {len(data)} temperature records")

        return data[['date', 'temperature_c']]

    @retry_on_ee_error(max_retries=3, delay=5)
    def extract_pm25_batch(self, start_date: str, end_date: str) -> pd.DataFrame:
        """
        Extract PM2.5 data for a specific date range.

        Args:
            start_date: Start date in 'YYYY-MM-DD' format
            end_date: End date in 'YYYY-MM-DD' format

        Returns:
            DataFrame with PM2.5 data
        """
        self.logger.info(f"Extracting PM2.5: {start_date} to {end_date}")

        # Load CAMS collection
        # Note: CAMS NRT data availability may be limited before 2016
        collection = ee.ImageCollection(self.config.PM25_COLLECTION) \
            .filterDate(start_date, end_date) \
            .select(self.config.PM25_BAND)

        # Define reduction function for spatial averaging
        def extract_pm25(image):
            # Calculate mean PM2.5 over the region
            stats = image.reduceRegion(
                reducer=ee.Reducer.mean(),
                geometry=self.region,
                scale=self.config.PM25_SCALE,
                maxPixels=1e9
            )

            # Get timestamp
            timestamp = image.get('system:time_start')

            return ee.Feature(None, {
                'timestamp': timestamp,
                'date': ee.Date(timestamp).format('YYYY-MM-dd HH:mm:ss'),
                'pm25': stats.get(self.config.PM25_BAND)
            })

        # Extract data
        features = collection.map(extract_pm25)

        # Convert to pandas DataFrame using Earth Engine's getInfo()
        feature_list = features.getInfo()['features']

        if not feature_list:
            self.logger.warning(f"No PM2.5 data returned for {start_date} to {end_date}")
            return pd.DataFrame()

        # Convert to pandas DataFrame
        data_records = [feat['properties'] for feat in feature_list]
        data = pd.DataFrame(data_records)

        data['date'] = pd.to_datetime(data['date'])

        # Convert PM2.5 from kg/m³ to μg/m³
        data['pm25'] = data['pm25'].apply(kg_to_micrograms_per_m3)

        self.logger.info(f"Extracted {len(data)} PM2.5 records")

        return data[['date', 'pm25']]

# ============================================================================
# BATCH PROCESSING
# ============================================================================

class BatchProcessor:
    """Handle batch processing of date ranges."""

    def __init__(self, config: PipelineConfig, logger: logging.Logger):
        self.config = config
        self.logger = logger

    def generate_date_batches(self, batch_size_months: Optional[int] = None) -> List[Tuple[str, str]]:
        """
        Generate date range batches for processing.

        Args:
            batch_size_months: Number of months per batch (defaults to config.BATCH_SIZE_MONTHS)

        Returns:
            List of (start_date, end_date) tuples
        """
        if batch_size_months is None:
            batch_size_months = self.config.BATCH_SIZE_MONTHS

        start = datetime.strptime(self.config.START_DATE, '%Y-%m-%d')
        end = datetime.strptime(self.config.END_DATE, '%Y-%m-%d')

        batches = []
        current = start

        while current < end:
            batch_end = current + timedelta(days=batch_size_months * 30)
            if batch_end > end:
                batch_end = end

            batches.append((
                current.strftime('%Y-%m-%d'),
                batch_end.strftime('%Y-%m-%d')
            ))

            current = batch_end

        self.logger.info(f"Generated {len(batches)} date batches ({batch_size_months} months each)")
        return batches

    def process_variable_batches(
        self,
        extractor: ClimateDataExtractor,
        variable: str,
        extract_func,
        batch_size_months: Optional[int] = None
    ) -> pd.DataFrame:
        """
        Process all batches for a specific variable.

        Args:
            extractor: ClimateDataExtractor instance
            variable: Variable name ('temperature' or 'pm25')
            extract_func: Extraction function to call
            batch_size_months: Number of months per batch (optional override)

        Returns:
            Combined DataFrame with all data
        """
        batches = self.generate_date_batches(batch_size_months)
        all_data = []

        for i, (start, end) in enumerate(batches, 1):
            self.logger.info(f"Processing {variable} batch {i}/{len(batches)}")

            try:
                batch_data = extract_func(start, end)
                if not batch_data.empty:
                    all_data.append(batch_data)

                # Add small delay to avoid rate limiting
                time.sleep(1)

            except Exception as e:
                self.logger.error(f"Failed to process batch {i} for {variable}: {e}")
                continue

        if not all_data:
            self.logger.warning(f"No data extracted for {variable}")
            return pd.DataFrame()

        combined = pd.concat(all_data, ignore_index=True)
        combined = combined.sort_values('date').reset_index(drop=True)

        self.logger.info(f"Total {variable} records: {len(combined)}")

        return combined

# ============================================================================
# STATISTICAL AGGREGATIONS
# ============================================================================

class StatisticalAggregator:
    """Compute temporal statistical aggregations."""

    def __init__(self, config: PipelineConfig, logger: logging.Logger):
        self.config = config
        self.logger = logger

    def compute_statistics(self, df: pd.DataFrame, column: str) -> Dict:
        """Compute mean, median, and IQR for a column."""
        return {
            f'{column}_mean': df[column].mean(),
            f'{column}_median': df[column].median(),
            f'{column}_q25': df[column].quantile(0.25),
            f'{column}_q75': df[column].quantile(0.75),
            f'{column}_q10': df[column].quantile(0.10),
            f'{column}_q90': df[column].quantile(0.90),
            f'{column}_iqr': df[column].quantile(0.75) - df[column].quantile(0.25),
            f'{column}_std': df[column].std(ddof=0),
            f'{column}_min': df[column].min(),
            f'{column}_max': df[column].max(),
            f'{column}_count': df[column].count()
        }

    def aggregate_monthly(self, df: pd.DataFrame, variable: str) -> pd.DataFrame:
        """Compute monthly statistics."""
        self.logger.info(f"Computing monthly statistics for {variable}")

        df = df.copy()
        df['year'] = df['date'].dt.year
        df['month'] = df['date'].dt.month

        monthly_stats = df.groupby(['year', 'month']).apply(
            lambda x: pd.Series(self.compute_statistics(x, variable)),
            include_groups=False
        ).reset_index()

        return monthly_stats

    def aggregate_seasonal(self, df: pd.DataFrame, variable: str) -> pd.DataFrame:
        """Compute seasonal statistics (Southern Hemisphere seasons)."""
        self.logger.info(f"Computing seasonal statistics for {variable}")

        df = df.copy()
        df['month'] = df['date'].dt.month
        df['year'] = df['date'].dt.year

        # Assign seasons
        def get_season(month, year):
            for season, months in self.config.SEASONS.items():
                if month in months:
                    # December belongs to next year's summer
                    if season == 'Summer' and month == 12:
                        return season, year + 1
                    return season, year
            return None, None

        df[['season', 'season_year']] = df.apply(
            lambda row: get_season(row['month'], row['year']),
            axis=1,
            result_type='expand'
        )

        seasonal_stats = df.groupby(['season_year', 'season']).apply(
            lambda x: pd.Series(self.compute_statistics(x, variable)),
            include_groups=False
        ).reset_index()

        return seasonal_stats

    def aggregate_annual(self, df: pd.DataFrame, variable: str) -> pd.DataFrame:
        """Compute annual statistics."""
        self.logger.info(f"Computing annual statistics for {variable}")

        df = df.copy()
        df['year'] = df['date'].dt.year

        annual_stats = df.groupby('year').apply(
            lambda x: pd.Series(self.compute_statistics(x, variable)),
            include_groups=False
        ).reset_index()

        return annual_stats

# ============================================================================
# DATA QUALITY CHECKS
# ============================================================================

class DataQualityChecker:
    """Perform data quality checks and validation."""

    def __init__(self, logger: logging.Logger):
        self.logger = logger

    def check_data_completeness(
        self,
        df: pd.DataFrame,
        start_date: str,
        end_date: str,
        variable: str
    ) -> Dict:
        """Check data completeness and identify gaps."""
        self.logger.info(f"Performing quality checks for {variable}")

        if df.empty:
            self.logger.error(f"No data available for {variable}")
            return {'status': 'FAILED', 'reason': 'No data'}

        # Check date range coverage
        actual_start = df['date'].min()
        actual_end = df['date'].max()
        expected_start = pd.to_datetime(start_date)
        expected_end = pd.to_datetime(end_date)

        # Check for missing values
        missing_count = df[variable].isna().sum()
        total_count = len(df)
        missing_pct = (missing_count / total_count) * 100

        # Check for outliers (using IQR method)
        q1 = df[variable].quantile(0.25)
        q3 = df[variable].quantile(0.75)
        iqr = q3 - q1
        lower_bound = q1 - 3 * iqr
        upper_bound = q3 + 3 * iqr
        outliers = df[(df[variable] < lower_bound) | (df[variable] > upper_bound)]

        quality_report = {
            'variable': variable,
            'total_records': total_count,
            'missing_values': missing_count,
            'missing_percentage': missing_pct,
            'outlier_count': len(outliers),
            'date_range_actual': f"{actual_start} to {actual_end}",
            'date_range_expected': f"{expected_start} to {expected_end}",
            'min_value': df[variable].min(),
            'max_value': df[variable].max(),
            'mean_value': df[variable].mean(),
            'status': 'PASSED' if missing_pct < 10 else 'WARNING'
        }

        self.logger.info(f"Quality check for {variable}: {quality_report['status']}")
        self.logger.info(f"  Records: {total_count}, Missing: {missing_pct:.2f}%, Outliers: {len(outliers)}")

        return quality_report

# ============================================================================
# PIPELINE ORCHESTRATION
# ============================================================================

class ClimatePipeline:
    """Main pipeline orchestrator."""

    def __init__(self):
        self.config = PipelineConfig()
        self.logger = setup_logging(self.config)
        self.extractor = None
        self.batch_processor = None
        self.aggregator = None
        self.quality_checker = DataQualityChecker(self.logger)

    def initialize(self) -> bool:
        """Initialize the pipeline components."""
        self.logger.info("Initializing pipeline components...")

        # Authenticate with GEE
        authenticator = GEEAuthenticator()
        if not authenticator.authenticate(self.logger):
            self.logger.error("Failed to authenticate with GEE")
            return False

        # Verify we can talk to the real datasets before extracting anything
        verification_windows = self.config.DATASET_VERIFICATION_WINDOWS
        temp_ok = authenticator.verify_collection_access(
            self.config.TEMPERATURE_COLLECTION,
            *verification_windows['temperature'],
            logger=self.logger
        )
        pm25_ok = authenticator.verify_collection_access(
            self.config.PM25_COLLECTION,
            *verification_windows['pm25'],
            logger=self.logger
        )

        if not (temp_ok and pm25_ok):
            self.logger.error("Aborting: failed to verify live access to one or more collections")
            return False

        # Initialize components
        self.extractor = ClimateDataExtractor(self.config, self.logger)
        self.batch_processor = BatchProcessor(self.config, self.logger)
        self.aggregator = StatisticalAggregator(self.config, self.logger)

        self.logger.info("Pipeline initialization complete")
        return True

    def extract_all_data(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Extract temperature and PM2.5 data."""
        self.logger.info("="*80)
        self.logger.info("STARTING DATA EXTRACTION")
        self.logger.info("="*80)

        # Extract temperature (6-month batches)
        temp_data = self.batch_processor.process_variable_batches(
            self.extractor,
            'temperature_c',
            self.extractor.extract_temperature_batch,
            batch_size_months=self.config.BATCH_SIZE_MONTHS
        )

        # Extract PM2.5 (2-month batches to avoid GEE limits)
        pm25_data = self.batch_processor.process_variable_batches(
            self.extractor,
            'pm25',
            self.extractor.extract_pm25_batch,
            batch_size_months=self.config.PM25_BATCH_SIZE_MONTHS
        )

        return temp_data, pm25_data

    def perform_quality_checks(
        self,
        temp_data: pd.DataFrame,
        pm25_data: pd.DataFrame
    ) -> Tuple[Dict, Dict]:
        """Perform quality checks on extracted data."""
        self.logger.info("="*80)
        self.logger.info("PERFORMING QUALITY CHECKS")
        self.logger.info("="*80)

        temp_qc = self.quality_checker.check_data_completeness(
            temp_data,
            self.config.START_DATE,
            self.config.END_DATE,
            'temperature_c'
        )

        pm25_qc = self.quality_checker.check_data_completeness(
            pm25_data,
            self.config.START_DATE,
            self.config.END_DATE,
            'pm25'
        )

        return temp_qc, pm25_qc

    def compute_all_aggregations(
        self,
        temp_data: pd.DataFrame,
        pm25_data: pd.DataFrame
    ) -> Dict[str, pd.DataFrame]:
        """Compute all temporal aggregations."""
        self.logger.info("="*80)
        self.logger.info("COMPUTING STATISTICAL AGGREGATIONS")
        self.logger.info("="*80)

        aggregations = {}

        # Temperature aggregations
        if not temp_data.empty:
            aggregations['temp_monthly'] = self.aggregator.aggregate_monthly(temp_data, 'temperature_c')
            aggregations['temp_seasonal'] = self.aggregator.aggregate_seasonal(temp_data, 'temperature_c')
            aggregations['temp_annual'] = self.aggregator.aggregate_annual(temp_data, 'temperature_c')

        # PM2.5 aggregations
        if not pm25_data.empty:
            aggregations['pm25_monthly'] = self.aggregator.aggregate_monthly(pm25_data, 'pm25')
            aggregations['pm25_seasonal'] = self.aggregator.aggregate_seasonal(pm25_data, 'pm25')
            aggregations['pm25_annual'] = self.aggregator.aggregate_annual(pm25_data, 'pm25')

        return aggregations

    def save_results(
        self,
        temp_data: pd.DataFrame,
        pm25_data: pd.DataFrame,
        aggregations: Dict[str, pd.DataFrame],
        temp_qc: Dict,
        pm25_qc: Dict
    ):
        """Save all results to files."""
        self.logger.info("="*80)
        self.logger.info("SAVING RESULTS")
        self.logger.info("="*80)

        def save_minmax_view(name: str, df: pd.DataFrame):
            """Save a compact table with min/max (and percentile context) for Admire."""
            min_col = next((col for col in df.columns if col.endswith('_min')), None)
            max_col = next((col for col in df.columns if col.endswith('_max')), None)

            if not (min_col and max_col):
                return

            context_cols = [col for col in ['year', 'season_year', 'season', 'month'] if col in df.columns]
            extra_cols = [
                col for col in df.columns
                if col.endswith(('_q10', '_q90', '_median', '_mean'))
            ]

            minmax_df = df[context_cols + extra_cols + [min_col, max_col]].copy()
            minmax_df = minmax_df.rename(columns={
                min_col: 'min_value',
                max_col: 'max_value'
            })

            out_path = self.config.OUTPUT_DIR / f'soweto_{name}_minmax.csv'
            minmax_df.to_csv(out_path, index=False)
            self.logger.info(f"Saved {name} min/max summary: {out_path}")

        # Save raw data
        if not temp_data.empty:
            temp_path = self.config.OUTPUT_DIR / 'soweto_temperature_raw.csv'
            temp_data.to_csv(temp_path, index=False)
            self.logger.info(f"Saved temperature raw data: {temp_path}")

        if not pm25_data.empty:
            pm25_path = self.config.OUTPUT_DIR / 'soweto_pm25_raw.csv'
            pm25_data.to_csv(pm25_path, index=False)
            self.logger.info(f"Saved PM2.5 raw data: {pm25_path}")

        # Save aggregations
        for name, df in aggregations.items():
            agg_path = self.config.OUTPUT_DIR / f'soweto_{name}_stats.csv'
            df.to_csv(agg_path, index=False)
            self.logger.info(f"Saved {name} aggregations: {agg_path}")
            save_minmax_view(name, df)

        # Save quality reports
        qc_report = {
            'temperature': temp_qc,
            'pm25': pm25_qc,
            'pipeline_info': {
                'execution_date': datetime.now().isoformat(),
                'location': f"Soweto ({self.config.SOWETO_LAT}, {self.config.SOWETO_LON})",
                'buffer_distance_m': self.config.BUFFER_DISTANCE,
                'date_range': f"{self.config.START_DATE} to {self.config.END_DATE}",
                'data_sources': {
                    'temperature': self.config.TEMPERATURE_COLLECTION,
                    'pm25': self.config.PM25_COLLECTION
                }
            }
        }

        qc_path = self.config.OUTPUT_DIR / 'quality_report.json'
        with open(qc_path, 'w') as f:
            json.dump(qc_report, f, indent=2, default=str)
        self.logger.info(f"Saved quality report: {qc_path}")

    def run(self):
        """Execute the complete pipeline."""
        start_time = datetime.now()
        self.logger.info(f"Pipeline execution started at {start_time}")

        try:
            # Initialize
            if not self.initialize():
                return

            # Extract data
            temp_data, pm25_data = self.extract_all_data()

            # Quality checks
            temp_qc, pm25_qc = self.perform_quality_checks(temp_data, pm25_data)

            # Compute aggregations
            aggregations = self.compute_all_aggregations(temp_data, pm25_data)

            # Save results
            self.save_results(temp_data, pm25_data, aggregations, temp_qc, pm25_qc)

            # Final summary
            end_time = datetime.now()
            duration = end_time - start_time

            self.logger.info("="*80)
            self.logger.info("PIPELINE EXECUTION COMPLETE")
            self.logger.info("="*80)
            self.logger.info(f"Duration: {duration}")
            self.logger.info(f"Temperature records: {len(temp_data)}")
            self.logger.info(f"PM2.5 records: {len(pm25_data)}")
            self.logger.info(f"Output directory: {self.config.OUTPUT_DIR}")
            self.logger.info("="*80)

        except Exception as e:
            self.logger.error(f"Pipeline failed with error: {e}", exc_info=True)
            raise

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main entry point for the pipeline."""
    pipeline = ClimatePipeline()
    pipeline.run()

if __name__ == "__main__":
    main()
