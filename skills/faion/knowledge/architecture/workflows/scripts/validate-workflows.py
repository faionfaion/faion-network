#!/usr/bin/env python3
"""validate-workflows.py

Validate a workflow-instance artefact against the schema declared in
content/02-output-contract.xml.

Inputs:
    --file PATH       path to workflow-instance JSON
    --self-test       run built-in fixtures (OK + BAD)
    --help            this message

Exit codes:
    0 = valid
    1 = invalid
    2 = usage / unreadable
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

INSTANCE_ID_RE = re.compile(r"^WF-[0-9]{3,5}$")
WORKFLOW_TYPES = {"system-design", "architecture-review", "adr", "tech-eval", "atam-cbam", "strangler-migration", "design-doc-review"}
ROLES = {"clarifier", "designer", "critic", "documenter", "stakeholder"}
FORMATS = {"md", "xml", "json", "yaml", "drawio", "pdf"}
DECISION_TYPES = {"type-1", "type-2", "none"}


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in ("instance_id", "workflow_type", "trigger", "abort_condition", "steps"):
        if k not in obj:
            errs.append(f"missing required field: {k}")

    if "instance_id" in obj and not INSTANCE_ID_RE.match(str(obj["instance_id"])):
        errs.append(f"instance_id must match ^WF-[0-9]{{3,5}}$: got {obj['instance_id']!r}")
    if obj.get("workflow_type") not in WORKFLOW_TYPES:
        errs.append(f"workflow_type must be one of canonical 7: got {obj.get('workflow_type')!r}")

    abort = obj.get("abort_condition", "")
    if len(abort) < 8:
        errs.append(f"abort_condition too short (<8 chars): {len(abort)}")

    steps = obj.get("steps") or []
    if not (isinstance(steps, list) and len(steps) >= 2):
        errs.append("steps must be a list with >=2 entries")
    role_to_names: dict[str, set[str]] = {}
    for i, s in enumerate(steps if isinstance(steps, list) else []):
        if not isinstance(s, dict):
            errs.append(f"steps[{i}] not an object")
            continue
        for k in ("n", "name", "role", "artefact_path", "artefact_format", "review_gate"):
            if k not in s:
                errs.append(f"steps[{i}] missing {k}")
        if s.get("role") not in ROLES:
            errs.append(f"steps[{i}].role must be in {sorted(ROLES)}: got {s.get('role')!r}")
        if s.get("artefact_format") not in FORMATS:
            errs.append(f"steps[{i}].artefact_format must be in {sorted(FORMATS)}: got {s.get('artefact_format')!r}")
        if not s.get("artefact_path"):
            errs.append(f"steps[{i}].artefact_path is empty")
        dt = s.get("decision_type", "none")
        if dt not in DECISION_TYPES:
            errs.append(f"steps[{i}].decision_type must be in {sorted(DECISION_TYPES)}: got {dt!r}")
        if dt == "type-1":
            if not s.get("review_gate"):
                errs.append(f"steps[{i}] type-1 decision without review_gate=true (review-gate-on-decision)")
            if not s.get("reviewer"):
                errs.append(f"steps[{i}] type-1 decision without named reviewer")
        # collect role-name pairs (use 'reviewer' as proxy if no explicit owner field)
        owner = s.get("owner") or s.get("reviewer") or s.get("role")
        if isinstance(owner, str):
            role_to_names.setdefault(s.get("role", "?"), set()).add(owner)

    # role-overload: if total steps >= 4, require >= 2 distinct human names overall
    if isinstance(steps, list) and len(steps) >= 4:
        all_names = set().union(*role_to_names.values()) if role_to_names else set()
        if len(all_names) < 2:
            errs.append("role-overload: workflow with >=4 steps needs >=2 distinct names")

    return errs


OK = {
    "instance_id": "WF-0042",
    "workflow_type": "atam-cbam",
    "trigger": "Monolith vs microservices for Phase 3 scale-up",
    "abort_condition": "Stakeholder map cannot be assembled within 2 working days",
    "steps": [
        {"n": 1, "name": "scope-utility-tree", "role": "clarifier", "owner": "alice", "artefact_path": "atam/utility-tree.md", "artefact_format": "md", "review_gate": False, "decision_type": "none"},
        {"n": 2, "name": "score-options", "role": "designer", "owner": "bob", "artefact_path": "atam/scorecard.json", "artefact_format": "json", "review_gate": True, "reviewer": "lead-architect", "decision_type": "type-1"},
        {"n": 3, "name": "write-adr", "role": "documenter", "owner": "alice", "artefact_path": "adr/ADR-0031.md", "artefact_format": "md", "review_gate": True, "reviewer": "ceo", "decision_type": "type-1"},
        {"n": 4, "name": "communicate", "role": "stakeholder", "owner": "ceo", "artefact_path": "comms/briefing.md", "artefact_format": "md", "review_gate": False, "decision_type": "none"},
    ],
}

BAD = {
    "instance_id": "WF-1",
    "workflow_type": "freestyle",
    "trigger": "x",
    "abort_condition": "x",
    "steps": [{"n": 1, "name": "think", "role": "team", "artefact_path": "", "artefact_format": "md", "review_gate": False, "decision_type": "type-1"}],
}


def self_test() -> int:
    errs_ok = validate(OK)
    if errs_ok:
        sys.stderr.write(f"OK fixture rejected: {errs_ok}\n")
        return 1
    if not validate(BAD):
        sys.stderr.write("BAD fixture accepted\n")
        return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--file", type=str, help="path to workflow-instance JSON")
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
    except Exception as e:
        sys.stderr.write(f"cannot parse JSON: {e}\n")
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
