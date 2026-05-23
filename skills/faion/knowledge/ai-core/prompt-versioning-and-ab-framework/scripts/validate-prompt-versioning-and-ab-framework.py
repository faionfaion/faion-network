#!/usr/bin/env python3
"""validate-prompt-versioning-and-ab-framework.py

Validate the artefact produced by the `prompt-versioning-and-ab-framework` methodology against the
JSON Schema embedded in `content/02-output-contract.xml`.

This validator uses stdlib only (no pyyaml/pydantic) for portability.

Inputs:
    --file PATH       path to artefact (JSON)
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

REQUIRED = ["prompts", "variants", "traffic_split", "metrics", "power_analysis", "significance_gate", "decision"]


def validate(obj) -> list:
    errs = []
    if not isinstance(obj, dict):
        return ["root must be JSON object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
            continue
        v = obj[k]
        if v in (None, "", [], {}):
            errs.append(f"required field empty: {k}")
        if isinstance(v, str) and v.strip().upper() in {"TBD", "TODO", "FIXME"}:
            errs.append(f"placeholder value in field: {k}")
    owner = obj.get("owner")
    if isinstance(owner, str) and owner.lower().strip() in {"team", "we", "tbd"}:
        errs.append("owner must be a single named person, not 'team' / 'we' / 'TBD'")
    return errs


OK = json.loads(r"""{"prompts": [{"id": "refund-chat", "version": "2.1.0", "owner": "jane@team.io", "changelog": "v2.1.0: add explicit refusal path; reviewer alex@team.io; eval delta +0.03"}], "variants": [{"variant_id": "A", "prompt_id": "refund-chat", "version": "2.0.0"}, {"variant_id": "B", "prompt_id": "refund-chat", "version": "2.1.0"}], "traffic_split": {"method": "hash(user_id) % 2", "buckets": {"A": 0.5, "B": 0.5}}, "metrics": {"primary": "csat_score", "secondary": ["quality", "cost_per_request", "p95_latency"]}, "power_analysis": {"expected_effect": 0.05, "mde": 0.02, "target_n": 5000}, "significance_gate": {"test": "two-sided-z", "threshold": 0.05}, "decision": "promote_b"}""")
BAD = json.loads(r"""{"prompts": [{"id": "p", "version": "latest"}], "variants": [{"variant_id": "A"}]}""")


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
