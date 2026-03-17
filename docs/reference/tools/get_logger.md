# `get_logger`

`get_logger()` returns a named Python logger.

## Signature

```python
get_logger(name="clevertools")
```

## Example

```python
from clevertools import get_logger

logger = get_logger("worker")
logger.info("hello")
```