# Quickstart

This quickstart shows a realistic small workflow that uses the most important parts of `clevertools` together:

- package-wide defaults with `configure()`
- logger setup with `configure_logger()`
- safe output with `mask()`
- structured file I/O with `write_json()` and `read_json()`
- merged configuration with `load_config()`

## End-to-end example

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
        "file_logging_enabled": True,
        "file_log_path": "logs/app.log",
    },
)

logger = configure_logger(name="demo", use_colors=False)

payload = {
    "service": "billing",
    "environment": "dev",
    "token": mask("sk-demo-123456789", 4, 3),
}

write_json("tmp/config.json", payload, indent=2, ensure_ascii=False)
loaded = read_json("tmp/config.json")

logger.info("Loaded payload: %s", loaded)

config = load_config("config/base.toml", "config/local.yaml")
logger.info("Billing enabled: %s", config.get("features.billing.enabled"))
```

## What happens in this example

1. `configure()` stores defaults for error handling and logger setup.
2. `configure_logger()` builds the final logger from those defaults.
3. `mask()` hides the sensitive part of the token before it is written anywhere.
4. `write_json()` writes a formatted JSON file and creates parent folders if needed.
5. `read_json()` loads the file again.
6. `load_config()` merges several config files into one object with attribute access and dot-path lookups.

## Smaller examples

### Plain file I/O

```python
from clevertools import read, write

write("tmp/notes.txt", "Hello from clevertools")
content = read("tmp/notes.txt")
print(content)
```

### TOML to YAML conversion

```python
from clevertools import read_toml, write_yaml

settings = read_toml("settings.toml", on_error="raise")
write_yaml("build/settings.yaml", settings, sort_keys=False)
```

### Shared logger for a simple script

```python
from clevertools import configure_logger, log

configure_logger(level="INFO", console_enabled=True, use_colors=False)
log.info("script started")
```

## Recommended next steps

- Read [Tools](./tools/README.md) for the full public API and per-tool examples.
- Read [Concepts](./concepts/README.md) for shared behavior such as `on_error`, logger presets, and write modes.