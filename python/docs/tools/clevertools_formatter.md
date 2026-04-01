# `CleverToolsFormatter`

`CleverToolsFormatter` is the custom formatter used by the built-in logging handlers in `clevertools`.

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

- injects `%(date)s` and `%(time)s` into each log record
- can colorize `%(levelname)s` when output is written to a TTY
- restores original record values after formatting so other handlers are not polluted

## Example: use the built-in structured fields

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

## Example: custom format

```python
import logging

from clevertools import CleverToolsFormatter

handler = logging.StreamHandler()
handler.setFormatter(
    CleverToolsFormatter(
        "[%(date)s %(time)s] %(levelname)s %(message)s",
        use_colors=False,
    )
)
```

## Notes

- `datefmt` only matters when your format string uses fields such as `%(asctime)s`.
- The formatter's custom `%(date)s` and `%(time)s` fields always use the library's internal date and time formats.