#!/usr/bin/env python3
"""validate-ai-product-success-metrics-catalog.py — Validate an AI metrics catalog.

Inputs:
  - <catalog.json>  Path to the catalog JSON.

Outputs:
  - stdout: PASS / FAIL with violation list.

Exit codes:
  0 - catalog validates.
  1 - catalog violates contract.
  2 - usage error.

Flags:
  --help        Show this message.
  --self-test   Run against a built-in fixture.
"""
from __future__ import annotations

import datetime as dt
import json
import re
import sys
from pathlib import Path

SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")
OWNER_RE = re.compile(r"^[a-zA-Z0-9._-]+:[a-zA-Z0-9._-]+$")
STALE_DAYS = 90
REQUIRED_METRICS = ("deflection_rate", "intervention_rate", "hallucination_rate", "time_to_correction", "retention_on_ai_features")

VALID_FIXTURE = {
    "artefact_id": "copilot-ai-metrics",
    "owner": "ai-pm:alice",
    "version": "1.0.0",
    "last_reviewed": dt.date.today().isoformat(),
    "metrics": {
        m: {"definition": "metric defined with at least twenty chars", "source": "logs", "baseline": 0.42}
        for m in REQUIRED_METRICS
    },
    "inputs_used": [{"name": "logs", "source": "https://dashboard/x"}],
}
INVALID_FIXTURE = {"owner": "team", "metrics": {}}


def validate(spec: dict) -> list[str]:
    out: list[str] = []
    for k in ("artefact_id", "owner", "version", "last_reviewed", "metrics", "inputs_used"):
        if k not in spec:
            out.append(f"{k} missing")
    if "owner" in spec and (not OWNER_RE.match(str(spec["owner"])) or str(spec["owner"]).lower().startswith(("team", "we", "us"))):
        out.append("owner must be role:person")
    if "version" in spec and not SEMVER_RE.match(str(spec["version"])):
        out.append("version must be semver")
    if "last_reviewed" in spec:
        try:
            d = dt.date.fromisoformat(str(spec["last_reviewed"]))
            age = (dt.date.today() - d).days
            if age > STALE_DAYS:
                out.append(f"last_reviewed stale ({age} days; max {STALE_DAYS})")
        except ValueError:
            out.append("last_reviewed not ISO date")
    metrics = spec.get("metrics", {})
    for k in REQUIRED_METRICS:
        if k not in metrics:
            out.append(f"metrics.{k} missing")
            continue
        m = metrics[k]
        if not isinstance(m, dict):
            out.append(f"metrics.{k} must be object")
            continue
        for sub in ("definition", "source", "baseline"):
            if sub not in m:
                out.append(f"metrics.{k}.{sub} missing")
        if "definition" in m and len(str(m["definition"])) < 20:
            out.append(f"metrics.{k}.definition must be >= 20 chars")
    if not isinstance(spec.get("inputs_used"), list) or not spec.get("inputs_used"):
        out.append("inputs_used must be non-empty list")
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
