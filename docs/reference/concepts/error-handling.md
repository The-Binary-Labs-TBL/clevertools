# Error Handling

Several helpers in `clevertools` use the same error handling model.

## Modes

- `"raise"` re-raises the original exception
- `"log"` logs the error and returns a fallback value when supported
- `"silent"` suppresses the error and returns a fallback value when supported

## Used By

- `read()`
- `write()`
- global defaults configured through `configure()`

## Example

```python
from clevertools import configure, read

configure(error_mode="silent")
content = read("missing.txt")
```