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
python main.py
```

Or via the watcher module:
```bash
python -m watcher
```

## Architecture

- **main.py** - Entry point that imports and runs `main()` from the watcher package
- **watcher/** - Main package directory containing the core watcher implementation
  - **__init__.py** - Package initialization (currently minimal)
  - **main.py** - Contains the watcher logic and event handlers

The project is in early development. The actual filesystem watching implementation using `watchdog` and logging with `loguru` is expected to be in `watcher/main.py`.

## Dependencies

- `loguru>=0.7.3` - Beautiful logging with colored output and automatic rotation
- `watchdog>=6.0.0` - Cross-platform filesystem event monitoring
