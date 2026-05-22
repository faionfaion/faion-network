#!/usr/bin/env python3
"""validate-python-typing.py — Validate the python-typing output report.

Inputs:
  - <report.json>  Path to a JSON file produced by the python-typing methodology run.

Outputs:
  - stdout: pass / fail with violation list.

Exit codes:
  0 - report validates.
  1 - report violates schema or self-check rules.
  2 - usage error.

Flags:
  --help        Show this message.
  --self-test   Run against a built-in fixture.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

SCHEMA_VERSION = "1.1.0"
IGNORE_CODE_RE = re.compile(r"^[a-z-]+$")
PY_FLOOR_RE = re.compile(r"^3\.(1[0-9]|[2-9][0-9])$")

VALID_FIXTURE = {
    "module": "myapp.services.billing",
    "python_version_floor": "3.12",
    "mypy_strict": True,
    "errors": {"before": 42, "after": 0},
    "any_count": {"before": 11, "after": 1},
    "ignores": [
        {
            "file": "myapp/services/billing.py",
            "line": 87,
            "code": "no-any-return",
            "justification": "django-stubs lacks typing for Manager.raw().",
        }
    ],
}

INVALID_FIXTURE = {
    "module": "x",
    "mypy_strict": True,
    "python_version_floor": "3.12",
    "errors": {"before": 1, "after": 3},
    "any_count": {"before": 0, "after": 0},
    "ignores": [],
}


def validate(report: dict) -> list[str]:
    violations: list[str] = []
    required = ["module", "python_version_floor", "mypy_strict", "errors", "any_count", "ignores"]
    for key in required:
        if key not in report:
            violations.append(f"missing required key: {key}")
    if violations:
        return violations
    if not isinstance(report["module"], str) or not report["module"]:
        violations.append("module must be non-empty string")
    if not PY_FLOOR_RE.match(report["python_version_floor"]):
        violations.append("python_version_floor must match ^3\\.(1[0-9]|[2-9][0-9])$")
    if report["mypy_strict"] is not True:
        violations.append("mypy_strict must be true")
    errors = report["errors"]
    if not isinstance(errors, dict) or "before" not in errors or "after" not in errors:
        violations.append("errors must be {before, after}")
    else:
        if errors["after"] != 0:
            violations.append(f"errors.after must be 0 (got {errors['after']})")
        if errors["before"] < 0 or errors["after"] < 0:
            violations.append("error counts must be non-negative")
    any_count = report["any_count"]
    if not isinstance(any_count, dict) or "before" not in any_count or "after" not in any_count:
        violations.append("any_count must be {before, after}")
    elif any_count["after"] < 0 or any_count["before"] < 0:
        violations.append("any_count must be non-negative")
    ignores = report["ignores"]
    if not isinstance(ignores, list):
        violations.append("ignores must be a list")
    else:
        for i, ig in enumerate(ignores):
            for key in ("file", "line", "code", "justification"):
                if key not in ig:
                    violations.append(f"ignores[{i}] missing {key}")
                    continue
            if "code" in ig and not IGNORE_CODE_RE.match(str(ig["code"])):
                violations.append(f"ignores[{i}].code must match ^[a-z-]+$ (got {ig['code']!r})")
            if "justification" in ig and len(str(ig["justification"])) < 5:
                violations.append(f"ignores[{i}].justification too short")
            if "line" in ig and (not isinstance(ig["line"], int) or ig["line"] < 1):
                violations.append(f"ignores[{i}].line must be int >= 1")
    return violations


def main(argv: list[str]) -> int:
    if len(argv) < 2 or argv[1] in ("--help", "-h"):
        sys.stdout.write(__doc__ or "")
        return 0 if "--help" in argv else 2
    if argv[1] == "--self-test":
        ok_violations = validate(VALID_FIXTURE)
        bad_violations = validate(INVALID_FIXTURE)
        if ok_violations:
            sys.stderr.write(f"self-test FAIL: valid fixture rejected: {ok_violations}\n")
            return 1
        if not bad_violations:
            sys.stderr.write("self-test FAIL: invalid fixture accepted\n")
            return 1
        sys.stdout.write("self-test OK\n")
        return 0
    report_path = Path(argv[1])
    if not report_path.is_file():
        sys.stderr.write(f"not a file: {report_path}\n")
        return 2
    try:
        report = json.loads(report_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        sys.stderr.write(f"invalid JSON: {exc}\n")
        return 1
    violations = validate(report)
    if violations:
        sys.stdout.write("FAIL\n")
        for v in violations:
            sys.stdout.write(f"  - {v}\n")
        return 1
    sys.stdout.write("PASS\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
