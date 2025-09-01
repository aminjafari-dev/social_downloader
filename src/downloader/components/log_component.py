"""
Log Component

This component handles logging and status display functionality for the TikTok Downloader GUI.
It provides a scrollable text area for log messages, status updates, and progress tracking.

Usage:
    # Create the component
    log_component = LogComponent(parent_frame)
    
    # Add log message
    log_component.log_message("Download started", "INFO")
    
    # Clear log
    log_component.clear_log()
    
    # Get log content
    content = log_component.get_log_content()
"""

import tkinter as tk
from tkinter import ttk
import datetime
import queue
from typing import Optional


class LogComponent:
    """
    Component for handling logging and status display functionality.
    
    This component provides a comprehensive logging interface with timestamp support,
    log levels, and thread-safe message handling through a message queue.
    
    Attributes:
        parent (tk.Widget): Parent widget to contain this component
        log_text (tk.Text): Text widget for displaying log messages
        status_var (tk.StringVar): Variable to store current status
        progress_bar (ttk.Progressbar): Progress bar for download operations
        message_queue (queue.Queue): Queue for thread-safe message updates
        frame (ttk.LabelFrame): Main frame containing all log-related widgets
    """
    
    def __init__(self, parent: tk.Widget):
        """
        Initialize the LogComponent.
        
        Args:
            parent (tk.Widget): Parent widget to contain this component
        """
        self.parent = parent
        
        # Initialize variables
        self.status_var = tk.StringVar(value="Ready")
        self.message_queue = queue.Queue()
        
        self.frame = None
        self.log_text = None
        self.progress_bar = None
        
        self._create_widgets()
        self._setup_layout()
        
        # Start message processing
        self._schedule_message_processing()
    
    def _create_widgets(self):
        """Create all widgets for the log component."""
        # Create main frame
        self.frame = ttk.LabelFrame(self.parent, text="Log & Status", padding="10")
        
        # Progress bar
        self.progress_bar = ttk.Progressbar(self.frame, mode='indeterminate')
        self.progress_bar.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Status label
        ttk.Label(self.frame, textvariable=self.status_var, foreground="green").grid(
            row=1, column=0, columnspan=2, pady=(0, 10)
        )
        
        # Log area
        self.log_text = tk.Text(self.frame, height=10, width=80)
        log_scrollbar = ttk.Scrollbar(self.frame, orient=tk.VERTICAL, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=log_scrollbar.set)
        
        self.log_text.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        log_scrollbar.grid(row=2, column=1, sticky=(tk.N, tk.S))
        
        # Control buttons
        control_frame = ttk.Frame(self.frame)
        control_frame.grid(row=3, column=0, columnspan=2, pady=(10, 0))
        
        ttk.Button(control_frame, text="Clear Log", command=self.clear_log).pack(side=tk.LEFT)
        ttk.Button(control_frame, text="Copy Log", command=self.copy_log).pack(side=tk.LEFT, padx=(10, 0))
        ttk.Button(control_frame, text="Save Log", command=self.save_log).pack(side=tk.LEFT, padx=(10, 0))
        
        # Configure grid weights for proper expansion
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(2, weight=1)
    
    def _setup_layout(self):
        """Setup the layout and grid weights."""
        # Grid weights are configured in _create_widgets
        pass
    
    def _schedule_message_processing(self):
        """Schedule the next message processing cycle."""
        # This will be called by the parent GUI to process messages
        pass
    
    def process_messages(self):
        """
        Process messages from the queue (thread-safe).
        
        This method should be called periodically by the parent GUI to process
        queued log messages in a thread-safe manner.
        """
        try:
            while True:
                message = self.message_queue.get_nowait()
                self._add_message_direct(message)
        except queue.Empty:
            pass
    
    def _add_message_direct(self, message: str):
        """
        Add a message directly to the log (not thread-safe).
        
        Args:
            message (str): Message to add
        """
        self.log_text.insert(tk.END, message)
        self.log_text.see(tk.END)
        self.log_text.update_idletasks()
    
    def log_message(self, message: str, level: str = "INFO"):
        """
        Add a message to the log with timestamp and level.
        
        Args:
            message (str): The message to log
            level (str): Log level (INFO, WARNING, ERROR, SUCCESS, etc.)
        """
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {level}: {message}\n"
        
        # Add to queue for thread-safe update
        self.message_queue.put(formatted_message)
    
    def set_status(self, status: str, is_error: bool = False):
        """
        Set the current status message.
        
        Args:
            status (str): Status message to display
            is_error (bool): Whether this is an error status
        """
        self.status_var.set(status)
        
        # Update status color based on type
        if is_error:
            self.frame.winfo_children()[1].configure(foreground="red")  # Status label
        else:
            self.frame.winfo_children()[1].configure(foreground="green")  # Status label
    
    def start_progress(self):
        """Start the progress bar animation."""
        self.progress_bar.start()
    
    def stop_progress(self):
        """Stop the progress bar animation."""
        self.progress_bar.stop()
    
    def clear_log(self):
        """Clear the log text area."""
        self.log_text.delete(1.0, tk.END)
        self.log_message("Log cleared", "INFO")
    
    def copy_log(self):
        """Copy the current log content to clipboard."""
        try:
            log_content = self.get_log_content()
            self.parent.clipboard_clear()
            self.parent.clipboard_append(log_content)
            self.log_message("Log content copied to clipboard", "SUCCESS")
        except Exception as e:
            self.log_message(f"Failed to copy log: {str(e)}", "ERROR")
    
    def save_log(self):
        """Save the current log content to a file."""
        try:
            from tkinter import filedialog
            file_path = filedialog.asksaveasfilename(
                title="Save Log File",
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
            )
            
            if file_path:
                log_content = self.get_log_content()
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(log_content)
                
                self.log_message(f"Log saved to: {file_path}", "SUCCESS")
        except Exception as e:
            self.log_message(f"Failed to save log: {str(e)}", "ERROR")
    
    def get_log_content(self) -> str:
        """
        Get the current log content.
        
        Returns:
            str: Current log content as string
        """
        return self.log_text.get(1.0, tk.END)
    
    def get_log_line_count(self) -> int:
        """
        Get the number of lines in the log.
        
        Returns:
            int: Number of lines in the log
        """
        return int(self.log_text.index('end-1c').split('.')[0])
    
    def is_empty(self) -> bool:
        """
        Check if the log is empty.
        
        Returns:
            bool: True if log is empty, False otherwise
        """
        return self.get_log_line_count() == 0
    
    def scroll_to_bottom(self):
        """Scroll the log to the bottom to show the latest messages."""
        self.log_text.see(tk.END)
    
    def scroll_to_top(self):
        """Scroll the log to the top to show the earliest messages."""
        self.log_text.see("1.0")
    
    def find_text(self, search_text: str, case_sensitive: bool = False):
        """
        Find and highlight text in the log.
        
        Args:
            search_text (str): Text to search for
            case_sensitive (bool): Whether search should be case sensitive
        """
        if not search_text:
            return
        
        # Clear previous highlights
        self.log_text.tag_remove("search", "1.0", tk.END)
        
        # Configure search tag
        self.log_text.tag_configure("search", background="yellow")
        
        # Search and highlight
        start_pos = "1.0"
        while True:
            if case_sensitive:
                pos = self.log_text.search(search_text, start_pos, tk.END)
            else:
                pos = self.log_text.search(search_text, start_pos, tk.END, nocase=True)
            
            if not pos:
                break
            
            end_pos = f"{pos}+{len(search_text)}c"
            self.log_text.tag_add("search", pos, end_pos)
            start_pos = end_pos
        
        self.log_message(f"Found {search_text} in log", "INFO")
    
    def set_max_lines(self, max_lines: int):
        """
        Set maximum number of lines to keep in log.
        
        Args:
            max_lines (int): Maximum number of lines to keep
        """
        current_lines = self.get_log_line_count()
        if current_lines > max_lines:
            # Remove oldest lines
            lines_to_remove = current_lines - max_lines
            self.log_text.delete("1.0", f"{lines_to_remove + 1}.0")
    
    def get_widget(self) -> ttk.LabelFrame:
        """
        Get the main frame widget for this component.
        
        Returns:
            ttk.LabelFrame: The main frame containing all log-related widgets
        """
        return self.frame
