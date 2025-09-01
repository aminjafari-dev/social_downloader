#!/bin/bash

echo "========================================"
echo "Social Downloader - macOS Setup"
echo "========================================"
echo

# Check if Python is installed
if command -v python3 &> /dev/null; then
    echo "Python 3 is already installed."
    python3 --version
else
    echo "Python 3 is not installed."
    echo "Installing Python 3 using Homebrew..."
    
    # Check if Homebrew is installed
    if command -v brew &> /dev/null; then
        brew install python
    else
        echo "Homebrew is not installed. Installing Homebrew first..."
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        brew install python
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
    echo "- Double-click start_mac.sh"
    echo "- Or run: python3 src/run.py"
    echo
else
    echo
    echo "Error installing packages. Please try again."
    echo "If the problem persists, try running with sudo."
    exit 1
fi

# Make start script executable
chmod +x start_mac.sh

echo "Press any key to continue..."
read -n 1
