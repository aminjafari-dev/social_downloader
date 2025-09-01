#!/usr/bin/env python3
"""
Test Script for Excel Download Functionality

This script demonstrates the new Excel download feature that processes each video individually:
1. Downloads the video first
2. Fetches its information/metadata
3. Adds metadata to Excel file
4. Moves to the next video

Usage:
    python test_excel_download.py
"""

import sys
import os
from pathlib import Path

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from core.download_manager import DownloadManager

def test_excel_download():
    """Test the new Excel download functionality."""
    print("Testing Excel Download Functionality")
    print("=" * 50)
    
    # Initialize download manager
    download_manager = DownloadManager(
        output_dir="test_downloads",
        quality="best",
        extract_audio=False,
        add_metadata=True,
        custom_base_name="test_excel",
        platform="tiktok"
    )
    
    # Test URLs (replace with actual TikTok URLs for testing)
    test_urls = [
        "https://www.tiktok.com/@example/video/1234567890123456789",
        "https://www.tiktok.com/@example/video/9876543210987654321",
        "https://www.tiktok.com/@example/video/5555555555555555555"
    ]
    
    print(f"Testing with {len(test_urls)} URLs")
    print("URLs:", test_urls)
    print()
    
    # Test the new Excel download method
    print("Testing download_videos_from_excel method...")
    
    def progress_callback(current, total, video_title):
        print(f"Progress: {current}/{total} - {video_title}")
    
    try:
        results = download_manager.download_videos_from_excel(
            test_urls,
            export_to_excel=True,
            progress_callback=progress_callback
        )
        
        print("\nDownload Results:")
        print(f"Total URLs: {results['total']}")
        print(f"Valid URLs: {results['valid_urls']}")
        print(f"Invalid URLs: {results['invalid_urls']}")
        print(f"Successful: {results['successful']}")
        print(f"Failed: {results['failed']}")
        print(f"Excel File: {results['excel_file']}")
        
        if results['excel_file']:
            print(f"\nExcel file created successfully at: {results['excel_file']}")
        
        # Show detailed results for each video
        print("\nDetailed Results:")
        for i, result in enumerate(results['results'], 1):
            print(f"\nVideo {i}:")
            print(f"  URL: {result['url']}")
            print(f"  Success: {result['success']}")
            print(f"  Step: {result['step']}")
            if result['error']:
                print(f"  Error: {result['error']}")
            if result['metadata']:
                title = result['metadata'].get('title', 'Unknown')
                print(f"  Title: {title}")
            if result['download_path']:
                print(f"  Download Path: {result['download_path']}")
        
    except Exception as e:
        print(f"Error during download: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Cleanup
        download_manager.cleanup()
        print("\nTest completed.")

if __name__ == "__main__":
    test_excel_download()
