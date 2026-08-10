#!/usr/bin/env python3
"""Validate a posttool-hook-self-correction config JSON.

Usage:
    validate-posttool-hook-self-correction.py <file.json>
    validate-posttool-hook-self-correction.py --self-test
    validate-posttool-hook-self-correction.py --help

Exit codes: 0=valid, 1=invalid, 2=bad invocation
"""
from __future__ import annotations
import json
import re
import sys
from pathlib import Path

SLUG = "posttool-hook-self-correction"
DECISION_REQUIRED = ["hooks", "retry_max", "exempt_globs", "settings_json_path"]
DRIVERS_REQUIRED = ["language", "runtime_per_file", "validators_available"]
SEMVER = re.compile(r"^\d+\.\d+\.\d+$")
RULE = re.compile(r"^r[0-9a-z-]+$")


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
        hooks = d.get("hooks") or []
        if not hooks: v.append("decision.hooks must be non-empty")
        for i, h in enumerate(hooks):
            for rk in ("matcher", "glob", "command", "timeout_seconds"):
                if rk not in h: v.append(f"hooks[{i}].{rk} required")
            t = h.get("timeout_seconds")
            if isinstance(t, int) and (t < 1 or t > 30):
                v.append(f"hooks[{i}].timeout_seconds must be 1..30")
        rm = d.get("retry_max")
        if isinstance(rm, int) and (rm < 1 or rm > 10):
            v.append("decision.retry_max must be 1..10")
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
            "decision": {"hooks": [{"matcher": "Write|Edit", "glob": "**/*.py", "command": "ruff check $CLAUDE_FILE_PATH", "timeout_seconds": 5}],
                         "retry_max": 3, "exempt_globs": [], "settings_json_path": ".claude/settings.json"},
            "drivers": {"language": "python", "runtime_per_file": 1, "validators_available": ["ruff"]},
            "audit": {"rule_refs": ["r-python-ruff"]}}
    if _violations(good): return 1
    bad = json.loads(json.dumps(good))
    bad["decision"]["hooks"][0]["timeout_seconds"] = 0
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
