# Media Bridge Viewer

An Adobe Bridge-style media viewer for comparing and selecting multiple media files at once. Perfect for reviewing different versions, crops, or variations of images and videos in a visual grid layout.

**🆕 NEW: Remote SSH Support!** Browse media files on remote servers from your local desktop.

![Media Bridge Viewer Screenshot](screenshot.png)

## Features

- **Grid View**: Display multiple media files in a customizable grid layout
- **Multi-format Support**: Images (JPG, PNG, GIF, BMP, TIFF, WebP) and Videos (MP4, AVI, MOV, MKV, WMV, FLV, WebM)
- **Video Thumbnails**: Automatic thumbnail generation from video files with play button overlay
- **Selection System**: Select multiple files with checkboxes and bulk operations
- **Preview Panel**: Click any file to see a larger preview with detailed metadata
- **Bulk Operations**: Keep selected, delete selected, select all, clear selection
- **Recursive Directory Scanning**: Option to scan subdirectories
- **Keyboard Shortcuts**: Ctrl+A (select all), Ctrl+D (clear), Delete (remove selected), F5 (refresh)
- **Customizable**: Adjustable grid columns, thumbnail sizes, and custom callbacks
- **Standalone Package**: Can be installed and used as a dependency in other projects
- **🌐 Remote SSH Support**: Browse files on remote servers via SSH
- **🖥️ Local GUI**: Full desktop experience with remote file access

## Installation

### From Source

```bash
git clone https://github.com/cfomodz/media-bridge-viewer.git
cd media-bridge-viewer
pip install -e .
```

### As a Dependency

```bash
pip install git+https://github.com/cfomodz/media-bridge-viewer.git
```

Or add to your `requirements.txt`:
```
git+https://github.com/cfomodz/media-bridge-viewer.git
```

## Usage

### Remote SSH Viewer (Recommended)

Browse media files on remote servers from your local desktop:

```bash
# Run the remote viewer
python3 remote_media_viewer.py
```

The script will prompt you for:
- SSH server hostname/IP
- SSH username and port
- Remote directory path
- Optional SSH key path

### Command Line (Local Files)

```bash
# Launch with folder browser
media-bridge

# Launch with specific directory
media-bridge /path/to/media/files

# Launch with custom settings
media-bridge /path/to/media --recursive --columns 6 --thumbnail-size 400x300
```

### As Python Module

```python
import tkinter as tk
from media_bridge_viewer import MediaBridgeViewer

# Create viewer
root = tk.Tk()
viewer = MediaBridgeViewer(root)

# Load directory
viewer.load_directory("/path/to/media/files")

# Set up callbacks (optional)
def on_selection_changed(selected_files):
    print(f"Selected {len(selected_files)} files")

viewer.set_selection_callback(on_selection_changed)

# Start application
viewer.run()
```

### Remote SSH Integration

```python
from media_bridge_viewer import RemoteMediaViewer
import tkinter as tk

# Create remote viewer
root = tk.Tk()
viewer = RemoteMediaViewer(root, "your-server.com", "username", 22, "/path/to/ssh/key")

# Load remote directory
viewer.load_directory("/path/to/remote/media/files")

# Set up callbacks
def on_selection_changed(selected_files):
    print(f"Selected {len(selected_files)} remote files")

viewer.set_selection_callback(on_selection_changed)
viewer.run()
```

### Integration with Existing Workflows

```python
from media_bridge_viewer import MediaBridgeViewer
import tkinter as tk

def process_video_crops():
    """Example: Select best video crops from multiple versions."""
    root = tk.Tk()
    viewer = MediaBridgeViewer(root)
    
    # Load your crop directory
    crops_dir = "workflow/05_video_processing/video_crops/"
    viewer.load_directory(crops_dir)
    
    def on_files_selected(selected_files):
        # Process the selected files
        for filepath in selected_files:
            print(f"Keeping: {filepath}")
            # Your processing logic here
    
    viewer.set_selection_callback(on_files_selected)
    viewer.run()
    
    return viewer.get_selected_files()
```

## Use Cases

### Video Production Workflows
- Compare different crops of the same video segment
- Review multiple render versions
- Select best takes from multiple recordings
- Choose thumbnails for video content

### Photo Management
- Compare different edits of the same photo
- Select best shots from a photo session
- Review batch processing results
- Organize photos by quality/preference

### Content Creation
- Compare different versions of graphics/assets
- Select final versions from design iterations
- Review exported content in different formats
- Organize media libraries

## Interface Overview

### Toolbar
- **Browse Folder**: Select directory to view
- **Columns**: Adjust grid layout (1-8 columns)
- **Select All/Clear Selection**: Bulk selection controls
- **Keep Selected**: Hide unselected files
- **Delete Selected**: Remove selected files (with confirmation)
- **Recursive**: Include subdirectories in scan

### Main View
- **Grid Area**: Scrollable grid of media thumbnails
- **Preview Panel**: Large preview with file information
- **Status Bar**: Shows selection count and loading progress

### Keyboard Shortcuts
- `Ctrl+A`: Select all files
- `Ctrl+D`: Clear selection
- `Delete`: Delete selected files
- `F5`: Refresh view
- `Mouse Wheel`: Scroll through grid

## API Reference

### MediaBridgeViewer

```python
class MediaBridgeViewer:
    def __init__(self, root: tk.Tk = None)
    def load_directory(self, directory: str)
    def get_selected_files(self) -> List[str]
    def set_selection_callback(self, callback: Callable[[List[str]], None])
    def set_double_click_callback(self, callback: Callable[[str], None])
    def run()
    def close()
```

### MediaHandler

```python
class MediaHandler:
    def __init__(self, thumbnail_size: Tuple[int, int] = (300, 200))
    def is_supported_file(self, filepath: str) -> bool
    def get_media_info(self, filepath: str) -> Dict
    def create_thumbnail(self, filepath: str) -> ImageTk.PhotoImage
    def get_files_in_directory(self, directory: str, recursive: bool = False) -> List[str]
```

## Configuration

### Thumbnail Sizes
Default thumbnail size is 300x200 pixels. You can customize this:

```python
from media_bridge_viewer import MediaBridgeViewer

viewer = MediaBridgeViewer()
viewer.media_handler.thumbnail_size = (400, 300)  # width, height
```

### Grid Layout
Adjust the number of columns:

```python
viewer.grid_columns = 6  # 1-8 columns supported
```

## Requirements

- Python 3.8+
- tkinter (usually included with Python)
- Pillow >= 8.0.0
- OpenCV >= 4.5.0
- NumPy >= 1.21.0

## Development

### Setup Development Environment

```bash
git clone https://github.com/cfomodz/media-bridge-viewer.git
cd media-bridge-viewer
pip install -e ".[dev]"
```

### Running Tests

```bash
pytest tests/
```

### Code Formatting

```bash
black media_bridge_viewer/
flake8 media_bridge_viewer/
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Changelog

### v0.1.0 (2024-12-19)
- Initial release
- Grid-based media viewer
- Video and image thumbnail support
- Selection and bulk operations
- Preview panel with metadata
- Command-line interface
- Python module API

## Acknowledgments

- Inspired by Adobe Bridge for its intuitive media browsing interface
- Built with tkinter for cross-platform compatibility
- Uses OpenCV for robust video thumbnail generation