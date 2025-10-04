import time
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from loguru import logger
from .logger import add_folder_logger, remove_folder_logger


class WatcherEventHandler(FileSystemEventHandler):
    """Handles filesystem events and logs them."""

    def __init__(self, watch_dir: Path, log_dir: Path):
        super().__init__()
        self.watch_dir = watch_dir
        self.log_dir = log_dir
        self.watch_dir_name = watch_dir.name
        # Track recently created files to avoid duplicate modified events
        self.recently_created = set()

    def on_modified(self, event):
        # Skip modified events for recently created files
        if event.src_path in self.recently_created:
            return
        logger.bind(watch_dir=self.watch_dir_name).info(f"Modified: {event.src_path}")

    def on_created(self, event):
        # Track this file as recently created
        self.recently_created.add(event.src_path)
        # Remove from tracking after a short delay (via on_modified skip)
        logger.bind(watch_dir=self.watch_dir_name).success(f"Created: {event.src_path}")

        # If a directory is created, start logging for it
        if event.is_directory:
            add_folder_logger(Path(event.src_path), self.watch_dir, self.log_dir)

    def on_deleted(self, event):
        # Remove from recently created tracking
        self.recently_created.discard(event.src_path)

        logger.bind(watch_dir=self.watch_dir_name).warning(f"Deleted: {event.src_path}")

        # If a directory is deleted, stop logging for it
        if event.is_directory:
            remove_folder_logger(Path(event.src_path))

    def on_moved(self, event):
        logger.bind(watch_dir=self.watch_dir_name).info(f"Moved: {event.src_path} -> {event.dest_path}")


class FileSystemWatcher:
    """Manages filesystem observation."""

    def __init__(self, watch_path: Path, log_dir: Path):
        self.watch_path = watch_path
        self.log_dir = log_dir
        self.event_handler = WatcherEventHandler(watch_path, log_dir)
        self.observer = Observer()

    def start(self):
        """Start watching the filesystem."""
        self.observer.schedule(self.event_handler, str(self.watch_path), recursive=True)
        self.observer.start()
        logger.bind(watch_dir=self.watch_path.name).info(f"Watching directory: {self.watch_path}")
        logger.bind(watch_dir="SYSTEM").info("Press Ctrl+C to quit")

    def run(self):
        """Run the watcher until interrupted."""
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            logger.bind(watch_dir=self.watch_path.name).info("Stopping watcher...")
            self.stop()

    def stop(self):
        """Stop the observer."""
        self.observer.stop()
        self.observer.join()
        logger.bind(watch_dir=self.watch_path.name).success("Watcher stopped")
