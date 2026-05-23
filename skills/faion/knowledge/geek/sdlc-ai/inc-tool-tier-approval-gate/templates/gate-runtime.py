# purpose: Reference tier gate evaluator
# consumes: see content/02-output-contract.xml inputs
# produces: artefact conforming to content/02-output-contract.xml
# depends-on: content/01-core-rules.xml
# token-budget-impact: ~200-500 tokens when loaded as context

#!/usr/bin/env python3
# purpose: evaluate tier gate for tool invocation
# consumes: tools.yaml + invocation request
# produces: allow/deny + reason
# depends-on: scripts/validate-inc-tool-tier-approval-gate.py
# token-budget-impact: ~200 tokens
"""Tier-gate evaluator."""
from __future__ import annotations


def evaluate(tool: dict, ctx: dict) -> tuple[bool, str]:
    tier = tool.get("tier", "T3")
    if tier in ("T0", "T1"):
        return True, "audit-only"
    if tier == "T2":
        if not ctx.get("signed_token_valid"):
            return False, "T2 requires signed token"
        return True, "token-ok"
    if tier == "T3":
        if not ctx.get("two_person_approved"):
            return False, "T3 requires two-person rule"
        if ctx.get("cooling_seconds_remaining", 0) > 0:
            return False, f"T3 cooling {ctx['cooling_seconds_remaining']}s remaining"
        return True, "two-person-cooling-ok"
    return False, f"unknown tier {tier}"
