# AI Feature Build vs Buy vs Finetune Decision

## Summary

**One-sentence:** ADR-style decision record selecting among build-from-scratch / buy-vendor-API / finetune-existing for a specific AI feature, scored on cost, quality, control, time-to-market.

**One-paragraph:** ADR-style decision record selecting among build-from-scratch / buy-vendor-API / finetune-existing for a specific AI feature, scored on cost, quality, control, time-to-market. This methodology codifies the rules, output contract, failure modes, and decision tree needed for a decision-record produced by an agent applying ai feature build vs buy vs finetune decision. The deliverable is validated against an explicit JSON Schema and routed through a decision tree that maps observable signals to rule ids in `01-core-rules.xml`.

**Ефективно для:**

- Building a reproducible decision-record for ai feature build vs buy vs finetune decision across teams.
- Reviewing AI-or-human work against an explicit contract instead of vibes.
- Wiring the output into downstream automation (CI gates, observability, post-mortems).
- Avoiding the failure modes listed in `03-failure-modes.xml`.

## Applies If (ALL must hold)

- team is deciding how to deliver a new AI feature (build, buy, finetune)
- decision will cost > $10k/yr or affect a user-visible surface
- decision will be revisited yearly and needs to be auditable

## Skip If (ANY kills it)

- decision was made <90 days ago for an adjacent feature with the same constraints — reuse it
- feature is exploratory only with no shipping plan — wait for the ship decision
- vendor is fixed by org policy (sole-source contract) — record that fact, skip the comparison

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Feature spec (inputs, outputs, success metric) | product spec | product |
| Quality + cost + latency targets | perf doc | engineering |
| Vendor shortlist (≥2) | research | ml-engineering |
| Internal training-data availability | data team | data engineering |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[inference-cost-unit-economics]] | Cost-per-outcome math |
| [[ai-feature-progressive-rollout]] | Rollout shape per option |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules grounding the methodology with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the deliverable + valid/invalid/forbidden examples | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom + root-cause + fix triplets | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure end-to-end | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `option_specification` | sonnet | Spec the 3 options in concrete terms. |
| `scoring` | opus | Score on cost / quality / control / time-to-market. |
| `risk_weighting` | opus | Weight scores by org risk profile. |

## Templates

| File | Purpose |
|------|---------|
| `templates/decision-record.md` | ADR skeleton |
| `templates/scoring-matrix.json` | Scoring matrix JSON skeleton |
| `templates/_smoke-test.md` | Minimum viable filled-in ADR |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ai-feature-build-buy-finetune-decision.py` | Validate the decision-record artefact against the 02-output-contract schema | After subagent returns, before commit/publish |

## Related

- [[inference-cost-unit-economics]]
- [[ai-feature-progressive-rollout]]
- [[ai-call-site-inventory]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals from inputs and intermediate artefacts to a rule from `01-core-rules.xml`, telling the agent which variant of the methodology to apply or when to stop. Walk it on every fresh invocation; do not memo-ise outcomes across distinct engagements.
