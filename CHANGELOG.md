# Changelog

## [0.1.0] - 2024-01-XX

### Added
- **Remote SSH Support**: Browse media files on remote servers via SSH
- **RemoteMediaViewer**: New class for remote file browsing
- **RemoteMediaHandler**: SSH-based media handler for remote files
- **Smart Downloading**: Files are downloaded temporarily when needed
- **SSH Integration**: Full SSH support with key authentication
- **Local GUI**: Full desktop experience with remote file access

### Features
- Grid view of remote media files
- Video thumbnail generation from remote videos
- Selection system for multiple files
- Bulk operations (keep selected, delete selected)
- Double-click to download and open files locally
- Automatic cleanup of temporary files
- SSH connection testing and validation

### Usage
```bash
# Install locally
pip install -e .

# Run remote viewer
media-bridge-remote

# Or use Python API
from media_bridge_viewer import RemoteMediaViewer
```

### Breaking Changes
- None (backward compatible)

### Dependencies
- Added SSH/SCP support for remote file access
- All existing dependencies maintained