<!--
purpose: A/B lift report comparing baseline zero-shot CoT vs candidate advanced pattern.
consumes: 50-case eval run with both patterns
produces: keep|revert decision
depends-on: content/04-procedure.xml step 4
token-budget-impact: docs-only
-->
# Lift report — {{call_site}}

Eval set: {{path}} ({{N}} cases)
Patterns: zero-shot-cot (baseline) vs {{candidate_pattern}}

| metric              | baseline | candidate | delta |
|---------------------|----------|-----------|-------|
| accuracy            |          |           | __ pp |
| cost / call (USD)   |          |           | __ x  |
| p95 latency (ms)    |          |           | __ ms |

## Decision

[ ] keep (delta_pp ≥ 3 AND cost_multiplier acceptable)
[ ] revert
