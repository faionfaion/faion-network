#!/usr/bin/env python3
"""validate-content-refresh-sop.py

Validates a playbook-step artefact produced by methodology 'content-refresh-sop' against the
JSON Schema embedded in content/02-output-contract.xml.

Inputs:
    --file PATH       artefact JSON path
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
import sys
from pathlib import Path

REQUIRED = ["slug", "owner", "steps", "decision_branches", "deviation_log_reference"]


def validate(obj) -> list:
    errs: list = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    if "slug" in obj and obj["slug"] != "content-refresh-sop":
        errs.append(f"slug must equal 'content-refresh-sop'")
    if "steps" in obj:
        if not isinstance(obj["steps"], list) or len(obj["steps"]) < 4:
            errs.append("steps must be array with >=4 items")
        else:
            for i, st in enumerate(obj["steps"]):
                if not isinstance(st, dict):
                    errs.append(f"steps[{i}] must be object")
                    continue
                for sk in ("id", "input", "owner", "exit_criterion", "output_location"):
                    if sk not in st:
                        errs.append(f"steps[{i}] missing {sk}")
    serialised = json.dumps(obj)
    for marker in ("TBD", "TODO", "FIXME"):
        if marker in serialised:
            errs.append(f"forbidden token in payload: {marker}")
    return errs


FIXTURE_OK = {"slug": "content-refresh-sop", "owner": "playbook owner", "steps": [{"id": "s1", "input": "brief", "owner": "lead", "exit_criterion": "brief reviewed + scope confirmed", "output_location": "docs/briefs/"}, {"id": "s2", "input": "data", "owner": "analyst", "exit_criterion": "dataset >=30 records validated", "output_location": "warehouse:tbl"}, {"id": "s3", "input": "draft", "owner": "writer", "exit_criterion": "draft passes editorial check", "output_location": "docs/drafts/"}, {"id": "s4", "input": "draft", "owner": "lead", "exit_criterion": "signed off by named reviewer", "output_location": "docs/published/"}], "decision_branches": [{"when": "data_records < 30", "then": "loop back to s2"}], "deviation_log_reference": "ops/deviation-log.md#L101"}


def self_test() -> int:
    errs = validate(FIXTURE_OK)
    if errs:
        for e in errs:
            sys.stderr.write(f"self-test fixture rejected: {e}\n")
        return 1
    errs2 = validate({"slug": "content-refresh-sop"})
    if not errs2:
        sys.stderr.write("self-test: deliberately-broken fixture accepted\n")
        return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
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
    except json.JSONDecodeError as e:
        sys.stderr.write(f"JSON parse error: {e}\n")
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
