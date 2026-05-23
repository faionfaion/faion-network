#!/usr/bin/env python3
"""validate-team-development.py

Validate a TeamDevelopmentReport JSON against the schema in
content/02-output-contract.xml. Stdlib-only.

Inputs:
    --file PATH       path to report JSON
    --self-test       run built-in fixtures
    --help            this message

Exit codes:
    0 = valid
    1 = invalid (violations on stderr)
    2 = usage / unreadable
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

STAGES = {"Forming", "Storming", "Norming", "Performing", "Adjourning"}
OPTIONS = ["training", "pairing", "contracting", "hiring"]
SEVERITY = {"low", "medium", "high"}
NAME_RX = re.compile(r"\b[A-Z][a-z]+\s+[A-Z][a-z]+\b")
SPRINT_RX = re.compile(r"^S[0-9]+$")


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in ("team_id", "as_of", "tuckman_stage", "tuckman_confidence",
             "tuckman_evidence", "charter", "skills_gap_plan", "themes"):
        if k not in obj:
            errs.append(f"missing required field: {k}")
    if errs:
        return errs

    if obj["tuckman_stage"] not in STAGES:
        errs.append(f"tuckman_stage must be one of {sorted(STAGES)}")
    conf = obj["tuckman_confidence"]
    if not isinstance(conf, (int, float)) or not (0.0 <= conf <= 1.0):
        errs.append("tuckman_confidence must be number in [0,1]")
    if not isinstance(obj["tuckman_evidence"], list) or len(obj["tuckman_evidence"]) < 2:
        errs.append("tuckman_evidence must have >= 2 entries (rule: tuckman-confidence-score)")

    charter = obj["charter"]
    for k in ("co_authored", "mission", "working_agreements"):
        if k not in charter:
            errs.append(f"charter.{k} missing")
    if "working_agreements" in charter and len(charter["working_agreements"]) < 3:
        errs.append("charter.working_agreements must have >= 3 entries")

    for i, gap in enumerate(obj["skills_gap_plan"]):
        for k in ("skill", "gap_severity", "gap_options_evaluated", "chosen_option",
                 "owner_role", "deadline_sprint"):
            if k not in gap:
                errs.append(f"skills_gap_plan[{i}].{k} missing"); continue
        if gap.get("gap_severity") not in SEVERITY:
            errs.append(f"skills_gap_plan[{i}].gap_severity invalid")
        opts = gap.get("gap_options_evaluated", [])
        if sorted(opts) != sorted(OPTIONS):
            errs.append(f"skills_gap_plan[{i}].gap_options_evaluated must be all 4 of {OPTIONS} (rule: training-before-hire)")
        if gap.get("chosen_option") not in OPTIONS:
            errs.append(f"skills_gap_plan[{i}].chosen_option invalid")
        if not gap.get("owner_role"):
            errs.append(f"skills_gap_plan[{i}].owner_role required (rule: retro-action-owner-deadline)")
        if not SPRINT_RX.match(str(gap.get("deadline_sprint", ""))):
            errs.append(f"skills_gap_plan[{i}].deadline_sprint must match ^S[0-9]+$")

    for i, t in enumerate(obj["themes"]):
        if "evidence_sprints" not in t or len(t["evidence_sprints"]) < 2:
            errs.append(f"themes[{i}].evidence_sprints must have >= 2 entries (rule: pattern-needs-two-sprints)")
        if "theme" not in t or not t["theme"]:
            errs.append(f"themes[{i}].theme missing")
        if NAME_RX.search(t.get("theme", "")):
            errs.append(f"themes[{i}].theme contains likely individual name (rule: no-individual-naming)")

    return errs


SMOKE_OK = {
    "team_id": "smoke", "as_of": "2026-05-23",
    "tuckman_stage": "Norming", "tuckman_confidence": 0.7,
    "tuckman_evidence": ["throughput stable", "PR SLA met"],
    "charter": {"co_authored": True, "mission": "Ship checkout",
                "working_agreements": ["a", "b", "c"]},
    "skills_gap_plan": [{"skill": "k6", "gap_severity": "high",
                         "gap_options_evaluated": ["training", "pairing", "contracting", "hiring"],
                         "chosen_option": "pairing", "owner_role": "SRE",
                         "deadline_sprint": "S14"}],
    "themes": [{"theme": "PR backlog", "evidence_sprints": ["S11", "S12"],
                "proposed_experiment": "WIP cap"}],
}
SMOKE_BAD = {"team_id": "x", "as_of": "2026-05-23",
             "tuckman_stage": "Performing", "tuckman_confidence": 0.4,
             "tuckman_evidence": ["vibes"],
             "charter": {"co_authored": True, "mission": "x", "working_agreements": ["a"]},
             "skills_gap_plan": [{"skill": "x", "gap_severity": "high",
                                  "gap_options_evaluated": ["hiring"],
                                  "chosen_option": "hiring", "owner_role": "PM",
                                  "deadline_sprint": "next"}],
             "themes": [{"theme": "Alice Smith complained",
                         "evidence_sprints": ["S13"], "proposed_experiment": "..."}]}


def self_test() -> int:
    if validate(SMOKE_OK):
        sys.stderr.write("smoke_ok rejected: " + "; ".join(validate(SMOKE_OK)) + "\n")
        return 1
    if not validate(SMOKE_BAD):
        sys.stderr.write("smoke_bad accepted\n")
        return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--file", type=str, help="path to report JSON")
    ap.add_argument("--self-test", action="store_true", help="run built-in fixtures")
    args = ap.parse_args()
    if args.self_test:
        return self_test()
    if not args.file:
        ap.print_help()
        return 2
    p = Path(args.file)
    if not p.is_file():
        sys.stderr.write(f"not a file: {p}\n"); return 2
    obj = json.loads(p.read_text())
    errs = validate(obj)
    if errs:
        for e in errs:
            sys.stderr.write(f"VIOLATION: {e}\n")
        return 1
    sys.stdout.write("OK\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
