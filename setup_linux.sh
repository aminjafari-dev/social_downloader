#!/bin/bash

echo "========================================"
echo "Social Downloader - Linux Setup"
echo "========================================"
echo

# Check if Python is installed
if command -v python3 &> /dev/null; then
    echo "Python 3 is already installed."
    python3 --version
else
    echo "Python 3 is not installed."
    echo "Installing Python 3..."
    
    # Detect package manager and install Python
    if command -v apt-get &> /dev/null; then
        sudo apt-get update
        sudo apt-get install -y python3 python3-pip
    elif command -v yum &> /dev/null; then
        sudo yum install -y python3 python3-pip
    elif command -v dnf &> /dev/null; then
        sudo dnf install -y python3 python3-pip
    elif command -v pacman &> /dev/null; then
        sudo pacman -S python python-pip
    else
        echo "Could not detect package manager. Please install Python 3 manually."
        exit 1
    fi
fi

echo
echo "Installing required packages..."
echo "This may take a few minutes..."
echo

# Install packages
pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo
    echo "========================================"
    echo "Setup completed successfully!"
    echo "========================================"
    echo
    echo "You can now run the application using:"
    echo "- Double-click start_linux.sh"
    echo "- Or run: python3 src/run.py"
    echo
else
    echo
    echo "Error installing packages. Please try again."
    echo "If the problem persists, try running with sudo."
    exit 1
fi

# Make start script executable
chmod +x start_linux.sh

echo "Press any key to continue..."
read -n 1
