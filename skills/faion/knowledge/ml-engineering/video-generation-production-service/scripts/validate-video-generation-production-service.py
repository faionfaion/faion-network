#!/usr/bin/env python3
"""validate-video-generation-production-service.py — validate service-config.yaml.

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

REQUIRED = ["queue", "workers", "providers", "ffmpeg", "tenant_quotas", "cost_cap", "idempotency"]


def validate(obj: object) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing: {k}")
    q = obj.get("queue", {})
    if isinstance(q, dict) and q.get("kind") not in ("redis-streams", "sqs", "rabbitmq"):
        errs.append("queue.kind must be persistent (r1-persistent-queue)")
    providers = obj.get("providers", [])
    if isinstance(providers, list) and len(providers) < 2:
        errs.append("providers length must be >=2 for fallback (fm-related)")
    quotas = obj.get("tenant_quotas", {})
    if isinstance(quotas, dict) and quotas.get("default_monthly_jobs", 0) <= 0:
        errs.append("tenant_quotas.default_monthly_jobs must be >0 (r2-per-tenant-quota)")
    cap = obj.get("cost_cap", {})
    if isinstance(cap, dict) and not (50 <= cap.get("reject_at_pct", 0) <= 100):
        errs.append("cost_cap.reject_at_pct must be in [50, 100] (r4-cost-cap-pre-submit)")
    idem = obj.get("idempotency", {})
    if isinstance(idem, dict) and idem.get("window_hours", 0) < 1:
        errs.append("idempotency.window_hours must be >=1 (r5-idempotent-by-design)")
    return errs


FIXTURE_VALID = """
queue: {kind: redis-streams, connection: redis://x:6379}
workers: {count: 8, concurrency: 5}
providers:
  - {name: runway, weight: 0.6}
  - {name: luma, weight: 0.4}
ffmpeg: {enabled: true, operations: [concat]}
tenant_quotas: {default_monthly_jobs: 100, default_monthly_usd: 50}
cost_cap: {global_monthly_usd: 2500, reject_at_pct: 95}
idempotency: {window_hours: 24}
"""

FIXTURE_INVALID = """
queue: {kind: in-memory, connection: ""}
workers: {count: 1, concurrency: 1}
providers:
  - {name: runway, weight: 1.0}
ffmpeg: {enabled: false, operations: []}
tenant_quotas: {default_monthly_jobs: 0, default_monthly_usd: 0}
cost_cap: {global_monthly_usd: 0, reject_at_pct: 200}
idempotency: {window_hours: 0}
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
    ap = argparse.ArgumentParser(prog="validate-video-generation-production-service", description=__doc__,
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
