# Social Downloader - User Guide

## 🎯 Getting Started

### First Time Setup
1. **Download the application** to your computer
2. **Extract the folder** to your Desktop or any location you prefer
3. **Run the setup script** for your operating system:
   - **Windows**: Double-click `setup_windows.bat`
   - **Mac**: Double-click `setup_mac.sh`
   - **Linux**: Double-click `setup_linux.sh`
4. **Wait for setup to complete** (this may take a few minutes)
5. **Verify installation** by running `python verify_installation.py`

### Starting the Application
1. **Windows**: Double-click `start_windows.bat`
2. **Mac**: Double-click `start_mac.sh`
3. **Linux**: Double-click `start_linux.sh`

## 🎮 How to Use the Application

### Basic Video Download

#### Step 1: Get a Video URL
1. Go to TikTok (or other supported platform)
2. Find the video you want to download
3. Copy the URL from your browser's address bar
4. The URL should look like: `https://www.tiktok.com/@username/video/1234567890`

#### Step 2: Download the Video
1. **Launch the application** using the start script
2. **Paste the URL** into the "Video URL" field
3. **Choose download quality** (Best, 720p, 480p, etc.)
4. **Click "Download"** button
5. **Wait for completion** - you'll see progress updates
6. **Find your video** in the `downloads` folder

### Batch Downloads (Multiple Videos)

#### Method 1: Multiple URLs
1. **Enter multiple URLs** separated by commas in the URL field
2. **Example**: `url1, url2, url3`
3. **Click "Download"** to download all videos

#### Method 2: Excel File Import
1. **Create an Excel file** with video URLs in the first column
2. **Click "Browse"** next to "Excel File" option
3. **Select your Excel file**
4. **Click "Download"** to download all videos from the file

### Advanced Settings

#### Download Quality
- **Best**: Highest available quality (larger file size)
- **720p**: Good quality, smaller file size
- **480p**: Medium quality, smaller file size
- **360p**: Lower quality, smallest file size

#### File Naming
- **Original**: Keep original video title
- **Custom**: Use your own naming pattern
- **Date**: Include download date in filename

#### Download Location
- **Default**: Videos save to `downloads` folder
- **Custom**: Choose your own folder location

## 📁 Understanding the Interface

### Main Window Components

#### URL Input Section
- **Video URL Field**: Paste your video URL here
- **Browse Button**: Select Excel file for batch downloads
- **Clear Button**: Clear the URL field

#### Settings Section
- **Quality Dropdown**: Choose video quality
- **Output Directory**: Select where to save videos
- **File Naming**: Choose how to name downloaded files

#### Download Section
- **Download Button**: Start the download process
- **Progress Bar**: Shows download progress
- **Status Text**: Displays current operation status

#### Log Section
- **Log Window**: Shows detailed information about downloads
- **Clear Log**: Clear the log window
- **Save Log**: Save log to a file

## 🔧 Troubleshooting Common Issues

### Download Problems

#### "Video not found" Error
- **Check the URL**: Make sure it's a valid TikTok URL
- **Try again**: Sometimes videos are temporarily unavailable
- **Check internet**: Ensure you have a stable internet connection

#### "Download failed" Error
- **Check permissions**: Make sure the app can write to the downloads folder
- **Check disk space**: Ensure you have enough free space
- **Try different quality**: Some videos may not be available in all qualities

#### "Network error" Message
- **Check internet connection**: Make sure you're connected to the internet
- **Try again later**: The platform might be experiencing issues
- **Check firewall**: Make sure the app isn't blocked by your firewall

### Application Problems

#### Application won't start
- **Run setup script**: Make sure you've run the setup script first
- **Check Python**: Ensure Python is installed correctly
- **Run as administrator**: Try running the start script as administrator

#### "Module not found" Error
- **Reinstall packages**: Run the setup script again
- **Check Python path**: Make sure Python is in your system PATH
- **Update Python**: Try updating to a newer Python version

#### GUI not appearing
- **Check display settings**: Ensure your display scaling is set correctly
- **Update graphics drivers**: Update your graphics card drivers
- **Try different resolution**: Change your screen resolution temporarily

## 📋 Tips for Best Results

### Download Quality
- **Use "Best" quality** for important videos you want to keep
- **Use "720p" or "480p"** for regular downloads to save space
- **Use "360p"** for quick previews or when storage is limited

### Batch Downloads
- **Limit batch size**: Download 10-20 videos at a time for better reliability
- **Check URLs**: Verify all URLs are valid before starting batch download
- **Monitor progress**: Keep an eye on the log window for any errors

### File Organization
- **Use descriptive names**: Choose custom naming to organize your videos
- **Create subfolders**: Organize downloads by date, creator, or category
- **Backup important videos**: Copy important downloads to a backup location

### Performance
- **Close other applications**: Free up system resources for faster downloads
- **Use wired connection**: Ethernet connection is more stable than WiFi
- **Avoid peak hours**: Download during off-peak hours for better speeds

## 🔒 Privacy and Legal Considerations

### Respect Copyright
- **Personal use only**: Download videos for personal viewing only
- **Don't redistribute**: Don't share downloaded videos without permission
- **Check terms of service**: Respect the platform's terms of service

### Data Privacy
- **Local storage**: Videos are stored locally on your computer
- **No data collection**: The app doesn't collect or share your data
- **Secure downloads**: Downloads are processed locally

### Responsible Use
- **Respect creators**: Support content creators when possible
- **Follow platform rules**: Don't violate platform terms of service
- **Use ethically**: Only download content you have permission to access

## 📞 Getting Help

### Before Asking for Help
1. **Check this guide**: Review the troubleshooting section
2. **Try the verification script**: Run `python verify_installation.py`
3. **Check the log**: Look at the application log for error details
4. **Try a simple download**: Test with a single, simple URL first

### When Contacting Support
- **Include error messages**: Copy the exact error message
- **Describe your setup**: Mention your operating system and Python version
- **Provide URLs**: Include the URLs that are causing problems
- **Attach logs**: Include the application log if possible

### Common Support Questions
- **"How do I install Python?"**: Follow the setup script instructions
- **"Where are my downloads?"**: Check the `downloads` folder
- **"Why is it slow?"**: Check your internet connection and try different quality settings
- **"Can I download from other platforms?"**: Currently supports TikTok and similar platforms

---

**Happy downloading!** 🎉
