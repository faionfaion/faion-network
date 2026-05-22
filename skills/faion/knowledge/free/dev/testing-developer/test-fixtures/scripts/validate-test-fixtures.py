#!/usr/bin/env python3
"""Validate a test-fixtures config JSON against the embedded schema.

Usage:
    validate-test-fixtures.py <file.json>
    validate-test-fixtures.py --self-test
    validate-test-fixtures.py --help

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

SLUG = "test-fixtures"
DECISION_REQUIRED = ["framework", "fixtures", "rollback_strategy", "xdist_db_strategy", "conftest_path"]
DRIVERS_REQUIRED = ["has_subobjects", "has_many_optional_fields", "domain_scenarios_named", "xdist_workers"]
SEMVER = re.compile(r"^\d+\.\d+\.\d+$")
RULE = re.compile(r"^r[0-9a-z-]+$")
ALLOWED_FW = {"django", "sqlalchemy", "sqlmodel"}
ALLOWED_PATTERN = {"factory", "builder", "object-mother", "factory+mother"}
ALLOWED_SCOPE = {"function", "class", "module", "session"}
ALLOWED_UNIQ = {"sequence", "uuid"}
ALLOWED_ROLLBACK = {"transactional", "truncate", "savepoint"}
ALLOWED_XDIST = {"worker-db", "single-db", "none"}


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
        for i, fx in enumerate(d.get("fixtures") or []):
            for rk in ("model", "pattern", "scope", "uniqueness"):
                if rk not in fx:
                    v.append(f"fixtures[{i}].{rk} required")
            if fx.get("pattern") and fx["pattern"] not in ALLOWED_PATTERN:
                v.append(f"fixtures[{i}].pattern invalid")
            if fx.get("scope") and fx["scope"] not in ALLOWED_SCOPE:
                v.append(f"fixtures[{i}].scope invalid")
            if fx.get("uniqueness") and fx["uniqueness"] not in ALLOWED_UNIQ:
                v.append(f"fixtures[{i}].uniqueness invalid")
        if d.get("rollback_strategy") and d["rollback_strategy"] not in ALLOWED_ROLLBACK:
            v.append("decision.rollback_strategy invalid")
        if d.get("xdist_db_strategy") and d["xdist_db_strategy"] not in ALLOWED_XDIST:
            v.append("decision.xdist_db_strategy invalid")
    dr = rec.get("drivers") or {}
    if not isinstance(dr, dict):
        v.append("drivers must be object")
    else:
        for k in DRIVERS_REQUIRED:
            if k not in dr:
                v.append(f"drivers.{k} required")
        # Cross-rule check: xdist_workers > 1 forces uuid + worker-db
        try:
            w = int(dr.get("xdist_workers") or 0)
            if w > 1:
                for fx in d.get("fixtures") or []:
                    if fx.get("uniqueness") == "sequence":
                        v.append("xdist_workers>1 requires uniqueness=uuid (r5)")
                if d.get("xdist_db_strategy") not in ("worker-db", "none"):
                    v.append("xdist_workers>1 requires xdist_db_strategy=worker-db (r6)")
        except (TypeError, ValueError):
            pass
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
            "framework": "django",
            "fixtures": [{"model": "User", "pattern": "factory+mother", "scope": "function", "uniqueness": "uuid"}],
            "rollback_strategy": "transactional",
            "xdist_db_strategy": "worker-db",
            "conftest_path": "tests/conftest.py",
        },
        "drivers": {"has_subobjects": False, "has_many_optional_fields": False, "domain_scenarios_named": True, "xdist_workers": 4},
        "audit": {"rule_refs": ["r-mother-pick"]},
    }
    if _violations(good):
        return 1
    bad = json.loads(json.dumps(good))
    bad["decision"]["fixtures"][0]["uniqueness"] = "sequence"
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
