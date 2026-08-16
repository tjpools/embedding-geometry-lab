#!/usr/bin/env python3

import argparse
from pathlib import Path

from engine.report import run


BOOK_DIR = Path(__file__).resolve().parents[1]
DEFAULT_REGISTRY = Path(__file__).with_name("runtime") / "registry.json"
DEFAULT_OUTPUT = Path(__file__).with_name("output")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate Book Two manuscript analytics.")
    parser.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    result = run(BOOK_DIR, args.registry, args.output)
    print(f"Mode: {result['mode']}")
    print(f"Analyzed {result['sources']} units and {result['words']:,} words.")
    print(f"Broken local links: {result['broken_links']}")
    print(f"Artifacts: {result['output']}")


if __name__ == "__main__":
    main()
