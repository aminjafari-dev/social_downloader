"""
Interactive Video Text Remover

A GUI application that shows video frames and allows manual selection of text areas
for precise text removal using LaMa inpainting.

Usage:
    python interactive_text_remover.py --input video.mp4
"""

import cv2
import numpy as np
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import queue
import os
import time
from pathlib import Path
import argparse
import logging
from typing import List, Tuple, Optional
import requests
import zipfile
from PIL import Image, ImageTk, ImageDraw


class VideoFrameSelector:
    """
    Interactive video frame selector with brush tool for text area selection.
    
    This class provides a GUI interface to view video frames and manually select
    text areas using a brush tool, then processes the video to remove selected areas.
    """
    
    def __init__(self, video_path: str):
        """
        Initialize the video frame selector.
        
        Args:
            video_path (str): Path to input video file
        """
        self.video_path = video_path
        self.cap = cv2.VideoCapture(video_path)
        
        if not self.cap.isOpened():
            raise ValueError(f"Could not open video file: {video_path}")
        
        # Video properties
        self.fps = int(self.cap.get(cv2.CAP_PROP_FPS))
        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        # Current frame
        self.current_frame_idx = 0
        self.current_frame = None
        self.mask = None
        self.brush_size = 20
        self.is_drawing = False
        self.last_x = None
        self.last_y = None
        
        # GUI elements
        self.root = None
        self.canvas = None
        self.photo = None
        self.message_queue = queue.Queue()
        
        # LaMa model
        self.lama_model = None
        
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def setup_gui(self):
        """Setup the GUI interface."""
        self.root = tk.Tk()
        self.root.title("Interactive Video Text Remover")
        self.root.geometry("1200x800")
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)
        
        # Create main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Interactive Video Text Remover", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Control panel
        self.create_control_panel(main_frame)
        
        # Video display
        self.create_video_display(main_frame)
        
        # Log panel
        self.create_log_panel(main_frame)
        
        # Status bar
        self.create_status_bar(main_frame)
        
        # Load first frame
        self.load_frame(0)
        
        # Start message processing
        self.process_messages()
    
    def create_control_panel(self, parent):
        """Create control panel with buttons and options."""
        control_frame = ttk.LabelFrame(parent, text="Controls", padding="10")
        control_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        # Frame navigation
        nav_frame = ttk.Frame(control_frame)
        nav_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(nav_frame, text="⏮ First", command=self.first_frame).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(nav_frame, text="⏪ Prev", command=self.prev_frame).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(nav_frame, text="⏩ Next", command=self.next_frame).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(nav_frame, text="⏭ Last", command=self.last_frame).pack(side=tk.LEFT)
        
        # Frame info
        self.frame_info_var = tk.StringVar(value="Frame: 0 / 0")
        ttk.Label(nav_frame, textvariable=self.frame_info_var).pack(side=tk.RIGHT)
        
        # Brush controls
        brush_frame = ttk.LabelFrame(control_frame, text="Brush Tool", padding="10")
        brush_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(brush_frame, text="Brush Size:").pack(anchor=tk.W)
        self.brush_size_var = tk.IntVar(value=self.brush_size)
        brush_scale = ttk.Scale(brush_frame, from_=5, to=50, variable=self.brush_size_var, 
                               orient=tk.HORIZONTAL, command=self.update_brush_size)
        brush_scale.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(brush_frame, text="Clear Mask", command=self.clear_mask).pack(fill=tk.X)
        
        # Processing controls
        process_frame = ttk.LabelFrame(control_frame, text="Processing", padding="10")
        process_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(process_frame, text="Download LaMa Model", 
                  command=self.download_lama_model).pack(fill=tk.X, pady=(0, 5))
        ttk.Button(process_frame, text="Process Video", 
                  command=self.process_video).pack(fill=tk.X)
        
        # Instructions
        instructions = """
Instructions:
1. Navigate through video frames
2. Use brush tool to select text areas
3. Adjust brush size as needed
4. Download LaMa model (first time)
5. Click "Process Video" to remove text
        """
        ttk.Label(control_frame, text=instructions, justify=tk.LEFT).pack(anchor=tk.W, pady=(10, 0))
    
    def create_video_display(self, parent):
        """Create video display canvas."""
        display_frame = ttk.LabelFrame(parent, text="Video Frame", padding="10")
        display_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        display_frame.columnconfigure(0, weight=1)
        display_frame.rowconfigure(0, weight=1)
        
        # Canvas for video display
        self.canvas = tk.Canvas(display_frame, bg="black")
        self.canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(display_frame, orient="vertical", command=self.canvas.yview)
        h_scrollbar = ttk.Scrollbar(display_frame, orient="horizontal", command=self.canvas.xview)
        self.canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        v_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        h_scrollbar.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        # Bind mouse events for brush tool
        self.canvas.bind("<Button-1>", self.start_drawing)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.stop_drawing)
    
    def create_log_panel(self, parent):
        """Create log panel."""
        log_frame = ttk.LabelFrame(parent, text="Log", padding="10")
        log_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        log_frame.columnconfigure(0, weight=1)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=8, width=100)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        ttk.Button(log_frame, text="Clear Log", command=self.clear_log).grid(row=1, column=0, sticky=tk.W, pady=(5, 0))
    
    def create_status_bar(self, parent):
        """Create status bar."""
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(parent, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
    
    def log_message(self, message: str, level: str = "INFO"):
        """Add message to log."""
        import datetime
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {level}: {message}\n"
        self.message_queue.put(formatted_message)
    
    def process_messages(self):
        """Process messages from queue."""
        try:
            while True:
                message = self.message_queue.get_nowait()
                self.log_text.insert(tk.END, message)
                self.log_text.see(tk.END)
                self.log_text.update_idletasks()
        except queue.Empty:
            pass
        
        self.root.after(100, self.process_messages)
    
    def update_brush_size(self, value):
        """Update brush size."""
        self.brush_size = int(value)
    
    def load_frame(self, frame_idx: int):
        """Load and display a specific frame."""
        if frame_idx < 0 or frame_idx >= self.total_frames:
            return
        
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
        ret, frame = self.cap.read()
        
        if ret:
            self.current_frame_idx = frame_idx
            self.current_frame = frame.copy()
            
            # Initialize mask if not exists
            if self.mask is None:
                self.mask = np.zeros((self.height, self.width), dtype=np.uint8)
            
            # Update frame info
            self.frame_info_var.set(f"Frame: {frame_idx + 1} / {self.total_frames}")
            
            # Display frame
            self.display_frame()
    
    def display_frame(self):
        """Display current frame with mask overlay."""
        if self.current_frame is None:
            return
        
        # Convert BGR to RGB
        frame_rgb = cv2.cvtColor(self.current_frame, cv2.COLOR_BGR2RGB)
        
        # Create mask overlay (red color)
        mask_overlay = np.zeros_like(frame_rgb)
        mask_overlay[self.mask > 0] = [255, 0, 0]  # Red color
        
        # Blend frame with mask overlay
        alpha = 0.3
        display_frame = cv2.addWeighted(frame_rgb, 1 - alpha, mask_overlay, alpha, 0)
        
        # Resize for display
        display_height, display_width = display_frame.shape[:2]
        max_width = 800
        max_height = 600
        
        if display_width > max_width or display_height > max_height:
            scale = min(max_width / display_width, max_height / display_height)
            new_width = int(display_width * scale)
            new_height = int(display_height * scale)
            display_frame = cv2.resize(display_frame, (new_width, new_height))
        
        # Convert to PIL Image
        pil_image = Image.fromarray(display_frame)
        self.photo = ImageTk.PhotoImage(pil_image)
        
        # Update canvas
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
    def start_drawing(self, event):
        """Start drawing on canvas."""
        self.is_drawing = True
        self.last_x = event.x
        self.last_y = event.y
    
    def draw(self, event):
        """Draw on canvas."""
        if not self.is_drawing or self.current_frame is None:
            return
        
        # Convert canvas coordinates to image coordinates
        scale_x = self.current_frame.shape[1] / self.canvas.winfo_width()
        scale_y = self.current_frame.shape[0] / self.canvas.winfo_height()
        
        x1 = int(self.last_x * scale_x)
        y1 = int(self.last_y * scale_y)
        x2 = int(event.x * scale_x)
        y2 = int(event.y * scale_y)
        
        # Draw line on mask
        cv2.line(self.mask, (x1, y1), (x2, y2), 255, self.brush_size)
        
        self.last_x = event.x
        self.last_y = event.y
        
        # Update display
        self.display_frame()
    
    def stop_drawing(self, event):
        """Stop drawing on canvas."""
        self.is_drawing = False
    
    def clear_mask(self):
        """Clear the current mask."""
        if self.mask is not None:
            self.mask = np.zeros((self.height, self.width), dtype=np.uint8)
            self.display_frame()
            self.log_message("Mask cleared")
    
    def first_frame(self):
        """Go to first frame."""
        self.load_frame(0)
    
    def prev_frame(self):
        """Go to previous frame."""
        self.load_frame(self.current_frame_idx - 1)
    
    def next_frame(self):
        """Go to next frame."""
        self.load_frame(self.current_frame_idx + 1)
    
    def last_frame(self):
        """Go to last frame."""
        self.load_frame(self.total_frames - 1)
    
    def clear_log(self):
        """Clear log text."""
        self.log_text.delete(1.0, tk.END)
    
    def download_lama_model(self):
        """Download LaMa model in background thread."""
        self.log_message("Starting LaMa model download...")
        self.status_var.set("Downloading LaMa model...")
        
        thread = threading.Thread(target=self._download_lama_model_worker)
        thread.daemon = True
        thread.start()
    
    def _download_lama_model_worker(self):
        """Worker thread for downloading LaMa model."""
        try:
            # Create models directory
            models_dir = Path("models")
            models_dir.mkdir(exist_ok=True)
            
            # Download LaMa model (simplified - you'd need the actual model URL)
            model_path = models_dir / "lama_model.pth"
            
            if model_path.exists():
                self.log_message("LaMa model already exists")
                self.root.after(0, lambda: self.status_var.set("Ready"))
                return
            
            # For now, create a placeholder
            self.log_message("LaMa model download not implemented yet")
            self.log_message("Please download LaMa model manually and place in models/ directory")
            
            self.root.after(0, lambda: self.status_var.set("Ready"))
            
        except Exception as e:
            self.log_message(f"Error downloading model: {e}", "ERROR")
            self.root.after(0, lambda: self.status_var.set("Error"))
    
    def process_video(self):
        """Process video to remove selected text areas."""
        if self.mask is None or np.sum(self.mask) == 0:
            messagebox.showwarning("Warning", "No areas selected for removal")
            return
        
        # Get output filename
        output_file = filedialog.asksaveasfilename(
            title="Save Processed Video",
            defaultextension=".mp4",
            filetypes=[("MP4 files", "*.mp4"), ("All files", "*.*")]
        )
        
        if not output_file:
            return
        
        self.log_message("Starting video processing...")
        self.status_var.set("Processing video...")
        
        # Start processing in background thread
        thread = threading.Thread(target=self._process_video_worker, args=(output_file,))
        thread.daemon = True
        thread.start()
    
    def _process_video_worker(self, output_file: str):
        """Worker thread for video processing."""
        try:
            # Initialize video writer
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(output_file, fourcc, self.fps, (self.width, self.height))
            
            # Process each frame
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            frame_count = 0
            
            while True:
                ret, frame = self.cap.read()
                if not ret:
                    break
                
                # Apply mask to current frame
                if self.mask is not None:
                    # For now, use simple inpainting
                    # In a real implementation, you'd use LaMa here
                    mask_resized = cv2.resize(self.mask, (self.width, self.height))
                    processed_frame = self.simple_inpaint(frame, mask_resized)
                else:
                    processed_frame = frame
                
                out.write(processed_frame)
                frame_count += 1
                
                if frame_count % 30 == 0:
                    self.log_message(f"Processed {frame_count}/{self.total_frames} frames")
            
            out.release()
            self.log_message(f"Video processing completed: {output_file}", "SUCCESS")
            self.root.after(0, lambda: self.status_var.set("Ready"))
            
        except Exception as e:
            self.log_message(f"Error processing video: {e}", "ERROR")
            self.root.after(0, lambda: self.status_var.set("Error"))
    
    def simple_inpaint(self, frame: np.ndarray, mask: np.ndarray) -> np.ndarray:
        """Simple inpainting using OpenCV (placeholder for LaMa)."""
        # Use OpenCV's inpainting as a placeholder
        # In real implementation, this would use LaMa
        return cv2.inpaint(frame, mask, 3, cv2.INPAINT_TELEA)
    
    def run(self):
        """Start the GUI application."""
        self.root.mainloop()
    
    def cleanup(self):
        """Cleanup resources."""
        if self.cap:
            self.cap.release()


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Interactive Video Text Remover")
    parser.add_argument('--input', '-i', required=True, help='Input video file')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.input):
        print(f"Error: Input file '{args.input}' not found")
        return
    
    try:
        app = VideoFrameSelector(args.input)
        app.setup_gui()
        app.run()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if 'app' in locals():
            app.cleanup()


if __name__ == "__main__":
    main()
