#!/usr/bin/env python3
"""Validate a tdd-workflow config JSON against the embedded schema.

Usage:
    validate-tdd-workflow.py <file.json>
    validate-tdd-workflow.py --self-test
    validate-tdd-workflow.py --help

Exit codes:
    0 = valid
    1 = invalid (violations to stderr)
    2 = bad invocation
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

SLUG = "tdd-workflow"
DECISION_REQUIRED = ["mode", "test_command", "claude_md_path", "settings_json_path", "behavior_order"]
DRIVERS_REQUIRED = ["behavior_known", "visual_feedback_drives", "performance_dominant"]
SEMVER = re.compile(r"^\d+\.\d+\.\d+$")
RULE = re.compile(r"^r[0-9a-z-]+$")
ALLOWED_MODE = {"strict-tdd", "spike-first", "benchmark-driven", "visual-deferred"}


def _violations(rec: dict) -> list[str]:
    v: list[str] = []
    if rec.get("slug") != SLUG:
        v.append(f"slug must equal '{SLUG}'")
    if not SEMVER.match(str(rec.get("version", ""))):
        v.append("version must be semver")
    d = rec.get("decision") or {}
    if not isinstance(d, dict):
        v.append("decision must be object")
    else:
        for k in DECISION_REQUIRED:
            if k not in d:
                v.append(f"decision.{k} required")
        if d.get("mode") and d["mode"] not in ALLOWED_MODE:
            v.append(f"decision.mode must be one of {sorted(ALLOWED_MODE)}")
        if isinstance(d.get("behavior_order"), list) and not d["behavior_order"]:
            v.append("decision.behavior_order must be non-empty")
    dr = rec.get("drivers") or {}
    if not isinstance(dr, dict):
        v.append("drivers must be object")
    else:
        for k in DRIVERS_REQUIRED:
            if k not in dr:
                v.append(f"drivers.{k} required")
    refs = (rec.get("audit") or {}).get("rule_refs") or []
    if not refs:
        v.append("audit.rule_refs must be non-empty array")
    for r in refs:
        if not RULE.match(str(r)):
            v.append(f"audit.rule_refs entry '{r}' must match ^r[0-9a-z-]+$")
    return v


def _self_test() -> int:
    good = {
        "slug": SLUG,
        "version": "2.0.0",
        "decision": {"mode": "strict-tdd", "test_command": "pytest -x", "claude_md_path": "CLAUDE.md", "settings_json_path": ".claude/settings.json", "behavior_order": ["b1"]},
        "drivers": {"behavior_known": True, "visual_feedback_drives": False, "performance_dominant": False},
        "audit": {"rule_refs": ["r-strict-tdd"]},
    }
    if _violations(good):
        return 1
    bad = json.loads(json.dumps(good))
    bad["decision"]["behavior_order"] = []
    return 0 if _violations(bad) else 1


def main(argv: list[str]) -> int:
    if "--help" in argv or "-h" in argv:
        sys.stdout.write(__doc__ or "")
        return 0
    if "--self-test" in argv:
        return _self_test()
    if len(argv) < 2:
        sys.stderr.write(f"usage: validate-{SLUG}.py <file.json>\n")
        return 2
    p = Path(argv[1])
    if not p.exists():
        sys.stderr.write(f"missing: {p}\n")
        return 2
    try:
        rec = json.loads(p.read_text())
    except json.JSONDecodeError as e:
        sys.stderr.write(f"bad json: {e}\n")
        return 2
    vs = _violations(rec)
    if vs:
        for x in vs:
            sys.stderr.write(f"VIOLATION: {x}\n")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
