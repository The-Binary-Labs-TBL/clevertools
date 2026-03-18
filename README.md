# clevertools

`clevertools` is a compact Python utility library for everyday workflows like file I/O, masking sensitive values, runtime configuration, and logger setup.

## What You Get

- simple text and binary file helpers
- JSON and TOML read/write helpers
- masking for tokens, secrets, IDs, and similar values
- global configuration for shared error behavior
- ready-to-use console and file logging
- lower-level logging utilities when you need more control

## Quick Example

```python
from clevertools import configure, configure_logger, mask, read_json, write_json

configure(
    error_mode="raise",
    logger_overrides={
        "level": "INFO",
        "console_enabled": True,
    },
)

logger = configure_logger(name="demo", use_colors=False)

payload = {
    "service": "billing",
    "token": mask("sk-demo-123456789", 4, 3),
}

write_json("tmp/config.json", payload)
loaded = read_json("tmp/config.json")

logger.info("Loaded config: %s", loaded)
```

For split TOML setups, `load_config()` merges multiple files into one config object with dot access.

## Public API Overview

### Core

- `configure`
- `log`
- `mask`

### File helpers

- `read`
- `write`
- `read_json`
- `write_json`
- `read_toml`
- `write_toml`
- `load_config`

### Logging helpers

- `configure_logger`
- `get_logger`
- `CleverToolsFormatter`
- `build_console_handler`
- `build_file_handler`
- `reset_handlers`
- `resolve_logger_options`

## Why It Exists

`clevertools` stays intentionally small. It focuses on practical helpers that are easy to drop into scripts and small projects without turning simple tasks into a framework.

## Repository Guide

- [docs/README.md](./docs/README.md) is the documentation entry point
- [docs/installation.md](./docs/installation.md) shows local setup
- [docs/quickstart.md](./docs/quickstart.md) shows an end-to-end example
- [docs/tools/README.md](./docs/tools/README.md) lists every tool page
- [docs/concepts/README.md](./docs/concepts/README.md) explains shared behavior
- [src/clevertools](./src/clevertools) contains the implementation
- [tests](./tests) contains the test suite

## Installation

```bash
pip install -e .
```

For a full local setup, see [docs/installation.md](./docs/installation.md).

## Requirements

- Python `>=3.11`