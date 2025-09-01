#!/usr/bin/env python3
"""
Test script to verify Excel metadata manager append functionality.

This script tests that the ExcelMetadataManager now properly appends new data
to existing Excel files instead of overwriting them.
"""

import sys
import os
from pathlib import Path

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from core.excel_metadata_manager import ExcelMetadataManager

def test_excel_append():
    """Test that Excel metadata manager appends data correctly."""
    print("Testing Excel metadata manager append functionality...")
    
    # Create test output directory
    test_dir = Path("test_excel_output")
    test_dir.mkdir(exist_ok=True)
    
    # Test data
    test_videos = [
        {
            'id': 'test_video_1',
            'title': 'Test Video 1',
            'description': 'This is test video 1 #test #video',
            'uploader': 'TestUser1',
            'uploader_id': 'user1',
            'channel': 'TestChannel1',
            'channel_id': 'channel1',
            'upload_date': '20240101',
            'duration': 120,
            'view_count': 1000,
            'like_count': 100,
            'comment_count': 50,
            'repost_count': 25,
            'webpage_url': 'https://tiktok.com/@testuser1/video/123456',
            'thumbnail': 'https://example.com/thumb1.jpg',
            'format': 'mp4',
            'filesize': 1024000,
            'width': 1920,
            'height': 1080,
            'ext': 'mp4'
        },
        {
            'id': 'test_video_2',
            'title': 'Test Video 2',
            'description': 'This is test video 2 #test #video2',
            'uploader': 'TestUser2',
            'uploader_id': 'user2',
            'channel': 'TestChannel2',
            'channel_id': 'channel2',
            'upload_date': '20240102',
            'duration': 180,
            'view_count': 2000,
            'like_count': 200,
            'comment_count': 75,
            'repost_count': 30,
            'webpage_url': 'https://tiktok.com/@testuser2/video/789012',
            'thumbnail': 'https://example.com/thumb2.jpg',
            'format': 'mp4',
            'filesize': 2048000,
            'width': 1920,
            'height': 1080,
            'ext': 'mp4'
        }
    ]
    
    excel_file = test_dir / "test_metadata.xlsx"
    
    # Test 1: Create new Excel file
    print("\n1. Creating new Excel file...")
    manager1 = ExcelMetadataManager(output_dir=str(test_dir), filename="test_metadata.xlsx")
    
    # Add first video
    manager1.add_video_metadata(test_videos[0], "downloads/test_video_1.mp4")
    manager1.save_excel_file()
    
    # Check file status
    status1 = manager1.get_file_status()
    print(f"   File status: {status1}")
    
    # Test 2: Load existing Excel file and add more data
    print("\n2. Loading existing Excel file and adding second video...")
    manager2 = ExcelMetadataManager(output_dir=str(test_dir), filename="test_metadata.xlsx")
    
    # Add second video
    manager2.add_video_metadata(test_videos[1], "downloads/test_video_2.mp4")
    manager2.save_excel_file()
    
    # Check file status
    status2 = manager2.get_file_status()
    print(f"   File status: {status2}")
    
    # Test 3: Try to add duplicate video (should be skipped)
    print("\n3. Trying to add duplicate video...")
    manager3 = ExcelMetadataManager(output_dir=str(test_dir), filename="test_metadata.xlsx")
    
    # Try to add the same video again
    manager3.add_video_metadata(test_videos[0], "downloads/test_video_1.mp4")
    manager3.save_excel_file()
    
    # Check final status
    status3 = manager3.get_file_status()
    print(f"   File status: {status3}")
    
    # Get Excel info
    info = manager3.get_excel_info()
    print(f"\nFinal Excel file info:")
    print(f"   File: {info['file_name']}")
    print(f"   Total rows: {info['total_rows']}")
    print(f"   Data rows: {info['data_rows']}")
    print(f"   File exists: {info['file_exists']}")
    
    # Cleanup
    manager3.close_workbook()
    
    print(f"\n✅ Test completed successfully!")
    print(f"   Excel file created at: {excel_file}")
    print(f"   Expected: 2 unique videos in the file")
    print(f"   Actual: {info['data_rows']} videos in the file")
    
    if info['data_rows'] == 2:
        print("   ✅ PASS: Excel file correctly appended new data without overwriting")
    else:
        print("   ❌ FAIL: Excel file did not append data correctly")

if __name__ == "__main__":
    test_excel_append()
