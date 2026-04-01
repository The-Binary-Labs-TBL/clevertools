# `configure`

`configure()` stores package-wide defaults for `clevertools`. It is the central place to define how helpers should behave when you do not want to pass the same options on every call.

## Signature

```python
configure(
    *,
    error_mode: Literal["raise", "log", "silent"] | None = None,
    logger_overrides: dict[str, Any] | None = None,
)
```

## What it controls

- `error_mode` becomes the default for helpers that support `on_error`
- `logger_overrides` becomes the default option set that `configure_logger()` will reuse later

## Return value

Returns a copy of the active configuration snapshot.

## Example: set a strict default

```python
from clevertools import configure, read_json

configure(error_mode="raise")

payload = read_json("config.json")
```

## Example: store logger defaults once

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

logger = configure_logger(name="app", use_colors=False)
```

## Notes

- Unsupported `error_mode` values raise `ValueError`.
- Passing `logger_overrides` replaces the stored override dictionary instead of merging into the previous one.
- Explicit arguments passed directly to `configure_logger()` still win over stored overrides.