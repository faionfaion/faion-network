#!/usr/bin/env python3
"""validate-jira-workflow-management.py

Validate a config artefact for Jira Workflow Management against the schema in
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

REQUIRED = ['site', 'project_key', 'workflow_yaml_path', 'saved_filters', 'automation_rules', 'token_scope']


def validate(obj):
    errs = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    import re
    if not re.match(r"^[a-z0-9-]+\.atlassian\.net$", str(obj.get("site", ""))):
        errs.append(f"site domain invalid: {obj.get('site')!r}")
    if not re.match(r"^[A-Z][A-Z0-9]+$", str(obj.get("project_key", ""))):
        errs.append(f"project_key invalid: {obj.get('project_key')!r}")
    if not obj.get("workflow_yaml_path"):
        errs.append("workflow_yaml_path empty")
    sf = obj.get("saved_filters") or []
    if not sf:
        errs.append("saved_filters must not be empty")
    for i, r in enumerate(obj.get("automation_rules") or []):
        for k in ("name", "scope", "rate_limit_per_min"):
            if k not in r:
                errs.append(f"automation_rules[{i}].{k} missing")
    ts = obj.get("token_scope") or {}
    scopes = ts.get("scopes") or []
    if any(s.startswith("admin") or "manage:jira" in s for s in scopes):
        errs.append("token scope contains admin/manage:jira")
    exp = ts.get("expiry_days")
    if not isinstance(exp, int) or not (7 <= exp <= 365):
        errs.append(f"expiry_days invalid: {exp!r}")

    return errs


GOOD = {'site': 'acme.atlassian.net', 'project_key': 'PLAT', 'workflow_yaml_path': './wf.yaml', 'saved_filters': [{'name': 'active', 'jql': 'x'}], 'automation_rules': [{'name': 'r1', 'scope': 'project', 'rate_limit_per_min': 60}], 'token_scope': {'scopes': ['read:jira-work'], 'expiry_days': 90}}
BAD = {'site': 'acme.com', 'project_key': 'p', 'workflow_yaml_path': '', 'saved_filters': [], 'automation_rules': [{'name': 'x'}], 'token_scope': {'scopes': ['admin'], 'expiry_days': 9999}}


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
