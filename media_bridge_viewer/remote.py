"""
Remote Media Bridge Viewer - Browse media files on remote server via SSH.
"""

import os
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import subprocess
import tempfile
import threading
import queue
from typing import Optional, Callable, List, Dict, Set
from .viewer import MediaBridgeViewer
from .media_handler import MediaHandler


class RemoteMediaHandler(MediaHandler):
    """Media handler that works with remote files via SSH."""
    
    def __init__(self, ssh_host, ssh_user, ssh_port=22, ssh_key=None):
        super().__init__()
        self.ssh_host = ssh_host
        self.ssh_user = ssh_user
        self.ssh_port = ssh_port
        self.ssh_key = ssh_key
        self.temp_dir = tempfile.mkdtemp(prefix="media_bridge_")
        
    def _run_ssh_command(self, command):
        """Run a command on the remote server via SSH."""
        ssh_cmd = [
            "ssh",
            "-o", "StrictHostKeyChecking=no",
            "-o", "UserKnownHostsFile=/dev/null",
            "-p", str(self.ssh_port)
        ]
        
        if self.ssh_key:
            ssh_cmd.extend(["-i", self.ssh_key])
            
        ssh_cmd.append(f"{self.ssh_user}@{self.ssh_host}")
        ssh_cmd.append(command)
        
        try:
            result = subprocess.run(ssh_cmd, capture_output=True, text=True, timeout=30)
            if result.returncode != 0:
                print(f"SSH command failed: {result.stderr}")
                return None
            return result.stdout
        except subprocess.TimeoutExpired:
            print("SSH command timed out")
            return None
        except Exception as e:
            print(f"SSH command error: {e}")
            return None
    
    def _download_file(self, remote_path, local_path):
        """Download a file from remote server."""
        scp_cmd = ["scp", "-o", "StrictHostKeyChecking=no", "-o", "UserKnownHostsFile=/dev/null"]
        
        if self.ssh_key:
            scp_cmd.extend(["-i", self.ssh_key])
            
        scp_cmd.extend(["-P", str(self.ssh_port)])
        scp_cmd.append(f"{self.ssh_user}@{self.ssh_host}:{remote_path}")
        scp_cmd.append(local_path)
        
        try:
            result = subprocess.run(scp_cmd, capture_output=True, text=True, timeout=60)
            return result.returncode == 0
        except Exception as e:
            print(f"Download error: {e}")
            return False
    
    def get_files_in_directory(self, directory, recursive=False):
        """Get media files from remote directory."""
        # Use find command to get all media files
        find_cmd = f"find '{directory}' -type f \\( "
        find_cmd += " -iname '*.jpg' -o -iname '*.jpeg' -o -iname '*.png' -o -iname '*.gif' "
        find_cmd += " -o -iname '*.bmp' -o -iname '*.tiff' -o -iname '*.webp' "
        find_cmd += " -o -iname '*.mp4' -o -iname '*.avi' -o -iname '*.mov' "
        find_cmd += " -o -iname '*.mkv' -o -iname '*.wmv' -o -iname '*.flv' -o -iname '*.webm' "
        find_cmd += " \\)"
        
        if not recursive:
            find_cmd += f" -maxdepth 1"
            
        find_cmd += " | sort"
        
        result = self._run_ssh_command(find_cmd)
        if not result:
            return []
            
        files = [line.strip() for line in result.split('\n') if line.strip()]
        return files
    
    def create_thumbnail(self, filepath):
        """Create thumbnail by downloading file temporarily."""
        # Create a local temp file
        filename = os.path.basename(filepath)
        local_path = os.path.join(self.temp_dir, filename)
        
        # Download the file
        if not self._download_file(filepath, local_path):
            return None
            
        try:
            # Create thumbnail using parent class method
            thumbnail = super().create_thumbnail(local_path)
            return thumbnail
        finally:
            # Clean up temp file
            if os.path.exists(local_path):
                os.remove(local_path)
    
    def get_media_info(self, filepath):
        """Get media info by downloading file temporarily."""
        filename = os.path.basename(filepath)
        local_path = os.path.join(self.temp_dir, filename)
        
        # Download the file
        if not self._download_file(filepath, local_path):
            return {"error": "Could not download file"}
            
        try:
            # Get info using parent class method
            info = super().get_media_info(local_path)
            return info
        finally:
            # Clean up temp file
            if os.path.exists(local_path):
                os.remove(local_path)
    
    def cleanup(self):
        """Clean up temporary files."""
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)


