#!/usr/bin/env python3
"""
TikTok Video Downloader - Main Entry Point

This is the main entry point for the TikTok Video Downloader application.
It provides a clean, organized way to run the modular GUI.

Usage:
    python main.py
"""

import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    """Main entry point for the TikTok Video Downloader application."""
    try:
        from downloader.tiktok_gui_modular import TikTokDownloaderModularGUI
        
        print("Starting TikTok Video Downloader - Modular Version...")
        app = TikTokDownloaderModularGUI()
        app.run()
        
    except ImportError as e:
        print(f"Import error: {e}")
        print("Please ensure all required modules are available.")
        sys.exit(1)
    except Exception as e:
        print(f"Failed to start application: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
