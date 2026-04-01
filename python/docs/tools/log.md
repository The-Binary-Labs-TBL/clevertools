# `log`

`log` is the shared default logger instance for the package. It is created with the default logger name `"clevertools"` and is useful when a single shared logger is enough.

## When to use it

Use `log` when:

- you are writing a small script
- one package-wide logger is sufficient
- you want to reuse defaults set with `configure()`

Use `get_logger()` or `configure_logger(name="...")` when you need separate named loggers.

## Example: simple script logger

```python
from clevertools import configure_logger, log

configure_logger(level="INFO", console_enabled=True, use_colors=False)
log.info("Application started")
```

## Example: combine with package defaults

```python
from clevertools import configure, configure_logger, log

configure(
    logger_overrides={
        "level": "DEBUG",
        "format_preset": "datetime",
        "console_enabled": True,
    }
)

configure_logger(use_colors=False)
log.debug("Debug logging is active")
```

## Notes

- `log` refers to the logger named `"clevertools"`.
- Re-running `configure_logger()` for the default logger updates the same underlying logger object.
- `configure_logger()` resets existing handlers first, so repeated setup does not duplicate messages.