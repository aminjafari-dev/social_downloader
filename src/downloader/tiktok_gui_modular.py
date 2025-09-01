"""
TikTok Video Downloader GUI - Modular Version

A modular graphical user interface for downloading TikTok videos using the new architecture.
This version separates the GUI into logical components for better maintainability and reusability.

Usage:
    # Run the modular GUI
    python tiktok_gui_modular.py
    
    # Or import and use programmatically
    from tiktok_gui_modular import TikTokDownloaderModularGUI
    gui = TikTokDownloaderModularGUI()
    gui.run()
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import os
from pathlib import Path
from typing import List

# Import our modular components
try:
    from .components import (
        VideoURLComponent,
        BatchModeComponent,
        DownloadSettingsComponent,
        ExcelIntegrationComponent,
        LogComponent
    )
except ImportError:
    try:
        from components import (
            VideoURLComponent,
            BatchModeComponent,
            DownloadSettingsComponent,
            ExcelIntegrationComponent,
            LogComponent
        )
    except ImportError:
        # Fallback for when running the file directly
        import sys
        import os
        sys.path.append(os.path.join(os.path.dirname(__file__), 'components'))
        from components import (
            VideoURLComponent,
            BatchModeComponent,
            DownloadSettingsComponent,
            ExcelIntegrationComponent,
            LogComponent
        )

# Import core functionality
try:
    from ..core import DownloadManager
except ImportError:
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
    from ..utils.excel_loader import ExcelLoader
except ImportError:
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


class TikTokDownloaderModularGUI:
    """
    Modular GUI class for TikTok video downloader using component-based architecture.
    
    This class orchestrates multiple GUI components to provide a comprehensive
    interface for downloading TikTok videos with options for single URLs, batch
    processing, and Excel integration.
    
    Attributes:
        root (tk.Tk): Main tkinter window
        download_manager (DownloadManager): Core download manager instance
        excel_loader (ExcelLoader): Excel loader utility
        components (dict): Dictionary containing all GUI components
        download_thread (threading.Thread): Thread for download operations
    """
    
    def __init__(self):
        """Initialize the modular GUI application."""
        self.root = tk.Tk()
        self.root.title("TikTok Video Downloader - Modular Version")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        
        # Initialize core components
        self.download_manager = DownloadManager(
            output_dir="downloads",
            quality="best",
            extract_audio=False,
            add_metadata=False,  # Changed to False by default
            custom_base_name="tiktok_video",  # Added default custom name
            platform="tiktok"
        )
        
        self.excel_loader = ExcelLoader()
        
        # Initialize GUI components
        self.components = {}
        self.download_thread = None
        
        # Create GUI elements
        self._create_widgets()
        self._setup_layout()
        self._setup_callbacks()
        
        # Start message processing
        self.root.after(100, self._process_messages)
        
        # Update Excel file status display
        self._update_excel_file_status()
        
        logger.info("TikTok Downloader Modular GUI initialized")
    
    def _create_widgets(self):
        """Create all GUI widgets and components with scrollable functionality."""
        # Create main scrollable frame
        self._create_scrollable_frame()
        
        # Title and control buttons
        title_frame = ttk.Frame(self.content_frame)
        title_frame.grid(row=0, column=0, columnspan=2, pady=(0, 20), sticky=(tk.W, tk.E))
        
        title_label = ttk.Label(
            title_frame, 
            text="TikTok Video Downloader - Modular Architecture", 
            style='Title.TLabel'
        )
        title_label.pack(side=tk.LEFT)
        
        # Control buttons on the right side
        control_frame = ttk.Frame(title_frame)
        control_frame.pack(side=tk.RIGHT)
        
        ttk.Button(
            control_frame, 
            text="Reset All", 
            command=self._reset_all
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(
            control_frame, 
            text="Exit", 
            command=self._exit_application
        ).pack(side=tk.LEFT)
        
        # Configure title frame grid weights
        title_frame.columnconfigure(0, weight=1)
        
        # Create components
        self._create_components()
        
        # Configure grid weights for content frame
        self.content_frame.columnconfigure(0, weight=1)
        self.content_frame.rowconfigure(5, weight=1)  # Log component row
    
    def _create_scrollable_frame(self):
        """
        Create a scrollable frame that contains all the GUI content.
        
        This method creates a canvas with scrollbars that allows users to scroll
        through all the content when the window is resized to be small.
        """
        # Create main container frame
        self.main_container = ttk.Frame(self.root)
        self.main_container.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Create canvas for scrolling
        self.canvas = tk.Canvas(self.main_container, bg='white')
        
        # Create scrollbars
        self.v_scrollbar = ttk.Scrollbar(self.main_container, orient="vertical", command=self.canvas.yview)
        self.h_scrollbar = ttk.Scrollbar(self.main_container, orient="horizontal", command=self.canvas.xview)
        
        # Create the content frame that will be placed inside the canvas
        self.content_frame = ttk.Frame(self.canvas, padding="10")
        
        # Configure canvas scrolling
        self.canvas.configure(
            yscrollcommand=self.v_scrollbar.set,
            xscrollcommand=self.h_scrollbar.set
        )
        
        # Create a window inside the canvas to hold the content frame
        self.canvas_window = self.canvas.create_window((0, 0), window=self.content_frame, anchor="nw")
        
        # Configure grid layout for the main container
        self.main_container.grid_rowconfigure(0, weight=1)
        self.main_container.grid_columnconfigure(0, weight=1)
        
        # Place canvas and scrollbars
        self.canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.v_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.h_scrollbar.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        # Bind events for dynamic scrolling
        self._bind_scroll_events()
        
        # Configure root window grid weights
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
    
    def _bind_scroll_events(self):
        """
        Bind events to handle dynamic scrolling and canvas resizing.
        
        This method sets up event handlers to:
        - Update scroll region when content changes
        - Handle mouse wheel scrolling
        - Resize canvas window when main window is resized
        """
        # Bind mouse wheel scrolling with better cross-platform support
        self.canvas.bind("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind("<Button-4>", self._on_mousewheel)
        self.canvas.bind("<Button-5>", self._on_mousewheel)
        
        # Bind to the content frame as well for better coverage
        self.content_frame.bind("<MouseWheel>", self._on_mousewheel)
        self.content_frame.bind("<Button-4>", self._on_mousewheel)
        self.content_frame.bind("<Button-5>", self._on_mousewheel)
        
        # Bind window resize events
        self.content_frame.bind("<Configure>", self._on_frame_configure)
        self.canvas.bind("<Configure>", self._on_canvas_configure)
        
        # Bind mouse wheel to scrollbars for better cross-platform support
        self.v_scrollbar.bind("<MouseWheel>", self._on_mousewheel)
        self.h_scrollbar.bind("<MouseWheel>", self._on_mousewheel)
        
        # Bind to the main container for comprehensive coverage
        self.main_container.bind("<MouseWheel>", self._on_mousewheel)
        self.main_container.bind("<Button-4>", self._on_mousewheel)
        self.main_container.bind("<Button-5>", self._on_mousewheel)
        
        # Bind keyboard shortcuts for scrolling
        self.root.bind("<Up>", self._on_key_scroll_up)
        self.root.bind("<Down>", self._on_key_scroll_down)
        self.root.bind("<Page_Up>", self._on_key_scroll_page_up)
        self.root.bind("<Page_Down>", self._on_key_scroll_page_down)
        self.root.bind("<Home>", self._on_key_scroll_home)
        self.root.bind("<End>", self._on_key_scroll_end)
        
        # Bind to all child widgets for comprehensive mouse wheel support
        self._bind_mousewheel_to_children(self.root)
    
    def _bind_mousewheel_to_children(self, widget):
        """
        Recursively bind mouse wheel events to all child widgets.
        
        Args:
            widget: The widget to bind events to and search for children
        """
        try:
            # Bind to current widget
            widget.bind("<MouseWheel>", self._on_mousewheel)
            widget.bind("<Button-4>", self._on_mousewheel)
            widget.bind("<Button-5>", self._on_mousewheel)
            
            # Recursively bind to all children
            for child in widget.winfo_children():
                self._bind_mousewheel_to_children(child)
        except:
            pass  # Ignore binding errors
    
    def _on_key_scroll_up(self, event):
        """Handle Up arrow key for scrolling up."""
        self.canvas.yview_scroll(-1, "units")
        return "break"  # Prevent default behavior
    
    def _on_key_scroll_down(self, event):
        """Handle Down arrow key for scrolling down."""
        self.canvas.yview_scroll(1, "units")
        return "break"  # Prevent default behavior
    
    def _on_key_scroll_page_up(self, event):
        """Handle Page Up key for scrolling up one page."""
        self.canvas.yview_scroll(-1, "pages")
        return "break"  # Prevent default behavior
    
    def _on_key_scroll_page_down(self, event):
        """Handle Page Down key for scrolling down one page."""
        self.canvas.yview_scroll(1, "pages")
        return "break"  # Prevent default behavior
    
    def _on_key_scroll_home(self, event):
        """Handle Home key for scrolling to top."""
        self.canvas.yview_moveto(0)
        return "break"  # Prevent default behavior
    
    def _on_key_scroll_end(self, event):
        """Handle End key for scrolling to bottom."""
        self.canvas.yview_moveto(1)
        return "break"  # Prevent default behavior
    
    def _on_mousewheel(self, event):
        """
        Handle mouse wheel scrolling events with improved cross-platform support.
        
        Args:
            event: The mouse wheel event
        """
        try:
            # Handle different mouse wheel events across platforms
            if hasattr(event, 'num'):
                # Linux scroll events
                if event.num == 4:  # Linux scroll up
                    self.canvas.yview_scroll(-1, "units")
                elif event.num == 5:  # Linux scroll down
                    self.canvas.yview_scroll(1, "units")
            elif hasattr(event, 'delta'):
                # Windows/Mac scroll events
                if event.delta != 0:
                    # Normalize the delta value for consistent scrolling
                    scroll_amount = int(-1 * (event.delta / 120))
                    self.canvas.yview_scroll(scroll_amount, "units")
            else:
                # Fallback for other platforms or event types
                # Try to determine scroll direction from event state
                if hasattr(event, 'state'):
                    # Check if shift is pressed for horizontal scrolling
                    if event.state & 1:  # Shift key
                        if event.delta > 0:
                            self.canvas.xview_scroll(-1, "units")
                        else:
                            self.canvas.xview_scroll(1, "units")
                    else:
                        if event.delta > 0:
                            self.canvas.yview_scroll(-1, "units")
                        else:
                            self.canvas.yview_scroll(1, "units")
                else:
                    # Default vertical scrolling
                    self.canvas.yview_scroll(-1, "units")
                    
        except Exception as e:
            # Fallback scrolling if event handling fails
            try:
                self.canvas.yview_scroll(-1, "units")
            except:
                pass  # Silently fail if scrolling is not possible
    
    def _on_frame_configure(self, event=None):
        """
        Update the scroll region when the content frame is configured.
        
        Args:
            event: The configure event (optional)
        """
        # Update the scroll region to encompass the inner frame
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
    def _on_canvas_configure(self, event):
        """
        Resize the canvas window when the canvas is resized.
        
        Args:
            event: The configure event
        """
        # Update the width of the canvas window to match the canvas width
        self.canvas.itemconfig(self.canvas_window, width=event.width)
    
    def _create_components(self):
        """Create all GUI components."""
        # Video URL component
        self.components['video_url'] = VideoURLComponent(self.content_frame)
        self.components['video_url'].get_widget().grid(
            row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10)
        )
        
        # Batch mode component
        self.components['batch_mode'] = BatchModeComponent(self.content_frame)
        self.components['batch_mode'].get_widget().grid(
            row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10)
        )
        
        # Download settings component
        self.components['download_settings'] = DownloadSettingsComponent(
            self.content_frame,
            on_settings_changed=self._on_settings_changed
        )
        self.components['download_settings'].get_widget().grid(
            row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10)
        )
        
        # Excel integration component
        self.components['excel_integration'] = ExcelIntegrationComponent(
            self.content_frame, 
            self.excel_loader,
            on_url_validation=self.download_manager.validate_url
        )
        self.components['excel_integration'].get_widget().grid(
            row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10)
        )
        
        # Log component
        self.components['log'] = LogComponent(self.content_frame)
        self.components['log'].get_widget().grid(
            row=5, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0)
        )
    

    def _setup_callbacks(self):
        """Setup callback functions for components."""
        # Set Excel integration callbacks
        self.components['excel_integration'].set_callbacks(
            on_columns_loaded=self._on_excel_columns_loaded,
            on_excel_download_start=self._on_excel_download_start,
            on_process_existing=self._on_process_existing_downloads
        )
        # Set Video URL component download callback for single URL downloads
        self.components['video_url'].set_download_callback(self._start_download_with_urls)
    
    def _setup_layout(self):
        """Setup the main layout and grid weights."""
        # The layout is now handled in _create_scrollable_frame()
        # Grid weights are configured there for proper scrolling behavior
        pass
    
    def _on_excel_columns_loaded(self, columns: List[str]):
        """Callback when Excel columns are loaded."""
        self.components['log'].log_message(f"Loaded Excel file with {len(columns)} columns", "INFO")
    
    def _on_excel_download_start(self, urls: List[str]):
        """Callback when Excel download starts."""
        if not urls:
            messagebox.showerror("Error", "No valid TikTok URLs found in Excel file")
            return
        
        self._start_download_with_urls(urls, "Excel")
    
    def _on_process_existing_downloads(self):
        """Callback when processing existing downloads."""
        self._process_existing_downloads()
    
    def _update_excel_file_status(self):
        """Update the Excel file status display."""
        try:
            status_message = self.download_manager.get_excel_file_status_message()
            self.components['excel_integration'].set_excel_file_status(status_message)
        except Exception as e:
            logger.error(f"Error updating Excel file status: {e}")
            self.components['excel_integration'].set_excel_file_status("Error checking file status")
    
    def _on_settings_changed(self):
        """Callback when download settings change."""
        try:
            # Update download manager settings
            settings = self.components['download_settings'].get_settings()
            self.download_manager.update_settings(**settings)
            
            # Update Excel file status display
            self._update_excel_file_status()
            
            logger.info("Download settings updated and Excel status refreshed")
        except Exception as e:
            logger.error(f"Error updating settings: {e}")
    
    def _process_messages(self):
        """Process messages from all components."""
        # Process log component messages
        self.components['log'].process_messages()
        
        # Schedule next check
        self.root.after(100, self._process_messages)
    
    def _get_urls_from_input(self) -> List[str]:
        """Get URLs from both single and batch input components."""
        urls = []
        
        # Get single URL if not empty
        single_url = self.components['video_url'].get_url()
        if single_url:
            urls.append(single_url)
        
        # Get batch URLs if batch mode is enabled
        if self.components['batch_mode'].is_batch_mode_enabled():
            batch_urls = self.components['batch_mode'].get_urls()
            urls.extend(batch_urls)
        
        # Filter out empty URLs
        urls = [url for url in urls if url.strip()]
        
        if not urls:
            return []
        
        try:
            # Use the download manager's URL processor with better error handling
            batch_text = '\n'.join(urls)
            self.components['log'].log_message(f"Processing {len(urls)} URLs...", "INFO")
            
            # Call process_batch_text and handle the result safely
            result = self.download_manager.process_batch_text(batch_text)
            
            # Check if result is a tuple with 2 elements
            if not isinstance(result, tuple) or len(result) != 2:
                self.components['log'].log_message(
                    f"Unexpected result from process_batch_text: {type(result)}, value: {result}", 
                    "ERROR"
                )
                # Fallback: try to validate URLs individually
                valid_urls = []
                invalid_urls = []
                for url in urls:
                    if self.download_manager.primary_downloader.validate_url(url):
                        valid_urls.append(url)
                    else:
                        invalid_urls.append(url)
                
                if invalid_urls:
                    self.components['log'].log_message(f"Found {len(invalid_urls)} invalid URLs", "WARNING")
                    for invalid_url in invalid_urls:
                        self.components['log'].log_message(f"  Invalid: {invalid_url}", "WARNING")
                
                if valid_urls:
                    self.components['log'].log_message(f"Found {len(valid_urls)} valid URLs", "INFO")
                    for valid_url in valid_urls:
                        self.components['log'].log_message(f"  Valid: {valid_url}", "INFO")
                
                return valid_urls
            
            # Unpack the tuple safely
            valid_urls, invalid_urls = result
            
            if invalid_urls:
                self.components['log'].log_message(f"Found {len(invalid_urls)} invalid URLs", "WARNING")
                for invalid_url in invalid_urls:
                    self.components['log'].log_message(f"  Invalid: {invalid_url}", "WARNING")
            
            if valid_urls:
                self.components['log'].log_message(f"Found {len(valid_urls)} valid URLs", "INFO")
                for valid_url in valid_urls:
                    self.components['log'].log_message(f"  Valid: {valid_url}", "INFO")
            
            return valid_urls
            
        except Exception as e:
            self.components['log'].log_message(f"Error processing URLs: {str(e)}", "ERROR")
            self.components['log'].log_message(f"Error type: {type(e)}", "ERROR")
            import traceback
            self.components['log'].log_message(f"Traceback: {traceback.format_exc()}", "ERROR")
            return []
    
    def _start_download_with_urls(self, urls: List[str], source: str):
        """Start download process with specified URLs."""
        # Update UI state
        self.components['log'].start_progress()
        self.components['log'].set_status(f"Downloading from {source}...")
        
        # Start download thread
        self.download_thread = threading.Thread(
            target=self._download_worker, 
            args=(urls, source)
        )
        self.download_thread.daemon = True
        self.download_thread.start()
    
    def _download_worker(self, urls: List[str], source: str):
        """Worker thread for downloading videos."""
        try:
            # Get current settings from components
            settings = self.components['download_settings'].get_settings()
            
            self.components['log'].log_message(f"Download settings: {settings}", "INFO")
            
            # Update download manager settings
            self.download_manager.update_settings(**settings)
            
            self.components['log'].log_message(f"Starting download of {len(urls)} video(s) from {source}")
            self.components['log'].log_message(f"Output directory: {self.download_manager.output_dir}")
            self.components['log'].log_message(f"Quality: {self.download_manager.quality}")
            self.components['log'].log_message(f"Platform: {self.download_manager.platform}")
            
            # Log each URL being processed
            for i, url in enumerate(urls, 1):
                self.components['log'].log_message(f"URL {i}: {url}", "INFO")
            
            # Use different download method based on source and settings
            # Always use Excel-optimized method when export_to_excel is enabled
            # or when the source is explicitly Excel
            use_excel_method = (source == "Excel" or settings.get('export_to_excel', False))
            
            self.components['log'].log_message(f"Source: {source}, Export to Excel: {settings.get('export_to_excel', False)}", "INFO")
            self.components['log'].log_message(f"Using Excel method: {use_excel_method}", "INFO")
            
            if use_excel_method:
                # Use the new Excel-specific method for better metadata handling
                self.components['log'].log_message("Using Excel-optimized download method...", "INFO")
                
                # Create a progress callback for Excel downloads
                def progress_callback(current: int, total: int, video_title: str = ""):
                    self.root.after(0, lambda: self.components['excel_integration'].update_download_progress(
                        current, total, video_title
                    ))
                
                # Pass the progress callback to the download method
                results = self.download_manager.download_videos_from_excel(
                    urls, 
                    export_to_excel=settings['export_to_excel'],
                    progress_callback=progress_callback
                )
            else:
                # Use the standard method for other sources
                self.components['log'].log_message("Using standard download method...", "INFO")
                results = self.download_manager.download_multiple_videos(
                    urls, 
                    export_to_excel=settings['export_to_excel']
                )
            
            self.components['log'].log_message(f"Download results: {results}", "INFO")
            
            # Log results
            self.components['log'].log_message(
                f"Download completed: {results['successful']}/{results['valid_urls']} successful", 
                "SUCCESS"
            )
            
            if settings['export_to_excel'] and results['excel_file']:
                self.components['log'].log_message(
                    f"Excel file saved: {results['excel_file']}", 
                    "SUCCESS"
                )
            
            # Update Excel integration component status if it was an Excel download
            if source == "Excel":
                self.root.after(0, lambda: self.components['excel_integration'].set_status_message(
                    f"Download completed: {results['successful']}/{results['valid_urls']} videos processed successfully"
                ))
            
        except Exception as e:
            self.components['log'].log_message(f"Unexpected error: {str(e)}", "ERROR")
            self.components['log'].log_message(f"Error type: {type(e)}", "ERROR")
            import traceback
            self.components['log'].log_message(f"Traceback: {traceback.format_exc()}", "ERROR")
        
        finally:
            # Update UI on main thread
            self.root.after(0, self._finish_download)
    
    def _finish_download(self):
        """Finish download process and update UI."""
        self.components['log'].stop_progress()
        self.components['log'].set_status("Ready")
    
    def _process_existing_downloads(self):
        """Process existing downloads and create Excel file."""
        try:
            # Get current settings
            settings = self.components['download_settings'].get_settings()
            
            # Update download manager settings
            self.download_manager.update_settings(**settings)
            
            self.components['log'].log_message("Processing existing downloads for Excel export...")
            self.components['log'].set_status("Processing existing downloads...")
            
            # Process in separate thread
            process_thread = threading.Thread(target=self._process_existing_worker)
            process_thread.daemon = True
            process_thread.start()
            
        except Exception as e:
            self.components['log'].log_message(f"Error starting process: {str(e)}", "ERROR")
    
    def _process_existing_worker(self):
        """Worker thread for processing existing downloads."""
        try:
            result = self.download_manager.process_existing_downloads(export_to_excel=True)
            
            if result['processed'] > 0:
                self.components['log'].log_message(
                    f"Successfully processed {result['processed']} existing downloads", 
                    "SUCCESS"
                )
                self.components['log'].log_message(
                    f"Excel file saved: {result['excel_file']}", 
                    "SUCCESS"
                )
            else:
                self.components['log'].log_message("No existing downloads found to process", "INFO")
            
        except Exception as e:
            self.components['log'].log_message(f"Error processing existing downloads: {str(e)}", "ERROR")
        
        finally:
            # Update UI on main thread
            self.root.after(0, lambda: self.components['log'].set_status("Ready"))
    
    def _reset_all(self):
        """Reset all components to their default state."""
        try:
            # Reset video URL component
            self.components['video_url'].clear_url()
            
            # Reset batch mode component
            self.components['batch_mode'].clear_urls()
            self.components['batch_mode'].batch_mode_var.set(False)
            
            # Reset download settings component
            self.components['download_settings'].reset_to_defaults()
            
            # Reset Excel integration component
            self.components['excel_integration'].clear_selection()
            
            # Reset log component
            self.components['log'].clear_log()
            self.components['log'].set_status("Ready")
            
            self.components['log'].log_message("All components reset to defaults", "INFO")
            
        except Exception as e:
            self.components['log'].log_message(f"Error resetting components: {str(e)}", "ERROR")
    
    def _exit_application(self):
        """Exit the application."""
        if messagebox.askokcancel("Exit", "Are you sure you want to exit?"):
            self.root.quit()
    
    def run(self):
        """Run the GUI application."""
        try:
            self.root.mainloop()
        except Exception as e:
            logger.error(f"GUI error: {e}")
            raise


def main():
    """Main function to run the modular GUI."""
    try:
        app = TikTokDownloaderModularGUI()
        app.run()
    except Exception as e:
        print(f"Failed to start modular GUI: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
