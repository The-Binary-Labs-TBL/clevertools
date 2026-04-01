# `read_yaml`

`read_yaml()` reads a YAML file and deserializes it with `yaml.safe_load()`.

## Signature

```python
read_yaml(
    file_path: str | Path,
    on_error: Literal["raise", "log", "silent"] | None = None,
) -> Any | None
```

## Example: load a service config

```python
from clevertools import read_yaml

config = read_yaml("config.yaml", on_error="raise")
print(config["service"])
```

## Example: optional content file

```python
from clevertools import read_yaml

content = read_yaml("content/pages.yaml", on_error="silent") or []
print(len(content))
```

## Notes

- Invalid YAML returns `None` unless the selected error mode raises.
- Missing files and directory paths follow the shared error policy.
- The YAML root can be any valid YAML type, not only a mapping.