#!/usr/bin/env python3
"""validate-sec-codeql-autofix-on-pr.py — validate CodeQL workflow + branch-protection artefact.

Inputs:
    --file PATH       path to artefact JSON (workflow + branch protection merged)
    --self-test       run built-in fixture (valid + invalid)
    --help            show this message

Exit codes:
    0 = valid OR self-test passed
    1 = invalid OR self-test failed
    2 = usage / unreadable input
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REQUIRED = ["workflow_path", "triggers", "language_matrix", "autofix_enabled", "branch_protection"]
WORKFLOW_RE = re.compile(r"\.github/workflows/.*\.ya?ml$")

VALID_FIXTURE = {
    "workflow_path": ".github/workflows/codeql.yml",
    "triggers": ["push", "pull_request"],
    "language_matrix": ["javascript", "python"],
    "autofix_enabled": True,
    "autofix_auto_merge": False,
    "ai_detections_languages": ["bash", "dockerfile"],
    "branch_protection": {"required_status_checks": ["codeql-analyze"]},
}

INVALID_FIXTURE = {
    "workflow_path": "scripts/codeql.sh",
    "triggers": ["push"],
    "language_matrix": [],
    "autofix_enabled": True,
    "autofix_auto_merge": True,
    "branch_protection": {"required_status_checks": []},
}


def validate(obj) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root: must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    wp = obj.get("workflow_path", "")
    if not WORKFLOW_RE.search(wp or ""):
        errs.append("workflow_path: must live under .github/workflows/")
    triggers = obj.get("triggers", [])
    if "pull_request" not in triggers:
        errs.append("triggers: must contain 'pull_request'")
    lm = obj.get("language_matrix", [])
    if not isinstance(lm, list) or len(lm) < 1:
        errs.append("language_matrix: must be non-empty array")
    if obj.get("autofix_enabled") is not True:
        errs.append("autofix_enabled: must be true")
    if obj.get("autofix_auto_merge") is True:
        errs.append("autofix_auto_merge: must be false (human-in-the-loop)")
    bp = obj.get("branch_protection", {})
    if not isinstance(bp, dict):
        errs.append("branch_protection: must be object")
    else:
        rsc = bp.get("required_status_checks", [])
        if "codeql-analyze" not in rsc:
            errs.append("branch_protection.required_status_checks: must contain 'codeql-analyze'")
    return errs


def self_test() -> int:
    errs_ok = validate(VALID_FIXTURE)
    if errs_ok:
        sys.stderr.write("self-test: VALID fixture rejected:\n  " + "\n  ".join(errs_ok) + "\n")
        return 1
    errs_bad = validate(INVALID_FIXTURE)
    if not errs_bad:
        sys.stderr.write("self-test: INVALID fixture accepted (should fail)\n")
        return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--file", type=str, help="path to artefact JSON")
    ap.add_argument("--self-test", action="store_true", help="run built-in fixtures")
    args = ap.parse_args()
    if args.self_test:
        return self_test()
    if not args.file:
        ap.print_help()
        return 2
    p = Path(args.file)
    if not p.is_file():
        sys.stderr.write(f"not a file: {p}\n")
        return 2
    try:
        obj = json.loads(p.read_text())
    except Exception as e:
        sys.stderr.write(f"unreadable JSON: {e}\n")
        return 2
    errs = validate(obj)
    if errs:
        for e in errs:
            sys.stderr.write(f"VIOLATION: {e}\n")
        return 1
    sys.stdout.write("OK\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
