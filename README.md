# File System Watcher

A Python filesystem watcher that monitors multiple directories for changes using `watchdog` and logs all events with `loguru` - featuring real-time tracking, colored output, multi-level logging, and automatic log rotation.

## Features

- 📂 **Multi-Directory Support** - Watch multiple directories simultaneously
- 📝 **Smart Logging** - Multi-level logging with master logs and per-folder logs
- 🎨 **Colored Output** - Beautiful colored console output for different event types
- 🔄 **Auto Rotation** - Automatic log rotation and compression
- 🏷️ **Context Tagging** - Each log entry tagged with watch directory name
- ✨ **Event Deduplication** - Intelligent handling of duplicate Windows events
- 🗂️ **Custom Log Directory** - Configurable log storage location

## Installation

This project uses `uv` for dependency management (Python >=3.12 required).

```bash
# Clone the repository
git clone https://github.com/ThanuMahee12/file-system-watcher.git
cd file-system-watcher

# Install dependencies
uv sync
```

## Usage

```bash
# Watch single directory
uv run python -m watcher /path/to/watch

# Watch multiple directories
uv run python -m watcher /path1 /path2 /path3

# Specify custom log directory
uv run python -m watcher /path1 /path2 --logs /custom/logs

# Example
uv run python -m watcher ./test ./data --logs ./my-logs
```

### Command Line Arguments

- **`watch_dirs`** (required) - One or more directories to watch
- **`--logs`** (optional) - Custom log directory (default: `logs`)

## Logging Structure

The watcher creates a sophisticated multi-level logging system:

### Master Logs
Located in `{log_dir}/`:
- **`monitor.log`** - All events from all watched directories
  - 100MB rotation, 30 days retention
  - Includes watch directory context
- **`monitor-error.log`** - Error events only
  - 10MB rotation, 30 days retention

### Per-Folder Logs
Located in `{log_dir}/folders/`:
- **`{watchdir}_{foldername}.log`** - Created automatically when a folder is created
- Tracks all events for that specific folder
- Automatically removed when folder is deleted
- 5MB rotation with ZIP compression

### Log Format

```
2025-10-04 14:52:09 | INFO     | test | Created: test\newfolder
2025-10-04 14:52:10 | SUCCESS  | data | Created: data\file.txt
2025-10-04 14:52:11 | WARNING  | test | Deleted: test\oldfile.txt
```

## Event Types

- **Created** - File or directory created (green/success)
- **Modified** - File or directory modified (blue/info)
- **Deleted** - File or directory deleted (yellow/warning)
- **Moved** - File or directory moved/renamed (blue/info)

## Architecture

```
file-system-watcher/
├── main.py              # Entry point
├── watcher/
│   ├── __init__.py      # Package initialization
│   ├── main.py          # CLI parsing & orchestration
│   ├── observer.py      # Watchdog event handlers
│   └── logger.py        # Multi-level logging setup
└── logs/                # Default log directory
    ├── monitor.log
    ├── monitor-error.log
    └── folders/
        └── test_newfolder.log
```

## Dependencies

- **`loguru>=0.7.3`** - Advanced logging with colors and rotation
- **`watchdog>=6.0.0`** - Cross-platform filesystem monitoring

## Stopping the Watcher

Press **Ctrl+C** to gracefully stop the watcher. All log file handles will be properly closed, allowing log files to be deleted or moved.




