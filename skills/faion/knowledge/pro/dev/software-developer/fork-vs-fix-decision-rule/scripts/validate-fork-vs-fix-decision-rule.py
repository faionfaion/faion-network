#!/usr/bin/env python3
"""validate-fork-vs-fix-decision-rule.py

Validate a FixDecision JSON against the schema in 02-output-contract.xml.

Inputs:
    --file PATH       artefact JSON
    --self-test       run built-in fixtures
    --help            this message

Exit codes:
    0 valid · 1 invalid · 2 usage / unreadable
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REQUIRED = [
    "decision_id",
    "library",
    "axes",
    "total_score",
    "action",
    "strategic_override_applied",
    "ban_list_blocked",
    "rollback_plan",
]
UUID_RE = re.compile(r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$")
AXIS_NAMES = {"urgency", "blast", "patch_size", "upstream_responsiveness", "strategic_dependency"}
ACTIONS = {"workaround", "monkey_patch", "upstream_pr", "fork_pin", "replace"}
BAN_LIST_HINT = {"next-auth", "passport", "openssl", "react-dom", "next", "django", "rails-core"}


def _band(total: int) -> str:
    if total <= 3:
        return "workaround"
    if total <= 6:
        return "monkey_patch"
    if total <= 9:
        return "upstream_pr"
    if total <= 12:
        return "fork_pin"
    return "replace"


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    if "decision_id" in obj and not UUID_RE.match(str(obj["decision_id"])):
        errs.append("decision_id must be UUID")
    axes = obj.get("axes") or []
    if len(axes) != 5:
        errs.append("axes must have exactly 5 entries (5-axis score)")
    score_sum = 0
    score_by_name: dict[str, int] = {}
    for a in axes:
        n = a.get("name")
        s = a.get("score")
        if n not in AXIS_NAMES:
            errs.append(f"axis name '{n}' must be one of {sorted(AXIS_NAMES)}")
        if not isinstance(s, int) or s < 0 or s > 3:
            errs.append(f"axis '{n}' score must be int in [0,3]")
        else:
            score_sum += s
            score_by_name[n] = s
    if "total_score" in obj and score_by_name and obj["total_score"] != score_sum:
        errs.append(f"total_score {obj['total_score']} != sum(axes) {score_sum}")
    action = obj.get("action")
    if action not in ACTIONS:
        errs.append(f"action must be one of {sorted(ACTIONS)}")
    if isinstance(obj.get("total_score"), int) and action and action in ACTIONS:
        expected = _band(obj["total_score"])
        if expected != action and not obj.get("strategic_override_applied"):
            errs.append(f"action '{action}' does not match band '{expected}' for total {obj['total_score']}")
    if score_by_name.get("strategic_dependency") == 3 and action in {"workaround", "monkey_patch"}:
        errs.append("strategic_dependency=3 requires action >= upstream_pr (r3 override)")
    lib_name = (obj.get("library") or {}).get("name", "")
    if any(b in str(lib_name).lower() for b in BAN_LIST_HINT) and action == "monkey_patch":
        errs.append(f"library '{lib_name}' is on the monkey-patch ban list (r5)")
    if action == "fork_pin" and not str(obj.get("sunset_criterion", "")).strip():
        errs.append("fork_pin requires non-empty sunset_criterion (r4 fork-hygiene)")
    if len(str(obj.get("rollback_plan", "")).strip()) < 10:
        errs.append("rollback_plan must be non-empty (>=10 chars)")
    return errs


OK = {
    "decision_id": "9b6c0a4e-3a44-4f3a-8a9d-1f0e1234ffff",
    "library": {
        "name": "n8n",
        "ecosystem": "npm",
        "current_version": "1.42.0",
        "bug_summary": "custom node loader does not support python-via-child_process",
        "repro_link": "https://github.com/faionfaion/n8n/issues/1",
    },
    "axes": [
        {"name": "urgency", "score": 2},
        {"name": "blast", "score": 3},
        {"name": "patch_size", "score": 2},
        {"name": "upstream_responsiveness", "score": 2},
        {"name": "strategic_dependency", "score": 3},
    ],
    "total_score": 12,
    "action": "fork_pin",
    "action_playbook_url": "decisions/2026-05-23-n8n-fork.md",
    "strategic_override_applied": True,
    "ban_list_blocked": False,
    "sunset_criterion": "when upstream PR merges OR by 2027-Q1",
    "rollback_plan": "drop fork pin; revert to public n8n with python loader workaround",
    "decided_by": "ruslan@faion.net",
    "decided_at": "2026-05-23T14:00:00Z",
}
BAD = {
    "decision_id": "not-a-uuid",
    "library": {"name": "next-auth", "ecosystem": "npm", "current_version": "5.0.0", "bug_summary": "tok exp 30s off", "repro_link": "n/a"},
    "axes": [{"name": "urgency", "score": 5}],
    "total_score": 4,
    "action": "monkey_patch",
    "strategic_override_applied": False,
    "ban_list_blocked": False,
    "rollback_plan": "",
}


def self_test() -> int:
    if validate(OK):
        sys.stderr.write("ok rejected\n")
        return 1
    if not validate(BAD):
        sys.stderr.write("bad accepted\n")
        return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
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
