# TikTok GUI with Excel Export Guide

## 🎯 Overview

The TikTok GUI now includes full Excel export functionality! You can automatically extract all video metadata and save it to Excel files through the graphical interface.

## 🚀 How to Use the GUI with Excel Export

### 1. Start the GUI

```bash
python downloader/tiktok_gui.py
```

### 2. GUI Features for Excel Export

The GUI now includes these Excel export features:

#### ✅ **Excel Export Checkbox**
- **Location**: In the "Download Options" section
- **Default**: Checked (enabled)
- **Function**: Enables automatic Excel export when downloading videos

#### ✅ **Excel Filename Field**
- **Location**: Below the Excel export checkbox
- **Default**: `tiktok_videos_metadata.xlsx`
- **Function**: Set custom filename for the Excel file

#### ✅ **Process Existing Downloads Button**
- **Location**: In the "Download Options" section
- **Function**: Process already downloaded videos and create Excel file from their metadata

## 📊 What Information is Extracted

The Excel file contains **23 columns** of detailed information:

### Basic Video Information
- **Video ID** - Unique TikTok identifier
- **Title** - Video title/caption
- **Description** - Full description with hashtags
- **Upload Date** - When posted (YYYY-MM-DD format)
- **Duration** - Length in seconds and MM:SS format

### Creator Information
- **Uploader** - Creator's username
- **Uploader ID** - Creator's unique ID
- **Channel** - Display name
- **Channel ID** - Channel identifier

### Engagement Metrics
- **View Count** - Number of views
- **Like Count** - Number of likes
- **Comment Count** - Number of comments
- **Repost Count** - Number of shares

### Content Analysis
- **Hashtags** - All hashtags (comma-separated)
- **Original URL** - Direct TikTok link
- **Thumbnail URL** - Preview image URL

### Technical Details
- **Video Quality** - Format and quality
- **File Size** - Size in bytes
- **Resolution** - Dimensions (width x height)
- **Format** - File format (mp4, etc.)

### Download Information
- **Download Date** - When downloaded
- **Download Path** - Local file location

## 🎮 Step-by-Step Usage

### Method 1: Download New Videos with Excel Export

1. **Start the GUI**
   ```bash
   python downloader/tiktok_gui.py
   ```

2. **Configure Excel Export**
   - ✅ Check "Export to Excel" checkbox
   - 📝 Set Excel filename (optional)
   - 📁 Set output directory

3. **Enter TikTok URL(s)**
   - Single URL: Paste in the URL field
   - Batch URLs: Check "Batch Mode" and paste multiple URLs

4. **Set Download Options**
   - Quality: best, 720p, 480p, etc.
   - Audio only: Check if you want audio only
   - Include metadata: Should be checked for Excel export

5. **Click "Download Video"**
   - Videos will download
   - Excel file will be created automatically
   - Progress shown in the log area

### Method 2: Process Existing Downloads

1. **Start the GUI**

2. **Configure Excel Export**
   - ✅ Check "Export to Excel" checkbox
   - 📝 Set Excel filename (optional)

3. **Click "Process Existing Downloads"**
   - GUI will scan your downloads folder
   - Find all `.info.json` files
   - Create Excel file from existing metadata
   - Show progress in log area

## 📁 File Organization

### Excel File Location
- **Default**: Same directory as downloaded videos
- **Path**: `downloads/tiktok_videos_metadata.xlsx`
- **Custom**: You can set any filename in the GUI

### File Naming
- **Auto-generated**: `tiktok_videos_metadata_YYYYMMDD_HHMMSS.xlsx`
- **Custom**: Set in the "Excel Filename" field

## 🎨 Excel Features

### Professional Formatting
- **Headers**: Bold white text on blue background
- **Numbers**: Formatted with thousands separators
- **Auto-sizing**: Column widths adjust to content
- **Clean layout**: Professional appearance

### Data Types
- **Text**: Titles, descriptions, URLs
- **Numbers**: View counts, like counts, file sizes
- **Dates**: Upload dates, download timestamps
- **Formatted text**: Duration in MM:SS format

## 📈 Example Output

Here's what you'll see in the Excel file:

| Video ID | Title | Uploader | Duration | View Count | Like Count | Comment Count |
|----------|-------|----------|----------|------------|------------|---------------|
| 7487241884029472022 | \| Funny Baby Moment \| 😂😂😂#funny #meme #fyp #top... | topworldmoment | 01:00 | 18,300,000 | 1,900,000 | 10,100 |
| 7523786006542241079 | The Cutest Reactions 🥺❤️ #baby #babiesoftiktok... | babyboofunny | 01:03 | 36,800,000 | 2,800,000 | 11,700 |
| 7536937672632192270 | 😭😭😭 funniest baby moments that will make your d... | ehfea | 01:05 | 2,000,000 | 77,900 | 2,034 |

## 🔧 Advanced Features

### Batch Processing
- Download multiple videos at once
- All metadata automatically added to Excel
- Progress tracking for each video
- Error handling for failed downloads

### Real-time Feedback
- Live progress updates in log area
- Success/error messages for each operation
- Status bar showing current operation
- Excel file location displayed when complete

### Error Handling
- Graceful handling of network errors
- Continues processing if individual videos fail
- Detailed error messages in log
- Automatic retry for temporary issues

## 🎯 Use Cases

### Content Analysis
- Track engagement metrics across videos
- Analyze hashtag usage patterns
- Monitor creator performance
- Study viral content characteristics

### Data Export
- Export data for external analysis tools
- Create reports for content strategy
- Backup metadata for downloaded content
- Share data with team members

### Research
- Study trending topics and hashtags
- Track content performance over time
- Analyze audience engagement patterns
- Compare different content types

## 🚨 Limitations

- **Comments content**: Only comment count, not actual text
- **Real-time data**: Metrics from download time, not live
- **Private videos**: Can only access public videos
- **Rate limiting**: TikTok may limit requests for large batches

## 📞 Troubleshooting

### Common Issues

1. **Excel file not created**
   - Check "Export to Excel" is checked
   - Verify output directory exists
   - Check log for error messages

2. **Missing metadata**
   - Ensure "Include Metadata" is checked
   - Check internet connection
   - Verify TikTok URLs are valid

3. **GUI not responding**
   - Check log for error messages
   - Restart the application
   - Verify all dependencies are installed

### Dependencies Required
```bash
pip install openpyxl yt-dlp colorama tkinter
```

## 🎉 Success!

Your TikTok GUI now provides:
- ✅ **Easy-to-use interface** for downloading videos
- ✅ **Automatic Excel export** with all metadata
- ✅ **Batch processing** for multiple videos
- ✅ **Professional Excel formatting**
- ✅ **Real-time progress tracking**
- ✅ **Error handling and logging**

**Happy downloading and analyzing! 🎉**
