#!/usr/bin/env python3
"""validate-cost-per-dau-defense-template.py — validate a cost-per-DAU defense report JSON.

Usage:
  validate-cost-per-dau-defense-template.py <report.json>
Flags: --help, --self-test
Exit: 0 ok, 1 violation, 2 usage/IO.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

REQUIRED = (
    "report_id", "feature", "owner", "cost_per_dau_usd", "dau",
    "drivers", "peer_benchmark", "plan_90_day", "version", "last_reviewed",
)
ID_RE = re.compile(r"^cpd-[a-z0-9-]+$")
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
COLLAPSED = {"team", "we", "us", "engineering", "the team"}


def _check(doc: dict[str, Any]) -> list[str]:
    errs: list[str] = []
    for k in REQUIRED:
        if k not in doc:
            errs.append(f"missing key: {k}")
    if errs:
        return errs
    if not ID_RE.match(str(doc["report_id"])):
        errs.append("report_id must match ^cpd-[a-z0-9-]+$")
    if str(doc["owner"]).strip().lower() in COLLAPSED:
        errs.append(f"owner is a collapsed plural: {doc['owner']!r}")
    cost = doc.get("cost_per_dau_usd")
    if not isinstance(cost, (int, float)) or cost < 0:
        errs.append("cost_per_dau_usd must be number >= 0")
    if not isinstance(doc.get("dau"), int) or doc["dau"] < 1:
        errs.append("dau must be integer >= 1")
    drivers = doc.get("drivers", [])
    if not isinstance(drivers, list) or len(drivers) != 3:
        errs.append(f"drivers must be exactly 3 entries, got {len(drivers) if isinstance(drivers, list) else 'n/a'}")
    else:
        total = 0.0
        for d in drivers:
            if not d.get("name") or not isinstance(d.get("pct"), (int, float)):
                errs.append(f"driver entry malformed: {d}")
            else:
                total += d["pct"]
        if total < 70:
            errs.append(f"driver percentages sum {total} < 70 (rule r2-three-drivers)")
    pb = doc.get("peer_benchmark", {})
    if not isinstance(pb, dict) or not pb.get("citation") or not pb.get("name"):
        errs.append("peer_benchmark requires name + citation")
    plan = doc.get("plan_90_day", {})
    if not isinstance(plan, dict):
        errs.append("plan_90_day must be object")
    else:
        if not isinstance(plan.get("target_cost_per_dau_usd"), (int, float)):
            errs.append("plan_90_day.target_cost_per_dau_usd must be number")
        if not plan.get("interventions") or not isinstance(plan["interventions"], list):
            errs.append("plan_90_day.interventions must be non-empty list")
        if not plan.get("owner") or str(plan["owner"]).strip().lower() in COLLAPSED:
            errs.append(f"plan_90_day.owner missing/collapsed: {plan.get('owner')!r}")
    if not SEMVER_RE.match(str(doc["version"])):
        errs.append("version must be semver")
    if not DATE_RE.match(str(doc["last_reviewed"])):
        errs.append("last_reviewed must be ISO date")
    return errs


def _self_test() -> int:
    fixture = {
        "report_id": "cpd-search-q2-2026",
        "feature": "AI search",
        "owner": "kim@acme.com",
        "cost_per_dau_usd": 0.0412,
        "dau": 84210,
        "drivers": [
            {"name": "long-context", "pct": 38},
            {"name": "embedding", "pct": 22},
            {"name": "tool calls", "pct": 15},
        ],
        "peer_benchmark": {"name": "Perplexity", "value_usd": 0.038, "citation": "https://example.com"},
        "plan_90_day": {"target_cost_per_dau_usd": 0.025, "interventions": ["swap"], "owner": "kim@acme.com"},
        "version": "1.0.0",
        "last_reviewed": "2026-05-22",
    }
    errs = _check(fixture)
    if errs:
        sys.stderr.write("self-test FAILED:\n" + "\n".join(errs) + "\n")
        return 1
    sys.stdout.write('{"self_test": "ok"}\n')
    return 0


def main(argv: list[str]) -> int:
    if "--help" in argv or "-h" in argv:
        sys.stdout.write(__doc__ or "")
        return 0
    if "--self-test" in argv:
        return _self_test()
    if len(argv) != 2:
        sys.stderr.write("usage: validate-cost-per-dau-defense-template.py <report.json>\n")
        return 2
    try:
        doc = json.loads(Path(argv[1]).read_text())
    except (OSError, json.JSONDecodeError) as exc:
        sys.stderr.write(f"read/parse error: {exc}\n")
        return 2
    errs = _check(doc)
    if errs:
        sys.stderr.write("violations:\n" + "\n".join(f" - {e}" for e in errs) + "\n")
        return 1
    sys.stdout.write(json.dumps({"ok": True}) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
