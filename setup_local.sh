#!/bin/bash
# Setup script for local Manjaro installation

echo "🎬 Setting up Media Bridge Viewer for local use..."

# Check if we're on Manjaro/Arch
if ! command -v pacman &> /dev/null; then
    echo "❌ This script is designed for Manjaro/Arch Linux"
    exit 1
fi

# Install system dependencies
echo "📦 Installing system dependencies..."
sudo pacman -S python python-pip python-pillow opencv python-numpy --noconfirm

# Install Python packages
echo "📦 Installing Python packages..."
pip install --user opencv-python numpy

# Make scripts executable
chmod +x remote_media_viewer.py
chmod +x install_local.sh

echo "✅ Setup complete!"
echo ""
echo "🚀 Usage:"
echo "  python3 remote_media_viewer.py"
echo ""
echo "📋 The script will prompt you for:"
echo "  - SSH server hostname/IP"
echo "  - SSH username"
echo "  - SSH port (default: 22)"
echo "  - SSH key path (optional)"
echo "  - Remote directory path"
echo ""
echo "💡 Example remote directory:"
echo "  /home/sam/domain-sticks/workflow/05_video_processing/4.6_Cycloalkanes_and_Cyclohexane_Chair_Conformatio"