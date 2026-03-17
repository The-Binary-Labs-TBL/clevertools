# `configure_logger`

`configure_logger()` creates and configures a Python logger for console or file
output.

## Signature

```python
configure_logger(
    *,
    name="clevertools",
    level=None,
    format_preset=None,
    fmt=None,
    date_format=None,
    console_enabled=None,
    file_logging_enabled=None,
    file_log_path=None,
    file_write_mode="runtime",
    use_colors=True,
)
```

## Common Uses

- configure a console logger for scripts
- write logs to a file
- apply defaults from `configure()`
- choose between the built-in default formats

## Example

```python
from clevertools import configure_logger

logger = configure_logger(
    name="worker",
    level="INFO",
    format_preset="datetime",
    file_logging_enabled=True,
    file_log_path="logs/worker.log",
)
```

## Built-In Formats

- `"default"`: `%(name)s | [%(levelname)s] %(message)s`
- `"datetime"`: `%(name)s | %(levelname)s | [%(date)s] [%(time)s] %(message)s`