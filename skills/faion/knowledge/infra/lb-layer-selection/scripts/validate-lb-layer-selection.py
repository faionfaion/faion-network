#!/usr/bin/env python3
"""validate-lb-layer-selection.py

Validate the LB layer-selection artefact against the schema in 02-output-contract.xml.

Inputs:
    --file PATH       path to artefact JSON
    --self-test       run built-in fixtures
    --help            this message

Exit codes:
    0 = valid
    1 = invalid
    2 = usage / unreadable
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REQUIRED = ["protocol", "layer", "tls_strategy", "features"]
L7_ONLY_FEATURES = {"path-routing", "header-routing", "cookie-sticky", "waf", "api-gateway"}


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    layer = obj.get("layer")
    feats = set(obj.get("features", []) or [])
    if layer == "L4" and (feats & L7_ONLY_FEATURES):
        errs.append(f"L4 cannot serve L7-only features: {sorted(feats & L7_ONLY_FEATURES)}")
    if layer == "L4" and obj.get("tls_strategy") == "terminate-at-lb":
        errs.append("L4 cannot terminate TLS at the LB (use L7 or pass-through)")
    rationale = obj.get("rationale", "")
    if not isinstance(rationale, str) or len(rationale) < 30:
        errs.append("rationale must be >= 30 chars")
    return errs


OK = {
    "protocol": "https",
    "layer": "L7",
    "tls_strategy": "terminate-at-lb",
    "features": ["path-routing", "header-routing", "waf"],
    "rationale": "HTTPS with path-based routing and WAF integration — L7 only.",
}
BAD = {
    "protocol": "tcp",
    "layer": "L4",
    "tls_strategy": "terminate-at-lb",
    "features": ["path-routing", "header-routing"],
    "rationale": "L4 for performance, route by /api path",
}


def self_test() -> int:
    if validate(OK):
        sys.stderr.write("ok rejected\n")
        return 1
    if not validate(BAD):
        sys.stderr.write("bad accepted\n")
        return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("--file", type=str)
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        return self_test()
    if not args.file:
        ap.print_help()
        return 2
    p = Path(args.file)
    if not p.is_file():
        sys.stderr.write(f"not a file: {p}\n")
        return 2
    obj = json.loads(p.read_text())
    errs = validate(obj)
    if errs:
        for e in errs:
            sys.stderr.write(f"VIOLATION: {e}\n")
        return 1
    sys.stdout.write("OK\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
