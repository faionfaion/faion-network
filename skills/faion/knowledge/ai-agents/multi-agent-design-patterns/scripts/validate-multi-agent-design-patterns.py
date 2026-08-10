#!/usr/bin/env python3
"""Validate a pattern decision record against the F-066 output contract.

Usage:
  validate-multi-agent-design-patterns.py <pdr.yaml|pdr.json>
  validate-multi-agent-design-patterns.py --self-test
  validate-multi-agent-design-patterns.py --help

Exit codes: 0 ok, 1 violations, 2 usage.
"""
from __future__ import annotations
import json, sys
from pathlib import Path
try:
    import yaml  # type: ignore
except ImportError:
    yaml = None

CANONICAL = {"sequential", "parallel_fanout", "hierarchical", "generator_critic", "loop", "human_in_loop", "router", "blackboard"}
IRREVERSIBLE_VERBS = ("write to", "send email", "deploy", "pay", "charge", "create issue", "publish", "delete", "drop")


def violations(pdr: dict) -> list[str]:
    errs: list[str] = []
    for key in ("task", "pattern", "rationale", "alternatives_considered", "tradeoffs", "downstream_methodology", "hitl_gates"):
        if key not in pdr:
            errs.append(f"missing required key: {key}")
    if errs:
        return errs
    if pdr["pattern"] not in CANONICAL:
        errs.append(f"pattern {pdr['pattern']!r} not in 8-canonical set (rule r1-one-named-pattern)")
    if len(pdr["rationale"]) < 32:
        errs.append("rationale must be >=32 chars")
    alts = pdr["alternatives_considered"]
    if not isinstance(alts, list) or len(alts) < 2:
        errs.append("alternatives_considered must list >=2 rejected patterns")
    for a in alts:
        if "pattern" not in a or "why_rejected" not in a or len(a.get("why_rejected", "")) < 16:
            errs.append("each alternative needs `pattern` + `why_rejected` (>=16 chars)")
    if not pdr["downstream_methodology"].startswith("geek/ai/ai-agents/"):
        errs.append(f"downstream_methodology {pdr['downstream_methodology']!r} must start with 'geek/ai/ai-agents/' (rule r2-downstream-impl-link)")
    tradeoffs = pdr["tradeoffs"]
    for axis in ("latency", "cost", "audit", "parallelism"):
        if axis not in tradeoffs:
            errs.append(f"tradeoffs.{axis} missing")
    task_low = pdr["task"].lower()
    has_irrev = any(v in task_low for v in IRREVERSIBLE_VERBS)
    if has_irrev and not pdr["hitl_gates"]:
        errs.append("task contains irreversible verb but hitl_gates is empty (rule r5-hitl-on-irreversible)")
    if pdr["pattern"] == "blackboard" and not pdr.get("concurrency_plan"):
        errs.append("pattern=blackboard requires concurrency_plan (rule r3-blackboard-locking)")
    if pdr["pattern"] == "router":
        acc = pdr.get("classifier_accuracy")
        if acc is None or acc < 0.85:
            errs.append("pattern=router requires classifier_accuracy >= 0.85 (rule r4-router-needs-classifier)")
    return errs


_GOOD = {
    "task": "Generate, critique, and finalize a 1500-word EU AI Act explainer for an engineering blog",
    "pattern": "generator_critic",
    "rationale": "Quality-critical text; one generator misses factual drift. Generator + opus critic catches errors.",
    "alternatives_considered": [
        {"pattern": "sequential", "why_rejected": "research→write→edit chain does not surface factual drift between researcher and editor"},
        {"pattern": "hierarchical", "why_rejected": "no clear subtask split; one writer, one critic — no manager needed"},
    ],
    "tradeoffs": {"latency": "+50% vs sequential", "cost": "+30% (opus critic)", "audit": "best", "parallelism": "none"},
    "downstream_methodology": "geek/ai/ai-agents/multi-agent-conversational",
    "hitl_gates": [],
}
_BAD = {
    "task": "Write to production DB then deploy",
    "pattern": "stacked",
    "rationale": "x",
    "alternatives_considered": [],
    "tradeoffs": {},
    "downstream_methodology": "wrong/path",
    "hitl_gates": [],
}


def self_test() -> int:
    g, b = violations(_GOOD), violations(_BAD)
    if g:
        sys.stderr.write(f"self-test good failed: {g}\n"); return 1
    if not b:
        sys.stderr.write("self-test bad passed\n"); return 1
    sys.stdout.write(f"self-test ok (bad surfaced {len(b)} violations)\n"); return 0


def main(argv: list[str]) -> int:
    if not argv or argv[0] in ("-h", "--help"):
        sys.stdout.write(__doc__ or ""); return 0
    if argv[0] == "--self-test":
        return self_test()
    p = Path(argv[0])
    try:
        pdr = yaml.safe_load(p.read_text()) if (p.suffix in (".yaml", ".yml") and yaml is not None) else json.loads(p.read_text())
    except (OSError, ValueError) as e:
        sys.stderr.write(f"cannot read {argv[0]}: {e}\n"); return 2
    errs = violations(pdr)
    if errs:
        for e in errs:
            sys.stderr.write(f"VIOLATION: {e}\n")
        return 1
    sys.stdout.write(f"{argv[0]}: ok\n"); return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
