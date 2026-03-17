# Error Handling

Many helpers in `clevertools` support an `on_error` argument. If you do not pass it, the global default from `configure()` is used.

## Error modes

- `"raise"` re-raises the original exception.
- `"log"` logs the error and returns a fallback value when the helper supports one.
- `"silent"` suppresses the error and returns a fallback value when the helper supports one.

## Helpers that use it

- `mask()`
- `read()` and `write()`
- `read_json()` and `write_json()`
- `read_toml()` and `write_toml()`

## Global default

```python
from clevertools import configure, read

configure(error_mode="silent")

content = read("missing.txt")
print(content)  # None
```

## Per-call override

```python
from clevertools import configure, read_json

configure(error_mode="silent")

payload = read_json("config.json", on_error="raise")
```
