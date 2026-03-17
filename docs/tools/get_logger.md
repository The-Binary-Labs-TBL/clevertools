# `get_logger`

`get_logger()` returns a named `logging.Logger` instance without changing its handlers.

## Signature

```python
get_logger(name: str = "clevertools") -> logging.Logger
```

## Example

```python
from clevertools import configure_logger, get_logger

configure_logger(name="worker", level="INFO", console_enabled=True, use_colors=False)

logger = get_logger("worker")
logger.info("hello")
```

## Notes

- Use this when the logger may already be configured elsewhere.
- Use `configure_logger()` when you also want handlers and formatting to be set up.