#!/usr/bin/env python3
"""validate-event-sourcing-projections.py

Validate a projection spec against the schema in 02-output-contract.xml.

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

REQUIRED = ["name", "handlers", "checkpoint", "rebuild_command", "has_side_effects"]
NAME_RE = re.compile(r"^[A-Z][A-Za-z0-9]+Projection$")
EVENT_RE = re.compile(r"^[A-Z][A-Za-z0-9]+$")


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    if "name" in obj and not NAME_RE.match(str(obj["name"])):
        errs.append("name must end with 'Projection'")
    for h in obj.get("handlers") or []:
        if not EVENT_RE.match(str(h.get("event_name", ""))):
            errs.append(f"handler event_name '{h.get('event_name')}' must be PascalCase")
        if h.get("operation") not in ("UPSERT", "DELETE"):
            errs.append(f"handler operation must be UPSERT or DELETE (got {h.get('operation')})")
        if h.get("idempotent") is not True:
            errs.append(f"handler for {h.get('event_name')} must be idempotent")
    cp = obj.get("checkpoint") or {}
    if not cp.get("table"):
        errs.append("checkpoint.table must be non-empty")
    if cp.get("tracks") not in ("stream_position", "global_sequence"):
        errs.append("checkpoint.tracks must be stream_position or global_sequence")
    if not str(obj.get("rebuild_command", "")).strip():
        errs.append("rebuild_command must be non-empty (rebuildable-from-zero)")
    if obj.get("has_side_effects") is True:
        errs.append("has_side_effects must be false (no-side-effects)")
    return errs


OK = {
    "name": "OrdersListProjection",
    "read_model_table": "orders_list",
    "handlers": [
        {"event_name": "OrderPlaced", "operation": "UPSERT", "idempotent": True},
        {"event_name": "OrderCancelled", "operation": "DELETE", "idempotent": True},
    ],
    "checkpoint": {"table": "projection_checkpoint", "tracks": "stream_position"},
    "rebuild_command": "python -m projections.orders_list rebuild",
    "has_side_effects": False,
}
BAD = {
    "name": "orders_proj",
    "handlers": [{"event_name": "OrderPlaced", "operation": "INSERT", "idempotent": False}],
    "checkpoint": {"table": "", "tracks": "stream_position"},
    "rebuild_command": "",
    "has_side_effects": True,
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
