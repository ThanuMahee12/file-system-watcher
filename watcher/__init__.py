"""File system watcher package for monitoring directory changes."""

from .main import main
from .observer import FileSystemWatcher, WatcherEventHandler
from .utils.logger import setup_logger, add_folder_logger, remove_folder_logger

__all__ = [
    "main",
    "FileSystemWatcher",
    "WatcherEventHandler",
    "setup_logger",
    "add_folder_logger",
    "remove_folder_logger",
]

__version__ = "1.0.0"