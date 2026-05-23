#!/usr/bin/env python3
"""validate-strangler-fig-playbook-vendor.py

Validate the artefact for strangler-fig-playbook-vendor against the schema in content/02-output-contract.xml.

Inputs:
    --file PATH       path to artefact JSON
    --self-test       run built-in fixtures (rc=0 if both pass)
    --help            this message

Exit codes:
    0 = valid (or self-test passed)
    1 = invalid
    2 = usage / unreadable
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REQUIRED = ['monolith_inventory', 'slice_scoring_table', 'cutover_runbook_per_slice', 'parity_burn_in_record', 'exit_criteria_signoff']


def validate(obj: object) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    return errs


OK_FIXTURE = '{"monolith_inventory": [{"route_or_job_name": "GET /api/products/recs", "traffic_rps": 120, "error_rate_baseline": 0.002, "p99_latency_ms_baseline": 180}], "slice_scoring_table": [{"slice_id": "S1", "coupling_depth": 2, "traffic_risk": 2, "business_priority": 4, "selection_order": 1}], "cutover_runbook_per_slice": [{"slice_id": "S1", "steps": [{"command_or_action": "shift weight 10%", "rollback_command": "shift weight 0%"}], "kill_switch_test_passed_at": "2026-05-15T10:00:00Z"}], "parity_burn_in_record": {"window_start": "2026-05-16T00:00:00Z", "window_end": "2026-05-23T00:00:00Z", "duration_hours": 168, "error_rate_delta_percent": 1.2, "p99_latency_delta_percent": 3.5}, "exit_criteria_signoff": {"legacy_5xx_for_7_days": true, "parity_within_threshold": true, "runbook_handed_off": true, "client_architect_signature_date": "2026-05-23"}}'
BAD_FIXTURE = '{"monolith_inventory": [], "slice_scoring_table": [{"slice_id": "X", "coupling_depth": 5, "traffic_risk": 5, "business_priority": 5, "selection_order": 1}], "parity_burn_in_record": {"duration_hours": 24}}'


def self_test() -> int:
    """Built-in fixtures: OK_FIXTURE accepted, BAD_FIXTURE rejected."""
    if validate(json.loads(OK_FIXTURE)):
        sys.stderr.write("self-test FAIL: valid fixture rejected\n")
        return 1
    if not validate(json.loads(BAD_FIXTURE)):
        sys.stderr.write("self-test FAIL: invalid fixture accepted\n")
        return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
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
