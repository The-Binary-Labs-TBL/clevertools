# `configure_logger`

`configure_logger()` creates and configures a Python logger for console or file
output.

## Signature

```python
configure_logger(
    *,
    name="clevertools",
    level=None,
    fmt=None,
    date_format=None,
    console_enabled=None,
    file_logging_enabled=None,
    file_log_path=None,
    file_write_mode="runtime",
    use_colors=True,
)
```

## Typical Use Cases

- configure a console logger for scripts
- write logs to a file
- apply defaults from `configure()`

## Example

```python
from clevertools import configure_logger

logger = configure_logger(
    name="worker",
    level="INFO",
    file_logging_enabled=True,
    file_log_path="logs/worker.log",
)
```