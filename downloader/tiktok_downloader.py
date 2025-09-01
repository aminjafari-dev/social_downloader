"""
TikTok Video Downloader Module

This module provides functionality to download TikTok videos using the new modular architecture.
It now uses the core modules for better organization and maintainability.

Usage:
    # Command line
    python tiktok_downloader.py --url "https://www.tiktok.com/@user/video/1234567890"
    
    # Programmatic
    from downloader.tiktok_downloader import TikTokDownloader
    downloader = TikTokDownloader()
    downloader.download_video("https://www.tiktok.com/@user/video/1234567890")
"""

import os
import sys
import logging
import argparse
from pathlib import Path
from typing import Optional, Dict, Any, List

# Import from core module
try:
    from core import DownloadManager
except ImportError:
    # Fallback for when running the file directly
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    from core import DownloadManager

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
    A class to handle TikTok video downloads using the new modular architecture.
    
    This class now acts as a wrapper around the core DownloadManager,
    providing backward compatibility while leveraging the new modular structure.
    
    Attributes:
        download_manager (DownloadManager): Core download manager instance
        output_dir (str): Directory where downloaded videos will be saved
        quality (str): Preferred video quality ('best', 'worst', '720p', etc.)
        extract_audio (bool): Whether to extract audio only
        add_metadata (bool): Whether to add metadata to downloaded files
        excel_file (str): Path to the Excel file for metadata export
    """
    
    def __init__(self, output_dir: str = "downloads", quality: str = "best", 
                 extract_audio: bool = False, add_metadata: bool = True, 
                 excel_file: str = None, custom_base_name: str = None):
        """
        Initialize the TikTok downloader with specified options.
        
        Args:
            output_dir (str): Directory to save downloaded videos (default: "downloads")
            quality (str): Preferred video quality (default: "best")
            extract_audio (bool): Extract audio only if True (default: False)
            add_metadata (bool): Add metadata to downloaded files (default: True)
            excel_file (str): Path to Excel file for metadata export (default: auto-generated)
            custom_base_name (str): Custom base name for video files (default: None)
        """
        # Initialize the core download manager
        self.download_manager = DownloadManager(
            output_dir=output_dir,
            quality=quality,
            extract_audio=extract_audio,
            add_metadata=add_metadata,
            custom_base_name=custom_base_name,
            platform="tiktok"
        )
        
        # Set Excel file path if specified
        if excel_file:
            self.download_manager.excel_manager.excel_file = Path(excel_file)
        
        # Backward compatibility attributes
        self.output_dir = self.download_manager.output_dir
        self.quality = self.download_manager.quality
        self.extract_audio = self.download_manager.extract_audio
        self.add_metadata = self.download_manager.add_metadata
        self.custom_base_name = self.download_manager.custom_base_name
        self.excel_file = self.download_manager.excel_manager.excel_file
        self.workbook = self.download_manager.excel_manager.workbook
        self.worksheet = self.download_manager.excel_manager.worksheet
        self.headers = self.download_manager.excel_manager.headers
        self.ydl_opts = self.download_manager.primary_downloader.ydl_opts
        
        logger.info(f"TikTokDownloader initialized with output_dir: {self.output_dir}, quality: {self.quality}")
    
    def validate_url(self, url: str) -> bool:
        """
        Validate if the provided URL is a valid TikTok URL.
        
        Args:
            url (str): The URL to validate
            
        Returns:
            bool: True if URL is valid, False otherwise
        """
        return self.download_manager.validate_url(url)
    
    def get_video_info(self, url: str) -> Optional[Dict[str, Any]]:
        """
        Extract video information without downloading.
        
        Args:
            url (str): TikTok video URL
            
        Returns:
            Optional[Dict[str, Any]]: Video information dictionary or None if failed
        """
        return self.download_manager.primary_downloader.get_video_info(url)
    
    def download_video(self, url: str) -> bool:
        """
        Download a TikTok video from the provided URL.
        
        Args:
            url (str): TikTok video URL to download
            
        Returns:
            bool: True if download successful, False otherwise
        """
        result = self.download_manager.download_single_video(url, export_to_excel=True)
        return result['success']
    
    def download_multiple_videos(self, urls: list) -> Dict[str, bool]:
        """
        Download multiple TikTok videos from a list of URLs.
        
        Args:
            urls (list): List of TikTok video URLs
            
        Returns:
            Dict[str, bool]: Dictionary mapping URLs to download success status
        """
        results = self.download_manager.download_multiple_videos(urls, export_to_excel=True)
        
        # Convert to backward-compatible format
        url_results = {}
        for result in results['results']:
            url_results[result['url']] = result['success']
        
        return url_results
    
    def save_excel_file(self):
        """Save the Excel file with all collected metadata."""
        return self.download_manager.excel_manager.save_excel_file()
    
    def process_existing_downloads(self):
        """
        Process existing downloaded videos and create Excel file from their metadata.
        This method reads existing .info.json files and adds them to the Excel.
        """
        result = self.download_manager.process_existing_downloads(export_to_excel=True)
        
        if result['processed'] > 0:
            print(f"Successfully processed {result['processed']} existing videos")
            print(f"Excel file saved: {result['excel_file']}")
        else:
            print("No existing downloads found to process")
    
    def is_url_already_downloaded(self, url: str) -> bool:
        """
        Check if a URL has already been downloaded by checking the Excel file.
        
        Args:
            url (str): The URL to check
            
        Returns:
            bool: True if URL already exists in Excel, False otherwise
        """
        return self.download_manager.primary_downloader.is_url_already_downloaded(
            url, self.download_manager.excel_manager.excel_file
        )
    
    def reset_video_counter(self):
        """Reset the video counter for new batch downloads."""
        if hasattr(self.download_manager.primary_downloader, 'reset_video_counter'):
            self.download_manager.primary_downloader.reset_video_counter()
    
    def find_next_video_number(self) -> int:
        """
        Find the next available video number by checking existing files.
        
        Returns:
            int: Next available video number
        """
        if hasattr(self.download_manager.primary_downloader, 'find_next_video_number'):
            return self.download_manager.primary_downloader.find_next_video_number()
        return 1
    
    def _configure_ydl_options(self) -> Dict[str, Any]:
        """
        Configure yt-dlp options based on user preferences.
        
        Returns:
            Dict[str, Any]: Configured yt-dlp options dictionary
        """
        return self.download_manager.primary_downloader.ydl_opts
    
    def _get_custom_filename(self) -> str:
        """
        Generate custom filename for videos.
        
        Returns:
            str: Custom filename template
        """
        if hasattr(self.download_manager.primary_downloader, '_get_custom_filename'):
            return self.download_manager.primary_downloader._get_custom_filename()
        return '%(title)s.%(ext)s'
    
    def _setup_excel_headers(self):
        """Setup Excel worksheet with headers and formatting."""
        # This is now handled by the ExcelMetadataManager
        pass
    
    def _add_metadata_to_excel(self, info: Dict[str, Any], download_path: str = ""):
        """
        Add video metadata to Excel worksheet.
        
        Args:
            info (Dict[str, Any]): Video information dictionary
            download_path (str): Path where video was downloaded
        """
        self.download_manager.excel_manager.add_video_metadata(info, download_path)
    
    def _extract_metadata_for_excel(self, info: Dict[str, Any], download_path: str = "") -> List[Any]:
        """
        Extract metadata from video info for Excel export.
        
        Args:
            info (Dict[str, Any]): Video information dictionary
            download_path (str): Path where video was downloaded
            
        Returns:
            List[Any]: List of metadata values for Excel row
        """
        # This is now handled by the ExcelMetadataManager
        return []
    
    def update_settings(self, **kwargs):
        """
        Update downloader settings.
        
        Args:
            **kwargs: Settings to update
        """
        self.download_manager.update_settings(**kwargs)
        
        # Update backward compatibility attributes
        self.output_dir = self.download_manager.output_dir
        self.quality = self.download_manager.quality
        self.extract_audio = self.download_manager.extract_audio
        self.add_metadata = self.download_manager.add_metadata
        self.custom_base_name = self.download_manager.custom_base_name
        self.excel_file = self.download_manager.excel_manager.excel_file
        self.ydl_opts = self.download_manager.primary_downloader.ydl_opts


def main():
    """
    Main function to handle command-line interface.
    
    This function parses command-line arguments and initiates the download process.
    It supports single video downloads, batch downloads from a file, and various options.
    """
    parser = argparse.ArgumentParser(
        description="Download TikTok videos using the new modular architecture",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python tiktok_downloader.py --url "https://www.tiktok.com/@user/video/1234567890"
  python tiktok_downloader.py --file urls.txt --quality 720p
  python tiktok_downloader.py --url "https://tiktok.com/@user/video/1234567890" --audio-only
  python tiktok_downloader.py --process-existing
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
    url_group.add_argument(
        '--process-existing',
        action='store_true',
        help='Process existing downloaded videos and create Excel file from metadata'
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
    parser.add_argument(
        '--custom-name',
        type=str,
        help='Custom base name for video files'
    )
    
    args = parser.parse_args()
    
    # Initialize downloader
    downloader = TikTokDownloader(
        output_dir=args.output_dir,
        quality=args.quality,
        extract_audio=args.audio_only,
        add_metadata=not args.no_metadata,
        custom_base_name=args.custom_name
    )
    
    try:
        if args.url:
            # Single video download
            success = downloader.download_video(args.url)
            if success:
                # Save Excel file for single download
                downloader.save_excel_file()
            sys.exit(0 if success else 1)
        
        elif args.file:
            # Batch download from file
            if not os.path.exists(args.file):
                print(f"Error: File '{args.file}' not found")
                sys.exit(1)
            
            with open(args.file, 'r') as f:
                urls = [line.strip() for line in f if line.strip()]
            
            if not urls:
                print(f"Error: No valid URLs found in file")
                sys.exit(1)
            
            results = downloader.download_multiple_videos(urls)
            successful = sum(results.values())
            sys.exit(0 if successful == len(urls) else 1)
        
        elif args.process_existing:
            # Process existing downloads
            downloader.process_existing_downloads()
            sys.exit(0)
    
    except KeyboardInterrupt:
        print("\nDownload interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
