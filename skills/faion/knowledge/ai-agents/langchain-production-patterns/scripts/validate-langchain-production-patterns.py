#!/usr/bin/env python3
"""Validate a langchain-production-patterns hardening-plan against the embedded schema.

Usage:
    validate-langchain-production-patterns.py <file.json>
    validate-langchain-production-patterns.py --self-test
    validate-langchain-production-patterns.py --help
Exit: 0 valid | 1 invalid | 2 bad invocation.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

BACKOFF = {"none", "linear", "exponential"}
PIN = {"exact-hash", "exact", "minor-upper-bound", "floating"}
DEP = {"locked", "floating"}
SEMVER = re.compile(r"^\d+\.\d+\.\d+$")
RULE = re.compile(r"^r\d+$")


def _violations(rec: dict) -> list[str]:
    v: list[str] = []
    if rec.get("slug") != "langchain-production-patterns":
        v.append("slug mismatch")
    if not SEMVER.match(rec.get("version", "")):
        v.append("version not semver")
    d = rec.get("decision") or {}
    if not isinstance(d.get("fallbacks"), list):
        v.append("decision.fallbacks must be list")
    r = d.get("retry") or {}
    if not isinstance(r.get("max_attempts"), int) or not (1 <= r["max_attempts"] <= 5):
        v.append("retry.max_attempts must be 1..5")
    if r.get("backoff") not in BACKOFF:
        v.append(f"retry.backoff in {sorted(BACKOFF)}")
    if not isinstance(d.get("configurable_fields"), list):
        v.append("decision.configurable_fields must be list")
    if d.get("pinning_mode") not in PIN:
        v.append(f"pinning_mode in {sorted(PIN)}")
    dr = rec.get("drivers") or {}
    tu = dr.get("target_uptime")
    if not isinstance(tu, (int, float)) or not (0.9 <= tu <= 1.0):
        v.append("target_uptime must be in [0.9,1.0]")
    if dr.get("dep_policy") not in DEP:
        v.append("dep_policy in {locked,floating}")
    if not isinstance(dr.get("providers"), list) or not dr.get("providers"):
        v.append("providers must be non-empty list")
    if isinstance(tu, (int, float)) and tu >= 0.99 and len(dr.get("providers", [])) >= 2 and not d.get("fallbacks"):
        v.append("target_uptime>=0.99 with 2+ providers demands non-empty fallbacks")
    if dr.get("dep_policy") == "locked" and d.get("pinning_mode") not in {"exact-hash", "exact"}:
        v.append("dep_policy=locked requires pinning_mode in {exact-hash,exact}")
    snippet = (rec.get("patch") or {}).get("snippet", "")
    if not isinstance(snippet, str) or len(snippet) < 40:
        v.append("patch.snippet must be string of length >=40")
    refs = (rec.get("audit") or {}).get("rule_refs") or []
    if not refs:
        v.append("audit.rule_refs empty")
    for x in refs:
        if not RULE.match(str(x)):
            v.append(f"rule_refs entry '{x}' invalid")
    return v


def _self_test() -> int:
    good = {
        "slug": "langchain-production-patterns",
        "version": "2.0.0",
        "decision": {"fallbacks": ["openai-gpt-4o"], "retry": {"max_attempts": 3, "backoff": "exponential"},
                     "configurable_fields": ["model"], "pinning_mode": "exact-hash"},
        "drivers": {"target_uptime": 0.999, "latency_budget_ms": 1500, "providers": ["anthropic", "openai"], "dep_policy": "locked"},
        "patch": {"snippet": "chain.with_fallbacks([b]).with_retry(stop_after_attempt=3, wait_exponential_jitter=True)"},
        "audit": {"rule_refs": ["r1"]},
    }
    if _violations(good):
        return 1
    bad = json.loads(json.dumps(good))
    bad["decision"]["retry"]["max_attempts"] = 99
    if not _violations(bad):
        return 1
    return 0


def main(argv: list[str]) -> int:
    if "--help" in argv or "-h" in argv:
        sys.stdout.write(__doc__ or "")
        return 0
    if "--self-test" in argv:
        return _self_test()
    if len(argv) < 2:
        sys.stderr.write("usage: <file.json>\n")
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
