# TikTok Video Downloader - Modular Architecture

This document describes the new modular architecture for the TikTok Video Downloader application. The code has been reorganized into separate, focused modules that are easier to maintain, test, and extend.

## 🏗️ Architecture Overview

The new architecture follows a modular design pattern where each component has a single responsibility and can be used independently or together.

```
core/
├── __init__.py                 # Core module exports
├── video_downloader.py         # Core video downloading functionality
├── tiktok_downloader.py        # TikTok-specific downloader
├── excel_metadata_manager.py   # Excel metadata management
├── url_processor.py            # URL validation and processing
└── download_manager.py         # Main orchestrator
```

## 🔧 Core Components

### 1. VideoDownloader (`core/video_downloader.py`)

**Purpose**: Core video downloading functionality using yt-dlp.

**Responsibilities**:
- Configure yt-dlp options
- Download videos from URLs
- Extract video information
- Manage download paths and naming
- Handle video counters

**Key Methods**:
- `download_video(url)` - Download a single video
- `download_multiple_videos(urls)` - Download multiple videos
- `get_video_info(url)` - Extract video metadata without downloading
- `validate_url(url)` - Basic URL validation
- `update_settings(**kwargs)` - Update downloader settings

**Usage Example**:
```python
from core import VideoDownloader

downloader = VideoDownloader(
    output_dir="downloads",
    quality="best",
    extract_audio=False,
    add_metadata=True
)

success = downloader.download_video("https://example.com/video")
```

### 2. TikTokDownloader (`core/tiktok_downloader.py`)

**Purpose**: TikTok-specific functionality that extends the core VideoDownloader.

**Responsibilities**:
- TikTok URL validation
- TikTok metadata extraction
- TikTok-specific file naming
- Backward compatibility with existing code

**Key Features**:
- Extends `VideoDownloader` class
- TikTok domain validation
- TikTok-specific metadata extraction
- Custom naming patterns for TikTok videos

**Usage Example**:
```python
from core import TikTokDownloader

tiktok_downloader = TikTokDownloader(
    output_dir="downloads",
    quality="best",
    custom_base_name="tiktok_video"
)

success = tiktok_downloader.download_video("https://www.tiktok.com/@user/video/123")
```

### 3. ExcelMetadataManager (`core/excel_metadata_manager.py`)

**Purpose**: Handle all Excel-related operations for storing video metadata.

**Responsibilities**:
- Create and configure Excel workbooks
- Add video metadata to Excel sheets
- Format and style Excel data
- Save and manage Excel files
- Process existing downloads

**Key Methods**:
- `add_video_metadata(info, download_path)` - Add video metadata to Excel
- `save_excel_file()` - Save the Excel file
- `process_existing_downloads()` - Process existing downloaded videos
- `load_existing_excel(file_path)` - Load existing Excel file

**Usage Example**:
```python
from core import ExcelMetadataManager

excel_manager = ExcelMetadataManager(
    output_dir="downloads",
    filename="videos_metadata.xlsx"
)

excel_manager.add_video_metadata(video_info, download_path)
excel_manager.save_excel_file()
```

### 4. URLProcessor (`core/url_processor.py`)

**Purpose**: Handle URL validation, processing, and batch operations.

**Responsibilities**:
- URL validation for different platforms
- Batch URL processing from text
- Duplicate URL detection and removal
- URL normalization and cleaning
- Platform detection

**Key Methods**:
- `validate_url(url, platform)` - Validate URL for specific platform
- `process_batch_text(text, platform)` - Process batch text containing URLs
- `remove_duplicates(urls)` - Remove duplicate URLs
- `get_platform_stats(urls)` - Get statistics about URLs by platform

**Usage Example**:
```python
from core import URLProcessor

processor = URLProcessor()

# Validate TikTok URLs
valid_urls, invalid_urls = processor.validate_urls(urls, platform="tiktok")

# Process batch text
valid_urls, invalid_urls = processor.process_batch_text(batch_text, platform="tiktok")
```

### 5. DownloadManager (`core/download_manager.py`)

**Purpose**: Main orchestrator that coordinates all components.

**Responsibilities**:
- Initialize and manage all components
- Coordinate download process
- Handle batch operations
- Manage Excel export
- Provide unified interface

**Key Methods**:
- `download_single_video(url, export_to_excel)` - Download single video
- `download_multiple_videos(urls, export_to_excel)` - Download multiple videos
- `process_existing_downloads(export_to_excel)` - Process existing downloads
- `update_settings(**kwargs)` - Update all component settings

**Usage Example**:
```python
from core import DownloadManager

manager = DownloadManager(
    output_dir="downloads",
    quality="best",
    platform="tiktok"
)

# Download single video
result = manager.download_single_video(url, export_to_excel=True)

# Download multiple videos
results = manager.download_multiple_videos(urls, export_to_excel=True)
```

## 🚀 Usage Examples

### Basic Single Video Download

```python
from core import DownloadManager

# Create download manager
manager = DownloadManager(
    output_dir="downloads",
    quality="best",
    platform="tiktok"
)

# Download a video
result = manager.download_single_video(
    "https://www.tiktok.com/@user/video/1234567890",
    export_to_excel=True
)

if result['success']:
    print(f"Downloaded: {result['metadata']['title']}")
    print(f"Excel file: {result['excel_file']}")
else:
    print(f"Error: {result['error']}")
```

