# `configure`

`configure()` sets global defaults for `clevertools`.

## Purpose

Use this helper to define shared package behavior once instead of repeating the
same options on every call.

## Signature

```python
configure(*, error_mode=None, logger_overrides=None)
```

## Options

- `error_mode`: one of `"raise"`, `"log"`, or `"silent"`
- `logger_overrides`: default keyword arguments used by `configure_logger()`

## Example

```python
from clevertools import configure

configure(
    error_mode="log",
    logger_overrides={
        "level": "DEBUG",
        "console_enabled": True,
    },
)
```