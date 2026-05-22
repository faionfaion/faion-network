---
slug: model-upgrade-migration-playbook
tier: pro
group: ai
domain: ai-core
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Model Upgrade Migration Playbook: codified ai practice that turns the recurring 'role-ml-engineer/Migrate an AI feature across a model upgrade without breaking users' decision into a repeatable, auditable artefact.
content_id: "a0069e8a0b17038e"
tags: [model-upgrade-migration-playbook, ai, pro]
---
# Model Upgrade Migration Playbook

## Summary

**One-sentence:** Model Upgrade Migration Playbook: codified ai practice that turns the recurring 'role-ml-engineer/Migrate an AI feature across a model upgrade without breaking users' decision into a repeatable, auditable artefact.

**One-paragraph:** Model Upgrade Migration Playbook addresses the gap identified by the role-ml-engineer/Migrate an AI feature across a model upgrade without breaking users playbook: Model deprecations and silent behavior shifts (Claude 4.6→4.7, GPT-4o sunset, embedding model versions) happen quarterly. No methodology walks the engineer through inventory → diff → adapt → cutover. This is a universal pain point. Mechanism: a typed input → bounded transformation → contract-checked output. Primary output: a versioned artefact (decision record, checklist, score, or report) that downstream tasks can consume without re-deriving the rationale.

## Applies If (ALL must hold)

- task is an instance of role-ml-engineer/Migrate an AI feature across a model upgrade without breaking users OR a closely-adjacent variant
- the operator has the artefacts named in Prerequisites available before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == pro or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working artefact for this gap — replace, do not duplicate
- the change being decided is greenfield prototype with no production users
- regulatory / compliance context overrides any in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the role-ml-engineer/Migrate an AI feature across a model upgrade without breaking users task (last 30 days)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/ai/ml-engineer` | parent role skill — provides the operating context for this methodology |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: r1-bound-scope, r2-typed-input, r3-named-owner, r4-versioned, r5-traceable-decision | ~900 |
| `content/02-output-contract.xml` | essential | Required fields, forbidden patterns, allowed transformations | ~700 |
| `content/03-failure-modes.xml` | essential | 5 failure modes with detector + repair | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft_inputs_summary` | haiku | Template fill, bounded transformation |
| `synthesize_decision` | sonnet | Per-instance judgment; bounded inputs |
| `review_for_compliance` | opus | Cross-input synthesis when stakes are high |

## Templates

| File | Purpose |
|------|---------|
| `templates/model-upgrade-migration-playbook.json` | JSON schema for the Model Upgrade Migration Playbook output contract |
| `templates/model-upgrade-migration-playbook.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-model-upgrade-migration-playbook.py` | Enforce Model Upgrade Migration Playbook output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `pro/ai/ml-engineer/`
- upstream playbook: `role-ml-engineer/Migrate an AI feature across a model upgrade without breaking users`
