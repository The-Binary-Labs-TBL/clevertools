# `configure_logger`

`configure_logger()` creates or reconfigures a logger with console and file handlers.

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
- resets existing handlers to avoid duplicate output
- optionally adds a console handler
- optionally adds a file handler

## Example

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

## Notes

- If `fmt` is set, it wins over `format_preset`.
- `file_log_path` defaults to `clevertools.log` when file logging is enabled and no path is given.