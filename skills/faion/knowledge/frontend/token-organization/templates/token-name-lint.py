#!/usr/bin/env python3
# token-name-lint.py — flag bad token names and duplicate values
# Input (stdin): JSON {"tokens":[{"name":"..","value":..},...]}
# Output: list of issues; exits 1 if any found, 0 if clean
import json
import re
import sys

# {category}.{property}[.{variant}[.{state}]] — 2-4 segments, lowercase kebab
PATTERN = re.compile(r"^[a-z]+(\.[a-z][a-z0-9-]*){1,3}$")


def main() -> int:
    data = json.load(sys.stdin)
    tokens = data.get("tokens", [])
    seen_values: dict[str, str] = {}
    issues: list[str] = []

    for t in tokens:
        name = t.get("name", "")
        val = json.dumps(t.get("value"))

        if not PATTERN.match(name):
            issues.append(f"bad-name: {name!r} — must match {{category}}.{{property}}[.{{variant}}[.{{state}}]]")

        segments = name.split(".")
        if len(segments) > 4:
            issues.append(f"depth-exceeded: {name!r} has {len(segments)} segments (max 4)")

        if val in seen_values and seen_values[val] != name:
            issues.append(f"duplicate-value: {name!r} == {seen_values[val]!r} (same value)")
        else:
            seen_values[val] = name

    if issues:
        for issue in issues:
            print(issue)
        return 1
    print(f"OK: {len(tokens)} tokens pass naming lint")
    return 0


if __name__ == "__main__":
    sys.exit(main())
