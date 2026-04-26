#!/usr/bin/env python3
"""
extract-strings.py — flatten i18n JSON to key:value list for batch language audit.

Usage:
    python extract-strings.py en.json > audit-input.txt
    python extract-strings.py en.json | grep -v "^#" | wc -l  # count strings

Output format: dotted.key.path: string value
"""

import json
import sys


def flatten(obj: dict, prefix: str = "") -> list[str]:
    """Recursively flatten nested JSON to dotted-key: value lines."""
    rows = []
    for k, v in obj.items():
        key = f"{prefix}.{k}" if prefix else k
        if isinstance(v, str):
            rows.append(f"{key}: {v}")
        elif isinstance(v, dict):
            rows.extend(flatten(v, key))
        elif isinstance(v, list):
            for i, item in enumerate(v):
                if isinstance(item, str):
                    rows.append(f"{key}[{i}]: {item}")
    return rows


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python extract-strings.py <i18n-file.json>", file=sys.stderr)
        sys.exit(1)

    filepath = sys.argv[1]
    with open(filepath, encoding="utf-8") as f:
        data = json.load(f)

    print(f"# Strings extracted from: {filepath}")
    print(f"# Total keys: {len(flatten(data))}")
    print("#")
    print("# Audit each string against Nielsen Heuristic #2:")
    print("# - Classify: OK | JARGON | TECHNICAL | ABBREVIATION | UNCLEAR")
    print("# - Provide plain-language alternative for non-OK items")
    print()

    for line in flatten(data):
        print(line)


if __name__ == "__main__":
    main()
