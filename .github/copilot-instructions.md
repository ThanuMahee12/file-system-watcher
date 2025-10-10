# Copilot Instructions for SyncWeave (File System Watcher)

## Project Overview
- **Purpose:** Real-time monitoring of multiple directories for file system changes, with advanced logging and event handling.
- **Core Tech:** Python 3.12+, [watchdog](https://pypi.org/project/watchdog/), [loguru](https://pypi.org/project/loguru/)
- **Entry Point:** `main.py` (delegates to `watcher/` package)

## Key Components
- `watcher/main.py`: CLI argument parsing, orchestrates watcher startup.
- `watcher/Observer/observer.py` & `EventHandler.py`: Implements event handling logic using watchdog observers.
- `watcher/utils/logger.py`: Sets up multi-level logging (master logs, per-folder logs, rotation, colored output).

## Developer Workflows
- **Install dependencies:** `uv sync` (requires [uv](https://github.com/astral-sh/uv))
- **Run watcher:** `uv run python -m watcher <dir1> <dir2> [--logs <logdir>]`
- **Stop watcher:** Ctrl+C (handles graceful shutdown)

## Logging & Event Patterns
- All events are logged to `logs/monitor.log` and per-folder logs in `logs/folders/`.
- Log rotation and retention are handled automatically (see `README.md` for details).
- Each log entry is tagged with the watched directory for context.
- Event deduplication is implemented for Windows-specific duplicate events.

## Project Conventions
- **No hardcoded paths:** All directories are passed via CLI or config.
- **Log files auto-cleaned:** Per-folder logs are created/deleted as folders appear/disappear.
- **Colored output:** Loguru is configured for colorized console output by event type.
- **Error logs:** Errors are separated into `monitor-error.log`.

## Extending/Modifying
- Add new event types or custom handlers in `watcher/Observer/EventHandler.py`.
- Adjust logging behavior in `watcher/utils/logger.py`.
- For new CLI options, update `watcher/main.py`.

## Examples
- Watch two folders, custom log dir: `uv run python -m watcher ./a ./b --logs ./my-logs`
- All logs will be in `my-logs/` with per-folder logs in `my-logs/folders/`.

## References
- See `README.md` for full usage, architecture, and logging details.
- See `pyproject.toml` for dependencies and Python version.
