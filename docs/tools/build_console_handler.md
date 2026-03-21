# `build_console_handler`

`build_console_handler()` creates a configured `logging.StreamHandler` using `CleverToolsFormatter`.

## Signature

```python
build_console_handler(options: ResolvedLoggerOptions) -> logging.Handler
```

## When to use it

Most users should prefer `configure_logger()`. Use `build_console_handler()` only when you want to assemble the logger manually.

## Example: manual console handler setup

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
logger.setLevel(options.level)
logger.addHandler(build_console_handler(options))
```

## Notes

- The handler uses `CleverToolsFormatter` internally.
- The optional stream is mainly used by the bootstrap logger path.