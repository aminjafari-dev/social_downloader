"""
Example usage of TikTok Video Downloader

This script demonstrates how to use the TikTokDownloader class programmatically
for various download scenarios.
"""

from tiktok_downloader import TikTokDownloader
import os


def example_single_download():
    """
    Example: Download a single TikTok video.
    
    This function demonstrates how to download a single video with basic settings.
    """
    print("=== Example: Single Video Download ===")
    
    # Initialize downloader with default settings
    downloader = TikTokDownloader()
    
    # Example TikTok URL (replace with actual URL)
    url = "https://www.tiktok.com/@example/video/1234567890"
    
    print(f"Attempting to download: {url}")
    
    # Download the video
    success = downloader.download_video(url)
    
    if success:
        print("✅ Download completed successfully!")
    else:
        print("❌ Download failed!")
    
    print()


def example_custom_settings():
    """
    Example: Download with custom settings.
    
    This function shows how to configure the downloader with custom options.
    """
    print("=== Example: Custom Settings Download ===")
    
    # Initialize downloader with custom settings
    downloader = TikTokDownloader(
        output_dir="custom_downloads",  # Custom output directory
        quality="720p",                 # Specific quality
        extract_audio=False,            # Download video (not audio only)
        add_metadata=True               # Include metadata
    )
    
    url = "https://www.tiktok.com/@example/video/1234567890"
    
    print(f"Downloading with custom settings:")
    print(f"  - Output directory: {downloader.output_dir}")
    print(f"  - Quality: {downloader.quality}")
    print(f"  - Audio only: {downloader.extract_audio}")
    print(f"  - Metadata: {downloader.add_metadata}")
    
    success = downloader.download_video(url)
    
    if success:
        print("✅ Custom download completed!")
    else:
        print("❌ Custom download failed!")
    
    print()


def example_audio_only():
    """
    Example: Download audio only from TikTok video.
    
    This function demonstrates how to extract just the audio from a video.
    """
    print("=== Example: Audio Only Download ===")
    
    # Initialize downloader for audio extraction
    downloader = TikTokDownloader(
        output_dir="audio_downloads",
        extract_audio=True,  # Extract audio only
        add_metadata=True
    )
    
    url = "https://www.tiktok.com/@example/video/1234567890"
    
    print(f"Extracting audio from: {url}")
    
    success = downloader.download_video(url)
    
    if success:
        print("✅ Audio extraction completed!")
    else:
        print("❌ Audio extraction failed!")
    
    print()


def example_batch_download():
    """
    Example: Download multiple videos in batch.
    
    This function shows how to download multiple videos from a list of URLs.
    """
    print("=== Example: Batch Download ===")
    
    # Initialize downloader
    downloader = TikTokDownloader(output_dir="batch_downloads")
    
    # List of example URLs (replace with actual URLs)
    urls = [
        "https://www.tiktok.com/@user1/video/1234567890",
        "https://www.tiktok.com/@user2/video/0987654321",
        "https://www.tiktok.com/@user3/video/1122334455"
    ]
    
    print(f"Starting batch download of {len(urls)} videos...")
    
    # Download multiple videos
    results = downloader.download_multiple_videos(urls)
    
    # Print results
    successful = sum(results.values())
    print(f"Batch download completed: {successful}/{len(urls)} successful")
    
    for url, success in results.items():
        status = "✅" if success else "❌"
        print(f"  {status} {url}")
    
    print()


def example_video_info():
    """
    Example: Get video information without downloading.
    
    This function demonstrates how to extract video metadata without downloading.
    """
    print("=== Example: Video Information ===")
    
    downloader = TikTokDownloader()
    
    url = "https://www.tiktok.com/@example/video/1234567890"
    
    print(f"Extracting information for: {url}")
    
    # Get video information
    info = downloader.get_video_info(url)
    
    if info:
        print("✅ Video information extracted:")
        print(f"  - Title: {info.get('title', 'Unknown')}")
        print(f"  - Duration: {info.get('duration', 'Unknown')} seconds")
        print(f"  - Uploader: {info.get('uploader', 'Unknown')}")
        print(f"  - View count: {info.get('view_count', 'Unknown')}")
        print(f"  - Like count: {info.get('like_count', 'Unknown')}")
    else:
        print("❌ Failed to extract video information")
    
    print()


def example_url_validation():
    """
    Example: URL validation.
    
    This function demonstrates how to validate TikTok URLs.
    """
    print("=== Example: URL Validation ===")
    
    downloader = TikTokDownloader()
    
    # Test URLs
    test_urls = [
        "https://www.tiktok.com/@user/video/1234567890",
        "https://vm.tiktok.com/xxxxx/",
        "https://vt.tiktok.com/xxxxx/",
        "https://youtube.com/watch?v=1234567890",  # Invalid (YouTube)
        "https://example.com/video",               # Invalid
        "not_a_url"                               # Invalid
    ]
    
    print("Testing URL validation:")
    
    for url in test_urls:
        is_valid = downloader.validate_url(url)
        status = "✅" if is_valid else "❌"
        print(f"  {status} {url}")
    
    print()


def create_sample_urls_file():
    """
    Create a sample URLs file for batch downloading.
    
    This function creates a sample file that can be used with the --file option.
    """
    print("=== Creating Sample URLs File ===")
    
    sample_urls = [
        "https://www.tiktok.com/@example1/video/1234567890",
        "https://www.tiktok.com/@example2/video/0987654321",
        "https://www.tiktok.com/@example3/video/1122334455",
        "# This is a comment line",
        "https://vm.tiktok.com/xxxxx/",
        ""
    ]
    
    filename = "sample_urls.txt"
    
    with open(filename, 'w') as f:
        for url in sample_urls:
            f.write(url + '\n')
    
    print(f"✅ Created sample URLs file: {filename}")
    print(f"   You can use it with: python tiktok_downloader.py --file {filename}")
    print()


def main():
    """
    Main function to run all examples.
    
    This function demonstrates various usage scenarios of the TikTok downloader.
    """
    print("TikTok Video Downloader - Usage Examples")
    print("=" * 50)
    print()
    
    # Note: These examples use placeholder URLs
    # Replace them with actual TikTok URLs to test
    
    print("⚠️  Note: These examples use placeholder URLs.")
    print("   Replace them with actual TikTok URLs to test the functionality.")
    print()
    
    # Run examples
    example_url_validation()
    example_video_info()
    example_single_download()
    example_custom_settings()
    example_audio_only()
    example_batch_download()
    create_sample_urls_file()
    
    print("=== Summary ===")
    print("✅ All examples completed!")
    print()
    print("To use with real URLs:")
    print("1. Replace the placeholder URLs in the examples with actual TikTok URLs")
    print("2. Run the specific example function you want to test")
    print("3. Check the 'downloads' directory for downloaded files")
    print()
    print("For more options, see the README.md file or run:")
    print("   python tiktok_downloader.py --help")


if __name__ == "__main__":
    main()
