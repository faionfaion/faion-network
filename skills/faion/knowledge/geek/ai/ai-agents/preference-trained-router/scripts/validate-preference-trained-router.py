#!/usr/bin/env python3
"""Validate a preference-trained-router spec JSON.

Usage: validate-preference-trained-router.py <file.json> | --self-test | --help
Exit codes: 0=valid, 1=invalid, 2=bad invocation
"""
from __future__ import annotations
import json, re, sys
from pathlib import Path

SLUG = "preference-trained-router"
DEC = ["mode", "router_arch", "weak_model", "strong_model", "uncertainty_band", "drift_threshold", "fallback_model"]
DRV = ["prompt_volume_per_day", "weak_strong_cost_ratio", "preference_data_size", "latency_budget_ms"]
SEMVER = re.compile(r"^\d+\.\d+\.\d+$"); RULE = re.compile(r"^r[0-9a-z-]+$")
MODES = {"router-deploy", "static-rule"}
ARCHS = {"logistic-regression", "small-bert", "lightgbm", "none"}


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
        if d.get("router_arch") and d["router_arch"] not in ARCHS: v.append("decision.router_arch invalid")
        for fk in ("uncertainty_band", "drift_threshold"):
            val = d.get(fk)
            if isinstance(val, (int, float)) and (val < 0 or val > 1):
                v.append(f"decision.{fk} must be 0..1")
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
            "decision": {"mode": "router-deploy", "router_arch": "small-bert", "weak_model": "haiku", "strong_model": "opus", "uncertainty_band": 0.1, "drift_threshold": 0.85, "fallback_model": "opus"},
            "drivers": {"prompt_volume_per_day": 5000, "weak_strong_cost_ratio": 15, "preference_data_size": 4000, "latency_budget_ms": 1500},
            "audit": {"rule_refs": ["r-deploy-router"]}}
    if _violations(good): return 1
    bad = json.loads(json.dumps(good))
    bad["decision"]["uncertainty_band"] = 2
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
