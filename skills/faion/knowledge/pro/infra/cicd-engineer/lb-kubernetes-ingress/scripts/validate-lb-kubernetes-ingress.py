#!/usr/bin/env python3
"""validate-lb-kubernetes-ingress.py

Validate the K8s Ingress artefact against the schema in 02-output-contract.xml.

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

REQUIRED = [
    "controller",
    "replicas",
    "pdb_min_available",
    "anti_affinity",
    "topology_spread",
    "annotation_namespace",
]
NS_MAP = {
    "ingress-nginx": "nginx.ingress.kubernetes.io",
    "haproxy-ingress": "haproxy.org",
    "traefik": "traefik.ingress.kubernetes.io",
    "envoy-gateway": "envoy-gateway",
}


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    if obj.get("replicas", 0) < 3:
        errs.append("replicas must be >= 3")
    if obj.get("pdb_min_available", 0) < 2:
        errs.append("pdb_min_available must be >= 2")
    if obj.get("anti_affinity") != "kubernetes.io/hostname":
        errs.append("anti_affinity must equal kubernetes.io/hostname")
    if obj.get("topology_spread") != "topology.kubernetes.io/zone":
        errs.append("topology_spread must equal topology.kubernetes.io/zone")
    ctrl = obj.get("controller")
    expected_ns = NS_MAP.get(ctrl)
    if expected_ns and obj.get("annotation_namespace") != expected_ns:
        errs.append(f"annotation_namespace for {ctrl} must be {expected_ns}")
    return errs


OK = {
    "controller": "ingress-nginx",
    "replicas": 3,
    "pdb_min_available": 2,
    "anti_affinity": "kubernetes.io/hostname",
    "topology_spread": "topology.kubernetes.io/zone",
    "annotation_namespace": "nginx.ingress.kubernetes.io",
    "tls_via_cert_manager": True,
    "rate_limit_rpm": 600,
    "body_size_limit": "8m",
}
BAD = {
    "controller": "ingress-nginx",
    "replicas": 1,
    "pdb_min_available": 0,
    "anti_affinity": "",
    "topology_spread": "",
    "annotation_namespace": "haproxy.org",
    "tls_via_cert_manager": False,
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
