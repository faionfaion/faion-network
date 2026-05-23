#!/usr/bin/env python3
"""validate-java-jpa-hibernate.py

Validate the JPA-layer manifest for the java-jpa-hibernate methodology against
the JSON Schema declared in 02-output-contract.xml.

Inputs:
    --file PATH       path to artefact JSON
    --self-test       run built-in fixtures
    --help            this message

Exit codes:
    0 = valid
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
    "spring_boot_version",
    "ddl_auto",
    "open_in_view",
    "entities",
    "migrations_paired",
    "fetch_audit",
]
SB_RE = re.compile(r"^3\.")


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    if not SB_RE.match(str(obj.get("spring_boot_version", ""))):
        errs.append("spring_boot_version must start with 3.")
    if obj.get("ddl_auto") != "validate":
        errs.append("ddl_auto must be 'validate'")
    if obj.get("open_in_view") is not False:
        errs.append("open_in_view must be false")
    entities = obj.get("entities") or []
    if not isinstance(entities, list) or len(entities) < 1:
        errs.append("entities must be non-empty list")
    for i, e in enumerate(entities):
        if not str(e.get("business_key", "")):
            errs.append(f"entities[{i}].business_key must be non-empty")
        if e.get("associations_lazy") is not True:
            errs.append(f"entities[{i}].associations_lazy must be true")
        if e.get("uses_lombok_data") is not False:
            errs.append(f"entities[{i}].uses_lombok_data must be false")
    if obj.get("migrations_paired") is not True:
        errs.append("migrations_paired must be true")
    eager = (obj.get("fetch_audit") or {}).get("eager_associations_found") or []
    if eager:
        errs.append(f"fetch_audit.eager_associations_found must be empty, got {eager}")
    forbidden = obj.get("forbidden_patterns_found") or []
    if forbidden:
        errs.append(f"forbidden_patterns_found must be empty, got {forbidden}")
    return errs


OK = {
    "spring_boot_version": "3.2.1",
    "ddl_auto": "validate",
    "open_in_view": False,
    "entities": [{"class": "com.acme.Invoice", "business_key": "invoiceNumber", "associations_lazy": True, "uses_lombok_data": False}],
    "migrations_paired": True,
    "fetch_audit": {"eager_associations_found": []},
    "forbidden_patterns_found": [],
}
BAD = {
    "spring_boot_version": "2.7.0",
    "ddl_auto": "update",
    "open_in_view": True,
    "entities": [{"class": "com.acme.Invoice", "business_key": "", "associations_lazy": False, "uses_lombok_data": True}],
    "migrations_paired": False,
    "fetch_audit": {"eager_associations_found": ["Invoice.lines"]},
    "forbidden_patterns_found": ["@Data on entity"],
}


def self_test() -> int:
    if validate(OK):
        sys.stderr.write("ok fixture rejected\n")
        return 1
    if not validate(BAD):
        sys.stderr.write("bad fixture accepted\n")
        return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
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
        sys.stderr.write(f"invalid JSON: {e}\n")
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
