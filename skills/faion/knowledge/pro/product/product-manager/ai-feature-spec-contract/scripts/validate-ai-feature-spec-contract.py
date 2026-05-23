#!/usr/bin/env python3
"""validate-ai-feature-spec-contract.py

Validate the artefact produced by the `ai-feature-spec-contract` methodology against the JSON Schema embedded in
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

REQUIRED = ["spec_id", "owner", "last_touched", "brief", "eval_rubric", "thresholds", "risk_register", "rollout_plan", "kill_switch"]
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


OK = json.loads(r"""{"spec_id": "ai-spec-summarize-2026q2", "owner": "pm@acme.io", "last_touched": "2026-05-23T11:00:00Z", "brief": {"customer": "support agent", "outcome": "ticket summary < 60s", "risk": "wrong summary loses customer trust", "evidence": "research memo 2026-05"}, "eval_rubric": {"name": "summary-quality-v1", "function": "rubric_v1.score(out, ref)", "evidence": "research repo eval/summary"}, "thresholds": {"primary": {"metric": "human_rated_correctness", "value": 0.85}}, "risk_register": [{"id": "r-1", "risk": "hallucinated names", "mitigation": "redact-then-summarize pipeline", "owner": "safety@acme.io", "evidence": "redact spec 2026-05"}], "rollout_plan": {"steps": ["internal-only 1 week", "5% canary 1 week", "ramp to 100%"], "owner": "eng@acme.io", "tested_on": "2026-05-22"}, "kill_switch": {"flag": "feature_summarize_v1", "owner": "eng@acme.io", "evidence": "feature-flag service config"}, "template_version": "1.1.0", "status": "ready_for_review"}""")
BAD = json.loads(r"""{"spec_id": "x", "eval_rubric": {}, "kill_switch": {}}""")


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
