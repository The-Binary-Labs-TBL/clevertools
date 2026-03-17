# First Steps

This example shows a small workflow with file helpers, masking, and logging.

## Import

```python
from clevertools import configure, configure_logger, mask, read, write
```

## Example

```python
from clevertools import configure, configure_logger, mask, read, write

configure(error_mode="log")

logger = configure_logger(name="example", level="INFO")

write("demo.txt", f"api_key={mask('sk-demo-123456789', 4, 3)}")
content = read("demo.txt")

logger.info("Loaded content: %s", content)
```

## Next

- [Reference overview](../reference/README.md)
- [Tool reference](../reference/tools/README.md)