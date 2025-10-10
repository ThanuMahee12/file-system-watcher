# Gemini Project: File System Watcher

## Project Overview

This project is a Python-based file system watcher that monitors one or more directories for changes. It uses the `watchdog` library to receive real-time file system events and the `loguru` library for advanced, colored, and multi-level logging. The watcher is designed to be run from the command line and can be configured to watch multiple directories simultaneously and store logs in a custom location.

**Key Technologies:**

*   **Python:** >=3.12
*   **`watchdog`:** For monitoring file system events.
*   **`loguru`:** For flexible and powerful logging.
*   **`uv`:** For dependency management.

**Architecture:**

The project is structured as a Python package named `watcher`. The main entry point is `main.py`, which calls the `main` function in `watcher/main.py`. The core logic is split into several modules:

*   `watcher/main.py`: Handles command-line argument parsing, directory validation, and the main application loop.
*   `watcher/observer.py`: Contains the `FileSystemWatcher` class, which wraps the `watchdog` observer, and the `WatcherEventHandler` class, which handles file system events.
*   `watcher/utils/logger.py`: Configures `loguru` to provide multi-level logging, including a master log, an error log, and per-folder logs.

## Building and Running

This project uses `uv` for dependency management.

**Installation:**

```bash
# Clone the repository
git clone https://github.com/ThanuMahee12/file-system-watcher.git
cd file-system-watcher

# Install dependencies
uv sync
```

**Running the Watcher:**

```bash
# Watch a single directory
uv run python -m watcher /path/to/watch

# Watch multiple directories
uv run python -m watcher /path1 /path2 /path3

# Specify a custom log directory
uv run python -m watcher /path1 /path2 --logs /custom/logs
```

## Development Conventions

*   **Dependency Management:** The project uses `uv` to manage dependencies, which are listed in `pyproject.toml`.
*   **Code Style:** The code is well-structured and follows standard Python conventions.
*   **Logging:** The project uses `loguru` for logging. The logging configuration in `watcher/utils/logger.py` sets up a sophisticated multi-level logging system with colored console output, log rotation, and separate log files for master logs, error logs, and individual folders.
*   **Modularity:** The code is organized into modules with specific responsibilities, promoting maintainability and reusability.
