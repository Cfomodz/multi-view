# 🎬 Remote Media Bridge Viewer

Browse and manage media files on remote servers from your local Manjaro desktop!

## 🚀 Quick Setup

### 1. Install Dependencies
```bash
# Run the setup script
chmod +x setup_local.sh
./setup_local.sh
```

### 2. Run the Remote Viewer
```bash
python3 remote_media_viewer.py
```

## 📋 What You'll Need

The script will prompt you for:

- **SSH Server**: Your server's hostname or IP address
- **SSH Username**: Your username on the remote server  
- **SSH Port**: Usually 22 (default)
- **SSH Key**: Optional path to your SSH private key
- **Remote Directory**: Path to your media files on the server

## 💡 Example Usage

1. **Start the viewer:**
   ```bash
   python3 remote_media_viewer.py
   ```

2. **Enter connection details:**
   - Server: `your-server-ip`
   - Username: `sam`
   - Port: `22`
   - Directory: `/home/sam/domain-sticks/workflow/05_video_processing/4.6_Cycloalkanes_and_Cyclohexane_Chair_Conformatio`

3. **Browse your media files!**
   - See all video crops in a grid
   - Select multiple files with checkboxes
   - Double-click to download and open files locally
   - Use "Keep Selected" to focus on good files
   - Use "Delete Selected" to remove unwanted crops

## ✨ Features

- **🖥️ Local GUI**: Full desktop experience on your Manjaro system
- **🌐 Remote Access**: Browse files on any SSH-accessible server
- **📱 Smart Downloading**: Files are downloaded temporarily when needed
- **🎥 Video Thumbnails**: Automatic thumbnail generation from remote videos
- **📁 File Management**: Select, keep, and delete files remotely
- **⚡ Fast Browsing**: Only downloads files when you need to view them

## 🔧 How It Works

1. **SSH Connection**: Connects to your remote server via SSH
2. **File Discovery**: Uses `find` command to locate media files
3. **Thumbnail Generation**: Downloads files temporarily to create thumbnails
4. **Local Viewing**: Downloads files when you double-click to open them
5. **Cleanup**: Automatically removes temporary files

## 🛠️ Troubleshooting

### SSH Connection Issues
- Make sure SSH key is in `~/.ssh/` directory
- Test SSH connection manually: `ssh user@server`
- Check if SSH port is correct (default: 22)

### Permission Issues
- Ensure you have read access to the remote directory
- Check if the remote directory exists and contains media files

### Performance
- Large files may take time to download
- Thumbnail generation requires downloading each file temporarily
- Consider using a fast internet connection for large media files

## 📁 File Structure

```
media-bridge-viewer/
├── remote_media_viewer.py    # Main remote viewer script
├── setup_local.sh           # Setup script for Manjaro
├── install_local.sh         # Installation script
├── media_bridge_viewer/     # Core viewer library
└── README_LOCAL.md          # This file
```

## 🎯 Perfect For Your Workflow

Instead of SSH + X11 forwarding or web interfaces, you get:

- **Native GUI experience** on your Manjaro desktop
- **Direct access** to remote media files
- **Full functionality** of the original Media Bridge Viewer
- **No server setup** required - just SSH access
- **Works with any remote server** that has your media files

Enjoy browsing your video crops remotely! 🎬✨