#!/usr/bin/env python3
"""validate-founder-dependency-audit.py

Validate the artefact produced by the `founder-dependency-audit` methodology against the JSON Schema embedded in
`content/02-output-contract.xml`. Stdlib-only.

Inputs:
    --file PATH       path to artefact JSON
    --self-test       run built-in fixtures
    --help            this message

Exit codes:
    0 = valid
    1 = invalid (violation list printed to stderr)
    2 = usage / unreadable
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REQUIRED = ["audit_id", "owner", "last_touched", "revenue_lines", "accounts", "client_relationships", "dependency_score", "remediation_plan"]
PLACEHOLDERS = {"TBD", "TODO", "FIXME"}


def validate(obj) -> list:
    errs: list = []
    if not isinstance(obj, dict):
        return ["root must be JSON object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
            continue
        v = obj[k]
        if v in (None, "", [], {}):
            errs.append(f"required field empty: {k}")
        if isinstance(v, str) and v.strip().upper() in PLACEHOLDERS:
            errs.append(f"placeholder value in field: {k}")
    owner = obj.get("owner")
    if isinstance(owner, str) and owner.lower().strip() in {"team", "we", "tbd"}:
        errs.append("owner must be a single named person, not 'team' / 'we' / 'TBD'")
    return errs


OK = json.loads(r"""{"audit_id": "fda-acme-2026q2", "owner": "alex@acme.io", "last_touched": "2026-05-23T10:00:00Z", "revenue_lines": [{"id": "rev-1", "monthly": 18000, "owner_email": "alex@acme.io", "fragility": "high", "evidence": "Stripe dashboard 2026-05-22 + contract abc-123"}], "accounts": [{"id": "stripe", "owner": "alex@acme.io", "transfer_path": "team admin invite + 2FA recovery codes", "evidence": "Stripe Team page screenshot 2026-05-22"}], "client_relationships": [{"id": "client-bigco", "primary_contact": "alex@acme.io", "secondary_contact": "ops@acme.io", "evidence": "CRM record bigco-2026"}], "dependency_score": 0.62, "remediation_plan": [{"action": "Add secondary admin to Stripe + DNS", "owner": "alex@acme.io", "due_cycle": "2026-06"}], "status": "ready_for_review", "template_version": "1.1.0"}""")
BAD = json.loads(r"""{"audit_id": "x", "owner": "team", "revenue_lines": []}""")


def self_test() -> int:
    errs_ok = validate(OK)
    if errs_ok:
        sys.stderr.write(f"valid fixture rejected: {errs_ok}\n")
        return 1
    errs_bad = validate(BAD)
    if not errs_bad:
        sys.stderr.write("invalid fixture accepted\n")
        return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("--file", type=str, help="artefact JSON path")
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
    except json.JSONDecodeError as e:
        sys.stderr.write(f"invalid JSON: {e}\n")
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
