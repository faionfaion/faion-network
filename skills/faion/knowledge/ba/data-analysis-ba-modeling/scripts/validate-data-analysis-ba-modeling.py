#!/usr/bin/env python3
"""validate-data-analysis.py

Validate a data-dictionary artefact (JSON) against 02-output-contract.xml.

Inputs:
    --file PATH       path to dictionary JSON
    --self-test       run built-in fixtures
    --help            this message

Exit codes:
    0 = valid; 1 = invalid; 2 = usage / unreadable.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

CANON_TYPES = {"string", "int", "float", "bool", "date", "datetime", "uuid", "json", "blob"}
DQ_DIMS = ("accuracy", "completeness", "consistency", "timeliness", "validity", "uniqueness")
SEMVER = re.compile(r"^v\d+\.\d+\.\d+$")
SEVERITIES = {"block", "warn", "info"}
ANON_OWNERS = {"data team", "team", "ops", "engineering", "?", ""}


def validate(obj: object) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in ("dictionary_id", "version_tag", "entities", "business_rules"):
        if k not in obj:
            errs.append(f"missing required field: {k}")
    vt = obj.get("version_tag", "")
    if not isinstance(vt, str) or not SEMVER.match(vt):
        errs.append("version_tag must match ^v\\d+\\.\\d+\\.\\d+$ (rule r5)")
    entities = obj.get("entities", [])
    if not entities:
        errs.append("entities must be non-empty")
    for i, e in enumerate(entities):
        if not isinstance(e, dict):
            errs.append(f"entities[{i}] must be object"); continue
        owner = (e.get("owner_name", "") or "").strip().lower()
        if not owner or owner in ANON_OWNERS or len(owner.split()) < 2:
            errs.append(f"entities[{i}].owner_name anonymous '{e.get('owner_name')}' (rule r4)")
        fields = e.get("fields", [])
        if not fields:
            errs.append(f"entities[{i}].fields empty (rule r1)")
        for j, f in enumerate(fields):
            if f.get("type") not in CANON_TYPES:
                errs.append(f"entities[{i}].fields[{j}].type '{f.get('type')}' not canonical (rule r1)")
            for req in ("source_system", "source_ref"):
                if not (f.get(req) or "").strip():
                    errs.append(f"entities[{i}].fields[{j}].{req} missing (rule r1)")
        dq = e.get("dq_baseline", {})
        for dim in DQ_DIMS:
            if dim not in dq:
                errs.append(f"entities[{i}].dq_baseline missing {dim} (rule r2)")
    rules = obj.get("business_rules", [])
    if not isinstance(rules, list):
        errs.append("business_rules must be list")
    else:
        for i, r in enumerate(rules):
            pred = (r.get("predicate") or "").strip()
            if len(pred) < 4:
                errs.append(f"business_rules[{i}].predicate too short / prose-only (rule r3)")
            if r.get("severity") not in SEVERITIES:
                errs.append(f"business_rules[{i}].severity must be one of {sorted(SEVERITIES)}")
    return errs


OK_FIXTURE = {
    "dictionary_id": "core-customer",
    "version_tag": "v1.0.0",
    "entities": [{
        "name": "customer", "owner_name": "Maria Lopes", "owner_role": "Steward",
        "fields": [{"name": "id", "type": "uuid", "source_system": "crm", "source_ref": "crm.customers.id", "nullable": False}],
        "dq_baseline": {d: 90 for d in DQ_DIMS},
    }],
    "business_rules": [{"id": "br-01", "entity": "customer", "predicate": "regex(email,'^[^@]+@[^@]+$')", "severity": "block"}],
}
BAD_FIXTURE = {"dictionary_id": "x", "version_tag": "latest", "entities": [], "business_rules": []}


def self_test() -> int:
    if validate(OK_FIXTURE):
        sys.stderr.write("OK rejected\n"); return 1
    if not validate(BAD_FIXTURE):
        sys.stderr.write("BAD accepted\n"); return 1
    sys.stdout.write("self-test OK\n"); return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--file", type=str)
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        return self_test()
    if not args.file:
        ap.print_help(); return 2
    p = Path(args.file)
    if not p.is_file():
        sys.stderr.write(f"not a file: {p}\n"); return 2
    obj = json.loads(p.read_text())
    errs = validate(obj)
    if errs:
        for e in errs:
            sys.stderr.write(f"VIOLATION: {e}\n")
        return 1
    sys.stdout.write("OK\n"); return 0


if __name__ == "__main__":
    sys.exit(main())
