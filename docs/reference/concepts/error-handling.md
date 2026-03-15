# Error Handling

Several helpers in `clevertools` support a shared error handling strategy.

## Modes

- `"raise"` re-raises the original exception
- `"log"` logs the error and returns a fallback value when supported
- `"silent"` suppresses the error and returns a fallback value when supported

## Where It Is Used

- `read()`
- `write()`
- global defaults configured through `configure()`

## Example

```python
from clevertools import configure, read

configure(error_mode="silent")
content = read("missing.txt")
```