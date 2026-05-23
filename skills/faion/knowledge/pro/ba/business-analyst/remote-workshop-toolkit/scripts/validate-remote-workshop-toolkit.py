#!/usr/bin/env python3
"""validate-remote-workshop-toolkit.py

Validate a config artefact produced by the remote-workshop-toolkit methodology
against the JSON Schema captured in content/02-output-contract.xml.

stdlib-only. Inputs / outputs / exit codes documented under --help.

Inputs:
    --file PATH       path to artefact JSON
    --self-test       run built-in fixture
    --help            this message

Exit codes:
    0 = valid
    1 = invalid
    2 = usage / unreadable
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REQUIRED = ['workshop_id', 'objective', 'agenda', 'pre_read', 'ground_rules', 'breakouts', 'canvas_links', 'time_zones', 'async_pulses', 'decision_log']


def validate(obj) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be a JSON object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    return errs


OK = json.loads('{"workshop_id": "ws-2026-05-23-process-map", "objective": "Build to-be process map for invoice exception handling with sign-off-ready BPMN draft", "agenda": [{"block": "Opening", "duration_min": 10, "mode": "plenary", "deliverable": "ground-rules ack"}], "pre_read": {"url": "https://wiki/ws/pre-read", "sent_at": "2026-05-21T09:00:00Z", "acknowledgement_threshold": 0.7, "acknowledgement_rate": 0.82}, "ground_rules": {"camera_policy": "on for plenary", "mic_policy": "on in breakouts \\u22646", "chat_use": "questions + side-notes", "hand_raise": "tool-native"}, "breakouts": [{"facilitator": "BA", "timekeeper": "PM", "scribe": "Ops lead", "canvas_frame": "frame-1", "deliverable_definition": "exception path bpmn draft", "read_out_template": "3-bullet summary"}], "canvas_links": [{"tool": "miro", "url": "https://miro/abc", "template_id": "process-map"}], "time_zones": {"zones": ["UTC+1", "UTC-5"], "working_hours_coverage_pct": 0.85, "split_decision": "single session"}, "async_pulses": [{"window": "T-24h", "questions": ["What is the worst exception you saw last month?"], "response_rate_threshold": 0.6}], "decision_log": []}')
BAD = json.loads('{"workshop_id": "x", "objective": "do stuff"}')


def self_test() -> int:
    if validate(OK):
        sys.stderr.write("self-test FAIL: good fixture rejected\n")
        return 1
    if not validate(BAD):
        sys.stderr.write("self-test FAIL: bad fixture accepted\n")
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
        obj = json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        sys.stderr.write(f"VIOLATION: invalid JSON: {e}\n")
        return 1
    errs = validate(obj)
    if errs:
        for e in errs:
            sys.stderr.write(f"VIOLATION: {e}\n")
        return 1
    sys.stdout.write("OK\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
