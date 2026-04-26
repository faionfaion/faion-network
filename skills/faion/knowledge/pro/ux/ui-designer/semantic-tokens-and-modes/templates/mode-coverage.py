#!/usr/bin/env python3
# mode-coverage.py — fail if any alias is missing a value in any declared mode
# Input: path to token JSON with collections.{name}.{modes:[...], aliases:{name:{values:{mode:val}}}}
# Output: list of missing (collection, alias, mode) triples; exits 1 if any found
import json
import sys


def check(path: str) -> int:
    with open(path) as f:
        data = json.load(f)

    missing: list[tuple[str, str, str]] = []

    for col_name, col in data.get("collections", {}).items():
        modes = col.get("modes", [])
        for alias_name, alias in col.get("aliases", {}).items():
            values = alias.get("values", {})
            for mode in modes:
                if mode not in values or values[mode] in (None, ""):
                    missing.append((col_name, alias_name, mode))

    for col, alias, mode in missing:
        print(f"missing: {col} / {alias} / {mode}")

    if missing:
        print(f"\nFAIL: {len(missing)} missing (alias, mode) pair(s)")
        return 1

    print(f"OK: all aliases have values in all declared modes")
    return 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: mode-coverage.py <tokens.json>")
        sys.exit(2)
    sys.exit(check(sys.argv[1]))
