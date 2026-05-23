#!/usr/bin/env python3
"""validate-journey-mapping.py - stdlib-only validator for the journey-mapping output artefact.

Inputs:
    --file PATH       path to artefact JSON
    --self-test       run built-in OK / BAD fixtures
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

REQUIRED = ["artefact_id", "owner", "version", "last_reviewed", "map_type", "persona", "scope", "stages"]
MAP_TYPES = {"current_state", "future_state", "day_in_life", "service_blueprint"}
STAGE_REQUIRED = ["name", "actions", "touchpoints", "thoughts", "emotions", "pain_points", "opportunities"]
PIPELINE_BAD = {"lead", "opportunity", "closed", "qualified", "won", "lost"}
SEMVER = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+$")
DATE = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}$")
PLURAL_OWNERS = {"team", "we", "us", "ourselves", "everyone", "the team"}


def _check_evidence_list(items, errs, where):
    if not isinstance(items, list):
        errs.append(f"{where}: must be a list")
        return
    for i, it in enumerate(items):
        if not isinstance(it, dict):
            errs.append(f"{where}[{i}]: must be object with text+evidence")
            continue
        if "text" not in it or "evidence" not in it:
            errs.append(f"{where}[{i}]: missing text or evidence field")


def validate(obj) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj or obj[k] in (None, "", []):
            errs.append(f"missing or empty required field: {k}")
    owner = obj.get("owner", "")
    if isinstance(owner, str) and owner.strip().lower() in PLURAL_OWNERS:
        errs.append("owner is plural pronoun / generic group; must be a named individual")
    v = obj.get("version", "")
    if isinstance(v, str) and v and not SEMVER.match(v):
        errs.append(f"version not semver: {v!r}")
    d = obj.get("last_reviewed", "")
    if isinstance(d, str) and d and not DATE.match(d):
        errs.append(f"last_reviewed not YYYY-MM-DD: {d!r}")
    mt = obj.get("map_type", "")
    if mt and mt not in MAP_TYPES:
        errs.append(f"map_type not in enum {sorted(MAP_TYPES)}: {mt!r}")
    scope = obj.get("scope", {})
    if isinstance(scope, dict):
        if not scope.get("start") or not scope.get("end"):
            errs.append("scope missing start or end")
    stages = obj.get("stages", [])
    if isinstance(stages, list):
        if not 4 <= len(stages) <= 8:
            errs.append(f"stages count {len(stages)} not in [4,8]")
        for i, st in enumerate(stages):
            if not isinstance(st, dict):
                errs.append(f"stages[{i}] not object")
                continue
            for k in STAGE_REQUIRED:
                if k not in st:
                    errs.append(f"stages[{i}] missing {k}")
            name = st.get("name", "")
            if isinstance(name, str) and name.strip().lower() in PIPELINE_BAD:
                errs.append(f"stages[{i}].name uses CRM pipeline term: {name!r}")
            _check_evidence_list(st.get("actions"), errs, f"stages[{i}].actions")
            _check_evidence_list(st.get("touchpoints"), errs, f"stages[{i}].touchpoints")
            _check_evidence_list(st.get("thoughts"), errs, f"stages[{i}].thoughts")
            _check_evidence_list(st.get("pain_points"), errs, f"stages[{i}].pain_points")
            emo = st.get("emotions", {})
            if isinstance(emo, dict):
                if not all(k in emo for k in ("score", "label", "evidence")):
                    errs.append(f"stages[{i}].emotions missing score/label/evidence")
                sc = emo.get("score")
                if isinstance(sc, int) and not 1 <= sc <= 5:
                    errs.append(f"stages[{i}].emotions.score out of range: {sc}")
            opps = st.get("opportunities", [])
            if isinstance(opps, list):
                for j, op in enumerate(opps):
                    if not isinstance(op, dict) or "linked_backlog_id" not in op:
                        errs.append(f"stages[{i}].opportunities[{j}] missing linked_backlog_id")
    return errs


OK_JSON = json.dumps({
    "artefact_id": "journey-shop-purchase-2026-05-23",
    "owner": "Maria Yuskiv <maria@faion.net>",
    "version": "1.0.0",
    "last_reviewed": "2026-05-23",
    "map_type": "current_state",
    "persona": "Sarah, mid-market buyer",
    "scope": {"start": "first ad impression", "end": "first product use"},
    "stages": [
        {
            "name": "Discover",
            "actions": [{"text": "sees ad", "evidence": "INT-04"}],
            "touchpoints": [{"text": "Instagram", "evidence": "ANL-1"}],
            "thoughts": [{"text": "is this for me?", "evidence": "INT-04"}],
            "emotions": {"score": 3, "label": "curious", "evidence": "INT-04"},
            "pain_points": [{"text": "no data", "evidence": "no data"}],
            "opportunities": [{"text": "tighten targeting", "linked_backlog_id": "BL-211"}],
        },
        {
            "name": "Research",
            "actions": [{"text": "reads reviews", "evidence": "INT-05"}],
            "touchpoints": [{"text": "site", "evidence": "ANL-2"}],
            "thoughts": [{"text": "is it reliable?", "evidence": "INT-05"}],
            "emotions": {"score": 4, "label": "engaged", "evidence": "INT-05"},
            "pain_points": [{"text": "missing specs", "evidence": "TKT-12"}],
            "opportunities": [{"text": "publish spec sheet", "linked_backlog_id": "BL-212"}],
        },
        {
            "name": "Decide",
            "actions": [{"text": "compares brands", "evidence": "INT-06"}],
            "touchpoints": [{"text": "site", "evidence": "ANL-3"}],
            "thoughts": [{"text": "best value?", "evidence": "INT-06"}],
            "emotions": {"score": 3, "label": "weighing", "evidence": "INT-06"},
            "pain_points": [{"text": "unclear comparison", "evidence": "INT-06"}],
            "opportunities": [{"text": "comparison module", "linked_backlog_id": "BL-213"}],
        },
        {
            "name": "Purchase",
            "actions": [{"text": "checks out", "evidence": "ANL-4"}],
            "touchpoints": [{"text": "checkout", "evidence": "ANL-4"}],
            "thoughts": [{"text": "what is total?", "evidence": "INT-07"}],
            "emotions": {"score": 2, "label": "anxious", "evidence": "INT-07"},
            "pain_points": [{"text": "hidden fees late", "evidence": "INT-07"}],
            "opportunities": [{"text": "early fee breakdown", "linked_backlog_id": "BL-214"}],
        },
    ],
})
BAD_JSON = json.dumps({
    "owner": "the team",
    "map_type": "best_guess",
    "persona": "general",
    "scope": {"start": "x"},
    "stages": [{"name": "Lead"}],
})


def self_test() -> int:
    ok = json.loads(OK_JSON)
    if validate(ok):
        sys.stderr.write("self-test FAIL: OK rejected: " + repr(validate(ok)) + "\n")
        return 1
    bad = json.loads(BAD_JSON)
    if not validate(bad):
        sys.stderr.write("self-test FAIL: BAD accepted\n")
        return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("--file", type=str, help="artefact JSON file to validate")
    ap.add_argument("--self-test", action="store_true", help="run built-in OK / BAD fixtures")
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
        sys.stderr.write(f"not valid JSON: {e}\n")
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
