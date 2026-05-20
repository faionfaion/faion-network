---
slug: audit-grade-api-design
tier: pro
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Audit Grade Api Design: codified engineering practice that turns the recurring 'p4-outsource-specialist/Compliance-Grade Feature Delivery (FinTech / HIPAA / PCI)' decision into a repeatable, auditable artefact.
content_id: "c0137e72f0e07379"
tags: [audit-grade-api-design, dev, pro]
---
# Audit Grade Api Design

## Summary

**One-sentence:** Audit Grade Api Design: codified engineering practice that turns the recurring 'p4-outsource-specialist/Compliance-Grade Feature Delivery (FinTech / HIPAA / PCI)' decision into a repeatable, auditable artefact.

**One-paragraph:** Audit Grade Api Design addresses the gap identified by the p4-outsource-specialist/Compliance-Grade Feature Delivery (FinTech / HIPAA / PCI) playbook: Existing api-contract-first and api-versioning sit in solo tier and cover happy-path REST. Outsource specialists in FinTech/banking-core need explicit audit-fields (actor, on_behalf_of, request_id, evidence_ref), immutable append-only event endpoints, regulator-friendly idempotency semantics, and signed-payload contracts. No methodology covers this today. Mechanism: a typed input → bounded transformation → contract-checked output. Primary output: a versioned artefact (decision record, checklist, score, or report) that downstream tasks can consume without re-deriving the rationale.

## Applies If (ALL must hold)

- task is an instance of p4-outsource-specialist/Compliance-Grade Feature Delivery (FinTech / HIPAA / PCI) OR a closely-adjacent variant
- the operator has the artefacts named in Prerequisites available before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == pro or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working artefact for this gap — replace, do not duplicate
- the change being decided is greenfield prototype with no production users
- regulatory / compliance context overrides any in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the p4-outsource-specialist/Compliance-Grade Feature Delivery (FinTech / HIPAA / PCI) task (last 30 days)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/dev/software-developer` | parent role skill — provides the operating context for this methodology |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: r1-bound-scope, r2-typed-input, r3-named-owner, r4-versioned, r5-contract-first | ~900 |
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
| `templates/audit-grade-api-design.json` | JSON schema for the Audit Grade Api Design output contract |
| `templates/audit-grade-api-design.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-audit-grade-api-design.py` | Enforce Audit Grade Api Design output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `pro/dev/`
- upstream playbook: `p4-outsource-specialist/Compliance-Grade Feature Delivery (FinTech / HIPAA / PCI)`
