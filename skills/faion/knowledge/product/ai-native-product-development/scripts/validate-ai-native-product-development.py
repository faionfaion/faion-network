#!/usr/bin/env python3
"""validate-ai-native-product-development.py — Validate an AI-native roadmap.

Inputs:
  - <roadmap.json>  Path to the roadmap JSON.

Outputs:
  - stdout: PASS / FAIL with violation list.

Exit codes:
  0 - roadmap validates.
  1 - roadmap violates contract.
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
MODEL_RE = re.compile(r"^[a-z][a-z0-9.-]+@[0-9]{4}-[0-9]{2}-[0-9]{2}$")
LAYERS = {"research", "design", "development", "testing", "analytics", "support"}
TIERS = {"prohibited", "high-risk", "limited", "minimal"}

VALID_FIXTURE = {
    "product": "design-suite",
    "owner": "ai-pm:alice",
    "version": "1.0.0",
    "components": [
        {
            "layer": "design",
            "name": "prototype-generator",
            "model_id": "claude-opus-4.6@2026-04-01",
            "risk_tier": "limited",
            "build_or_buy": "build",
            "build_rationale": {"core_differentiator": True, "unique_data_advantage": True, "revisit_date": "2027-04-01"},
            "inference_cost_per_active_user_usd_day": 0.12,
            "human_refines_ux": {"surface": "inline-refine-pill", "telemetry_event": "design.refine.applied"},
        }
    ],
}
INVALID_FIXTURE = {"product": "x", "components": [{"layer": "design", "model_id": "latest"}]}


def validate(spec: dict) -> list[str]:
    out: list[str] = []
    for k in ("product", "owner", "version", "components"):
        if k not in spec:
            out.append(f"{k} missing")
    if "owner" in spec and not OWNER_RE.match(str(spec["owner"])):
        out.append("owner must be role:person")
    comps = spec.get("components", [])
    if not isinstance(comps, list) or not comps:
        out.append("components must be non-empty list")
        return out
    for i, c in enumerate(comps):
        if not isinstance(c, dict):
            out.append(f"components[{i}] not object")
            continue
        if c.get("layer") not in LAYERS:
            out.append(f"components[{i}].layer must be one of {sorted(LAYERS)}")
        mid = str(c.get("model_id", ""))
        if not MODEL_RE.match(mid) or "latest" in mid.lower() or "best" in mid.lower():
            out.append(f"components[{i}].model_id must match `name@YYYY-MM-DD` and not be 'latest'/'best available'")
        if c.get("risk_tier") not in TIERS:
            out.append(f"components[{i}].risk_tier must be one of {sorted(TIERS)}")
        bob = c.get("build_or_buy")
        if bob not in ("build", "buy"):
            out.append(f"components[{i}].build_or_buy must be 'build' or 'buy'")
        if bob == "build":
            br = c.get("build_rationale", {})
            if not (br.get("core_differentiator") and br.get("unique_data_advantage")):
                out.append(f"components[{i}].build_rationale must show core_differentiator AND unique_data_advantage")
            if not br.get("revisit_date"):
                out.append(f"components[{i}].build_rationale.revisit_date missing (12-18 month rule)")
        if not isinstance(c.get("inference_cost_per_active_user_usd_day"), (int, float)):
            out.append(f"components[{i}].inference_cost_per_active_user_usd_day must be numeric")
        rux = c.get("human_refines_ux", {})
        if not isinstance(rux, dict) or not rux.get("surface") or not rux.get("telemetry_event"):
            out.append(f"components[{i}].human_refines_ux must include surface and telemetry_event")
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
