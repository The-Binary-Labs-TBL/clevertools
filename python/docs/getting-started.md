# Getting Started

This page is a guided first tour of `clevertools`. If you only have a few minutes, this is the fastest way to understand what the package can do and which page you should read next.

## What clevertools helps with

`clevertools` groups a few common utility concerns into one small package:

- file I/O for text, bytes, JSON, TOML, and YAML
- shared error handling through `on_error`
- masking secrets before logging or displaying them
- merged config loading from multiple files
- logging setup for console and files

It is most useful in scripts, internal tools, CLIs, automation projects, and smaller applications where you want consistent helpers without introducing a larger framework.

## The three main areas

### 1. File and config helpers

Use these when you need to read or write files quickly and consistently:

- `read()` and `write()` for plain text and bytes
- `read_json()`, `read_toml()`, `read_yaml()` for structured reads
- `write_json()`, `write_toml()`, `write_yaml()` for structured writes
- `load_config()` when settings are split across several files

Example:

```python
from clevertools import read_json, write_yaml

payload = read_json("config/app.json", on_error="raise")
write_yaml("build/config.yaml", payload, sort_keys=False)
```

### 2. Safety and consistency helpers

Use these when you want predictable behavior across the package:

- `configure()` sets package-wide defaults
- `mask()` hides the middle part of a sensitive string

Example:

```python
from clevertools import configure, mask

configure(error_mode="raise")

print(mask("sk-demo-1234567890", 4, 2))
```

### 3. Logging helpers

Use these when you want fast logger setup without repeating standard-library boilerplate:

- `log` for the shared default logger
- `configure_logger()` for normal logger setup
- `start_file_logger()` when you need to capture startup output before your final logger config is ready
- `stop_file_logger()` to restore `stdout` and `stderr`

Example:

```python
from clevertools import configure_logger

logger = configure_logger(
    name="demo",
    level="INFO",
    console_enabled=True,
    file_logging_enabled=True,
    file_log_path="logs/demo.log",
    use_colors=False,
)

logger.info("ready")
```

## First steps for new users

1. Install the package with the instructions in [Installation](./installation.md).
2. Read [Quickstart](./quickstart.md) for one end-to-end example.
3. Open [Tools](./tools/README.md) to find the helper that matches your use case.
4. Read [Concepts](./concepts/README.md) if you want to understand shared behavior such as error handling and logger configuration.

## Which page should you read next?

- If you want to start using the package right away, go to [Quickstart](./quickstart.md).
- If you want the full API overview, go to [Tools](./tools/README.md).
- If you want to understand package-wide behavior, go to [Concepts](./concepts/README.md).