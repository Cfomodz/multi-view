"""
Main Media Bridge Viewer interface.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from typing import List, Dict, Optional, Callable
import threading
from .media_handler import MediaHandler


class MediaBridgeViewer:
    """Main application window for the Media Bridge Viewer."""
    
    def __init__(self, root: Optional[tk.Tk] = None):
        self.root = root or tk.Tk()
        self.root.title("Media Bridge Viewer")
        self.root.geometry("1200x800")
        
        # Initialize media handler
        self.media_handler = MediaHandler()
        
        # State
        self.current_directory = ""
        self.media_files = []
        self.selected_files = set()
        self.grid_columns = 4
        self.current_preview = None
        
        # Callbacks
        self.on_selection_changed: Optional[Callable] = None
        self.on_file_double_click: Optional[Callable] = None
        
        # Setup UI
        self._setup_ui()
        self._setup_bindings()
        
    def _setup_ui(self):
        """Setup the user interface."""
        # Create main frames
        self.toolbar_frame = ttk.Frame(self.root)
        self.toolbar_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.status_frame = ttk.Frame(self.root)
        self.status_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self._setup_toolbar()
        self._setup_main_area()
        self._setup_status_bar()
        
    def _setup_toolbar(self):
        """Setup the toolbar."""
        # Directory selection
        ttk.Button(
            self.toolbar_frame, 
            text="Browse Folder", 
            command=self._browse_folder
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Separator(self.toolbar_frame, orient=tk.VERTICAL).pack(
            side=tk.LEFT, fill=tk.Y, padx=10
        )
        
        # Grid size controls
        ttk.Label(self.toolbar_frame, text="Columns:").pack(side=tk.LEFT, padx=5)
        
        self.columns_var = tk.StringVar(value=str(self.grid_columns))
        columns_spinbox = ttk.Spinbox(
            self.toolbar_frame,
            from_=1, to=8,
            width=5,
            textvariable=self.columns_var,
            command=self._update_grid_columns
        )
        columns_spinbox.pack(side=tk.LEFT, padx=5)
        
        ttk.Separator(self.toolbar_frame, orient=tk.VERTICAL).pack(
            side=tk.LEFT, fill=tk.Y, padx=10
        )
        
        # Selection controls
        ttk.Button(
            self.toolbar_frame, 
            text="Select All", 
            command=self._select_all
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            self.toolbar_frame, 
            text="Clear Selection", 
            command=self._clear_selection
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            self.toolbar_frame, 
            text="Keep Selected", 
            command=self._keep_selected
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            self.toolbar_frame, 
            text="Delete Selected", 
            command=self._delete_selected
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Separator(self.toolbar_frame, orient=tk.VERTICAL).pack(
            side=tk.LEFT, fill=tk.Y, padx=10
        )
        
        # View options
        self.recursive_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            self.toolbar_frame,
            text="Recursive",
            variable=self.recursive_var,
            command=self._refresh_view
        ).pack(side=tk.LEFT, padx=5)
        
    def _setup_main_area(self):
        """Setup the main viewing area."""
        # Create paned window for grid and preview
        self.paned_window = ttk.PanedWindow(self.main_frame, orient=tk.HORIZONTAL)
        self.paned_window.pack(fill=tk.BOTH, expand=True)
        
        # Grid frame (left side)
        self.grid_frame_container = ttk.Frame(self.paned_window)
        self.paned_window.add(self.grid_frame_container, weight=3)
        
        # Create scrollable grid
        self.grid_canvas = tk.Canvas(self.grid_frame_container, bg='white')
        self.grid_scrollbar_v = ttk.Scrollbar(
            self.grid_frame_container, 
            orient=tk.VERTICAL, 
            command=self.grid_canvas.yview
        )
        self.grid_scrollbar_h = ttk.Scrollbar(
            self.grid_frame_container, 
            orient=tk.HORIZONTAL, 
            command=self.grid_canvas.xview
        )
        
        self.grid_canvas.configure(
            yscrollcommand=self.grid_scrollbar_v.set,
            xscrollcommand=self.grid_scrollbar_h.set
        )
        
        # Pack scrollbars and canvas
        self.grid_scrollbar_v.pack(side=tk.RIGHT, fill=tk.Y)
        self.grid_scrollbar_h.pack(side=tk.BOTTOM, fill=tk.X)
        self.grid_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Create frame inside canvas for grid items
        self.grid_frame = ttk.Frame(self.grid_canvas)
        self.grid_canvas_window = self.grid_canvas.create_window(
            0, 0, anchor=tk.NW, window=self.grid_frame
        )
        
        # Preview frame (right side)
        self.preview_frame = ttk.Frame(self.paned_window)
        self.paned_window.add(self.preview_frame, weight=1)
        
        # Preview content
        ttk.Label(self.preview_frame, text="Preview", font=('Arial', 12, 'bold')).pack(pady=5)
        
        self.preview_label = ttk.Label(self.preview_frame, text="Select a file to preview")
        self.preview_label.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        
        self.preview_info_text = tk.Text(
            self.preview_frame, 
            height=8, 
            wrap=tk.WORD, 
            state=tk.DISABLED
        )
        self.preview_info_text.pack(fill=tk.X, padx=10, pady=5)
        
    def _setup_status_bar(self):
        """Setup the status bar."""
        self.status_var = tk.StringVar(value="Ready")
        self.status_label = ttk.Label(self.status_frame, textvariable=self.status_var)
        self.status_label.pack(side=tk.LEFT)
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            self.status_frame, 
            variable=self.progress_var,
            length=200
        )
        self.progress_bar.pack(side=tk.RIGHT, padx=10)
        
    def _setup_bindings(self):
        """Setup event bindings."""
        # Canvas scrolling
        self.grid_canvas.bind('<Configure>', self._on_canvas_configure)
        self.grid_frame.bind('<Configure>', self._on_frame_configure)
        
        # Mouse wheel scrolling
        self.grid_canvas.bind("<MouseWheel>", self._on_mousewheel)
        self.grid_canvas.bind("<Button-4>", self._on_mousewheel)
        self.grid_canvas.bind("<Button-5>", self._on_mousewheel)
        
        # Keyboard shortcuts
        self.root.bind('<Control-a>', lambda e: self._select_all())
        self.root.bind('<Control-d>', lambda e: self._clear_selection())
        self.root.bind('<Delete>', lambda e: self._delete_selected())
        self.root.bind('<F5>', lambda e: self._refresh_view())
        
    def _browse_folder(self):
        """Browse for a folder to view."""
        folder = filedialog.askdirectory(
            title="Select folder containing media files",
            initialdir=self.current_directory or os.path.expanduser("~")
        )
        
        if folder:
            self.load_directory(folder)
            
    def load_directory(self, directory: str):
        """Load media files from a directory."""
        if not os.path.exists(directory):
            messagebox.showerror("Error", f"Directory not found: {directory}")
            return
            
        self.current_directory = directory
        self.status_var.set(f"Loading files from {directory}...")
        
        # Clear current state
        self.selected_files.clear()
        self._clear_grid()
        
        # Load files in background
        def load_files():
            try:
                recursive = self.recursive_var.get()
                self.media_files = self.media_handler.get_files_in_directory(
                    directory, recursive=recursive
                )
                
                # Update UI in main thread
                self.root.after(0, self._populate_grid)
                
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Error", f"Failed to load directory: {e}"))
                
        thread = threading.Thread(target=load_files, daemon=True)
        thread.start()
        
    def _populate_grid(self):
        """Populate the grid with media files."""
        if not self.media_files:
            self.status_var.set("No supported media files found")
            return
            
        self.status_var.set(f"Loading thumbnails for {len(self.media_files)} files...")
        
        # Create grid items
        for i, filepath in enumerate(self.media_files):
            row = i // self.grid_columns
            col = i % self.grid_columns
            
            self._create_grid_item(filepath, row, col)
            
        # Start thumbnail loading
        self._load_thumbnails()
        
        # Update canvas scroll region
        self.root.after(100, self._update_scroll_region)
        
    def _create_grid_item(self, filepath: str, row: int, col: int):
        """Create a grid item for a media file."""
        # Create frame for this item
        item_frame = ttk.Frame(self.grid_frame, relief=tk.RAISED, borderwidth=1)
        item_frame.grid(row=row, column=col, padx=5, pady=5, sticky='nsew')
        
        # Configure grid weights
        self.grid_frame.grid_rowconfigure(row, weight=1)
        self.grid_frame.grid_columnconfigure(col, weight=1)
        
        # Thumbnail placeholder
        thumbnail_frame = ttk.Frame(item_frame, width=300, height=200)
        thumbnail_frame.pack(padx=5, pady=5)
        thumbnail_frame.pack_propagate(False)
        
        placeholder_label = ttk.Label(
            thumbnail_frame, 
            text="Loading...", 
            anchor=tk.CENTER
        )
        placeholder_label.pack(expand=True, fill=tk.BOTH)
        
        # Filename label
        filename = os.path.basename(filepath)
        name_label = ttk.Label(
            item_frame, 
            text=filename if len(filename) <= 30 else filename[:27] + "...",
            wraplength=280
        )
        name_label.pack(padx=5, pady=(0, 5))
        
        # Selection checkbox
        selected_var = tk.BooleanVar()
        checkbox = ttk.Checkbutton(
            item_frame,
            text="Select",
            variable=selected_var,
            command=lambda: self._toggle_selection(filepath, selected_var.get())
        )
        checkbox.pack(pady=(0, 5))
        
        # Store references
        item_frame.filepath = filepath
        item_frame.thumbnail_label = placeholder_label
        item_frame.selected_var = selected_var
        item_frame.thumbnail_frame = thumbnail_frame
        
        # Bind click events
        for widget in [item_frame, thumbnail_frame, placeholder_label, name_label]:
            widget.bind("<Button-1>", lambda e, fp=filepath: self._on_item_click(fp))
            widget.bind("<Double-Button-1>", lambda e, fp=filepath: self._on_item_double_click(fp))
            
    def _load_thumbnails(self):
        """Load thumbnails for all media files."""
        def progress_callback(current, total, filepath):
            progress = (current / total) * 100
            self.progress_var.set(progress)
            
            # Update thumbnail in UI
            self.root.after(0, lambda: self._update_thumbnail(filepath))
            
            if current == total:
                self.root.after(0, lambda: (
                    self.status_var.set(f"Loaded {len(self.media_files)} files"),
                    self.progress_var.set(0)
                ))
                
        self.media_handler.preload_thumbnails(self.media_files, progress_callback)
        
    def _update_thumbnail(self, filepath: str):
        """Update thumbnail for a specific file."""
        thumbnail = self.media_handler.create_thumbnail(filepath)
        
        if thumbnail:
            # Find the grid item for this file
            for child in self.grid_frame.winfo_children():
                if hasattr(child, 'filepath') and child.filepath == filepath:
                    child.thumbnail_label.configure(image=thumbnail, text="")
                    child.thumbnail_label.image = thumbnail  # Keep reference
                    break
                    
    def _clear_grid(self):
        """Clear all items from the grid."""
        for child in self.grid_frame.winfo_children():
            child.destroy()
            
    def _update_grid_columns(self):
        """Update the number of grid columns."""
        try:
            new_columns = int(self.columns_var.get())
            if 1 <= new_columns <= 8:
                self.grid_columns = new_columns
                self._refresh_view()
        except ValueError:
            self.columns_var.set(str(self.grid_columns))
            
    def _refresh_view(self):
        """Refresh the current view."""
        if self.current_directory:
            self.load_directory(self.current_directory)
            
    def _toggle_selection(self, filepath: str, selected: bool):
        """Toggle selection state of a file."""
        if selected:
            self.selected_files.add(filepath)
        else:
            self.selected_files.discard(filepath)
            
        self._update_selection_display()
        
        if self.on_selection_changed:
            self.on_selection_changed(list(self.selected_files))
            
    def _select_all(self):
        """Select all files."""
        self.selected_files = set(self.media_files)
        
        # Update checkboxes
        for child in self.grid_frame.winfo_children():
            if hasattr(child, 'selected_var'):
                child.selected_var.set(True)
                
        self._update_selection_display()
        
    def _clear_selection(self):
        """Clear all selections."""
        self.selected_files.clear()
        
        # Update checkboxes
        for child in self.grid_frame.winfo_children():
            if hasattr(child, 'selected_var'):
                child.selected_var.set(False)
                
        self._update_selection_display()
        
    def _update_selection_display(self):
        """Update the selection display."""
        count = len(self.selected_files)
        total = len(self.media_files)
        
        if count > 0:
            self.status_var.set(f"Selected {count} of {total} files")
        else:
            self.status_var.set(f"Loaded {total} files")
            
    def _keep_selected(self):
        """Keep only selected files (hide others)."""
        if not self.selected_files:
            messagebox.showwarning("Warning", "No files selected")
            return
            
        # Filter media files to only selected ones
        self.media_files = [f for f in self.media_files if f in self.selected_files]
        self.selected_files.clear()
        
        # Refresh display
        self._clear_grid()
        self._populate_grid()
        
    def _delete_selected(self):
        """Delete selected files (with confirmation)."""
        if not self.selected_files:
            messagebox.showwarning("Warning", "No files selected")
            return
            
        count = len(self.selected_files)
        result = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete {count} selected files?\n\nThis action cannot be undone."
        )
        
        if result:
            deleted_count = 0
            for filepath in list(self.selected_files):
                try:
                    os.remove(filepath)
                    deleted_count += 1
                except Exception as e:
                    print(f"Error deleting {filepath}: {e}")
                    
            messagebox.showinfo("Delete Complete", f"Deleted {deleted_count} of {count} files")
            self._refresh_view()
            
    def _on_item_click(self, filepath: str):
        """Handle item click - show preview."""
        self._show_preview(filepath)
        
    def _on_item_double_click(self, filepath: str):
        """Handle item double-click."""
        if self.on_file_double_click:
            self.on_file_double_click(filepath)
        else:
            # Default: open file with system default application
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
                messagebox.showerror("Error", f"Could not open file: {e}")
                
    def _show_preview(self, filepath: str):
        """Show preview of selected file."""
        self.current_preview = filepath
        
        # Update preview image
        thumbnail = self.media_handler.create_thumbnail(filepath)
        if thumbnail:
            self.preview_label.configure(image=thumbnail, text="")
            self.preview_label.image = thumbnail
        else:
            self.preview_label.configure(image="", text="Preview not available")
            
        # Update info text
        info = self.media_handler.get_media_info(filepath)
        info_text = self._format_file_info(info)
        
        self.preview_info_text.configure(state=tk.NORMAL)
        self.preview_info_text.delete(1.0, tk.END)
        self.preview_info_text.insert(1.0, info_text)
        self.preview_info_text.configure(state=tk.DISABLED)
        
    def _format_file_info(self, info: Dict) -> str:
        """Format file information for display."""
        lines = []
        lines.append(f"File: {info.get('filename', 'Unknown')}")
        lines.append(f"Type: {info.get('type', 'Unknown').title()}")
        
        if 'width' in info and 'height' in info:
            lines.append(f"Dimensions: {info['width']} × {info['height']}")
            
        if 'size' in info:
            size_mb = info['size'] / (1024 * 1024)
            lines.append(f"Size: {size_mb:.1f} MB")
            
        if info.get('type') == 'video':
            if 'duration' in info:
                duration = info['duration']
                mins, secs = divmod(int(duration), 60)
                lines.append(f"Duration: {mins:02d}:{secs:02d}")
                
            if 'fps' in info:
                lines.append(f"FPS: {info['fps']:.1f}")
                
            if 'frame_count' in info:
                lines.append(f"Frames: {info['frame_count']}")
                
        if 'error' in info:
            lines.append(f"Error: {info['error']}")
            
        return "\n".join(lines)
        
    def _on_canvas_configure(self, event):
        """Handle canvas resize."""
        self.grid_canvas.configure(scrollregion=self.grid_canvas.bbox('all'))
        
        # Update the window width to match canvas
        canvas_width = event.width
        self.grid_canvas.itemconfig(self.grid_canvas_window, width=canvas_width)
        
    def _on_frame_configure(self, event):
        """Handle frame resize."""
        self.grid_canvas.configure(scrollregion=self.grid_canvas.bbox('all'))
        
    def _update_scroll_region(self):
        """Update the scroll region."""
        self.grid_canvas.configure(scrollregion=self.grid_canvas.bbox('all'))
        
    def _on_mousewheel(self, event):
        """Handle mouse wheel scrolling."""
        if event.num == 4 or event.delta > 0:
            delta = -1
        elif event.num == 5 or event.delta < 0:
            delta = 1
        else:
            delta = 0
            
        self.grid_canvas.yview_scroll(delta, "units")
        
    def get_selected_files(self) -> List[str]:
        """Get list of currently selected files."""
        return list(self.selected_files)
        
    def set_selection_callback(self, callback: Callable[[List[str]], None]):
        """Set callback for selection changes."""
        self.on_selection_changed = callback
        
    def set_double_click_callback(self, callback: Callable[[str], None]):
        """Set callback for file double-click."""
        self.on_file_double_click = callback
        
    def run(self):
        """Start the application."""
        self.root.mainloop()
        
    def close(self):
        """Close the application."""
        self.media_handler.stop_loading.set()
        self.root.quit()
        self.root.destroy()