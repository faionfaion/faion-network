#!/usr/bin/env python3
"""validate-indie-portfolio-scorecard.py — stdlib-only validator for the Indie Portfolio Scorecard artefact.

Inputs:
    --file PATH       path to artefact JSON
    --self-test       run built-in OK + BAD fixtures (rc=0 if both pass)
    --help            this message

Exit codes:
    0 = valid (or self-test passed)
    1 = invalid
    2 = usage / unreadable
"""
from __future__ import annotations

import argparse
import json
import re
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
KNOWN_RULE_IDS = set(["five-columns-required", "ninety-day-growth-window", "hours-self-report-honest", "monthly-review-cadence", "explicit-decision-per-product", "skip-this-methodology"])
PLURAL_OWNERS = {"", "team", "we", "us", "everyone", "tbd"}
DATETIME = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}.*$")


def validate(obj: object) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    rules = obj.get("rules_applied")
    if isinstance(rules, list):
        if not rules:
            errs.append("rules_applied must be non-empty")
        for i, r in enumerate(rules):
            if not isinstance(r, str) or not r:
                errs.append(f"rules_applied[{i}] must be non-empty string")
                continue
            if r not in KNOWN_RULE_IDS:
                errs.append(f"rules_applied[{i}]={r!r} not in 01-core-rules.xml")
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
                errs.append(f"evidence[{i}].source_type={st!r} not in {sorted(ALLOWED_SOURCE_TYPES)}")
    for k in ("consumer", "owner"):
        v = obj.get(k)
        if isinstance(v, str) and v.strip().lower() in PLURAL_OWNERS:
            errs.append(f"{k} must be a named individual or agent, got {v!r}")
    lt = obj.get("last_touched")
    if isinstance(lt, str) and lt and not DATETIME.match(lt):
        errs.append(f"last_touched not ISO-8601 datetime: {lt!r}")
    op = obj.get("output_payload")
    if op is not None and not isinstance(op, dict):
        errs.append("output_payload must be an object")
    return errs


OK_FIXTURE = json.dumps(
    {
        "artefact_id": "01HXT3KQ7P9B2YJZG4N3R5VWFM",
        "trigger": "Indie Portfolio Scorecard engagement",
        "rules_applied": ["five-columns-required"],
        "evidence": [
            {
                "rule_id": "five-columns-required",
                "citation": "https://example.com/source",
                "source_type": "url",
            }
        ],
        "output_payload": {"status": "complete"},
        "consumer": "Mariia Ivanova (delivery PM)",
        "owner": "Oleh Petrov (operator)",
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
    ok_errs = validate(json.loads(OK_FIXTURE))
    if ok_errs:
        sys.stderr.write(f"self-test FAIL: OK fixture rejected: {ok_errs}\n")
        return 1
    bad_errs = validate(json.loads(BAD_FIXTURE))
    if not bad_errs:
        sys.stderr.write("self-test FAIL: BAD fixture accepted\n")
        return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("--file", type=str, help="artefact JSON file to validate")
    ap.add_argument("--self-test", action="store_true", help="run built-in OK + BAD fixtures")
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
