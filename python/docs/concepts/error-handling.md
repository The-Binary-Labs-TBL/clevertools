# Error Handling

Many `clevertools` helpers support an `on_error` argument. This gives the package a consistent error model across file operations, config loading, and masking.

If `on_error` is omitted, the helper uses the global default stored with `configure(error_mode=...)`.

## The three modes

### `raise`

The original exception is raised immediately.

Use this when:

- you are in application startup
- failures must stop execution
- you want Python tracebacks during development

### `log`

The exception is logged through the package logger and the helper returns its fallback value.

Use this when:

- you want visibility into failures
- a best-effort result is acceptable
- you are running scripts, workers, or background tasks

### `silent`

The exception is suppressed and the helper returns its fallback value without logging.

Use this when:

- the operation is optional
- missing data is expected
- you want complete control over your own fallback handling

## Typical fallback values

Different helpers return different fallback values:

- `read()`, `read_json()`, `read_toml()`, `read_yaml()`, and `load_config()` related reads commonly return `None` on failure
- `mask()` returns an empty string on validation failure when not raising
- write helpers return `None` and simply stop

That means your code should treat the return value as optional whenever you are not in `"raise"` mode.

## Set the global default once

```python
from clevertools import configure, read_json

configure(error_mode="silent")

payload = read_json("optional.json")
print(payload)  # None if the file is missing or invalid
```

## Override the mode per call

```python
from clevertools import configure, read_json

configure(error_mode="silent")

payload = read_json("required.json", on_error="raise")
```

## Example: soft failure for optional files

```python
from clevertools import read_yaml

theme = read_yaml("config/theme.yaml", on_error="silent") or {}
print(theme.get("name", "default"))
```

## Example: strict startup validation

```python
from clevertools import load_config

config = load_config("config/base.toml", "config/prod.yaml", on_error="raise")
```

## Helpers that use this model

- `mask()`
- `read()` and `write()`
- `read_json()` and `write_json()`
- `read_toml()` and `write_toml()`
- `read_yaml()` and `write_yaml()`
- `load_config()`

## Good rule of thumb

- choose `"raise"` for required inputs
- choose `"log"` for recoverable problems you still want to see
- choose `"silent"` for optional inputs where absence is normal