# TikTok Video Downloader

A powerful Python application for downloading TikTok videos from URLs with metadata extraction and quality selection.

## Features

- **Single Video Download**: Download individual TikTok videos with quality selection
- **Batch Download**: Download multiple videos from a list of URLs
- **Quality Selection**: Choose video quality (best, 720p, 480p, etc.)
- **Metadata Extraction**: Extract video information and save metadata
- **GUI Interface**: User-friendly graphical interface for downloads
- **Progress Tracking**: Real-time download progress and status
- **Error Handling**: Comprehensive error handling and retry logic
- **Organized Output**: Automatic file organization and naming

## Installation

1. Clone or download this repository
2. Install required dependencies:

```bash
pip install -r requirements.txt
```

## Quick Start

### Download a Single Video
```bash
python main.py download --url "https://tiktok.com/@user/video/123456789"
```

### Download with Custom Quality
```bash
python main.py download --url "https://tiktok.com/@user/video/123456789" --quality 720p
```

### Batch Download from File
```bash
python main.py download-batch --file urls.txt --output-dir downloads
```

### Using the GUI
```bash
python downloader/tiktok_gui.py
```

## Usage Examples

### Example 1: Single Video Download
```python
from downloader.tiktok_downloader import TikTokDownloader

# Initialize downloader
downloader = TikTokDownloader(output_dir="downloads", quality="best")

# Download a video
success = downloader.download_video("https://tiktok.com/@user/video/123456789")

if success:
    print("Video downloaded successfully!")
```

### Example 2: Batch Download
```python
from downloader.tiktok_downloader import TikTokDownloader

# Initialize downloader
downloader = TikTokDownloader(output_dir="downloads", quality="720p")

# List of URLs to download
urls = [
    "https://tiktok.com/@user1/video/123456789",
    "https://tiktok.com/@user2/video/987654321",
    "https://tiktok.com/@user3/video/456789123"
]

# Download multiple videos
results = downloader.download_multiple_videos(urls)

# Check results
successful = sum(results.values())
print(f"Successfully downloaded {successful}/{len(urls)} videos")
```

### Example 3: GUI Usage
```python
from downloader.tiktok_gui import TikTokDownloaderGUI

# Launch GUI
app = TikTokDownloaderGUI()
app.run()
```

## Command Line Interface

### Download Command
```bash
python main.py download [OPTIONS]

Options:
  --url, -u TEXT        TikTok video URL [required]
  --output-dir TEXT     Output directory [default: downloads]
  --quality TEXT        Video quality (best, 720p, 480p, etc.) [default: best]
```

### Batch Download Command
```bash
python main.py download-batch [OPTIONS]

Options:
  --file, -f TEXT       File containing TikTok URLs (one per line) [required]
  --output-dir TEXT     Output directory [default: downloads]
  --quality TEXT        Video quality (best, 720p, 480p, etc.) [default: best]
```

## Project Structure

```
social_downloader/
├── main.py                     # Main application entry point
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── QUICK_START_GUIDE.md        # Quick start guide
├── downloader/                 # Core download functionality
│   ├── __init__.py
│   ├── tiktok_downloader.py    # Core TikTok downloader
│   └── tiktok_gui.py           # GUI interface
├── core/                       # Shared utilities
│   ├── __init__.py
│   └── example.py              # Example usage
├── gui/                        # GUI utilities
│   └── __init__.py
├── tests/                      # Test files
│   ├── __init__.py
│   └── test_installation.py    # Installation tests
├── docs/                       # Documentation
├── downloads/                  # Downloaded content
│   ├── original/               # Original downloaded videos
│   ├── processed/              # Processed videos (if any)
│   └── metadata/               # Video metadata
└── models/                     # Data models
```

## Download Features

### Quality Options
- **best**: Highest available quality
- **720p**: 720p resolution
- **480p**: 480p resolution
- **360p**: 360p resolution
- **auto**: Automatic quality selection

### Output Organization
- **Original Videos**: Downloaded videos in original format
- **Metadata**: JSON files with video information
- **Descriptions**: Text files with video descriptions
- **Thumbnails**: Video thumbnail images

### File Naming
- Automatic sanitization of filenames
- Preservation of original video titles
- Unique naming to prevent conflicts
- Organized folder structure

## Configuration

### Download Settings
- **Output Directory**: Customizable download location
- **Quality Selection**: Configurable video quality
- **Retry Logic**: Automatic retry on failures
- **Timeout Settings**: Configurable download timeouts
- **Concurrent Downloads**: Parallel download support

### Browser Settings
- **User Agent**: Custom user agent to avoid detection
- **Headers**: Configurable HTTP headers
- **Cookies**: Session management
- **Proxy Support**: Optional proxy configuration

## Error Handling

The application includes comprehensive error handling:
- **Network Errors**: Automatic retry with exponential backoff
- **Invalid URLs**: Skip invalid or inaccessible videos
- **Rate Limiting**: Intelligent delays and user agent rotation
- **Disk Space**: Check available space before downloads
- **File Conflicts**: Handle duplicate filenames

## Logging

Detailed logging is provided:
- **File Logging**: Logs saved to `tiktok_downloader.log`
- **Console Output**: Real-time progress updates
- **Error Tracking**: Detailed error messages and stack traces
- **Download Statistics**: Success/failure rates and performance metrics

## GUI Features

### Main Interface
- **URL Input**: Paste TikTok video URLs
- **Quality Selection**: Choose download quality
- **Output Directory**: Select download location
- **Progress Bar**: Real-time download progress
- **Status Updates**: Current operation status

### Batch Operations
- **File Import**: Import URLs from text files
- **URL List**: Manage multiple URLs
- **Progress Tracking**: Individual file progress
- **Results Summary**: Download success/failure summary

## Troubleshooting

### Common Issues

1. **Download Failures**
   - Check internet connection
   - Verify TikTok URL validity
   - Ensure sufficient disk space
   - Try different quality settings

2. **Browser Issues**
   - Update Chrome/Chromium
   - Check ChromeDriver compatibility
   - Verify system permissions
   - Clear browser cache

3. **File Access Errors**
   - Check file permissions
   - Verify output directory exists
   - Ensure write access to download location
   - Close any open files

### Performance Tips

1. **Use Appropriate Quality**: Choose quality based on needs
2. **Batch Downloads**: Use batch mode for multiple videos
3. **Stable Internet**: Ensure reliable connection
4. **Adequate Resources**: Sufficient RAM and CPU
5. **Regular Updates**: Keep dependencies updated

## Legal and Ethical Considerations

- **Terms of Service**: Respect TikTok's terms of service
- **Rate Limiting**: Use reasonable download rates
- **Content Rights**: Respect copyright and content ownership
- **Personal Use**: Intended for personal, educational, or research purposes
- **Data Privacy**: Handle user data responsibly

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is for educational and personal use. Please respect TikTok's terms of service and applicable laws.

## Support

For issues and questions:
1. Check the documentation in the `docs/` folder
2. Review the troubleshooting section
3. Check existing issues
4. Create a new issue with detailed information

## Changelog

### Version 1.0.0
- Initial release
- Single video download functionality
- Batch download capability
- GUI interface
- Quality selection options
- Comprehensive error handling
- Detailed logging and progress tracking

