#!/usr/bin/env python3
"""validate-strict-mode-required-fields.py — validate a StrictModeAuditReport.

Inputs:
  - <report.json>  Path to a JSON file matching 02-output-contract.

Outputs:
  - stdout: PASS / FAIL with violation list.

Exit codes:
  0 - report validates.
  1 - report violates schema or self-check rules.
  2 - usage error.

Flags:
  --help        Show this message.
  --self-test   Run against built-in fixtures.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

TARGETS = {"openai", "anthropic", "azure", "gemini"}
CODES = {
    "missing-additional-properties-false",
    "required-not-equal-properties",
    "missing-extra-forbid",
    "optional-not-nullable",
    "empty-string-sentinel",
    "metadata-bag-in-strict",
}

VALID_FIXTURE = {
    "model_path": "myapp/schemas/invoice.py",
    "target": "openai",
    "violations": [
        {
            "node_title": "Invoice",
            "code": "missing-extra-forbid",
            "message": "ConfigDict(extra='forbid') missing on Invoice.",
        }
    ],
    "patches": [
        {
            "file": "myapp/schemas/invoice.py",
            "diff_summary": "Added extra='forbid' to Invoice and LineItem.",
        }
    ],
    "ci_assert_present": True,
}

INVALID_FIXTURE = {
    "model_path": "x",
    "target": "openai",
    "violations": [{"node_title": "X", "code": "unknown", "message": "x"}],
    "patches": [],
    "ci_assert_present": "yes",
}


def validate(report: dict) -> list[str]:
    v: list[str] = []
    for k in ("model_path", "target", "violations", "patches", "ci_assert_present"):
        if k not in report:
            v.append(f"missing required key: {k}")
    if v:
        return v
    if not isinstance(report["model_path"], str) or not report["model_path"]:
        v.append("model_path must be non-empty string")
    if report["target"] not in TARGETS:
        v.append(f"target not in {sorted(TARGETS)} (got {report['target']!r})")
    if not isinstance(report["violations"], list):
        v.append("violations must be a list")
    else:
        for i, vio in enumerate(report["violations"]):
            for k in ("node_title", "code", "message"):
                if k not in vio:
                    v.append(f"violations[{i}] missing {k}")
            if "code" in vio and vio["code"] not in CODES:
                v.append(f"violations[{i}].code not in closed enum (got {vio['code']!r})")
            if "message" in vio and len(str(vio["message"])) < 8:
                v.append(f"violations[{i}].message too short")
    if not isinstance(report["patches"], list):
        v.append("patches must be a list")
    if not isinstance(report["ci_assert_present"], bool):
        v.append("ci_assert_present must be bool")
    if isinstance(report.get("violations"), list) and report["violations"] and isinstance(report.get("patches"), list) and not report["patches"]:
        v.append("non-empty violations require non-empty patches (audit incomplete)")
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
