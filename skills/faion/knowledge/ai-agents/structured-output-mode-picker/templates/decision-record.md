<!--
purpose: decision-record skeleton for picking the structured-output mode for one agent stage
consumes: classified consumer + provider matrix + per-mode eval results
produces: JSON record matching content/02-output-contract.xml
depends-on: provider docs + at least one eval set with >= 10 rows
token-budget-impact: ~250 tokens to render
variables:
  - name: stage_name
    type: string
    required: true
    description: The pipeline stage this decision binds, spelled as the code spells it. The picker is per-stage - a repo-wide answer is how a strict-schema extraction stage ends up sharing json-mode with a chat reply.
  - name: consumer
    type: enum
    required: true
    options: [extraction, action, dsl, legacy]
    description: What consumes the output. extraction = fields land in a store; action = a call that changes state; dsl = a grammar somebody else parses; legacy = a format you are not allowed to change.
  - name: provider
    type: enum
    required: true
    options: [openai, anthropic, azure, gemini, vllm, ollama]
    description: The provider this stage runs on today. Mode support differs per provider and per model tier, so a decision made against one does not transfer to another.
  - name: chosen_mode
    type: enum
    required: true
    options: [so-strict, tool-call, grammar, json-mode]
    description: The mode you are committing this stage to. json-mode guarantees only that the bytes parse - if you pick it, the follow-up section below has to name the issue tracking the way out.
  - name: eval_rows
    type: integer
    required: true
    description: How many rows the eval behind this decision ran on. Under ten the accuracy delta below is noise - give the real number and let the reader discount it themselves.
  - name: rationale
    type: text
    required: true
    description: Name the consumer and say why each rejected mode lost. Refusal rate, schema violations, latency, or a provider that does not support it - be specific enough that a reviewer can disagree.
-->

# Output-Mode Decision — `{{stage_name}}`

## Context

- Stage: `{{stage_name}}`
- Consumer: `{{consumer}}`
- Provider: `{{provider}}`

## Decision

**Chosen mode:** `{{chosen_mode}}`

## Alternatives considered

- `[alternative 1]` — rejected because …
- `[alternative 2]` — rejected because …

## Rationale

{{rationale}}

## Eval delta

| Mode | Rows | Accuracy | Cost / row | p95 latency |
|---|---|---|---|---|
| `{{chosen_mode}}` | {{eval_rows}} | `[accuracy]` | `[usd]` | `[ms]` |
| `[runner-up]` | {{eval_rows}} | `[accuracy]` | `[usd]` | `[ms]` |

Delta: `[winning accuracy - runner-up accuracy]` absolute points.

## Follow-up

- If the chosen mode is `json-mode` — link the tracking issue for migration once strict structured output is supported.
- If the chosen mode is `grammar` — link the upgrade plan for when the provider adds native CFG support.
- Otherwise `null`.
