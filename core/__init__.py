"""
Core Module for Social Media Downloader

This module provides the core functionality for downloading videos from various social media platforms.
It includes modular components for video downloading, metadata management, and URL processing.

Main Components:
- VideoDownloader: Core video downloading functionality
- TikTokDownloader: TikTok-specific downloader
- ExcelMetadataManager: Excel metadata management
- URLProcessor: URL validation and processing
- DownloadManager: Main orchestrator for the download process

Usage:
    from core import DownloadManager
    
    manager = DownloadManager(output_dir="downloads", quality="best")
    results = manager.download_multiple_videos(urls)
"""

from .video_downloader import VideoDownloader
from .tiktok_downloader import TikTokDownloader
from .excel_metadata_manager import ExcelMetadataManager
from .url_processor import URLProcessor
from .download_manager import DownloadManager

__all__ = [
    'VideoDownloader',
    'TikTokDownloader', 
    'ExcelMetadataManager',
    'URLProcessor',
    'DownloadManager'
]

__version__ = "1.0.0"
__author__ = "Social Media Downloader Team"

