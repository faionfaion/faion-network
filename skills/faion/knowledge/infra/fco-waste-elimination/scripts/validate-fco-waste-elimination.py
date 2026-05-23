#!/usr/bin/env python3
"""validate-fco-waste-elimination.py

Validate the artefact produced by the `fco-waste-elimination` methodology against the
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

REQUIRED = ['scope', 'idle_audit', 'schedules', 'exceptions_policy', 'automation', 'kpi_targets', 'owner', 'last_reviewed']


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


OK = json.loads("{\"scope\": {\"accounts\": [\"aws:111122223333\"], \"regions\": [\"eu-central-1\"], \"environments\": [\"dev\", \"staging\", \"qa\"]}, \"idle_audit\": [{\"resource_type\": \"ebs_volume\", \"detector\": \"status==available AND age_days>7\", \"action\": \"snapshot-then-delete\"}, {\"resource_type\": \"elastic_ip\", \"detector\": \"association==null\", \"action\": \"release\"}, {\"resource_type\": \"stopped_instance\", \"detector\": \"state==stopped AND age_days>30\", \"action\": \"terminate-with-approval\"}], \"schedules\": [{\"env\": \"dev\", \"begin\": \"08:00\", \"end\": \"20:00\", \"weekdays\": \"mon-fri\", \"timezone\": \"Europe/Warsaw\"}, {\"env\": \"staging\", \"begin\": \"06:00\", \"end\": \"22:00\", \"weekdays\": \"mon-fri\", \"timezone\": \"Europe/Warsaw\"}], \"exceptions_policy\": {\"tag_key\": \"waste-exception\", \"required_fields\": [\"reason\", \"owner\", \"expiry\"], \"expiry_days\": 90}, \"automation\": {\"scanner\": \"lambda:idle-hunter\", \"frequency\": \"weekly\", \"dry_run_default\": true, \"notification_channel\": \"slack:#finops\"}, \"kpi_targets\": {\"waste_rate_max_pct\": 25, \"untagged_max_pct\": 5, \"non_prod_savings_min_pct\": 70}, \"owner\": \"jane@team.io\", \"last_reviewed\": \"2026-05-23\"}")
BAD = json.loads("{\"scope\": null, \"owner\": \"team\"}")


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
