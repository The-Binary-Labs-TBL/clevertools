from __future__ import annotations

from pathlib import Path

import pytest

from clevertools import ensure_dir, ensure_file
from clevertools.errors.exceptions import ValidationError


def test_ensure_file_creates_missing_file_and_parent_dirs(cache_dir: Path) -> None:
    path = cache_dir / "nested" / "notes.txt"

    ensure_file(path, on_error="raise")

    assert path.exists()
    assert path.is_file()


def test_ensure_file_supports_lists_of_paths(cache_dir: Path) -> None:
    first = cache_dir / "a.txt"
    second = cache_dir / "deep" / "b.txt"

    ensure_file([first, str(second)], on_error="raise")

    assert first.exists()
    assert first.is_file()
    assert second.exists()
    assert second.is_file()


def test_ensure_file_replaces_content_when_requested(cache_dir: Path) -> None:
    path = cache_dir / "replace.txt"
    path.write_text("old", encoding="utf-8")

    ensure_file(path, default_content="new", replace=True, on_error="raise")

    assert path.read_text(encoding="utf-8") == "new"


def test_ensure_file_preserves_existing_content_by_default(cache_dir: Path) -> None:
    path = cache_dir / "keep.txt"
    path.write_text("keep-me", encoding="utf-8")

    ensure_file(path, default_content="replace-me", on_error="raise")

    assert path.read_text(encoding="utf-8") == "keep-me"


def test_ensure_file_supports_binary_default_content(cache_dir: Path) -> None:
    path = cache_dir / "blob.bin"

    ensure_file(path, default_content=b"\x00\x01test", replace=True, on_error="raise")

    assert path.read_bytes() == b"\x00\x01test"


def test_ensure_file_raises_for_directory_target(cache_dir: Path) -> None:
    directory = cache_dir / "as-dir"
    directory.mkdir()

    with pytest.raises(ValidationError, match="Expected a file path, but got a directory"):
        ensure_file(directory, on_error="raise")


def test_ensure_dir_creates_missing_directories(cache_dir: Path) -> None:
    path = cache_dir / "nested" / "logs"

    ensure_dir(path, on_error="raise")

    assert path.exists()
    assert path.is_dir()


def test_ensure_dir_supports_lists_of_paths(cache_dir: Path) -> None:
    first = cache_dir / "tmp"
    second = cache_dir / "var" / "cache"

    ensure_dir([first, str(second)], on_error="raise")

    assert first.exists()
    assert first.is_dir()
    assert second.exists()
    assert second.is_dir()


def test_ensure_dir_raises_for_file_target(cache_dir: Path) -> None:
    path = cache_dir / "not-a-dir.txt"
    path.write_text("hello", encoding="utf-8")

    with pytest.raises(ValidationError, match="Expected a directory path, but got a file"):
        ensure_dir(path, on_error="raise")


def test_ensure_helpers_reject_invalid_list_entries(cache_dir: Path) -> None:
    with pytest.raises(ValidationError, match="All entries in 'paths' must be of type 'str' or 'Path'."):
        ensure_file([cache_dir / "ok.txt", 123], on_error="raise")  # type: ignore[list-item]

    with pytest.raises(ValidationError, match="All entries in 'paths' must be of type 'str' or 'Path'."):
        ensure_dir([cache_dir / "ok", 123], on_error="raise")  # type: ignore[list-item]


def test_ensure_helpers_reject_invalid_top_level_input() -> None:
    with pytest.raises(ValidationError, match="'paths' must be a 'str', 'Path', or a list of those values."):
        ensure_file(123, on_error="raise")  # type: ignore[arg-type]

    with pytest.raises(ValidationError, match="'paths' must be a 'str', 'Path', or a list of those values."):
        ensure_dir(123, on_error="raise")  # type: ignore[arg-type]