from __future__ import annotations

import os


def debug(message: str) -> None:
    if os.getenv("CLEVERTOOLS_TEST_DEBUG", "").lower() in {"1", "true", "yes", "on"}:
        print(f"[TEST DEBUG] {message}")