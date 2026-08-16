<!-- purpose: Markdown skeleton for the SOW appendix decision record -->
<!-- consumes: signal scores + decision-tree output -->
<!-- produces: decision-record artefact (decision-record produces type) -->
<!-- depends-on: content/01-core-rules.xml -->
<!-- token-budget-impact: ~300 tokens when filled -->

# Engagement Shape Decision — `<CLIENT>` — `<ENGAGEMENT>`

- **decision_id:** `fvh-<slug>`
- **decider:** `@<handle>`
- **decided_at:** `<YYYY-MM-DD>`
- **reassessment_at_25pct:** `<YYYY-MM-DD>`

## Scope summary

<one paragraph>

## Signal scores

| Signal | Score | Evidence |
|--------|-------|----------|
| scope_clarity | low / medium / high | <source> |
| change_rate | low / medium / high | <source> |
| client_maturity | low / medium / high | <source> |
| domain_familiarity | low / medium / high | <source> |

## Options considered

- fixed: <fixed>
- hourly: <hourly>
- hybrid: <hybrid>

## Chosen

`fixed | hourly | hybrid`

## Kill criteria (per option)

- `fixed`: <numeric threshold to reopen>
- `hourly`: <numeric_threshold>
- `hybrid`: <numeric_threshold>

## Reversal trigger

<numeric trigger that reopens the decision; ≥20 chars>

## Reassessment plan

At 25% project elapsed (`<DATE>`): re-score signals; file delta if any band flipped.
