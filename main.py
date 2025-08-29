#!/usr/bin/env python3
"""
Social Downloader - Main Entry Point

This is the main entry point for the Social Downloader application.
It provides a command-line interface to access different modules:
- Video Downloader
- Text Remover
- GUI Applications

Usage:
    python main.py [module] [options]
    
Examples:
    python main.py downloader --help
    python main.py text-remover --help
    python main.py gui
"""

import sys
import argparse
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def main():
    """Main entry point for the Social Downloader application."""
    parser = argparse.ArgumentParser(
        description="Social Downloader - Download and process social media videos",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py downloader --url "https://tiktok.com/..." --output downloads/
  python main.py text-remover --input video.mp4 --output processed_video.mp4
  python main.py gui
        """
    )
    
    subparsers = parser.add_subparsers(dest='module', help='Available modules')
    
    # Downloader module
    downloader_parser = subparsers.add_parser('downloader', help='Download videos from social media platforms')
    downloader_parser.add_argument('--url', help='URL of the video to download')
    downloader_parser.add_argument('--output', default='downloads/original/', help='Output directory for downloads')
    downloader_parser.add_argument('--gui', action='store_true', help='Launch downloader GUI')
    
    # Text remover module
    text_remover_parser = subparsers.add_parser('text-remover', help='Remove text overlays from videos')
    text_remover_parser.add_argument('--input', help='Input video file path')
    text_remover_parser.add_argument('--output', help='Output video file path')
    text_remover_parser.add_argument('--gui', action='store_true', help='Launch text remover GUI')
    text_remover_parser.add_argument('--interactive', action='store_true', help='Launch interactive text remover')
    
    # GUI module
    gui_parser = subparsers.add_parser('gui', help='Launch GUI applications')
    gui_parser.add_argument('--type', choices=['downloader', 'text-remover', 'all'], 
                           default='all', help='Type of GUI to launch')
    
    args = parser.parse_args()
    
    if not args.module:
        parser.print_help()
        return
    
    try:
        if args.module == 'downloader':
            handle_downloader(args)
        elif args.module == 'text-remover':
            handle_text_remover(args)
        elif args.module == 'gui':
            handle_gui(args)
    except ImportError as e:
        print(f"Error: Could not import required module. {e}")
        print("Please ensure all dependencies are installed: pip install -r requirements.txt")
    except Exception as e:
        print(f"Error: {e}")

def handle_downloader(args):
    """Handle downloader module execution."""
    if args.gui:
        # Launch downloader GUI
        from downloader.tiktok_gui import main as gui_main
        gui_main()
    elif args.url:
        # Command line download
        from downloader.tiktok_downloader import download_video
        download_video(args.url, args.output)
    else:
        print("Please provide either --url for command line download or --gui for GUI mode")

def handle_text_remover(args):
    """Handle text remover module execution."""
    if args.gui:
        # Launch text remover GUI
        from text_remover.text_remover_gui import main as gui_main
        gui_main()
    elif args.interactive:
        # Launch interactive text remover
        from text_remover.interactive_text_remover import main as interactive_main
        interactive_main()
    elif args.input and args.output:
        # Command line text removal
        from text_remover.video_text_remover import remove_text_from_video
        remove_text_from_video(args.input, args.output)
    else:
        print("Please provide --input and --output for command line processing, or --gui/--interactive for GUI modes")

def handle_gui(args):
    """Handle GUI module execution."""
    if args.type == 'downloader':
        from downloader.tiktok_gui import main as gui_main
        gui_main()
    elif args.type == 'text-remover':
        from text_remover.text_remover_gui import main as gui_main
        gui_main()
    elif args.type == 'all':
        print("Launching all GUI applications...")
        print("Note: You may need to run them separately due to GUI limitations")
        print("Use: python main.py gui --type downloader")
        print("Use: python main.py gui --type text-remover")

if __name__ == "__main__":
    main()
