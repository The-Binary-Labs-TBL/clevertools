# `log`

`log` is the shared logger instance created by `configure_logger(name="clevertools")`.

## When to use it

- for small scripts
- when one global logger is enough
- when you want to reuse the defaults from `configure()`

## Example

```python
from clevertools import configure, configure_logger, log

configure(
    logger_overrides={
        "level": "INFO",
        "console_enabled": True,
    }
)

configure_logger(use_colors=False)
log.info("Application started")
```

## Notes

- `log` and `configure_logger()` point to the same logger object when the default name is used.
- Re-running `configure_logger()` resets handlers before attaching new ones.