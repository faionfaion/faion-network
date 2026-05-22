#!/usr/bin/env python3
"""Validate a reasoning-first-architectures spec JSON.

Usage: validate-reasoning-first-architectures.py <file.json> | --self-test | --help
Exit codes: 0=valid, 1=invalid, 2=bad invocation
"""
from __future__ import annotations
import json, re, sys
from pathlib import Path

SLUG = "reasoning-first-architectures"
DEC = ["architecture", "max_turns", "thinking_budget_tokens", "replan_trigger"]
DRV = ["task_complexity", "branching", "error_recovery_needed", "horizon"]
SEMVER = re.compile(r"^\d+\.\d+\.\d+$")
RULE = re.compile(r"^r[0-9a-z-]+$")


def _violations(rec: dict) -> list[str]:
    v = []
    if rec.get("slug") != SLUG: v.append(f"slug must equal '{SLUG}'")
    if not SEMVER.match(str(rec.get("version", ""))): v.append("version must be semver")
    d = rec.get("decision") or {}
    if not isinstance(d, dict): v.append("decision must be object")
    else:
        for k in DEC:
            if k not in d: v.append(f"decision.{k} required")
    dr = rec.get("drivers") or {}
    if not isinstance(dr, dict): v.append("drivers must be object")
    else:
        for k in DRV:
            if k not in dr: v.append(f"drivers.{k} required")
    refs = (rec.get("audit") or {}).get("rule_refs") or []
    if not refs: v.append("audit.rule_refs must be non-empty array")
    for r in refs:
        if not RULE.match(str(r)): v.append(f"audit.rule_refs entry '{r}' invalid")
    return v


def _self_test() -> int:
    good = {
        "slug": SLUG, "version": "2.0.0",
        "decision": {k: "x" for k in DEC},
        "drivers": {k: "x" for k in DRV},
        "audit": {"rule_refs": ["r1-thought-before-action"]},
    }
    if _violations(good): return 1
    bad = {"slug": SLUG, "version": "2.0.0", "decision": {}, "drivers": {}, "audit": {"rule_refs": []}}
    return 0 if _violations(bad) else 1


def main(argv: list[str]) -> int:
    if "--help" in argv or "-h" in argv: sys.stdout.write(__doc__ or ""); return 0
    if "--self-test" in argv: return _self_test()
    if len(argv) < 2: sys.stderr.write(f"usage: validate-{SLUG}.py <file.json>\n"); return 2
    p = Path(argv[1])
    if not p.exists(): sys.stderr.write(f"missing: {p}\n"); return 2
    try: rec = json.loads(p.read_text())
    except json.JSONDecodeError as e: sys.stderr.write(f"bad json: {e}\n"); return 2
    vs = _violations(rec)
    if vs:
        for x in vs: sys.stderr.write(f"VIOLATION: {x}\n")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
