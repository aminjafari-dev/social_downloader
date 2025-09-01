# Excel Import Feature Guide

## Overview

The TikTok Video Downloader now includes an **Excel Import Feature** that allows you to download multiple TikTok videos by reading URLs from an Excel file. This is perfect for batch downloading when you have a list of TikTok URLs stored in a spreadsheet.

## Features

- **Excel File Support**: Supports both `.xlsx` and `.xls` files
- **Column Selection**: Automatically detects and lets you choose which column contains the URLs
- **URL Validation**: Validates URLs before downloading to ensure they are valid TikTok links
- **Preview Function**: Preview URLs before downloading to verify the selection
- **Duplicate Removal**: Automatically removes duplicate URLs
- **Progress Tracking**: Shows download progress for each video
- **Error Handling**: Graceful handling of invalid URLs and file errors

## How to Use

### Step 1: Prepare Your Excel File

Your Excel file should have a column containing TikTok URLs. The column can be named anything (e.g., "URL", "Link", "TikTok URL", etc.).

Example Excel structure:
| Title | URL | Description |
|-------|-----|-------------|
| Video 1 | https://www.tiktok.com/@user1/video/1234567890123456789 | First video |
| Video 2 | https://www.tiktok.com/@user2/video/9876543210987654321 | Second video |

### Step 2: Open the GUI

Run the TikTok Video Downloader GUI:
```bash
python main.py
```

### Step 3: Use the Excel Import Section

1. **Select Excel File**:
   - Click the "Browse" button in the "Excel File Import" section
   - Navigate to and select your Excel file
   - The file path will appear in the text field

2. **Load Columns**:
   - Click "Load Columns" to read the column names from your Excel file
   - The system will automatically detect columns that might contain URLs
   - If a column with "url" in the name is found, it will be auto-selected

3. **Select URL Column**:
   - Choose the column that contains your TikTok URLs from the dropdown
   - If no column is auto-selected, manually select the appropriate column

4. **Preview URLs (Optional)**:
   - Click "Preview URLs" to see a summary of the URLs found
   - This shows the total number of URLs and the first 5 URLs
   - Helps verify you've selected the correct column

5. **Start Download**:
   - Click "Download from Excel" to begin downloading all videos
   - The system will validate URLs and remove duplicates automatically
   - Download progress will be shown in the log section

## Excel File Requirements

### Supported Formats
- `.xlsx` (Excel 2007 and later)
- `.xls` (Excel 97-2003)

### Column Requirements
- Must contain at least one column with TikTok URLs
- URLs should be valid TikTok video links
- Empty cells are automatically ignored
- Non-URL content in the URL column will be filtered out

### URL Format
The system accepts various TikTok URL formats:
- `https://www.tiktok.com/@username/video/1234567890123456789`
- `https://vm.tiktok.com/xxxxx/`
- `https://www.tiktok.com/t/xxxxx/`

## Example Workflow

1. **Create Excel File**: Export your TikTok URLs to Excel or create a spreadsheet with URLs
2. **Open GUI**: Launch the TikTok Video Downloader
3. **Import Excel**: Use the Excel import section to load your file
4. **Configure Options**: Set your preferred download options (quality, output directory, etc.)
5. **Download**: Start the batch download process
6. **Monitor Progress**: Watch the log for download progress and any errors

## Error Handling

### Common Issues and Solutions

**"Failed to load Excel file"**
- Ensure the file is not corrupted
- Check that the file is a valid Excel format
- Make sure the file is not open in another application

**"Column not found"**
- Verify the column name exactly matches what's in your Excel file
- Column names are case-sensitive
- Check for extra spaces in column names

**"No valid TikTok URLs found"**
- Ensure your URLs are valid TikTok video links
- Check that the URLs are in the correct column
- Verify URLs are not truncated or malformed

**"Duplicate URLs removed"**
- This is normal behavior to prevent downloading the same video multiple times
- The system will continue with unique URLs only

## Tips and Best Practices

1. **Backup Your Data**: Always keep a backup of your Excel file before processing
2. **Test with Small Files**: Start with a small number of URLs to test the process
3. **Check URLs**: Use the preview function to verify your URLs before downloading
4. **Monitor Downloads**: Watch the log for any failed downloads or errors
5. **Use Descriptive Column Names**: Name your URL column clearly (e.g., "TikTok URL", "Video Link")
6. **Clean Your Data**: Remove any non-URL content from your URL column before importing

## Advanced Features

### Custom Naming
- Use the "Custom Base Name" option to give your downloaded videos a specific naming pattern
- Videos will be named: `customname__1.mp4`, `customname__2.mp4`, etc.

### Excel Export
- Enable "Export to Excel" to create a metadata file with information about downloaded videos
- This creates a separate Excel file with video details like title, description, uploader, etc.

### Quality Selection
- Choose video quality before downloading (best, worst, 720p, 480p, 360p)
- Audio-only option available for extracting just the audio

## Troubleshooting

If you encounter issues:

1. **Check the Log**: The log section shows detailed information about what's happening
2. **Verify File Permissions**: Ensure you have read access to the Excel file
3. **Update Dependencies**: Make sure you have the latest version of pandas and openpyxl
4. **Test URL Format**: Try copying a URL directly to the single URL input to test if it works

## Support

For additional help or to report issues:
- Check the log output for error messages
- Verify your Excel file format and content
- Ensure all required dependencies are installed

---

**Note**: This feature requires the `pandas` library to be installed. If you encounter import errors, install it with:
```bash
pip install pandas
```

