#!/usr/bin/env python3
"""validate-event-sourcing-aggregate.py

Validate an ES aggregate spec against the schema in 02-output-contract.xml.

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

REQUIRED = ["aggregate", "events", "apply_handlers", "commands", "repository"]
NAME_RE = re.compile(r"^[A-Z][A-Za-z0-9]+$")
HANDLER_RE = re.compile(r"^_apply_[A-Z][A-Za-z0-9]+$")
CMD_RE = re.compile(r"^[a-z][a-z0-9_]+$")


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    if "aggregate" in obj and not NAME_RE.match(str(obj["aggregate"])):
        errs.append("aggregate must be PascalCase")
    events = obj.get("events") or []
    if not events:
        errs.append("events must contain at least 1 entry")
    for e in events:
        if not NAME_RE.match(str(e)):
            errs.append(f"event '{e}' must be PascalCase")
    handlers = obj.get("apply_handlers") or []
    for h in handlers:
        if not HANDLER_RE.match(str(h)):
            errs.append(f"apply handler '{h}' must match _apply_PascalCase")
    if events and len(handlers) < len(events):
        errs.append("missing apply handler for at least one event (lazy-apply)")
    for c in obj.get("commands") or []:
        if not CMD_RE.match(str(c.get("name", ""))):
            errs.append(f"command '{c.get('name')}' must be snake_case")
        if c.get("mutates_state_in_body") is True:
            errs.append(f"command '{c.get('name')}' mutates state in body (apply-only-mutation)")
    repo = obj.get("repository") or {}
    if repo.get("save_uses_expected_version") is not True:
        errs.append("repository.save_uses_expected_version must be true (expected-version-on-save)")
    if obj.get("has_collect_pending_events") is not True:
        errs.append("has_collect_pending_events must be true (collect-pending-boundary)")
    return errs


OK = {
    "aggregate": "Order",
    "events": ["OrderPlaced", "ItemAdded"],
    "apply_handlers": ["_apply_OrderPlaced", "_apply_ItemAdded"],
    "commands": [
        {"name": "place", "mutates_state_in_body": False},
        {"name": "add_item", "mutates_state_in_body": False},
    ],
    "repository": {
        "load_signature": "load(stream_id) -> tuple[Order, int]",
        "save_signature": "save(stream_id, events, expected_version) -> int",
        "save_uses_expected_version": True,
    },
    "has_collect_pending_events": True,
}
BAD = {
    "aggregate": "order",
    "events": [],
    "apply_handlers": ["update_state"],
    "commands": [{"name": "Place", "mutates_state_in_body": True}],
    "repository": {"load_signature": "", "save_signature": "save(events)", "save_uses_expected_version": False},
    "has_collect_pending_events": False,
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
