# `read_json`

`read_json()` reads a JSON file and deserializes it with Python's `json` module.

## Signature

```python
read_json(
    file_path: str | Path,
    on_error: Literal["raise", "log", "silent"] | None = None,
) -> Any | None
```

## Example

```python
from clevertools import read_json

config = read_json("config.json")
print(config["service"])
```

## Notes

- Invalid JSON returns `None` unless the active error mode raises.
- Missing files and directory paths are handled through the shared error policy.