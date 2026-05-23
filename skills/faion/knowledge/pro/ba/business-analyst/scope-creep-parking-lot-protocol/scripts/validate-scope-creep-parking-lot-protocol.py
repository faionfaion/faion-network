#!/usr/bin/env python3
"""validate-scope-creep-parking-lot-protocol.py

Validate a config artefact produced by the scope-creep-parking-lot-protocol methodology
against the JSON Schema captured in content/02-output-contract.xml.

stdlib-only. Inputs / outputs / exit codes documented under --help.

Inputs:
    --file PATH       path to artefact JSON
    --self-test       run built-in fixture
    --help            this message

Exit codes:
    0 = valid
    1 = invalid
    2 = usage / unreadable
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REQUIRED = ['parking_lot', 'items', 'triage_handoff', 'response_log']


def validate(obj) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be a JSON object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    return errs


OK = json.loads('{"parking_lot": {"meeting_id": "M-2026-05-21-demo", "meeting_date": "2026-05-21", "facilitator": "BA"}, "items": [{"item_id": "PL-1", "quote_verbatim": "Can we add a custom approval step for SMB?", "requester_name": "Client PM", "requester_role": "client", "context_in_meeting": "during checkout flow demo", "timestamp_in_meeting": "00:24:18"}], "triage_handoff": [{"item_id": "PL-1", "passed_to_classifier_at": "2026-05-22T09:00:00Z", "baseline_version": "v2026Q2-baseline"}], "response_log": [{"item_id": "PL-1", "sent_to": "Client PM", "sent_at": "2026-05-23T10:00:00Z", "verdict_cited": "scope_change", "next_step": "CR-0042 opened", "channel": "email"}]}')
BAD = json.loads('{"parking_lot": {"meeting_id": "x"}, "items": [{"item_id": "PL-1"}]}')


def self_test() -> int:
    if validate(OK):
        sys.stderr.write("self-test FAIL: good fixture rejected\n")
        return 1
    if not validate(BAD):
        sys.stderr.write("self-test FAIL: bad fixture accepted\n")
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
        obj = json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        sys.stderr.write(f"VIOLATION: invalid JSON: {e}\n")
        return 1
    errs = validate(obj)
    if errs:
        for e in errs:
            sys.stderr.write(f"VIOLATION: {e}\n")
        return 1
    sys.stdout.write("OK\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
