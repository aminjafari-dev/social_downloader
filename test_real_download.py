#!/usr/bin/env python3
"""
Test script to test the actual download process with a real TikTok URL.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'downloader'))

from tiktok_downloader import TikTokDownloader
from pathlib import Path

def test_real_download():
    """Test the actual download process with a real TikTok URL."""
    
    print("🧪 Testing Real Download Process")
    print("=" * 50)
    
    # Initialize downloader
    downloader = TikTokDownloader(
        output_dir="downloads",
        quality="best",
        extract_audio=False,
        add_metadata=True
    )
    
    # Set custom base name
    downloader.custom_base_name = "real_test"
    
    # Test with a real TikTok URL (replace with a real one)
    # You can get a real TikTok URL from any TikTok video
    test_url = "https://www.tiktok.com/@tiktok/video/1234567890123456789"  # Replace with real URL
    
    print(f"📊 Testing with URL: {test_url}")
    print(f"🎯 Custom base name: {downloader.custom_base_name}")
    print(f"📁 Output directory: {downloader.output_dir}")
    print(f"📄 Excel file: {downloader.excel_file}")
    
    # Reset video counter
    print("\n🔄 Resetting video counter...")
    downloader.reset_video_counter()
    print(f"📊 Video counter after reset: {downloader.video_counter}")
    
    # Check if URL is valid
    print("\n🔍 Validating URL...")
    is_valid = downloader.validate_url(test_url)
    print(f"✅ URL valid: {is_valid}")
    
    if not is_valid:
        print("❌ Invalid URL, please provide a real TikTok URL")
        return
    
    # Check if already downloaded
    print("\n🔍 Checking if already downloaded...")
    already_downloaded = downloader.is_url_already_downloaded(test_url)
    print(f"📋 Already downloaded: {already_downloaded}")
    
    if already_downloaded:
        print("⏭️  URL already downloaded, skipping")
        return
    
    # Try to download
    print("\n🔄 Starting download...")
    try:
        success = downloader.download_video(test_url)
        if success:
            print("✅ Download successful!")
            print(f"📊 Video counter after download: {downloader.video_counter}")
            
            # Check if Excel file was created
            if downloader.excel_file.exists():
                print(f"✅ Excel file created: {downloader.excel_file}")
            else:
                print("❌ Excel file not created")
        else:
            print("❌ Download failed")
            
    except Exception as e:
        print(f"❌ Error during download: {e}")
    
    print("\n🎉 Real download test completed!")

if __name__ == "__main__":
    test_real_download()