### Batch Download with Custom Naming

```python
from core import DownloadManager

# Create download manager with custom naming
manager = DownloadManager(
    output_dir="downloads",
    quality="720p",
    custom_base_name="my_videos",
    platform="tiktok"
)

# List of URLs to download
urls = [
    "https://www.tiktok.com/@user1/video/123",
    "https://www.tiktok.com/@user2/video/456",
    "https://www.tiktok.com/@user3/video/789"
]

# Download all videos
results = manager.download_multiple_videos(urls, export_to_excel=True)

print(f"Downloaded {results['successful']}/{results['valid_urls']} videos")
print(f"Excel file: {results['excel_file']}")
```

### URL Processing and Validation

```python
from core import URLProcessor

processor = URLProcessor()

# Process batch text
batch_text = """
https://www.tiktok.com/@user1/video/123
https://www.tiktok.com/@user2/video/456
https://invalid-url.com
"""

valid_urls, invalid_urls = processor.process_batch_text(batch_text, platform="tiktok")

print(f"Valid URLs: {valid_urls}")
print(f"Invalid URLs: {invalid_urls}")

# Get platform statistics
stats = processor.get_platform_stats(valid_urls)
print(f"Platform stats: {stats}")
```

### Excel Metadata Management

```python
from core import ExcelMetadataManager

# Create Excel manager
excel_manager = ExcelMetadataManager(
    output_dir="downloads",
    filename="my_videos_metadata.xlsx"
)

# Add video metadata
video_info = {
    'id': '123456',
    'title': 'Example Video',
    'uploader': 'Example User',
    'duration': 30,
    # ... other metadata
}

excel_manager.add_video_metadata(video_info, "/path/to/video.mp4")

# Save Excel file
excel_manager.save_excel_file()

# Get file information
info = excel_manager.get_excel_info()
print(f"Excel file: {info['file_name']}")
print(f"Total rows: {info['total_rows']}")
```

### Context Manager Usage

```python
from core import DownloadManager

# Use as context manager for automatic cleanup
with DownloadManager(output_dir="downloads", platform="tiktok") as manager:
    # Download videos
    results = manager.download_multiple_videos(urls, export_to_excel=True)
    print(f"Downloaded {results['successful']} videos")

# Resources automatically cleaned up when exiting context
```

## 🔄 Backward Compatibility

The new modular architecture maintains backward compatibility with existing code:

```python
# Old way (still works)
from downloader.tiktok_downloader import TikTokDownloader

downloader = TikTokDownloader(output_dir="downloads", quality="best")
success = downloader.download_video("https://www.tiktok.com/@user/video/123")

# New way (recommended)
from core import DownloadManager

manager = DownloadManager(output_dir="downloads", quality="best", platform="tiktok")
result = manager.download_single_video("https://www.tiktok.com/@user/video/123")
```

## 🧪 Testing the New Architecture

Run the example script to test all components:

```bash
python example_modular_usage.py
```

This will demonstrate:
- Basic video downloads
- Batch downloads
- URL processing
- Excel management
- Backward compatibility
- Context manager usage

## 📁 File Structure

```
project_root/
├── core/                           # Core modular components
│   ├── __init__.py                # Module exports
│   ├── video_downloader.py        # Core video downloader
│   ├── tiktok_downloader.py       # TikTok-specific downloader
│   ├── excel_metadata_manager.py  # Excel metadata management
│   ├── url_processor.py           # URL processing
│   └── download_manager.py        # Main orchestrator
├── downloader/                     # Legacy downloader (backward compatible)
│   ├── tiktok_downloader.py       # Updated to use core modules
│   └── tiktok_gui.py             # Updated GUI
├── utils/                         # Utility modules
│   └── excel_loader.py            # Excel loading utilities
├── example_modular_usage.py       # Example usage script
└── MODULAR_ARCHITECTURE_README.md # This file
```

## 🎯 Benefits of the New Architecture

1. **Modularity**: Each component has a single responsibility
2. **Reusability**: Components can be used independently
3. **Maintainability**: Easier to fix bugs and add features
4. **Testability**: Each component can be tested separately
5. **Extensibility**: Easy to add support for new platforms
6. **Backward Compatibility**: Existing code continues to work
7. **Clean Separation**: Clear boundaries between different concerns

## 🔮 Future Enhancements

The modular architecture makes it easy to add new features:

- **Multi-platform Support**: Add downloaders for YouTube, Instagram, etc.
- **Advanced Metadata**: Support for more metadata formats
- **Database Integration**: Replace Excel with database storage
- **API Interface**: REST API for remote downloads
- **Plugin System**: Allow third-party extensions

## 🚨 Important Notes

1. **Dependencies**: Make sure `yt-dlp` and `openpyxl` are installed
2. **Python Path**: The core module must be in the Python path
3. **Error Handling**: All components include proper error handling and logging
4. **Thread Safety**: Components are designed to be thread-safe
5. **Resource Management**: Use context managers for automatic cleanup

## 📞 Support

If you encounter issues with the new modular architecture:

1. Check that all dependencies are installed
2. Verify the Python path includes the project root
3. Run the example script to test basic functionality
4. Check the logs for detailed error information
5. Ensure you're using the correct import statements

The new architecture provides a solid foundation for future development while maintaining compatibility with existing code.
