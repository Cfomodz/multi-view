#!/usr/bin/env python3
"""
Example usage of the Remote Media Bridge Viewer.
"""

import sys
import os
import tkinter as tk
from media_bridge_viewer import RemoteMediaViewer

def example_remote_usage():
    """Example of using the remote media viewer."""
    
    # Connection details (you can modify these)
    SSH_HOST = "your-server.com"
    SSH_USER = "username"
    SSH_PORT = 22
    SSH_KEY = None  # Optional: "/path/to/ssh/key"
    REMOTE_DIR = "/path/to/remote/media/files"
    
    print("🎬 Remote Media Bridge Viewer Example")
    print("=" * 40)
    print(f"Connecting to: {SSH_USER}@{SSH_HOST}:{SSH_PORT}")
    print(f"Remote directory: {REMOTE_DIR}")
    
    # Create the viewer
    root = tk.Tk()
    viewer = RemoteMediaViewer(root, SSH_HOST, SSH_USER, SSH_PORT, SSH_KEY)
    
    # Set up callbacks
    def on_selection_changed(selected_files):
        print(f"Selected {len(selected_files)} files:")
        for file in selected_files:
            print(f"  - {os.path.basename(file)}")
    
    def on_file_double_clicked(filepath):
        filename = os.path.basename(filepath)
        print(f"Double-clicked: {filename}")
        print("File will be downloaded and opened locally...")
    
    viewer.set_selection_callback(on_selection_changed)
    viewer.set_double_click_callback(on_file_double_clicked)
    
    # Load remote directory
    viewer.load_directory(REMOTE_DIR)
    
    # Start the viewer
    print("🚀 Starting Remote Media Bridge Viewer...")
    print("💡 Tip: Double-click files to download and open them locally")
    
    try:
        viewer.run()
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    finally:
        viewer.close()

if __name__ == "__main__":
    example_remote_usage()