# Documentation

This folder is the main entry point for understanding `clevertools`. The goal is that someone who has never seen the package before can quickly answer four questions:

1. What does the library do?
2. Which helper should I use for my task?
3. How do the helpers behave on errors?
4. How do I wire everything together in a real script or app?

## Recommended reading order

If you are new to the project, read these pages in order:

1. [Installation](./installation.md)
2. [Getting Started](./getting-started.md)
3. [Quickstart](./quickstart.md)
4. [Tools](./tools/README.md)
5. [Concepts](./concepts/README.md)

## Choose a page by goal

Read [Installation](./installation.md) when you want:

- local setup instructions
- Python version requirements
- a quick editable install for development

Read [Getting Started](./getting-started.md) when you want:

- a fast orientation through the package
- to understand which helpers solve which kind of problem
- the best first pages to read next

Read [Quickstart](./quickstart.md) when you want:

- one realistic example that combines several helpers
- a compact workflow for config, file I/O, masking, and logging
- a starting point you can copy into a script

Read [Tools](./tools/README.md) when you want:

- the complete public API
- per-tool descriptions
- links to detailed pages and examples for each helper

Read [Concepts](./concepts/README.md) when you want:

- shared behavior that affects multiple helpers
- error-handling rules
- logging architecture and write modes

## Documentation layout

- `docs/installation.md` explains setup and environment requirements
- `docs/getting-started.md` gives a guided first tour
- `docs/quickstart.md` shows an end-to-end usage example
- `docs/tools/` contains one page per public helper
- `docs/concepts/` explains cross-cutting behavior

## Fast API map

### Core

- `configure()` stores defaults for error handling and logger behavior
- `log` gives you a ready-to-use shared logger
- `mask()` protects sensitive strings before output

### Files and config

- `read()` and `write()` for plain text and bytes
- `read_json()`, `read_toml()`, `read_yaml()` for structured reads
- `write_json()`, `write_toml()`, `write_yaml()` for structured writes
- `load_config()` for merging multiple config files into one object

### Logging

- `configure_logger()` for the standard logger setup path
- `start_file_logger()` and `stop_file_logger()` for early startup capture
- `get_logger()` for retrieving an existing logger
- `CleverToolsFormatter`, `build_console_handler()`, `build_file_handler()`, `reset_handlers()`, and `resolve_logger_options()` for lower-level control