class RemoteMediaViewer(MediaBridgeViewer):
    """Media Bridge Viewer that works with remote files."""
    
    def __init__(self, root, ssh_host, ssh_user, ssh_port=22, ssh_key=None):
        # Initialize with remote media handler
        self.remote_handler = RemoteMediaHandler(ssh_host, ssh_user, ssh_port, ssh_key)
        super().__init__(root)
        self.media_handler = self.remote_handler
        
    def load_directory(self, directory):
        """Load directory from remote server."""
        self.current_directory = directory
        self.media_files = self.remote_handler.get_files_in_directory(directory, self.recursive_var.get())
        self._refresh_view()
        
    def _open_file_externally(self, filepath):
        """Open remote file by downloading and opening locally."""
        filename = os.path.basename(filepath)
        local_path = os.path.join(self.remote_handler.temp_dir, filename)
        
        # Show progress
        self.status_var.set(f"Downloading {filename}...")
        self.root.update()
        
        # Download file
        if self.remote_handler._download_file(filepath, local_path):
            # Open with default application
            import subprocess
            import platform
            
            system = platform.system()
            if system == "Darwin":  # macOS
                subprocess.run(["open", local_path])
            elif system == "Windows":
                os.startfile(local_path)
            else:  # Linux
                subprocess.run(["xdg-open", local_path])
            
            self.status_var.set(f"Opened {filename}")
        else:
            messagebox.showerror("Error", f"Could not download {filename}")
            self.status_var.set("Download failed")
    
    def close(self):
        """Clean up when closing."""
        self.remote_handler.cleanup()
        super().close()


def get_ssh_connection():
    """Get SSH connection details from user."""
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    
    # Get connection details
    ssh_host = simpledialog.askstring("SSH Connection", "Enter server hostname/IP:")
    if not ssh_host:
        return None
        
    ssh_user = simpledialog.askstring("SSH Connection", "Enter username:")
    if not ssh_user:
        return None
        
    ssh_port = simpledialog.askstring("SSH Connection", "Enter SSH port (default: 22):")
    ssh_port = int(ssh_port) if ssh_port else 22
    
    ssh_key = simpledialog.askstring("SSH Connection", "Enter SSH key path (optional, press Enter to skip):")
    if not ssh_key or ssh_key.strip() == "":
        ssh_key = None
    
    root.destroy()
    return ssh_host, ssh_user, ssh_port, ssh_key


def get_remote_directory():
    """Get remote directory path from user."""
    root = tk.Tk()
    root.withdraw()
    
    directory = simpledialog.askstring("Remote Directory", 
        "Enter remote directory path:\n(e.g., /home/sam/domain-sticks/workflow/05_video_processing/4.6_Cycloalkanes_and_Cyclohexane_Chair_Conformatio)")
    
    root.destroy()
    return directory


def main():
    """Main function to run the remote media viewer."""
    print("🎬 Remote Media Bridge Viewer")
    print("=" * 40)
    
    # Get SSH connection details
    connection = get_ssh_connection()
    if not connection:
        print("❌ Connection cancelled")
        return
        
    ssh_host, ssh_user, ssh_port, ssh_key = connection
    
    # Get remote directory
    remote_dir = get_remote_directory()
    if not remote_dir:
        print("❌ Directory selection cancelled")
        return
    
    print(f"🔗 Connecting to {ssh_user}@{ssh_host}:{ssh_port}")
    print(f"📁 Browsing directory: {remote_dir}")
    
    # Test SSH connection
    print("🔍 Testing SSH connection...")
    test_handler = RemoteMediaHandler(ssh_host, ssh_user, ssh_port, ssh_key)
    test_result = test_handler._run_ssh_command("echo 'SSH connection successful'")
    
    if not test_result:
        print("❌ SSH connection failed!")
        print("Please check your connection details and try again.")
        return
    
    print("✅ SSH connection successful!")
    
    # Create and run the viewer
    root = tk.Tk()
    viewer = RemoteMediaViewer(root, ssh_host, ssh_user, ssh_port, ssh_key)
    
    # Load the remote directory
    viewer.load_directory(remote_dir)
    
    # Add some helpful info
    viewer.status_var.set(f"Connected to {ssh_user}@{ssh_host} - {len(viewer.media_files)} files")
    
    print("🚀 Starting Media Bridge Viewer...")
    print("💡 Tip: Double-click files to download and open them locally")
    
    try:
        viewer.run()
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    finally:
        viewer.close()


if __name__ == "__main__":
    main()