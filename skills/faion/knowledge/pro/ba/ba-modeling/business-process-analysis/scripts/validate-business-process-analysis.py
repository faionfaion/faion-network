#!/usr/bin/env python3
"""validate-business-process-analysis.py

Validate a business-process-analysis report (JSON) against 02-output-contract.xml.

Inputs:
    --file PATH       path to report JSON
    --self-test       run built-in fixtures
    --help            this message

Exit codes:
    0 = valid
    1 = invalid (violations to stderr)
    2 = usage / unreadable
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ACTIONS = {"keep", "cut", "change", "add"}
CHANNELS = {"pr_comment", "email", "slack_ack"}
ANON_OWNERS = {"team", "ops", "client", "the client", "ops team", "client team", "?", ""}


def validate(obj: object) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in ("process_id", "current_state", "analysis", "future_state", "signoffs"):
        if k not in obj:
            errs.append(f"missing required field: {k}")
    cs = obj.get("current_state", {})
    steps = cs.get("steps", []) if isinstance(cs, dict) else []
    lanes = cs.get("lanes", []) if isinstance(cs, dict) else []
    if not steps:
        errs.append("current_state.steps must be non-empty")
    if not lanes:
        errs.append("current_state.lanes must be non-empty")
    step_ids: set[str] = set()
    for i, s in enumerate(steps):
        if not isinstance(s, dict):
            errs.append(f"steps[{i}] must be object"); continue
        for f in ("id", "lane", "description", "source"):
            if f not in s:
                errs.append(f"steps[{i}] missing {f} (rule r1)")
        if not (s.get("source") or "").strip():
            errs.append(f"steps[{i}] empty source (rule r1)")
        step_ids.add(s.get("id", ""))
    for i, l in enumerate(lanes):
        if not isinstance(l, dict):
            errs.append(f"lanes[{i}] must be object"); continue
        owner = (l.get("owner_name", "") or "").strip().lower()
        if not owner or owner in ANON_OWNERS or len(owner.split()) < 2:
            errs.append(f"lanes[{i}] anonymous owner_name '{l.get('owner_name')}' (rule r2)")
    analysis = obj.get("analysis", [])
    if not analysis:
        errs.append("analysis must be non-empty (rule r3)")
    for i, a in enumerate(analysis):
        for f in ("step_id", "value_add", "cycle_time_min", "cost_usd"):
            if f not in a:
                errs.append(f"analysis[{i}] missing {f} (rule r3)")
    fs = obj.get("future_state", [])
    if not fs:
        errs.append("future_state must be non-empty diff (rule r4)")
    for i, f in enumerate(fs):
        if f.get("action") not in ACTIONS:
            errs.append(f"future_state[{i}].action must be one of {sorted(ACTIONS)} (rule r4)")
        if not (f.get("expected_delta") or "").strip():
            errs.append(f"future_state[{i}].expected_delta missing (rule r4)")
        if step_ids and f.get("step_id") not in step_ids and f.get("action") != "add":
            errs.append(f"future_state[{i}].step_id '{f.get('step_id')}' not in current_state.steps (rule r4)")
    signoffs = obj.get("signoffs", [])
    lane_names = {l.get("name") for l in lanes if isinstance(l, dict)}
    covered = {s.get("lane") for s in signoffs if isinstance(s, dict)}
    missing = lane_names - covered
    if missing:
        errs.append(f"signoffs missing lanes: {sorted(missing)} (rule r5)")
    for i, s in enumerate(signoffs):
        if s.get("channel") not in CHANNELS:
            errs.append(f"signoffs[{i}].channel must be one of {sorted(CHANNELS)} (rule r5)")
    return errs


OK_FIXTURE = {
    "process_id": "invoice-approval",
    "current_state": {
        "steps": [{"id": "s-01", "lane": "AP", "description": "Receive email", "source": "ops/sop.md#L8"}],
        "lanes": [{"name": "AP", "owner_name": "Maria Lopes", "owner_role": "AP Lead"}],
    },
    "analysis": [{"step_id": "s-01", "value_add": False, "cycle_time_min": 5, "cost_usd": 1.2}],
    "future_state": [{"step_id": "s-01", "action": "change", "expected_delta": "Mailgun webhook; -4 min"}],
    "signoffs": [{"lane": "AP", "owner_name": "Maria Lopes", "signoff_ts": "2026-05-23T10:00:00Z", "channel": "pr_comment"}],
}
BAD_FIXTURE = {
    "process_id": "x",
    "current_state": {"steps": [{"id": "s-01", "lane": "x", "description": "y", "source": ""}],
                      "lanes": [{"name": "Ops", "owner_name": "Team", "owner_role": "?"}]},
    "analysis": [],
    "future_state": [{"step_id": "s-01", "action": "automate", "expected_delta": ""}],
    "signoffs": [],
}


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
