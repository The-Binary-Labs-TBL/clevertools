# clevertools

`clevertools` is a utility library providing practical tools for common
workflows.

## Public Tools

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

## Project Goal

`clevertools` is intentionally compact. It focuses on practical helpers for
everyday workflows without introducing a large framework or unnecessary
abstraction.

## Documentation

- Start here: [docs/README.md](./docs/README.md)
- Getting started: [docs/getting-started/README.md](./docs/getting-started/README.md)
- Reference: [docs/reference/README.md](./docs/reference/README.md)

## Requirements

- Python `>=3.10`