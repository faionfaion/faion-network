#!/usr/bin/env python3
"""validate-ddd-aggregates.py

Validate an aggregate spec against the schema in 02-output-contract.xml.

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

REQUIRED = ["aggregate_root", "commands", "invariants", "events", "cross_aggregate_refs", "child_entity_count"]
ROOT_RE = re.compile(r"^[A-Z][A-Za-z0-9]+$")
CMD_RE = re.compile(r"^[a-z][a-z0-9_]+$")
INV_RE = re.compile(r"^test_(cannot|can|must)_[a-z0-9_]+$")
EVT_RE = re.compile(r"^[A-Z][A-Za-z0-9]+$")


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    if "aggregate_root" in obj and not ROOT_RE.match(str(obj["aggregate_root"])):
        errs.append("aggregate_root must be PascalCase")
    if obj.get("has_public_setters") is True:
        errs.append("has_public_setters must be false")
    cmds = obj.get("commands") or []
    if not cmds:
        errs.append("commands must contain at least 1 entry")
    for c in cmds:
        if not CMD_RE.match(str(c)):
            errs.append(f"command '{c}' must be snake_case verb")
    invs = obj.get("invariants") or []
    if not invs:
        errs.append("invariants must contain at least 1 entry")
    for inv in invs:
        if not INV_RE.match(str(inv.get("test_name", ""))):
            errs.append(f"invariant test name '{inv.get('test_name')}' must start with test_cannot_/test_can_/test_must_")
    evs = obj.get("events") or []
    if not evs and cmds:
        errs.append("events empty while commands present (raise-event-on-mutation)")
    for e in evs:
        if not EVT_RE.match(str(e)):
            errs.append(f"event '{e}' must be PascalCase")
    for r in obj.get("cross_aggregate_refs") or []:
        if r.get("ref_kind") == "object":
            errs.append(f"cross-aggregate ref to {r.get('aggregate')} must be identity, not object")
    if obj.get("child_entity_count", 0) > 5:
        errs.append("child_entity_count > 5 violates small-aggregate")
    return errs


OK = {
    "aggregate_root": "Order",
    "has_public_setters": False,
    "commands": ["place", "add_item", "cancel"],
    "invariants": [
        {"name": "empty order", "test_name": "test_cannot_place_empty_order"},
        {"name": "shipped cancel", "test_name": "test_cannot_cancel_shipped_order"},
    ],
    "events": ["OrderPlaced", "OrderCancelled"],
    "cross_aggregate_refs": [{"aggregate": "Customer", "ref_kind": "identity"}],
    "child_entity_count": 2,
}
BAD = {
    "aggregate_root": "order",
    "has_public_setters": True,
    "commands": ["SetStatus"],
    "invariants": [{"name": "x", "test_name": "shouldWork"}],
    "events": [],
    "cross_aggregate_refs": [{"aggregate": "Customer", "ref_kind": "object"}],
    "child_entity_count": 12,
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
