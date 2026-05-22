#!/usr/bin/env python3
"""Validate an e2e-testing suite-config JSON against the embedded schema.

Usage:
    validate-e2e-testing.py <file.json>
    validate-e2e-testing.py --self-test
    validate-e2e-testing.py --help

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

SLUG = "e2e-testing"
DECISION_REQUIRED = ["framework", "ci_shard_count", "auth_strategy", "visual_regression", "pom_base_path", "test_dir"]
DRIVERS_REQUIRED = ["framework_preference", "visual_regression_needed", "ci_machine_budget", "journey_count"]
SEMVER = re.compile(r"^\d+\.\d+\.\d+$")
RULE = re.compile(r"^r[0-9a-z-]+$")
ALLOWED_FRAMEWORK = {"playwright", "cypress"}
ALLOWED_AUTH = {"storage-state", "api-token-injection", "none"}
ALLOWED_VR = {"none", "component-scoped"}


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
        if d.get("framework") and d["framework"] not in ALLOWED_FRAMEWORK:
            v.append(f"decision.framework must be one of {sorted(ALLOWED_FRAMEWORK)}")
        if d.get("auth_strategy") and d["auth_strategy"] not in ALLOWED_AUTH:
            v.append(f"decision.auth_strategy must be one of {sorted(ALLOWED_AUTH)}")
        if d.get("visual_regression") and d["visual_regression"] not in ALLOWED_VR:
            v.append(f"decision.visual_regression must be one of {sorted(ALLOWED_VR)}")
        if isinstance(d.get("ci_shard_count"), int) and d["ci_shard_count"] < 1:
            v.append("decision.ci_shard_count must be >= 1")
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
            "framework": "playwright",
            "ci_shard_count": 4,
            "auth_strategy": "storage-state",
            "visual_regression": "component-scoped",
            "pom_base_path": "tests/e2e/pages/base.ts",
            "test_dir": "tests/e2e",
        },
        "drivers": {"framework_preference": "greenfield", "visual_regression_needed": True, "ci_machine_budget": 4, "journey_count": 12},
        "audit": {"rule_refs": ["r-greenfield"]},
    }
    if _violations(good):
        return 1
    bad = json.loads(json.dumps(good))
    bad["decision"].pop("ci_shard_count")
    bad["audit"]["rule_refs"] = []
    vs = _violations(bad)
    return 0 if vs else 1


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
