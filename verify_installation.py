#!/usr/bin/env python3
"""
Social Downloader - Installation Verification Script

This script checks if all required packages are installed correctly
and verifies that the application can start properly.

Usage:
    python verify_installation.py
"""

import sys
import importlib
import os

def check_python_version():
    """Check if Python version is compatible."""
    print("Checking Python version...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print(f"❌ Python {version.major}.{version.minor} is not supported.")
        print("Please install Python 3.7 or higher.")
        return False
    else:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible.")
        return True

def check_required_packages():
    """Check if all required packages are installed."""
    print("\nChecking required packages...")
    
    required_packages = [
        'yt_dlp',
        'requests',
        'colorama',
        'selenium',
        'webdriver_manager',
        'openpyxl',
        'fake_useragent',
        'cv2',  # opencv-python
        'numpy',
        'PIL',  # pillow
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            importlib.import_module(package)
            print(f"✅ {package} is installed.")
        except ImportError:
            print(f"❌ {package} is missing.")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n❌ Missing packages: {', '.join(missing_packages)}")
        print("Please run the setup script again.")
        return False
    else:
        print("\n✅ All required packages are installed.")
        return True

def check_application_files():
    """Check if all required application files exist."""
    print("\nChecking application files...")
    
    required_files = [
        'src/run.py',
        'src/downloader/tiktok_gui_modular.py',
        'src/core/tiktok_downloader.py',
        'requirements.txt',
    ]
    
    missing_files = []
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path} exists.")
        else:
            print(f"❌ {file_path} is missing.")
            missing_files.append(file_path)
    
    if missing_files:
        print(f"\n❌ Missing files: {', '.join(missing_files)}")
        return False
    else:
        print("\n✅ All required files are present.")
        return True

def test_imports():
    """Test if the application modules can be imported."""
    print("\nTesting application imports...")
    
    try:
        # Add src to path
        sys.path.insert(0, os.path.join(os.getcwd(), 'src'))
        
        # Test core imports
        from core.tiktok_downloader import TikTokDownloader
        print("✅ TikTokDownloader imported successfully.")
        
        # Test downloader imports
        from downloader.tiktok_gui_modular import TikTokDownloaderModularGUI
        print("✅ TikTokDownloaderModularGUI imported successfully.")
        
        print("\n✅ All application modules can be imported.")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def main():
    """Main verification function."""
    print("=" * 50)
    print("Social Downloader - Installation Verification")
    print("=" * 50)
    
    checks = [
        check_python_version(),
        check_required_packages(),
        check_application_files(),
        test_imports(),
    ]
    
    print("\n" + "=" * 50)
    if all(checks):
        print("🎉 Installation verification completed successfully!")
        print("You can now run the application using:")
        print("- Windows: Double-click start_windows.bat")
        print("- Mac: Double-click start_mac.sh")
        print("- Linux: Double-click start_linux.sh")
        print("- Or run: python src/run.py")
    else:
        print("❌ Installation verification failed.")
        print("Please run the setup script again and try this verification again.")
    
    print("=" * 50)

if __name__ == "__main__":
    main()
