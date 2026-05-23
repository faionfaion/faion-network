---
slug: feature-sunset-and-deprecation
tier: pro
group: product
domain: product
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Feature Sunset And Deprecation delivers a concrete, testable methodology that turns the recurring task of 'Validate an AI feature before it consumes a quarter' into an auditable artefact, addressing the gap: Product-lifecycle and technical-debt-management touch this but no method
content_id: "74a66979cf915ee6"
complexity: medium
produces: spec
est_tokens: 4400
tags: [product, pro, method, methodology]
---
# Feature Sunset And Deprecation

## Summary

**One-sentence:** Feature Sunset And Deprecation delivers a concrete, testable methodology that turns the recurring task of 'Validate an AI feature before it consumes a quarter' into an auditable artefact, addressing the gap: Product-lifecycle and technical-debt-management touch this but no methodology covers the full sunset playbook: usage forensics, migration path design, user comms cadence, internal stakeholder negotiation, post-sunset audit. PMs avoid this work because the playbook is missing.

**One-paragraph:** Product-lifecycle and technical-debt-management touch this but no methodology covers the full sunset playbook: usage forensics, migration path design, user comms cadence, internal stakeholder negotiation, post-sunset audit. PMs avoid this work because the playbook is missing. Feature Sunset And Deprecation closes this gap with a small set of hard rules, a strict output contract, and a failure-mode catalogue tuned for LLM-assisted execution. The methodology is anchored to the triggering work 'Validate an AI feature before it consumes a quarter' (role-product-manager, pro tier). It produces a structured artefact that a downstream agent or human reviewer can sign off without re-deriving the reasoning.

**Ефективно для:**

- Feature accumulates негативний ROI, але stakeholders бояться його видалити.
- PM потребує deprecation criteria, comms-плану, та migration window як артефакт.
- Product-lifecycle література touches це, але немає конкретного методологічного output.

## Applies If (ALL must hold)

- The triggering activity 'Validate an AI feature before it consumes a quarter' (role: role-product-manager) is in your current workload at least once per cycle.
- You have authority to act on the artefact this methodology produces (write access, sign-off rights).
- A named consumer exists for the artefact — human reviewer OR downstream agent.
- An auditable source-of-truth is available for the inputs the methodology needs.

## Skip If (ANY kills it)

- One-off, never-to-repeat work — methodology overhead does not pay back.
- No named consumer — artefact will be orphaned regardless of quality.
- Cannot access the input source-of-truth (system down, access denied) — paraphrased substitutes are worse than skipping.

## Prerequisites

- Read access to the systems / dashboards / docs that feed the methodology's inputs.
- A storage location for the produced artefact (git repo, doc, ticket) where the consumer can read it.
- Prior cycle's artefact (if any) accessible for carry-forward and trend comparison.

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/product/AGENTS.md` | Parent group context (vocabulary, neighbouring methodologies) |
| `pro/sdd/AGENTS.md` if present | SDD discipline for the artefact lifecycle (status flow, owners, review) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules grounded in the cited gap | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples | 700 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with symptom/root-cause/fix | 900 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | 800 |
| `content/05-examples.xml` | medium | One worked example end-to-end | 700 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `feature_sunset_and_deprecation_template_fill` | haiku | Template fill, no judgment |
| `feature_sunset_and_deprecation_evidence_check` | sonnet | Bounded comparison + judgment |
| `feature_sunset_and_deprecation_synthesis` | opus | Cross-input synthesis + final write-up |

## Templates

| File | Purpose |
|------|---------|
| `templates/feature-sunset-and-deprecation.md` | Filled artefact skeleton conforming to 02-output-contract.xml |
| `templates/feature-sunset-and-deprecation.schema.json` | JSON Schema for the artefact (mirrors content/02-output-contract.xml) |
| `templates/_smoke-test.md` | Minimum-viable filled-in version exercised by scripts/validate-feature-sunset-and-deprecation.py --self-test |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-feature-sunset-and-deprecation.py` | Validate artefact against 02-output-contract.xml schema. Exit 0/1/2. | After subagent returns; pre-commit on artefact change. |

## Related

- parent skill: `pro/product/` (see neighbouring methodologies)
- triggering activity: `role-product-manager/Validate an AI feature before it consumes a quarter`
- external: industry references cited inline in `content/01-core-rules.xml`

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (preconditions hold, inputs typed, rules pass) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it before producing the artefact to confirm the methodology applies and the rules pass.
