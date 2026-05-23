#!/usr/bin/env python3
"""validate-blameless-postmortem-facilitation.py

Validate the artefact for blameless-postmortem-facilitation against the schema in content/02-output-contract.xml.

Inputs:
    --file PATH       path to artefact JSON
    --self-test       run built-in fixtures (rc=0 if both pass)
    --help            this message

Exit codes:
    0 = valid (or self-test passed)
    1 = invalid
    2 = usage / unreadable
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REQUIRED = ['incident_id', 'severity', 'timeline', 'contributing_factors', 'action_items', 'language_lint_passed', 'facilitator', 'on_call_responder']


def validate(obj: object) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    return errs


OK_FIXTURE = '{"incident_id": "inc-2026-05-12", "severity": "sev2", "timeline": [{"timestamp": "2026-05-12T14:02:00Z", "what": "Error rate spike on /checkout", "evidence_url": "https://dash/abc"}, {"timestamp": "2026-05-12T14:05:00Z", "what": "On-call paged", "evidence_url": "https://pd/123"}, {"timestamp": "2026-05-12T14:08:00Z", "what": "Responder ack", "evidence_url": "https://pd/123#ack"}, {"timestamp": "2026-05-12T14:21:00Z", "what": "Rollback initiated", "evidence_url": "https://gh/pr/9"}, {"timestamp": "2026-05-12T14:34:00Z", "what": "Error rate restored", "evidence_url": "https://dash/abc"}], "contributing_factors": ["staging diverged from prod schema", "rollout did not pause on saturation signal", "alert threshold tuned for previous load"], "action_items": [{"title": "Add schema-parity gate to rollout", "owner": "platform-team", "deadline": "2026-06-01", "verifier": "sre-lead"}], "language_lint_passed": true, "facilitator": "alex.k", "on_call_responder": "sam.l"}'
BAD_FIXTURE = '{"incident_id": "inc-2026-05-12", "contributing_factors": ["Sam should have caught it"], "language_lint_passed": false}'


def self_test() -> int:
    """Built-in fixtures: OK_FIXTURE accepted, BAD_FIXTURE rejected."""
    if validate(json.loads(OK_FIXTURE)):
        sys.stderr.write("self-test FAIL: valid fixture rejected\n")
        return 1
    if not validate(json.loads(BAD_FIXTURE)):
        sys.stderr.write("self-test FAIL: invalid fixture accepted\n")
        return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
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
    try:
        obj = json.loads(p.read_text())
    except json.JSONDecodeError as e:
        sys.stderr.write(f"invalid JSON: {e}\n")
        return 1
    errs = validate(obj)
    if errs:
        for e in errs:
            sys.stderr.write(f"VIOLATION: {e}\n")
        return 1
    sys.stdout.write("OK\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
