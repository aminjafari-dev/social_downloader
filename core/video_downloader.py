"""
Core Video Downloader Module

This module provides the core functionality for downloading videos using yt-dlp.
It's designed to be framework-agnostic and can be used by both GUI and CLI applications.

Usage:
    from core.video_downloader import VideoDownloader
    
    downloader = VideoDownloader(output_dir="downloads", quality="best")
    success = downloader.download_video("https://example.com/video")
"""

import os
import logging
import yt_dlp
from pathlib import Path
from typing import Optional, Dict, Any, List
from datetime import datetime

# Configure logging
logger = logging.getLogger(__name__)


class VideoDownloader:
    """
    Core video downloader class that handles video downloads using yt-dlp.
    
    This class is responsible for:
    - Configuring yt-dlp options
    - Downloading videos
    - Extracting video information
    - Managing download paths and naming
    
    Attributes:
        output_dir (Path): Directory where downloaded videos will be saved
        quality (str): Preferred video quality ('best', 'worst', '720p', etc.)
        extract_audio (bool): Whether to extract audio only
        add_metadata (bool): Whether to add metadata to downloaded files
        custom_base_name (str): Custom base name for video files
        video_counter (int): Counter for video numbering
        ydl_opts (Dict): yt-dlp configuration options
    """
    
    def __init__(self, output_dir: str = "downloads", quality: str = "best", 
                 extract_audio: bool = False, add_metadata: bool = True,
                 custom_base_name: str = None):
        """
        Initialize the video downloader with specified options.
        
        Args:
            output_dir (str): Directory to save downloaded videos (default: "downloads")
            quality (str): Preferred video quality (default: "best")
            extract_audio (bool): Extract audio only if True (default: False)
            add_metadata (bool): Add metadata to downloaded files (default: True)
            custom_base_name (str): Custom base name for video files (default: None)
        """
        self.output_dir = Path(output_dir)
        self.quality = quality
        self.extract_audio = extract_audio
        self.add_metadata = add_metadata
        self.custom_base_name = custom_base_name
        self.video_counter = 1
        
        # Create output directory if it doesn't exist
        self.output_dir.mkdir(exist_ok=True)
        
        # Configure yt-dlp options
        self.ydl_opts = self._configure_ydl_options()
        
        logger.info(f"VideoDownloader initialized with output_dir: {self.output_dir}, quality: {self.quality}")
    
    def _configure_ydl_options(self) -> Dict[str, Any]:
        """
        Configure yt-dlp options based on user preferences.
        
        Returns:
            Dict[str, Any]: Configured yt-dlp options dictionary
        """
        options = {
            'outtmpl': str(self.output_dir / self._get_custom_filename()),
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
        
        logger.debug(f"Configured yt-dlp options: {options}")
        return options
    
    def _get_custom_filename(self) -> str:
        """
        Generate custom filename for videos.
        
        Returns:
            str: Custom filename template
        """
        if self.custom_base_name:
            filename = f"{self.custom_base_name}__{self.video_counter}.%(ext)s"
            self.video_counter += 1
            return filename
        else:
            return '%(title)s.%(ext)s'
    
    def reset_video_counter(self):
        """Reset the video counter for new batch downloads."""
        self.video_counter = self.find_next_video_number()
        logger.info(f"Video counter reset to: {self.video_counter}")
    
    def find_next_video_number(self) -> int:
        """
        Find the next available video number by checking existing files.
        
        Returns:
            int: Next available video number
        """
        if not self.custom_base_name:
            return 1
        
        # Check existing files in output directory
        existing_files = list(self.output_dir.glob(f"{self.custom_base_name}__*.*"))
        if existing_files:
            max_number = 0
            for file in existing_files:
                import re
                match = re.search(rf'{re.escape(self.custom_base_name)}__(\d+)', file.name)
                if match:
                    max_number = max(max_number, int(match.group(1)))
            next_number = max_number + 1
            logger.info(f"Found existing files, next video number: {next_number}")
            return next_number
        
        logger.info("No existing files found, starting from 1")
        return 1
    
    def validate_url(self, url: str) -> bool:
        """
        Validate if the provided URL is a valid video URL.
        
        Args:
            url (str): The URL to validate
            
        Returns:
            bool: True if URL is valid, False otherwise
        """
        if not url or not url.strip():
            return False
        
        # Basic URL validation
        try:
            import urllib.parse
            parsed = urllib.parse.urlparse(url.strip())
            return bool(parsed.scheme and parsed.netloc)
        except Exception:
            return False
    
    def get_video_info(self, url: str) -> Optional[Dict[str, Any]]:
        """
        Extract video information without downloading.
        
        Args:
            url (str): Video URL
            
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
        Download a video from the provided URL.
        
        Args:
            url (str): Video URL to download
            
        Returns:
            bool: True if download successful, False otherwise
        """
        if not self.validate_url(url):
            logger.error(f"Invalid URL: {url}")
            return False
        
        try:
            logger.info(f"Starting download for: {url}")
            
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                # Extract info first
                info = ydl.extract_info(url, download=False)
                if not info:
                    logger.error("Failed to extract video information")
                    return False
                
                logger.info(f"Video Title: {info.get('title', 'Unknown')}")
                logger.info(f"Duration: {info.get('duration', 'Unknown')} seconds")
                logger.info(f"Uploader: {info.get('uploader', 'Unknown')}")
                
                # Download the video
                ydl.download([url])
                
                logger.info("Download completed successfully")
                return True
                
        except yt_dlp.DownloadError as e:
            logger.error(f"Download error: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error during download: {e}")
            return False
    
    def download_multiple_videos(self, urls: List[str]) -> Dict[str, bool]:
        """
        Download multiple videos from a list of URLs.
        
        Args:
            urls (List[str]): List of video URLs
            
        Returns:
            Dict[str, bool]: Dictionary mapping URLs to download success status
        """
        results = {}
        
        logger.info(f"Starting batch download of {len(urls)} videos...")
        
        for i, url in enumerate(urls, 1):
            logger.info(f"[{i}/{len(urls)}] Processing: {url}")
            results[url] = self.download_video(url)
        
        # Print summary
        successful = sum(results.values())
        logger.info(f"Batch download completed! Successful: {successful}/{len(urls)}")
        
        return results
    
    def update_settings(self, output_dir: str = None, quality: str = None, 
                       extract_audio: bool = None, add_metadata: bool = None,
                       custom_base_name: str = None):
        """
        Update downloader settings and reconfigure yt-dlp options.
        
        Args:
            output_dir (str): New output directory
            quality (str): New quality setting
            extract_audio (bool): New audio-only setting
            add_metadata (bool): New metadata setting
            custom_base_name (str): New custom base name
        """
        if output_dir is not None:
            self.output_dir = Path(output_dir)
            self.output_dir.mkdir(exist_ok=True)
        
        if quality is not None:
            self.quality = quality
        
        if extract_audio is not None:
            self.extract_audio = extract_audio
        
        if add_metadata is not None:
            self.add_metadata = add_metadata
        
        if custom_base_name is not None:
            self.custom_base_name = custom_base_name
        
        # Reconfigure yt-dlp options
        self.ydl_opts = self._configure_ydl_options()
        logger.info("Downloader settings updated and yt-dlp options reconfigured")
