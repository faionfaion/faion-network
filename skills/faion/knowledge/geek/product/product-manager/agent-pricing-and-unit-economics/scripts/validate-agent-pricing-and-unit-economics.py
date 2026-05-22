#!/usr/bin/env python3
"""validate-agent-pricing-and-unit-economics.py — Validate a unit-economics report.

Inputs:
  - <report.json>  Path to the unit-economics report JSON.

Outputs:
  - stdout: PASS / FAIL with violation list.

Exit codes:
  0 - report validates.
  1 - report violates rules (margin floor, measured COGS, model fit, cap presence).
  2 - usage error.

Flags:
  --help        Show this message.
  --self-test   Run against a built-in fixture.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

OWNER_RE = re.compile(r"^[a-zA-Z0-9._-]+:[a-zA-Z0-9._-]+$")
MIN_MARGIN_PCT = 60
ALLOWED_MODELS = {"per-seat", "metered", "outcome"}
MIN_SAMPLE = 100

VALID_FIXTURE = {
    "product": "support-agent",
    "owner": "ai-pm:alice",
    "task_sample_size": 250,
    "cogs": {"p50": 0.18, "p95": 0.55, "median_total": 0.18},
    "price_per_task": 0.50,
    "gross_margin_pct": 64,
    "pricing_model": "metered",
    "cap": {"monthly_tasks": 5000, "overage_per_task": 0.05},
    "repricing_trigger": {"on_provider_price_change_pct": 10, "on_p95_shift_pct": 50},
}
INVALID_FIXTURE = {"product": "x", "task_sample_size": 5, "gross_margin_pct": 20, "pricing_model": "vibes"}


def validate(spec: dict) -> list[str]:
    out: list[str] = []
    for k in ("product", "owner", "task_sample_size", "cogs", "price_per_task", "gross_margin_pct", "pricing_model", "cap", "repricing_trigger"):
        if k not in spec:
            out.append(f"{k} missing")
    if "owner" in spec and not OWNER_RE.match(str(spec["owner"])):
        out.append("owner must be role:person")
    ts = spec.get("task_sample_size", 0)
    if not isinstance(ts, int) or ts < MIN_SAMPLE:
        out.append(f"task_sample_size must be >= {MIN_SAMPLE} (rule r1-measure-cogs-not-estimate)")
    margin = spec.get("gross_margin_pct", 0)
    if not isinstance(margin, (int, float)) or margin < MIN_MARGIN_PCT:
        out.append(f"gross_margin_pct must be >= {MIN_MARGIN_PCT} (rule r2-gross-margin-floor)")
    pm = spec.get("pricing_model")
    if pm not in ALLOWED_MODELS:
        out.append(f"pricing_model must be one of {sorted(ALLOWED_MODELS)}")
    cap = spec.get("cap", {})
    if not isinstance(cap, dict) or not cap.get("monthly_tasks"):
        out.append("cap.monthly_tasks must be set (rule r4-cap-protect-heavy-users)")
    repricing = spec.get("repricing_trigger", {})
    if not isinstance(repricing, dict) or not repricing.get("on_provider_price_change_pct"):
        out.append("repricing_trigger.on_provider_price_change_pct must be set (rule r5-reprice-on-model-changes)")
    cogs = spec.get("cogs", {})
    if isinstance(cogs, dict) and cogs.get("p95") and cogs.get("p50"):
        ratio = cogs["p95"] / cogs["p50"] if cogs["p50"] > 0 else 0
        if ratio > 5 and pm == "per-seat":
            out.append(f"per-seat pricing with high variance (p95/p50={ratio:.1f}) — switch to metered or outcome (rule r3-pricing-model-fits-variance)")
    return out


def main(argv: list[str]) -> int:
    if len(argv) < 2 or argv[1] in ("--help", "-h"):
        sys.stdout.write(__doc__ or "")
        return 0 if "--help" in argv else 2
    if argv[1] == "--self-test":
        ok = validate(VALID_FIXTURE)
        bad = validate(INVALID_FIXTURE)
        if ok:
            sys.stderr.write(f"self-test FAIL: valid fixture rejected: {ok}\n")
            return 1
        if not bad:
            sys.stderr.write("self-test FAIL: invalid fixture accepted\n")
            return 1
        sys.stdout.write("self-test OK\n")
        return 0
    p = Path(argv[1])
    if not p.is_file():
        sys.stderr.write(f"not a file: {p}\n")
        return 2
    try:
        spec = json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        sys.stderr.write(f"invalid JSON: {exc}\n")
        return 1
    v = validate(spec)
    if v:
        sys.stdout.write("FAIL\n")
        for x in v:
            sys.stdout.write(f"  - {x}\n")
        return 1
    sys.stdout.write("PASS\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
