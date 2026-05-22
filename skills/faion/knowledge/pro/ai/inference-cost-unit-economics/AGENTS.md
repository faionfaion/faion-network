---
slug: inference-cost-unit-economics
tier: pro
group: ai
domain: ai-core
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "a795f5cb8c56fe05"
summary: "Inference Cost Unit Economics — testable methodology for LLM-agent design, evals, safety, cost. cost-reduction-strategies and cost-optimization exist as tactical lists. Missing: how to compute cost-per-user-action, cost-per-feature-call, gross-margin-per-AI-feature; how to set a cost ceiling; how to alert on cost runaway. ML engineers need this to defend ..."
tags: [ai, pro, methodology]
---
# Inference Cost Unit Economics

## Summary

**One-sentence:** Inference Cost Unit Economics — testable methodology for LLM-agent design, evals, safety, cost. cost-reduction-strategies and cost-optimization exist as tactical lists. Missing: how to compute cost-per-user-action, cost-per-feature-call, gross-margin-per-AI-feature; how to set a cost ceiling; how to alert on cost runaway. ML engineers need this to defend ...

**One-paragraph:** Inference Cost Unit Economics closes a known gap in ai practice: cost-reduction-strategies and cost-optimization exist as tactical lists. Missing: how to compute cost-per-user-action, cost-per-feature-call, gross-margin-per-AI-feature; how to set a cost ceiling; how to alert on cost runaway. ML engineers need this to defend the feature to product/finance. The methodology is anchored to the recurring activity 'Ship a new AI feature from spike to GA inside a non-AI product (role: role-ml-engineer)' and produces an auditable artefact that a downstream agent or human reviewer can sign off without re-deriving the reasoning.

## Applies If (ALL must hold)

- The triggering activity 'Ship a new AI feature from spike to GA inside a non-AI product (role: role-ml-engineer)' shows up in the user's workload at least once per cycle.
- The operator has authority to act on the artefact this methodology produces (write access, sign-off rights).
- A named consumer exists for the output — either a human reviewer or a downstream agent.
- An auditable source-of-truth is available for the inputs this methodology requires.

## Skip If (ANY kills it)

- One-off, never-to-repeat work — methodology overhead does not pay back.
- No named consumer — the artefact will be orphaned regardless of quality.
- Cannot access the input source-of-truth (system down, access denied) — paraphrased substitutes are worse than skipping.

## Prerequisites

- Read access to the systems, dashboards, or transcripts that feed the methodology's inputs.
- A storage location for the produced artefact (git repo, doc, ticket) where the consumer can read it.
- Prior cycle's artefact (if any) accessible for carry-forward and trend comparison.

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/ai/AGENTS.md` | Parent group context (vocabulary, neighbouring methodologies) |
| `pro/sdd/AGENTS.md` if present | SDD discipline for the artefact lifecycle (status flow, owners, review) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 3-5 testable rules every application enforces | ~900 |
| `content/02-output-contract.xml` | essential | Required output schema, forbidden patterns, allowed transformations | ~700 |
| `content/03-failure-modes.xml` | essential | 4-8 detector + repair clauses for known agent failures | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `inference_cost_unit_economics_template_fill` | haiku | Template fill, no judgement |
| `inference_cost_unit_economics_evidence_check` | sonnet | Bounded comparison + judgement |
| `inference_cost_unit_economics_synthesis` | opus | Cross-input synthesis + final write-up |

## Templates

| File | Purpose |
|------|---------|
| `templates/output-schema.json` | JSON Schema for the methodology's required output |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-output.py` | Enforce the output-contract before main agent accepts | After subagent returns, before commit/publish |

## Related

- parent skill: `pro/ai/` (see neighbouring methodologies)
- triggering activity: `Ship a new AI feature from spike to GA inside a non-AI product (role: role-ml-engineer)`
- external: industry references cited inline in `content/01-core-rules.xml`
