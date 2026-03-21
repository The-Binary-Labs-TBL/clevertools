# `ensure_dir`

`ensure_dir()` makes sure that one directory or several directories exist and are valid directory targets.

## Signature

```python
ensure_dir(
    paths: str | Path | list[str | Path],
    on_error: Literal["raise", "log", "silent"] | None = "log",
) -> None
```

## What It Does

Use this helper when you want to prepare directory paths up front before writing files, logs, caches, exports, or temporary data.

The helper accepts either a single path or a list of paths. It normalizes all values to `Path` objects, creates missing directories recursively, and verifies that existing targets are actual directories.

## Behavior

- A missing directory is created recursively with `parents=True`.
- Existing directories are left unchanged.
- If a target already exists as a file, the helper follows the shared error policy.
- Invalid path inputs also follow the shared error policy.

## Example: ensure one directory exists

```python
from clevertools import ensure_dir

ensure_dir("var/cache", on_error="raise")
```

## Example: ensure multiple directories exist

```python
from clevertools import ensure_dir

ensure_dir(
    ["tmp/cache", "logs/archive/2026"],
    on_error="raise",
)
```

## Example: prepare directories before later writes

```python
from clevertools import ensure_dir, write

ensure_dir("runtime/reports/2026", on_error="raise")
write("runtime/reports/2026/summary.txt", "ready", on_error="raise")
```

## Notes

- Existing directories are left unchanged.
- The helper does not delete or replace files that block a directory path.
- Non-`str` and non-`Path` entries inside a path list are rejected.