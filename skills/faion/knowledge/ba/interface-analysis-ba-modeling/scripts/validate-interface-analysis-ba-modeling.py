#!/usr/bin/env python3
"""validate-interface-analysis.py

Validate an interface-inventory artefact against 02-output-contract.xml.

Inputs:
    --file PATH       path to inventory JSON
    --self-test       run built-in fixtures
    --help            this message

Exit codes:
    0 = valid; 1 = invalid; 2 = usage / unreadable.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

PROTOCOLS = {"http-rest", "http-webhook", "grpc", "message-bus", "file", "ui", "hardware"}
CONTRACT_TYPES = {"openapi-3.0", "openapi-3.1", "asyncapi-2", "asyncapi-3", "json-schema", "avro", "protobuf"}
SLA_FIELDS = ("latency_p95_ms", "availability_pct", "throughput_rps", "degradation_policy")
SEMVER = re.compile(r"^v\d+\.\d+\.\d+$")
ANON = {"team", "vendor", "ops", "?", ""}


def _anon(name: str) -> bool:
    n = (name or "").strip().lower()
    return not n or n in ANON or len(n.split()) < 2


def validate(obj: object) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in ("inventory_id", "version_tag", "interfaces"):
        if k not in obj:
            errs.append(f"missing required field: {k}")
    if not SEMVER.match(obj.get("version_tag", "")):
        errs.append("version_tag must match ^v\\d+\\.\\d+\\.\\d+$ (rule r5)")
    ifaces = obj.get("interfaces", [])
    if not ifaces:
        errs.append("interfaces must be non-empty")
    for i, x in enumerate(ifaces):
        if x.get("protocol") not in PROTOCOLS:
            errs.append(f"interfaces[{i}].protocol must be in {sorted(PROTOCOLS)} (rule r1)")
        ct = x.get("contract", {}).get("type")
        if ct not in CONTRACT_TYPES:
            errs.append(f"interfaces[{i}].contract.type '{ct}' not in {sorted(CONTRACT_TYPES)} (rule r1)")
        if not (x.get("contract", {}).get("ref") or "").strip():
            errs.append(f"interfaces[{i}].contract.ref empty (rule r1)")
        owners = x.get("owners", {})
        for side in ("producer", "consumer"):
            o = owners.get(side, {})
            if _anon(o.get("name", "")):
                errs.append(f"interfaces[{i}].owners.{side}.name anonymous (rule r2)")
        if not x.get("error_codes"):
            errs.append(f"interfaces[{i}].error_codes empty (rule r3)")
        sla = x.get("sla", {})
        for f in SLA_FIELDS:
            if f not in sla:
                errs.append(f"interfaces[{i}].sla missing {f} (rule r4)")
        fx = x.get("fixtures", {})
        if not fx.get("happy_path") or not fx.get("failure_paths"):
            errs.append(f"interfaces[{i}].fixtures.happy_path/failure_paths missing (rule r5)")
    return errs


OK_FIXTURE = {
    "inventory_id": "x", "version_tag": "v1.0.0",
    "interfaces": [{
        "id": "w", "protocol": "http-webhook",
        "contract": {"type": "openapi-3.1", "ref": "contracts/w.yaml"},
        "owners": {"producer": {"name": "Stripe Vendor", "role": "Vendor"},
                   "consumer": {"name": "Pedro Silva", "role": "Lead"}},
        "error_codes": [{"http": 400, "code": "bad", "retry": False}],
        "sla": {"latency_p95_ms": 500, "availability_pct": 99.9, "throughput_rps": 50, "degradation_policy": "queue"},
        "fixtures": {"happy_path": "h.json", "failure_paths": ["f.json"]},
    }]
}
BAD_FIXTURE = {"inventory_id": "x", "version_tag": "latest", "interfaces": [{}]}


def self_test() -> int:
    if validate(OK_FIXTURE):
        sys.stderr.write("OK rejected\n"); return 1
    if not validate(BAD_FIXTURE):
        sys.stderr.write("BAD accepted\n"); return 1
    sys.stdout.write("self-test OK\n"); return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
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
    obj = json.loads(p.read_text())
    errs = validate(obj)
    if errs:
        for e in errs:
            sys.stderr.write(f"VIOLATION: {e}\n")
        return 1
    sys.stdout.write("OK\n"); return 0


if __name__ == "__main__":
    sys.exit(main())
