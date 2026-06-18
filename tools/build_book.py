#!/usr/bin/env python3
import yaml, pathlib, subprocess

BOOK = pathlib.Path("book")
BUILD = pathlib.Path("build")
MANIFEST = BOOK / "manifest.yml"

def main():
    BUILD.mkdir(exist_ok=True)

    manifest = yaml.safe_load(MANIFEST.read_text())
    chapters = [pathlib.Path(entry) for entry in manifest["chapters"]]

    out = []

    for p in chapters:
        text = p.read_text()
        out.append(f"\n\n<!-- BEGIN {p.name} -->\n\n")
        out.append(text)
        out.append(f"\n\n<!-- END {p.name} -->\n\n")

    combined = "\n".join(out)
    (BUILD / "book.md").write_text(combined)

    # Optional: build EPUB/PDF via Pandoc
    try:
        subprocess.run(
            ["pandoc", "book.md", "-o", "book.epub"],
            cwd=BUILD,
            check=True
        )
        subprocess.run(
            ["pandoc", "book.md", "-o", "book.pdf"],
            cwd=BUILD,
            check=True
        )
    except Exception:
        print("Skipping EPUB/PDF build (Pandoc not available).")

    print("Build complete.")

if __name__ == "__main__":
    main()
