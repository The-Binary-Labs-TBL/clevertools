# `configure_logger`

`configure_logger()` is the main entry point for logging in `clevertools`. It creates or refreshes a logger with the selected console and file handlers.

## Signature

```python
configure_logger(
    *,
    name: str = "clevertools",
    level: int | str | None = None,
    format_preset: Literal["default", "datetime"] | None = None,
    fmt: str | None = None,
    date_format: str | None = None,
    console_enabled: bool | None = None,
    file_logging_enabled: bool | None = None,
    file_log_path: str | Path | None = None,
    file_write_mode: Literal["runtime", "buffered"] = "runtime",
    use_colors: bool = True,
) -> logging.Logger
```

## What it does

- resolves final options from explicit arguments and `configure()`
- fetches the named logger
- resets existing handlers to avoid duplicates
- adds a console handler if enabled
- adds a file handler if enabled
- flushes any buffered startup records from `start_file_logger()`

## Example: normal application logger

```python
from clevertools import configure_logger

logger = configure_logger(
    name="worker",
    level="INFO",
    format_preset="datetime",
    console_enabled=True,
    file_logging_enabled=True,
    file_log_path="logs/worker.log",
    file_write_mode="buffered",
    use_colors=False,
)

logger.info("worker ready")
```

## Example: rely on stored defaults

```python
from clevertools import configure, configure_logger

configure(
    logger_overrides={
        "level": "DEBUG",
        "console_enabled": True,
        "format_preset": "default",
    }
)

logger = configure_logger(name="debug-run", use_colors=False)
logger.debug("using stored logger defaults")
```

## Notes

- If `fmt` is set, it overrides `format_preset`.
- If file logging is enabled and no path is provided, the default file path becomes `clevertools.log`.
- Reconfiguring the same logger replaces its handlers rather than stacking new ones on top.