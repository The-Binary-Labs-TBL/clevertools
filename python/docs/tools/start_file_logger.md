# `start_file_logger`

`start_file_logger()` starts bootstrap logging for early application startup. It buffers log records in memory until you later call `configure_logger()` with the final handlers and file path.

## Signature

```python
start_file_logger(
    *,
    name: str = "clevertools",
    level: int | str = "INFO",
    capture_stdout: bool = False,
    capture_stderr: bool = False,
) -> logging.Logger
```

## What it does

- resets the current handlers for the selected logger
- adds an in-memory handler for startup records
- can redirect `stdout` into the logger at `INFO` level
- can redirect `stderr` into the logger at `ERROR` level
- keeps the records until `configure_logger()` replays them into the final handlers

## Example: capture startup output

```python
from clevertools import configure_logger, start_file_logger

start_file_logger(name="app", capture_stdout=True, capture_stderr=True)

print("booting")

logger = configure_logger(
    name="app",
    file_logging_enabled=True,
    file_log_path="logs/app.log",
    console_enabled=False,
    use_colors=False,
)

logger.info("ready")
```

## Example: bootstrap only logger messages

```python
from clevertools import get_logger, start_file_logger

logger = start_file_logger(name="setup", level="DEBUG")
logger.debug("starting setup phase")

existing = get_logger("setup")
existing.info("same logger instance")
```

## Notes

- Output written before `start_file_logger()` starts cannot be captured retroactively.
- Call `configure_logger()` once the final logger format and destination are known.
- If you redirected streams, finish by calling `stop_file_logger()`.