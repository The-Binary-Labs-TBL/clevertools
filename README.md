# clevertools

`clevertools` is a practical Python helper library for everyday application code. It focuses on the boring but important parts that show up in many projects: reading and writing files, handling JSON/TOML/YAML, masking sensitive values, loading split configuration, and setting up logging without repetitive boilerplate.

The package is intentionally small, but it still gives you enough structure that a new teammate can open the project and understand how configuration, file access, and logging are supposed to work.

## What clevertools is for

Use `clevertools` when you want:

- a consistent way to read and write text, bytes, JSON, TOML, and YAML
- one shared error-handling model across helpers
- simple masking for API keys, tokens, emails, IDs, and similar values
- merged configuration from multiple files with dot access
- fast logger setup for console and file logging
- lower-level logging primitives when you need custom control

## What is included

### Core helpers

- `configure()` stores package-wide defaults such as error handling and logger overrides
- `log` is the shared default logger
- `mask()` partially hides sensitive strings before you log or display them

### File helpers

- `read()` and `write()` handle plain text and raw bytes
- `ensure_file()` and `ensure_dir()` make sure file and directory paths exist
- `read_json()` and `write_json()` handle JSON files
- `read_toml()` and `write_toml()` handle TOML files
- `read_yaml()` and `write_yaml()` handle YAML files
- `load_config()` merges multiple config files into one object

### Logging helpers

- `configure_logger()` creates or refreshes a logger with console and file handlers
- `start_file_logger()` captures early startup output before final logger setup is ready
- `stop_file_logger()` restores captured `stdout` and `stderr`
- `get_logger()` returns a named logger without modifying it
- `CleverToolsFormatter` adds structured time fields and optional colors
- `build_console_handler()` and `build_file_handler()` expose the low-level handler builders
- `reset_handlers()` safely clears existing handlers
- `resolve_logger_options()` shows the final logger settings after overrides are applied

## Quick example

```python
from clevertools import (
    configure,
    configure_logger,
    load_config,
    mask,
    read_json,
    write_json,
)

configure(
    error_mode="raise",
    logger_overrides={
        "level": "INFO",
        "format_preset": "datetime",
        "console_enabled": True,
    },
)

logger = configure_logger(name="billing", use_colors=False)

payload = {
    "service": "billing",
    "token": mask("sk-demo-123456789", 4, 3),
    "retries": 3,
}

write_json("tmp/config.json", payload, indent=2, ensure_ascii=False)
loaded = read_json("tmp/config.json")

logger.info("Loaded config: %s", loaded)

config = load_config("config/base.toml", "config/local.yaml")
logger.info("Feature enabled: %s", config.get("features.billing.enabled"))
```

## Typical workflows

### 1. Read and write structured files

```python
from clevertools import read_toml, write_yaml

settings = read_toml("settings.toml", on_error="raise")
write_yaml("build/settings.yaml", settings, sort_keys=False)
```

### 2. Hide secrets before logging

```python
from clevertools import mask, log

token = "sk-prod-abcdef1234567890"
log.info("Using token %s", mask(token, 5, 4))
```

### 3. Merge config from multiple sources

```python
from clevertools import load_config

config = load_config(
    "config/defaults.toml",
    "config/team.json",
    "config/local.yaml",
)

print(config.database.host)
print(config.get("features.search.enabled", False))
```

### 4. Set up application logging

```python
from clevertools import configure_logger

logger = configure_logger(
    name="worker",
    level="INFO",
    format_preset="datetime",
    console_enabled=True,
    file_logging_enabled=True,
    file_log_path="logs/worker.log",
    file_write_mode="buffered",
    use_colors=False,
)

logger.info("worker started")
```

## Error handling model

Most helpers support `on_error`. If you do not pass it, the package-wide default from `configure()` is used.

- `"raise"` raises the original exception
- `"log"` logs the error and returns the helper's fallback value
- `"silent"` suppresses the error and returns the helper's fallback value

Example:

```python
from clevertools import configure, read_json

configure(error_mode="silent")

payload = read_json("missing.json")
print(payload)  # None
```

## Documentation map

If this is your first time in the repository, read the docs in this order:

1. [docs/README.md](./docs/README.md)
2. [docs/installation.md](./docs/installation.md)
3. [docs/quickstart.md](./docs/quickstart.md)
4. [docs/tools/README.md](./docs/tools/README.md)
5. [docs/concepts/README.md](./docs/concepts/README.md)

Important reference pages:

- [docs/getting-started.md](./docs/getting-started.md) for a guided first run
- [docs/tools/README.md](./docs/tools/README.md) for the full API map
- [docs/concepts/error-handling.md](./docs/concepts/error-handling.md) for shared fallback behavior
- [docs/concepts/logging.md](./docs/concepts/logging.md) for logger architecture and write modes

## Repository layout

- `src/clevertools/` contains the library code
- `tests/` contains the automated test suite
- `docs/` contains the user-facing documentation
- `README.md` is the first overview for new users

## Installation

```bash
pip install -e .
```

For a full local setup including virtual environments and dependencies, see [docs/installation.md](./docs/installation.md).

## Requirements

- Python `>=3.11`