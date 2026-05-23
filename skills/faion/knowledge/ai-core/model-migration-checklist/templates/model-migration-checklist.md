<!--
purpose: Markdown skeleton for an authored Model Migration Checklist (human-readable).
consumes: from_model + to_model + prompt set + gold eval + cost/latency bands + owner
produces: filled-in record matching the JSON schema sibling file
depends-on: content/02-output-contract.xml
token-budget-impact: 0 — template
-->

# Model Migration Checklist — `<artefact_id>`

- **Owner:** `<single named handle / email / role>`
- **Version:** `<semver>`
- **Last reviewed:** `<YYYY-MM-DD>`
- **From:** `<from_model>` → **To:** `<to_model>`
- **Eval baseline:** `<eval_baseline_id>`

## Decision

`<one-line: what we are migrating and the chosen rollout stance>`

## Inputs used

| Name | Source path / URL |
|---|---|
| `<prompt-set>` | `<path>` |
| `<gold-eval>` | `<path>` |
| `<cost-latency-bands>` | `<path>` |

## Rollout

- [ ] Shadow (no user impact) for ≥24h
- [ ] Canary 1% / 5% / 25% with kill switch armed
- [ ] 100% only after eval delta ≤ tolerance and SLO bands green

## Rationale

`<≥2 sentences citing at least one input by name; explain why the migration is worth the risk>`
