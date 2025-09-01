# Social Downloader - User Guide

## 🎯 What is this application?

Social Downloader is a user-friendly application that helps you download videos from TikTok and other social media platforms. It features a simple graphical interface that makes downloading videos easy, even if you have no programming experience.

## ✨ Features

- **Easy-to-use GUI**: Simple interface with buttons and forms
- **Batch Downloads**: Download multiple videos at once
- **Excel Integration**: Import video URLs from Excel files
- **Custom Naming**: Choose how your downloaded files are named
- **Download Progress**: See real-time progress of your downloads
- **Error Handling**: Clear messages when something goes wrong

## 🚀 Quick Start Guide

### Step 1: Download and Extract
1. Download the application folder to your computer
2. Extract (unzip) the folder to a location you can easily find (like Desktop)

### Step 2: Run the Setup Script
1. **Windows Users**: Double-click on `setup_windows.bat`
2. **Mac Users**: Double-click on `setup_mac.sh`
3. **Linux Users**: Double-click on `setup_linux.sh`

The setup script will automatically:
- Install Python (if not already installed)
- Install all required packages
- Set up the application for first use

### Step 3: Launch the Application
1. **Windows Users**: Double-click on `start_windows.bat`
2. **Mac Users**: Double-click on `start_mac.sh`
3. **Linux Users**: Double-click on `start_linux.sh`

## 📋 System Requirements

- **Operating System**: Windows 10/11, macOS 10.14+, or Linux
- **Internet Connection**: Required for downloading videos
- **Storage Space**: At least 500MB free space
- **Memory**: 4GB RAM recommended

## 🛠️ Manual Setup (If Auto-Setup Doesn't Work)

### Windows Manual Setup
1. Download Python from [python.org](https://www.python.org/downloads/)
2. During installation, make sure to check "Add Python to PATH"
3. Open Command Prompt (cmd) in the application folder
4. Type: `pip install -r requirements.txt`
5. Type: `python src/run.py`

### Mac Manual Setup
1. Install Python using Homebrew: `brew install python`
2. Open Terminal in the application folder
3. Type: `pip3 install -r requirements.txt`
4. Type: `python3 src/run.py`

### Linux Manual Setup
1. Install Python: `sudo apt-get install python3 python3-pip`
2. Open Terminal in the application folder
3. Type: `pip3 install -r requirements.txt`
4. Type: `python3 src/run.py`

## 🎮 How to Use the Application

### Basic Usage
1. **Launch the app** using the start script
2. **Enter a video URL** in the text field
3. **Click "Download"** to start downloading
4. **Find your video** in the `downloads` folder

### Advanced Features
- **Batch Mode**: Add multiple URLs separated by commas
- **Excel Import**: Use the Excel integration to download from a spreadsheet
- **Custom Settings**: Adjust download quality and file naming
- **Progress Tracking**: Monitor download progress in real-time

## 📁 File Structure

```
social_downloader/
├── downloads/              # Downloaded videos go here
├── src/                    # Application source code
├── requirements.txt        # Required packages
├── setup_windows.bat      # Windows setup script
├── setup_mac.sh           # Mac setup script
├── setup_linux.sh         # Linux setup script
├── start_windows.bat      # Windows start script
├── start_mac.sh           # Mac start script
├── start_linux.sh         # Linux start script
└── README.md              # This file
```

## 🔧 Troubleshooting

### Common Issues and Solutions

**Problem**: "Python is not recognized"
- **Solution**: Run the setup script again or install Python manually

**Problem**: "Module not found" error
- **Solution**: Run `pip install -r requirements.txt` in the application folder

**Problem**: Application won't start
- **Solution**: Make sure you're running the start script from the main folder

**Problem**: Downloads fail
- **Solution**: Check your internet connection and try again

**Problem**: Permission denied (Mac/Linux)
- **Solution**: Right-click the script and select "Open" or run from terminal

### Getting Help
If you encounter any issues:
1. Check the troubleshooting section above
2. Make sure all files are in the correct folders
3. Try running the setup script again
4. Contact support with the exact error message

## 📝 Notes

- Downloaded videos are saved in the `downloads` folder
- The application requires an internet connection to download videos
- Some videos may be protected and cannot be downloaded
- Always respect copyright and terms of service when downloading content

## 🔄 Updates

To update the application:
1. Download the new version
2. Replace the old files with new ones
3. Run the setup script again
4. Your downloaded videos will remain in the downloads folder

---

**Enjoy downloading your favorite videos!** 🎉

