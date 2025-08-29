#!/usr/bin/env python3
"""
Show Project Structure

This script displays the organized structure of the Social Downloader project
to help users understand the new folder organization.
"""

import os
from pathlib import Path

def print_tree(directory, prefix="", exclude_dirs=None):
    """Print a tree-like structure of the directory."""
    if exclude_dirs is None:
        exclude_dirs = {'.git', '__pycache__', '.DS_Store'}
    
    items = sorted(os.listdir(directory))
    
    for i, item in enumerate(items):
        if item in exclude_dirs:
            continue
            
        path = os.path.join(directory, item)
        is_last = i == len(items) - 1
        
        if os.path.isdir(path):
            print(f"{prefix}{'└── ' if is_last else '├── '}{item}/")
            new_prefix = prefix + ('    ' if is_last else '│   ')
            print_tree(path, new_prefix, exclude_dirs)
        else:
            print(f"{prefix}{'└── ' if is_last else '├── '}{item}")

def main():
    """Display the project structure."""
    print("🌳 Social Downloader - Project Structure")
    print("=" * 50)
    print()
    
    # Get the project root
    project_root = Path(__file__).parent
    
    print("📁 Root Directory Structure:")
    print_tree(str(project_root))
    
    print("\n" + "=" * 50)
    print("📋 Directory Descriptions:")
    print()
    
    descriptions = {
        "main.py": "Main entry point for the application with unified CLI",
        "downloader/": "Video downloading functionality (TikTok, etc.)",
        "text_remover/": "AI-powered text removal from videos",
        "core/": "Shared utilities, examples, and core functionality",
        "gui/": "GUI utilities and shared components",
        "tests/": "Test files and testing utilities",
        "docs/": "Documentation files (README, guides, etc.)",
        "downloads/": "Downloaded and processed content",
        "downloads/original/": "Original downloaded videos",
        "downloads/processed/": "Videos with text removed",
        "downloads/metadata/": "Video metadata (JSON, descriptions, images)",
        "models/": "AI/ML models (currently empty)",
    }
    
    for path, desc in descriptions.items():
        print(f"  {path:<25} - {desc}")
    
    print("\n" + "=" * 50)
    print("🚀 Quick Usage Examples:")
    print()
    print("  # Download a video")
    print("  python main.py downloader --url 'https://tiktok.com/...'")
    print()
    print("  # Remove text from video")
    print("  python main.py text-remover --input video.mp4 --output clean.mp4")
    print()
    print("  # Launch GUI")
    print("  python main.py gui --type downloader")
    print("  python main.py gui --type text-remover")
    print()
    print("  # Get help")
    print("  python main.py --help")

if __name__ == "__main__":
    main()
