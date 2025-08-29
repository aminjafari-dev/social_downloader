"""
Video Text Remover GUI

A graphical user interface for removing text overlays from videos.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import queue
import os
from pathlib import Path
from video_text_remover import VideoTextRemover


class TextRemoverGUI:
    """
    GUI class for video text remover.
    
    This class provides a user-friendly interface for removing text from videos
    with options to select input/output files and processing methods.
    """
    
    def __init__(self):
        """Initialize the GUI application."""
        self.root = tk.Tk()
        self.root.title("Video Text Remover")
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        
        self.message_queue = queue.Queue()
        
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
        
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'))
        style.configure('Heading.TLabel', font=('Arial', 12, 'bold'))
        style.configure('Success.TLabel', foreground='green')
        style.configure('Error.TLabel', foreground='red')
    
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
        title_label = ttk.Label(main_frame, text="Video Text Remover", style='Title.TLabel')
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Input file section
        self.create_input_section(main_frame)
        
        # Output file section
        self.create_output_section(main_frame)
        
        # Options section
        self.create_options_section(main_frame)
        
        # Process button
        self.create_process_section(main_frame)
        
        # Progress and log section
        self.create_progress_section(main_frame)
        
        # Status bar
        self.create_status_bar(main_frame)
    
    def create_input_section(self, parent):
        """Create input file selection section."""
        input_frame = ttk.LabelFrame(parent, text="Input Video", padding="10")
        input_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        input_frame.columnconfigure(1, weight=1)
        
        ttk.Label(input_frame, text="Video File:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        
        self.input_var = tk.StringVar()
        input_entry = ttk.Entry(input_frame, textvariable=self.input_var, width=50)
        input_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        
        browse_btn = ttk.Button(input_frame, text="Browse", command=self.browse_input_file)
        browse_btn.grid(row=0, column=2)
    
    def create_output_section(self, parent):
        """Create output file selection section."""
        output_frame = ttk.LabelFrame(parent, text="Output Video", padding="10")
        output_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        output_frame.columnconfigure(1, weight=1)
        
        ttk.Label(output_frame, text="Output File:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        
        self.output_var = tk.StringVar()
        output_entry = ttk.Entry(output_frame, textvariable=self.output_var, width=50)
        output_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        
        save_btn = ttk.Button(output_frame, text="Save As", command=self.browse_output_file)
        save_btn.grid(row=0, column=2)
    
    def create_options_section(self, parent):
        """Create processing options section."""
        options_frame = ttk.LabelFrame(parent, text="Processing Options", padding="10")
        options_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Method selection
        ttk.Label(options_frame, text="Removal Method:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        
        self.method_var = tk.StringVar(value="inpaint")
        method_combo = ttk.Combobox(options_frame, textvariable=self.method_var, 
                                  values=["inpaint", "blur", "crop"], 
                                  state="readonly", width=15)
        method_combo.grid(row=0, column=1, sticky=tk.W, padx=(0, 20))
        
        # Method descriptions
        method_desc = {
            "inpaint": "Best quality - fills text areas with surrounding content",
            "blur": "Fast - blurs text areas",
            "crop": "Simple - crops top portion (if text is at top)"
        }
        
        self.method_desc_label = ttk.Label(options_frame, text=method_desc["inpaint"], 
                                         foreground="gray", font=("Arial", 9))
        self.method_desc_label.grid(row=0, column=2, sticky=tk.W, padx=(20, 0))
        
        # Update description when method changes
        method_combo.bind('<<ComboboxSelected>>', self.update_method_description)
        
        # Preview checkbox
        self.preview_var = tk.BooleanVar()
        preview_check = ttk.Checkbutton(options_frame, text="Show Preview Windows", 
                                       variable=self.preview_var)
        preview_check.grid(row=1, column=0, columnspan=3, sticky=tk.W, pady=(10, 0))
    
    def create_process_section(self, parent):
        """Create process control section."""
        process_frame = ttk.Frame(parent)
        process_frame.grid(row=4, column=0, columnspan=3, pady=(0, 10))
        
        self.process_btn = ttk.Button(process_frame, text="Remove Text from Video", 
                                    command=self.start_processing, style='Accent.TButton')
        self.process_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.stop_btn = ttk.Button(process_frame, text="Stop", command=self.stop_processing, 
                                 state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT)
    
    def create_progress_section(self, parent):
        """Create progress and log section."""
        progress_frame = ttk.LabelFrame(parent, text="Progress & Log", padding="10")
        progress_frame.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        progress_frame.columnconfigure(0, weight=1)
        progress_frame.rowconfigure(1, weight=1)
        parent.rowconfigure(5, weight=1)
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, 
                                          mode='indeterminate')
        self.progress_bar.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Log text area
        self.log_text = tk.Text(progress_frame, height=12, width=70)
        log_scrollbar = ttk.Scrollbar(progress_frame, orient="vertical", command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=log_scrollbar.set)
        
        self.log_text.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        log_scrollbar.grid(row=1, column=1, sticky=(tk.N, tk.S))
        
        # Clear log button
        clear_log_btn = ttk.Button(progress_frame, text="Clear Log", command=self.clear_log)
        clear_log_btn.grid(row=2, column=0, sticky=tk.W, pady=(10, 0))
    
    def create_status_bar(self, parent):
        """Create status bar."""
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(parent, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E))
    
    def update_method_description(self, event=None):
        """Update method description when selection changes."""
        method_desc = {
            "inpaint": "Best quality - fills text areas with surrounding content",
            "blur": "Fast - blurs text areas",
            "crop": "Simple - crops top portion (if text is at top)"
        }
        selected_method = self.method_var.get()
        self.method_desc_label.config(text=method_desc.get(selected_method, ""))
    
    def browse_input_file(self):
        """Browse for input video file."""
        filetypes = [
            ("Video files", "*.mp4 *.avi *.mov *.mkv *.wmv"),
            ("MP4 files", "*.mp4"),
            ("All files", "*.*")
        ]
        filename = filedialog.askopenfilename(
            title="Select Input Video",
            filetypes=filetypes
        )
        if filename:
            self.input_var.set(filename)
            # Auto-generate output filename
            input_path = Path(filename)
            output_path = input_path.parent / f"{input_path.stem}_clean{input_path.suffix}"
            self.output_var.set(str(output_path))
    
    def browse_output_file(self):
        """Browse for output video file."""
        filetypes = [
            ("MP4 files", "*.mp4"),
            ("Video files", "*.mp4 *.avi *.mov *.mkv"),
            ("All files", "*.*")
        ]
        filename = filedialog.asksaveasfilename(
            title="Save Output Video As",
            filetypes=filetypes,
            defaultextension=".mp4"
        )
        if filename:
            self.output_var.set(filename)
    
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
    
    def start_processing(self):
        """Start video processing in separate thread."""
        input_file = self.input_var.get().strip()
        output_file = self.output_var.get().strip()
        method = self.method_var.get()
        show_preview = self.preview_var.get()
        
        if not input_file:
            messagebox.showerror("Error", "Please select an input video file")
            return
        
        if not output_file:
            messagebox.showerror("Error", "Please select an output video file")
            return
        
        if not os.path.exists(input_file):
            messagebox.showerror("Error", f"Input file not found: {input_file}")
            return
        
        # Update UI state
        self.process_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.progress_bar.start()
        self.status_var.set("Processing...")
        
        # Start processing thread
        self.processing_thread = threading.Thread(
            target=self.processing_worker, 
            args=(input_file, output_file, method, show_preview)
        )
        self.processing_thread.daemon = True
        self.processing_thread.start()
    
    def stop_processing(self):
        """Stop video processing."""
        self.status_var.set("Stopping...")
        # Note: This is a placeholder for future implementation
        self.finish_processing()
    
    def processing_worker(self, input_file, output_file, method, show_preview):
        """Worker thread for video processing."""
        try:
            self.log_message(f"Starting text removal process")
            self.log_message(f"Input: {input_file}")
            self.log_message(f"Output: {output_file}")
            self.log_message(f"Method: {method}")
            
            # Create text remover
            remover = VideoTextRemover(
                input_path=input_file,
                output_path=output_file,
                method=method
            )
            
            # Process video
            remover.process_video(show_preview=show_preview)
            
            self.log_message("Text removal completed successfully!", "SUCCESS")
            
        except Exception as e:
            self.log_message(f"Error during processing: {str(e)}", "ERROR")
        
        finally:
            # Update UI on main thread
            self.root.after(0, self.finish_processing)
    
    def finish_processing(self):
        """Finish processing and update UI."""
        self.process_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.progress_bar.stop()
        self.status_var.set("Ready")
    
    def run(self):
        """Start the GUI application."""
        self.root.mainloop()


def main():
    """Main function to start the GUI application."""
    try:
        app = TextRemoverGUI()
        app.run()
    except Exception as e:
        print(f"Error starting GUI: {e}")
        messagebox.showerror("Error", f"Failed to start application: {e}")


if __name__ == "__main__":
    main()
