# `configure`

`configure()` updates the global `clevertools` defaults.

## Signature

```python
configure(
    *,
    error_mode: Literal["raise", "log", "silent"] | None = None,
    logger_overrides: dict[str, Any] | None = None,
)
```

## What it changes

- `error_mode` sets the default behavior for helpers that support `on_error`.
- `logger_overrides` stores default arguments that `configure_logger()` will use later.

## Returns

Returns a copy of the active configuration snapshot.

## Example

```python
from clevertools import configure

config = configure(
    error_mode="raise",
    logger_overrides={
        "level": "DEBUG",
        "console_enabled": True,
        "format_preset": "datetime",
    },
)

print(config.error_mode)
```

## Notes

- Unsupported `error_mode` values raise `ValueError`.
- A later call replaces the stored `logger_overrides` dictionary.