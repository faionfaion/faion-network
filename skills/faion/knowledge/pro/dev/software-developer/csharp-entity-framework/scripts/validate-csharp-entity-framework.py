#!/usr/bin/env python3
"""validate-csharp-entity-framework.py

Validate entity + configuration + repository + migration spec.

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

REQUIRED = ["entity", "configuration", "repository", "migration"]
ENT_RE = re.compile(r"^[A-Z][A-Za-z0-9]+$")
CONF_RE = re.compile(r"^[A-Z][A-Za-z0-9]+Configuration$")
REPO_RE = re.compile(r"^[A-Z][A-Za-z0-9]+Repository$")
MIG_RE = re.compile(r"^[A-Z][A-Za-z0-9]+$")


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    ent = obj.get("entity") or {}
    if not ENT_RE.match(str(ent.get("class_name", ""))):
        errs.append("entity.class_name must be PascalCase")
    if ent.get("has_public_setters") is True:
        errs.append("entity.has_public_setters must be false")
    if ent.get("data_annotations_present") is True:
        errs.append("entity.data_annotations_present must be false (fluent-config-only)")
    conf = obj.get("configuration") or {}
    if not CONF_RE.match(str(conf.get("class_name", ""))):
        errs.append("configuration.class_name must end with 'Configuration'")
    if conf.get("configures_keys") is not True:
        errs.append("configuration.configures_keys must be true")
    repo = obj.get("repository") or {}
    if not REPO_RE.match(str(repo.get("class_name", ""))):
        errs.append("repository.class_name must end with 'Repository'")
    if repo.get("list_uses_asnotracking") is not True:
        errs.append("repository.list_uses_asnotracking must be true")
    if repo.get("returns_iqueryable") is True:
        errs.append("repository.returns_iqueryable must be false (no-iqueryable-return)")
    mig = obj.get("migration") or {}
    if not MIG_RE.match(str(mig.get("name", ""))):
        errs.append("migration.name must be PascalCase verb-prefix")
    if mig.get("appended") is not True:
        errs.append("migration.appended must be true (append-only-migrations)")
    return errs


OK = {
    "entity": {"class_name": "Order", "has_public_setters": False, "data_annotations_present": False},
    "configuration": {"class_name": "OrderConfiguration", "configures_keys": True, "configures_indexes": True},
    "repository": {"class_name": "OrderRepository", "list_uses_asnotracking": True, "returns_iqueryable": False, "multi_collection_split_query": True},
    "migration": {"name": "AddOrdersTable", "appended": True},
}
BAD = {
    "entity": {"class_name": "order", "has_public_setters": True, "data_annotations_present": True},
    "configuration": {"class_name": "OrderConfig", "configures_keys": False},
    "repository": {"class_name": "OrderRepo", "list_uses_asnotracking": False, "returns_iqueryable": True},
    "migration": {"name": "fix_typo", "appended": False},
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
