#!/usr/bin/env python3
"""validate-semantic-field-naming.py — validate the rename-rubric output.

Inputs:
  - <report.json>  Path to a JSON file matching the 02-output-contract schema.

Outputs:
  - stdout: PASS / FAIL with violation list.

Exit codes:
  0 - report validates.
  1 - report violates schema or self-check rules.
  2 - usage error.

Flags:
  --help        Show this message.
  --self-test   Run against built-in fixtures (valid + invalid).
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

SNAKE_RE = re.compile(r"^[a-z][a-z0-9_]*$")
PATH_RE = re.compile(r"^[A-Za-z][A-Za-z0-9_.]*$")
SEMVER_RE = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+$")
REASONS = {
    "generic-placeholder",
    "missing-unit",
    "missing-direction",
    "redundant-suffix",
    "non-english",
    "cardinality-mismatch",
    "cryptic-enum",
}

VALID_FIXTURE = {
    "model_path": "myapp/schemas/order.py",
    "schema_version": "1.1.0",
    "renames": [
        {
            "field_path": "Order.flag",
            "old_name": "flag",
            "new_name": "is_paid",
            "reason_code": "missing-direction",
            "rationale": "Boolean lacks is_/has_ prefix.",
        }
    ],
    "kept": ["Order.customer_id"],
    "ab_eval": {
        "rows": 20,
        "baseline_accuracy": 0.55,
        "renamed_accuracy": 0.95,
        "delta_points": 0.40,
    },
}

INVALID_FIXTURE = {
    "model_path": "x",
    "renames": [
        {
            "field_path": "Order.flag",
            "old_name": "flag",
            "new_name": "IsPaid",
            "reason_code": "generic-placeholder",
            "rationale": "x",
        }
    ],
    "ab_eval": {
        "rows": 2,
        "baseline_accuracy": 0.5,
        "renamed_accuracy": 0.9,
        "delta_points": 0.4,
    },
}


def validate(report: dict) -> list[str]:
    v: list[str] = []
    for key in ("model_path", "schema_version", "renames", "kept", "ab_eval"):
        if key not in report:
            v.append(f"missing required key: {key}")
    if v:
        return v
    if not isinstance(report["model_path"], str) or not report["model_path"]:
        v.append("model_path must be non-empty string")
    if not SEMVER_RE.match(str(report["schema_version"])):
        v.append("schema_version must match semver X.Y.Z")
    if not isinstance(report["renames"], list):
        v.append("renames must be a list")
    else:
        for i, r in enumerate(report["renames"]):
            for k in ("field_path", "old_name", "new_name", "reason_code", "rationale"):
                if k not in r:
                    v.append(f"renames[{i}] missing {k}")
            if "new_name" in r and not SNAKE_RE.match(str(r["new_name"])):
                v.append(f"renames[{i}].new_name must be lower_snake_case (got {r['new_name']!r})")
            if "field_path" in r and not PATH_RE.match(str(r["field_path"])):
                v.append(f"renames[{i}].field_path must match path regex")
            if "reason_code" in r and r["reason_code"] not in REASONS:
                v.append(f"renames[{i}].reason_code not in closed enum (got {r['reason_code']!r})")
            if "rationale" in r and len(str(r["rationale"])) < 12:
                v.append(f"renames[{i}].rationale too short (>= 12 chars)")
    ab = report.get("ab_eval", {})
    if not isinstance(ab, dict):
        v.append("ab_eval must be object")
    else:
        for k in ("rows", "baseline_accuracy", "renamed_accuracy", "delta_points"):
            if k not in ab:
                v.append(f"ab_eval missing {k}")
        if "rows" in ab and (not isinstance(ab["rows"], int) or ab["rows"] < 5):
            v.append("ab_eval.rows must be int >= 5")
        for k in ("baseline_accuracy", "renamed_accuracy"):
            if k in ab and not (0.0 <= float(ab[k]) <= 1.0):
                v.append(f"ab_eval.{k} must be in [0,1]")
        if all(k in ab for k in ("baseline_accuracy", "renamed_accuracy", "delta_points")):
            expected = float(ab["renamed_accuracy"]) - float(ab["baseline_accuracy"])
            if abs(float(ab["delta_points"]) - expected) > 1e-6:
                v.append("ab_eval.delta_points must equal renamed_accuracy - baseline_accuracy")
    return v


def main(argv: list[str]) -> int:
    if len(argv) < 2 or argv[1] in ("--help", "-h"):
        sys.stdout.write(__doc__ or "")
        return 0 if "--help" in argv or "-h" in argv else 2
    if argv[1] == "--self-test":
        ok = validate(VALID_FIXTURE)
        bad = validate(INVALID_FIXTURE)
        if ok:
            sys.stderr.write(f"self-test FAIL: valid fixture rejected: {ok}\n")
            return 1
        if not bad:
            sys.stderr.write("self-test FAIL: invalid fixture accepted\n")
            return 1
        sys.stdout.write("self-test OK\n")
        return 0
    p = Path(argv[1])
    if not p.is_file():
        sys.stderr.write(f"not a file: {p}\n")
        return 2
    try:
        report = json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        sys.stderr.write(f"invalid JSON: {exc}\n")
        return 1
    violations = validate(report)
    if violations:
        sys.stdout.write("FAIL\n")
        for x in violations:
            sys.stdout.write(f"  - {x}\n")
        return 1
    sys.stdout.write("PASS\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
