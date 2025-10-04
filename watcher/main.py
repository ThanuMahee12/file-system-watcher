import sys
import argparse
from pathlib import Path
from loguru import logger
from .logger import setup_logger
from .observer import FileSystemWatcher


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Filesystem watcher with advanced logging",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m watcher /path/to/watch
  python -m watcher /path1 /path2 /path3
  python -m watcher /path1 /path2 --log-dir /custom/logs
        """
    )

    parser.add_argument(
        'watch_dirs',
        nargs='+',
        type=str,
        help='One or more directories to watch (required)'
    )

    parser.add_argument(
        '--logs',
        type=str,
        default='logs',
        help='Directory to store logs (default: logs)'
    )

    return parser.parse_args()


def validate_directories(watch_dirs):
    """Validate that all watch directories exist."""
    invalid_dirs = []
    valid_paths = []

    for dir_path in watch_dirs:
        path = Path(dir_path)
        if not path.exists():
            invalid_dirs.append(dir_path)
        elif not path.is_dir():
            logger.error(f"Not a directory: {dir_path}")
            invalid_dirs.append(dir_path)
        else:
            valid_paths.append(path)

    if invalid_dirs:
        logger.error(f"Invalid directories: {', '.join(invalid_dirs)}")
        sys.exit(1)

    return valid_paths


def main():
    """Main entry point for the filesystem watcher."""
    # Parse command line arguments
    args = parse_arguments()

    # Validate watch directories
    watch_paths = validate_directories(args.watch_dirs)

    # Setup logger with custom log directory
    log_dir = Path(args.logs)
    setup_logger(log_dir)

    logger.bind(watch_dir="SYSTEM").info(f"Starting filesystem watcher for {len(watch_paths)} director{'y' if len(watch_paths) == 1 else 'ies'}")

    # Create watchers for each directory
    watchers = []
    for watch_path in watch_paths:
        watcher = FileSystemWatcher(watch_path, log_dir)
        watcher.start()
        watchers.append(watcher)

    # Run all watchers (blocks until Ctrl+C)
    try:
        if watchers:
            watchers[0].run()
    except KeyboardInterrupt:
        logger.bind(watch_dir="SYSTEM").info("Stopping all watchers...")
        for watcher in watchers:
            watcher.stop()
    finally:
        # Close all logger handlers to release file locks
        logger.complete()


if __name__ == "__main__":
    main()