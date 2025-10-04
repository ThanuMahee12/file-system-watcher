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
# Watch single directory (default: logs/)
python -m watcher /path/to/watch

# Watch multiple directories
python -m watcher /path1 /path2 /path3

# Specify custom log directory
python -m watcher /path1 /path2 --logs /custom/logs
```

## Architecture

- **main.py** - Entry point that imports and runs `main()` from the watcher package
- **watcher/** - Main package directory containing the core watcher implementation
  - **__init__.py** - Package initialization (currently minimal)
  - **main.py** - CLI argument parsing, validation, and watcher orchestration
  - **observer.py** - Watchdog event handlers and filesystem observation logic
  - **logger.py** - Logger configuration with multi-level logging strategy

## Command Line Arguments

- **watch_dirs** (positional, required) - One or more directories to watch
- **--logs** (optional) - Custom log directory (default: `logs`)

All watch directories are validated before starting. Non-existent or invalid paths will cause the program to exit with an error.

## Logging Strategy

The watcher uses a sophisticated multi-level logging approach with watch directory context:

### Master Logs
- **{log_dir}/monitor.log** - All events with watch directory tags (100MB rotation, 30 days retention)
- **{log_dir}/monitor-error.log** - Errors only (10MB rotation, 30 days retention)
- Format: `YYYY-MM-DD HH:mm:ss | LEVEL | watch_dir | message`

### Per-Folder Logs
- **{log_dir}/folders/watchdir_foldername.log** - Automatically created when a folder is created
- Naming format includes parent watch directory to avoid conflicts
- Tracks all events related to that specific folder
- Automatically removed when the folder is deleted
- 5MB rotation with compression

### Logger Functions
- `setup_logger(log_dir)` - Initializes console and master log handlers with custom directory
- `add_folder_logger(folder_path, watch_dir, log_dir)` - Creates dedicated log for a folder
- `remove_folder_logger(folder_path)` - Removes folder-specific logging handler

### Event Deduplication
The event handler tracks recently created files to prevent Windows from reporting file creation as "modified". This ensures accurate event reporting.

## Dependencies

- `loguru>=0.7.3` - Beautiful logging with colored output and automatic rotation
- `watchdog>=6.0.0` - Cross-platform filesystem event monitoring
