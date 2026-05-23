#!/usr/bin/env python3
"""validate-qa-exploratory-charter-template.py

Validate the charter + observation log + debrief artefact against the JSON
Schema in content/02-output-contract.xml.

Inputs:
    --file PATH       path to artefact JSON
    --self-test       run built-in fixtures
    --help            this message

Exit codes:
    0 = valid
    1 = invalid (violation list on stderr)
    2 = usage / unreadable input
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

TIMEBOXES = {60, 75, 90, 120}
LOG_KINDS = {"idea", "observation", "question", "bug"}
SEVERITIES = {"low", "medium", "high", "critical"}


def validate(obj) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be JSON object"]
    for k in ("charter", "observation_log", "debrief"):
        if k not in obj:
            errs.append(f"missing required top-level field: {k}")
    ch = obj.get("charter")
    if isinstance(ch, dict):
        for k in ("session_id", "date", "explorer", "mission", "target", "time_box_minutes", "focus_areas", "heuristics"):
            if k not in ch:
                errs.append(f"charter.{k} missing")
        if isinstance(ch.get("mission"), str) and len(ch["mission"]) < 20:
            errs.append("charter.mission must be at least 20 characters")
        tb = ch.get("time_box_minutes")
        if tb is not None and tb not in TIMEBOXES:
            errs.append(f"charter.time_box_minutes must be one of {sorted(TIMEBOXES)}")
        fa = ch.get("focus_areas", [])
        if isinstance(fa, list):
            if len(fa) < 3 or len(fa) > 5:
                errs.append("charter.focus_areas must have 3..5 entries")
        heur = ch.get("heuristics", [])
        if isinstance(heur, list) and len(heur) < 1:
            errs.append("charter.heuristics must have at least 1 entry")
    log = obj.get("observation_log")
    if isinstance(log, list):
        if len(log) < 5:
            errs.append("observation_log must have at least 5 entries")
        for i, e in enumerate(log):
            if not isinstance(e, dict):
                errs.append(f"observation_log[{i}] not an object")
                continue
            for k in ("timestamp", "kind", "text"):
                if k not in e:
                    errs.append(f"observation_log[{i}].{k} missing")
            if e.get("kind") and e["kind"] not in LOG_KINDS:
                errs.append(f"observation_log[{i}].kind not in {sorted(LOG_KINDS)}")
    debrief = obj.get("debrief")
    if isinstance(debrief, dict):
        for k in ("key_findings", "bugs_filed", "follow_up_questions", "debt_items", "actual_time_minutes", "published_at"):
            if k not in debrief:
                errs.append(f"debrief.{k} missing")
        kf = debrief.get("key_findings", [])
        if isinstance(kf, list):
            if len(kf) < 3 or len(kf) > 5:
                errs.append("debrief.key_findings must have 3..5 entries")
        atm = debrief.get("actual_time_minutes")
        if isinstance(atm, int) and (atm < 1 or atm > 120):
            errs.append("debrief.actual_time_minutes must be 1..120")
        for j, b in enumerate(debrief.get("bugs_filed", [])):
            if not isinstance(b, dict):
                errs.append(f"debrief.bugs_filed[{j}] not an object")
                continue
            for k in ("id", "severity", "brief"):
                if k not in b:
                    errs.append(f"debrief.bugs_filed[{j}].{k} missing")
            if b.get("severity") and b["severity"] not in SEVERITIES:
                errs.append(f"debrief.bugs_filed[{j}].severity not in {sorted(SEVERITIES)}")
    return errs


def self_test() -> int:
    good = {
        "charter": {
            "session_id": "ES-014",
            "date": "2026-05-23",
            "explorer": "Ruslan",
            "mission": "Explore the email-onboarding flow to discover failure modes in i18n, timezone, and rendering.",
            "target": "/onboarding/email/*",
            "time_box_minutes": 75,
            "focus_areas": ["i18n", "timezone", "rendering"],
            "heuristics": ["input variety"],
        },
        "observation_log": [
            {"timestamp": "14:23", "kind": "idea", "text": "try unicode emoji"},
            {"timestamp": "14:24", "kind": "observation", "text": "rendered raw"},
            {"timestamp": "14:26", "kind": "bug", "text": "filed BUG-2118"},
            {"timestamp": "14:27", "kind": "question", "text": "support tickets?"},
            {"timestamp": "14:30", "kind": "idea", "text": "API bypass"},
        ],
        "debrief": {
            "key_findings": ["theme 1", "theme 2", "theme 3"],
            "bugs_filed": [{"id": "BUG-2118", "severity": "medium", "brief": "ZWJ"}],
            "follow_up_questions": [],
            "debt_items": [],
            "actual_time_minutes": 72,
            "published_at": "2026-05-23T16:00:00Z",
        },
    }
    errs = validate(good)
    if errs:
        sys.stderr.write("self-test: good fixture rejected: " + json.dumps(errs) + "\n")
        return 1
    bad = {
        "charter": {
            "session_id": "ES-015",
            "date": "2026-05-23",
            "explorer": "Anna",
            "mission": "explore",
            "target": "/x",
            "time_box_minutes": 45,
            "focus_areas": ["a", "b"],
            "heuristics": [],
        },
        "observation_log": [],
        "debrief": {
            "key_findings": ["x", "y"],
            "bugs_filed": [],
            "follow_up_questions": [],
            "debt_items": [],
            "actual_time_minutes": 30,
            "published_at": "2026-05-25T18:00:00Z",
        },
    }
    if not validate(bad):
        sys.stderr.write("self-test: bad fixture accepted\n")
        return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("--file", type=str, help="artefact JSON to validate")
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
