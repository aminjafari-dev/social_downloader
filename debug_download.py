#!/usr/bin/env python3
"""
Debug Script for Download Issues

This script tests the download functionality to identify any problems.
"""

import sys
import os
from pathlib import Path

# Add the project root to the Python path
sys.path.append(str(Path(__file__).parent))

def test_download_manager():
    """Test the DownloadManager functionality."""
    try:
        from core import DownloadManager
        print("✅ Successfully imported DownloadManager")
        
        # Create a download manager
        manager = DownloadManager(
            output_dir="downloads",
            quality="best",
            platform="tiktok"
        )
        print("✅ DownloadManager created successfully")
        
        # Test URL validation
        test_url = "https://www.tiktok.com/@example/video/1234567890"
        is_valid = manager.validate_url(test_url)
        print(f"✅ URL validation test: {test_url} -> {'Valid' if is_valid else 'Invalid'}")
        
        # Test batch text processing
        test_text = "https://www.tiktok.com/@user1/video/123\nhttps://www.tiktok.com/@user2/video/456"
        valid_urls, invalid_urls = manager.process_batch_text(test_text)
        print(f"✅ Batch text processing: {len(valid_urls)} valid, {len(invalid_urls)} invalid")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing DownloadManager: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_tiktok_downloader():
    """Test the TikTokDownloader functionality."""
    try:
        from downloader.tiktok_downloader import TikTokDownloader
        print("✅ Successfully imported TikTokDownloader")
        
        # Create a TikTok downloader
        downloader = TikTokDownloader(
            output_dir="downloads",
            quality="best"
        )
        print("✅ TikTokDownloader created successfully")
        
        # Test URL validation
        test_url = "https://www.tiktok.com/@example/video/1234567890"
        is_valid = downloader.validate_url(test_url)
        print(f"✅ TikTokDownloader URL validation: {test_url} -> {'Valid' if is_valid else 'Invalid'}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing TikTokDownloader: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_gui_url_processing():
    """Test the GUI URL processing logic."""
    try:
        # Simulate the GUI's get_urls method
        from core import DownloadManager
        
        manager = DownloadManager(output_dir="downloads", platform="tiktok")
        
        # Test single URL
        single_url = "https://www.tiktok.com/@example/video/1234567890"
        single_urls = [single_url] if single_url else []
        
        # Test batch URLs
        batch_text = "https://www.tiktok.com/@user1/video/123\nhttps://www.tiktok.com/@user2/video/456"
        batch_urls = batch_text.strip().split('\n')
        
        print(f"✅ Single URL test: {single_urls}")
        print(f"✅ Batch URLs test: {batch_urls}")
        
        # Process batch text
        valid_urls, invalid_urls = manager.process_batch_text('\n'.join(single_urls))
        print(f"✅ Single URL processing: {len(valid_urls)} valid, {len(invalid_urls)} invalid")
        
        valid_urls, invalid_urls = manager.process_batch_text('\n'.join(batch_urls))
        print(f"✅ Batch URL processing: {len(valid_urls)} valid, {len(invalid_urls)} invalid")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing GUI URL processing: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_actual_download():
    """Test an actual download (optional)."""
    try:
        from core import DownloadManager
        
        manager = DownloadManager(
            output_dir="downloads",
            quality="best",
            platform="tiktok"
        )
        
        # Test with a real TikTok URL (replace with actual URL)
        test_url = "https://www.tiktok.com/@example/video/1234567890"
        
        print(f"🔄 Testing download with URL: {test_url}")
        print("⚠️  Note: This will attempt to download a video. Replace with a real URL to test.")
        
        # Uncomment the line below to test actual download
        # result = manager.download_single_video(test_url, export_to_excel=False)
        # print(f"Download result: {result}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing actual download: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests."""
    print("🔍 Debugging Download Issues")
    print("=" * 50)
    
    tests = [
        ("DownloadManager", test_download_manager),
        ("TikTokDownloader", test_tiktok_downloader),
        ("GUI URL Processing", test_gui_url_processing),
        ("Actual Download", test_actual_download),
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        print(f"\n🧪 Testing {test_name}...")
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"❌ Test {test_name} failed with exception: {e}")
            results[test_name] = False
    
    print("\n📊 Test Results:")
    print("=" * 50)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
    
    all_passed = all(results.values())
    
    if all_passed:
        print("\n🎉 All tests passed! The download functionality should work.")
    else:
        print("\n⚠️  Some tests failed. Check the errors above.")
    
    print("\n💡 Next steps:")
    print("1. If all tests pass, try downloading a video in the GUI")
    print("2. If tests fail, check the error messages above")
    print("3. Make sure you have yt-dlp installed: pip install yt-dlp")
    print("4. Check that your TikTok URLs are valid and accessible")

if __name__ == "__main__":
    main()
