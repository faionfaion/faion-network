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
        # audit-timestamps — optional key, but false is always a violation.
        if "has_audit_timestamps" in e and e.get("has_audit_timestamps") is not True:
            errs.append(f"entities[{i}].has_audit_timestamps must be true (audit-timestamps)")
        # justified-cascade-fetch — every declared association carries a reason.
        for j, a in enumerate(e.get("associations") or []):
            where = f"entities[{i}].associations[{j}]"
            if a.get("kind") not in ASSOC_KINDS:
                errs.append(f"{where}.kind must be one of {sorted(ASSOC_KINDS)}")
            if len(str(a.get("justification", "")).strip()) < 10:
                errs.append(f"{where}.justification must be non-empty (>=10 chars)")
            if str(a.get("cascade", "")).upper() == "ALL" and len(str(a.get("justification", ""))) < 20:
                errs.append(f"{where}: CascadeType.ALL requires substantial justification (>=20 chars)")
    # narrow_repository / service — optional blocks; fully checked when present.
    if "narrow_repository" in obj:
        repo = obj.get("narrow_repository") or {}
        if not REPO_RE.match(str(repo.get("interface_name", ""))):
            errs.append("narrow_repository.interface_name must be PascalCase ending with Repository")
        if repo.get("extends_jparepository_directly") is not False:
            errs.append("narrow_repository.extends_jparepository_directly must be false (narrow-repo-interface)")
    if "service" in obj:
        svc = obj.get("service") or {}
        if not SVC_RE.match(str(svc.get("class_name", ""))):
            errs.append("service.class_name must be PascalCase ending with Service")
        if svc.get("uses_dto_projection_on_reads") is not True:
            errs.append("service.uses_dto_projection_on_reads must be true (dto-projection-on-reads)")
        if "readonly_tx_on_queries" in svc and svc.get("readonly_tx_on_queries") is not True:
            errs.append("service.readonly_tx_on_queries must be true (service-owns-transaction-boundary)")
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
    "entities": [{
        "class": "com.acme.Invoice",
        "business_key": "invoiceNumber",
        "associations_lazy": True,
        "uses_lombok_data": False,
        "has_audit_timestamps": True,
        "version_column": True,
        "associations": [
            {"kind": "OneToMany", "cascade": "PERSIST", "fetch": "LAZY",
             "justification": "Lines owned by Invoice; persist with parent"}
        ],
    }],
    "narrow_repository": {"interface_name": "InvoiceRepository", "extends_jparepository_directly": False, "method_count": 5},
    "service": {"class_name": "InvoiceService", "uses_dto_projection_on_reads": True,
                "uses_joinfetch_or_entitygraph": True, "readonly_tx_on_queries": True},
    "migrations_paired": True,
    "fetch_audit": {"eager_associations_found": []},
    "forbidden_patterns_found": [],
}
# A fetch/migration-only audit is still valid: narrow_repository + service are optional.
OK_MINIMAL = {
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
    "entities": [{
        "class": "com.acme.Invoice",
        "business_key": "",
        "associations_lazy": False,
        "uses_lombok_data": True,
        "has_audit_timestamps": False,
        "associations": [{"kind": "OneToMany", "cascade": "ALL", "fetch": "EAGER", "justification": ""}],
    }],
    "narrow_repository": {"interface_name": "InvoiceRepo", "extends_jparepository_directly": True},
    "service": {"class_name": "invoiceSvc", "uses_dto_projection_on_reads": False},
    "migrations_paired": False,
    "fetch_audit": {"eager_associations_found": ["Invoice.lines"]},
    "forbidden_patterns_found": ["@Data on entity"],
}


def self_test() -> int:
    if validate(OK):
        sys.stderr.write("ok fixture rejected\n")
        return 1
    if validate(OK_MINIMAL):
        sys.stderr.write("minimal ok fixture rejected\n")
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
