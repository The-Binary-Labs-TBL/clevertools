# `read_toml`

`read_toml()` reads a TOML file and returns its content as a dictionary.

## Signature

```python
read_toml(
    file_path: str | Path,
    on_error: Literal["raise", "log", "silent"] | None = None,
) -> dict[str, Any] | None
```

## Example

```python
from clevertools import read_toml

settings = read_toml("pyproject.toml")
print(settings["project"]["name"])
```

## Notes

- The TOML root must be a table-like mapping.
- Missing files, parse errors, and directory paths follow the shared error policy.