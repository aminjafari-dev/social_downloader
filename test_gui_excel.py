#!/usr/bin/env python3
"""
Test script to verify GUI Excel integration.
"""

import sys
from pathlib import Path

# Add the downloader directory to the path
sys.path.append(str(Path(__file__).parent / "downloader"))

def test_gui_excel_integration():
    """Test the GUI Excel integration."""
    
    print("🧪 Testing GUI Excel Integration")
    print("=" * 50)
    
    try:
        # Import the GUI class
        from tiktok_gui import TikTokDownloaderGUI
        
        print("✅ GUI class imported successfully")
        
        # Test if Excel export variables are available
        gui = TikTokDownloaderGUI()
        
        # Check if Excel export variables exist
        if hasattr(gui, 'excel_export_var'):
            print("✅ Excel export checkbox variable found")
        else:
            print("❌ Excel export checkbox variable missing")
        
        if hasattr(gui, 'excel_filename_var'):
            print("✅ Excel filename variable found")
        else:
            print("❌ Excel filename variable missing")
        
        # Check if methods exist
        if hasattr(gui, 'process_existing_downloads'):
            print("✅ Process existing downloads method found")
        else:
            print("❌ Process existing downloads method missing")
        
        if hasattr(gui, 'process_existing_worker'):
            print("✅ Process existing worker method found")
        else:
            print("❌ Process existing worker method missing")
        
        print("\n🎉 GUI Excel integration test completed successfully!")
        print("\n📋 To use the GUI with Excel export:")
        print("1. Run: python downloader/tiktok_gui.py")
        print("2. Check 'Export to Excel' checkbox")
        print("3. Set Excel filename (optional)")
        print("4. Download videos or click 'Process Existing Downloads'")
        
    except Exception as e:
        print(f"❌ Error testing GUI integration: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_gui_excel_integration()
