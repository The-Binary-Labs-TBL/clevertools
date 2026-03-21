# `load_config`

`load_config()` reads multiple config files, merges them in order, and returns one configuration object with both attribute access and helper methods.

## Signature

```python
load_config(*file_paths: str | Path, on_error: ErrorMode | None = None)
```

## Supported file types

- `.toml`
- `.json`
- `.yaml`
- `.yml`

## Merge behavior

- files are processed in the order you pass them
- later files override earlier values
- nested mappings are merged recursively
- non-mapping root values are rejected because they cannot be merged safely

## How to access values

You can use:

- attribute access such as `config.database.host`
- key access such as `config["database"]["host"]`
- dot-path lookup such as `config.get("database.host")`
- plain dictionary export with `config.as_dict()`

## Example: merge environment layers

```python
from clevertools import load_config

config = load_config(
    "config/defaults.toml",
    "config/team.json",
    "config/local.yaml",
    on_error="raise",
)

print(config.database.host)
print(config.get("features.search.enabled", False))
```

## Example: convert merged config back to a plain dict

```python
from clevertools import load_config

config = load_config("config/base.toml", "config/override.yaml")
plain = config.as_dict()

print(type(plain))
print(plain["paths"]["cache"])
```

## Notes

- Missing files and parse errors follow the shared error policy of the underlying reader.
- If the same key is a mapping in one file and a scalar in a later file, the later value replaces the earlier structure.
- This helper is ideal for layered application config such as defaults, environment, and local overrides.