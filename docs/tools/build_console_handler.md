# `build_console_handler`

`build_console_handler()` creates a `logging.StreamHandler` with `CleverToolsFormatter`.

## Signature

```python
build_console_handler(options: ResolvedLoggerOptions) -> logging.Handler
```

## Example

```python
import logging

from clevertools import build_console_handler, resolve_logger_options

options = resolve_logger_options(
    level="INFO",
    format_preset="default",
    fmt=None,
    date_format=None,
    console_enabled=True,
    file_logging_enabled=False,
    file_log_path=None,
    file_write_mode="runtime",
    use_colors=False,
)

logger = logging.getLogger("manual-console")
logger.addHandler(build_console_handler(options))
```

## Notes

- Most users should call `configure_logger()` instead of building handlers manually.