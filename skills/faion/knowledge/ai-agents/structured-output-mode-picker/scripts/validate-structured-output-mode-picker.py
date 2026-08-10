#!/usr/bin/env python3
"""validate-structured-output-mode-picker.py — validate an OutputModeDecisionRecord.

Inputs:
  - <record.json>  Path to a JSON file matching 02-output-contract.

Outputs:
  - stdout: PASS / FAIL with violation list.

Exit codes:
  0 - record validates.
  1 - record violates schema or self-check rules.
  2 - usage error.

Flags:
  --help        Show this message.
  --self-test   Run against built-in fixtures.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

CONSUMERS = {"extraction", "action", "dsl", "legacy"}
MODES = {"json-mode", "so-strict", "tool-call", "grammar"}
PROVIDERS = {"openai", "anthropic", "azure", "gemini", "vllm", "ollama"}

VALID_FIXTURE = {
    "stage": "invoice-extraction",
    "consumer": "extraction",
    "chosen_mode": "so-strict",
    "alternatives_considered": ["tool-call", "json-mode"],
    "rationale": "Output is typed Invoice; SO strict gives schema compliance.",
    "provider": "openai",
    "eval_delta": {"rows": 30, "winning_accuracy": 0.97, "runner_up_accuracy": 0.86},
    "follow_up_issue": None,
}

INVALID_FIXTURE = {
    "stage": "x",
    "consumer": "extraction",
    "chosen_mode": "so-strict",
    "alternatives_considered": [],
    "rationale": "short",
    "provider": "openai",
    "eval_delta": {"rows": 5, "winning_accuracy": 1.5, "runner_up_accuracy": 0.5},
}


def validate(rec: dict) -> list[str]:
    v: list[str] = []
    req = ["stage", "consumer", "chosen_mode", "alternatives_considered", "rationale", "provider", "eval_delta"]
    for k in req:
        if k not in rec:
            v.append(f"missing required key: {k}")
    if v:
        return v
    if not isinstance(rec["stage"], str) or not rec["stage"]:
        v.append("stage must be non-empty string")
    if rec["consumer"] not in CONSUMERS:
        v.append(f"consumer not in {sorted(CONSUMERS)} (got {rec['consumer']!r})")
    if rec["chosen_mode"] not in MODES:
        v.append(f"chosen_mode not in {sorted(MODES)} (got {rec['chosen_mode']!r})")
    if not isinstance(rec["alternatives_considered"], list) or not rec["alternatives_considered"]:
        v.append("alternatives_considered must be non-empty list")
    else:
        for alt in rec["alternatives_considered"]:
            if alt not in MODES:
                v.append(f"alternatives_considered contains invalid mode {alt!r}")
        if rec["chosen_mode"] in rec["alternatives_considered"]:
            v.append("chosen_mode must not appear in alternatives_considered")
    if not isinstance(rec["rationale"], str) or len(rec["rationale"]) < 24:
        v.append("rationale must be string >= 24 chars")
    if rec["provider"] not in PROVIDERS:
        v.append(f"provider not in {sorted(PROVIDERS)} (got {rec['provider']!r})")
    ed = rec.get("eval_delta", {})
    if not isinstance(ed, dict):
        v.append("eval_delta must be object")
    else:
        for k in ("rows", "winning_accuracy", "runner_up_accuracy"):
            if k not in ed:
                v.append(f"eval_delta missing {k}")
        if "rows" in ed and (not isinstance(ed["rows"], int) or ed["rows"] < 10):
            v.append("eval_delta.rows must be int >= 10")
        for k in ("winning_accuracy", "runner_up_accuracy"):
            if k in ed and not (0.0 <= float(ed[k]) <= 1.0):
                v.append(f"eval_delta.{k} must be in [0,1]")
    if rec["chosen_mode"] == "json-mode":
        if rec.get("follow_up_issue") in (None, ""):
            v.append("json-mode pick requires non-null follow_up_issue tracking link")
    return v


def main(argv: list[str]) -> int:
    if len(argv) < 2 or argv[1] in ("--help", "-h"):
        sys.stdout.write(__doc__ or "")
        return 0 if "--help" in argv or "-h" in argv else 2
    if argv[1] == "--self-test":
        ok = validate(VALID_FIXTURE)
        bad = validate(INVALID_FIXTURE)
        if ok:
            sys.stderr.write(f"self-test FAIL: valid fixture rejected: {ok}\n")
            return 1
        if not bad:
            sys.stderr.write("self-test FAIL: invalid fixture accepted\n")
            return 1
        sys.stdout.write("self-test OK\n")
        return 0
    p = Path(argv[1])
    if not p.is_file():
        sys.stderr.write(f"not a file: {p}\n")
        return 2
    try:
        rec = json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        sys.stderr.write(f"invalid JSON: {exc}\n")
        return 1
    violations = validate(rec)
    if violations:
        sys.stdout.write("FAIL\n")
        for x in violations:
            sys.stdout.write(f"  - {x}\n")
        return 1
    sys.stdout.write("PASS\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
