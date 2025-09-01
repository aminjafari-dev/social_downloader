"""
Download Manager Module

This module orchestrates the entire download process by coordinating between
the video downloader, Excel metadata manager, and URL processor.

Usage:
    from core.download_manager import DownloadManager
    
    manager = DownloadManager(output_dir="downloads", quality="best")
    results = manager.download_videos(urls, export_to_excel=True)
"""

import logging
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime

from .video_downloader import VideoDownloader
from .tiktok_downloader import TikTokDownloader
from .excel_metadata_manager import ExcelMetadataManager
from .url_processor import URLProcessor

# Configure logging
logger = logging.getLogger(__name__)


class DownloadManager:
    """
    Orchestrates the entire download process.
    
    This class coordinates between:
    - Video downloader (core downloading functionality)
    - TikTok downloader (TikTok-specific features)
    - Excel metadata manager (metadata storage)
    - URL processor (URL validation and processing)
    
    Attributes:
        output_dir (Path): Directory for downloads
        quality (str): Video quality preference
        extract_audio (bool): Whether to extract audio only
        add_metadata (bool): Whether to add metadata
        custom_base_name (str): Custom base name for files
        video_downloader (VideoDownloader): Core video downloader
        tiktok_downloader (TikTokDownloader): TikTok-specific downloader
        excel_manager (ExcelMetadataManager): Excel metadata manager
        url_processor (URLProcessor): URL processing utility
    """
    
    def __init__(self, output_dir: str = "downloads", quality: str = "best", 
                 extract_audio: bool = False, add_metadata: bool = True,
                 custom_base_name: str = None, platform: str = "tiktok"):
        """
        Initialize the download manager.
        
        Args:
            output_dir (str): Directory for downloads (default: "downloads")
            quality (str): Video quality preference (default: "best")
            extract_audio (bool): Extract audio only if True (default: False)
            add_metadata (bool): Add metadata to files (default: True)
            custom_base_name (str): Custom base name for files (default: None)
            platform (str): Platform to download from (default: "tiktok")
        """
        self.output_dir = Path(output_dir)
        self.quality = quality
        self.extract_audio = extract_audio
        self.add_metadata = add_metadata
        self.custom_base_name = custom_base_name
        self.platform = platform.lower()
        
        # Create output directory
        self.output_dir.mkdir(exist_ok=True)
        
        # Initialize components
        self._initialize_components()
        
        logger.info(f"DownloadManager initialized for {platform} platform")
    
    def _initialize_components(self):
        """Initialize all required components."""
        # Initialize core video downloader
        self.video_downloader = VideoDownloader(
            output_dir=str(self.output_dir),
            quality=self.quality,
            extract_audio=self.extract_audio,
            add_metadata=self.add_metadata,
            custom_base_name=self.custom_base_name
        )
        
        # Initialize TikTok-specific downloader if needed
        if self.platform == "tiktok":
            self.tiktok_downloader = TikTokDownloader(
                output_dir=str(self.output_dir),
                quality=self.quality,
                extract_audio=self.extract_audio,
                add_metadata=self.add_metadata,
                custom_base_name=self.custom_base_name
            )
            # Use TikTok downloader as primary
            self.primary_downloader = self.tiktok_downloader
        else:
            # Use generic video downloader for other platforms
            self.primary_downloader = self.video_downloader
        
        # Initialize Excel metadata manager
        excel_filename = None
        if self.custom_base_name:
            excel_filename = f"{self.custom_base_name}__metadata.xlsx"
        
        self.excel_manager = ExcelMetadataManager(
            output_dir=str(self.output_dir),
            filename=excel_filename
        )
        
        # Initialize URL processor
        self.url_processor = URLProcessor()
        
        logger.debug("All components initialized successfully")
    
    def update_settings(self, **kwargs):
        """
        Update download manager settings.
        
        Args:
            **kwargs: Settings to update (output_dir, quality, extract_audio, etc.)
        """
        # Update local settings
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        
        # Update component settings
        if 'output_dir' in kwargs:
            self.output_dir = Path(kwargs['output_dir'])
            self.output_dir.mkdir(exist_ok=True)
        
        # Update downloader settings
        downloader_kwargs = {}
        for key in ['output_dir', 'quality', 'extract_audio', 'add_metadata', 'custom_base_name']:
            if key in kwargs:
                downloader_kwargs[key] = kwargs[key]
        
        if downloader_kwargs:
            self.primary_downloader.update_settings(**downloader_kwargs)
        
        # Update Excel manager if needed
        if 'output_dir' in kwargs or 'custom_base_name' in kwargs:
            excel_filename = None
            if self.custom_base_name:
                excel_filename = f"{self.custom_base_name}__metadata.xlsx"
            
            self.excel_manager = ExcelMetadataManager(
                output_dir=str(self.output_dir),
                filename=excel_filename
            )
        
        logger.info("Download manager settings updated")
    
    def validate_url(self, url: str) -> bool:
        """
        Validate if the provided URL is valid for the current platform.
        
        Args:
            url (str): The URL to validate
            
        Returns:
            bool: True if URL is valid, False otherwise
        """
        return self.url_processor.validate_url(url, self.platform)
    
    def validate_urls(self, urls: List[str]) -> List[str]:
        """
        Validate a list of URLs and return only valid ones.
        
        Args:
            urls (List[str]): List of URLs to validate
            
        Returns:
            List[str]: List of valid URLs only
        """
        valid_urls, _ = self.url_processor.validate_urls(urls, self.platform)
        return valid_urls
    
    def validate_urls_with_details(self, urls: List[str]) -> Tuple[List[str], List[str]]:
        """
        Validate URLs for the current platform and return both valid and invalid.
        
        Args:
            urls (List[str]): List of URLs to validate
            
        Returns:
            Tuple[List[str], List[str]]: (valid_urls, invalid_urls)
        """
        return self.url_processor.validate_urls(urls, self.platform)
    
    def process_batch_text(self, text: str) -> Tuple[List[str], List[str]]:
        """
        Process batch text containing URLs.
        
        Args:
            text (str): Text containing URLs
            
        Returns:
            Tuple[List[str], List[str]]: (valid_urls, invalid_urls)
        """
        return self.url_processor.process_batch_text(text, self.platform)
    
    def download_single_video(self, url: str, export_to_excel: bool = True) -> Dict[str, Any]:
        """
        Download a single video and optionally export metadata to Excel.
        
        Args:
            url (str): URL of the video to download
            export_to_excel (bool): Whether to export metadata to Excel (default: True)
            
        Returns:
            Dict[str, Any]: Download result information
        """
        result = {
            'url': url,
            'success': False,
            'error': None,
            'metadata': None,
            'download_path': None
        }
        
        try:
            # Validate URL
            if not self.primary_downloader.validate_url(url):
                result['error'] = f"Invalid {self.platform} URL: {url}"
                return result
            
            # Check if already downloaded
            if hasattr(self.primary_downloader, 'is_url_already_downloaded'):
                if self.primary_downloader.is_url_already_downloaded(url, self.excel_manager.excel_file):
                    result['success'] = True
                    result['error'] = "Video already downloaded"
                    return result
            
            # Get video info first
            info = self.primary_downloader.get_video_info(url)
            if not info:
                result['error'] = "Failed to extract video information"
                return result
            
            # Download the video
            success = self.primary_downloader.download_video(url)
            if not success:
                result['error'] = "Download failed"
                return result
            
            # Get download path
            if hasattr(self.primary_downloader, 'get_download_path'):
                download_path = self.primary_downloader.get_download_path(info)
            else:
                download_path = ""
            
            # Extract metadata
            if self.platform == "tiktok" and hasattr(self.primary_downloader, 'extract_tiktok_metadata'):
                metadata = self.primary_downloader.extract_tiktok_metadata(info)
            else:
                metadata = info
            
            # Export to Excel if requested
            if export_to_excel:
                self.excel_manager.add_video_metadata(info, download_path)
            
            result.update({
                'success': True,
                'metadata': metadata,
                'download_path': download_path
            })
            
            logger.info(f"Successfully downloaded video: {info.get('title', 'Unknown')}")
            
        except Exception as e:
            result['error'] = str(e)
            logger.error(f"Error downloading video {url}: {e}")
        
        return result
    
    def download_multiple_videos(self, urls: List[str], export_to_excel: bool = True) -> Dict[str, Any]:
        """
        Download multiple videos and optionally export metadata to Excel.
        
        Args:
            urls (List[str]): List of video URLs to download
            export_to_excel (bool): Whether to export metadata to Excel (default: True)
            
        Returns:
            Dict[str, Any]: Batch download results
        """
        if not urls:
            return {'total': 0, 'successful': 0, 'failed': 0, 'results': []}
        
        # Validate and clean URLs using the correct method
        valid_urls, invalid_urls = self.url_processor.validate_urls(urls, self.platform)
        
        if not valid_urls:
            return {
                'total': len(urls),
                'successful': 0,
                'failed': len(urls),
                'valid_urls': [],
                'invalid_urls': invalid_urls,
                'results': []
            }
        
        # Reset video counter for new batch
        if hasattr(self.primary_downloader, 'reset_video_counter'):
            self.primary_downloader.reset_video_counter()
        
        # Download videos
        results = []
        successful = 0
        failed = 0
        
        for i, url in enumerate(valid_urls, 1):
            logger.info(f"Processing video {i}/{len(valid_urls)}: {url}")
            
            result = self.download_single_video(url, export_to_excel)
            results.append(result)
            
            if result['success']:
                successful += 1
            else:
                failed += 1
        
        # Save Excel file if metadata was exported
        if export_to_excel and successful > 0:
            try:
                self.excel_manager.save_excel_file()
                logger.info(f"Excel metadata saved to: {self.excel_manager.excel_file}")
            except Exception as e:
                logger.error(f"Error saving Excel file: {e}")
        
        # Prepare summary
        summary = {
            'total': len(urls),
            'valid_urls': len(valid_urls),
            'invalid_urls': len(invalid_urls),
            'successful': successful,
            'failed': failed,
            'results': results,
            'excel_file': str(self.excel_manager.excel_file) if export_to_excel else None
        }
        
        logger.info(f"Batch download completed: {successful}/{len(valid_urls)} successful")
        return summary
    
    def process_existing_downloads(self, export_to_excel: bool = True) -> Dict[str, Any]:
        """
        Process existing downloaded videos and export metadata to Excel.
        
        Args:
            export_to_excel (bool): Whether to export metadata to Excel (default: True)
            
        Returns:
            Dict[str, Any]: Processing results
        """
        if not export_to_excel:
            return {'processed': 0, 'excel_file': None}
        
        try:
            processed_count = self.excel_manager.process_existing_downloads(
                str(self.output_dir), 
                self.custom_base_name
            )
            
            if processed_count > 0:
                self.excel_manager.save_excel_file()
                logger.info(f"Processed {processed_count} existing downloads")
            
            return {
                'processed': processed_count,
                'excel_file': str(self.excel_manager.excel_file)
            }
            
        except Exception as e:
            logger.error(f"Error processing existing downloads: {e}")
            return {'processed': 0, 'error': str(e), 'excel_file': None}
    
    def get_download_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the download process.
        
        Returns:
            Dict[str, Any]: Download statistics
        """
        stats = {
            'output_dir': str(self.output_dir),
            'platform': self.platform,
            'quality': self.quality,
            'extract_audio': self.extract_audio,
            'add_metadata': self.add_metadata,
            'custom_base_name': self.custom_base_name,
            'excel_file': str(self.excel_manager.excel_file),
            'excel_info': self.excel_manager.get_excel_info()
        }
        
        return stats
    
    def cleanup(self):
        """Clean up resources and close files."""
        try:
            self.excel_manager.close_workbook()
            logger.info("Download manager cleanup completed")
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.cleanup()
