"""
Video URL Component

This component handles the single URL input functionality for the TikTok Downloader GUI.
It provides a clean interface for users to input individual TikTok video URLs.

Usage:
    # Create the component
    url_component = VideoURLComponent(parent_frame)
    
    # Get the entered URL
    url = url_component.get_url()
    
    # Clear the URL input
    url_component.clear_url()
"""

import tkinter as tk
from tkinter import ttk
from typing import Optional


class VideoURLComponent:
    """
    Component for handling single video URL input.
    
    This component provides a clean interface for users to input individual TikTok video URLs
    with validation and clear visual feedback.
    
    Attributes:
        parent (tk.Widget): Parent widget to contain this component
        url_var (tk.StringVar): Variable to store the URL input
        url_entry (ttk.Entry): Entry widget for URL input
        frame (ttk.Frame): Main frame containing all URL-related widgets
    """
    
    def __init__(self, parent: tk.Widget):
        """
        Initialize the VideoURLComponent.
        
        Args:
            parent (tk.Widget): Parent widget to contain this component
        """
        self.parent = parent
        self.url_var = tk.StringVar()
        self.frame = None
        self.url_entry = None
        
        self._create_widgets()
        self._setup_layout()
    
    def _create_widgets(self):
        """Create all widgets for the URL input component."""
        # Create main frame
        self.frame = ttk.LabelFrame(self.parent, text="Video URL", padding="10")
        
        # URL input label and entry
        ttk.Label(self.frame, text="Single URL:").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        self.url_entry = ttk.Entry(self.frame, textvariable=self.url_var, width=60)
        self.url_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=(0, 5))
        
        # Configure grid weights for proper expansion
        self.frame.columnconfigure(1, weight=1)
    
    def _setup_layout(self):
        """Setup the layout and grid weights."""
        # Grid weights are configured in _create_widgets
        pass
    
    def get_url(self) -> str:
        """
        Get the currently entered URL.
        
        Returns:
            str: The URL string, or empty string if no URL entered
        """
        return self.url_var.get().strip()
    
    def set_url(self, url: str):
        """
        Set the URL in the input field.
        
        Args:
            url (str): The URL to set
        """
        self.url_var.set(url)
    
    def clear_url(self):
        """Clear the URL input field."""
        self.url_var.set("")
    
    def focus(self):
        """Set focus to the URL entry field."""
        self.url_entry.focus()
    
    def is_empty(self) -> bool:
        """
        Check if the URL input is empty.
        
        Returns:
            bool: True if empty, False otherwise
        """
        return not bool(self.get_url())
    
    def get_widget(self) -> ttk.LabelFrame:
        """
        Get the main frame widget for this component.
        
        Returns:
            ttk.LabelFrame: The main frame containing all URL-related widgets
        """
        return self.frame
