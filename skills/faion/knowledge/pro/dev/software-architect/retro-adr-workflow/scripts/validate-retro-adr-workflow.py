#!/usr/bin/env python3
"""validate-retro-adr-workflow.py

Validate the artefact for retro-adr-workflow against the schema in content/02-output-contract.xml.

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

REQUIRED = ['id', 'title', 'status', 'decided_on_estimated', 'authored_on', 'owner', 'sources', 'body']


def validate(obj: object) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    return errs


OK_FIXTURE = '{"id": "ADR-0042", "title": "Authentication uses opaque tokens, not JWT", "status": "accepted-retroactively", "decided_on_estimated": "q3-2025", "authored_on": "2026-05-20", "owner": "jonas@co", "sources": ["PR #312", "chat thread #auth 2025-09-12", "commit 7f3a9b2"], "body": {"original_intent": "Opaque tokens were chosen because the auth flow already terminated at the gateway and JWT validation would have required a sidecar per service.", "current_reconstruction": "Opaque tokens shifted validation cost to a Redis lookup per request, fine at \\u2264200 RPS but a problem at horizontal shard scale.", "consequences": "Redis becomes a critical dependency; outage = auth outage.", "alternatives_considered_now": "JWT + JWKS removes Redis dependency at the cost of refresh logic per service."}}'
BAD_FIXTURE = '{"id": "X", "status": "accepted", "owner": "platform team"}'


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
