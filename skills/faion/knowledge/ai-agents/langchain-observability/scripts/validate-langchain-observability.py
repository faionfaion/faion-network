#!/usr/bin/env python3
"""Validate a langchain-observability tracing-config against the embedded schema.

Usage:
    validate-langchain-observability.py <file.json>
    validate-langchain-observability.py --self-test
    validate-langchain-observability.py --help

Exit codes: 0 valid | 1 invalid | 2 bad invocation.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

TBACK = {"langsmith", "opentelemetry", "none"}
PII = {"public", "internal", "no-export"}
SEMVER = re.compile(r"^\d+\.\d+\.\d+$")
RULE = re.compile(r"^r\d+$")


def _violations(rec: dict) -> list[str]:
    v: list[str] = []
    if rec.get("slug") != "langchain-observability":
        v.append("slug must equal 'langchain-observability'")
    if not SEMVER.match(rec.get("version", "")):
        v.append("version must be semver")
    d = rec.get("decision") or {}
    if d.get("tracing_backend") not in TBACK:
        v.append(f"decision.tracing_backend must be in {sorted(TBACK)}")
    if not isinstance(d.get("streaming"), bool):
        v.append("decision.streaming must be bool")
    if not isinstance(d.get("redact_payloads"), bool):
        v.append("decision.redact_payloads must be bool")
    sr = d.get("sample_rate")
    if not isinstance(sr, (int, float)) or not (0 <= sr <= 1):
        v.append("decision.sample_rate must be in [0,1]")
    dr = rec.get("drivers") or {}
    if dr.get("pii_posture") not in PII:
        v.append(f"drivers.pii_posture must be in {sorted(PII)}")
    if dr.get("pii_posture") == "no-export" and d.get("tracing_backend") == "langsmith":
        v.append("pii_posture=no-export incompatible with langsmith")
    env = rec.get("env") or {}
    if "LANGCHAIN_TRACING_V2" not in env or "LANGCHAIN_PROJECT" not in env:
        v.append("env missing LANGCHAIN_TRACING_V2 or LANGCHAIN_PROJECT")
    refs = (rec.get("audit") or {}).get("rule_refs") or []
    if not refs:
        v.append("audit.rule_refs empty")
    for r in refs:
        if not RULE.match(str(r)):
            v.append(f"audit.rule_refs entry '{r}' must match ^r\\d+$")
    return v


def _self_test() -> int:
    good = {
        "slug": "langchain-observability",
        "version": "2.0.0",
        "decision": {"tracing_backend": "langsmith", "streaming": True, "redact_payloads": True, "sample_rate": 1.0},
        "drivers": {"latency_target_ms": 400, "cost_cap_per_turn_usd": 0.02, "pii_posture": "internal"},
        "env": {"LANGCHAIN_TRACING_V2": "true", "LANGCHAIN_PROJECT": "p"},
        "audit": {"rule_refs": ["r1"]},
    }
    if _violations(good):
        return 1
    bad = json.loads(json.dumps(good))
    bad["drivers"]["pii_posture"] = "no-export"
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
        sys.stderr.write("usage: validate-langchain-observability.py <file.json>\n")
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
