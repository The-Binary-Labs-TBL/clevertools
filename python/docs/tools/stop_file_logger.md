# `stop_file_logger`

`stop_file_logger()` stops bootstrap stream capture for a logger and restores the original `stdout` and `stderr` streams if they were redirected.

## Signature

```python
stop_file_logger(name: str = "clevertools") -> None
```

## When to use it

Use this after `start_file_logger()` when:

- you captured `stdout`
- you captured `stderr`
- your final logger configuration is already in place
- you want normal console stream behavior back

## Example

```python
from clevertools import configure_logger, start_file_logger, stop_file_logger

start_file_logger(name="app", capture_stdout=True, capture_stderr=True)

print("booting")

logger = configure_logger(
    name="app",
    console_enabled=False,
    file_logging_enabled=True,
    file_log_path="logs/app.log",
    use_colors=False,
)

logger.info("ready")
stop_file_logger("app")
```

## Notes

- Calling it for a logger that is not in bootstrap mode does nothing.
- It restores streams but does not remove your final logger handlers.
- Buffered records are replayed by `configure_logger()`, not by `stop_file_logger()` itself.