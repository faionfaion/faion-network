---
slug: iac-patterns-dry
tier: pro
group: infra
domain: infra
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "DRY rubric (config) for IaC repos: when to factor (rule of three), for_each over copy-paste, locals + module inputs, env-overlay via tfvars/Pulumi stack config."
content_id: "59b4afe953f1d219"
complexity: medium
produces: rubric
est_tokens: 3200
tags: [iac, terraform, dry, for-each, locals]
---
# IaC DRY Patterns

## Summary

**One-sentence:** DRY rubric (config) for IaC repos: when to factor (rule of three), for_each over copy-paste, locals + module inputs, env-overlay via tfvars/Pulumi stack config.

**One-paragraph:** DRY rubric (config) for IaC repos: when to factor (rule of three), for_each over copy-paste, locals + module inputs, env-overlay via tfvars/Pulumi stack config. The methodology pins the discipline that turns folklore into a reviewable, owned, version-controlled operating artefact: rule-bound output contract, evidence anchors, named owner, published review cadence. Outputs of the wrong shape are rejected at review; outputs without evidence are demoted to hypotheses; outputs without owners are tagged stale.

## Applies If (ALL must hold)

- Spotting >= 3 near-identical resource blocks in the same root.
- Adding a new environment cloned from an existing one.
- Standardising tags / labels across modules.
- Auditing a codebase for copy-paste fatigue.

## Skip If (ANY kills it)

- Two-environment project where DRY would add abstraction with no payoff.
- Resource blocks differ in essentially every field (false DRY trigger).

**Ефективно для:**

- Repo з 5+ env (regions / tenants).
- Tagging policies що повторюються 100+ разів.
- Networks з 4+ subnet tiers повторюваної форми.
- Multi-tenant SaaS provisioning.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| IaC repo + tool | repo | team |
| List of duplicated blocks | audit doc | team |
| Module ownership map | RACI | platform team |
| Variable / locals naming convention | doc | team |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/infra/infrastructure-engineer/iac-patterns-module-design` | Module shape rules. |

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
| `templates/rubric.json` | Rubric skeleton matching the output schema. |
| `templates/_smoke-test.json` | Minimum viable filled artefact. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-iac-patterns-dry.py` | Validate artefact against the JSON Schema in `content/02-output-contract.xml`. Stdlib-only. | CI on artefact change; pre-commit. |

## Related

- [[iac-patterns-composition]]
- [[iac-patterns-module-design]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, evidence presence, owner presence, cadence status) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
