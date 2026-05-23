#!/usr/bin/env python3
"""validate-inbound-intake-qualification.py

Validate the artefact for inbound-intake-qualification against the schema in content/02-output-contract.xml.

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

REQUIRED = [
    "artefact_id",
    "trigger",
    "rules_applied",
    "evidence",
    "output_payload",
    "consumer",
    "owner",
    "last_touched",
]
ALLOWED_SOURCE_TYPES = {"url", "ticket", "doc", "transcript", "contract"}


def validate(obj: object) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    if isinstance(obj.get("rules_applied"), list) and not obj["rules_applied"]:
        errs.append("rules_applied must be non-empty")
    ev = obj.get("evidence")
    if isinstance(ev, list):
        if not ev:
            errs.append("evidence must be non-empty")
        for i, e in enumerate(ev):
            if not isinstance(e, dict):
                errs.append(f"evidence[{i}] not object")
                continue
            for ek in ("rule_id", "citation", "source_type"):
                if ek not in e:
                    errs.append(f"evidence[{i}].{ek} missing")
            st = e.get("source_type")
            if st is not None and st not in ALLOWED_SOURCE_TYPES:
                errs.append(f"evidence[{i}].source_type not in {sorted(ALLOWED_SOURCE_TYPES)}")
    for k in ("consumer", "owner"):
        v = obj.get(k)
        if isinstance(v, str) and v.strip().lower() in {"", "team", "tbd", "everyone"}:
            errs.append(f"{k} must be a named individual or agent, got {v!r}")
    return errs


OK_FIXTURE = json.dumps(
    {
        "artefact_id": "01HXT3KQ7P9B2YJZG4N3R5VWFM",
        "trigger": "inbound-intake-qualification engagement",
        "rules_applied": ["five-question-rubric"],
        "evidence": [
            {
                "rule_id": "five-question-rubric",
                "citation": "https://example.com/source",
                "source_type": "url",
            }
        ],
        "output_payload": {"status": "complete"},
        "consumer": "Mariia Ivanova (delivery PM)",
        "owner": "Oleh Petrov (BA)",
        "last_touched": "2026-05-23T10:00:00Z",
    }
)
BAD_FIXTURE = json.dumps(
    {
        "artefact_id": "x",
        "trigger": "vague",
        "rules_applied": [],
        "output_payload": {},
    }
)


def self_test() -> int:
    if validate(json.loads(OK_FIXTURE)):
        sys.stderr.write("self-test FAIL: valid fixture rejected\n")
        return 1
    if not validate(json.loads(BAD_FIXTURE)):
        sys.stderr.write("self-test FAIL: invalid fixture accepted\n")
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
