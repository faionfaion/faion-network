---
slug: strangler-pattern-checklist-product-dev-team
tier: geek
group: dev
domain: dev
version: 1.1.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: "Gate-by-gate checklist for a 4-12-engineer strangler migration: legacy contract freeze, ACL coverage, shadow-read window, staged traffic shift, sunset criteria."
content_id: "2ab07d3302b638de"
complexity: deep
produces: checklist
est_tokens: 3800
tags: [strangler, migration, product-dev-team, checklist, geek, dev]
---

# Strangler Pattern Checklist — Product Dev Team

## Summary

**One-sentence:** Gate-by-gate checklist for a 4-12-engineer strangler migration: legacy contract freeze, ACL coverage, shadow-read window, staged traffic shift, sunset criteria.

**One-paragraph:** Gate-by-gate checklist for a 4-12-engineer strangler migration: legacy contract freeze, ACL coverage, shadow-read window, staged traffic shift, sunset criteria. This methodology converts the inputs in Prerequisites into the artefact described in Output Contract, gated by the rules in 01-core-rules.xml and the decision tree in 06-decision-tree.xml.

**Ефективно для:** the kinds of tasks listed in 'Applies If' — primary use cases are teams shipping the artefact (`checklist`) at a deep complexity level, where the failure modes in 03-failure-modes.xml are realistic risks worth the methodology's overhead.

## Applies If (ALL must hold)

- Product team of 4-12 engineers running a migration projected to last ≥6 weeks.
- Migration crosses a data store boundary OR a service boundary.
- Team owns both the legacy and the new stack.
- Production observability is mature enough to compare legacy vs new on latency/error/business metrics.

## Skip If (ANY kills it)

- Migration is single-developer scope — use the pattern essay alone.
- No write traffic to migrate — shadow-read alone suffices.
- Vendor end-of-life within 4 weeks — emergency playbook applies, not this checklist.
- No production observability — stand it up FIRST as a separate effort.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| ACL spec | Markdown / YAML | design doc |
| Observability dashboard | Grafana / Honeycomb | platform team |
| Traffic-shift mechanism | feature flag / DNS / LB / middleware | infra |
| Migration runbook | Markdown | incident playbook |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/dev/software-developer/strangler-fig-migration-pattern` | The pattern essay; this is the team-execution complement. |
| `geek/dev/software-developer/dual-write-shadow-read-template` | Exact shape of the shadow-read gate. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples | ~700 |
| `content/03-failure-modes.xml` | essential | 3-5 antipatterns with symptom/root-cause/fix | ~800 |
| `content/04-procedure.xml` | medium | 4-6 step procedure with input/action/output per step | ~900 |
| `content/06-decision-tree.xml` | essential | Decision tree gating whether this methodology applies | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `gate_status_audit` | haiku | Deterministic check on each gate (binary). |
| `shadow_read_divergence_triage` | sonnet | Diagnose divergence root cause. |
| `traffic_shift_decision` | opus | Multi-input go/no-go at 1/10/50/100%. |

## Templates

| File | Purpose |
|------|---------|
| `templates/migration-checklist.md` | Five-gate checkbox checklist with owners/dates. |
| `templates/acl-coverage-matrix.md` | Op-by-op ACL coverage table. |
| `templates/shadow-read-divergence-log.md` | Per-day shadow-read divergence record. |
| `templates/sunset-plan.md` | Sunset criteria + named deletion-PR owner. |
| `templates/_smoke-test.md` | Minimum-viable filled-in example (smoke test). |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-strangler-pattern-checklist-product-dev-team.py` | Validate methodology output against `02-output-contract.xml` schema. | Pre-commit and CI before merge. |

## Related

- parent skill: `geek/dev/`
- `[[strangler-fig-migration-pattern]]`
- `[[dual-write-shadow-read-template]]`

## Decision tree

The decision tree at `content/06-decision-tree.xml` filters whether strangler-pattern-checklist-product-dev-team applies: root question — "Is the migration ≥6 weeks projected scope AND crosses a data store / service boundary?". Branches lead to a specific core rule (e.g., `rule:r1`) when the methodology fits, or to a `skip-this-methodology` conclusion when it does not.
