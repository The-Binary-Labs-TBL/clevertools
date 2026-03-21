# `reset_handlers`

`reset_handlers()` removes and closes all handlers attached to a logger.

## Signature

```python
reset_handlers(logger: logging.Logger) -> None
```

## When to use it

Use this when you manage loggers manually and want a clean handler state before attaching new ones.

## Example

```python
from clevertools import configure_logger, reset_handlers

logger = configure_logger(name="cleanup-demo", console_enabled=True, use_colors=False)
reset_handlers(logger)
```

## Notes

- `configure_logger()` already calls this internally before attaching fresh handlers.
- Closing handlers matters because file handlers may otherwise keep file descriptors open.