# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A Python filesystem watcher that monitors directories for changes using `watchdog` and logs all events with `loguru` - featuring real-time tracking, colored output, and automatic log rotation.

## Development Setup

This project uses `uv` for dependency management (Python >=3.12 required).

**Install dependencies:**
```bash
uv sync
```

**Run the watcher:**
```bash
# Watch single directory
uv run python -m watcher /path/to/watch

# Watch multiple directories
uv run python -m watcher /path1 /path2 /path3

# Specify custom log directory
uv run python -m watcher /path1 /path2 --logs /custom/logs
```

## Architecture

- **main.py** - Entry point that imports and runs `main()` from `watcher.main`
- **watcher/** - Main package directory
  - **main.py** - CLI argument parsing (`parse_arguments`), directory validation (`validate_directories`), and watcher orchestration
  - **Observer/** - Watchdog implementation
    - **observer.py** - Contains `WatcherEventHandler` (event handling with deduplication) and `FileSystemWatcher` (observer management)
    - **EventHandler.py** - Base import (minimal)
  - **utils/** - Utility modules
    - **logger.py** - Logger configuration with multi-level logging setup

### Key Architecture Notes

- Each `FileSystemWatcher` instance manages one watchdog Observer for a single directory (watcher/Observer/observer.py:50-79)
- Multiple watchers run concurrently but share the event loop from the first watcher (watcher/main.py:84-85)
- Event handler (`WatcherEventHandler`) uses `recently_created` set for Windows event deduplication (watcher/Observer/observer.py:18)
- Logger context binding (`logger.bind(watch_dir=...)`) is used throughout to tag events with their source directory

## Command Line Arguments

- **watch_dirs** (positional, required) - One or more directories to watch
- **--logs** (optional) - Custom log directory (default: `logs`)

All watch directories are validated before starting. Non-existent or invalid paths will cause the program to exit with an error.

## Logging Strategy

The watcher uses a sophisticated multi-level logging approach with watch directory context:

### Master Logs
- **{log_dir}/monitor.log** - All events with watch directory tags (100MB rotation, 30 days retention, ZIP compressed)
- **{log_dir}/monitor-error.log** - ERROR level events only (10MB rotation, 30 days retention, ZIP compressed)
- Format: `YYYY-MM-DD HH:mm:ss | LEVEL | watch_dir | message`

### Per-Folder Logs
- **{log_dir}/folders/{watchdir}_{foldername}.log** - Automatically created when a folder is created (watcher/utils/logger.py:46-64)
- Naming format includes parent watch directory to avoid conflicts
- Filters events via message content matching (`filter=lambda record: folder_name in record["message"]`)
- Automatically removed when the folder is deleted (watcher/Observer/observer.py:43-44)
- 5MB rotation with ZIP compression
- Handler IDs tracked in `folder_handlers` dict for proper cleanup

### Logger Functions
- `setup_logger(log_dir)` - Initializes console (colored), master log, and error log handlers. Sets default context `watch_dir: "UNKNOWN"`
- `add_folder_logger(folder_path, watch_dir, log_dir)` - Creates dedicated log for a folder, stores handler ID in `folder_handlers` dict
- `remove_folder_logger(folder_path)` - Removes folder-specific logging handler using stored handler ID

### Event Deduplication
The `WatcherEventHandler` maintains a `recently_created` set to prevent Windows from reporting file creation as "modified" (watcher/Observer/observer.py:18-30). Files are added on creation (line 28) and removed on deletion (line 38) or skipped during modification checks (line 22-23).

## Dependencies

- `loguru>=0.7.3` - Beautiful logging with colored output and automatic rotation
- `watchdog>=6.0.0` - Cross-platform filesystem event monitoring
