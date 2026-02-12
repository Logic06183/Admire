#!/bin/bash

# Soweto Climate Data Extraction Pipeline
# Quick Start Execution Script

echo "========================================================================"
echo "Soweto Climate Data Extraction Pipeline"
echo "========================================================================"
echo ""

# Change to script directory
cd "$(dirname "$0")"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Creating one..."
    python3 -m venv venv
    echo "Installing dependencies..."
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
else
    echo "Activating virtual environment..."
    source venv/bin/activate
fi

echo ""
echo "Starting pipeline execution..."
echo "This will take approximately 15-30 minutes depending on GEE server load."
echo ""
echo "Output will be saved to: climate_data_output/"
echo "Logs will be saved to: climate_data_output/soweto_climate_extraction.log"
echo ""
echo "------------------------------------------------------------------------"
echo ""

# Run the pipeline
python soweto_climate_pipeline.py

# Check exit status
if [ $? -eq 0 ]; then
    echo ""
    echo "========================================================================"
    echo "Pipeline completed successfully!"
    echo "========================================================================"
    echo ""
    echo "Check the following files in climate_data_output/:"
    echo "  - soweto_temperature_raw.csv"
    echo "  - soweto_pm25_raw.csv"
    echo "  - soweto_temp_*_stats.csv"
    echo "  - soweto_pm25_*_stats.csv"
    echo "  - quality_report.json"
    echo "  - soweto_climate_extraction.log"
else
    echo ""
    echo "========================================================================"
    echo "Pipeline encountered an error!"
    echo "========================================================================"
    echo ""
    echo "Check the log file for details:"
    echo "  climate_data_output/soweto_climate_extraction.log"
fi

echo ""
