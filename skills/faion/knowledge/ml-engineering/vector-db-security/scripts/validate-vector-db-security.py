#!/usr/bin/env python3
"""validate-vector-db-security.py — validate security-config.yaml.

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

REQUIRED = ["auth", "tls", "network", "encryption_at_rest", "audit", "pii"]


def validate(obj: object) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing: {k}")
    if not obj.get("auth", {}).get("enabled"):
        errs.append("auth.enabled must be true (r1-no-anonymous)")
    tls = obj.get("tls", {})
    if not tls.get("enabled") or tls.get("min_version") not in ("1.2", "1.3"):
        errs.append("tls.enabled + min_version >=1.2 required (r2-tls-everywhere)")
    if obj.get("network", {}).get("public_internet_exposed"):
        errs.append("network.public_internet_exposed must be false (r3-private-network-only)")
    if not obj.get("audit", {}).get("enabled"):
        errs.append("audit.enabled must be true (r4-audit-every-admin-call)")
    pii = obj.get("pii", {})
    if pii.get("erasure_sla_hours", 9999) > 720:
        errs.append("pii.erasure_sla_hours must be <=720 (GDPR Art 17; r5-pii-handling-procedure)")
    return errs


FIXTURE_VALID = """
auth: {enabled: true, method: api-key}
tls: {enabled: true, min_version: "1.3"}
network: {binding: 10.x.x.x:6333, public_internet_exposed: false}
encryption_at_rest: {enabled: true}
audit: {enabled: true, sink: s3://x}
pii: {detection: presidio, redaction: pseudonymise, retention_days: 365, erasure_sla_hours: 168}
"""

FIXTURE_INVALID = """
auth: {enabled: false, method: api-key}
tls: {enabled: false, min_version: "1.0"}
network: {binding: 0.0.0.0:6333, public_internet_exposed: true}
encryption_at_rest: {enabled: false}
audit: {enabled: false, sink: ""}
pii: {detection: none, redaction: none, retention_days: 0, erasure_sla_hours: 999}
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
    ap = argparse.ArgumentParser(prog="validate-vector-db-security", description=__doc__,
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
