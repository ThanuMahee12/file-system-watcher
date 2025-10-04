import sys
from pathlib import Path
from loguru import logger


# Track folder-specific log handlers
folder_handlers = {}


def setup_logger(log_dir: Path = Path("logs")):
    """Configure loguru logger with colored output and file rotation."""
    logger.remove()  # Remove default handler

    # Create log directory if it doesn't exist
    log_dir.mkdir(parents=True, exist_ok=True)

    # Console output with default watch_dir
    logger.add(
        sys.stderr,
        colorize=True,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{extra[watch_dir]}</cyan> | <level>{message}</level>"
    )

    # Master logs with watch directory context
    logger.add(
        log_dir / "monitor.log",
        rotation="100 MB",
        retention="30 days",
        compression="zip",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {extra[watch_dir]} | {message}"
    )

    logger.add(
        log_dir / "monitor-error.log",
        rotation="10 MB",
        retention="30 days",
        compression="zip",
        level="ERROR",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {extra[watch_dir]} | {message}"
    )

    # Configure default context
    logger.configure(extra={"watch_dir": "UNKNOWN"})


def add_folder_logger(folder_path: Path, watch_dir: Path, log_dir: Path):
    """Add a dedicated log file for a specific folder."""
    folder_name = folder_path.name
    watch_dir_name = watch_dir.name

    # Create folder log path: logs/folders/watchdir_foldername.log
    log_path = log_dir / "folders" / f"{watch_dir_name}_{folder_name}.log"
    log_path.parent.mkdir(parents=True, exist_ok=True)

    # Add handler and store its ID
    handler_id = logger.add(
        str(log_path),
        rotation="5 MB",
        compression="zip",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {message}",
        filter=lambda record: folder_name in record["message"]
    )

    folder_handlers[str(folder_path)] = handler_id


def remove_folder_logger(folder_path: Path):
    """Remove the log handler for a deleted folder."""
    folder_key = str(folder_path)
    if folder_key in folder_handlers:
        logger.remove(folder_handlers[folder_key])
        del folder_handlers[folder_key]
