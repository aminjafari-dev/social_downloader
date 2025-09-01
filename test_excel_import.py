#!/usr/bin/env python3
"""
Test script to create a sample Excel file with TikTok URLs for testing the Excel import feature.
"""

import pandas as pd
import os

def create_test_excel_file():
    """Create a sample Excel file with TikTok URLs for testing."""
    
    # Sample TikTok URLs (these are example URLs - replace with real ones for testing)
    sample_urls = [
        "https://www.tiktok.com/@user1/video/1234567890123456789",
        "https://www.tiktok.com/@user2/video/9876543210987654321",
        "https://www.tiktok.com/@user3/video/5556667778889990001",
        "https://www.tiktok.com/@user4/video/1112223334445556667",
        "https://www.tiktok.com/@user5/video/9998887776665554443"
    ]
    
    # Create DataFrame with URLs and some additional data
    data = {
        'Title': ['Video 1', 'Video 2', 'Video 3', 'Video 4', 'Video 5'],
        'URL': sample_urls,
        'Description': ['First video', 'Second video', 'Third video', 'Fourth video', 'Fifth video'],
        'Category': ['Funny', 'Dance', 'Music', 'Comedy', 'Tutorial']
    }
    
    df = pd.DataFrame(data)
    
    # Create test Excel file
    excel_filename = "test_tiktok_urls.xlsx"
    df.to_excel(excel_filename, index=False)
    
    print(f"✅ Created test Excel file: {excel_filename}")
    print(f"📊 File contains {len(sample_urls)} sample TikTok URLs")
    print(f"📋 Columns: {list(df.columns)}")
    print("\n📝 Instructions for testing:")
    print("1. Run the GUI: python main.py")
    print("2. In the 'Excel File Import' section:")
    print("   - Click 'Browse' and select this file")
    print("   - Click 'Load Columns' to load column names")
    print("   - Select 'URL' column from dropdown")
    print("   - Click 'Preview URLs' to see the URLs")
    print("   - Click 'Download from Excel' to start downloading")
    
    return excel_filename

if __name__ == "__main__":
    create_test_excel_file()

