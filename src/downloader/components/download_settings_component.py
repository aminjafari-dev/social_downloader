"""
Download Settings Component

This component handles the download configuration settings for the TikTok Downloader GUI.
It provides controls for output directory, quality, custom naming, and other download options.

Usage:
    # Create the component
    settings_component = DownloadSettingsComponent(parent_frame)
    
    # Get current settings
    settings = settings_component.get_settings()
    
    # Update settings
    settings_component.update_settings(output_dir="new_path", quality="720p")
    
    # Reset to defaults
    settings_component.reset_to_defaults()
"""

import tkinter as tk
from tkinter import ttk, filedialog
from typing import Dict, Any


class DownloadSettingsComponent:
    """
    Component for handling download configuration settings.
    
    This component provides controls for configuring various download options including
    output directory, quality, custom naming, audio extraction, metadata, and Excel export.
    
    Attributes:
        parent (tk.Widget): Parent widget to contain this component
        output_dir_var (tk.StringVar): Variable to store output directory path
        quality_var (tk.StringVar): Variable to store quality selection
        custom_name_var (tk.StringVar): Variable to store custom base name
        audio_only_var (tk.BooleanVar): Variable to store audio-only flag
        metadata_var (tk.BooleanVar): Variable to store metadata flag
        excel_export_var (tk.BooleanVar): Variable to store Excel export flag
        frame (ttk.LabelFrame): Main frame containing all settings widgets
    """
    
    def __init__(self, parent: tk.Widget):
        """
        Initialize the DownloadSettingsComponent.
        
        Args:
            parent (tk.Widget): Parent widget to contain this component
        """
        self.parent = parent
        
        # Initialize variables with default values
        self.output_dir_var = tk.StringVar(value="downloads")
        self.quality_var = tk.StringVar(value="best")
        self.custom_name_var = tk.StringVar()
        self.audio_only_var = tk.BooleanVar()
        self.metadata_var = tk.BooleanVar(value=True)
        self.excel_export_var = tk.BooleanVar(value=True)
        
        self.frame = None
        
        self._create_widgets()
        self._setup_layout()
    
    def _create_widgets(self):
        """Create all widgets for the download settings component."""
        # Create main frame
        self.frame = ttk.LabelFrame(self.parent, text="Download Settings", padding="10")
        
        # Output directory
        ttk.Label(self.frame, text="Output Directory:").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        output_dir_entry = ttk.Entry(self.frame, textvariable=self.output_dir_var, width=40)
        output_dir_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 5), pady=(0, 5))
        ttk.Button(self.frame, text="Browse", command=self._browse_output_dir).grid(row=0, column=2, pady=(0, 5))
        
        # Quality selection
        ttk.Label(self.frame, text="Quality:").grid(row=1, column=0, sticky=tk.W, pady=(0, 5))
        quality_combo = ttk.Combobox(
            self.frame, 
            textvariable=self.quality_var, 
            values=["best", "720p", "480p", "360p"], 
            width=15,
            state="readonly"
        )
        quality_combo.grid(row=1, column=1, sticky=tk.W, padx=(10, 0), pady=(0, 5))
        
        # Custom name
        ttk.Label(self.frame, text="Custom Name:").grid(row=2, column=0, sticky=tk.W, pady=(0, 5))
        custom_name_entry = ttk.Entry(self.frame, textvariable=self.custom_name_var, width=40)
        custom_name_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=(0, 5))
        
        # Options row
        self.audio_only_var = tk.BooleanVar()
        audio_check = ttk.Checkbutton(self.frame, text="Audio Only", variable=self.audio_only_var)
        audio_check.grid(row=3, column=0, sticky=tk.W, pady=(0, 5))
        
        self.metadata_var = tk.BooleanVar(value=True)
        metadata_check = ttk.Checkbutton(self.frame, text="Add Metadata", variable=self.metadata_var)
        metadata_check.grid(row=3, column=1, sticky=tk.W, padx=(10, 0), pady=(0, 5))
        
        # Excel export
        self.excel_export_var = tk.BooleanVar(value=True)
        excel_check = ttk.Checkbutton(self.frame, text="Export to Excel", variable=self.excel_export_var)
        excel_check.grid(row=3, column=2, sticky=tk.W, padx=(10, 0), pady=(0, 5))
        
        # Configure grid weights for proper expansion
        self.frame.columnconfigure(1, weight=1)
    
    def _setup_layout(self):
        """Setup the layout and grid weights."""
        # Grid weights are configured in _create_widgets
        pass
    
    def _browse_output_dir(self):
        """Browse for output directory."""
        directory = filedialog.askdirectory(initialdir=self.output_dir_var.get())
        if directory:
            self.output_dir_var.set(directory)
    
    def get_settings(self) -> Dict[str, Any]:
        """
        Get all current download settings.
        
        Returns:
            Dict[str, Any]: Dictionary containing all current settings
        """
        return {
            'output_dir': self.output_dir_var.get(),
            'quality': self.quality_var.get(),
            'custom_base_name': self.custom_name_var.get().strip() if self.custom_name_var.get().strip() else None,
            'extract_audio': self.audio_only_var.get(),
            'add_metadata': self.metadata_var.get(),
            'export_to_excel': self.excel_export_var.get()
        }
    
    def update_settings(self, **kwargs):
        """
        Update specific settings.
        
        Args:
            **kwargs: Settings to update (e.g., output_dir="new_path", quality="720p")
        """
        if 'output_dir' in kwargs:
            self.output_dir_var.set(kwargs['output_dir'])
        
        if 'quality' in kwargs:
            self.quality_var.set(kwargs['quality'])
        
        if 'custom_base_name' in kwargs:
            self.custom_name_var.set(kwargs['custom_base_name'] or '')
        
        if 'extract_audio' in kwargs:
            self.audio_only_var.set(kwargs['extract_audio'])
        
        if 'add_metadata' in kwargs:
            self.metadata_var.set(kwargs['add_metadata'])
        
        if 'export_to_excel' in kwargs:
            self.excel_export_var.set(kwargs['export_to_excel'])
    
    def reset_to_defaults(self):
        """Reset all settings to their default values."""
        self.output_dir_var.set("downloads")
        self.quality_var.set("best")
        self.custom_name_var.set("")
        self.audio_only_var.set(False)
        self.metadata_var.set(True)
        self.excel_export_var.set(True)
    
    def validate_settings(self) -> tuple[bool, str]:
        """
        Validate current settings.
        
        Returns:
            tuple[bool, str]: (is_valid, error_message)
        """
        output_dir = self.output_dir_var.get().strip()
        if not output_dir:
            return False, "Output directory cannot be empty"
        
        quality = self.quality_var.get()
        valid_qualities = ["best", "720p", "480p", "360p"]
        if quality not in valid_qualities:
            return False, f"Invalid quality: {quality}. Must be one of {valid_qualities}"
        
        return True, ""
    
    def get_output_directory(self) -> str:
        """
        Get the current output directory.
        
        Returns:
            str: Output directory path
        """
        return self.output_dir_var.get()
    
    def get_quality(self) -> str:
        """
        Get the current quality setting.
        
        Returns:
            str: Quality setting
        """
        return self.quality_var.get()
    
    def get_custom_name(self) -> str:
        """
        Get the current custom name.
        
        Returns:
            str: Custom name or empty string
        """
        return self.custom_name_var.get().strip()
    
    def is_audio_only(self) -> bool:
        """
        Check if audio-only mode is enabled.
        
        Returns:
            bool: True if audio-only mode is enabled
        """
        return self.audio_only_var.get()
    
    def is_metadata_enabled(self) -> bool:
        """
        Check if metadata is enabled.
        
        Returns:
            bool: True if metadata is enabled
        """
        return self.metadata_var.get()
    
    def is_excel_export_enabled(self) -> bool:
        """
        Check if Excel export is enabled.
        
        Returns:
            bool: True if Excel export is enabled
        """
        return self.excel_export_var.get()
    
    def get_widget(self) -> ttk.LabelFrame:
        """
        Get the main frame widget for this component.
        
        Returns:
            ttk.LabelFrame: The main frame containing all settings widgets
        """
        return self.frame
