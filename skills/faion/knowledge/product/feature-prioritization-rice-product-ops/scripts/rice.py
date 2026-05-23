#!/usr/bin/env python3
"""
rice.py — compute RICE scores from JSON input and return ranked output.

Usage:
  echo '[{"id":"A","reach":5000,"impact":2,"confidence":0.8,"effort":0.5}]' | python rice.py
  python rice.py < features.json

Input JSON: array of objects with fields:
  id (str), reach (int, users/quarter), impact (float: 3|2|1|0.5|0.25),
  confidence (float: 0.5|0.8|1.0), effort (float, person-months > 0)

Output JSON: same array with score and rank fields added, sorted descending by score.

Validation rules:
  - effort must be > 0
  - confidence must be one of 0.5, 0.8, 1.0 (no inflation)
  - impact must be one of 3, 2, 1, 0.5, 0.25 (fixed scale)
  - reach_source field required (empty string triggers warning)
"""
import json
import sys

VALID_IMPACT = {3, 2, 1, 0.5, 0.25}
VALID_CONFIDENCE = {0.5, 0.8, 1.0}


def rice(reach: int, impact: float, confidence: float, effort: float) -> float:
    if effort <= 0:
        raise ValueError("effort must be > 0")
    return round((reach * impact * confidence) / effort, 1)


def validate(row: dict) -> list[str]:
    errors = []
    if row.get("effort", 0) <= 0:
        errors.append(f"[{row.get('id')}] effort must be > 0")
    if row.get("impact") not in VALID_IMPACT:
        errors.append(f"[{row.get('id')}] impact must be one of {sorted(VALID_IMPACT)}, got {row.get('impact')}")
    if row.get("confidence") not in VALID_CONFIDENCE:
        errors.append(f"[{row.get('id')}] confidence must be one of {sorted(VALID_CONFIDENCE)}, got {row.get('confidence')}")
    if not row.get("reach_source"):
        errors.append(f"[{row.get('id')}] WARNING: no reach_source — confidence should be capped at 0.5")
    return errors


def main():
    try:
        rows = json.load(sys.stdin)
    except json.JSONDecodeError as e:
        sys.exit(f"JSON parse error: {e}")

    all_errors = []
    for row in rows:
        all_errors.extend(validate(row))

    if any(not e.startswith("[") or "WARNING" not in e for e in all_errors
           if not e.startswith("[") or "WARNING" not in e):
        hard_errors = [e for e in all_errors if "WARNING" not in e]
        if hard_errors:
            print("Validation errors:", file=sys.stderr)
            for e in hard_errors:
                print(f"  {e}", file=sys.stderr)
            sys.exit(1)

    for warn in [e for e in all_errors if "WARNING" in e]:
        print(warn, file=sys.stderr)

    for row in rows:
        row["score"] = rice(row["reach"], row["impact"], row["confidence"], row["effort"])

    rows.sort(key=lambda x: x["score"], reverse=True)
    for n, row in enumerate(rows, 1):
        row["rank"] = n

    json.dump(rows, sys.stdout, indent=2)
    print()


if __name__ == "__main__":
    main()
