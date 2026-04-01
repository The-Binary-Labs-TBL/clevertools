# `get_logger`

`get_logger()` returns a named `logging.Logger` instance without modifying its handlers, level, or formatting.

## Signature

```python
get_logger(name: str = "clevertools") -> logging.Logger
```

## When to use it

Use `get_logger()` when:

- the logger is already configured elsewhere
- you only need the existing logger object
- you want to avoid resetting handlers

Use `configure_logger()` when you want setup and configuration, not only retrieval.

## Example: access an already configured logger

```python
from clevertools import configure_logger, get_logger

configure_logger(name="worker", level="INFO", console_enabled=True, use_colors=False)

logger = get_logger("worker")
logger.info("hello")
```

## Example: share a logger across modules

```python
from clevertools import get_logger

logger = get_logger("app")
logger.debug("module initialized")
```

## Notes

- This is a thin wrapper around `logging.getLogger(name)`.
- If the logger has not been configured yet, you still get a logger object, but it may not have handlers attached.