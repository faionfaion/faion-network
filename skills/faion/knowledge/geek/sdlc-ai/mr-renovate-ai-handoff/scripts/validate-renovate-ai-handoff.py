#!/usr/bin/env python3
"""validate-renovate-ai-handoff.py — validate Renovate config artefact.

Inputs:
    --file PATH       path to artefact (JSON)
    --self-test       run built-in fixture (valid + invalid)
    --help            show this message

Exit codes:
    0 = valid OR self-test passed
    1 = invalid OR self-test failed
    2 = usage / unreadable input
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REQUIRED_TOP = ["extends", "packageRules", "vulnerabilityAlerts", "agent_handoff_workflow"]

VALID_FIXTURE = {
    "extends": ["config:recommended", "schedule:weekly"],
    "packageRules": [
        {"matchUpdateTypes": ["patch", "minor"], "automerge": True, "labels": []},
        {"matchUpdateTypes": ["major"], "automerge": False, "labels": ["agent-fixable"]},
    ],
    "vulnerabilityAlerts": {"labels": ["agent-fixable", "security"], "automerge": False},
    "agent_handoff_workflow": ".github/workflows/dependabot-agent-handoff.yml",
}

INVALID_FIXTURE = {
    "extends": [],
    "packageRules": [{"matchUpdateTypes": ["major"], "automerge": True}],
    "vulnerabilityAlerts": {"labels": [], "automerge": True},
}


def validate(obj) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root: must be object"]
    for k in REQUIRED_TOP:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    if "extends" in obj:
        if not isinstance(obj["extends"], list) or len(obj["extends"]) < 1:
            errs.append("extends: must be non-empty array")
    if "packageRules" in obj:
        prs = obj["packageRules"]
        if not isinstance(prs, list) or len(prs) < 2:
            errs.append("packageRules: must be array with minItems 2")
        else:
            for i, pr in enumerate(prs):
                if not isinstance(pr, dict):
                    errs.append(f"packageRules[{i}]: must be object")
                    continue
                if "matchUpdateTypes" not in pr:
                    errs.append(f"packageRules[{i}]: missing matchUpdateTypes")
                muts = pr.get("matchUpdateTypes", [])
                if "major" in muts and pr.get("automerge") is True:
                    errs.append(f"packageRules[{i}]: forbidden — major automerge=true")
    if "vulnerabilityAlerts" in obj:
        va = obj["vulnerabilityAlerts"]
        if not isinstance(va, dict):
            errs.append("vulnerabilityAlerts: must be object")
        else:
            if va.get("automerge") is not False:
                errs.append("vulnerabilityAlerts.automerge: must be false")
            labels = va.get("labels", [])
            if "agent-fixable" not in labels:
                errs.append("vulnerabilityAlerts.labels: must contain 'agent-fixable'")
    return errs


def self_test() -> int:
    errs_ok = validate(VALID_FIXTURE)
    if errs_ok:
        sys.stderr.write("self-test: VALID fixture rejected:\n  " + "\n  ".join(errs_ok) + "\n")
        return 1
    errs_bad = validate(INVALID_FIXTURE)
    if not errs_bad:
        sys.stderr.write("self-test: INVALID fixture accepted (should fail)\n")
        return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--file", type=str, help="path to artefact JSON")
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
        sys.stderr.write(f"unreadable JSON: {e}\n")
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
