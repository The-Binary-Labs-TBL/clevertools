# `read_yaml`

`read_yaml()` reads a YAML file and deserializes it with `yaml.safe_load()`.

## Signature

```python
read_yaml(
    file_path: str | Path,
    on_error: Literal["raise", "log", "silent"] | None = None,
) -> Any | None
```

## Example

```python
from clevertools import read_yaml

config = read_yaml("config.yaml")
print(config["service"])
```

## Notes

- Invalid YAML returns `None` unless the active error mode raises.
- Missing files and directory paths are handled through the shared error policy.