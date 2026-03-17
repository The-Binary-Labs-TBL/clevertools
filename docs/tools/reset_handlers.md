# `reset_handlers`

`reset_handlers()` removes and closes all handlers attached to a logger.

## Signature

```python
reset_handlers(logger: logging.Logger) -> None
```

## Example

```python
from clevertools import configure_logger, reset_handlers

logger = configure_logger(name="cleanup-demo", console_enabled=True, use_colors=False)
reset_handlers(logger)
```

## Notes

- `configure_logger()` already calls this internally before adding new handlers.
- This is useful when you manage handlers yourself and want to avoid duplicates.