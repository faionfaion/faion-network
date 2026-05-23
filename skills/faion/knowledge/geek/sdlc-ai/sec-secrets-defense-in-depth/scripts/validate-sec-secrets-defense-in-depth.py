#!/usr/bin/env python3
"""validate-sec-secrets-defense-in-depth.py — validate two-layer secret-scan config.

Inputs:
    --file PATH       path to artefact JSON
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

REQUIRED = ["precommit_hook", "ci_workflow", "gitleaks_config_path", "trufflehog_verified_flag", "verified_finding_response"]
PRECOMMIT_ENUM = {"pre-commit", "lefthook", "husky"}
RESPONSE_ENUM = {"rotate_then_revert", "rotate_and_revert"}
WORKFLOW_RE = re.compile(r"\.github/workflows/.*\.ya?ml$")

VALID_FIXTURE = {
    "precommit_hook": "pre-commit",
    "ci_workflow": ".github/workflows/trufflehog.yml",
    "gitleaks_config_path": "gitleaks.toml",
    "trufflehog_verified_flag": True,
    "verified_finding_response": "rotate_then_revert",
    "detect_secrets_baseline": ".secrets.baseline",
    "allowlist_entries_have_comments": True,
}

INVALID_FIXTURE = {
    "precommit_hook": "manual",
    "ci_workflow": "scripts/scan.sh",
    "gitleaks_config_path": "gitleaks.toml",
    "trufflehog_verified_flag": False,
    "verified_finding_response": "ignore",
}


def validate(obj) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root: must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    if obj.get("precommit_hook") not in PRECOMMIT_ENUM and "precommit_hook" in obj:
        errs.append(f"precommit_hook: not in {sorted(PRECOMMIT_ENUM)}")
    wf = obj.get("ci_workflow", "")
    if not WORKFLOW_RE.search(wf or ""):
        errs.append("ci_workflow: must live under .github/workflows/")
    if obj.get("trufflehog_verified_flag") is not True:
        errs.append("trufflehog_verified_flag: must be true")
    if obj.get("verified_finding_response") not in RESPONSE_ENUM:
        errs.append(f"verified_finding_response: not in {sorted(RESPONSE_ENUM)}")
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
