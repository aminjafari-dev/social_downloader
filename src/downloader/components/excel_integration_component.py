"""
Excel Integration Component

This component handles Excel file operations and integration for the TikTok Downloader GUI.
It provides functionality for loading Excel files, selecting columns, previewing URLs, and
managing Excel-related operations.

Usage:
    # Create the component
    excel_component = ExcelIntegrationComponent(parent_frame, excel_loader)
    
    # Load Excel file
    excel_component.load_excel_file("path/to/file.xlsx")
    
    # Get selected URLs
    urls = excel_component.get_selected_urls()
    
    # Preview URLs
    excel_component.preview_urls()
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from typing import List, Optional, Callable


class ExcelIntegrationComponent:
    """
    Component for handling Excel file operations and integration.
    
    This component provides a comprehensive interface for working with Excel files,
    including file selection, column loading, URL preview, and download management.
    
    Attributes:
        parent (tk.Widget): Parent widget to contain this component
        excel_loader: Excel loader utility for file operations
        excel_file_var (tk.StringVar): Variable to store Excel file path
        url_column_var (tk.StringVar): Variable to store selected URL column
        url_column_combo (ttk.Combobox): Combobox for URL column selection
        excel_status_var (tk.StringVar): Variable to store Excel status messages
        frame (ttk.LabelFrame): Main frame containing all Excel-related widgets
        on_url_validation (Callable): Callback function for URL validation
    """
    
    def __init__(self, parent: tk.Widget, excel_loader, on_url_validation: Optional[Callable] = None):
        """
        Initialize the ExcelIntegrationComponent.
        
        Args:
            parent (tk.Widget): Parent widget to contain this component
            excel_loader: Excel loader utility for file operations
            on_url_validation (Callable, optional): Callback function for URL validation
        """
        self.parent = parent
        self.excel_loader = excel_loader
        self.on_url_validation = on_url_validation
        
        # Initialize variables
        self.excel_file_var = tk.StringVar()
        self.url_column_var = tk.StringVar()
        self.excel_status_var = tk.StringVar(value="No Excel file selected")
        
        self.frame = None
        self.url_column_combo = None
        
        self._create_widgets()
        self._setup_layout()
    
    def _create_widgets(self):
        """Create all widgets for the Excel integration component."""
        # Create main frame
        self.frame = ttk.LabelFrame(self.parent, text="Excel Integration", padding="10")
        
        # Excel file selection
        ttk.Label(self.frame, text="Excel File:").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        excel_file_entry = ttk.Entry(self.frame, textvariable=self.excel_file_var, width=50)
        excel_file_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 5), pady=(0, 5))
        ttk.Button(self.frame, text="Browse", command=self._browse_excel_file).grid(row=0, column=2, pady=(0, 5))
        
        # URL column selection
        ttk.Label(self.frame, text="URL Column:").grid(row=1, column=0, sticky=tk.W, pady=(0, 5))
        self.url_column_combo = ttk.Combobox(self.frame, textvariable=self.url_column_var, width=20, state="readonly")
        self.url_column_combo.grid(row=1, column=1, sticky=tk.W, padx=(10, 0), pady=(0, 5))
        
        # Excel buttons
        excel_button_frame = ttk.Frame(self.frame)
        excel_button_frame.grid(row=2, column=0, columnspan=3, pady=(10, 0))
        
        ttk.Button(excel_button_frame, text="Load Columns", command=self._load_excel_columns).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(excel_button_frame, text="Preview URLs", command=self._preview_excel_urls).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(excel_button_frame, text="Download from Excel", command=self._start_excel_download).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(excel_button_frame, text="Process Existing", command=self._process_existing_downloads).pack(side=tk.LEFT)
        
        # Excel status
        ttk.Label(self.frame, textvariable=self.excel_status_var, foreground="blue").grid(row=3, column=0, columnspan=3, pady=(5, 0))
        
        # Configure grid weights for proper expansion
        self.frame.columnconfigure(1, weight=1)
    
    def _setup_layout(self):
        """Setup the layout and grid weights."""
        # Grid weights are configured in _create_widgets
        pass
    
    def _browse_excel_file(self):
        """Browse for Excel file."""
        file_path = filedialog.askopenfilename(
            title="Select Excel File",
            filetypes=[
                ("Excel files", "*.xlsx *.xls"),
                ("All files", "*.*")
            ]
        )
        if file_path:
            self.excel_file_var.set(file_path)
            self.excel_status_var.set(f"Selected: {os.path.basename(file_path)}")
            # Auto-load columns when file is selected
            self._load_excel_columns()
    
    def _load_excel_columns(self):
        """Load column names from Excel file."""
        excel_path = self.excel_file_var.get().strip()
        if not excel_path:
            messagebox.showerror("Error", "Please select an Excel file first")
            return
        
        try:
            # Use Excel loader to get column names
            columns = self.excel_loader.get_column_names(excel_path)
            
            # Update combobox with column names
            self.url_column_combo['values'] = columns
            
            # Try to auto-select URL column
            url_columns = [col for col in columns if 'url' in col.lower()]
            if url_columns:
                self.url_column_var.set(url_columns[0])
                self.excel_status_var.set(f"Found {len(columns)} columns, auto-selected: {url_columns[0]}")
            else:
                self.excel_status_var.set(f"Found {len(columns)} columns, please select URL column")
            
            # Trigger callback if available
            if hasattr(self, 'on_columns_loaded'):
                self.on_columns_loaded(columns)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load Excel file: {str(e)}")
            self.excel_status_var.set(f"Error loading file: {str(e)}")
    
    def _preview_excel_urls(self):
        """Preview URLs from selected column."""
        excel_path = self.excel_file_var.get().strip()
        url_column = self.url_column_var.get().strip()
        
        if not excel_path or not url_column:
            messagebox.showerror("Error", "Please select Excel file and URL column first")
            return
        
        try:
            # Use Excel loader to get preview
            preview_text = self.excel_loader.get_excel_preview(excel_path, url_column, max_preview=5)
            
            # Get valid URLs for additional info if validation callback is available
            if self.on_url_validation:
                urls = self.excel_loader.extract_urls_from_column(excel_path, url_column, self.on_url_validation)
                valid_urls = [url for url in urls if self.on_url_validation(url)]
                
                # Enhance preview with validation info
                enhanced_preview = f"Total URLs in column '{url_column}': {len(urls)}\n"
                enhanced_preview += f"Valid TikTok URLs: {len(valid_urls)}\n\n"
                enhanced_preview += preview_text
                
                messagebox.showinfo("URL Preview", enhanced_preview)
            else:
                messagebox.showinfo("URL Preview", preview_text)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to preview URLs: {str(e)}")
            self.excel_status_var.set(f"Error previewing URLs: {str(e)}")
    
    def _start_excel_download(self):
        """Start download process from Excel file."""
        urls = self.get_selected_urls()
        
        if not urls:
            messagebox.showerror("Error", "No valid TikTok URLs found in Excel file")
            return
        
        # Show confirmation with URL count
        url_count = len(urls)
        confirm = messagebox.askyesno(
            "Confirm Excel Download", 
            f"Found {url_count} valid TikTok URL(s) in the Excel file.\n\n"
            f"This will download each video individually and update the Excel file "
            f"with metadata after each successful download.\n\n"
            f"Continue with the download?"
        )
        
        if not confirm:
            return
        
        # Update status
        self.set_status_message(f"Starting download of {url_count} videos from Excel...")
        
        # Trigger callback if available
        if hasattr(self, 'on_excel_download_start'):
            self.on_excel_download_start(urls)
    
    def _process_existing_downloads(self):
        """Process existing downloads and create Excel file."""
        # Trigger callback if available
        if hasattr(self, 'on_process_existing'):
            self.on_process_existing()
    
    def get_excel_file_path(self) -> str:
        """
        Get the current Excel file path.
        
        Returns:
            str: Excel file path or empty string
        """
        return self.excel_file_var.get().strip()
    
    def get_selected_url_column(self) -> str:
        """
        Get the selected URL column name.
        
        Returns:
            str: Selected column name or empty string
        """
        return self.url_column_var.get().strip()
    
    def get_selected_urls(self) -> List[str]:
        """
        Get URLs from the selected Excel file and column.
        
        Returns:
            List[str]: List of URLs from the Excel file
        """
        excel_path = self.get_excel_file_path()
        url_column = self.get_selected_url_column()
        
        if not excel_path or not url_column:
            return []
        
        try:
            # Use Excel loader to extract URLs with validation if available
            if self.on_url_validation:
                urls = self.excel_loader.extract_urls_from_column(
                    excel_path, 
                    url_column, 
                    self.on_url_validation
                )
            else:
                urls = self.excel_loader.extract_urls_from_column(excel_path, url_column)
            
            return urls
            
        except Exception as e:
            self.excel_status_var.set(f"Error reading Excel file: {str(e)}")
            return []
    
    def is_file_selected(self) -> bool:
        """
        Check if an Excel file is selected.
        
        Returns:
            bool: True if file is selected, False otherwise
        """
        return bool(self.get_excel_file_path())
    
    def is_column_selected(self) -> bool:
        """
        Check if a URL column is selected.
        
        Returns:
            bool: True if column is selected, False otherwise
        """
        return bool(self.get_selected_url_column())
    
    def is_ready_for_download(self) -> bool:
        """
        Check if the component is ready for download operations.
        
        Returns:
            bool: True if ready, False otherwise
        """
        return self.is_file_selected() and self.is_column_selected()
    
    def set_status_message(self, message: str, is_error: bool = False):
        """
        Set the status message.
        
        Args:
            message (str): Status message to display
            is_error (bool): Whether this is an error message
        """
        self.excel_status_var.set(message)
        if is_error:
            # Change color to red for errors
            self.frame.winfo_children()[-1].configure(foreground="red")
        else:
            # Reset to blue for normal messages
            self.frame.winfo_children()[-1].configure(foreground="blue")
    
    def update_download_progress(self, current: int, total: int, video_title: str = ""):
        """
        Update the download progress display.
        
        Args:
            current (int): Current video number being processed
            total (int): Total number of videos to process
            video_title (str): Title of the current video being processed
        """
        if video_title:
            # Truncate long titles for display
            display_title = video_title[:50] + "..." if len(video_title) > 50 else video_title
            progress_message = f"Processing video {current}/{total}: {display_title}"
        else:
            progress_message = f"Processing video {current}/{total}"
        
        self.set_status_message(progress_message)
    
    def clear_selection(self):
        """Clear the current Excel file and column selection."""
        self.excel_file_var.set("")
        self.url_column_var.set("")
        self.url_column_combo['values'] = []
        self.excel_status_var.set("No Excel file selected")
    
    def set_callbacks(self, on_columns_loaded=None, on_excel_download_start=None, on_process_existing=None):
        """
        Set callback functions for various events.
        
        Args:
            on_columns_loaded: Callback when columns are loaded
            on_excel_download_start: Callback when Excel download starts
            on_process_existing: Callback when processing existing downloads
        """
        if on_columns_loaded:
            self.on_columns_loaded = on_columns_loaded
        if on_excel_download_start:
            self.on_excel_download_start = on_excel_download_start
        if on_process_existing:
            self.on_process_existing = on_process_existing
    
    def get_widget(self) -> ttk.LabelFrame:
        """
        Get the main frame widget for this component.
        
        Returns:
            ttk.LabelFrame: The main frame containing all Excel-related widgets
        """
        return self.frame
