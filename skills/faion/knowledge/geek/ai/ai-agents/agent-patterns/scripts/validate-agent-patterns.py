#!/usr/bin/env python3
"""validate-agent-patterns.py — validate an agent-patterns decision record.

Inputs:  path to a JSON output file.
Outputs: exit 0 if valid, exit 1 with violation list on stderr.
Exit codes: 0=valid, 1=violations, 2=usage error, 3=schema load error.

stdlib + json only (no external deps).
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

SCHEMA_PATH = Path(__file__).parent.parent / "templates" / "decision-record.json"
ALLOWED_PATTERNS = {"react", "plan-and-execute", "reflexion", "escalate-to-human"}
REJECTED_PATTERN_ENUM = {"react", "plan-and-execute", "reflexion"}
DESTRUCTIVE_VERBS = ("write", "send", "post", "delete", "deploy", "publish")


def fail(violations: list[str]) -> None:
    for v in violations:
        sys.stderr.write(f"VIOLATION: {v}\n")
    sys.exit(1)


def validate(payload: dict) -> list[str]:
    v: list[str] = []
    required = [
        "task_id",
        "chosen_pattern",
        "caps",
        "terminal_condition",
        "rationale",
        "rejected_patterns",
        "actor_model",
        "human_gate_required",
        "version",
        "produced_at",
    ]
    for key in required:
        if key not in payload:
            v.append(f"missing required field: {key}")
    if v:
        return v

    if payload["chosen_pattern"] not in ALLOWED_PATTERNS:
        v.append(f"chosen_pattern must be one of {sorted(ALLOWED_PATTERNS)}")

    caps = payload.get("caps") or {}
    if not isinstance(caps, dict):
        v.append("caps must be an object")
    else:
        for k, val in caps.items():
            if not isinstance(val, int) or val < 1:
                v.append(f"caps.{k} must be positive int")
        if "max_iterations" in caps and caps["max_iterations"] > 50:
            v.append("caps.max_iterations > 50 (cost runaway, see fm-01)")

    if payload["chosen_pattern"] == "reflexion":
        tc = payload["terminal_condition"].lower()
        bad_markers = ("vibes", "feels", "thinks", "decides", "looks good")
        if any(m in tc for m in bad_markers):
            v.append("f1: reflexion + non-deterministic terminal_condition")
        if not payload.get("critic_model"):
            v.append("reflexion requires critic_model")

    if not isinstance(payload["rejected_patterns"], list) or not payload["rejected_patterns"]:
        v.append("f4: rejected_patterns must be non-empty list")
    else:
        for rp in payload["rejected_patterns"]:
            if not isinstance(rp, dict) or "pattern" not in rp or "reason" not in rp:
                v.append("rejected_patterns items need {pattern, reason}")
            elif rp["pattern"] not in REJECTED_PATTERN_ENUM:
                v.append(f"rejected_patterns.pattern must be in {sorted(REJECTED_PATTERN_ENUM)}")

    if "success" not in payload["rationale"].lower() and "signal" not in payload["rationale"].lower():
        v.append("f5: rationale must mention success-signal availability")

    if not re.fullmatch(r"\d+\.\d+\.\d+", payload["version"]):
        v.append("version must be semver (x.y.z)")

    if not payload["human_gate_required"]:
        rec_text = json.dumps(payload).lower()
        if any(verb in rec_text for verb in DESTRUCTIVE_VERBS):
            v.append("f2: destructive verb present but human_gate_required=false")

    return v


def main(argv: list[str]) -> int:
    if "--help" in argv or "-h" in argv:
        sys.stdout.write(__doc__ or "")
        return 0
    if "--self-test" in argv:
        good = {
            "task_id": "T1",
            "chosen_pattern": "react",
            "caps": {"max_iterations": 10},
            "terminal_condition": "no tool calls in response",
            "rationale": "Reversible read-only research task; no success signal so ReAct is the safe default.",
            "rejected_patterns": [{"pattern": "reflexion", "reason": "no objective check exists"}],
            "actor_model": "claude-sonnet-4",
            "human_gate_required": False,
            "version": "1.0.0",
            "produced_at": "2026-05-22T10:00:00Z",
        }
        violations = validate(good)
        if violations:
            sys.stderr.write(f"self-test FAILED: {violations}\n")
            return 1
        sys.stdout.write("self-test passed\n")
        return 0

    if len(argv) < 2:
        sys.stderr.write("usage: validate-agent-patterns.py <path-to-record.json> [--self-test] [--help]\n")
        return 2

    p = Path(argv[1])
    try:
        payload = json.loads(p.read_text())
    except Exception as exc:
        sys.stderr.write(f"cannot read {p}: {exc}\n")
        return 3

    violations = validate(payload)
    if violations:
        fail(violations)
    sys.stdout.write(f"OK: {p} is a valid agent-patterns decision record\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
