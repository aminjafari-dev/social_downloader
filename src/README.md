# TikTok Video Downloader - Clean Architecture

This is the clean, organized version of the TikTok Video Downloader application with a modular GUI architecture.

## Project Structure

```
src/
├── main.py                     # Main entry point
├── requirements.txt            # Python dependencies
├── .gitignore                 # Git ignore rules
├── core/                      # Core functionality
│   ├── __init__.py
│   ├── download_manager.py    # Main download orchestrator
│   ├── excel_metadata_manager.py  # Excel metadata handling
│   ├── video_downloader.py   # Core video downloader
│   ├── tiktok_downloader.py  # TikTok-specific downloader
│   └── url_processor.py      # URL validation and processing
├── downloader/                # GUI components
│   ├── __init__.py
│   ├── tiktok_gui_modular.py # Main modular GUI
│   └── components/            # GUI components
│       ├── __init__.py
│       ├── video_url_component.py      # URL input component
│       ├── batch_mode_component.py     # Batch processing component
│       ├── download_settings_component.py  # Settings component
│       ├── excel_integration_component.py  # Excel integration
│       ├── log_component.py           # Logging component
│       └── README.md                  # Components documentation
└── utils/                     # Utility functions
    ├── __init__.py
    ├── excel_loader.py        # Excel file loading utilities
    └── README.md              # Utils documentation
```

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application:**
   ```bash
   python main.py
   ```

## Features

- **Modular GUI Architecture**: Clean separation of concerns with reusable components
- **Single URL Download**: Download individual TikTok videos
- **Batch Processing**: Process multiple URLs at once
- **Excel Integration**: Import/export URLs and metadata via Excel
- **Configurable Settings**: Quality, output directory, metadata options
- **Real-time Logging**: Monitor download progress and status

## Architecture

The application follows a clean, modular architecture:

- **Core Layer**: Business logic for video downloading and metadata management
- **GUI Layer**: Component-based user interface with clear separation
- **Utils Layer**: Reusable utility functions for Excel and file operations

## Components

Each GUI component is self-contained and handles a specific aspect of the application:

- **VideoURLComponent**: Single URL input and validation
- **BatchModeComponent**: Multiple URL input and processing
- **DownloadSettingsComponent**: Download configuration options
- **ExcelIntegrationComponent**: Excel file import/export
- **LogComponent**: Progress tracking and status display

## Dependencies

- `tkinter`: GUI framework (built-in)
- `yt-dlp`: Video downloading engine
- `pandas`: Excel file processing
- `openpyxl`: Excel file format support

## Notes

- The application automatically creates a `downloads/` directory for video storage
- Excel files are generated with comprehensive metadata
- All downloads include video information and thumbnails
- The modular design makes it easy to extend and maintain
