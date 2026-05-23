#!/usr/bin/env python3
"""validate-cross-tool-migration.py

Validate a playbook-step artefact for Cross-Tool Migration against the schema in
content/02-output-contract.xml. Stdlib-only.

Inputs:
    --file PATH    path to artefact JSON
    --self-test    run built-in fixtures and exit
    --help         this message

Exit codes:
    0 = valid
    1 = invalid (violations on stderr)
    2 = usage / unreadable
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REQUIRED = ['source_tool', 'target_tool', 'phase_state', 'field_map_path', 'identity_merge_strategy', 'rollback_gate']


def validate(obj):
    errs = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    ps = obj.get("phase_state") or {}
    if not isinstance(ps, dict):
        errs.append("phase_state must be object")
    else:
        for k in ("discover", "field_map", "dry_run", "cutover",
                  "verify", "decommission"):
            if k not in ps:
                errs.append(f"phase_state.{k} missing")
        # phase order constraint
        if ps.get("decommission") != "pending" and ps.get("verify") != "done":
            errs.append("decommission active before verify done")
        if ps.get("cutover") != "pending" and ps.get("dry_run") != "done":
            errs.append("cutover active before dry_run done")
    rg = obj.get("rollback_gate") or {}
    for k in ("deadline", "rollback_owner", "verification_criteria"):
        if k not in rg:
            errs.append(f"rollback_gate.{k} missing")

    return errs


GOOD = {'source_tool': 'jira', 'target_tool': 'linear', 'phase_state': {'discover': 'done', 'field_map': 'done', 'dry_run': 'done', 'cutover': 'in-progress', 'verify': 'pending', 'decommission': 'pending'}, 'field_map_path': './field-map.yaml', 'identity_merge_strategy': 'sso-mapping', 'rollback_gate': {'deadline': '2026-06-15T20:00:00Z', 'rollback_owner': 'U_PM', 'verification_criteria': ['parity 100%']}}
BAD = {'source_tool': 'jira', 'target_tool': 'linear', 'phase_state': {'discover': 'done'}, 'field_map_path': '', 'identity_merge_strategy': 'guess', 'rollback_gate': {}}


def self_test():
    if validate(GOOD):
        sys.stderr.write("good rejected\n"); return 1
    if not validate(BAD):
        sys.stderr.write("bad accepted\n"); return 1
    sys.stdout.write("self-test OK\n"); return 0


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
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
    try:
        obj = json.loads(p.read_text())
    except json.JSONDecodeError as e:
        sys.stderr.write(f"JSON parse error: {e}\n"); return 2
    errs = validate(obj)
    if errs:
        for e in errs:
            sys.stderr.write(f"VIOLATION: {e}\n")
        return 1
    sys.stdout.write("OK\n"); return 0


if __name__ == "__main__":
    sys.exit(main())
