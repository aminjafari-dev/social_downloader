"""
TikTok Video Downloader GUI

A graphical user interface for downloading TikTok videos using tkinter.
This provides an easy-to-use interface for users who prefer GUI over command line.

Usage:
    python tiktok_gui.py
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import queue
import os
from pathlib import Path
from typing import Optional
import yt_dlp
from colorama import Fore, Style
import re

# Import our downloader class
from tiktok_downloader import TikTokDownloader


class TikTokDownloaderGUI:
    """
    GUI class for TikTok video downloader.
    
    This class provides a user-friendly interface for downloading TikTok videos
    with features like drag-and-drop, batch processing, and real-time progress updates.
    
    Attributes:
        root (tk.Tk): Main tkinter window
        downloader (TikTokDownloader): Instance of the downloader class
        message_queue (queue.Queue): Queue for thread-safe message updates
    """
    
    def __init__(self):
        """Initialize the GUI application."""
        self.root = tk.Tk()
        self.root.title("TikTok Video Downloader")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # Initialize downloader
        self.downloader = TikTokDownloader()
        self.message_queue = queue.Queue()
        
        # Excel export variables
        self.excel_export_var = tk.BooleanVar(value=True)
        self.excel_filename_var = tk.StringVar(value="tiktok_videos_metadata.xlsx")
        
        # Configure styles
        self.setup_styles()
        
        # Create GUI elements
        self.create_widgets()
        
        # Start message processing
        self.process_messages()
    
    def setup_styles(self):
        """Configure ttk styles for a modern look."""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'))
        style.configure('Heading.TLabel', font=('Arial', 12, 'bold'))
        style.configure('Success.TLabel', foreground='green')
        style.configure('Error.TLabel', foreground='red')
        style.configure('Info.TLabel', foreground='blue')
    
    def create_widgets(self):
        """Create and arrange all GUI widgets."""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="TikTok Video Downloader", style='Title.TLabel')
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # URL input section
        self.create_url_section(main_frame)
        
        # Options section
        self.create_options_section(main_frame)
        
        # Download button
        self.create_download_section(main_frame)
        
        # Progress and log section
        self.create_progress_section(main_frame)
        
        # Status bar
        self.create_status_bar(main_frame)
    
    def create_url_section(self, parent):
        """Create URL input section."""
        # URL input frame
        url_frame = ttk.LabelFrame(parent, text="Video URL", padding="10")
        url_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        url_frame.columnconfigure(1, weight=1)
        
        # URL label
        ttk.Label(url_frame, text="TikTok URL:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        
        # URL entry
        self.url_var = tk.StringVar()
        self.url_entry = ttk.Entry(url_frame, textvariable=self.url_var, width=60)
        self.url_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        
        # Paste button
        paste_btn = ttk.Button(url_frame, text="Paste", command=self.paste_url)
        paste_btn.grid(row=0, column=2, padx=(0, 10))
        
        # Clear button
        clear_btn = ttk.Button(url_frame, text="Clear", command=self.clear_url)
        clear_btn.grid(row=0, column=3)
        
        # Batch mode checkbox
        self.batch_mode_var = tk.BooleanVar()
        batch_check = ttk.Checkbutton(url_frame, text="Batch Mode (one URL per line)", 
                                    variable=self.batch_mode_var, command=self.toggle_batch_mode)
        batch_check.grid(row=1, column=0, columnspan=4, sticky=tk.W, pady=(10, 0))
        
        # Batch text area (initially hidden)
        self.batch_text = scrolledtext.ScrolledText(url_frame, height=5, width=70)
        self.batch_text.grid(row=2, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=(10, 0))
        self.batch_text.grid_remove()  # Hidden by default
    
    def create_options_section(self, parent):
        """Create download options section."""
        # Options frame
        options_frame = ttk.LabelFrame(parent, text="Download Options", padding="10")
        options_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Output directory
        ttk.Label(options_frame, text="Output Directory:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        
        self.output_dir_var = tk.StringVar(value="downloads")
        output_entry = ttk.Entry(options_frame, textvariable=self.output_dir_var, width=40)
        output_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        
        browse_btn = ttk.Button(options_frame, text="Browse", command=self.browse_output_dir)
        browse_btn.grid(row=0, column=2)
        
        # Quality selection
        ttk.Label(options_frame, text="Quality:").grid(row=1, column=0, sticky=tk.W, padx=(0, 10), pady=(10, 0))
        
        self.quality_var = tk.StringVar(value="best")
        quality_combo = ttk.Combobox(options_frame, textvariable=self.quality_var, 
                                   values=["best", "worst", "720p", "480p", "360p"], 
                                   state="readonly", width=15)
        quality_combo.grid(row=1, column=1, sticky=tk.W, padx=(0, 10), pady=(10, 0))
        
        # Audio only checkbox
        self.audio_only_var = tk.BooleanVar()
        audio_check = ttk.Checkbutton(options_frame, text="Audio Only", variable=self.audio_only_var)
        audio_check.grid(row=1, column=2, sticky=tk.W, pady=(10, 0))
        
        # Metadata checkbox
        self.metadata_var = tk.BooleanVar(value=True)
        metadata_check = ttk.Checkbutton(options_frame, text="Include Metadata", variable=self.metadata_var)
        metadata_check.grid(row=2, column=0, columnspan=3, sticky=tk.W, pady=(10, 0))
        
        # Excel export checkbox
        self.excel_export_var = tk.BooleanVar(value=True)
        excel_check = ttk.Checkbutton(options_frame, text="Export to Excel", variable=self.excel_export_var)
        excel_check.grid(row=3, column=0, columnspan=3, sticky=tk.W, pady=(10, 0))
        
        # Excel filename
        ttk.Label(options_frame, text="Excel Filename:").grid(row=4, column=0, sticky=tk.W, padx=(0, 10), pady=(10, 0))
        
        self.excel_filename_var = tk.StringVar(value="tiktok_videos_metadata.xlsx")
        excel_entry = ttk.Entry(options_frame, textvariable=self.excel_filename_var, width=30)
        excel_entry.grid(row=4, column=1, sticky=tk.W, padx=(0, 10), pady=(10, 0))
        
        # Process existing button
        process_existing_btn = ttk.Button(options_frame, text="Process Existing Downloads", 
                                        command=self.process_existing_downloads)
        process_existing_btn.grid(row=5, column=0, columnspan=3, sticky=tk.W, pady=(10, 0))
    
    def create_download_section(self, parent):
        """Create download control section."""
        # Download frame
        download_frame = ttk.Frame(parent)
        download_frame.grid(row=3, column=0, columnspan=3, pady=(0, 10))
        
        # Download button
        self.download_btn = ttk.Button(download_frame, text="Download Video", 
                                     command=self.start_download, style='Accent.TButton')
        self.download_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Stop button
        self.stop_btn = ttk.Button(download_frame, text="Stop", command=self.stop_download, state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT)
    
    def create_progress_section(self, parent):
        """Create progress and log section."""
        # Progress frame
        progress_frame = ttk.LabelFrame(parent, text="Progress & Log", padding="10")
        progress_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        progress_frame.columnconfigure(0, weight=1)
        progress_frame.rowconfigure(1, weight=1)
        parent.rowconfigure(4, weight=1)
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, 
                                          mode='indeterminate')
        self.progress_bar.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Log text area
        self.log_text = scrolledtext.ScrolledText(progress_frame, height=15, width=80)
        self.log_text.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Clear log button
        clear_log_btn = ttk.Button(progress_frame, text="Clear Log", command=self.clear_log)
        clear_log_btn.grid(row=2, column=0, sticky=tk.W, pady=(10, 0))
    
    def create_status_bar(self, parent):
        """Create status bar."""
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(parent, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E))
    
    def toggle_batch_mode(self):
        """Toggle between single URL and batch mode."""
        if self.batch_mode_var.get():
            self.url_entry.grid_remove()
            self.batch_text.grid()
        else:
            self.batch_text.grid_remove()
            self.url_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
    
    def paste_url(self):
        """Paste URL from clipboard."""
        try:
            clipboard_text = self.root.clipboard_get()
            if self.batch_mode_var.get():
                self.batch_text.insert(tk.END, clipboard_text + "\n")
            else:
                self.url_var.set(clipboard_text)
        except tk.TclError:
            messagebox.showwarning("Clipboard Error", "No text in clipboard")
    
    def clear_url(self):
        """Clear URL input."""
        if self.batch_mode_var.get():
            self.batch_text.delete(1.0, tk.END)
        else:
            self.url_var.set("")
    
    def browse_output_dir(self):
        """Browse for output directory."""
        directory = filedialog.askdirectory(initialdir=self.output_dir_var.get())
        if directory:
            self.output_dir_var.set(directory)
    
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
    
    def validate_urls(self, urls: list) -> list:
        """Validate and filter URLs."""
        valid_urls = []
        for url in urls:
            url = url.strip()
            if url and self.downloader.validate_url(url):
                valid_urls.append(url)
            elif url:
                self.log_message(f"Invalid URL: {url}", "WARNING")
        
        return valid_urls
    
    def get_urls(self) -> list:
        """Get URLs from input (single or batch)."""
        if self.batch_mode_var.get():
            text = self.batch_text.get(1.0, tk.END)
            urls = text.strip().split('\n')
        else:
            url = self.url_var.get().strip()
            urls = [url] if url else []
        
        return self.validate_urls(urls)
    
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
            # Update downloader settings
            self.downloader.output_dir = Path(self.output_dir_var.get())
            self.downloader.quality = self.quality_var.get()
            self.downloader.extract_audio = self.audio_only_var.get()
            self.downloader.add_metadata = self.metadata_var.get()
            self.downloader.ydl_opts = self.downloader._configure_ydl_options()
            
            # Set Excel export settings
            if self.excel_export_var.get():
                excel_path = self.downloader.output_dir / self.excel_filename_var.get()
                self.downloader.excel_file = excel_path
                self.log_message("Excel export enabled")
            
            # Create output directory
            self.downloader.output_dir.mkdir(exist_ok=True)
            
            self.log_message(f"Starting download of {len(urls)} video(s)")
            self.log_message(f"Output directory: {self.downloader.output_dir}")
            self.log_message(f"Quality: {self.downloader.quality}")
            
            # Download videos
            for i, url in enumerate(urls, 1):
                self.log_message(f"Processing video {i}/{len(urls)}: {url}")
                
                try:
                    success = self.downloader.download_video(url)
                    if success:
                        self.log_message(f"Successfully downloaded video {i}", "SUCCESS")
                    else:
                        self.log_message(f"Failed to download video {i}", "ERROR")
                except Exception as e:
                    self.log_message(f"Error downloading video {i}: {str(e)}", "ERROR")
            
            # Save Excel file if enabled
            if self.excel_export_var.get():
                self.log_message("Saving Excel file with metadata...")
                try:
                    self.downloader.save_excel_file()
                    self.log_message(f"Excel file saved: {self.downloader.excel_file}", "SUCCESS")
                except Exception as e:
                    self.log_message(f"Error saving Excel file: {str(e)}", "ERROR")
            
            self.log_message("Download process completed", "SUCCESS")
            
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
            # Update downloader settings
            self.downloader.output_dir = Path(self.output_dir_var.get())
            
            # Set Excel filename if specified
            if self.excel_filename_var.get():
                excel_path = self.downloader.output_dir / self.excel_filename_var.get()
                self.downloader.excel_file = excel_path
            
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
            self.downloader.process_existing_downloads()
            self.log_message("Successfully processed existing downloads", "SUCCESS")
            self.log_message(f"Excel file saved: {self.downloader.excel_file}", "SUCCESS")
            
        except Exception as e:
            self.log_message(f"Error processing existing downloads: {str(e)}", "ERROR")
        
        finally:
            # Update UI on main thread
            self.root.after(0, lambda: self.status_var.set("Ready"))
    
    def run(self):
        """Start the GUI application."""
        self.root.mainloop()


def main():
    """Main function to start the GUI application."""
    try:
        app = TikTokDownloaderGUI()
        app.run()
    except Exception as e:
        print(f"Error starting GUI: {e}")
        messagebox.showerror("Error", f"Failed to start application: {e}")


if __name__ == "__main__":
    main()
