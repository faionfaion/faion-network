---
slug: iac-patterns-composition
tier: pro
group: infra
domain: infra
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Module composition rubric (config): root vs leaf modules, dependency graph rules, output contracts, inter-module data passing without circular refs."
content_id: "35f90377a3a7fc4e"
complexity: medium
produces: config
est_tokens: 3400
tags: [iac, terraform, modules, composition, patterns]
---
# IaC Module Composition Patterns

## Summary

**One-sentence:** Module composition rubric (config): root vs leaf modules, dependency graph rules, output contracts, inter-module data passing without circular refs.

**One-paragraph:** Module composition rubric (config): root vs leaf modules, dependency graph rules, output contracts, inter-module data passing without circular refs. The methodology pins the discipline that turns folklore into a reviewable, owned, version-controlled operating artefact: rule-bound output contract, evidence anchors, named owner, published review cadence. Outputs of the wrong shape are rejected at review; outputs without evidence are demoted to hypotheses; outputs without owners are tagged stale.

## Applies If (ALL must hold)

- Combining >= 3 modules in a root configuration.
- Refactoring a flat IaC project into root + leaf modules.
- Adding a new shared module (network/IAM/audit) used by multiple roots.
- Resolving a circular-dependency error between modules.

## Skip If (ANY kills it)

- Single-file main.tf project - no composition needed yet.
- Inside-module refactor (use iac-patterns-module-design instead).

**Ефективно для:**

- Multi-root монорепа з shared modules.
- Network + IAM + workload разом у одному root.
- Інтеграції з registry modules (HashiCorp / private).
- Декомпозиція моноліту після першого incident.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| IaC tool + state remote | tool | platform team |
| Module dependency map | doc | team |
| Naming conventions (slug) | doc | team |
| Registry for shared modules | registry | platform team |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/infra/infrastructure-engineer/iac-patterns-module-design` | Per-module shape rules. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid/forbidden examples | 900 |
| `content/03-failure-modes.xml` | essential | Antipatterns with symptom / root-cause / fix | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure to apply the methodology end-to-end | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals -> rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-config` | haiku | Mechanical template fill from prerequisites table. |
| `populate-policy` | sonnet | Per-clause translation into config fields with judgment. |
| `review-breach-cases` | opus | Cross-engagement risk + failure-mode synthesis. |

## Templates

| File | Purpose |
|------|---------|
| `templates/config.json` | Config skeleton matching the output schema. |
| `templates/_smoke-test.json` | Minimum viable filled artefact. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-iac-patterns-composition.py` | Validate artefact against the JSON Schema in `content/02-output-contract.xml`. Stdlib-only. | CI on artefact change; pre-commit. |

## Related

- [[iac-patterns-module-design]]
- [[iac-patterns-dry]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, evidence presence, owner presence, cadence status) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
