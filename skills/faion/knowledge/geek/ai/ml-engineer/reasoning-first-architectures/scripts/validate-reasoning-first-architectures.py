#!/usr/bin/env python3
"""validate-reasoning-first-architectures.py — validate reasoning-routing.yaml.

Inputs:
    --file PATH    YAML or JSON file
    --self-test    Run built-in fixtures
    --help         Show this message

Exit codes:
    0  valid
    1  invalid
    2  usage error
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

REQUIRED = ["version", "classifier", "task_types", "eval_evidence", "budget_cap", "human_gate"]
IRREVERSIBLE = {"deploy", "delete", "payment", "db-migration"}


def validate(obj: object) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    if not obj.get("classifier"):
        errs.append("classifier required (r3-classifier-first)")
    task_types = obj.get("task_types", {})
    if not isinstance(task_types, dict) or len(task_types) < 2:
        errs.append("task_types must have >= 2 entries")
    else:
        budgets = set()
        for name, t in task_types.items():
            if not isinstance(t, dict):
                continue
            budgets.add(t.get("thinking_budget"))
            if "standard_fallback" not in t:
                errs.append(f"task_types.{name}.standard_fallback missing (r5-fall-through-on-budget-cap)")
        # single global budget across all types is forbidden
        if len(budgets) == 1 and len(task_types) >= 2:
            errs.append("single global thinking_budget across task_types (r2-task-type-budget)")
    ev = obj.get("eval_evidence", {})
    if isinstance(ev, dict):
        if ev.get("sample_size", 0) < 50:
            errs.append("eval_evidence.sample_size must be >= 50 (r1-eval-before-spend)")
    cap = obj.get("budget_cap", {})
    if isinstance(cap, dict) and cap.get("on_cap_hit") != "fall-through":
        errs.append("budget_cap.on_cap_hit must be 'fall-through' (r5-fall-through-on-budget-cap)")
    gate = obj.get("human_gate", {})
    if isinstance(gate, dict):
        actions = set(gate.get("actions", []))
        if actions & IRREVERSIBLE and not gate.get("enabled"):
            errs.append("human_gate.enabled must be true when irreversible actions listed (r4-human-gate-irreversible)")
    return errs


FIXTURE_VALID = """
version: 1.0.0
classifier: {model: claude-haiku, prompt_version: v3, confidence_field: score}
task_types:
  simple: {route: standard, thinking_budget: 0, standard_fallback: {model: x, trigger: always}}
  hard: {route: extended-thinking, thinking_budget: 8192, standard_fallback: {model: x, trigger: unhealthy}}
eval_evidence: {set_path: evals/x.jsonl, sample_size: 78, reasoning_lift: {hard: 0.18}}
budget_cap: {monthly_usd: 3500, on_cap_hit: fall-through}
human_gate: {enabled: true, actions: [deploy], confidence_floor: 0.65}
"""

FIXTURE_INVALID = """
version: 1.0.0
classifier: null
task_types:
  one: {route: extended-thinking, thinking_budget: 8192, standard_fallback: {model: x, trigger: always}}
  two: {route: o3, thinking_budget: 8192, standard_fallback: {model: x, trigger: always}}
eval_evidence: {set_path: x, sample_size: 10, reasoning_lift: {}}
budget_cap: {monthly_usd: 1000, on_cap_hit: fail}
human_gate: {enabled: false, actions: [deploy, payment], confidence_floor: 0.5}
"""


def self_test() -> int:
    if yaml is None:
        sys.stderr.write("pyyaml required\n")
        return 2
    if validate(yaml.safe_load(FIXTURE_VALID)):
        sys.stderr.write("valid fixture rejected\n")
        return 1
    errs = validate(yaml.safe_load(FIXTURE_INVALID))
    if not errs:
        sys.stderr.write("invalid fixture accepted\n")
        return 1
    sys.stdout.write(f"self-test OK ({len(errs)} violations on invalid)\n")
    return 0


def load(p: Path) -> object:
    raw = p.read_text(encoding="utf-8")
    if p.suffix in (".yml", ".yaml"):
        if yaml is None:
            raise RuntimeError("pyyaml required for YAML input")
        return yaml.safe_load(raw)
    return json.loads(raw)


def main() -> int:
    ap = argparse.ArgumentParser(
        prog="validate-reasoning-first-architectures",
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
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
    try:
        obj = load(p)
    except Exception as e:  # noqa: BLE001
        sys.stderr.write(f"parse error: {e}\n")
        return 1
    errs = validate(obj)
    if errs:
        for e in errs:
            sys.stderr.write(f"VIOLATION: {e}\n")
        return 1
    sys.stdout.write("OK\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
