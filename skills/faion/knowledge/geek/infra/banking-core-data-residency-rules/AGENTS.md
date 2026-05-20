---
slug: banking-core-data-residency-rules
tier: geek
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Banking Core Data Residency Rules: codified platform / SRE practice that turns the recurring 'p4-outsource-specialist/FinTech / HIPAA compliance audit prep (4 weeks)' decision into a repeatable, auditable artefact.
content_id: "6057aaf5ee98b6cb"
tags: [banking-core-data-residency-rules, infra, geek]
---
# Banking Core Data Residency Rules

## Summary

**One-sentence:** Banking Core Data Residency Rules: codified platform / SRE practice that turns the recurring 'p4-outsource-specialist/FinTech / HIPAA compliance audit prep (4 weeks)' decision into a repeatable, auditable artefact.

**One-paragraph:** Banking Core Data Residency Rules addresses the gap identified by the p4-outsource-specialist/FinTech / HIPAA compliance audit prep (4 weeks) playbook: Banking-core projects collide with EU / UK / APAC residency rules. faion's cloud-architecture material does not enumerate residency constraints per regulator. Mechanism: a typed input → bounded transformation → contract-checked output. Primary output: a versioned artefact (decision record, checklist, score, or report) that downstream tasks can consume without re-deriving the rationale.

## Applies If (ALL must hold)

- task is an instance of p4-outsource-specialist/FinTech / HIPAA compliance audit prep (4 weeks) OR a closely-adjacent variant
- the operator has the artefacts named in Prerequisites available before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == geek or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working artefact for this gap — replace, do not duplicate
- the change being decided is greenfield prototype with no production users
- regulatory / compliance context overrides any in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the p4-outsource-specialist/FinTech / HIPAA compliance audit prep (4 weeks) task (last 30 days)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/infra/devops-engineer` | parent role skill — provides the operating context for this methodology |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 4 testable rules: r1-bound-scope, r2-typed-input, r3-named-owner, r4-versioned | ~900 |
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
| `templates/banking-core-data-residency-rules.json` | JSON schema for the Banking Core Data Residency Rules output contract |
| `templates/banking-core-data-residency-rules.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-banking-core-data-residency-rules.py` | Enforce Banking Core Data Residency Rules output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `geek/infra/`
- upstream playbook: `p4-outsource-specialist/FinTech / HIPAA compliance audit prep (4 weeks)`
