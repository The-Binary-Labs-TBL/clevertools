# `get_logger`

`get_logger()` returns a named Python logger.

## Signature

```python
get_logger(name="clevertools")
```

## Purpose

Use this helper when you only want to fetch a logger by name without changing
its handlers or configuration.

## Example

```python
from clevertools import get_logger

logger = get_logger("worker")
logger.info("hello")
```