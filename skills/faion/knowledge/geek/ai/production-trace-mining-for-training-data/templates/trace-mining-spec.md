<!-- purpose: trace-mining-spec narrative markdown skeleton -->
<!-- consumes: trace-mining-spec.json artefact -->
<!-- produces: human-readable review draft -->
<!-- depends-on: content/02-output-contract.xml schema -->
<!-- token-budget-impact: ~200 tokens when loaded as context -->

# Trace Mining Spec — `<artefact_id>`

- **Owner:** `<handle>`
- **Version:** `1.0.0`
- **Last reviewed:** `2026-05-22`
- **Trigger:** `schedule: monthly: 1st`
- **Scrub spec:** `git://<repo>/specs/<scrub-spec>.json`

## Capabilities

| Capability | Sample size | Label mode |
|------------|------------|------------|
| intent_classification | `<n>` | heuristic_plus_judge |
| tool_call_routing | `<n>` | heuristic_plus_judge |

## Label inference

- **Mode:** `heuristic_plus_judge`
- **Rules ref:** `git://<repo>/labels/<rules>.yaml`

## Retention

- **Days:** `365`

## Review cadence

- **Next review:** `<+3 months>`
- **Outcome metric:** `<eval delta vs prior cycle>`
