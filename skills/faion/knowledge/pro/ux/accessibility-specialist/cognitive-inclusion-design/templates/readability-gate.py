#!/usr/bin/env python3
"""
readability-gate.py
Fails CI if any UI string in locales/**/*.json has Flesch reading ease < THRESHOLD.
Requires: pip install textstat
Usage: python readability-gate.py [threshold=60] [locales-dir=locales]
"""
import json
import sys
import pathlib

try:
    import textstat
except ImportError:
    print("Install textstat: pip install textstat", file=sys.stderr)
    sys.exit(2)

THRESHOLD = float(sys.argv[1]) if len(sys.argv) > 1 else 60.0
LOCALES_DIR = sys.argv[2] if len(sys.argv) > 2 else "locales"
MIN_WORDS = 6  # Skip very short strings (labels, single words)

errors = []

def walk(data: dict | str | list, path_key: str = "") -> None:
    if isinstance(data, dict):
        for key, val in data.items():
            walk(val, f"{path_key}.{key}" if path_key else key)
    elif isinstance(data, list):
        for i, val in enumerate(data):
            walk(val, f"{path_key}[{i}]")
    elif isinstance(data, str) and len(data.split()) >= MIN_WORDS:
        score = textstat.flesch_reading_ease(data)
        if score < THRESHOLD:
            errors.append({
                "key": path_key,
                "score": round(score, 1),
                "text": data[:80],
            })

for json_file in pathlib.Path(LOCALES_DIR).rglob("en.json"):
    try:
        data = json.loads(json_file.read_text(encoding="utf-8"))
        walk(data)
        if errors:
            print(f"File: {json_file}")
    except (json.JSONDecodeError, OSError) as e:
        print(f"Warning: could not read {json_file}: {e}", file=sys.stderr)

for err in errors:
    print(f"  [{err['score']} < {THRESHOLD}] {err['key']}: {err['text']!r}")

if errors:
    print(f"\nFAIL: {len(errors)} string(s) below Flesch {THRESHOLD}.")
    sys.exit(1)
else:
    print(f"OK: All strings pass Flesch >= {THRESHOLD}.")
