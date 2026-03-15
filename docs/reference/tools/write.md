# `write`

`write()` stores UTF-8 text in a file.

## Signature

```python
write(file_path, data, on_error=None)
```

## Behavior

- accepts `str` and `Path`
- writes the provided text exactly as given
- uses the shared error handling configuration when `on_error` is omitted

## Example

```python
from clevertools import write

write("notes.txt", "Hello from clevertools")
```