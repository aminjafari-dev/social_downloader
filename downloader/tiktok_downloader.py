"""
TikTok Video Downloader Module

This module provides functionality to download TikTok videos using yt-dlp.
It includes both command-line and programmatic interfaces for downloading videos.

Usage:
    # Command line
    python tiktok_downloader.py --url "https://www.tiktok.com/@user/video/1234567890"
    
    # Programmatic
    from tiktok_downloader import TikTokDownloader
    downloader = TikTokDownloader()
    downloader.download_video("https://www.tiktok.com/@user/video/1234567890")
"""

import os
import sys
import logging
import argparse
from pathlib import Path
from typing import Optional, Dict, Any
import yt_dlp
from colorama import init, Fore, Style

# Initialize colorama for cross-platform colored output
init(autoreset=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('tiktok_downloader.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


class TikTokDownloader:
    """
    A class to handle TikTok video downloads using yt-dlp.
    
    This class provides methods to download TikTok videos with various options
    including quality selection, output directory specification, and metadata extraction.
    
    Attributes:
        output_dir (str): Directory where downloaded videos will be saved
        quality (str): Preferred video quality ('best', 'worst', '720p', etc.)
        extract_audio (bool): Whether to extract audio only
        add_metadata (bool): Whether to add metadata to downloaded files
    """
    
    def __init__(self, output_dir: str = "downloads", quality: str = "best", 
                 extract_audio: bool = False, add_metadata: bool = True):
        """
        Initialize the TikTok downloader with specified options.
        
        Args:
            output_dir (str): Directory to save downloaded videos (default: "downloads")
            quality (str): Preferred video quality (default: "best")
            extract_audio (bool): Extract audio only if True (default: False)
            add_metadata (bool): Add metadata to downloaded files (default: True)
        """
        self.output_dir = Path(output_dir)
        self.quality = quality
        self.extract_audio = extract_audio
        self.add_metadata = add_metadata
        
        # Create output directory if it doesn't exist
        self.output_dir.mkdir(exist_ok=True)
        
        # Configure yt-dlp options
        self.ydl_opts = self._configure_ydl_options()
    
    def _configure_ydl_options(self) -> Dict[str, Any]:
        """
        Configure yt-dlp options based on user preferences.
        
        Returns:
            Dict[str, Any]: Configured yt-dlp options dictionary
        """
        options = {
            'outtmpl': str(self.output_dir / '%(title)s.%(ext)s'),
            'format': 'bestaudio/best' if self.extract_audio else self.quality,
            'writesubtitles': False,
            'writeautomaticsub': False,
            'ignoreerrors': False,
            'no_warnings': False,
            'quiet': False,
            'verbose': True,
        }
        
        # Add metadata options if enabled
        if self.add_metadata:
            options.update({
                'writethumbnail': True,
                'writedescription': True,
                'writeinfojson': True,
            })
        
        return options
    
    def validate_url(self, url: str) -> bool:
        """
        Validate if the provided URL is a valid TikTok URL.
        
        Args:
            url (str): The URL to validate
            
        Returns:
            bool: True if URL is valid, False otherwise
        """
        valid_domains = [
            'tiktok.com',
            'vm.tiktok.com',
            'vt.tiktok.com',
            'www.tiktok.com'
        ]
        
        try:
            import urllib.parse
            parsed = urllib.parse.urlparse(url)
            return any(domain in parsed.netloc for domain in valid_domains)
        except Exception:
            return False
    
    def get_video_info(self, url: str) -> Optional[Dict[str, Any]]:
        """
        Extract video information without downloading.
        
        Args:
            url (str): TikTok video URL
            
        Returns:
            Optional[Dict[str, Any]]: Video information dictionary or None if failed
        """
        try:
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                logger.info(f"Extracting info for: {url}")
                info = ydl.extract_info(url, download=False)
                return info
        except Exception as e:
            logger.error(f"Failed to extract video info: {e}")
            return None
    
    def download_video(self, url: str) -> bool:
        """
        Download a TikTok video from the provided URL.
        
        Args:
            url (str): TikTok video URL to download
            
        Returns:
            bool: True if download successful, False otherwise
        """
        if not self.validate_url(url):
            logger.error(f"Invalid TikTok URL: {url}")
            print(f"{Fore.RED}Error: Invalid TikTok URL provided{Style.RESET_ALL}")
            return False
        
        try:
            print(f"{Fore.CYAN}Starting download for: {url}{Style.RESET_ALL}")
            logger.info(f"Starting download for URL: {url}")
            
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                # Extract info first
                info = ydl.extract_info(url, download=False)
                if not info:
                    logger.error("Failed to extract video information")
                    return False
                
                print(f"{Fore.GREEN}Video Title: {info.get('title', 'Unknown')}{Style.RESET_ALL}")
                print(f"{Fore.GREEN}Duration: {info.get('duration', 'Unknown')} seconds{Style.RESET_ALL}")
                print(f"{Fore.GREEN}Uploader: {info.get('uploader', 'Unknown')}{Style.RESET_ALL}")
                
                # Download the video
                ydl.download([url])
                
                print(f"{Fore.GREEN}Download completed successfully!{Style.RESET_ALL}")
                logger.info("Download completed successfully")
                return True
                
        except yt_dlp.DownloadError as e:
            logger.error(f"Download error: {e}")
            print(f"{Fore.RED}Download failed: {e}{Style.RESET_ALL}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error during download: {e}")
            print(f"{Fore.RED}Unexpected error: {e}{Style.RESET_ALL}")
            return False
    
    def download_multiple_videos(self, urls: list) -> Dict[str, bool]:
        """
        Download multiple TikTok videos from a list of URLs.
        
        Args:
            urls (list): List of TikTok video URLs
            
        Returns:
            Dict[str, bool]: Dictionary mapping URLs to download success status
        """
        results = {}
        
        print(f"{Fore.YELLOW}Starting batch download of {len(urls)} videos...{Style.RESET_ALL}")
        
        for i, url in enumerate(urls, 1):
            print(f"\n{Fore.CYAN}[{i}/{len(urls)}] Processing: {url}{Style.RESET_ALL}")
            results[url] = self.download_video(url)
        
        # Print summary
        successful = sum(results.values())
        print(f"\n{Fore.GREEN}Batch download completed!{Style.RESET_ALL}")
        print(f"{Fore.GREEN}Successful: {successful}/{len(urls)}{Style.RESET_ALL}")
        
        return results


def main():
    """
    Main function to handle command-line interface.
    
    This function parses command-line arguments and initiates the download process.
    It supports single video downloads, batch downloads from a file, and various options.
    """
    parser = argparse.ArgumentParser(
        description="Download TikTok videos using yt-dlp",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python tiktok_downloader.py --url "https://www.tiktok.com/@user/video/1234567890"
  python tiktok_downloader.py --file urls.txt --quality 720p
  python tiktok_downloader.py --url "https://tiktok.com/@user/video/1234567890" --audio-only
        """
    )
    
    # URL input options
    url_group = parser.add_mutually_exclusive_group(required=True)
    url_group.add_argument(
        '--url', 
        type=str, 
        help='Single TikTok video URL to download'
    )
    url_group.add_argument(
        '--file', 
        type=str, 
        help='Text file containing TikTok URLs (one per line)'
    )
    
    # Download options
    parser.add_argument(
        '--output-dir', 
        type=str, 
        default='downloads',
        help='Output directory for downloaded videos (default: downloads)'
    )
    parser.add_argument(
        '--quality', 
        type=str, 
        default='best',
        help='Video quality preference (default: best)'
    )
    parser.add_argument(
        '--audio-only', 
        action='store_true',
        help='Download audio only (no video)'
    )
    parser.add_argument(
        '--no-metadata', 
        action='store_true',
        help='Skip metadata extraction'
    )
    
    args = parser.parse_args()
    
    # Initialize downloader
    downloader = TikTokDownloader(
        output_dir=args.output_dir,
        quality=args.quality,
        extract_audio=args.audio_only,
        add_metadata=not args.no_metadata
    )
    
    try:
        if args.url:
            # Single video download
            success = downloader.download_video(args.url)
            sys.exit(0 if success else 1)
        
        elif args.file:
            # Batch download from file
            if not os.path.exists(args.file):
                print(f"{Fore.RED}Error: File '{args.file}' not found{Style.RESET_ALL}")
                sys.exit(1)
            
            with open(args.file, 'r') as f:
                urls = [line.strip() for line in f if line.strip()]
            
            if not urls:
                print(f"{Fore.RED}Error: No valid URLs found in file{Style.RESET_ALL}")
                sys.exit(1)
            
            results = downloader.download_multiple_videos(urls)
            successful = sum(results.values())
            sys.exit(0 if successful == len(urls) else 1)
    
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Download interrupted by user{Style.RESET_ALL}")
        sys.exit(1)
    except Exception as e:
        print(f"{Fore.RED}Unexpected error: {e}{Style.RESET_ALL}")
        sys.exit(1)


if __name__ == "__main__":
    main()
