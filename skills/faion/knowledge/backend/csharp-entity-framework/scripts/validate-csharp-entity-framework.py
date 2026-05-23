#!/usr/bin/env python3
"""validate-csharp-entity-framework.py

Validate the EF data-layer manifest for the csharp-entity-framework methodology
against the JSON Schema declared in 02-output-contract.xml.

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
    "dbcontext_name",
    "provider",
    "entities",
    "asnotracking_audit",
    "concurrency_audit",
    "audit_interceptor",
    "migration_sql_reviewed",
]
ALLOWED_PROVIDERS = {"Npgsql", "SqlServer", "Sqlite"}
DBCONTEXT_RE = re.compile(r"^[A-Z][A-Za-z0-9]+DbContext$")


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    if not DBCONTEXT_RE.match(obj.get("dbcontext_name", "")):
        errs.append("dbcontext_name must match ^[A-Z][A-Za-z0-9]+DbContext$")
    if obj.get("provider") not in ALLOWED_PROVIDERS:
        errs.append(f"provider must be one of {sorted(ALLOWED_PROVIDERS)}")
    entities = obj.get("entities") or []
    if not isinstance(entities, list) or len(entities) < 1:
        errs.append("entities must be non-empty list")
    for i, e in enumerate(entities):
        if not isinstance(e, dict):
            errs.append(f"entities[{i}] must be object")
            continue
        for k in ("name", "configuration_class", "is_aggregate_root"):
            if k not in e:
                errs.append(f"entities[{i}].{k} missing")
        cls = e.get("configuration_class", "")
        if not cls.endswith("Configuration"):
            errs.append(f"entities[{i}].configuration_class must end with 'Configuration'")
        if e.get("is_aggregate_root") is True and not e.get("concurrency_token_field"):
            errs.append(f"entities[{i}] aggregate root must declare concurrency_token_field")
    if not (obj.get("asnotracking_audit") or {}).get("read_paths_pass") is True:
        errs.append("asnotracking_audit.read_paths_pass must be true")
    if not (obj.get("concurrency_audit") or {}).get("aggregates_have_token") is True:
        errs.append("concurrency_audit.aggregates_have_token must be true")
    if not (obj.get("audit_interceptor") or {}).get("registered") is True:
        errs.append("audit_interceptor.registered must be true")
    if obj.get("migration_sql_reviewed") is not True:
        errs.append("migration_sql_reviewed must be true")
    forbidden = obj.get("forbidden_patterns_found") or []
    if forbidden:
        errs.append(f"forbidden_patterns_found must be empty, got {forbidden}")
    return errs


OK = {
    "dbcontext_name": "BillingDbContext",
    "provider": "Npgsql",
    "entities": [
        {"name": "Invoice", "configuration_class": "InvoiceConfiguration", "is_aggregate_root": True, "concurrency_token_field": "xmin"}
    ],
    "asnotracking_audit": {"read_paths_pass": True},
    "concurrency_audit": {"aggregates_have_token": True},
    "audit_interceptor": {"registered": True},
    "migration_sql_reviewed": True,
    "forbidden_patterns_found": [],
}
BAD = {
    "dbcontext_name": "billing_db",
    "provider": "MariaDB",
    "entities": [],
    "asnotracking_audit": {"read_paths_pass": False},
    "concurrency_audit": {"aggregates_have_token": False},
    "audit_interceptor": {"registered": False},
    "migration_sql_reviewed": False,
    "forbidden_patterns_found": ["IQueryable leak"],
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
