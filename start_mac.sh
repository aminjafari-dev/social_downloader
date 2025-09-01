#!/bin/bash

echo "========================================"
echo "Social Downloader - Starting Application"
echo "========================================"
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed. Please run setup_mac.sh first."
    read -p "Press any key to continue..."
    exit 1
fi

echo "Starting Social Downloader..."
echo

# Change to the script directory
cd "$(dirname "$0")"

# Run the application
python3 src/run.py

if [ $? -ne 0 ]; then
    echo
    echo "Error starting the application."
    echo "Please make sure you have run setup_mac.sh first."
    read -p "Press any key to continue..."
fi
