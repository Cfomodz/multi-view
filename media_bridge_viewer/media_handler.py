"""
Media Handler for processing and preparing media files for display.
"""

import os
import cv2
import numpy as np
from PIL import Image, ImageTk
from typing import List, Dict, Tuple, Optional, Union
import threading
import queue


class MediaHandler:
    """Handles loading, processing, and caching of media files."""
    
    SUPPORTED_IMAGE_FORMATS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp'}
    SUPPORTED_VIDEO_FORMATS = {'.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm'}
    
    def __init__(self, thumbnail_size: Tuple[int, int] = (300, 200)):
        self.thumbnail_size = thumbnail_size
        self.cache = {}
        self.loading_queue = queue.Queue()
        self.stop_loading = threading.Event()
        
    def is_supported_file(self, filepath: str) -> bool:
        """Check if file format is supported."""
        ext = os.path.splitext(filepath)[1].lower()
        return ext in self.SUPPORTED_IMAGE_FORMATS or ext in self.SUPPORTED_VIDEO_FORMATS
    
    def is_video_file(self, filepath: str) -> bool:
        """Check if file is a video format."""
        ext = os.path.splitext(filepath)[1].lower()
        return ext in self.SUPPORTED_VIDEO_FORMATS
    
    def is_image_file(self, filepath: str) -> bool:
        """Check if file is an image format."""
        ext = os.path.splitext(filepath)[1].lower()
        return ext in self.SUPPORTED_IMAGE_FORMATS
    
    def get_media_info(self, filepath: str) -> Dict:
        """Get basic information about media file."""
        if not os.path.exists(filepath):
            return {"error": "File not found"}
            
        info = {
            "filepath": filepath,
            "filename": os.path.basename(filepath),
            "size": os.path.getsize(filepath),
            "type": "video" if self.is_video_file(filepath) else "image",
            "supported": self.is_supported_file(filepath)
        }
        
        try:
            if self.is_video_file(filepath):
                cap = cv2.VideoCapture(filepath)
                if cap.isOpened():
                    info["width"] = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                    info["height"] = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                    info["fps"] = cap.get(cv2.CAP_PROP_FPS)
                    info["frame_count"] = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
                    info["duration"] = info["frame_count"] / info["fps"] if info["fps"] > 0 else 0
                cap.release()
            else:
                with Image.open(filepath) as img:
                    info["width"], info["height"] = img.size
                    info["format"] = img.format
        except Exception as e:
            info["error"] = str(e)
            
        return info
    
    def create_thumbnail(self, filepath: str) -> Optional[ImageTk.PhotoImage]:
        """Create thumbnail for display."""
        if filepath in self.cache:
            return self.cache[filepath]
            
        try:
            if self.is_video_file(filepath):
                thumbnail = self._create_video_thumbnail(filepath)
            else:
                thumbnail = self._create_image_thumbnail(filepath)
                
            if thumbnail:
                self.cache[filepath] = thumbnail
                return thumbnail
                
        except Exception as e:
            print(f"Error creating thumbnail for {filepath}: {e}")
            
        return None
    
    def _create_video_thumbnail(self, filepath: str) -> Optional[ImageTk.PhotoImage]:
        """Create thumbnail from video file (first frame)."""
        cap = cv2.VideoCapture(filepath)
        if not cap.isOpened():
            return None
            
        # Get frame from 10% into the video to avoid black frames
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        target_frame = max(1, int(frame_count * 0.1))
        cap.set(cv2.CAP_PROP_POS_FRAMES, target_frame)
        
        ret, frame = cap.read()
        cap.release()
        
        if not ret:
            return None
            
        # Convert BGR to RGB
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Create PIL Image and resize
        image = Image.fromarray(frame)
        image.thumbnail(self.thumbnail_size, Image.Resampling.LANCZOS)
        
        # Add video indicator overlay
        image = self._add_video_indicator(image)
        
        return ImageTk.PhotoImage(image)
    
    def _create_image_thumbnail(self, filepath: str) -> Optional[ImageTk.PhotoImage]:
        """Create thumbnail from image file."""
        with Image.open(filepath) as image:
            # Convert to RGB if needed
            if image.mode != 'RGB':
                image = image.convert('RGB')
                
            # Create thumbnail
            image.thumbnail(self.thumbnail_size, Image.Resampling.LANCZOS)
            
            return ImageTk.PhotoImage(image)
    
    def _add_video_indicator(self, image: Image.Image) -> Image.Image:
        """Add a play button overlay to indicate video files."""
        # Create a simple play button overlay
        overlay = Image.new('RGBA', image.size, (0, 0, 0, 0))
        
        # Calculate play button position and size
        w, h = image.size
        button_size = min(w, h) // 4
        x = (w - button_size) // 2
        y = (h - button_size) // 2
        
        # Simple triangle for play button
        from PIL import ImageDraw
        draw = ImageDraw.Draw(overlay)
        
        # Semi-transparent black circle background
        circle_coords = [x - 5, y - 5, x + button_size + 5, y + button_size + 5]
        draw.ellipse(circle_coords, fill=(0, 0, 0, 128))
        
        # White triangle
        triangle_coords = [
            x + button_size // 4, y + button_size // 4,
            x + 3 * button_size // 4, y + button_size // 2,
            x + button_size // 4, y + 3 * button_size // 4
        ]
        draw.polygon(triangle_coords, fill=(255, 255, 255, 255))
        
        # Composite the overlay
        if image.mode != 'RGBA':
            image = image.convert('RGBA')
        
        return Image.alpha_composite(image, overlay).convert('RGB')
    
    def get_files_in_directory(self, directory: str, recursive: bool = False) -> List[str]:
        """Get all supported media files in a directory."""
        files = []
        
        if recursive:
            for root, dirs, filenames in os.walk(directory):
                for filename in filenames:
                    filepath = os.path.join(root, filename)
                    if self.is_supported_file(filepath):
                        files.append(filepath)
        else:
            try:
                for filename in os.listdir(directory):
                    filepath = os.path.join(directory, filename)
                    if os.path.isfile(filepath) and self.is_supported_file(filepath):
                        files.append(filepath)
            except (OSError, PermissionError):
                pass
                
        return sorted(files)
    
    def clear_cache(self):
        """Clear the thumbnail cache."""
        self.cache.clear()
    
    def preload_thumbnails(self, filepaths: List[str], callback=None):
        """Preload thumbnails in background thread."""
        def worker():
            for i, filepath in enumerate(filepaths):
                if self.stop_loading.is_set():
                    break
                    
                if filepath not in self.cache:
                    self.create_thumbnail(filepath)
                    
                if callback:
                    callback(i + 1, len(filepaths), filepath)
                    
        thread = threading.Thread(target=worker, daemon=True)
        thread.start()
        return thread