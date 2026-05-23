#!/usr/bin/env python3
"""Validate power-calc-spec artefact + recompute per-arm n for cross-check.

USAGE:
    validate-prompt-ab-power-calculator.py <input.json>
    validate-prompt-ab-power-calculator.py --self-test
    validate-prompt-ab-power-calculator.py --help

EXIT CODES:
    0 valid
    1 schema violation
    2 usage / unreadable

NO EXTERNAL DEPS — stdlib only.
"""
from __future__ import annotations

import argparse
import json
import math
import re
import sys
from pathlib import Path

# Z-values for two-tailed alpha and one-tailed power
Z_ALPHA = {0.05: 1.96, 0.01: 2.576, 0.10: 1.645, 0.025: 2.241}
Z_POWER = {0.8: 0.84, 0.9: 1.28, 0.95: 1.645}
SEMVER_RE = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+$")
DATE_RE = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}$")
FORBIDDEN_OWNERS = {"team", "we", "us", "engineering", ""}
FORBIDDEN_TRIGGERS = ("when needed", "as required", "ad hoc")


def required_n(baseline: float, mde: float, alpha: float, power: float) -> int:
    za = Z_ALPHA.get(alpha, 1.96)
    zb = Z_POWER.get(power, 0.84)
    p_avg = baseline + mde / 2.0
    return int(math.ceil(((za + zb) ** 2) * 2 * p_avg * (1 - p_avg) / (mde ** 2)))


def validate(s: dict) -> list[str]:
    v: list[str] = []
    if not isinstance(s, dict):
        return ["root must be object"]
    for k in ("artefact_id", "owner", "trigger", "baseline_rate", "mde", "alpha", "power", "traffic_per_day", "per_arm_n", "inputs_used", "version", "last_reviewed"):
        if k not in s:
            v.append(f"missing required field: {k}")
    owner = (s.get("owner") or "").strip().lower()
    if owner in FORBIDDEN_OWNERS:
        v.append(f"owner forbidden value {owner!r} (rule r4)")
    tr = s.get("trigger") or {}
    val = (tr.get("value") or "").lower()
    for bad in FORBIDDEN_TRIGGERS:
        if bad in val:
            v.append(f"trigger.value contains forbidden phrase {bad!r} (rule r1)")
    b = s.get("baseline_rate")
    if not isinstance(b, (int, float)) or not (0 < b < 1):
        v.append("baseline_rate must be in (0,1)")
    mde = s.get("mde")
    if not isinstance(mde, (int, float)) or mde <= 0 or mde > 0.5:
        v.append("mde must be in (0,0.5]")
    a = s.get("alpha")
    if not isinstance(a, (int, float)) or a <= 0 or a > 0.2:
        v.append("alpha must be in (0,0.2] (rule r5)")
    p = s.get("power")
    if not isinstance(p, (int, float)) or p < 0.5 or p > 0.99:
        v.append("power must be in [0.5,0.99]")
    tpd = s.get("traffic_per_day")
    if not isinstance(tpd, int) or tpd < 1:
        v.append("traffic_per_day must be ≥ 1")
    n = s.get("per_arm_n")
    if not isinstance(n, int) or n < 10:
        v.append("per_arm_n must be ≥ 10")
    if all(isinstance(s.get(k), (int, float)) for k in ("baseline_rate", "mde", "alpha", "power")):
        expected = required_n(s["baseline_rate"], s["mde"], s["alpha"], s["power"])
        if isinstance(n, int) and abs(n - expected) > 0.05 * expected:
            v.append(f"per_arm_n={n} differs from recomputed n={expected} by >5% (rule r3)")
    iu = s.get("inputs_used")
    if not isinstance(iu, list) or len(iu) < 3:
        v.append("inputs_used must list ≥3 sourced inputs (rule r3)")
    if not SEMVER_RE.match(s.get("version", "") or ""):
        v.append("version must be semver")
    if not DATE_RE.match(s.get("last_reviewed", "") or ""):
        v.append("last_reviewed must be ISO YYYY-MM-DD")
    return v


GOOD = {
    "artefact_id": "ab-greeting-2026q2",
    "owner": "ruslan@faion.net",
    "trigger": {"kind": "schedule", "value": "weekly: thursday"},
    "baseline_rate": 0.62,
    "mde": 0.04,
    "alpha": 0.05,
    "power": 0.8,
    "traffic_per_day": 1200,
    "per_arm_n": required_n(0.62, 0.04, 0.05, 0.8),
    "inputs_used": [
        {"name": "baseline_eval", "source": "git://faion/eval/q2.json"},
        {"name": "mde_target", "source": "git://faion/product/q2.md"},
        {"name": "traffic_analytics", "source": "warehouse://analytics.daily"},
    ],
    "version": "1.0.0",
    "last_reviewed": "2026-05-22",
}
BAD = {
    "artefact_id": "x",
    "owner": "team",
    "trigger": {"kind": "event", "value": "when needed"},
    "baseline_rate": 1.5,
    "mde": -0.1,
    "alpha": 0.3,
    "power": 0.3,
    "traffic_per_day": 0,
    "per_arm_n": 5,
    "inputs_used": [],
    "version": "v1",
    "last_reviewed": "yesterday",
}


def _self_test() -> int:
    errs = validate(GOOD)
    assert errs == [], f"happy path failed: {errs}"
    bad = validate(BAD)
    assert any("owner" in x for x in bad)
    assert any("alpha" in x for x in bad)
    assert any("power" in x for x in bad)
    assert any("traffic_per_day" in x for x in bad)
    sys.stdout.write("self-test PASSED\n")
    return 0


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(prog="validate-prompt-ab-power-calculator.py")
    p.add_argument("path", nargs="?", help="JSON artefact to validate")
    p.add_argument("--self-test", action="store_true")
    args = p.parse_args(argv)
    if args.self_test:
        return _self_test()
    if not args.path:
        p.print_help()
        return 2
    out = validate(json.loads(Path(args.path).read_text()))
    if out:
        for x in out:
            sys.stdout.write(f"VIOLATION: {x}\n")
        return 1
    sys.stdout.write("OK\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
