from __future__ import annotations

from clevertools.configuration import configure, get_config
from clevertools.errors.policy import handle_error
import pytest

from ._debug import debug

def test_configure_updates_error_mode_and_returns_copy() -> None:
    debug("Lese Ausgangskonfiguration und aktualisiere den error_mode auf 'silent'.")
    original = get_config()
    updated = configure(error_mode="silent")
    snapshot = get_config()

    debug(f"Original: {original.error_mode}, updated: {updated.error_mode}, snapshot: {snapshot.error_mode}")

    assert updated.error_mode == "silent"
    assert snapshot.error_mode == "silent"
    assert updated is not snapshot

    assert original.error_mode in {"raise", "log", "silent"}


def test_configure_rejects_unsupported_error_mode() -> None:
    debug("Pruefe ValueError fuer einen ungueltigen error_mode.")

    with pytest.raises(ValueError, match="Unsupported error_mode"):
        configure(error_mode="kaputt")  # type: ignore[arg-type]


def test_handle_error_returns_fallback_in_silent_mode() -> None:
    debug("Fuehre handle_error im silent-Modus aus und pruefe den Fallback.")
    result = handle_error(RuntimeError("debug fallback"), on_error="silent", fallback="SAFE")
    debug(f"Fallback-Ergebnis: {result}")

    assert result == "SAFE"