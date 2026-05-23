#!/usr/bin/env python3
"""validate-gha-deployment-patterns.py

Validate the artefact produced by the `gha-deployment-patterns` methodology against the
JSON Schema embedded in `content/02-output-contract.xml`.

This validator uses stdlib only (no pyyaml/pydantic) for portability.

Inputs:
    --file PATH       path to artefact (JSON)
    --self-test       run built-in fixtures
    --help            this message

Exit codes:
    0 = valid
    1 = invalid (violation list printed to stderr)
    2 = usage / unreadable
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REQUIRED = ['environments', 'reusable_workflow_ref', 'strategy', 'release_automation', 'owner', 'last_reviewed']


def validate(obj) -> list:
    errs = []
    if not isinstance(obj, dict):
        return ["root must be JSON object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
            continue
        v = obj[k]
        if v in (None, "", [], {}):
            errs.append(f"required field empty: {k}")
        if isinstance(v, str) and v.strip().upper() in {"TBD", "TODO", "FIXME"}:
            errs.append(f"placeholder value in field: {k}")
    owner = obj.get("owner")
    if isinstance(owner, str) and owner.lower().strip() in {"team", "we", "tbd"}:
        errs.append("owner must be a single named person, not 'team' / 'we' / 'TBD'")
    return errs


OK = json.loads("{\"environments\": [{\"name\": \"staging\", \"url\": \"https://staging.acme.io\", \"approvers\": [], \"branch_filter\": \"main\"}, {\"name\": \"production\", \"url\": \"https://acme.io\", \"approvers\": [\"release-captain@team.io\"], \"branch_filter\": \"main\"}], \"reusable_workflow_ref\": {\"uses\": \"acme/cd-library/.github/workflows/deploy.yml\", \"version_tag\": \"v2.4.0\"}, \"strategy\": {\"type\": \"canary\", \"rollout_steps\": [\"10%\", \"50%\", \"100%\"], \"rollback_gate\": {\"metric\": \"http_5xx_ratio\", \"threshold\": 0.02, \"window_minutes\": 5}}, \"release_automation\": {\"tag_pattern\": \"v{major}.{minor}.{patch}\", \"changelog_generator\": \"release-drafter\", \"release_artifacts\": [\"binary\", \"sbom\"]}, \"owner\": \"cd-lead@team.io\", \"last_reviewed\": \"2026-05-23\"}")
BAD = json.loads("{\"environments\": null, \"owner\": \"team\"}")


def self_test() -> int:
    errs_ok = validate(OK)
    if errs_ok:
        sys.stderr.write(f"valid fixture rejected: {errs_ok}\n")
        return 1
    errs_bad = validate(BAD)
    if not errs_bad:
        sys.stderr.write("invalid fixture accepted\n")
        return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("--file", type=str, help="artefact JSON path")
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
