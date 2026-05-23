#!/usr/bin/env python3
"""validate-sec-trivy-pinned-supply-chain-scan.py — validate Trivy + SBOM config artefact.

Inputs:
    --file PATH       path to artefact JSON
    --self-test       run built-in fixture (valid + invalid)
    --help            show this message

Exit codes:
    0 = valid OR self-test passed
    1 = invalid OR self-test failed
    2 = usage / unreadable input
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REQUIRED = ["workflow_path", "action_sha", "binary_version", "scan_modes", "severity_threshold", "sbom_emission"]
SHA_RE = re.compile(r"^[a-f0-9]{40}$")
WORKFLOW_RE = re.compile(r"\.github/workflows/.*\.ya?ml$")
SEVERITY_ENUM = {"HIGH,CRITICAL", "CRITICAL"}
SBOM_FORMAT_ENUM = {"cyclonedx", "spdx-json"}

VALID_FIXTURE = {
    "workflow_path": ".github/workflows/trivy.yml",
    "action_sha": "0123456789abcdef0123456789abcdef01234567",
    "binary_version": "v0.70.0",
    "scan_modes": ["fs", "image"],
    "severity_threshold": "HIGH,CRITICAL",
    "sbom_emission": {"format": "cyclonedx", "attach_to_release": True},
}

INVALID_FIXTURE = {
    "workflow_path": ".github/workflows/trivy.yml",
    "action_sha": "v0.30.0",
    "binary_version": "latest",
    "scan_modes": ["fs"],
    "severity_threshold": "MEDIUM",
    "sbom_emission": {"format": "txt", "attach_to_release": False},
}


def validate(obj) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root: must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    wp = obj.get("workflow_path", "")
    if not WORKFLOW_RE.search(wp or ""):
        errs.append("workflow_path: must be under .github/workflows/")
    sha = obj.get("action_sha", "")
    if not SHA_RE.match(sha or ""):
        errs.append("action_sha: must be 40-char hex (tag pinning forbidden)")
    bv = obj.get("binary_version", "")
    if bv == "latest" or not isinstance(bv, str) or not bv:
        errs.append("binary_version: cannot be 'latest' and must be set")
    modes = obj.get("scan_modes", [])
    if "fs" not in modes or "image" not in modes:
        errs.append("scan_modes: must include both 'fs' and 'image'")
    sv = obj.get("severity_threshold")
    if sv not in SEVERITY_ENUM:
        errs.append(f"severity_threshold: not in {sorted(SEVERITY_ENUM)}")
    sbom = obj.get("sbom_emission", {})
    if not isinstance(sbom, dict):
        errs.append("sbom_emission: must be object")
    else:
        if sbom.get("format") not in SBOM_FORMAT_ENUM:
            errs.append(f"sbom_emission.format: not in {sorted(SBOM_FORMAT_ENUM)}")
        if sbom.get("attach_to_release") is not True:
            errs.append("sbom_emission.attach_to_release: must be true")
    return errs


def self_test() -> int:
    errs_ok = validate(VALID_FIXTURE)
    if errs_ok:
        sys.stderr.write("self-test: VALID fixture rejected:\n  " + "\n  ".join(errs_ok) + "\n")
        return 1
    errs_bad = validate(INVALID_FIXTURE)
    if not errs_bad:
        sys.stderr.write("self-test: INVALID fixture accepted (should fail)\n")
        return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--file", type=str, help="path to artefact JSON")
    ap.add_argument("--self-test", action="store_true", help="run built-in fixtures")
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
    try:
        obj = json.loads(p.read_text())
    except Exception as e:
        sys.stderr.write(f"unreadable JSON: {e}\n")
        return 2
    errs = validate(obj)
    if errs:
        for e in errs:
            sys.stderr.write(f"VIOLATION: {e}\n")
        return 1
    sys.stdout.write("OK\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
