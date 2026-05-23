#!/usr/bin/env python3
"""validate-ddd-repositories.py

Validate a repository spec against the schema in 02-output-contract.xml.

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

REQUIRED = ["aggregate", "interface", "methods", "implementation", "in_memory_double"]
AGG_RE = re.compile(r"^[A-Z][A-Za-z0-9]+$")
REPO_RE = re.compile(r"^[A-Z][A-Za-z0-9]+Repository$")
INMEM_RE = re.compile(r"^InMemory[A-Z][A-Za-z0-9]+Repository$")
METHOD_RE = re.compile(r"^(find_by_[a-z_]+|save|delete)$")


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    if "aggregate" in obj and not AGG_RE.match(str(obj["aggregate"])):
        errs.append("aggregate must be PascalCase")
    iface = obj.get("interface") or {}
    if not REPO_RE.match(str(iface.get("name", ""))):
        errs.append("interface.name must end with 'Repository'")
    if iface.get("layer") != "domain":
        errs.append("interface.layer must be 'domain'")
    if iface.get("imports_orm") is True:
        errs.append("interface.imports_orm must be false (domain-owns-interface)")
    methods = obj.get("methods") or []
    if not methods:
        errs.append("methods must contain at least 1 entry")
    for m in methods:
        if not METHOD_RE.match(str(m.get("name", ""))):
            errs.append(f"method name '{m.get('name')}' must be find_by_*/save/delete (identity-only-queries)")
    impl = obj.get("implementation") or {}
    if not REPO_RE.match(str(impl.get("name", ""))):
        errs.append("implementation.name must end with 'Repository'")
    if impl.get("layer") != "infrastructure":
        errs.append("implementation.layer must be 'infrastructure'")
    if impl.get("returns_aggregates") is not True:
        errs.append("implementation.returns_aggregates must be true (return-aggregates)")
    mem = obj.get("in_memory_double") or {}
    if not INMEM_RE.match(str(mem.get("name", ""))):
        errs.append("in_memory_double.name must start with 'InMemory'")
    if mem.get("layer") != "tests":
        errs.append("in_memory_double.layer must be 'tests'")
    return errs


OK = {
    "aggregate": "Order",
    "interface": {"name": "OrderRepository", "layer": "domain", "imports_orm": False},
    "methods": [
        {"name": "find_by_id", "kind": "identity_lookup"},
        {"name": "find_by_external_key", "kind": "identity_lookup"},
        {"name": "save", "kind": "save"},
        {"name": "delete", "kind": "delete"},
    ],
    "implementation": {"name": "SqlAlchemyOrderRepository", "layer": "infrastructure", "returns_aggregates": True},
    "in_memory_double": {"name": "InMemoryOrderRepository", "layer": "tests"},
}
BAD = {
    "aggregate": "Order",
    "interface": {"name": "OrderRepo", "layer": "infrastructure", "imports_orm": True},
    "methods": [{"name": "find_orders_for_customer", "kind": "identity_lookup"}],
    "implementation": {"name": "OrderRepo", "layer": "domain", "returns_aggregates": False},
    "in_memory_double": {"name": "FakeRepo", "layer": "tests"},
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
