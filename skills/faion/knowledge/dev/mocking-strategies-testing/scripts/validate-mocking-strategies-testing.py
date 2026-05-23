#!/usr/bin/env python3
"""Validate a mocking-strategies spec JSON against the embedded schema.

Usage:
    validate-mocking-strategies.py <file.json>
    validate-mocking-strategies.py --self-test
    validate-mocking-strategies.py --help

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

SLUG = "mocking-strategies"
DECISION_REQUIRED = ["language", "runner", "doubles", "adapter_layer_path"]
DRIVERS_REQUIRED = ["is_own_code", "is_io_or_time_or_random", "verify_calls_needed", "stateful_reuse_count"]
SEMVER = re.compile(r"^\d+\.\d+\.\d+$")
RULE = re.compile(r"^r[0-9a-z-]+$")
ALLOWED_LANG = {"python", "typescript", "go"}
ALLOWED_RUNNER = {"pytest", "vitest", "jest", "go-test"}
ALLOWED_TYPE = {"dummy", "stub", "spy", "mock", "fake", "real"}
ALLOWED_BOUNDARY = {"io-network", "io-fs", "time", "random", "third-party", "own-code"}


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
        if d.get("language") and d["language"] not in ALLOWED_LANG:
            v.append("decision.language invalid")
        if d.get("runner") and d["runner"] not in ALLOWED_RUNNER:
            v.append("decision.runner invalid")
        for i, dbl in enumerate(d.get("doubles") or []):
            for rk in ("dep_name", "type", "boundary", "tool"):
                if rk not in dbl:
                    v.append(f"doubles[{i}].{rk} required")
            if dbl.get("type") and dbl["type"] not in ALLOWED_TYPE:
                v.append(f"doubles[{i}].type invalid")
            if dbl.get("boundary") and dbl["boundary"] not in ALLOWED_BOUNDARY:
                v.append(f"doubles[{i}].boundary invalid")
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
        "decision": {
            "language": "python",
            "runner": "pytest",
            "doubles": [{"dep_name": "x", "type": "stub", "boundary": "io-network", "tool": "pytest-mock"}],
            "adapter_layer_path": "myapp/adapters/",
        },
        "drivers": {"is_own_code": False, "is_io_or_time_or_random": True, "verify_calls_needed": False, "stateful_reuse_count": 1},
        "audit": {"rule_refs": ["r-stub-pick"]},
    }
    if _violations(good):
        return 1
    bad = json.loads(json.dumps(good))
    bad["decision"].pop("doubles")
    bad["audit"]["rule_refs"] = []
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
