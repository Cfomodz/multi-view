# Quick Start Guide

## What We Built

**Media Bridge Viewer** - A standalone Adobe Bridge-style application for comparing and selecting multiple media files at once. Perfect for your video crop workflow!

## Installation

```bash
cd /home/sam/domain-sticks
source venv/bin/activate
cd /home/sam/media-bridge-viewer
pip install -e .
```

## Usage Examples

### 1. Command Line - View Your Video Crops

```bash
# Launch with your workflow directory
media-bridge "/home/sam/domain-sticks/workflow/05_video_processing/4.6_Cycloalkanes_and_Cyclohexane_Chair_Conformatio" --columns 3

# Or browse for any directory
media-bridge --columns 4
```

### 2. Python Integration

```python
from media_bridge_viewer import MediaBridgeViewer
import tkinter as tk

# Create viewer
root = tk.Tk()
viewer = MediaBridgeViewer(root)

# Load your crops directory
viewer.load_directory("workflow/05_video_processing/...")

# Set up callback to process selected files
def handle_selection(selected_files):
    print(f"User selected {len(selected_files)} files:")
    for file in selected_files:
        print(f"  - {file}")
    # Your processing logic here

viewer.set_selection_callback(handle_selection)
viewer.run()
```

## Key Features

- **Grid View**: See all your video crops at once in thumbnails
- **Video Previews**: Automatic thumbnail generation with play button overlay
- **Selection System**: Check boxes to select multiple files
- **Preview Panel**: Click any file to see larger preview + metadata
- **Bulk Operations**:
  - "Keep Selected" - hide unselected files
  - "Delete Selected" - remove unwanted crops (with confirmation)
  - "Select All" / "Clear Selection"
- **Keyboard Shortcuts**: Ctrl+A, Ctrl+D, Delete, F5
- **Customizable**: Adjust columns, thumbnail sizes

## Perfect For Your Workflow

Instead of opening files one by one in a file manager, you can now:

1. Launch the viewer on your crop directory
2. See all variations (cropped, letterbox, layered_triple, split, etc.) at once
3. Select the best ones with checkboxes
4. Use "Keep Selected" to focus on just the good ones
5. Delete unwanted versions with "Delete Selected"
6. Double-click to open in your video player for full review

## Repository Ready

The package is structured as a proper Python package that you can:
- Upload to GitHub as `media-bridge-viewer`
- Install in other projects with `pip install git+https://github.com/cfomodz/media-bridge-viewer.git`
- Use as a dependency in other video processing workflows

## File Structure

```
media-bridge-viewer/
├── media_bridge_viewer/
│   ├── __init__.py
│   ├── viewer.py          # Main GUI application
│   ├── media_handler.py   # Media file processing
│   └── cli.py            # Command line interface
├── setup.py
├── requirements.txt
├── README.md
├── LICENSE
├── example_usage.py
└── test_with_workflow.py
```

The viewer is now running in the background showing your video crops!