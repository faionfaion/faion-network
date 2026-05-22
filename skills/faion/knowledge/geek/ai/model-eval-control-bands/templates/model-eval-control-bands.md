<!--
purpose: Markdown skeleton for an authored Model Eval Control Bands record (human-readable).
consumes: typed-input list + owner + historical metric series
produces: filled-in record matching the JSON schema sibling file
depends-on: content/02-output-contract.xml
token-budget-impact: 0 — template
-->

# Model Eval Control Bands — `<artefact_id>`

- **Owner:** `<single named handle / email / role>`
- **Version:** `<semver>`
- **Last reviewed:** `<YYYY-MM-DD>`

## Decision

`<one-line: what is being banded and the decision shipped>`

## Inputs used

| Name | Source path / URL |
|---|---|
| `<metric-series-1>` | `<path>` |
| `<eval-suite-def>` | `<path>` |

## Bands

| Metric | Lower | Upper | Alerting |
|---|---|---|---|
| `<metric>` | `<lo>` | `<hi>` | warn / page / block |

## Rationale

`<≥2 sentences; cite at least one input by name; explain why the bounds are where they are based on historical variance / expected distribution>`
