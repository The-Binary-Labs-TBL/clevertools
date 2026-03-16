# `configure`

`configure()` sets global defaults for `clevertools`.

## Signature

```python
configure(*, error_mode=None, logger_overrides=None)
```

## Parameters

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