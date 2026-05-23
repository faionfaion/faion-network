<!-- purpose: AI-feature PRD skeleton with eval + guardrail sections baked in -->
<!-- consumes: inputs declared in AGENTS.md Prerequisites table -->
<!-- produces: artefact conforming to content/02-output-contract.xml (ai-native-product-development) -->
<!-- depends-on: content/01-core-rules.xml -->
<!-- token-budget-impact: ~150-400 tokens when loaded as context -->

# AI Feature PRD — <feature_id>

## Problem & user

<one paragraph>

## Eval contract

- **eval_set_id:** <support-q2-2026>
- **thresholds:**
    - faithfulness_min: 0.85
    - refusal_max_rate: 0.05
    - p95_latency_seconds: 3.0

## Prompts

Repo path: `prompts/<feature_id>/` — semver v1.0.0.

## Guardrails

- prompt-injection test fixtures: <path>
- PII allow/deny list: <path>
- jailbreak test set: <path>

## Telemetry

- model metrics: faithfulness, refusal_rate, p95_latency
- product metrics: task_success_rate, retention_d7, NPS

## Owners (>= 2)

- product: <name>
- ml: <name>
