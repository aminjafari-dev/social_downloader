"""
Test script to verify TikTok Video Downloader installation.

This script checks if all required dependencies are installed and the downloader
can be imported and initialized properly.
"""

import sys
import importlib


def test_imports():
    """
    Test if all required modules can be imported.
    
    Returns:
        bool: True if all imports succeed, False otherwise
    """
    print("Testing module imports...")
    
    required_modules = [
        'yt_dlp',
        'colorama',
        'tkinter',
        'pathlib',
        'logging',
        'argparse',
        'threading',
        'queue'
    ]
    
    failed_imports = []
    
    for module in required_modules:
        try:
            importlib.import_module(module)
            print(f"  ✅ {module}")
        except ImportError as e:
            print(f"  ❌ {module}: {e}")
            failed_imports.append(module)
    
    if failed_imports:
        print(f"\n❌ Failed to import: {', '.join(failed_imports)}")
        return False
    else:
        print("\n✅ All modules imported successfully!")
        return True


def test_downloader_class():
    """
    Test if the TikTokDownloader class can be imported and instantiated.
    
    Returns:
        bool: True if successful, False otherwise
    """
    print("\nTesting TikTokDownloader class...")
    
    try:
        from tiktok_downloader import TikTokDownloader
        print("  ✅ TikTokDownloader imported successfully")
        
        # Test instantiation
        downloader = TikTokDownloader()
        print("  ✅ TikTokDownloader instantiated successfully")
        
        # Test basic attributes
        assert hasattr(downloader, 'output_dir'), "Missing output_dir attribute"
        assert hasattr(downloader, 'quality'), "Missing quality attribute"
        assert hasattr(downloader, 'download_video'), "Missing download_video method"
        assert hasattr(downloader, 'validate_url'), "Missing validate_url method"
        
        print("  ✅ All required attributes and methods present")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False


def test_gui_import():
    """
    Test if the GUI module can be imported.
    
    Returns:
        bool: True if successful, False otherwise
    """
    print("\nTesting GUI module...")
    
    try:
        import tiktok_gui
        print("  ✅ GUI module imported successfully")
        return True
    except Exception as e:
        print(f"  ❌ GUI import error: {e}")
        return False


def test_url_validation():
    """
    Test URL validation functionality.
    
    Returns:
        bool: True if successful, False otherwise
    """
    print("\nTesting URL validation...")
    
    try:
        from tiktok_downloader import TikTokDownloader
        downloader = TikTokDownloader()
        
        # Test valid URLs
        valid_urls = [
            "https://www.tiktok.com/@user/video/1234567890",
            "https://vm.tiktok.com/xxxxx/",
            "https://vt.tiktok.com/xxxxx/"
        ]
        
        for url in valid_urls:
            if not downloader.validate_url(url):
                print(f"  ❌ Valid URL not recognized: {url}")
                return False
        
        # Test invalid URLs
        invalid_urls = [
            "https://youtube.com/watch?v=1234567890",
            "https://example.com/video",
            "not_a_url"
        ]
        
        for url in invalid_urls:
            if downloader.validate_url(url):
                print(f"  ❌ Invalid URL incorrectly accepted: {url}")
                return False
        
        print("  ✅ URL validation working correctly")
        return True
        
    except Exception as e:
        print(f"  ❌ URL validation error: {e}")
        return False


def test_python_version():
    """
    Test if Python version is compatible.
    
    Returns:
        bool: True if compatible, False otherwise
    """
    print("\nTesting Python version...")
    
    version = sys.version_info
    print(f"  Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major >= 3 and version.minor >= 7:
        print("  ✅ Python version is compatible (3.7+)")
        return True
    else:
        print("  ❌ Python version too old (requires 3.7+)")
        return False


def main():
    """
    Main function to run all tests.
    
    This function runs comprehensive tests to verify the installation.
    """
    print("TikTok Video Downloader - Installation Test")
    print("=" * 50)
    print()
    
    tests = [
        ("Python Version", test_python_version),
        ("Module Imports", test_imports),
        ("Downloader Class", test_downloader_class),
        ("GUI Module", test_gui_import),
        ("URL Validation", test_url_validation)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"Running {test_name} test...")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"  ❌ Test failed with exception: {e}")
            results.append((test_name, False))
        print()
    
    # Summary
    print("Test Results Summary:")
    print("-" * 30)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Installation is successful.")
        print("\nYou can now use the TikTok Video Downloader:")
        print("  - Command line: python tiktok_downloader.py --help")
        print("  - GUI: python tiktok_gui.py")
        print("  - Examples: python example.py")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please check the errors above.")
        print("\nTroubleshooting:")
        print("1. Install missing dependencies: pip install -r requirements.txt")
        print("2. Ensure Python 3.7+ is installed")
        print("3. Check if all files are in the same directory")
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
