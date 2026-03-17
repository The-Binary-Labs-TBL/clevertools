# `CleverToolsFormatter`

`CleverToolsFormatter` is the custom formatter used by the built-in logger handlers.

## Signature

```python
CleverToolsFormatter(
    fmt: str,
    datefmt: str | None = None,
    *,
    use_colors: bool = False,
)
```

## Features

- injects `%(date)s` and `%(time)s` fields into log records
- can colorize `%(levelname)s` for TTY output
- restores the original record values after formatting

## Example

```python
import logging

from clevertools import CleverToolsFormatter

handler = logging.StreamHandler()
handler.setFormatter(
    CleverToolsFormatter(
        "%(name)s | %(levelname)s | [%(date)s] [%(time)s] = %(message)s",
        use_colors=False,
    )
)
```

## Notes

- `datefmt` only matters when your format string uses fields like `%(asctime)s`.
- The built-in presets rely on `%(date)s` and `%(time)s`, which are generated internally.