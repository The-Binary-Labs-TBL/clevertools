# Logging

`clevertools` includes a compact logging toolkit built on top of Python's standard `logging` module. It is designed for the common cases:

- configure a logger quickly
- avoid duplicate handlers
- write to console and file
- keep logger options consistent across the project
- optionally capture very early startup output

## The main logging pieces

- `log` is the shared default logger instance named `"clevertools"`
- `configure_logger()` is the standard high-level entry point
- `configure()` can store logger defaults for later calls
- `get_logger()` fetches a named logger without changing handlers
- `start_file_logger()` begins bootstrap logging before final configuration exists
- `stop_file_logger()` restores captured streams
- `CleverToolsFormatter` adds `date` and `time` fields and optional colors

## The normal workflow

For most applications, this is the path you want:

```python
from clevertools import configure, configure_logger

configure(
    logger_overrides={
        "level": "INFO",
        "format_preset": "datetime",
        "console_enabled": True,
        "file_logging_enabled": True,
        "file_log_path": "logs/app.log",
    }
)

logger = configure_logger(name="app", use_colors=False)
logger.info("ready")
```

What `configure_logger()` does:

- resolves final logger options from explicit arguments and global overrides
- resets existing handlers so repeated configuration does not duplicate output
- creates a console handler if enabled
- creates a file handler if enabled
- flushes any buffered bootstrap log records into the final handlers

## Format presets

### `default`

```text
%(name)s | [%(levelname)s] = %(message)s
```

### `datetime`

```text
%(name)s | %(levelname)s | [%(date)s] [%(time)s] = %(message)s
```

`CleverToolsFormatter` injects the `date` and `time` fields automatically, so these presets work without extra setup.

## Write modes

- `"runtime"` opens the log file in write mode and replaces previous content
- `"buffered"` opens the log file in append mode and keeps existing lines

Choose `"runtime"` when each run should start with a fresh file. Choose `"buffered"` when you want a cumulative log history.

## Bootstrap logging

Sometimes your program needs to log very early, before the final file path or logger format is known. That is what `start_file_logger()` is for.

Example:

```python
from clevertools import configure_logger, start_file_logger, stop_file_logger

start_file_logger(capture_stdout=True, capture_stderr=True)

print("starting application")

logger = configure_logger(
    name="app",
    console_enabled=False,
    file_logging_enabled=True,
    file_log_path="logs/app.log",
    use_colors=False,
)

logger.info("logger is fully configured")
stop_file_logger("app")
```

In this flow:

- startup logs are buffered in memory first
- `stdout` and `stderr` can be redirected into the logger
- `configure_logger()` replays the buffered records into the final handlers
- `stop_file_logger()` restores the original streams

## Global logger overrides

You can define default logger options once and reuse them throughout the project:

```python
from clevertools import configure, configure_logger

configure(
    logger_overrides={
        "level": "DEBUG",
        "console_enabled": True,
        "format_preset": "datetime",
    }
)

logger = configure_logger(name="worker", use_colors=False)
```

Explicit arguments still win over stored overrides.

## Low-level logging helpers

Most users do not need these directly, but they are available when you want more manual control:

- `resolve_logger_options()` computes the final logger config
- `build_console_handler()` creates a configured stream handler
- `build_file_handler()` creates a configured file handler
- `reset_handlers()` removes and closes old handlers
- `get_logger()` returns the underlying `logging.Logger`