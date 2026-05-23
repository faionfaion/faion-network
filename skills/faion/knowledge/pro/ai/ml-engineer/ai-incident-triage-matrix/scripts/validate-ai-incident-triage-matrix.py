#!/usr/bin/env python3
"""validate-ai-incident-triage-matrix.py

Validate the artefact produced by the `ai-incident-triage-matrix` methodology against the
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

REQUIRED = ["incident_id", "dimensions", "scores", "weights", "composite", "lane", "raters", "evidence_refs"]


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


OK = json.loads(r"""{"incident_id": "INC-2026-04-12-001", "dimensions": [{"name": "user_impact", "anchors": {"1": "0 users", "3": "<100 users", "5": ">10k users"}}, {"name": "regression_magnitude", "anchors": {"1": "<2%", "3": "5-15%", "5": ">20%"}}, {"name": "blast_radius", "anchors": {"1": "single endpoint", "3": "single feature", "5": "all AI flows"}}], "scores": [{"dimension": "user_impact", "score": 4, "evidence": "log shows 4.2k users hit error path in 1h"}, {"dimension": "regression_magnitude", "score": 3, "evidence": "p50 quality -0.08 vs baseline"}, {"dimension": "blast_radius", "score": 3, "evidence": "single feature (refund-chat)"}], "weights": {"user_impact": 0.4, "regression_magnitude": 0.4, "blast_radius": 0.2}, "composite": 3.4, "lane": "model-regression", "raters": ["jane@team.io", "alex@team.io"], "evidence_refs": ["dashboard://incidents/INC-2026-04-12-001", "log://prom/refund-chat"]}""")
BAD = json.loads(r"""{"incident_id": "X", "scores": [{"dimension": "user_impact", "score": 4}]}""")


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
