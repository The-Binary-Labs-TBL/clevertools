# Logging

`clevertools` includes helpers for simple logger setup.

## Main Helpers

- `log` is the shared global logger instance
- `configure_logger()` creates and configures a logger
- `get_logger()` returns a logger by name
- `configure()` can define default logger options

## Features

- console logging
- file logging
- configurable formatting
- two built-in default format presets
- optional colored output in terminals

## Example

```python
from clevertools import configure, configure_logger, log

configure(
    logger_overrides={
        "level": "INFO",
        "console_enabled": True,
        "format_preset": "datetime",
    }
)

configure_logger()
log.info("ready")
```