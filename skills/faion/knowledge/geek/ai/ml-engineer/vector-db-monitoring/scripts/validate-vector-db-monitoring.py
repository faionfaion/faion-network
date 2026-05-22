#!/usr/bin/env python3
"""validate-vector-db-monitoring.py — validate monitoring.yaml.

Inputs: --file PATH | --self-test | --help
Exit:   0 valid, 1 invalid, 2 usage
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

try:
    import yaml  # type: ignore
except ImportError:
    yaml = None  # type: ignore

REQUIRED = ["metrics", "alerts", "capacity", "dashboard"]
PILLARS = {"latency", "error", "memory", "disk"}
SEVERITIES = {"page", "ticket"}


def validate(obj: object) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing: {k}")
    metrics = obj.get("metrics", [])
    if isinstance(metrics, list):
        seen = {m.get("pillar") for m in metrics if isinstance(m, dict)}
        missing = PILLARS - seen
        if missing:
            errs.append(f"missing pillars: {sorted(missing)} (r1-four-pillar-coverage)")
    alerts = obj.get("alerts", [])
    if isinstance(alerts, list):
        for a in alerts:
            if not isinstance(a, dict):
                continue
            if a.get("severity") not in SEVERITIES:
                errs.append(f"alert {a.get('name', '?')}.severity must be page|ticket (r2-paged-vs-ticket)")
            if not a.get("runbook_url"):
                errs.append(f"alert {a.get('name', '?')}.runbook_url required (r5-runbook-link-required)")
    cap = obj.get("capacity", {})
    if isinstance(cap, dict) and cap.get("alert_when_lt_days", 0) < 14:
        errs.append("capacity.alert_when_lt_days must be >= 14 (r3-capacity-baseline)")
    dash = obj.get("dashboard", {})
    if isinstance(dash, dict) and not dash.get("slo_overlay"):
        errs.append("dashboard.slo_overlay must be true (r4-slo-panel-on-dashboard)")
    return errs


FIXTURE_VALID = """
metrics:
  - {name: a, pillar: latency, slo: {target: x}}
  - {name: b, pillar: error, slo: {target: x}}
  - {name: c, pillar: memory, slo: {target: x}}
  - {name: d, pillar: disk, slo: {target: x}}
alerts:
  - {name: A, expr: x, severity: page, runbook_url: https://example.com/x}
capacity: {forecast_window_days: 30, alert_when_lt_days: 14}
dashboard: {slo_overlay: true}
"""

FIXTURE_INVALID = """
metrics:
  - {name: a, pillar: latency, slo: {target: x}}
alerts:
  - {name: A, expr: x, severity: high, runbook_url: ""}
capacity: {forecast_window_days: 30, alert_when_lt_days: 3}
dashboard: {slo_overlay: false}
"""


def self_test() -> int:
    if yaml is None:
        sys.stderr.write("pyyaml required\n"); return 2
    if validate(yaml.safe_load(FIXTURE_VALID)):
        sys.stderr.write("valid fixture rejected\n"); return 1
    errs = validate(yaml.safe_load(FIXTURE_INVALID))
    if not errs:
        sys.stderr.write("invalid fixture accepted\n"); return 1
    sys.stdout.write(f"self-test OK ({len(errs)} violations on invalid)\n")
    return 0


def load(p: Path) -> object:
    raw = p.read_text(encoding="utf-8")
    if p.suffix in (".yml", ".yaml"):
        if yaml is None:
            raise RuntimeError("pyyaml required")
        return yaml.safe_load(raw)
    return json.loads(raw)


def main() -> int:
    ap = argparse.ArgumentParser(prog="validate-vector-db-monitoring", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--file", type=str)
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        return self_test()
    if not args.file:
        ap.print_help(); return 2
    p = Path(args.file)
    if not p.is_file():
        sys.stderr.write(f"not a file: {p}\n"); return 2
    try:
        obj = load(p)
    except Exception as e:  # noqa: BLE001
        sys.stderr.write(f"parse error: {e}\n"); return 1
    errs = validate(obj)
    if errs:
        for e in errs:
            sys.stderr.write(f"VIOLATION: {e}\n")
        return 1
    sys.stdout.write("OK\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
