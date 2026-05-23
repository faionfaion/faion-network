#!/usr/bin/env python3
"""validate-ddd-domain-events.py

Validate a domain-event + outbox spec against the schema in 02-output-contract.xml.

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

REQUIRED = ["event_name", "frozen", "raised_in", "metadata", "delivery"]
NAME_RE = re.compile(r"^[A-Z][A-Za-z0-9]+$")
METHOD_RE = re.compile(r"^[a-z][a-z0-9_]+$")


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    if "event_name" in obj and not NAME_RE.match(str(obj["event_name"])):
        errs.append("event_name must be PascalCase past-tense fact")
    if obj.get("frozen") is not True:
        errs.append("frozen must be true (frozen-events)")
    ri = obj.get("raised_in") or {}
    if not NAME_RE.match(str(ri.get("aggregate", ""))):
        errs.append("raised_in.aggregate must be PascalCase")
    if not METHOD_RE.match(str(ri.get("command_method", ""))):
        errs.append("raised_in.command_method must be snake_case")
    md = obj.get("metadata") or {}
    if md.get("event_id") != "UUID":
        errs.append("metadata.event_id must be 'UUID'")
    if md.get("occurred_at") != "datetime":
        errs.append("metadata.occurred_at must be 'datetime'")
    if not str(md.get("aggregate_identity", "")).strip():
        errs.append("metadata.aggregate_identity must be non-empty")
    dlv = obj.get("delivery") or {}
    if dlv.get("target") not in ("in-process", "broker"):
        errs.append("delivery.target must be in-process or broker")
    if dlv.get("collect_after_commit") is not True:
        errs.append("delivery.collect_after_commit must be true")
    if dlv.get("target") == "broker" and dlv.get("uses_outbox") is not True:
        errs.append("broker target requires uses_outbox=true (outbox-on-broker)")
    return errs


OK = {
    "event_name": "OrderPlaced",
    "frozen": True,
    "raised_in": {"aggregate": "Order", "command_method": "place"},
    "metadata": {"event_id": "UUID", "occurred_at": "datetime", "aggregate_identity": "order_id"},
    "delivery": {"target": "broker", "uses_outbox": True, "collect_after_commit": True},
}
BAD = {
    "event_name": "orderPlaced",
    "frozen": False,
    "raised_in": {"aggregate": "order", "command_method": "Place"},
    "metadata": {"aggregate_identity": ""},
    "delivery": {"target": "broker", "uses_outbox": False, "collect_after_commit": False},
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
