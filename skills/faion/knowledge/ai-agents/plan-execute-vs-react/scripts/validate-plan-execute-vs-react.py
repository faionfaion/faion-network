#!/usr/bin/env python3
"""Validate a plan-execute-vs-react spec JSON.

Usage:
    validate-plan-execute-vs-react.py <file.json>
    validate-plan-execute-vs-react.py --self-test
    validate-plan-execute-vs-react.py --help

Exit codes: 0=valid, 1=invalid, 2=bad invocation
"""
from __future__ import annotations
import json
import re
import sys
from pathlib import Path

SLUG = "plan-execute-vs-react"
DECISION_REQUIRED = ["loop_type", "max_turns", "plan_model", "execute_model", "replan_on_failure"]
DRIVERS_REQUIRED = ["known_substeps", "horizon", "adaptability_needed", "audit_required", "mixed_predictability"]
SEMVER = re.compile(r"^\d+\.\d+\.\d+$")
RULE = re.compile(r"^r[0-9a-z-]+$")
ALLOWED_LOOP = {"plan-execute", "react", "hybrid"}


def _violations(rec: dict) -> list[str]:
    v = []
    if rec.get("slug") != SLUG: v.append(f"slug must equal '{SLUG}'")
    if not SEMVER.match(str(rec.get("version", ""))): v.append("version must be semver")
    d = rec.get("decision") or {}
    if not isinstance(d, dict):
        v.append("decision must be object")
    else:
        for k in DECISION_REQUIRED:
            if k not in d: v.append(f"decision.{k} required")
        if d.get("loop_type") and d["loop_type"] not in ALLOWED_LOOP:
            v.append("decision.loop_type invalid")
        mt = d.get("max_turns")
        if isinstance(mt, int) and mt < 1:
            v.append("decision.max_turns must be >= 1")
    dr = rec.get("drivers") or {}
    if not isinstance(dr, dict):
        v.append("drivers must be object")
    else:
        for k in DRIVERS_REQUIRED:
            if k not in dr: v.append(f"drivers.{k} required")
    refs = (rec.get("audit") or {}).get("rule_refs") or []
    if not refs: v.append("audit.rule_refs must be non-empty array")
    for r in refs:
        if not RULE.match(str(r)): v.append(f"audit.rule_refs entry '{r}' must match ^r[0-9a-z-]+$")
    return v


def _self_test() -> int:
    good = {"slug": SLUG, "version": "2.0.0",
            "decision": {"loop_type": "hybrid", "max_turns": 5, "plan_model": "opus", "execute_model": "sonnet", "replan_on_failure": True},
            "drivers": {"known_substeps": "unknown", "horizon": 15, "adaptability_needed": True, "audit_required": True, "mixed_predictability": True},
            "audit": {"rule_refs": ["r3-hybrid-long-horizon"]}}
    if _violations(good): return 1
    bad = json.loads(json.dumps(good))
    bad["decision"]["max_turns"] = 0
    return 0 if _violations(bad) else 1


def main(argv: list[str]) -> int:
    if "--help" in argv or "-h" in argv:
        sys.stdout.write(__doc__ or ""); return 0
    if "--self-test" in argv: return _self_test()
    if len(argv) < 2:
        sys.stderr.write(f"usage: validate-{SLUG}.py <file.json>\n"); return 2
    p = Path(argv[1])
    if not p.exists():
        sys.stderr.write(f"missing: {p}\n"); return 2
    try:
        rec = json.loads(p.read_text())
    except json.JSONDecodeError as e:
        sys.stderr.write(f"bad json: {e}\n"); return 2
    vs = _violations(rec)
    if vs:
        for x in vs: sys.stderr.write(f"VIOLATION: {x}\n")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
