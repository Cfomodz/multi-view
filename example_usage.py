#!/usr/bin/env python3
"""
Example usage of Media Bridge Viewer as a Python module.
"""

import tkinter as tk
from media_bridge_viewer import MediaBridgeViewer
import os


def example_basic_usage():
    """Basic usage example."""
    print("Starting Media Bridge Viewer...")
    
    # Create the main window
    root = tk.Tk()
    
    # Create the viewer
    viewer = MediaBridgeViewer(root)
    
    # Optional: Set up custom callbacks
    def on_files_selected(selected_files):
        print(f"User selected {len(selected_files)} files:")
        for filepath in selected_files:
            print(f"  - {os.path.basename(filepath)}")
    
    def on_file_opened(filepath):
        print(f"User double-clicked: {os.path.basename(filepath)}")
        # You could implement custom file handling here
        # For example, copy to a specific location, add to a playlist, etc.
    
    # Set callbacks
    viewer.set_selection_callback(on_files_selected)
    viewer.set_double_click_callback(on_file_opened)
    
    # Optional: Load a specific directory on startup
    # viewer.load_directory("/path/to/your/media/files")
    
    # Start the application
    viewer.run()


def example_custom_integration():
    """Example of integrating with existing workflow."""
    
    class CustomMediaProcessor:
        def __init__(self):
            self.selected_files = []
            
        def process_selected_files(self, files):
            """Process the files selected by user."""
            self.selected_files = files
            print(f"Processing {len(files)} selected files...")
            
            # Your custom processing logic here
            for filepath in files:
                print(f"Processing: {os.path.basename(filepath)}")
                # Example: copy to output directory, convert format, etc.
            
        def launch_viewer(self, directory):
            """Launch viewer for file selection."""
            root = tk.Tk()
            viewer = MediaBridgeViewer(root)
            
            # Set up callback to process selected files
            def on_selection_done():
                selected = viewer.get_selected_files()
                if selected:
                    self.process_selected_files(selected)
                    viewer.close()
                else:
                    print("No files selected!")
            
            # Add a custom button to the toolbar
            import tkinter.ttk as ttk
            process_button = ttk.Button(
                viewer.toolbar_frame,
                text="Process Selected",
                command=on_selection_done
            )
            process_button.pack(side=tk.RIGHT, padx=5)
            
            # Load the directory
            viewer.load_directory(directory)
            
            # Start the viewer
            viewer.run()
            
            return self.selected_files
    
    # Usage
    processor = CustomMediaProcessor()
    
    # This would typically be your workflow directory
    # workflow_dir = "/home/sam/domain-sticks/workflow/05_video_processing/4.6_Cycloalkanes_and_Cyclohexane_Chair_Conformatio"
    # selected_files = processor.launch_viewer(workflow_dir)
    
    print("Custom integration example ready!")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--custom":
        example_custom_integration()
    else:
        example_basic_usage()