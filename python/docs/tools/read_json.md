# `read_json`

`read_json()` reads a JSON file and deserializes it with Python's built-in `json` module.

## Signature

```python
read_json(
    file_path: str | Path,
    on_error: Literal["raise", "log", "silent"] | None = None,
) -> Any | None
```

## Example: load a config file

```python
from clevertools import read_json

config = read_json("config.json", on_error="raise")
print(config["service"])
```

## Example: optional JSON file

```python
from clevertools import read_json

payload = read_json("optional.json", on_error="silent") or {}
print(payload.get("enabled", False))
```

## Notes

- Invalid JSON returns `None` unless the selected error mode raises.
- Missing files and directory paths follow the shared error policy.
- The JSON root can be any valid JSON type, not only an object.