"""
Media Bridge Viewer - Adobe Bridge-style media comparison tool.

A standalone package for viewing and comparing multiple media files
(images, videos) in a grid layout with selection capabilities.
"""

__version__ = "0.1.0"
__author__ = "Your Name"

from .viewer import MediaBridgeViewer
from .media_handler import MediaHandler
from .remote import RemoteMediaViewer, RemoteMediaHandler

__all__ = ["MediaBridgeViewer", "MediaHandler", "RemoteMediaViewer", "RemoteMediaHandler"]