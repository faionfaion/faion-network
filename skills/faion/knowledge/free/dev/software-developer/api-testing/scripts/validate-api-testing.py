#!/usr/bin/env python3
"""validate-api-testing.py — Validate the api-testing report.

Inputs:
  - <report.json>  Path to the test-suite report JSON.

Outputs:
  - stdout: PASS / FAIL with violation list.

Exit codes:
  0 - report validates.
  1 - report violates schema/pyramid/oasdiff/fuzzing rules.
  2 - usage error.

Flags:
  --help        Show this message.
  --self-test   Run against a built-in fixture.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

VALID = {
    "counts": {"unit": 220, "integration": 70, "contract": 8, "e2e": 4},
    "schema_coverage_pct": 96.4,
    "oasdiff": {"breaking": [], "non_breaking": []},
    "fuzzing": {"ran": True, "passed": True},
}
INVALID = {
    "counts": {"unit": 10, "integration": 80, "contract": 50, "e2e": 200},
    "schema_coverage_pct": 12,
    "oasdiff": {"breaking": ["x"], "non_breaking": []},
    "fuzzing": {"ran": False, "passed": False},
}


def validate(rep: dict, breaking_approved: bool = False) -> list[str]:
    out: list[str] = []
    for k in ("counts", "schema_coverage_pct", "oasdiff", "fuzzing"):
        if k not in rep:
            out.append(f"missing {k}")
    if out:
        return out
    c = rep["counts"]
    for k in ("unit", "integration", "contract", "e2e"):
        if k not in c or not isinstance(c[k], int) or c[k] < 0:
            out.append(f"counts.{k} must be non-negative int")
    if out:
        return out
    total = sum(c[k] for k in ("unit", "integration", "contract", "e2e"))
    if total > 0 and c["unit"] / total < 0.7:
        out.append(f"pyramid violation: unit fraction {c['unit']/total:.2f} < 0.70")
    if c["e2e"] > total * 0.05 + 1:
        out.append(f"pyramid violation: e2e count {c['e2e']} > 5% of total")
    if not isinstance(rep["schema_coverage_pct"], (int, float)) or rep["schema_coverage_pct"] < 90:
        out.append("schema_coverage_pct must be >= 90")
    oas = rep["oasdiff"]
    if not isinstance(oas.get("breaking"), list) or not isinstance(oas.get("non_breaking"), list):
        out.append("oasdiff.breaking/non_breaking must be lists")
    elif oas["breaking"] and not breaking_approved:
        out.append(f"oasdiff has {len(oas['breaking'])} breaking change(s) without breaking-change-approved")
    fz = rep["fuzzing"]
    if not fz.get("ran"):
        out.append("fuzzing.ran must be true")
    if not fz.get("passed"):
        out.append("fuzzing.passed must be true")
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
        rep = json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        sys.stderr.write(f"invalid JSON: {exc}\n")
        return 1
    v = validate(rep)
    if v:
        sys.stdout.write("FAIL\n")
        for x in v:
            sys.stdout.write(f"  - {x}\n")
        return 1
    sys.stdout.write("PASS\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
