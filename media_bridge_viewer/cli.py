"""
Command-line interface for Media Bridge Viewer.
"""

import argparse
import sys
import tkinter as tk
from typing import List
from .viewer import MediaBridgeViewer


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Media Bridge Viewer - Adobe Bridge-style media comparison tool"
    )
    
    parser.add_argument(
        "directory",
        nargs="?",
        help="Directory to load media files from"
    )
    
    parser.add_argument(
        "--recursive", "-r",
        action="store_true",
        help="Search directories recursively"
    )
    
    parser.add_argument(
        "--columns", "-c",
        type=int,
        default=4,
        help="Number of columns in grid view (default: 4)"
    )
    
    parser.add_argument(
        "--thumbnail-size",
        type=str,
        default="300x200",
        help="Thumbnail size in format WIDTHxHEIGHT (default: 300x200)"
    )
    
    args = parser.parse_args()
    
    # Parse thumbnail size
    try:
        if 'x' in args.thumbnail_size.lower():
            width, height = map(int, args.thumbnail_size.lower().split('x'))
        else:
            width = height = int(args.thumbnail_size)
        thumbnail_size = (width, height)
    except ValueError:
        print(f"Error: Invalid thumbnail size format: {args.thumbnail_size}")
        print("Use format like '300x200' or just '300' for square thumbnails")
        sys.exit(1)
    
    # Validate columns
    if not 1 <= args.columns <= 8:
        print("Error: Columns must be between 1 and 8")
        sys.exit(1)
    
    try:
        # Create Tkinter root
        root = tk.Tk()
        
        # Create viewer with custom settings
        viewer = MediaBridgeViewer(root)
        viewer.media_handler.thumbnail_size = thumbnail_size
        viewer.grid_columns = args.columns
        viewer.columns_var.set(str(args.columns))
        
        if args.recursive:
            viewer.recursive_var.set(True)
        
        # Load directory if provided
        if args.directory:
            viewer.load_directory(args.directory)
        
        # Set up selection callback for CLI feedback
        def on_selection_changed(selected_files: List[str]):
            if selected_files:
                print(f"Selected {len(selected_files)} files:")
                for filepath in selected_files:
                    print(f"  - {filepath}")
            else:
                print("No files selected")
        
        viewer.set_selection_callback(on_selection_changed)
        
        # Run the application
        viewer.run()
        
    except KeyboardInterrupt:
        print("\nExiting...")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()