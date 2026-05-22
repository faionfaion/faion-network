<!--
purpose: 30-day vendor trial protocol scaffold.
consumes: chosen candidate + rubric axes.
produces: A trial-run plan with workload-migration checklist + day-by-day check-ins.
depends-on: ../scripts/validate-vendor-eval-framework.py.
token-budget-impact: ~300 tokens when filled.
-->

# Trial protocol — <vendor> (<category>)

## Duration

- Start: <ISO date>
- End: <ISO date>  (≥30 days from start)

## Real workload migrated

- Source: <current vendor / in-house system>
- Workload: <named real workload, not a synthetic dataset>
- Acceptance criteria: <specific, measurable>

## Daily / weekly check-ins

- Day 1: install + baseline measurement
- Day 7: first axis scores from each stakeholder
- Day 14: mid-trial review; raise blockers
- Day 30: final scores + decision recommendation

## Stakeholders (must score their axis)

- eng-lead:<person> — fit, exit_cost
- ops-lead:<person> — integrations, support
- finance:<person> — pricing
- security:<person> — security
