---
slug: decomposition-rails
tier: pro
group: dev
domain: backend
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: LLM-friendly Rails 7+ decomposition — Service Objects, Query Objects, Form Objects, Policies, Serializers — narrow concerns, canonical return shape, enforced by a structural lint.
content_id: "ec9c8fa0e62f069a"
complexity: medium
produces: code
est_tokens: 3900
tags: [rails, ruby, decomposition, service-object, query-object]
---
# Rails Decomposition Patterns

## Summary

**One-sentence:** LLM-friendly Rails 7+ decomposition — Service Objects, Query Objects, Form Objects, Policies, Serializers — narrow concerns, canonical return shape, enforced by a structural lint.

**One-paragraph:** LLM-friendly code organisation for Rails 7+ using Service Objects (`app/services/`), Query Objects (`app/queries/`), Form Objects (`app/forms/`), Policies (`app/policies/`, Pundit) and Serializers (`app/serializers/`). Service Objects expose a single `call` method returning a canonical Result or entity (never `void`). Query Objects compose existing model scopes — they MUST NOT re-implement filters. Form Objects use `ActiveModel::Model`; Serializers list attributes explicitly. The namespace whitelist + file-size budgets are enforced by `templates/decomp-rails-lint.sh` in CI.

**Ефективно для:**

- Greenfield Rails project where LLM agents extend the codebase without re-reading 500-line controllers.
- Refactoring legacy "fat ActiveRecord model" apps before agent contributions.
- Multi-developer or multi-agent parallel work where separate services avoid merge collisions.
- SDD-driven projects: one task = one Service / Query / Form.

## Applies If (ALL must hold)

- Greenfield Rails 7+ project with LLM agent contributions.
- Refactoring legacy fat-model / fat-controller apps before agent contributions.
- Multi-developer codebase that needs parallel work without merge collisions.

## Skip If (ANY kills it)

- Tiny CRUD admin tools (<20 endpoints) — Service / Query ceremony costs more than the readability gain.
- Codebases on Trailblazer / Hanami / dry-rb — they have their own decomposition idioms; mixing produces incoherence.
- Hot paths (>1k jobs/s) — service-object indirection adds GC pressure; use POROs or direct AR.
- Prototype phase with unstable domain — locking shapes slows discovery.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Use-case catalogue | Markdown verb list | product / BA |
| Allowed-namespace policy | text | ADR |
| Standard Service return shape (Result vs entity-or-raise) | text | ADR |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[ruby-rails]] | Sub-module covering controller / model patterns. |
| [[ruby-activerecord]] | Scope discipline that Query Objects build on. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 rules: service-call-returns-result, query-objects-reuse-scopes, form-uses-activemodel, serializer-explicit-attributes, namespace-whitelist, policy-scope-on-find | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the structural-lint manifest + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 6 antipatterns: service-explosion, return-shape-drift, concern-dumping-ground, form-service-overlap, scope-drift, update-columns-bypass | 900 |
| `content/04-procedure.xml` | essential | 5-step procedure: scaffold namespaces → service per verb → query per filter set → form per input shape → policy + lint | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree mapping observable signals to a rule from 01-core-rules.xml | 700 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `extract-service-from-controller` | sonnet | Reading legacy controller + extracting verbs. |
| `build-query-object` | sonnet | Scope composition needs judgment. |
| `run-decomp-rails-lint` | haiku | Mechanical file-size + namespace check. |

## Templates

| File | Purpose |
|------|---------|
| `templates/decomp-rails-lint.sh` | Structural lint enforcing file-size budgets + namespace whitelist. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-decomposition-rails.py` | Validate the structural-lint manifest against the JSON Schema. | Pre-commit; CI on every methodology PR. |

## Related

- [[ruby-rails]]
- [[ruby-rails-patterns]]
- [[ruby-activerecord]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (endpoint count, existing convention, prototype-vs-product, model fatness) to a rule from `01-core-rules.xml`. Use it before extracting services or query objects.
