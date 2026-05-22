#!/usr/bin/env python3
"""validate-documentation.py — Validate the documentation output record against 02-output-contract.xml.

Inputs:
  - <record.json>  Path to the output record JSON file.

Outputs:
  - stdout: PASS / FAIL with violation list.

Exit codes:
  0 - record validates.
  1 - record violates the contract.
  2 - usage error.

Flags:
  --help        Show this message.
  --self-test   Run against a built-in fixture.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

# Minimal schema enforcement: every output record must carry a non-empty
# slug-tagged "produced_by" and a non-empty "evidence" list anchoring the work.
VALID = {
    "produced_by": "documentation",
    "version": "1.1.0",
    "evidence": ["https://example.com/evidence"],
}
INVALID = {"produced_by": "other", "version": "x", "evidence": []}


def validate(rec: dict) -> list[str]:
    out: list[str] = []
    if rec.get("produced_by") != "documentation":
        out.append("produced_by must equal 'documentation'")
    if not isinstance(rec.get("version"), str) or not rec["version"].count(".") == 2:
        out.append("version must be semver (X.Y.Z)")
    if not isinstance(rec.get("evidence"), list) or not rec["evidence"]:
        out.append("evidence must be a non-empty list of URLs / paths / refs")
    return out


def main(argv: list[str]) -> int:
    if len(argv) < 2 or argv[1] in ("--help", "-h"):
        sys.stdout.write(__doc__ or "")
        return 0 if "--help" in argv else 2
    if argv[1] == "--self-test":
        ok = validate(VALID)
        bad = validate(INVALID)
        if ok:
            sys.stderr.write(f"self-test FAIL: valid rejected: {ok}\n")
            return 1
        if not bad:
            sys.stderr.write("self-test FAIL: invalid accepted\n")
            return 1
        sys.stdout.write("self-test OK\n")
        return 0
    p = Path(argv[1])
    if not p.is_file():
        sys.stderr.write(f"not a file: {p}\n")
        return 2
    try:
        rec = json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        sys.stderr.write(f"invalid JSON: {exc}\n")
        return 1
    v = validate(rec)
    if v:
        sys.stdout.write("FAIL\n")
        for x in v:
            sys.stdout.write(f"  - {x}\n")
        return 1
    sys.stdout.write("PASS\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
