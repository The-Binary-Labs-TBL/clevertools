# Logging

`clevertools` includes helpers for simple logger setup.

## Main Helpers

- `configure_logger()` creates and configures a logger
- `get_logger()` returns a logger by name
- `configure()` can define default logger options

## Features

- console logging
- file logging
- configurable formatting
- optional colored output in terminals

## Example

```python
from clevertools import configure, configure_logger

configure(
    logger_overrides={
        "level": "INFO",
        "console_enabled": True,
    }
)

logger = configure_logger(name="app")
logger.info("ready")
```