# `read`

`read()` loads a file as UTF-8 text.

## Signature

```python
read(file_path, on_error=None)
```

## Behavior

- accepts `str` and `Path`
- returns file content as `str`
- returns `None` when reading fails and the chosen error mode does not raise

## Example

```python
from clevertools import read

content = read("notes.txt")
```