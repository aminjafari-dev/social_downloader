# TikTok Downloader Excel Export Guide

## 🎯 Overview

Your TikTok downloader now includes comprehensive Excel export functionality that extracts and organizes all available metadata from TikTok videos into a structured Excel file.

## 📊 What Information is Extracted

The Excel file contains **23 columns** of detailed information for each video:

### Basic Video Information
- **Video ID** - Unique TikTok video identifier
- **Title** - Video title/caption
- **Description** - Full video description with hashtags
- **Upload Date** - When the video was posted (YYYY-MM-DD format)
- **Duration** - Video length in both seconds and MM:SS format

### Creator Information
- **Uploader** - Creator's username/handle
- **Uploader ID** - Creator's unique identifier
- **Channel** - Display name
- **Channel ID** - Channel identifier

### Engagement Metrics
- **View Count** - Number of views
- **Like Count** - Number of likes
- **Comment Count** - Number of comments
- **Repost Count** - Number of shares/reposts

### Content Analysis
- **Hashtags** - All hashtags used in the video (comma-separated)
- **Original URL** - Direct link to the TikTok video
- **Thumbnail URL** - Video preview image URL

### Technical Details
- **Video Quality** - Selected video format and quality
- **File Size** - Video file size in bytes
- **Resolution** - Video dimensions (width x height)
- **Format** - Video file format (mp4, etc.)

### Download Information
- **Download Date** - When the video was downloaded
- **Download Path** - Local file path where video is stored

## 🚀 How to Use

### 1. Download New Videos with Excel Export

```bash
# Single video download
python downloader/tiktok_downloader.py --url "https://www.tiktok.com/@user/video/1234567890"

# Batch download from file
python downloader/tiktok_downloader.py --file urls.txt

# Download with specific quality
python downloader/tiktok_downloader.py --url "https://tiktok.com/@user/video/1234567890" --quality 720p
```

### 2. Process Existing Downloads

If you already have downloaded videos, you can create an Excel file from their existing metadata:

```bash
python downloader/tiktok_downloader.py --process-existing
```

### 3. Programmatic Usage

```python
from downloader.tiktok_downloader import TikTokDownloader

# Initialize downloader
downloader = TikTokDownloader(
    output_dir="downloads",
    quality="best",
    add_metadata=True
)

# Download single video
success = downloader.download_video("https://www.tiktok.com/@user/video/1234567890")
if success:
    downloader.save_excel_file()

# Process existing downloads
downloader.process_existing_downloads()
```

## 📁 File Organization

### Excel File Naming
- **Auto-generated**: `tiktok_videos_metadata_YYYYMMDD_HHMMSS.xlsx`
- **Custom**: You can specify a custom filename in the constructor

### File Location
- Excel files are saved in the same directory as downloaded videos
- Default location: `downloads/tiktok_videos_metadata_*.xlsx`

## 🎨 Excel Features

### Formatting
- **Headers**: Bold white text on blue background
- **Numbers**: Formatted with thousands separators
- **Auto-sizing**: Column widths adjust to content
- **Professional styling**: Clean, readable layout

### Data Types
- **Text**: Titles, descriptions, URLs
- **Numbers**: View counts, like counts, file sizes
- **Dates**: Upload dates, download timestamps
- **Formatted text**: Duration in MM:SS format

## 📈 Example Output

Here's what the Excel file looks like for your existing downloads:

| Video ID | Title | Uploader | Duration | View Count | Like Count | Comment Count |
|----------|-------|----------|----------|------------|------------|---------------|
| 7487241884029472022 | \| Funny Baby Moment \| 😂😂😂#funny #meme #fyp #top... | topworldmoment | 01:00 | 18,300,000 | 1,900,000 | 10,100 |
| 7523786006542241079 | The Cutest Reactions 🥺❤️ #baby #babiesoftiktok... | babyboofunny | 01:03 | 36,800,000 | 2,800,000 | 11,700 |
| 7536937672632192270 | 😭😭😭 funniest baby moments that will make your d... | ehfea | 01:05 | 2,000,000 | 77,900 | 2,034 |

## 🔧 Advanced Features

### Custom Excel File Path
```python
downloader = TikTokDownloader(
    output_dir="downloads",
    excel_file="custom_metadata.xlsx"
)
```

### Batch Processing
The downloader automatically:
- Extracts metadata during download
- Adds each video to the Excel file
- Saves the file after batch completion
- Provides progress feedback

### Error Handling
- Graceful handling of missing metadata
- Logging of any processing errors
- Continues processing even if individual videos fail

## 📋 Requirements

Make sure you have the required dependencies:
```bash
pip install openpyxl yt-dlp colorama
```

## 🎯 Use Cases

### Content Analysis
- Track engagement metrics across videos
- Analyze hashtag usage patterns
- Monitor creator performance

### Data Export
- Export data for external analysis tools
- Create reports for content strategy
- Backup metadata for downloaded content

### Research
- Study viral content characteristics
- Analyze trending topics and hashtags
- Track content performance over time

## 🚨 Limitations

- **Comments content**: Only comment count is available, not actual comment text
- **Real-time data**: Metrics are from download time, not live
- **Private videos**: Can only access public videos
- **Rate limiting**: TikTok may limit requests for large batches

## 📞 Support

If you encounter any issues:
1. Check the log file: `tiktok_downloader.log`
2. Verify your internet connection
3. Ensure TikTok URLs are valid and public
4. Check that all dependencies are installed

---

**Happy downloading and analyzing! 🎉**

