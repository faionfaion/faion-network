#!/usr/bin/env python3
"""Validate an integration-testing config JSON against the embedded schema.

Usage:
    validate-integration-testing.py <file.json>
    validate-integration-testing.py --self-test
    validate-integration-testing.py --help

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

SLUG = "integration-testing"
DECISION_REQUIRED = ["framework", "isolation_strategy", "container_engine", "external_http_strategy", "factory_uniqueness", "conftest_path"]
DRIVERS_REQUIRED = ["db_engine_required", "commit_time_behavior_under_test", "parallel_target", "external_http_calls"]
SEMVER = re.compile(r"^\d+\.\d+\.\d+$")
RULE = re.compile(r"^r[0-9a-z-]+$")
ALLOWED_FW = {"fastapi", "django", "flask"}
ALLOWED_ISO = {"rollback", "truncate", "unique-id-only", "in-memory-sqlite"}
ALLOWED_HTTP = {"respx", "wiremock", "none"}
ALLOWED_FACT = {"sequence", "uuid"}


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
        if d.get("framework") and d["framework"] not in ALLOWED_FW:
            v.append("decision.framework invalid")
        if d.get("isolation_strategy") and d["isolation_strategy"] not in ALLOWED_ISO:
            v.append("decision.isolation_strategy invalid")
        if d.get("external_http_strategy") and d["external_http_strategy"] not in ALLOWED_HTTP:
            v.append("decision.external_http_strategy invalid")
        if d.get("factory_uniqueness") and d["factory_uniqueness"] not in ALLOWED_FACT:
            v.append("decision.factory_uniqueness invalid")
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
            "framework": "fastapi",
            "isolation_strategy": "rollback",
            "container_engine": "postgres",
            "external_http_strategy": "respx",
            "factory_uniqueness": "uuid",
            "conftest_path": "tests/conftest.py",
        },
        "drivers": {"db_engine_required": True, "commit_time_behavior_under_test": False, "parallel_target": 4, "external_http_calls": "few"},
        "audit": {"rule_refs": ["r-respx-pick"]},
    }
    if _violations(good):
        return 1
    bad = json.loads(json.dumps(good))
    bad["decision"].pop("isolation_strategy")
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
