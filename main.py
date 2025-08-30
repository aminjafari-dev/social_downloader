#!/usr/bin/env python3
"""
TikTok Video Downloader - Main Application

This is the main entry point for the TikTok Video Downloader application.
It provides functionality for downloading TikTok videos from URLs.

Usage:
    python main.py --help
    python main.py download --url "https://tiktok.com/..."
    python main.py download-batch --file urls.txt
"""

import sys
import argparse
import logging
from pathlib import Path

# Add the downloader directory to the Python path
sys.path.append(str(Path(__file__).parent / "downloader"))

from downloader.tiktok_downloader import TikTokDownloader


def setup_logging():
    """Set up logging configuration."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('tiktok_downloader.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )


def main():
    """Main function to handle command-line interface."""
    parser = argparse.ArgumentParser(
        description="TikTok Video Downloader - Download TikTok videos from URLs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py download --url "https://tiktok.com/@user/video/123456789"
  python main.py download --url "https://tiktok.com/@user/video/123456789" --quality 720p
  python main.py download-batch --file urls.txt --output-dir downloads
        """
    )
    
    # Create subparsers for different commands
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Download command
    download_parser = subparsers.add_parser('download', help='Download a TikTok video')
    download_parser.add_argument('--url', '-u', required=True, help='TikTok video URL')
    download_parser.add_argument('--output-dir', default='downloads', help='Output directory')
    download_parser.add_argument('--quality', default='best', help='Video quality (best, 720p, 480p, etc.)')
    
    # Batch download command
    batch_parser = subparsers.add_parser('download-batch', help='Download multiple TikTok videos')
    batch_parser.add_argument('--file', '-f', required=True, help='File containing TikTok URLs (one per line)')
    batch_parser.add_argument('--output-dir', default='downloads', help='Output directory')
    batch_parser.add_argument('--quality', default='best', help='Video quality (best, 720p, 480p, etc.)')
    
    args = parser.parse_args()
    
    # Set up logging
    setup_logging()
    
    if args.command == 'download':
        print(f"Downloading video from: {args.url}")
        
        # Initialize downloader
        downloader = TikTokDownloader(output_dir=args.output_dir, quality=args.quality)
        
        try:
            # Download video
            success = downloader.download_video(args.url)
            
            if success:
                print(f"✅ Successfully downloaded video to: {args.output_dir}")
            else:
                print("❌ Failed to download video")
                sys.exit(1)
                
        except Exception as e:
            print(f"❌ Error during download: {e}")
            sys.exit(1)
    
    elif args.command == 'download-batch':
        print(f"Downloading videos from file: {args.file}")
        
        # Check if file exists
        if not Path(args.file).exists():
            print(f"❌ File not found: {args.file}")
            sys.exit(1)
        
        # Read URLs from file
        try:
            with open(args.file, 'r') as f:
                urls = [line.strip() for line in f if line.strip()]
        except Exception as e:
            print(f"❌ Error reading file: {e}")
            sys.exit(1)
        
        if not urls:
            print("❌ No URLs found in file")
            sys.exit(1)
        
        print(f"Found {len(urls)} URLs to download")
        
        # Initialize downloader
        downloader = TikTokDownloader(output_dir=args.output_dir, quality=args.quality)
        
        try:
            # Download videos
            results = downloader.download_multiple_videos(urls)
            
            successful = sum(results.values())
            print(f"✅ Successfully downloaded {successful}/{len(urls)} videos")
            
            # Show failed downloads
            failed_urls = [url for url, success in results.items() if not success]
            if failed_urls:
                print(f"❌ Failed downloads ({len(failed_urls)}):")
                for url in failed_urls:
                    print(f"  - {url}")
                
        except Exception as e:
            print(f"❌ Error during batch download: {e}")
            sys.exit(1)
    
    else:
        # No command specified, show help
        parser.print_help()


if __name__ == "__main__":
    main()

