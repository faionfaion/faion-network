<!--

purpose: decision-record skeleton for picking the structured-output mode for one agent stage
consumes: classified consumer + provider matrix + per-mode eval results
produces: JSON record matching content/02-output-contract.xml
depends-on: provider docs + at least one eval set with >= 10 rows
token-budget-impact: ~250 tokens to render
-->



# Output-Mode Decision — `<stage_name>`

## Context

- Stage: `<stage_name>`
- Consumer: `<consumer>`
- Provider: `<provider>`

## Decision

**Chosen mode:** `<chosen_mode>`

## Alternatives considered

- `[alternative 1]` — rejected because …
- `[alternative 2]` — rejected because …

## Rationale

<rationale>

## Eval delta

| Mode | Rows | Accuracy | Cost / row | p95 latency |
|---|---|---|---|---|
| `<chosen_mode>` | <eval_rows> | `[accuracy]` | `[usd]` | `[ms]` |
| `[runner-up]` | <eval_rows> | `[accuracy]` | `[usd]` | `[ms]` |

Delta: `[winning accuracy - runner-up accuracy]` absolute points.

## Follow-up

- If the chosen mode is `json-mode` — link the tracking issue for migration once strict structured output is supported.
- If the chosen mode is `grammar` — link the upgrade plan for when the provider adds native CFG support.
- Otherwise `null`.
