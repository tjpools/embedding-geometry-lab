#!/usr/bin/env python3
from __future__ import annotations

import pathlib
import sys
from typing import Any

import yaml


REPO_ROOT = pathlib.Path(".").resolve()
BOOK_DIR = REPO_ROOT / "book"
MANIFEST_PATH = BOOK_DIR / "manifest.yml"
SPINE_ROOT_FILES = {
    "copyright.md",
    "dedication.md",
    "epigraph.md",
    "HOW_TO_READ_THIS_BOOK.md",
    "promise_to_the_reader.md",
    "preface.md",
    "epilogue_one_question_one_table.md",
    "afterword_how_the_manifold_became_visible.md",
    "Postscript.md",
}


def fail(message: str) -> None:
    print(f"VALIDATION ERROR: {message}")
    sys.exit(1)


def load_manifest() -> dict[str, Any]:
    if not MANIFEST_PATH.exists():
        fail("book/manifest.yml not found")

    try:
        data = yaml.safe_load(MANIFEST_PATH.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"unable to parse manifest.yml: {exc}")

    if not isinstance(data, dict):
        fail("manifest.yml must be a mapping with keys: version, chapters")

    if "version" not in data:
        fail("manifest.yml missing required key: version")
    if "chapters" not in data:
        fail("manifest.yml missing required key: chapters")

    if not isinstance(data["chapters"], list):
        fail("manifest.yml: chapters must be a list")

    return data


def normalize_manifest_path(raw_entry: Any) -> pathlib.Path:
    if not isinstance(raw_entry, str) or not raw_entry.strip():
        fail(f"chapter entry must be a non-empty string, got: {raw_entry!r}")

    raw = pathlib.Path(raw_entry)

    # Disallow absolute paths
    if raw.is_absolute():
        fail(f"chapter entry must be repository-relative, got absolute path: {raw_entry}")

    # Require explicit book/ prefix to preserve coordinate discipline
    if raw.parts[0] != "book":
        fail(f"chapter entry must start with 'book/': {raw_entry}")

    # Normalize and ensure still under book/
    normalized = pathlib.Path(*raw.parts)
    if normalized.parts[0] != "book":
        fail(f"invalid chapter path after normalization: {raw_entry}")

    # Protect against traversal (book/../...)
    candidate = (REPO_ROOT / normalized).resolve()
    try:
        candidate.relative_to(BOOK_DIR.resolve())
    except ValueError:
        fail(f"chapter entry escapes book/ directory: {raw_entry}")

    return normalized


def main() -> None:
    manifest = load_manifest()
    chapters_raw = manifest["chapters"]

    normalized_entries: list[pathlib.Path] = [normalize_manifest_path(e) for e in chapters_raw]

    # Uniqueness check
    duplicates = sorted({str(p) for p in normalized_entries if normalized_entries.count(p) > 1})
    if duplicates:
        fail(f"duplicate chapter entries in manifest: {duplicates}")

    # Validate each manifest entry
    for rel_path in normalized_entries:
        abs_path = REPO_ROOT / rel_path
        if not abs_path.exists():
            fail(f"manifest entry missing: {rel_path}")
        if not abs_path.is_file():
            fail(f"manifest entry is not a file: {rel_path}")
        if abs_path.suffix.lower() != ".md":
            fail(f"manifest entry is not Markdown (.md): {rel_path}")
        if abs_path.name.lower() == "manifest.yml":
            fail("manifest.yml cannot appear in chapters list")

    # Orphan detection applies only to the publication spine, not support docs.
    book_md_files = sorted(
        p.relative_to(REPO_ROOT)
        for p in BOOK_DIR.glob("*.md")
        if p.name.startswith("chapter_") or p.name in SPINE_ROOT_FILES
    )
    manifest_set = set(normalized_entries)
    book_set = set(book_md_files)

    orphans = sorted(str(p) for p in (book_set - manifest_set))
    if orphans:
        fail(f"orphan Markdown files not in manifest: {orphans}")

    extras = sorted(str(p) for p in (manifest_set - book_set))
    if extras:
        fail(f"manifest references Markdown files not in book root set: {extras}")

    print("Validation OK")


if __name__ == "__main__":
    main()
