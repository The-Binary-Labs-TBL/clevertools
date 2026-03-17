# Logging

`clevertools` ships with a small logging toolkit that covers the common cases without a lot of setup.

## Main pieces

- `log` is the shared default logger instance.
- `configure_logger()` builds and resets logger handlers safely.
- `get_logger()` returns a named logger without configuring handlers.
- `configure()` can define logger defaults for later calls.
- `CleverToolsFormatter` adds `date` and `time` fields and optional colorized levels.

## Built-in format presets

- `"default"` renders `%(name)s | [%(levelname)s] = %(message)s`
- `"datetime"` renders `%(name)s | %(levelname)s | [%(date)s] [%(time)s] = %(message)s`

## Typical setup

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

logger = configure_logger(use_colors=False)
logger.info("ready")
```

## Write modes

- `"runtime"` opens the file in write mode and replaces old content.
- `"buffered"` opens the file in append mode and keeps older log lines.
