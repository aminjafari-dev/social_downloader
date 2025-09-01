#!/usr/bin/env python3
"""
Test script for TikTok downloader with Excel export functionality.

This script demonstrates how to use the enhanced TikTok downloader
to extract metadata and save it to Excel files.
"""

import sys
from pathlib import Path

# Add the downloader directory to the path
sys.path.append(str(Path(__file__).parent / "downloader"))

from tiktok_downloader import TikTokDownloader

def test_excel_export():
    """Test the Excel export functionality with existing downloads."""
    
    print("🧪 Testing TikTok Downloader Excel Export Functionality")
    print("=" * 60)
    
    # Initialize downloader
    downloader = TikTokDownloader(
        output_dir="downloads",
        quality="best",
        add_metadata=True
    )
    
    print(f"📁 Output directory: {downloader.output_dir}")
    print(f"📊 Excel file will be saved as: {downloader.excel_file}")
    print()
    
    # Process existing downloads
    print("🔄 Processing existing downloads...")
    downloader.process_existing_downloads()
    
    print("\n✅ Test completed!")
    print(f"📊 Check the Excel file: {downloader.excel_file}")

if __name__ == "__main__":
    test_excel_export()

