#!/bin/bash
# Script to install media-bridge-viewer locally on Manjaro

echo "🎬 Installing Media Bridge Viewer locally..."

# Check if we're on Manjaro/Arch
if ! command -v pacman &> /dev/null; then
    echo "❌ This script is designed for Manjaro/Arch Linux"
    exit 1
fi

# Install Python dependencies
echo "📦 Installing Python dependencies..."
sudo pacman -S python python-pip python-pillow opencv python-numpy --noconfirm

# Install Python packages
echo "📦 Installing Python packages..."
pip install --user opencv-python numpy

echo "✅ Installation complete!"
echo ""
echo "🚀 Usage:"
echo "  python3 remote_media_viewer.py"
echo ""
echo "📁 The script will prompt you for:"
echo "  - SSH connection details (server, username, port)"
echo "  - Remote directory path"
echo "  - Optional: SSH key path"