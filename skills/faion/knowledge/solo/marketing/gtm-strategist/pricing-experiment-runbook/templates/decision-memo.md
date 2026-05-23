<!--
purpose: post-experiment go/no-go memo skeleton
consumes: experiment readout
produces: decision_memo section of the bundle
depends-on: content/01-core-rules.xml
token-budget-impact: ~350 tokens when loaded as context
-->
# Decision Memo — REPLACE-EXPERIMENT-ID

- written_at: YYYY-MM-DDThh:mm:ssZ
- decision: adopt_new \| revert_to_old \| extend_with_adjustment

## Metric readouts

| Metric | Variant old | Variant new | Delta | Significance |
|--------|-------------|-------------|-------|--------------|
| trial_to_paid_conversion_pct | 0.REPLACE | 0.REPLACE | +/- 0.REPLACE | p=REPLACE |
| MRR contribution | $REPLACE | $REPLACE | +/- $REPLACE | n/a |
| refund_rate | 0.REPLACE | 0.REPLACE | +/- 0.REPLACE | guardrail |
| dispute_rate | 0.REPLACE | 0.REPLACE | +/- 0.REPLACE | guardrail |

## Qualitative signals

- Support tickets: REPLACE-count, themes
- Cancellations citing pricing: REPLACE-count
- Customer feedback excerpts: REPLACE

## Decision rationale

REPLACE — one paragraph explaining the decision and why the metric readouts + qualitative signals justify it. If extend_with_adjustment, name the change.

## Next action

REPLACE — one concrete step (move all signups, restore old router, schedule second test).
