"""
Video Text Remover

A Python script to remove text overlays from videos using OpenCV and image processing.
This script can detect and remove text regions from video frames.

Usage:
    python video_text_remover.py --input video.mp4 --output clean_video.mp4
"""

import cv2
import numpy as np
import argparse
import os
from pathlib import Path
import logging
from typing import Tuple, List, Optional
import time


class VideoTextRemover:
    """
    A class to remove text overlays from videos using computer vision techniques.
    
    This class provides methods to detect and remove text regions from video frames
    using various image processing techniques including inpainting and blurring.
    
    Attributes:
        input_path (str): Path to input video file
        output_path (str): Path to output video file
        method (str): Text removal method ('inpaint', 'blur', 'crop')
        confidence_threshold (float): Confidence threshold for text detection
    """
    
    def __init__(self, input_path: str, output_path: str, method: str = 'inpaint', 
                 confidence_threshold: float = 0.5):
        """
        Initialize the video text remover.
        
        Args:
            input_path (str): Path to input video file
            output_path (str): Path to output video file
            method (str): Text removal method ('inpaint', 'blur', 'crop')
            confidence_threshold (float): Confidence threshold for text detection
        """
        self.input_path = input_path
        self.output_path = output_path
        self.method = method
        self.confidence_threshold = confidence_threshold
        
        # Initialize video capture
        self.cap = cv2.VideoCapture(input_path)
        if not self.cap.isOpened():
            raise ValueError(f"Could not open video file: {input_path}")
        
        # Get video properties
        self.fps = int(self.cap.get(cv2.CAP_PROP_FPS))
        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        # Initialize video writer
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.out = cv2.VideoWriter(output_path, fourcc, self.fps, (self.width, self.height))
        
        # Initialize logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Initialize text detection model (if available)
        self.text_detector = self._initialize_text_detector()
    
    def _initialize_text_detector(self):
        """
        Initialize text detection model.
        
        Returns:
            Optional: Text detection model or None if not available
        """
        try:
            # Try to use EAST text detector if available
            # You can download the model from: https://github.com/oyyd/frozen_east_text_detection.pb
            model_path = "frozen_east_text_detection.pb"
            if os.path.exists(model_path):
                return cv2.dnn.readNet(model_path)
            else:
                self.logger.warning("EAST text detection model not found. Using basic text detection.")
                return None
        except Exception as e:
            self.logger.warning(f"Could not initialize text detector: {e}")
            return None
    
    def detect_text_regions(self, frame: np.ndarray) -> List[Tuple[int, int, int, int]]:
        """
        Detect text regions in a frame.
        
        Args:
            frame (np.ndarray): Input frame
            
        Returns:
            List[Tuple[int, int, int, int]]: List of bounding boxes (x, y, w, h)
        """
        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Method 1: Simple threshold-based text detection
        # This works well for white text on dark backgrounds
        _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
        
        # Find contours
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        text_regions = []
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            
            # Filter by size (text regions are usually small and rectangular)
            if 20 < w < self.width // 2 and 10 < h < self.height // 4:
                # Check aspect ratio (text is usually wider than tall)
                aspect_ratio = w / h
                if 1.5 < aspect_ratio < 10:
                    text_regions.append((x, y, w, h))
        
        # Method 2: Edge detection for text boundaries
        edges = cv2.Canny(gray, 50, 150)
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            if 30 < w < self.width // 2 and 15 < h < self.height // 3:
                aspect_ratio = w / h
                if 2 < aspect_ratio < 8:
                    text_regions.append((x, y, w, h))
        
        # Remove overlapping regions
        return self._remove_overlapping_regions(text_regions)
    
    def _remove_overlapping_regions(self, regions: List[Tuple[int, int, int, int]]) -> List[Tuple[int, int, int, int]]:
        """
        Remove overlapping text regions.
        
        Args:
            regions (List[Tuple[int, int, int, int]]): List of bounding boxes
            
        Returns:
            List[Tuple[int, int, int, int]]: Filtered regions
        """
        if not regions:
            return []
        
        # Sort by area (largest first)
        regions = sorted(regions, key=lambda x: x[2] * x[3], reverse=True)
        
        filtered_regions = []
        for region in regions:
            x1, y1, w1, h1 = region
            is_overlapping = False
            
            for existing_region in filtered_regions:
                x2, y2, w2, h2 = existing_region
                
                # Check for overlap
                if (x1 < x2 + w2 and x1 + w1 > x2 and 
                    y1 < y2 + h2 and y1 + h1 > y2):
                    is_overlapping = True
                    break
            
            if not is_overlapping:
                filtered_regions.append(region)
        
        return filtered_regions
    
    def remove_text_inpaint(self, frame: np.ndarray, text_regions: List[Tuple[int, int, int, int]]) -> np.ndarray:
        """
        Remove text using inpainting technique.
        
        Args:
            frame (np.ndarray): Input frame
            text_regions (List[Tuple[int, int, int, int]]): Text regions to remove
            
        Returns:
            np.ndarray: Frame with text removed
        """
        # Create mask for text regions
        mask = np.zeros(frame.shape[:2], dtype=np.uint8)
        
        for x, y, w, h in text_regions:
            # Expand region slightly for better inpainting
            x1 = max(0, x - 5)
            y1 = max(0, y - 5)
            x2 = min(self.width, x + w + 5)
            y2 = min(self.height, y + h + 5)
            
            mask[y1:y2, x1:x2] = 255
        
        # Apply inpainting
        result = cv2.inpaint(frame, mask, 3, cv2.INPAINT_TELEA)
        return result
    
    def remove_text_blur(self, frame: np.ndarray, text_regions: List[Tuple[int, int, int, int]]) -> np.ndarray:
        """
        Remove text by blurring the regions.
        
        Args:
            frame (np.ndarray): Input frame
            text_regions (List[Tuple[int, int, int, int]]): Text regions to blur
            
        Returns:
            np.ndarray: Frame with text blurred
        """
        result = frame.copy()
        
        for x, y, w, h in text_regions:
            # Expand region slightly
            x1 = max(0, x - 10)
            y1 = max(0, y - 10)
            x2 = min(self.width, x + w + 10)
            y2 = min(self.height, y + h + 10)
            
            # Apply Gaussian blur
            region = result[y1:y2, x1:x2]
            blurred_region = cv2.GaussianBlur(region, (25, 25), 0)
            result[y1:y2, x1:x2] = blurred_region
        
        return result
    
    def remove_text_crop(self, frame: np.ndarray, text_regions: List[Tuple[int, int, int, int]]) -> np.ndarray:
        """
        Remove text by cropping the top portion (if text is at top).
        
        Args:
            frame (np.ndarray): Input frame
            text_regions (List[Tuple[int, int, int, int]]): Text regions to crop
            
        Returns:
            np.ndarray: Cropped frame
        """
        if not text_regions:
            return frame
        
        # Find the highest text region (top of screen)
        min_y = min(y for x, y, w, h in text_regions)
        
        # Crop from below the text region
        crop_y = min_y + 50  # Add some margin
        if crop_y < self.height:
            return frame[crop_y:, :]
        
        return frame
    
    def process_video(self, show_preview: bool = False):
        """
        Process the entire video to remove text.
        
        Args:
            show_preview (bool): Whether to show preview windows
        """
        self.logger.info(f"Processing video: {self.input_path}")
        self.logger.info(f"Output: {self.output_path}")
        self.logger.info(f"Method: {self.method}")
        self.logger.info(f"Total frames: {self.total_frames}")
        
        frame_count = 0
        start_time = time.time()
        
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break
            
            frame_count += 1
            
            # Detect text regions
            text_regions = self.detect_text_regions(frame)
            
            # Remove text based on selected method
            if self.method == 'inpaint':
                processed_frame = self.remove_text_inpaint(frame, text_regions)
            elif self.method == 'blur':
                processed_frame = self.remove_text_blur(frame, text_regions)
            elif self.method == 'crop':
                processed_frame = self.remove_text_crop(frame, text_regions)
            else:
                processed_frame = frame
            
            # Write processed frame
            self.out.write(processed_frame)
            
            # Show preview
            if show_preview and frame_count % 30 == 0:  # Show every 30th frame
                # Draw detected text regions on original frame
                debug_frame = frame.copy()
                for x, y, w, h in text_regions:
                    cv2.rectangle(debug_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                
                # Resize for display
                scale = 0.5
                debug_frame = cv2.resize(debug_frame, None, fx=scale, fy=scale)
                processed_frame_display = cv2.resize(processed_frame, None, fx=scale, fy=scale)
                
                cv2.imshow('Original with Text Detection', debug_frame)
                cv2.imshow('Processed Frame', processed_frame_display)
                
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            
            # Progress update
            if frame_count % 100 == 0:
                elapsed_time = time.time() - start_time
                fps_processed = frame_count / elapsed_time
                remaining_frames = self.total_frames - frame_count
                eta = remaining_frames / fps_processed if fps_processed > 0 else 0
                
                self.logger.info(f"Processed {frame_count}/{self.total_frames} frames "
                               f"({frame_count/self.total_frames*100:.1f}%) "
                               f"ETA: {eta:.1f}s")
        
        # Cleanup
        self.cap.release()
        self.out.release()
        cv2.destroyAllWindows()
        
        elapsed_time = time.time() - start_time
        self.logger.info(f"Processing completed in {elapsed_time:.1f} seconds")
        self.logger.info(f"Output saved to: {self.output_path}")


def main():
    """
    Main function to handle command-line interface.
    """
    parser = argparse.ArgumentParser(description="Remove text overlays from videos")
    parser.add_argument('--input', '-i', required=True, help='Input video file')
    parser.add_argument('--output', '-o', required=True, help='Output video file')
    parser.add_argument('--method', '-m', choices=['inpaint', 'blur', 'crop'], 
                       default='inpaint', help='Text removal method')
    parser.add_argument('--preview', '-p', action='store_true', 
                       help='Show preview windows during processing')
    parser.add_argument('--confidence', '-c', type=float, default=0.5,
                       help='Confidence threshold for text detection')
    
    args = parser.parse_args()
    
    # Check if input file exists
    if not os.path.exists(args.input):
        print(f"Error: Input file '{args.input}' not found")
        return
    
    try:
        # Create text remover
        remover = VideoTextRemover(
            input_path=args.input,
            output_path=args.output,
            method=args.method,
            confidence_threshold=args.confidence
        )
        
        # Process video
        remover.process_video(show_preview=args.preview)
        
        print(f"✅ Text removal completed! Output: {args.output}")
        
    except Exception as e:
        print(f"❌ Error processing video: {e}")


if __name__ == "__main__":
    main()
