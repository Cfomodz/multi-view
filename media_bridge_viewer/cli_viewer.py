#!/usr/bin/env python3
"""
Command-line interface for Media Bridge Viewer.
Text-based interface for when GUI is not available.
"""

import os
import sys
from typing import List, Dict, Set
from .media_handler import MediaHandler


class CLIMediaViewer:
    """Command-line media viewer for headless environments."""
    
    def __init__(self):
        self.media_handler = MediaHandler()
        self.media_files: List[str] = []
        self.selected_files: Set[str] = set()
        self.current_directory = ""
        
    def load_directory(self, directory: str, recursive: bool = False) -> bool:
        """Load media files from directory."""
        if not os.path.exists(directory):
            print(f"Error: Directory not found: {directory}")
            return False
            
        self.current_directory = directory
        print(f"Loading files from: {directory}")
        
        self.media_files = self.media_handler.get_files_in_directory(directory, recursive)
        
        if not self.media_files:
            print("No supported media files found.")
            return False
            
        print(f"Found {len(self.media_files)} media files.")
        return True
        
    def display_files(self):
        """Display list of media files with selection status."""
        if not self.media_files:
            print("No files loaded.")
            return
            
        print(f"\n{'='*80}")
        print(f"Media files in: {self.current_directory}")
        print(f"{'='*80}")
        
        for i, filepath in enumerate(self.media_files, 1):
            filename = os.path.basename(filepath)
            selected = "✓" if filepath in self.selected_files else " "
            
            # Get file info
            info = self.media_handler.get_media_info(filepath)
            size_mb = info.get('size', 0) / (1024 * 1024)
            
            # Format display
            type_icon = "🎬" if info.get('type') == 'video' else "🖼️"
            
            print(f"{i:3d}. [{selected}] {type_icon} {filename}")
            
            # Show dimensions and size
            if 'width' in info and 'height' in info:
                dims = f"{info['width']}×{info['height']}"
            else:
                dims = "Unknown"
                
            print(f"     Size: {size_mb:.1f}MB, Dimensions: {dims}")
            
            # Show duration for videos
            if info.get('type') == 'video' and 'duration' in info:
                duration = info['duration']
                mins, secs = divmod(int(duration), 60)
                print(f"     Duration: {mins:02d}:{secs:02d}")
                
        print(f"\nSelected: {len(self.selected_files)} of {len(self.media_files)} files")
        print(f"{'='*80}\n")
        
    def show_help(self):
        """Show available commands."""
        print("""
Available commands:
  l, list          - List all files
  s <numbers>      - Select files by number (e.g., 's 1 3 5' or 's 1-5')
  d <numbers>      - Deselect files by number
  a, all           - Select all files
  c, clear         - Clear all selections
  k, keep          - Keep only selected files (hide others)
  r, remove        - Delete selected files (PERMANENT!)
  i <number>       - Show detailed info for a file
  o <number>       - Open file with system default application
  q, quit, exit    - Exit the viewer
  h, help          - Show this help
  
Examples:
  s 1 3 5          - Select files 1, 3, and 5
  s 1-10           - Select files 1 through 10
  d 3              - Deselect file 3
  i 5              - Show detailed info for file 5
""")
        
    def parse_numbers(self, args: List[str]) -> List[int]:
        """Parse number arguments (supports ranges like 1-5)."""
        numbers = []
        for arg in args:
            if '-' in arg and arg.replace('-', '').isdigit():
                # Handle ranges like 1-5
                try:
                    start, end = map(int, arg.split('-'))
                    numbers.extend(range(start, end + 1))
                except ValueError:
                    print(f"Invalid range: {arg}")
            elif arg.isdigit():
                numbers.append(int(arg))
            else:
                print(f"Invalid number: {arg}")
        return numbers
        
    def select_files(self, numbers: List[int]):
        """Select files by number."""
        selected_count = 0
        for num in numbers:
            if 1 <= num <= len(self.media_files):
                filepath = self.media_files[num - 1]
                self.selected_files.add(filepath)
                selected_count += 1
            else:
                print(f"Invalid file number: {num}")
                
        if selected_count > 0:
            print(f"Selected {selected_count} files.")
            
    def deselect_files(self, numbers: List[int]):
        """Deselect files by number."""
        deselected_count = 0
        for num in numbers:
            if 1 <= num <= len(self.media_files):
                filepath = self.media_files[num - 1]
                if filepath in self.selected_files:
                    self.selected_files.remove(filepath)
                    deselected_count += 1
            else:
                print(f"Invalid file number: {num}")
                
        if deselected_count > 0:
            print(f"Deselected {deselected_count} files.")
            
    def show_file_info(self, number: int):
        """Show detailed info for a file."""
        if not 1 <= number <= len(self.media_files):
            print(f"Invalid file number: {number}")
            return
            
        filepath = self.media_files[number - 1]
        info = self.media_handler.get_media_info(filepath)
        
        print(f"\nFile #{number}: {os.path.basename(filepath)}")
        print(f"Path: {filepath}")
        print(f"Type: {info.get('type', 'Unknown').title()}")
        
        if 'width' in info and 'height' in info:
            print(f"Dimensions: {info['width']} × {info['height']}")
            
        if 'size' in info:
            size_mb = info['size'] / (1024 * 1024)
            print(f"Size: {size_mb:.1f} MB")
            
        if info.get('type') == 'video':
            if 'duration' in info:
                duration = info['duration']
                mins, secs = divmod(int(duration), 60)
                print(f"Duration: {mins:02d}:{secs:02d}")
                
            if 'fps' in info:
                print(f"FPS: {info['fps']:.1f}")
                
            if 'frame_count' in info:
                print(f"Frames: {info['frame_count']}")
                
        if 'error' in info:
            print(f"Error: {info['error']}")
            
        selected = "Yes" if filepath in self.selected_files else "No"
        print(f"Selected: {selected}")
        print()
        
    def open_file(self, number: int):
        """Open file with system default application."""
        if not 1 <= number <= len(self.media_files):
            print(f"Invalid file number: {number}")
            return
            
        filepath = self.media_files[number - 1]
        print(f"Opening: {os.path.basename(filepath)}")
        
        import subprocess
        import platform
        
        try:
            if platform.system() == 'Darwin':  # macOS
                subprocess.call(['open', filepath])
            elif platform.system() == 'Windows':
                os.startfile(filepath)
            else:  # Linux
                subprocess.call(['xdg-open', filepath])
        except Exception as e:
            print(f"Error opening file: {e}")
            
    def keep_selected(self):
        """Keep only selected files."""
        if not self.selected_files:
            print("No files selected.")
            return
            
        original_count = len(self.media_files)
        self.media_files = [f for f in self.media_files if f in self.selected_files]
        self.selected_files.clear()
        
        kept_count = len(self.media_files)
        hidden_count = original_count - kept_count
        
        print(f"Kept {kept_count} files, hidden {hidden_count} files.")
        
    def delete_selected(self):
        """Delete selected files with confirmation."""
        if not self.selected_files:
            print("No files selected.")
            return
            
        count = len(self.selected_files)
        print(f"You are about to DELETE {count} files:")
        for filepath in self.selected_files:
            print(f"  - {os.path.basename(filepath)}")
            
        response = input(f"\nAre you sure you want to delete these {count} files? (yes/no): ").strip().lower()
        
        if response not in ['yes', 'y']:
            print("Delete cancelled.")
            return
            
        deleted_count = 0
        for filepath in list(self.selected_files):
            try:
                os.remove(filepath)
                deleted_count += 1
                self.media_files.remove(filepath)
                self.selected_files.remove(filepath)
                print(f"Deleted: {os.path.basename(filepath)}")
            except Exception as e:
                print(f"Error deleting {os.path.basename(filepath)}: {e}")
                
        print(f"Successfully deleted {deleted_count} of {count} files.")
        
    def run_interactive(self):
        """Run interactive command loop."""
        print("Media Bridge CLI Viewer")
        print("Type 'help' for available commands.")
        
        while True:
            try:
                command = input("> ").strip()
                if not command:
                    continue
                    
                parts = command.split()
                cmd = parts[0].lower()
                args = parts[1:] if len(parts) > 1 else []
                
                if cmd in ['q', 'quit', 'exit']:
                    break
                elif cmd in ['h', 'help']:
                    self.show_help()
                elif cmd in ['l', 'list']:
                    self.display_files()
                elif cmd == 's':
                    if args:
                        numbers = self.parse_numbers(args)
                        self.select_files(numbers)
                    else:
                        print("Usage: s <numbers> (e.g., 's 1 3 5' or 's 1-10')")
                elif cmd == 'd':
                    if args:
                        numbers = self.parse_numbers(args)
                        self.deselect_files(numbers)
                    else:
                        print("Usage: d <numbers>")
                elif cmd in ['a', 'all']:
                    self.selected_files = set(self.media_files)
                    print(f"Selected all {len(self.media_files)} files.")
                elif cmd in ['c', 'clear']:
                    self.selected_files.clear()
                    print("Cleared all selections.")
                elif cmd in ['k', 'keep']:
                    self.keep_selected()
                elif cmd in ['r', 'remove']:
                    self.delete_selected()
                elif cmd == 'i':
                    if args and args[0].isdigit():
                        self.show_file_info(int(args[0]))
                    else:
                        print("Usage: i <number>")
                elif cmd == 'o':
                    if args and args[0].isdigit():
                        self.open_file(int(args[0]))
                    else:
                        print("Usage: o <number>")
                else:
                    print(f"Unknown command: {cmd}. Type 'help' for available commands.")
                    
            except KeyboardInterrupt:
                print("\nExiting...")
                break
            except Exception as e:
                print(f"Error: {e}")
                
        print("Goodbye!")


def main():
    """Main CLI entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="CLI Media Bridge Viewer")
    parser.add_argument("directory", nargs="?", help="Directory to load")
    parser.add_argument("--recursive", "-r", action="store_true", help="Search recursively")
    
    args = parser.parse_args()
    
    viewer = CLIMediaViewer()
    
    if args.directory:
        if viewer.load_directory(args.directory, args.recursive):
            viewer.display_files()
            viewer.run_interactive()
    else:
        print("Usage: cli-media-viewer <directory>")
        print("Example: cli-media-viewer /path/to/your/media/files")


if __name__ == "__main__":
    main()