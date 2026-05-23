#!/usr/bin/env python3
"""validate-java-jpa-hibernate.py

Validate entity + narrow-repository + service spec against 02-output-contract.xml.

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

REQUIRED = ["entity", "narrow_repository", "service", "open_in_view"]
NAME_RE = re.compile(r"^[A-Z][A-Za-z0-9]+$")
REPO_RE = re.compile(r"^[A-Z][A-Za-z0-9]+Repository$")
SVC_RE = re.compile(r"^[A-Z][A-Za-z0-9]+Service$")
ASSOC_KINDS = {"OneToMany", "ManyToOne", "ManyToMany", "OneToOne"}


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    ent = obj.get("entity") or {}
    if not NAME_RE.match(str(ent.get("class_name", ""))):
        errs.append("entity.class_name must be PascalCase")
    if ent.get("has_audit_timestamps") is not True:
        errs.append("entity.has_audit_timestamps must be true (audit-timestamps)")
    for a in ent.get("associations") or []:
        if a.get("kind") not in ASSOC_KINDS:
            errs.append(f"association.kind must be one of {sorted(ASSOC_KINDS)}")
        if len(str(a.get("justification", "")).strip()) < 10:
            errs.append("association.justification must be non-empty (>=10 chars)")
        if str(a.get("cascade", "")).upper() == "ALL" and len(str(a.get("justification", ""))) < 20:
            errs.append("CascadeType.ALL requires substantial justification (>=20 chars)")
    repo = obj.get("narrow_repository") or {}
    if not REPO_RE.match(str(repo.get("interface_name", ""))):
        errs.append("narrow_repository.interface_name must end with Repository")
    if repo.get("extends_jparepository_directly") is True:
        errs.append("narrow_repository.extends_jparepository_directly must be false (narrow-repo-interface)")
    svc = obj.get("service") or {}
    if not SVC_RE.match(str(svc.get("class_name", ""))):
        errs.append("service.class_name must end with Service")
    if svc.get("uses_dto_projection_on_reads") is not True:
        errs.append("service.uses_dto_projection_on_reads must be true")
    if obj.get("open_in_view") is True:
        errs.append("open_in_view must be false (joinfetch-for-eager)")
    return errs


OK = {
    "entity": {
        "class_name": "Order",
        "has_audit_timestamps": True,
        "version_column": True,
        "associations": [
            {"kind": "OneToMany", "cascade": "PERSIST", "fetch": "LAZY",
             "justification": "Items owned by Order; persist with parent"}
        ],
    },
    "narrow_repository": {"interface_name": "OrderRepository", "extends_jparepository_directly": False, "method_count": 5},
    "service": {"class_name": "OrderService", "uses_dto_projection_on_reads": True, "uses_joinfetch_or_entitygraph": True},
    "open_in_view": False,
}
BAD = {
    "entity": {
        "class_name": "order",
        "has_audit_timestamps": False,
        "associations": [{"kind": "OneToMany", "cascade": "ALL", "fetch": "EAGER", "justification": ""}],
    },
    "narrow_repository": {"interface_name": "OrderRepo", "extends_jparepository_directly": True},
    "service": {"class_name": "orderSvc", "uses_dto_projection_on_reads": False, "uses_joinfetch_or_entitygraph": False},
    "open_in_view": True,
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
