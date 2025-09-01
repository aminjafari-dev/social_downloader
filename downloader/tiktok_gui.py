"""
TikTok Video Downloader GUI

A graphical user interface for downloading TikTok videos using the new modular architecture.
This provides an easy-to-use interface for users who prefer GUI over command line.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import queue
import os
from pathlib import Path
from typing import Optional

# Import our modular components
try:
    from core import DownloadManager
except ImportError:
    # Fallback for when running the file directly
    import sys
    import os
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    from core import DownloadManager

# Import Excel utilities
try:
    from utils.excel_loader import ExcelLoader
except ImportError:
    # Fallback for when running the file directly
    import sys
    import os
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    from utils.excel_loader import ExcelLoader

# Configure logging
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TikTokDownloaderGUI:
    """
    GUI class for TikTok video downloader using the new modular architecture.
    
    This class provides a user-friendly interface for downloading TikTok videos
    with options for single URLs, batch processing, and Excel integration.
    
    Attributes:
        root (tk.Tk): Main tkinter window
        download_manager (DownloadManager): Core download manager instance
        message_queue (queue.Queue): Queue for thread-safe message updates
    """
    
    def __init__(self):
        """Initialize the GUI application."""
        self.root = tk.Tk()
        self.root.title("TikTok Video Downloader - Modular Version")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # Initialize download manager
        self.download_manager = DownloadManager(
            output_dir="downloads",
            quality="best",
            extract_audio=False,
            add_metadata=True,
            custom_base_name=None,
            platform="tiktok"
        )
        
        self.message_queue = queue.Queue()
        
        # Initialize Excel loader
        self.excel_loader = ExcelLoader()
        
        # Create GUI elements
        self._create_widgets()
        self._setup_layout()
        
        # Start message processing
        self.root.after(100, self.process_messages)
        
        logger.info("TikTok Downloader GUI initialized")
    
    def _create_widgets(self):
        """Create all GUI widgets."""
        # Main frame
        self.main_frame = ttk.Frame(self.root, padding="10")
        
        # Title
        title_label = ttk.Label(self.main_frame, text="TikTok Video Downloader - Modular", style='Title.TLabel')
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # URL input section
        url_frame = ttk.LabelFrame(self.main_frame, text="Video URL(s)", padding="10")
        url_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Single URL input
        ttk.Label(url_frame, text="Single URL:").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        self.url_var = tk.StringVar()
        url_entry = ttk.Entry(url_frame, textvariable=self.url_var, width=60)
        url_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=(0, 5))
        
        # Batch mode toggle
        self.batch_mode_var = tk.BooleanVar()
        batch_check = ttk.Checkbutton(url_frame, text="Batch Mode", variable=self.batch_mode_var)
        batch_check.grid(row=1, column=0, sticky=tk.W, pady=(0, 5))
        
        # Batch text area
        ttk.Label(url_frame, text="Batch URLs (one per line):").grid(row=2, column=0, sticky=tk.W, pady=(0, 5))
        self.batch_text = tk.Text(url_frame, height=5, width=60)
        self.batch_text.grid(row=2, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=(0, 5))
        
        # Configure grid weights for URL frame
        url_frame.columnconfigure(1, weight=1)
        
        # Settings section
        settings_frame = ttk.LabelFrame(self.main_frame, text="Download Settings", padding="10")
        settings_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Output directory
        ttk.Label(settings_frame, text="Output Directory:").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        self.output_dir_var = tk.StringVar(value="downloads")
        output_dir_entry = ttk.Entry(settings_frame, textvariable=self.output_dir_var, width=40)
        output_dir_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 5), pady=(0, 5))
        ttk.Button(settings_frame, text="Browse", command=self.browse_output_dir).grid(row=0, column=2, pady=(0, 5))
        
        # Quality selection
        ttk.Label(settings_frame, text="Quality:").grid(row=1, column=0, sticky=tk.W, pady=(0, 5))
        self.quality_var = tk.StringVar(value="best")
        quality_combo = ttk.Combobox(settings_frame, textvariable=self.quality_var, 
                                    values=["best", "720p", "480p", "360p"], width=15)
        quality_combo.grid(row=1, column=1, sticky=tk.W, padx=(10, 0), pady=(0, 5))
        
        # Custom name
        ttk.Label(settings_frame, text="Custom Name:").grid(row=2, column=0, sticky=tk.W, pady=(0, 5))
        self.custom_name_var = tk.StringVar()
        custom_name_entry = ttk.Entry(settings_frame, textvariable=self.custom_name_var, width=40)
        custom_name_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=(0, 5))
        
        # Options
        self.audio_only_var = tk.BooleanVar()
        audio_check = ttk.Checkbutton(settings_frame, text="Audio Only", variable=self.audio_only_var)
        audio_check.grid(row=3, column=0, sticky=tk.W, pady=(0, 5))
        
        self.metadata_var = tk.BooleanVar(value=True)
        metadata_check = ttk.Checkbutton(settings_frame, text="Add Metadata", variable=self.metadata_var)
        metadata_check.grid(row=3, column=1, sticky=tk.W, padx=(10, 0), pady=(0, 5))
        
        # Excel export
        self.excel_export_var = tk.BooleanVar(value=True)
        excel_check = ttk.Checkbutton(settings_frame, text="Export to Excel", variable=self.excel_export_var)
        excel_check.grid(row=3, column=2, sticky=tk.W, padx=(10, 0), pady=(0, 5))
        
        # Configure grid weights for settings frame
        settings_frame.columnconfigure(1, weight=1)
        
        # Excel section
        excel_frame = ttk.LabelFrame(self.main_frame, text="Excel Integration", padding="10")
        excel_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Excel file selection
        ttk.Label(excel_frame, text="Excel File:").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        self.excel_file_var = tk.StringVar()
        excel_file_entry = ttk.Entry(excel_frame, textvariable=self.excel_file_var, width=50)
        excel_file_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 5), pady=(0, 5))
        ttk.Button(excel_frame, text="Browse", command=self.browse_excel_file).grid(row=0, column=2, pady=(0, 5))
        
        # URL column selection
        ttk.Label(excel_frame, text="URL Column:").grid(row=1, column=0, sticky=tk.W, pady=(0, 5))
        self.url_column_var = tk.StringVar()
        self.url_column_combo = ttk.Combobox(excel_frame, textvariable=self.url_column_var, width=20)
        self.url_column_combo.grid(row=1, column=1, sticky=tk.W, padx=(10, 0), pady=(0, 5))
        
        # Excel buttons
        excel_button_frame = ttk.Frame(excel_frame)
        excel_button_frame.grid(row=2, column=0, columnspan=3, pady=(10, 0))
        
        ttk.Button(excel_button_frame, text="Load Columns", command=self.load_excel_columns).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(excel_button_frame, text="Preview URLs", command=self.preview_excel_urls).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(excel_button_frame, text="Download from Excel", command=self.start_excel_download).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(excel_button_frame, text="Process Existing", command=self.process_existing_downloads).pack(side=tk.LEFT)
        
        # Excel status
        self.excel_status_var = tk.StringVar(value="No Excel file selected")
        ttk.Label(excel_frame, textvariable=self.excel_status_var, foreground="blue").grid(row=3, column=0, columnspan=3, pady=(5, 0))
        
        # Configure grid weights for Excel frame
        excel_frame.columnconfigure(1, weight=1)
        
        # Control buttons
        control_frame = ttk.Frame(self.main_frame)
        control_frame.grid(row=4, column=0, columnspan=3, pady=(10, 0))
        
        self.download_btn = ttk.Button(control_frame, text="Start Download", command=self.start_download)
        self.download_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.stop_btn = ttk.Button(control_frame, text="Stop", command=self.stop_download, state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(control_frame, text="Clear Log", command=self.clear_log).pack(side=tk.LEFT)
        
        # Progress bar
        self.progress_bar = ttk.Progressbar(self.main_frame, mode='indeterminate')
        self.progress_bar.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Status
        self.status_var = tk.StringVar(value="Ready")
        ttk.Label(self.main_frame, textvariable=self.status_var, foreground="green").grid(row=6, column=0, columnspan=3, pady=(5, 0))
        
        # Log area
        log_frame = ttk.LabelFrame(self.main_frame, text="Log", padding="10")
        log_frame.grid(row=7, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        
        self.log_text = tk.Text(log_frame, height=10, width=80)
        log_scrollbar = ttk.Scrollbar(log_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=log_scrollbar.set)
        
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        log_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Configure grid weights for log frame
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
    
    def _setup_layout(self):
        """Setup the main layout and grid weights."""
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(7, weight=1)
    
    def browse_output_dir(self):
        """Browse for output directory."""
        directory = filedialog.askdirectory(initialdir=self.output_dir_var.get())
        if directory:
            self.output_dir_var.set(directory)
    
    def browse_excel_file(self):
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
    
    def load_excel_columns(self):
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
            
            self.log_message(f"Loaded Excel file with {len(columns)} columns")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load Excel file: {str(e)}")
            self.log_message(f"Error loading Excel file: {str(e)}", "ERROR")
    
    def preview_excel_urls(self):
        """Preview URLs from selected column."""
        excel_path = self.excel_file_var.get().strip()
        url_column = self.url_column_var.get().strip()
        
        if not excel_path or not url_column:
            messagebox.showerror("Error", "Please select Excel file and URL column first")
            return
        
        try:
            # Use Excel loader to get preview
            preview_text = self.excel_loader.get_excel_preview(excel_path, url_column, max_preview=5)
            
            # Get valid URLs for additional info
            urls = self.excel_loader.extract_urls_from_column(excel_path, url_column, self.download_manager.validate_url)
            valid_urls = self.download_manager.validate_urls(urls)
            
            # Enhance preview with validation info
            enhanced_preview = f"Total URLs in column '{url_column}': {len(urls)}\n"
            enhanced_preview += f"Valid TikTok URLs: {len(valid_urls)}\n\n"
            enhanced_preview += preview_text
            
            messagebox.showinfo("URL Preview", enhanced_preview)
            self.log_message(f"Preview: {len(valid_urls)} valid URLs found in Excel")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to preview URLs: {str(e)}")
            self.log_message(f"Error previewing URLs: {str(e)}", "ERROR")
    
    def get_excel_urls(self) -> list:
        """Get URLs from Excel file."""
        excel_path = self.excel_file_var.get().strip()
        url_column = self.url_column_var.get().strip()
        
        if not excel_path or not url_column:
            return []
        
        try:
            # Use Excel loader to extract URLs with validation
            urls = self.excel_loader.extract_urls_from_column(
                excel_path, 
                url_column, 
                self.download_manager.validate_url
            )
            
            return urls
            
        except Exception as e:
            self.log_message(f"Error reading Excel file: {str(e)}", "ERROR")
            return []
    
    def start_excel_download(self):
        """Start download process from Excel file."""
        urls = self.get_excel_urls()
        
        if not urls:
            messagebox.showerror("Error", "No valid TikTok URLs found in Excel file")
            return
        
        # Update UI state
        self.download_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.progress_bar.start()
        self.status_var.set("Downloading from Excel...")
        
        # Start download thread
        self.download_thread = threading.Thread(target=self.download_worker, args=(urls,))
        self.download_thread.daemon = True
        self.download_thread.start()
    
    def clear_log(self):
        """Clear log text area."""
        self.log_text.delete(1.0, tk.END)
    
    def log_message(self, message: str, level: str = "INFO"):
        """Add message to log with timestamp and level."""
        import datetime
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {level}: {message}\n"
        
        # Add to queue for thread-safe update
        self.message_queue.put(formatted_message)
    
    def process_messages(self):
        """Process messages from queue (thread-safe)."""
        try:
            while True:
                message = self.message_queue.get_nowait()
                self.log_text.insert(tk.END, message)
                self.log_text.see(tk.END)
                self.log_text.update_idletasks()
        except queue.Empty:
            pass
        
        # Schedule next check
        self.root.after(100, self.process_messages)
    
    def get_urls(self) -> list:
        """Get URLs from input (single or batch)."""
        if self.batch_mode_var.get():
            text = self.batch_text.get(1.0, tk.END)
            urls = [url.strip() for url in text.strip().split('\n') if url.strip()]
        else:
            url = self.url_var.get().strip()
            urls = [url] if url else []
        
        # Filter out empty URLs
        urls = [url for url in urls if url]
        
        if not urls:
            return []
        
        try:
            # Use the download manager's URL processor
            valid_urls, invalid_urls = self.download_manager.process_batch_text('\n'.join(urls))
            
            if invalid_urls:
                self.log_message(f"Found {len(invalid_urls)} invalid URLs", "WARNING")
                for invalid_url in invalid_urls:
                    self.log_message(f"  Invalid: {invalid_url}", "WARNING")
            
            if valid_urls:
                self.log_message(f"Found {len(valid_urls)} valid URLs", "INFO")
                for valid_url in valid_urls:
                    self.log_message(f"  Valid: {valid_url}", "INFO")
            
            return valid_urls
            
        except Exception as e:
            self.log_message(f"Error processing URLs: {str(e)}", "ERROR")
            return []
    
    def start_download(self):
        """Start download process in separate thread."""
        urls = self.get_urls()
        
        if not urls:
            messagebox.showerror("Error", "Please enter valid TikTok URL(s)")
            return
        
        # Update UI state
        self.download_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.progress_bar.start()
        self.status_var.set("Downloading...")
        
        # Start download thread
        self.download_thread = threading.Thread(target=self.download_worker, args=(urls,))
        self.download_thread.daemon = True
        self.download_thread.start()
    
    def stop_download(self):
        """Stop download process."""
        self.status_var.set("Stopping...")
        # Note: yt-dlp doesn't have a built-in stop mechanism
        # This is a placeholder for future implementation
        self.finish_download()
    
    def download_worker(self, urls: list):
        """Worker thread for downloading videos."""
        try:
            # Update download manager settings
            self.download_manager.update_settings(
                output_dir=self.output_dir_var.get(),
                quality=self.quality_var.get(),
                extract_audio=self.audio_only_var.get(),
                add_metadata=self.metadata_var.get(),
                custom_base_name=self.custom_name_var.get().strip() if self.custom_name_var.get().strip() else None
            )
            
            self.log_message(f"Starting download of {len(urls)} video(s)")
            self.log_message(f"Output directory: {self.download_manager.output_dir}")
            self.log_message(f"Quality: {self.download_manager.quality}")
            
            # Download videos using the download manager
            results = self.download_manager.download_multiple_videos(
                urls, 
                export_to_excel=self.excel_export_var.get()
            )
            
            # Log results
            self.log_message(f"Download completed: {results['successful']}/{results['valid_urls']} successful")
            
            if self.excel_export_var.get() and results['excel_file']:
                self.log_message(f"Excel file saved: {results['excel_file']}", "SUCCESS")
            
        except Exception as e:
            self.log_message(f"Unexpected error: {str(e)}", "ERROR")
        
        finally:
            # Update UI on main thread
            self.root.after(0, self.finish_download)
    
    def finish_download(self):
        """Finish download process and update UI."""
        self.download_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.progress_bar.stop()
        self.status_var.set("Ready")
    
    def process_existing_downloads(self):
        """Process existing downloads and create Excel file."""
        try:
            # Update download manager settings
            self.download_manager.update_settings(
                output_dir=self.output_dir_var.get(),
                custom_base_name=self.custom_name_var.get().strip() if self.custom_name_var.get().strip() else None
            )
            
            self.log_message("Processing existing downloads for Excel export...")
            self.status_var.set("Processing existing downloads...")
            
            # Process in separate thread
            process_thread = threading.Thread(target=self.process_existing_worker)
            process_thread.daemon = True
            process_thread.start()
            
        except Exception as e:
            self.log_message(f"Error starting process: {str(e)}", "ERROR")
    
    def process_existing_worker(self):
        """Worker thread for processing existing downloads."""
        try:
            result = self.download_manager.process_existing_downloads(export_to_excel=True)
            
            if result['processed'] > 0:
                self.log_message(f"Successfully processed {result['processed']} existing downloads", "SUCCESS")
                self.log_message(f"Excel file saved: {result['excel_file']}", "SUCCESS")
            else:
                self.log_message("No existing downloads found to process", "INFO")
            
        except Exception as e:
            self.log_message(f"Error processing existing downloads: {str(e)}", "ERROR")
        
        finally:
            # Update UI on main thread
            self.root.after(0, lambda: self.status_var.set("Ready"))
    
    def run(self):
        """Run the GUI application."""
        try:
            self.root.mainloop()
        except Exception as e:
            logger.error(f"GUI error: {e}")
            raise


def main():
    """Main function to run the GUI."""
    try:
        app = TikTokDownloaderGUI()
        app.run()
    except Exception as e:
        print(f"Failed to start GUI: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
