#!/usr/bin/env python3
"""validate-react-hooks.py

Validate a hook-correctness spec JSON against the schema in 02-output-contract.xml.

Inputs:
    --file PATH       path to JSON spec
    --self-test       run built-in fixtures
    --help            this message

Exit codes:
    0 = valid
    1 = invalid (violations on stderr)
    2 = usage / unreadable
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
ALLOWED_RULES = {
    "rules-of-hooks",
    "exhaustive-deps",
    "cleanup-missing",
    "sync-via-effect",
    "memo-bloat",
}


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    for k in ("react_version", "eslint_rules", "audit", "version", "last_reviewed"):
        if k not in obj:
            errs.append(f"missing required field: {k}")
    if "react_version" in obj and not SEMVER_RE.match(str(obj["react_version"])):
        errs.append("react_version must be semver")
    er = obj.get("eslint_rules") or {}
    if er.get("rules-of-hooks") != "error":
        errs.append("eslint_rules.rules-of-hooks must be 'error'")
    if er.get("exhaustive-deps") != "error":
        errs.append("eslint_rules.exhaustive-deps must be 'error'")
    audit = obj.get("audit") or {}
    if "files_scanned" not in audit:
        errs.append("audit.files_scanned missing")
    elif not isinstance(audit["files_scanned"], int) or audit["files_scanned"] < 0:
        errs.append("audit.files_scanned must be non-negative int")
    vs = audit.get("violations")
    if not isinstance(vs, list):
        errs.append("audit.violations must be list")
    else:
        for i, v in enumerate(vs):
            if not isinstance(v, dict):
                errs.append(f"audit.violations[{i}] must be object")
                continue
            for k in ("file", "line", "rule"):
                if k not in v:
                    errs.append(f"audit.violations[{i}] missing {k}")
            if "rule" in v and v["rule"] not in ALLOWED_RULES:
                errs.append(f"audit.violations[{i}].rule must be in {sorted(ALLOWED_RULES)}")
            if "line" in v and (not isinstance(v["line"], int) or v["line"] < 1):
                errs.append(f"audit.violations[{i}].line must be int >= 1")
    if "version" in obj and not SEMVER_RE.match(str(obj["version"])):
        errs.append("version must be semver")
    if "last_reviewed" in obj and not DATE_RE.match(str(obj["last_reviewed"])):
        errs.append("last_reviewed must be ISO date")
    return errs


OK = {
    "react_version": "19.0.0",
    "strict_mode": True,
    "compiler_enabled": True,
    "eslint_rules": {"rules-of-hooks": "error", "exhaustive-deps": "error"},
    "audit": {
        "files_scanned": 100,
        "violations": [{"file": "a.tsx", "line": 4, "rule": "exhaustive-deps"}],
    },
    "version": "1.0.0",
    "last_reviewed": "2026-05-22",
}
BAD = {
    "react_version": "19",
    "eslint_rules": {"rules-of-hooks": "warn", "exhaustive-deps": "off"},
    "audit": {"files_scanned": -1, "violations": "many"},
}


def self_test() -> int:
    if validate(OK):
        sys.stderr.write("OK rejected\n")
        return 1
    if not validate(BAD):
        sys.stderr.write("BAD accepted\n")
        return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("--file", type=str)
    ap.add_argument("--self-test", action="store_true")
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
    errs = validate(json.loads(p.read_text()))
    if errs:
        for e in errs:
            sys.stderr.write(f"VIOLATION: {e}\n")
        return 1
    sys.stdout.write("OK\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
