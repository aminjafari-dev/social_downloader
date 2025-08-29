# Quick Start Guide

Get up and running with TikTok Video Downloader in minutes!

## 🚀 Quick Installation

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Test the installation:**
   ```bash
   python test_installation.py
   ```

3. **You're ready to go!** 🎉

## 📖 Quick Usage

### Command Line (Fastest)

Download a single video:
```bash
python tiktok_downloader.py --url "https://www.tiktok.com/@user/video/1234567890"
```

### GUI (User-Friendly)

Open the graphical interface:
```bash
python tiktok_gui.py
```

### Examples

Run the example script to see all features:
```bash
python example.py
```

## 🎯 Common Use Cases

### Download Best Quality Video
```bash
python tiktok_downloader.py --url "YOUR_TIKTOK_URL"
```

### Download Audio Only
```bash
python tiktok_downloader.py --url "YOUR_TIKTOK_URL" --audio-only
```

### Download Multiple Videos
1. Create a file `urls.txt` with one URL per line
2. Run: `python tiktok_downloader.py --file urls.txt`

### Custom Quality
```bash
python tiktok_downloader.py --url "YOUR_TIKTOK_URL" --quality 720p
```

## 📁 Output

Videos are saved to the `downloads/` folder by default.

## ❓ Need Help?

- Check the full [README.md](README.md) for detailed documentation
- Run `python tiktok_downloader.py --help` for command options
- Use the GUI for a visual interface

## ⚠️ Important

- Only download videos you have permission to download
- Respect content creators' rights
- This tool is for personal use only
