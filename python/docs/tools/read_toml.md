# `read_toml`

`read_toml()` reads a TOML file and returns the parsed document as a dictionary.

## Signature

```python
read_toml(
    file_path: str | Path,
    on_error: Literal["raise", "log", "silent"] | None = None,
) -> dict[str, Any] | None
```

## Example: inspect a project file

```python
from clevertools import read_toml

settings = read_toml("pyproject.toml", on_error="raise")
print(settings["project"]["name"])
```

## Example: optional environment config

```python
from clevertools import read_toml

env = read_toml("config/local.toml", on_error="silent") or {}
print(env.get("debug", False))
```

## Notes

- The TOML root must be a mapping.
- Missing files, parse errors, and directory paths follow the shared error policy.
- TOML is read using Python's standard `tomllib`.