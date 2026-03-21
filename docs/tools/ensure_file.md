# `ensure_file`

`ensure_file()` makes sure that one file or several files exist and are valid regular-file targets.

## Signature

```python
ensure_file(
    paths: str | Path | list[str | Path],
    default_content: str | bytes = "No default content was provided for the new file.",
    replace: bool = False,
    on_error: Literal["raise", "log", "silent"] | None = "log",
) -> None
```

## What It Does

Use this helper when you want a path to be ready for later file operations without repeating the same existence checks in every caller.

The helper accepts either a single path or a list of paths. It normalizes all values to `Path` objects, creates missing parent directories, and then ensures that each target is a real file path.

## Behavior

- A missing parent directory is created automatically.
- A missing file is created as an empty file when `replace=False`.
- An existing file is left unchanged when `replace=False`.
- The helper writes `default_content` to the target when `replace=True`.
- Both text (`str`) and binary (`bytes`) replacement content are supported.
- If a target already exists as a directory, the helper follows the shared error policy.
- Invalid path inputs also follow the shared error policy.

## Example: ensure one file exists

```python
from clevertools import ensure_file

ensure_file("logs/app.log", on_error="raise")
```

## Example: ensure multiple files exist

```python
from clevertools import ensure_file

ensure_file(
    ["tmp/a.txt", "tmp/nested/b.txt"],
    on_error="raise",
)
```

## Example: create parents automatically

```python
from clevertools import ensure_file

ensure_file("runtime/cache/session/token.txt", on_error="raise")
```

## Example: replace file content

```python
from clevertools import ensure_file

ensure_file(
    "config/example.env",
    default_content="DEBUG=false\n",
    replace=True,
    on_error="raise",
)
```

## Example: write binary content

```python
from clevertools import ensure_file

ensure_file(
    "runtime/blob.bin",
    default_content=b"\x00\x01hello\xff",
    replace=True,
    on_error="raise",
)
```

## Notes

- Existing files are left unchanged unless `replace=True`.
- The helper is intended for file preparation, not full schema validation.
- If you need to write structured content, pair it with `write()`, `write_json()`, `write_toml()`, or `write_yaml()`.
- Non-`str` and non-`Path` entries inside a path list are rejected.