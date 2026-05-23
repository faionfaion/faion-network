<!--
purpose: Markdown skeleton for an authored Model Upgrade Checklist (human-readable).
consumes: current_model + target_model + prompt set + gold eval + rollout plan + owner
produces: filled-in record matching the JSON schema sibling file
depends-on: content/02-output-contract.xml
token-budget-impact: 0 — template
-->

# Model Upgrade Checklist — `<artefact_id>`

- **Owner:** `<single named handle / email / role>`
- **Version:** `<semver>`
- **Last reviewed:** `<YYYY-MM-DD>`
- **From:** `<current_model>` → **To:** `<target_model>`
- **Eval baseline:** `<eval_baseline_id>`

## Decision

`<one-line: what we are upgrading and the chosen rollout stance>`

## Inputs used

| Name | Source path / URL |
|---|---|
| `<prompt-set>` | `<path>` |
| `<gold-eval>` | `<path>` |
| `<cost-latency-bands>` | `<path>` |

## Rollout (kill switch armed)

- [ ] Shadow (no user impact) ≥24h
- [ ] Canary 1% / 5% / 25% with eval deltas in bands
- [ ] 100% only after eval delta ≤ tolerance and SLOs green

## Rationale

`<≥2 sentences citing at least one input by name; explain why this upgrade is worth the risk>`
