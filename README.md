# Social Downloader

A comprehensive Python application for downloading videos from social media platforms and removing text overlays using AI/ML technology.

## 🚀 Features

- **Video Downloading**: Download videos from TikTok and other social media platforms
- **Text Removal**: AI-powered text overlay removal from videos
- **GUI Applications**: User-friendly graphical interfaces for both downloading and text removal
- **Interactive Tools**: Interactive text removal with real-time preview
- **Batch Processing**: Process multiple videos efficiently

## 📁 Project Structure

```
social_downloader/
├── main.py                 # Main entry point for the application
├── requirements.txt        # Python dependencies
├── .gitignore             # Git ignore file
├── .DS_Store              # macOS system file
│
├── downloader/            # Video downloading functionality
│   ├── __init__.py
│   ├── tiktok_downloader.py  # Core TikTok downloader
│   └── tiktok_gui.py         # GUI for video downloads
│
├── text_remover/          # Text removal functionality
│   ├── __init__.py
│   ├── video_text_remover.py      # Core text removal
│   ├── text_remover_gui.py        # GUI for text removal
│   └── interactive_text_remover.py # Interactive text remover
│
├── core/                  # Shared utilities and core functionality
│   ├── __init__.py
│   ├── example.py             # Example usage and demonstrations
│   └── tiktok_downloader.log  # Application logs
│
├── gui/                   # GUI utilities and shared components
│   └── __init__.py
│
├── tests/                 # Test files and testing utilities
│   ├── __init__.py
│   └── test_installation.py  # Installation and dependency tests
│
├── docs/                  # Documentation files
│   ├── README.md              # Main documentation (this file)
│   ├── QUICKSTART.md          # Quick start guide
│   └── INTERACTIVE_GUIDE.md   # Interactive tool guide
│
├── downloads/             # Downloaded and processed content
│   ├── original/          # Original downloaded videos
│   ├── processed/         # Videos with text removed
│   └── metadata/          # Video metadata (JSON, descriptions, images)
│
└── models/                # AI/ML models (currently empty)
```

## 🛠️ Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd social_downloader
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Test installation**:
   ```bash
   python tests/test_installation.py
   ```

## 🚀 Quick Start

### Using the Main Application

The application provides a unified command-line interface through `main.py`:

```bash
# Show help
python main.py --help

# Download a video
python main.py downloader --url "https://tiktok.com/..." --output downloads/original/

# Remove text from a video
python main.py text-remover --input video.mp4 --output processed_video.mp4

# Launch GUI applications
python main.py gui --type downloader
python main.py gui --type text-remover
```

### Direct Module Usage

You can also run individual modules directly:

#### Video Downloader
```bash
# Command line download
python downloader/tiktok_downloader.py

# GUI downloader
python downloader/tiktok_gui.py
```

#### Text Remover
```bash
# Command line text removal
python text_remover/video_text_remover.py

# GUI text remover
python text_remover/text_remover_gui.py

# Interactive text remover
python text_remover/interactive_text_remover.py
```

## 📖 Documentation

- **[Quick Start Guide](docs/QUICKSTART.md)**: Get up and running quickly
- **[Interactive Guide](docs/INTERACTIVE_GUIDE.md)**: Learn to use the interactive text remover
- **[Core Examples](core/example.py)**: See example usage patterns

## 🎯 Usage Examples

### Downloading Videos

```python
from downloader.tiktok_downloader import download_video

# Download a TikTok video
download_video("https://tiktok.com/@user/video/123456789", "downloads/original/")
```

### Removing Text from Videos

```python
from text_remover.video_text_remover import remove_text_from_video

# Remove text overlays from a video
remove_text_from_video("input_video.mp4", "output_video.mp4")
```

## 🔧 Configuration

### Download Settings
- Default download directory: `downloads/original/`
- Supported platforms: TikTok (expandable to other platforms)
- Automatic metadata extraction

### Text Removal Settings
- AI/ML model-based text detection
- Configurable confidence thresholds
- Support for various text overlay types

## 🧪 Testing

Run the test suite to ensure everything is working correctly:

```bash
python tests/test_installation.py
```

## 📝 Logging

Application logs are stored in `core/tiktok_downloader.log` and provide detailed information about:
- Download progress and status
- Text removal operations
- Error messages and debugging information

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

If you encounter any issues:

1. Check the [documentation](docs/)
2. Review the [examples](core/example.py)
3. Check the [logs](core/tiktok_downloader.log)
4. Open an issue on GitHub

## 🔄 Updates

Stay updated with the latest features and improvements by regularly pulling from the repository:

```bash
git pull origin main
pip install -r requirements.txt --upgrade
```

---

**Happy downloading and processing! 🎉**
