"""
Batch Mode Component

This component handles the batch URL input functionality for the TikTok Downloader GUI.
It provides an interface for users to input multiple TikTok video URLs at once.

Usage:
    # Create the component
    batch_component = BatchModeComponent(parent_frame)
    
    # Get all batch URLs
    urls = batch_component.get_urls()
    
    # Check if batch mode is enabled
    is_enabled = batch_component.is_batch_mode_enabled()
    
    # Clear all batch URLs
    batch_component.clear_urls()
"""

import tkinter as tk
from tkinter import ttk
from typing import List


class BatchModeComponent:
    """
    Component for handling batch URL input functionality.
    
    This component provides an interface for users to input multiple TikTok video URLs
    at once, with a toggle to enable/disable batch mode and a text area for URL input.
    
    Attributes:
        parent (tk.Widget): Parent widget to contain this component
        batch_mode_var (tk.BooleanVar): Variable to store batch mode state
        batch_text (tk.Text): Text widget for batch URL input
        frame (ttk.LabelFrame): Main frame containing all batch-related widgets
    """
    
    def __init__(self, parent: tk.Widget):
        """
        Initialize the BatchModeComponent.
        
        Args:
            parent (tk.Widget): Parent widget to contain this component
        """
        self.parent = parent
        self.batch_mode_var = tk.BooleanVar()
        self.batch_text = None
        self.frame = None
        
        self._create_widgets()
        self._setup_layout()
    
    def _create_widgets(self):
        """Create all widgets for the batch mode component."""
        # Create main frame
        self.frame = ttk.LabelFrame(self.parent, text="Batch Mode", padding="10")
        
        # Batch mode toggle
        batch_check = ttk.Checkbutton(
            self.frame, 
            text="Enable Batch Mode", 
            variable=self.batch_mode_var,
            command=self._on_batch_mode_toggle
        )
        batch_check.grid(row=0, column=0, sticky=tk.W, pady=(0, 10))
        
        # Batch text area label
        ttk.Label(self.frame, text="Batch URLs (one per line):").grid(
            row=1, column=0, sticky=tk.W, pady=(0, 5)
        )
        
        # Batch text area
        self.batch_text = tk.Text(self.frame, height=5, width=60)
        self.batch_text.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        
        # Add scrollbar for the text area
        batch_scrollbar = ttk.Scrollbar(self.frame, orient=tk.VERTICAL, command=self.batch_text.yview)
        self.batch_text.configure(yscrollcommand=batch_scrollbar.set)
        batch_scrollbar.grid(row=2, column=1, sticky=(tk.N, tk.S))
        
        # Configure grid weights for proper expansion
        self.frame.columnconfigure(0, weight=1)
    
    def _setup_layout(self):
        """Setup the layout and grid weights."""
        # Grid weights are configured in _create_widgets
        pass
    
    def _on_batch_mode_toggle(self):
        """Handle batch mode toggle state change."""
        # Enable/disable text area based on batch mode state
        if self.batch_mode_var.get():
            self.batch_text.config(state=tk.NORMAL)
        else:
            self.batch_text.config(state=tk.DISABLED)
    
    def is_batch_mode_enabled(self) -> bool:
        """
        Check if batch mode is currently enabled.
        
        Returns:
            bool: True if batch mode is enabled, False otherwise
        """
        return self.batch_mode_var.get()
    
    def get_urls(self) -> List[str]:
        """
        Get all URLs from the batch text area.
        
        Returns:
            List[str]: List of URLs, with empty strings filtered out
        """
        if not self.is_batch_mode_enabled():
            return []
        
        text = self.batch_text.get(1.0, tk.END)
        urls = [url.strip() for url in text.strip().split('\n') if url.strip()]
        return urls
    
    def set_urls(self, urls: List[str]):
        """
        Set URLs in the batch text area.
        
        Args:
            urls (List[str]): List of URLs to set
        """
        if not self.is_batch_mode_enabled():
            self.batch_mode_var.set(True)
            self._on_batch_mode_toggle()
        
        # Clear existing content
        self.batch_text.delete(1.0, tk.END)
        
        # Insert new URLs
        for url in urls:
            self.batch_text.insert(tk.END, url + '\n')
    
    def add_url(self, url: str):
        """
        Add a single URL to the batch text area.
        
        Args:
            url (str): URL to add
        """
        if not self.is_batch_mode_enabled():
            self.batch_mode_var.set(True)
            self._on_batch_mode_toggle()
        
        self.batch_text.insert(tk.END, url + '\n')
    
    def clear_urls(self):
        """Clear all URLs from the batch text area."""
        self.batch_text.delete(1.0, tk.END)
    
    def get_url_count(self) -> int:
        """
        Get the count of URLs in the batch text area.
        
        Returns:
            int: Number of URLs
        """
        return len(self.get_urls())
    
    def is_empty(self) -> bool:
        """
        Check if the batch text area is empty.
        
        Returns:
            bool: True if empty, False otherwise
        """
        return self.get_url_count() == 0
    
    def get_widget(self) -> ttk.LabelFrame:
        """
        Get the main frame widget for this component.
        
        Returns:
            ttk.LabelFrame: The main frame containing all batch-related widgets
        """
        return self.frame
