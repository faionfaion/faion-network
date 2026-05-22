<!--
purpose: ABx rollout-gate report for a proposed model swap on one call site.
consumes: 48h of telemetry + baseline
produces: ship | revert decision
depends-on: content/04-procedure.xml step 4
token-budget-impact: docs-only
-->
# Rollout report — {{site_id}}

Window: {{start}} → {{end}} (≥48h)
Traffic split: 10% candidate / 90% baseline

## Latency

| metric | baseline | candidate | delta | breached SLO? |
|--------|----------|-----------|-------|----------------|
| p50    |          |           |       |                |
| p95    |          |           |       |                |

## Quality

| metric | baseline | candidate | delta |
|--------|----------|-----------|-------|
| eval score |       |           |       |

## Cost

| metric | baseline | candidate | delta |
|--------|----------|-----------|-------|
| $/call |          |           |       |

## Decision

[ ] ship (all axes within SLO + improvement on at least one axis)
[ ] hold (no axis worse, no axis better; do not ship)
[ ] revert (any axis breach)
