#!/usr/bin/env python3
"""validate-event-sourcing-fundamentals.py

Validate an ES-decision spec against the schema in 02-output-contract.xml.

Inputs:
    --file PATH       artefact JSON
    --self-test       run built-in fixtures
    --help            this message

Exit codes:
    0 valid · 1 invalid · 2 usage / unreadable
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REQUIRED = ["aggregate", "decision", "rationale", "event_catalog"]
NAME_RE = re.compile(r"^[A-Z][A-Za-z0-9]+$")
DECISIONS = {"use_event_sourcing", "use_state_stored", "defer"}


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    if "aggregate" in obj and not NAME_RE.match(str(obj["aggregate"])):
        errs.append("aggregate must be PascalCase")
    if obj.get("decision") not in DECISIONS:
        errs.append(f"decision must be one of {sorted(DECISIONS)}")
    if len(str(obj.get("rationale", ""))) < 20:
        errs.append("rationale must be at least 20 chars")
    if obj.get("decision") == "use_event_sourcing" and obj.get("schema_stable") is False:
        errs.append("decision=use_event_sourcing forbidden when schema_stable=false")
    if "stream_strategy" in obj and obj["stream_strategy"] != "one_per_aggregate_instance":
        errs.append("stream_strategy must be 'one_per_aggregate_instance'")
    events = obj.get("event_catalog") or []
    if not events:
        errs.append("event_catalog must contain at least 1 entry")
    for e in events:
        if not NAME_RE.match(str(e.get("name", ""))):
            errs.append(f"event '{e.get('name')}' must be PascalCase")
        if e.get("past_tense") is not True:
            errs.append(f"event '{e.get('name')}' must be past-tense (past_tense=true)")
    return errs


OK = {
    "aggregate": "Order",
    "decision": "use_event_sourcing",
    "rationale": "regulatory audit required; replay supports refunds + dispute investigation",
    "audit_required": True,
    "replay_required": True,
    "schema_stable": True,
    "stream_strategy": "one_per_aggregate_instance",
    "event_catalog": [
        {"name": "OrderPlaced", "past_tense": True},
        {"name": "ItemAdded", "past_tense": True},
    ],
}
BAD = {
    "aggregate": "Order",
    "decision": "use_event_sourcing",
    "rationale": "we like it",
    "schema_stable": False,
    "stream_strategy": "shared_stream",
    "event_catalog": [{"name": "UpdateOrder", "past_tense": False}],
}


def self_test() -> int:
    if validate(OK):
        sys.stderr.write("ok rejected\n")
        return 1
    if not validate(BAD):
        sys.stderr.write("bad accepted\n")
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
    obj = json.loads(p.read_text())
    errs = validate(obj)
    if errs:
        for e in errs:
            sys.stderr.write(f"VIOLATION: {e}\n")
        return 1
    sys.stdout.write("OK\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
