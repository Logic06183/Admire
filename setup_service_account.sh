#!/bin/bash
# Setup script for using GEE with service account credentials

echo "📋 Google Earth Engine - Service Account Setup"
echo "=============================================="
echo ""
echo "Follow these steps in your browser:"
echo ""
echo "1. Service Accounts page should be open"
echo "   If not, visit: https://console.cloud.google.com/iam-admin/serviceaccounts"
echo ""
echo "2. CREATE SERVICE ACCOUNT"
echo "   Name: earth-engine-pipeline"
echo "   Role: Earth Engine Resource Writer"
echo ""
echo "3. CREATE JSON KEY and download it"
echo ""
echo "4. Move the downloaded JSON file to this directory:"
echo "   $(pwd)"
echo ""
echo "5. Then run:"
echo "   export GOOGLE_APPLICATION_CREDENTIALS='$(pwd)/your-key-file.json'"
echo "   python3 test_gee_connection.py"
echo ""
echo "=============================================="
echo ""
read -p "Have you downloaded the JSON key file? (y/n): " response

if [[ "$response" == "y" || "$response" == "Y" ]]; then
    echo ""
    echo "Great! What's the filename of your JSON key?"
    echo "It's probably something like: soweto-climate-analysis-abc123.json"
    echo ""
    ls -1 *.json 2>/dev/null || echo "No .json files found in current directory"
    echo ""
    read -p "Enter the filename: " keyfile

    if [ -f "$keyfile" ]; then
        echo ""
        echo "✅ Found: $keyfile"
        echo ""
        echo "Setting environment variable and testing connection..."
        export GOOGLE_APPLICATION_CREDENTIALS="$(pwd)/$keyfile"

        # Test connection
        python3 test_gee_connection.py

        echo ""
        echo "=============================================="
        echo "To use this credential in future sessions, run:"
        echo ""
        echo "  export GOOGLE_APPLICATION_CREDENTIALS='$(pwd)/$keyfile'"
        echo ""
        echo "Or add it to your ~/.zshrc or ~/.bash_profile"
        echo "=============================================="
    else
        echo ""
        echo "❌ File not found: $keyfile"
        echo "Please make sure the JSON key is in:"
        echo "$(pwd)"
    fi
else
    echo ""
    echo "📌 Complete steps 1-4 above, then re-run this script"
fi
