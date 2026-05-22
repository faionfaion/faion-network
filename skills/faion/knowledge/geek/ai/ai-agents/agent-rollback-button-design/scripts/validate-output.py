#!/usr/bin/env python3
"""validate-output.py — validate an agent-rollback-button-design spec.

Inputs:  path to a JSON spec file.
Outputs: exit 0 if valid; exit 1 with violation list on stderr.
Exit codes: 0=valid, 1=violations, 2=usage error, 3=load error.

stdlib + json only.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ALLOWED_ENVS = {"prod", "staging", "shadow"}
PLURAL_OWNERS = {"team", "we", "us", "tbd", ""}


def validate(payload: dict) -> list[str]:
    v: list[str] = []
    required = [
        "spec_id",
        "environment",
        "bundle_fields",
        "immutable_fields",
        "eval_gate",
        "button_label",
        "audit_log_path",
        "owner",
        "version",
        "last_reviewed",
    ]
    for k in required:
        if k not in payload:
            v.append(f"missing required field: {k}")
    if v:
        return v

    if payload["environment"] not in ALLOWED_ENVS:
        v.append(f"environment must be in {sorted(ALLOWED_ENVS)}")

    bundle = set(payload["bundle_fields"] or [])
    immutable = set(payload["immutable_fields"] or [])
    if not bundle:
        v.append("bundle_fields must be non-empty")
    if bundle & immutable:
        v.append(f"f1: bundle_fields and immutable_fields overlap: {sorted(bundle & immutable)}")

    if payload["environment"] != "shadow" and not immutable:
        v.append("f2: immutable_fields empty in non-shadow environment")

    eg = payload["eval_gate"] or {}
    mpr = eg.get("min_pass_rate")
    if not isinstance(mpr, (int, float)) or not (0 <= mpr <= 1):
        v.append("f3: eval_gate.min_pass_rate must be number in [0,1]")
    if "golden_set_version" not in eg:
        v.append("eval_gate.golden_set_version missing")

    if str(payload["owner"]).strip().lower() in PLURAL_OWNERS:
        v.append("f5: owner must be a named individual, not pronoun")

    if len(payload["button_label"]) > 40:
        v.append("button_label > 40 chars")

    if not re.fullmatch(r"\d+\.\d+\.\d+", payload["version"]):
        v.append("version must be semver")

    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", payload["last_reviewed"]):
        v.append("last_reviewed must be ISO date")

    return v


def main(argv: list[str]) -> int:
    if "--help" in argv or "-h" in argv:
        sys.stdout.write(__doc__ or "")
        return 0
    if "--self-test" in argv:
        good = {
            "spec_id": "rb-1",
            "environment": "prod",
            "bundle_fields": ["prompt_sha", "model"],
            "immutable_fields": ["conversations.messages"],
            "eval_gate": {"golden_set_version": "v1", "min_pass_rate": 0.8},
            "button_label": "Rollback",
            "audit_log_path": "s3://x/",
            "owner": "alex@faion.net",
            "version": "1.0.0",
            "last_reviewed": "2026-05-22",
        }
        violations = validate(good)
        if violations:
            sys.stderr.write(f"self-test FAILED: {violations}\n")
            return 1
        sys.stdout.write("self-test passed\n")
        return 0

    if len(argv) < 2:
        sys.stderr.write("usage: validate-output.py <spec.json> [--self-test] [--help]\n")
        return 2

    p = Path(argv[1])
    try:
        payload = json.loads(p.read_text())
    except Exception as exc:
        sys.stderr.write(f"cannot read {p}: {exc}\n")
        return 3

    violations = validate(payload)
    if violations:
        for vio in violations:
            sys.stderr.write(f"VIOLATION: {vio}\n")
        return 1
    sys.stdout.write(f"OK: {p}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
