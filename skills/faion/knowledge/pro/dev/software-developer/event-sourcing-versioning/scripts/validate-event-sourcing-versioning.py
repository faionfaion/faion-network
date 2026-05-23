#!/usr/bin/env python3
"""validate-event-sourcing-versioning.py

Validate an event-catalog-entry / upcaster spec against the schema in 02-output-contract.xml.

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

REQUIRED = ["event_name", "event_version", "fields", "pii_handling", "ci_gate_enabled"]
NAME_RE = re.compile(r"^[A-Z][A-Za-z0-9]+$")
PII_KEYS = {"email", "phone", "name", "address", "ssn", "card_number"}
PII_POLICIES = {"none", "crypto_shredding", "externalized_side_table"}


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    if "event_name" in obj and not NAME_RE.match(str(obj["event_name"])):
        errs.append("event_name must be PascalCase")
    v = obj.get("event_version")
    if not isinstance(v, int) or v < 1:
        errs.append("event_version must be int >= 1")
    if isinstance(v, int) and v >= 2:
        if "upcaster_from" not in obj or "upcaster_module" not in obj:
            errs.append("event_version >= 2 requires upcaster_from + upcaster_module")
    if obj.get("pii_handling") not in PII_POLICIES:
        errs.append(f"pii_handling must be one of {sorted(PII_POLICIES)}")
    if obj.get("ci_gate_enabled") is not True:
        errs.append("ci_gate_enabled must be true")
    field_names = [str(f.get("name", "")) for f in obj.get("fields") or []]
    if any(fn in PII_KEYS for fn in field_names) and obj.get("pii_handling") == "none":
        errs.append(f"PII-like field present ({[fn for fn in field_names if fn in PII_KEYS]}) but pii_handling=none")
    return errs


OK = {
    "event_name": "OrderPlaced",
    "event_version": 2,
    "fields": [
        {"name": "order_id", "type": "UUID"},
        {"name": "buyer_id", "type": "UUID"},
        {"name": "total_cents", "type": "int"},
    ],
    "upcaster_from": 1,
    "upcaster_module": "faion.events.upcasters.order_placed_v1_to_v2",
    "pii_handling": "externalized_side_table",
    "ci_gate_enabled": True,
}
BAD = {
    "event_name": "orderPlaced",
    "event_version": 3,
    "fields": [{"name": "email", "type": "str"}],
    "pii_handling": "none",
    "ci_gate_enabled": False,
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
