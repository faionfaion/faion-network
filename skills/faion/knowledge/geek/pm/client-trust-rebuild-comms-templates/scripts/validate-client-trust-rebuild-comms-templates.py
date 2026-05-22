#!/usr/bin/env python3
"""validate-client-trust-rebuild-comms-templates.py — validate output artefacts against the client-trust-rebuild-comms-templates output contract.

Inputs:
  - path to a JSON file produced by the methodology

Outputs:
  - stdout: human-readable violation list (empty on pass)
  - exit 0 on pass, 1 on fail

Exit codes:
  0 — valid
  1 — schema violations
  2 — usage error
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REQUIRED = ['artefact_id', 'owner', 'decision', 'rationale', 'inputs_used', 'version', 'last_reviewed', 'forbidden_seen']
FORBIDDEN_OWNERS = {'team', 'we', 'us', '', 'engineering', 'the team', 'the squad', 'the group'}


def validate(doc: dict) -> list[str]:
    errs: list[str] = []
    for k in REQUIRED:
        if k not in doc:
            errs.append(f"missing required field: {k}")
    owner = (doc.get("owner") or "").strip().lower()
    if owner in FORBIDDEN_OWNERS:
        errs.append(f"forbidden owner value: {doc.get('owner')!r}")
    fs = doc.get("forbidden_seen", None)
    if fs is None:
        errs.append("missing forbidden_seen array (required)")
    elif not isinstance(fs, list):
        errs.append("forbidden_seen must be an array")
    elif len(fs) > 0:
        errs.append(f"forbidden_seen non-empty: {fs}")
    inputs = doc.get("inputs_used")
    decision = doc.get("decision")
    if inputs is not None and isinstance(inputs, list) and len(inputs) == 0 and decision and decision != "no-op":
        errs.append("inputs_used is empty AND decision is not 'no-op'")
    return errs


SMOKE = {
    "artefact_id": "client-trust-rebuild-comms-templates-2026-05-22-001",
    "owner": "example-handle",
    "decision": "example-value",
    "rationale": "Per input A and input B, the chosen value is example-value.",
    "inputs_used": ["input-a@path/to/a.yaml", "input-b@path/to/b.yaml"],
    "version": "1.0.0",
    "last_reviewed": "2026-05-22",
    "forbidden_seen": [],
}


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate client-trust-rebuild-comms-templates output JSON.")
    parser.add_argument("path", nargs="?", help="Path to JSON output to validate.")
    parser.add_argument("--self-test", action="store_true", help="Run an in-process smoke test with a built-in fixture.")
    args = parser.parse_args()

    if args.self_test:
        errs = validate(SMOKE)
        if errs:
            print("self-test failed:", errs, file=sys.stderr)
            return 1
        print("self-test ok")
        return 0

    if not args.path:
        parser.print_help()
        return 2

    p = Path(args.path)
    if not p.exists():
        print(f"file not found: {p}", file=sys.stderr)
        return 2

    try:
        doc = json.loads(p.read_text())
    except Exception as e:
        print(f"json parse error: {e}", file=sys.stderr)
        return 1

    errs = validate(doc)
    if errs:
        for e in errs:
            print(e)
        return 1
    print("ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
