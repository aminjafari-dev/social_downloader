#!/usr/bin/env python3
"""
TikTok Video Downloader - Launcher Script

This script sets up the correct Python path and launches the modular GUI.
It works around the import issues without modifying the original code.

Usage:
    python run.py
"""

import sys
import os

# Add the current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Add the downloader directory to Python path for component imports
downloader_dir = os.path.join(current_dir, 'downloader')
sys.path.insert(0, downloader_dir)

# Add the core directory to Python path
core_dir = os.path.join(current_dir, 'core')
sys.path.insert(0, core_dir)

# Add the utils directory to Python path
utils_dir = os.path.join(current_dir, 'utils')
sys.path.insert(0, utils_dir)

def main():
    """Launch the TikTok Video Downloader application."""
    try:
        print("Setting up Python path...")
        print(f"Current directory: {current_dir}")
        print(f"Downloader directory: {downloader_dir}")
        print(f"Core directory: {core_dir}")
        print(f"Utils directory: {utils_dir}")
        
        print("\nStarting TikTok Video Downloader - Modular Version...")
        from downloader.tiktok_gui_modular import TikTokDownloaderModularGUI
        
        app = TikTokDownloaderModularGUI()
        app.run()
        
    except ImportError as e:
        print(f"Import error: {e}")
        print("Please ensure all required modules are available.")
        print(f"Python path: {sys.path}")
        sys.exit(1)
    except Exception as e:
        print(f"Failed to start application: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
