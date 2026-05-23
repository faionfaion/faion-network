#!/usr/bin/env python3
"""Validate a multi-agent-production-bus spec JSON against the embedded schema.

Usage:
    validate-multi-agent-production-bus.py <file.json>
    validate-multi-agent-production-bus.py --self-test
    validate-multi-agent-production-bus.py --help

Exit codes:
    0 = valid
    1 = invalid
    2 = bad invocation
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

SLUG = "multi-agent-production-bus"
DECISION_REQUIRED = ["strategy", "agents", "handler_timeout_seconds", "per_run_token_cap", "observability_backend", "message_schema_ref"]
DRIVERS_REQUIRED = ["subtasks_independent", "chain_shape", "agent_count", "audit_required"]
SEMVER = re.compile(r"^\d+\.\d+\.\d+$")
RULE = re.compile(r"^r[0-9a-z-]+$")
ALLOWED_STRAT = {"sequential", "parallel", "hierarchical"}
ALLOWED_OBS = {"agentops", "langsmith", "none"}


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
        if d.get("strategy") and d["strategy"] not in ALLOWED_STRAT:
            v.append("decision.strategy invalid")
        if d.get("observability_backend") and d["observability_backend"] not in ALLOWED_OBS:
            v.append("decision.observability_backend invalid")
        if isinstance(d.get("agents"), list):
            if len(d["agents"]) < 2:
                v.append("decision.agents must have >= 2 entries")
            for i, a in enumerate(d["agents"]):
                for rk in ("name", "role", "model", "budget_tokens"):
                    if rk not in a:
                        v.append(f"agents[{i}].{rk} required")
        if isinstance(d.get("handler_timeout_seconds"), int) and d["handler_timeout_seconds"] < 1:
            v.append("handler_timeout_seconds must be >= 1")
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
            "strategy": "hierarchical",
            "agents": [{"name": "a", "role": "x", "model": "sonnet", "budget_tokens": 1000}, {"name": "b", "role": "y", "model": "sonnet", "budget_tokens": 1000}],
            "handler_timeout_seconds": 60,
            "per_run_token_cap": 5000,
            "observability_backend": "agentops",
            "message_schema_ref": "templates/message-bus.py#Message",
        },
        "drivers": {"subtasks_independent": False, "chain_shape": "dependent_dag", "agent_count": 2, "audit_required": True},
        "audit": {"rule_refs": ["r-hierarchical"]},
    }
    if _violations(good):
        return 1
    bad = json.loads(json.dumps(good))
    bad["decision"].pop("handler_timeout_seconds")
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
