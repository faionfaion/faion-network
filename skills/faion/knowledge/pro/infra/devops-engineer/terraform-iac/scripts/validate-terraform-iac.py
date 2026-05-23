#!/usr/bin/env python3
"""validate-terraform-iac.py

Validate an artefact produced by the Terraform IaC methodology
against the JSON Schema declared in content/02-output-contract.xml.

Inputs:
    --file PATH       path to the artefact JSON file
    --self-test       run built-in fixtures (OK + BAD) and exit 0 on pass
    --help            this message

Exit codes:
    0 = valid (or self-test pass)
    1 = invalid (or self-test fail)
    2 = usage / unreadable
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REQUIRED = ['blast_radius_doc_path', 'cross_workspace_pattern', 'module_sources', 'refactor_method', 'repo_layout', 'workspaces']


def validate(obj: dict) -> list:
    errs = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    return errs


OK = {'repo_layout': 'monorepo', 'workspaces': [{'env': 'prod', 'layer': 'network', 'state_backend': 's3://acme-tfstate/prod-network'}, {'env': 'prod', 'layer': 'app', 'state_backend': 's3://acme-tfstate/prod-app'}], 'module_sources': [{'source': 'registry.acme/vpc', 'version': '2.1.0'}], 'cross_workspace_pattern': 'remote_state', 'refactor_method': 'moved_block', 'blast_radius_doc_path': 'envs/prod/network/README.md'}
BAD = {'repo_layout': 'monorepo', 'workspaces': [{'env': 'all', 'layer': 'all', 'state_backend': 's3://acme-tfstate/everything'}], 'module_sources': [{'source': '../modules/vpc', 'version': 'inline'}], 'refactor_method': 'state_rm'}


def self_test() -> int:
    errs_ok = validate(OK)
    if errs_ok:
        sys.stderr.write(f"self-test FAIL: OK fixture rejected: {errs_ok}\n")
        return 1
    errs_bad = validate(BAD)
    if not errs_bad:
        sys.stderr.write("self-test FAIL: BAD fixture accepted\n")
        return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--file", type=str, help="artefact JSON file to validate")
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
        return 1
    errs = validate(obj)
    if errs:
        for e in errs:
            sys.stderr.write(f"VIOLATION: {e}\n")
        return 1
    sys.stdout.write("OK\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
