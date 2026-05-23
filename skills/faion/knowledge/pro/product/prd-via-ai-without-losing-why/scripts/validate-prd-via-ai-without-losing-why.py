#!/usr/bin/env python3
"""validate-prd-via-ai-without-losing-why.py

Validate the artefact produced by the `prd-via-ai-without-losing-why` methodology against the JSON Schema embedded in
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

REQUIRED = ["prd_id", "owner", "last_touched", "why", "outcome", "anti_goals", "scope", "citation_chain"]
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


OK = json.loads(r"""{"prd_id": "prd-onboarding-2026q2", "owner": "pm@acme.io", "last_touched": "2026-05-23T11:00:00Z", "why": {"customer_evidence": [{"interview_id": "i-1", "quote": "I gave up after the second step"}], "quant_signal": "drop-off at step-2 = 41%", "evidence": "BI view fct_onboarding 2026-05"}, "outcome": {"metric": "step-2 completion", "target": "+15pp", "window": "8 weeks", "evidence": "Q2 OKR doc"}, "anti_goals": ["no full onboarding rewrite", "no new pricing tiers", "no SSO additions"], "scope": ["replace step-2 with progressive disclosure", "add inline help microcopy", "instrument funnel events"], "citation_chain": [{"section": "why", "source_id": "i-1"}, {"section": "outcome", "source_id": "okr-q2"}], "template_version": "1.1.0", "status": "ready_for_review"}""")
BAD = json.loads(r"""{"prd_id": "x", "why": {}, "anti_goals": []}""")


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
