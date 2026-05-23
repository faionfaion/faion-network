<!-- purpose: Markdown skeleton for the debt ledger (items + scores + decisions). -->
<!-- consumes: see content/02-output-contract.xml inputs for tech-debt-budget-for-solos -->
<!-- produces: artefact conforming to content/02-output-contract.xml -->
<!-- depends-on: content/01-core-rules.xml + content/04-procedure.xml -->
<!-- token-budget-impact: ~200-700 tokens when loaded as context -->

# Tech-Debt Ledger

- owner: REPLACE
- cycle_length_days: REPLACE
- cap_percent: 20
- last_signed_utc: REPLACE

## Items

| ID | Title | Impact (1-5) | Interest (1-5) | Decision |
|----|-------|--------------|----------------|----------|
| td-001 | TITLE | 4 | 3 | pay |
| td-002 | TITLE | 2 | 1 | monitor |
| td-003 | TITLE | 5 | 4 | pay |

## Cycle allocation

- paid this cycle: td-001 (1.5d), td-003 (1d)
- total paid: 2.5d / cap 2.8d (under cap)
