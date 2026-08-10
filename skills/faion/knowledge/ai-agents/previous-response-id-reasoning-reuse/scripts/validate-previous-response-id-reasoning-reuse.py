#!/usr/bin/env python3
"""Validate a previous-response-id-reasoning-reuse spec JSON.

Usage: validate-previous-response-id-reasoning-reuse.py <file.json> | --self-test | --help
"""
from __future__ import annotations
import json, re, sys
from pathlib import Path

SLUG = "previous-response-id-reasoning-reuse"
DEC = ["mode", "session_store", "retention_ttl_hours", "log_destination"]
DRV = ["api_flavor", "multi_turn", "reasoning_model_used"]
SEMVER = re.compile(r"^\d+\.\d+\.\d+$"); RULE = re.compile(r"^r[0-9a-z-]+$")
MODES = {"previous-response-id", "message-array"}


def _violations(rec: dict) -> list[str]:
    v = []
    if rec.get("slug") != SLUG: v.append(f"slug must equal '{SLUG}'")
    if not SEMVER.match(str(rec.get("version", ""))): v.append("version must be semver")
    d = rec.get("decision") or {}
    if not isinstance(d, dict): v.append("decision must be object")
    else:
        for k in DEC:
            if k not in d: v.append(f"decision.{k} required")
        if d.get("mode") and d["mode"] not in MODES: v.append("decision.mode invalid")
        ttl = d.get("retention_ttl_hours")
        if isinstance(ttl, int) and ttl < 1: v.append("retention_ttl_hours must be >= 1")
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
    good = {"slug": SLUG, "version": "2.0.0",
            "decision": {"mode": "previous-response-id", "session_store": "redis://x", "retention_ttl_hours": 24, "log_destination": "stdout"},
            "drivers": {"api_flavor": "responses", "multi_turn": True, "reasoning_model_used": True},
            "audit": {"rule_refs": ["r-use-previous-id"]}}
    if _violations(good): return 1
    bad = json.loads(json.dumps(good))
    bad["decision"]["retention_ttl_hours"] = 0
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
