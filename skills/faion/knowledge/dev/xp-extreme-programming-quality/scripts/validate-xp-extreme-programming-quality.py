#!/usr/bin/env python3
"""validate-xp-extreme-programming.py

Validate an XP readiness checklist JSON against schema + adoption-phase rule.

Inputs:
    --file PATH      path to checklist JSON
    --self-test      run built-in valid + invalid fixtures
    --help           this message

Exit codes:
    0 = valid
    1 = invalid (violation list printed to stderr)
    2 = usage / unreadable file
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ID_RE = re.compile(r"^xp-[a-z0-9-]{6,}$")
VER_RE = re.compile(r"^\d+\.\d+\.\d+$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
PRACTICES = ("tdd", "ci", "small_releases", "refactor", "simple_design", "pair_programming", "collective_ownership", "coding_standards", "metaphor", "planning_game", "on_site_customer", "sustainable_pace")
SUBSTRATE = ("tdd", "ci", "small_releases")
FLOW = ("refactor", "simple_design", "sustainable_pace")
CRAFT = ("pair_programming", "collective_ownership", "metaphor", "planning_game", "on_site_customer")
PHASES = {"phase-1-substrate", "phase-2-flow", "phase-3-craft", "complete"}
VERDICTS = {"phase-1", "phase-2", "phase-3", "block-substrate-missing", "block-org-hostile"}


def avg(scores):
    return sum(scores) / max(len(scores), 1)


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    for k in ("artefact_id", "team", "practices", "phase", "verdict", "version", "last_reviewed"):
        if k not in obj:
            errs.append(f"missing required field: {k}")

    if "artefact_id" in obj and not ID_RE.match(str(obj["artefact_id"])):
        errs.append("artefact_id must match ^xp-[a-z0-9-]{6,}$")

    pr = obj.get("practices") or {}
    if not isinstance(pr, dict):
        errs.append("practices must be an object")
    else:
        for p in PRACTICES:
            block = pr.get(p)
            if not isinstance(block, dict):
                errs.append(f"practices.{p} missing or not object")
                continue
            for sub in ("score", "evidence"):
                if sub not in block:
                    errs.append(f"practices.{p}.{sub} missing")
            sc = block.get("score")
            if not isinstance(sc, int) or not (0 <= sc <= 5):
                errs.append(f"practices.{p}.score must be int in [0,5]")
            ev = block.get("evidence")
            if not isinstance(ev, str) or len(ev) < 5:
                errs.append(f"practices.{p}.evidence must be non-empty string")

    if obj.get("phase") not in PHASES:
        errs.append(f"phase must be one of {sorted(PHASES)}")
    verdict = obj.get("verdict")
    if verdict and verdict not in VERDICTS:
        errs.append(f"verdict must be one of {sorted(VERDICTS)}")

    # Consistency: if verdict claims phase-3, substrate must be green AND done wired.
    if isinstance(pr, dict) and all(p in pr and isinstance(pr[p].get("score"), int) for p in PRACTICES):
        substrate_avg = avg([pr[p]["score"] for p in SUBSTRATE])
        flow_avg = avg([pr[p]["score"] for p in FLOW])
        if verdict == "phase-3":
            if substrate_avg < 3 or flow_avg < 3:
                errs.append("verdict=phase-3 requires substrate avg >= 3 AND flow avg >= 3")
            if not obj.get("done_definition_wired"):
                errs.append("verdict=phase-3 requires done_definition_wired=true")
        if verdict == "phase-2" and substrate_avg < 3:
            errs.append("verdict=phase-2 requires substrate avg >= 3")
        if any(pr[p]["score"] < 3 for p in SUBSTRATE) and verdict == "phase-3":
            errs.append("any substrate practice score < 3 blocks verdict=phase-3 (r7)")

    if "version" in obj and not VER_RE.match(str(obj["version"])):
        errs.append("version must be semver MAJOR.MINOR.PATCH")
    if "last_reviewed" in obj and not DATE_RE.match(str(obj["last_reviewed"])):
        errs.append("last_reviewed must be ISO date YYYY-MM-DD")
    return errs


def _practice(score, ev="evidence string"):
    return {"score": score, "evidence": ev}


VALID_FIXTURE = {
    "artefact_id": "xp-faion-net",
    "team": "faion-net",
    "practices": {
        "tdd": _practice(4), "ci": _practice(5), "small_releases": _practice(4),
        "refactor": _practice(3), "simple_design": _practice(4), "sustainable_pace": _practice(4),
        "pair_programming": _practice(2), "collective_ownership": _practice(3),
        "coding_standards": _practice(5), "metaphor": _practice(2),
        "planning_game": _practice(3), "on_site_customer": _practice(2),
    },
    "done_definition_wired": True,
    "phase": "phase-3-craft",
    "verdict": "phase-3",
    "version": "1.0.0",
    "last_reviewed": "2026-05-23",
}

INVALID_FIXTURE = {
    "artefact_id": "xp",
    "team": "team",
    "practices": {"tdd": {"score": 9}},
    "phase": "phase-3-craft",
    "verdict": "phase-3",
    "version": "1.0",
    "last_reviewed": "today",
}


def self_test() -> int:
    errs = validate(VALID_FIXTURE)
    if errs:
        sys.stderr.write(f"self-test FAILED: valid fixture rejected: {errs}\n")
        return 1
    errs = validate(INVALID_FIXTURE)
    if not errs:
        sys.stderr.write("self-test FAILED: invalid fixture accepted\n")
        return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--file", type=str, help="path to checklist JSON")
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
