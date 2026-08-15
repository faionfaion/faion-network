<!--
purpose: Markdown skeleton for an authored Model Migration Checklist (human-readable).
consumes: from_model + to_model + prompt set + gold eval + cost/latency bands + owner
produces: filled-in record matching the JSON schema sibling file
depends-on: content/02-output-contract.xml
token-budget-impact: 0 — template
variables:
  - name: slug
    type: string
    required: true
    description: Kebab-case id for this migration, naming both ends - "gpt4o-to-sonnet45-support-triage". It is how the rollback conversation refers to this document at 2am.
  - name: owner
    type: string
    required: true
    description: One named handle or email accountable for the cutover. Not the team channel - somebody has to decide whether the canary numbers are good enough.
  - name: from_model
    type: string
    required: true
    description: The model you are leaving, with its exact snapshot or version id. "GPT-4" is not a model; the snapshot is what your baseline evals were actually run against.
  - name: to_model
    type: string
    required: true
    description: The model you are moving to, exact snapshot or version id. If the provider has already published a retirement date for it, say so here - you may be migrating twice.
  - name: eval_baseline_id
    type: string
    required: true
    description: The id of the eval run that is the "before" picture. If no baseline run exists, stop and make one - you cannot measure a delta against a memory of how it used to feel.
  - name: rollout_stance
    type: text
    required: true
    description: One line: what is moving and how far you are prepared to take it. Name the stance - shadow only, canary to 5 percent, or full cut - and who is allowed to stop it.
  - name: rationale
    type: text
    required: true
    description: Why this migration is worth the risk, citing at least one input by name. Cost, a capability you need, or a forced retirement - say which, and what happens if you do nothing.
-->

# Model Migration Checklist — `{{slug}}`

- **Owner:** `{{owner}}`
- **Version:** `1.0.0`
- **Last reviewed:** `2026-05-23`
- **From:** `{{from_model}}` → **To:** `{{to_model}}`
- **Eval baseline:** `{{eval_baseline_id}}`

## Decision

{{rollout_stance}}

## Inputs used

| Name | Source path / URL |
|---|---|
| prompt-set | `[path]` |
| gold-eval | `[path]` |
| cost-latency-bands | `[path]` |

## Rollout

- [ ] Shadow (no user impact) for ≥24h
- [ ] Canary 1% / 5% / 25% with kill switch armed
- [ ] 100% only after eval delta ≤ tolerance and SLO bands green

## Rationale

{{rationale}}
