<!--
purpose: decision-record skeleton for picking the structured-output mode for one agent stage
consumes: classified consumer + provider matrix + per-mode eval results
produces: JSON record matching content/02-output-contract.xml
depends-on: provider docs + at least one eval set with >= 10 rows
token-budget-impact: ~250 tokens to render
-->

# Output-Mode Decision — `<stage>`

## Context

- Stage: `<stage>`
- Consumer: `extraction | action | dsl | legacy`
- Provider: `openai | anthropic | azure | gemini | vllm | ollama`

## Decision

**Chosen mode:** `so-strict | tool-call | grammar | json-mode`

## Alternatives considered

- `<alt-1>` — rejected because …
- `<alt-2>` — rejected because …

## Rationale

`<≥24 chars naming the consumer + the rejection reasons>`

## Eval delta

| Mode | Rows | Accuracy | Cost / row | p95 latency |
|---|---|---|---|---|
| `<chosen>` | `<N>` | `<acc>` | `<usd>` | `<ms>` |
| `<runner-up>` | `<N>` | `<acc>` | `<usd>` | `<ms>` |

Delta: `<winning_accuracy - runner_up_accuracy>` absolute points.

## Follow-up

- If `chosen_mode == "json-mode"` — link to tracking issue for migration once strict SO is supported.
- If `chosen_mode == "grammar"` — link to grammar-mode upgrade plan if provider adds native CFG support.
- Otherwise `null`.
