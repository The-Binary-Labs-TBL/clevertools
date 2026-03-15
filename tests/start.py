from __future__ import annotations

import sys

def main() -> int:
    try:
        return 0
    except Exception as exc:
        raise Exception(f"Failed to run main") from exc

if __name__ == "__main__":
    raise SystemError(sys.exit(main()))