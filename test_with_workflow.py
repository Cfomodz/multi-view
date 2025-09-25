#!/usr/bin/env python3
"""
Test script to demonstrate Media Bridge Viewer with your workflow directory.
"""

import sys
import os
import tkinter as tk
from media_bridge_viewer import MediaBridgeViewer


def test_workflow_directory():
    """Test with your actual workflow/05 directory."""
    
    # Path to your workflow directory
    workflow_dir = "/home/sam/domain-sticks/workflow/05_video_processing/4.6_Cycloalkanes_and_Cyclohexane_Chair_Conformatio"
    
    if not os.path.exists(workflow_dir):
        print(f"Error: Workflow directory not found: {workflow_dir}")
        print("Please check the path and try again.")
        return
    
    print(f"Loading Media Bridge Viewer with directory: {workflow_dir}")
    print("\nThis will show all your video crops in a grid layout.")
    print("You can:")
    print("- Click on any video to see a preview")
    print("- Select multiple videos with checkboxes")
    print("- Use 'Keep Selected' to hide others")
    print("- Use 'Delete Selected' to remove unwanted crops")
    print("- Double-click to open with default video player")
    
    # Create the viewer
    root = tk.Tk()
    viewer = MediaBridgeViewer(root)
    
    # Configure for better video viewing
    viewer.grid_columns = 3  # Fewer columns for larger thumbnails
    viewer.columns_var.set("3")
    
    # Set up callbacks to show what's happening
    def on_selection_changed(selected_files):
        if selected_files:
            print(f"\n=== SELECTED {len(selected_files)} FILES ===")
            for filepath in selected_files:
                filename = os.path.basename(filepath)
                print(f"  ✓ {filename}")
        else:
            print("\n=== NO FILES SELECTED ===")
    
    def on_file_double_clicked(filepath):
        filename = os.path.basename(filepath)
        print(f"\n=== DOUBLE-CLICKED: {filename} ===")
        print("Opening with default application...")
    
    viewer.set_selection_callback(on_selection_changed)
    viewer.set_double_click_callback(on_file_double_clicked)
    
    # Load your workflow directory
    viewer.load_directory(workflow_dir)
    
    # Add a custom button for workflow-specific actions
    import tkinter.ttk as ttk
    
    def export_selected():
        selected = viewer.get_selected_files()
        if not selected:
            tk.messagebox.showwarning("No Selection", "Please select files first!")
            return
            
        print(f"\n=== EXPORTING {len(selected)} SELECTED FILES ===")
        for filepath in selected:
            filename = os.path.basename(filepath)
            print(f"  → {filename}")
        
        # Here you could implement actual export logic
        tk.messagebox.showinfo("Export", f"Would export {len(selected)} selected files\\n(This is just a demo)")
    
    export_button = ttk.Button(
        viewer.toolbar_frame,
        text="Export Selected",
        command=export_selected
    )
    export_button.pack(side=tk.RIGHT, padx=5)
    
    # Start the viewer
    print("\nStarting Media Bridge Viewer...")
    viewer.run()


if __name__ == "__main__":
    try:
        test_workflow_directory()
    except KeyboardInterrupt:
        print("\nExiting...")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)