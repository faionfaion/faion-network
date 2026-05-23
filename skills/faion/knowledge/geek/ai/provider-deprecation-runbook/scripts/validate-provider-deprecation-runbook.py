#!/usr/bin/env python3
"""Validate provider-deprecation-runbook artefact.

USAGE:
    validate-provider-deprecation-runbook.py <input.json>
    validate-provider-deprecation-runbook.py --self-test
    validate-provider-deprecation-runbook.py --help

EXIT CODES:
    0 valid
    1 schema violation
    2 usage / unreadable

NO EXTERNAL DEPS — stdlib only.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

SEMVER_RE = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+$")
DATE_RE = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}$")
FORBIDDEN_OWNERS = {"team", "we", "us", "engineering", ""}
FORBIDDEN_ACTORS = {"someone", "somebody", "the team", "they", "we"}


def validate(s: dict) -> list[str]:
    v: list[str] = []
    if not isinstance(s, dict):
        return ["root must be object"]
    for k in ("artefact_id", "owner", "on_call", "deprecation_date", "phases", "version", "last_reviewed"):
        if k not in s:
            v.append(f"missing required field: {k}")
    owner = (s.get("owner") or "").strip().lower()
    if owner in FORBIDDEN_OWNERS:
        v.append(f"owner forbidden value {owner!r} (rule r5)")
    if not (s.get("on_call") or "").strip():
        v.append("on_call required (rule r5)")
    if not DATE_RE.match(s.get("deprecation_date", "") or ""):
        v.append("deprecation_date must be ISO YYYY-MM-DD")
    phases = s.get("phases")
    if not isinstance(phases, list) or len(phases) < 1:
        v.append("phases must be non-empty list")
    if isinstance(phases, list):
        for i, ph in enumerate(phases):
            if not isinstance(ph, dict):
                v.append(f"phases[{i}] must be object")
                continue
            bm = ph.get("budget_min")
            if not isinstance(bm, int) or bm < 1 or bm > 720:
                v.append(f"phases[{i}].budget_min must be int in [1,720] (rule r3)")
            steps = ph.get("steps")
            if not isinstance(steps, list) or len(steps) < 1:
                v.append(f"phases[{i}].steps must be non-empty list")
                continue
            for j, st in enumerate(steps):
                if not isinstance(st, dict):
                    v.append(f"phases[{i}].steps[{j}] must be object")
                    continue
                actor = (st.get("actor") or "").strip().lower()
                if not actor or actor in FORBIDDEN_ACTORS:
                    v.append(f"phases[{i}].steps[{j}].actor must be named (rule r1)")
                if not (st.get("action") or "").strip():
                    v.append(f"phases[{i}].steps[{j}].action required")
                if not (st.get("artefact") or "").strip():
                    v.append(f"phases[{i}].steps[{j}].artefact required")
                if not (st.get("rollback") or st.get("stop_branch") or "").strip():
                    v.append(f"phases[{i}].steps[{j}] needs rollback or stop_branch (rule r2)")
    if not SEMVER_RE.match(s.get("version", "") or ""):
        v.append("version must be semver")
    if not DATE_RE.match(s.get("last_reviewed", "") or ""):
        v.append("last_reviewed must be ISO YYYY-MM-DD")
    return v


GOOD = {
    "artefact_id": "deprecate-claude-opus-3x-2026-09",
    "owner": "ruslan@faion.net",
    "on_call": "ml-oncall-rotation",
    "deprecation_date": "2026-09-01",
    "phases": [{
        "name": "canary",
        "budget_min": 60,
        "steps": [{"id": "s1", "actor": "ml-engineer:platform", "action": "flip 1%", "artefact": "url", "rollback": "set 0%"}],
    }],
    "version": "1.0.0",
    "last_reviewed": "2026-05-22",
}
BAD = {
    "artefact_id": "x",
    "owner": "team",
    "on_call": "",
    "deprecation_date": "soon",
    "phases": [{"name": "canary", "steps": [{"id": "s1", "actor": "someone", "action": "do it", "artefact": "x"}]}],
    "version": "v1",
    "last_reviewed": "yesterday",
}


def _self_test() -> int:
    assert validate(GOOD) == [], f"happy failed: {validate(GOOD)}"
    bad = validate(BAD)
    assert any("budget_min" in x for x in bad)
    assert any("actor" in x for x in bad)
    assert any("rollback" in x for x in bad)
    sys.stdout.write("self-test PASSED\n")
    return 0


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(prog="validate-provider-deprecation-runbook.py")
    p.add_argument("path", nargs="?")
    p.add_argument("--self-test", action="store_true")
    args = p.parse_args(argv)
    if args.self_test:
        return _self_test()
    if not args.path:
        p.print_help()
        return 2
    out = validate(json.loads(Path(args.path).read_text()))
    if out:
        for x in out:
            sys.stdout.write(f"VIOLATION: {x}\n")
        return 1
    sys.stdout.write("OK\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
