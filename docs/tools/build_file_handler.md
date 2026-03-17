# `build_file_handler`

`build_file_handler()` creates a file-based log handler with the configured formatter.

## Signature

```python
build_file_handler(options: ResolvedLoggerOptions) -> logging.Handler
```

## Example

```python
import logging

from clevertools import build_file_handler, resolve_logger_options

options = resolve_logger_options(
    level="INFO",
    format_preset="datetime",
    fmt=None,
    date_format=None,
    console_enabled=False,
    file_logging_enabled=True,
    file_log_path="logs/manual.log",
    file_write_mode="buffered",
    use_colors=False,
)

logger = logging.getLogger("manual-file")
logger.addHandler(build_file_handler(options))
```

## Notes

- Missing parent folders for the log file are created automatically.
- `"runtime"` overwrites the log file and `"buffered"` appends to it.