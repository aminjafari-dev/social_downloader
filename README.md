# TikTok Video Downloader

A powerful and user-friendly Python application for downloading TikTok videos with both command-line and graphical interfaces.

## Features

- **Multiple Interface Options**: Command-line interface for power users and GUI for beginners
- **Batch Downloading**: Download multiple videos at once from a list of URLs
- **Quality Selection**: Choose from various video qualities (best, worst, 720p, 480p, 360p)
- **Audio Extraction**: Option to download audio only
- **Metadata Support**: Automatically extract and save video metadata
- **URL Validation**: Built-in validation for TikTok URLs
- **Progress Tracking**: Real-time progress updates and logging
- **Cross-Platform**: Works on Windows, macOS, and Linux

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Step 1: Clone or Download

```bash
git clone <repository-url>
cd social_downloader
```

Or download the files directly to your desired directory.

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Verify Installation

```bash
python tiktok_downloader.py --help
```

## Usage

### Command Line Interface

#### Single Video Download

```bash
# Basic download
python tiktok_downloader.py --url "https://www.tiktok.com/@user/video/1234567890"

# Download with specific quality
python tiktok_downloader.py --url "https://www.tiktok.com/@user/video/1234567890" --quality 720p

# Download audio only
python tiktok_downloader.py --url "https://www.tiktok.com/@user/video/1234567890" --audio-only

# Custom output directory
python tiktok_downloader.py --url "https://www.tiktok.com/@user/video/1234567890" --output-dir "my_videos"
```

#### Batch Download

Create a text file (e.g., `urls.txt`) with one TikTok URL per line:

```
https://www.tiktok.com/@user1/video/1234567890
https://www.tiktok.com/@user2/video/0987654321
https://www.tiktok.com/@user3/video/1122334455
```

Then run:

```bash
python tiktok_downloader.py --file urls.txt
```

#### Command Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `--url` | Single TikTok video URL | - |
| `--file` | Text file containing URLs (one per line) | - |
| `--output-dir` | Output directory for downloaded videos | `downloads` |
| `--quality` | Video quality preference | `best` |
| `--audio-only` | Download audio only (no video) | False |
| `--no-metadata` | Skip metadata extraction | False |

### Graphical User Interface

For users who prefer a graphical interface:

```bash
python tiktok_gui.py
```

#### GUI Features

- **Single/Batch Mode**: Toggle between single URL and batch processing
- **Clipboard Integration**: Paste URLs directly from clipboard
- **File Browser**: Browse for output directory
- **Real-time Logging**: See download progress and status
- **Quality Selection**: Dropdown menu for quality options
- **Options Panel**: Configure audio-only, metadata, and other settings

## Supported URL Formats

The downloader supports various TikTok URL formats:

- `https://www.tiktok.com/@username/video/1234567890`
- `https://vm.tiktok.com/xxxxx/`
- `https://vt.tiktok.com/xxxxx/`
- `https://tiktok.com/@username/video/1234567890`

## Output Structure

Downloaded videos are saved with the following structure:

```
downloads/
├── video_title.mp4              # Main video file
├── video_title.jpg              # Thumbnail (if metadata enabled)
├── video_title.description      # Video description (if metadata enabled)
└── video_title.info.json        # Complete metadata (if metadata enabled)
```

## Error Handling

The application includes comprehensive error handling:

- **Invalid URLs**: Automatic validation and user feedback
- **Network Issues**: Graceful handling of connection problems
- **File System Errors**: Proper handling of permission and disk space issues
- **Download Failures**: Detailed error messages and logging

## Logging

All operations are logged to both console and file:

- **Console Output**: Colored output for immediate feedback
- **Log File**: `tiktok_downloader.log` for detailed debugging
- **GUI Log**: Real-time log display in the graphical interface

## Troubleshooting

### Common Issues

1. **"Module not found" errors**
   ```bash
   pip install -r requirements.txt
   ```

2. **Download fails with "Video unavailable"**
   - Check if the video is still available on TikTok
   - Verify the URL is correct and accessible
   - Some videos may be region-restricted

3. **Permission errors**
   - Ensure you have write permissions to the output directory
   - Try running as administrator (Windows) or with sudo (Linux/macOS)

4. **GUI doesn't start**
   - Ensure tkinter is installed: `python -m tkinter`
   - On Linux: `sudo apt-get install python3-tk`

### Performance Tips

- Use batch mode for multiple downloads
- Choose appropriate quality settings to balance speed and file size
- Close other applications to free up system resources
- Use SSD storage for faster write speeds

## Legal and Ethical Considerations

⚠️ **Important**: Please respect copyright laws and TikTok's Terms of Service:

- Only download videos you have permission to download
- Respect content creators' rights
- Do not use downloaded content for commercial purposes without permission
- This tool is for personal use and educational purposes only

## Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.

### Development Setup

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - The powerful video downloader library
- [colorama](https://github.com/tartley/colorama) - Cross-platform colored terminal text
- [tkinter](https://docs.python.org/3/library/tkinter.html) - Python's standard GUI library

## Support

If you encounter any issues or have questions:

1. Check the troubleshooting section above
2. Review the log files for detailed error information
3. Open an issue on the project repository
4. Ensure you're using the latest version of the application

## Version History

- **v1.0.0**: Initial release with CLI and GUI interfaces
- Basic video downloading functionality
- Batch processing support
- Quality and format options
- Comprehensive error handling and logging
