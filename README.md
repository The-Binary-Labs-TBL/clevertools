# clevertools

`clevertools` is a small utility library for common everyday tasks.

## Included Tools

- plain-text file helpers
- masking for sensitive values
- global runtime configuration
- simple console and file logger setup

## Example

```python
from clevertools import mask, read

secret = mask("sk-example-secret-token", 3, 4)
content = read("example.txt")
```

## Why It Exists

`clevertools` stays intentionally small. It gives you practical helpers without
turning simple workflows into a framework.

## Documentation

- [Documentation home](./docs/README.md)
- [Getting started](./docs/getting-started/README.md)
- [Reference](./docs/reference/README.md)

## Requirements

- Python `>=3.10`