---
slug: ruby-activerecord
tier: pro
group: dev
domain: backend
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Rails ActiveRecord methodology — composable Query Objects, named scopes (no default_scope), eager-load at the controller boundary, find_each for bulk, Bullet + Prosopite N+1 gates in CI.
content_id: "bb8ac802d640c07b"
complexity: deep
produces: code
est_tokens: 4400
tags: [activerecord, rails, query-objects, orm, performance]
---
# ActiveRecord Patterns for Rails

## Summary

**One-sentence:** Rails ActiveRecord methodology — composable Query Objects, named scopes (no default_scope), eager-load at the controller boundary, find_each for bulk, Bullet + Prosopite N+1 gates in CI.

**One-paragraph:** Patterns for Rails 7+ ActiveRecord. Query Objects accept a relation in the constructor (default `Model.all`), chain methods that return `self`, and expose a terminal `results` returning the relation (never an array). Named scopes (`scope :active`) replace `default_scope`. Eager-loading happens at the controller boundary via `.includes`/`.preload`/`.eager_load`. Bulk iteration uses `find_each` / `in_batches`. CI gates N+1 with Bullet (development) + Prosopite (CI), and runs `n_plus_one_query` middleware in feature specs.

**Ефективно для:**

- Rails apps where models exceed ~150 lines and inline `where` chains scatter across controllers.
- Multi-tenant Rails apps where scopes + tenant-aware queries must be enforced consistently.
- Measured ORM hot paths (>30 % of request time in AR) — Query Objects + eager loading measurably improve.
- LLM-driven feature work where each AR query must be reviewable in isolation.
- Codebases adopting Trailblazer / dry-rb partials — Query Objects play nicely as ingest.

## Applies If (ALL must hold)

- Rails 7+ app on Ruby 3.1+.
- Codebase has ≥5 models with meaningful relations.
- Performance-sensitive endpoints in the hot path.

## Skip If (ANY kills it)

- Simple CRUD admin (Rails Admin / ActiveAdmin) — the framework manages queries.
- Rails apps under 1k LOC — direct AR scope blocks + thin controllers are fine.
- Read-replicas or sharded DBs needing raw `connected_to(role: :reading)` — query-object DSL hides the switch.
- Background workers operating on enqueued IDs via `find_each` — no benefit from a chained query object.
- Reporting / analytics — drop to `ActiveRecord::Base.connection.execute` with explicit SQL.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Model list | Markdown | data modelling |
| Filter taxonomy | Markdown | product / BA |
| N+1 gate config | YAML | platform |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[ruby-rails]] | Umbrella for controller / service layering. |
| [[decomposition-rails]] | Service / Query / Form decomposition. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 rules: query-object-relation-chain, named-scopes-no-default-scope, eager-load-at-boundary, find-each-for-bulk, no-arel-string-injection, n-plus-one-gate-in-ci | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the AR-discipline manifest + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: default-scope-invisible, query-object-god-class, view-triggered-query, all-each-memory-blowup, scope-on-query-object-bypassed | 900 |
| `content/04-procedure.xml` | essential | 5-step procedure: identify hot path → extract Query Object → eager-load at boundary → find_each for bulk → wire N+1 gate | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree mapping observable signals to a rule from 01-core-rules.xml | 700 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `extract-query-object` | sonnet | Composition design + chain shape needs judgment. |
| `audit-n-plus-one` | haiku | Mechanical scan with `ar-budget.sh`. |
| `design-bulk-job` | opus | `find_each` vs explicit batch SQL trade-off. |

## Templates

| File | Purpose |
|------|---------|
| `templates/ar-budget.sh` | CI helper running Prosopite N+1 assertions across the request spec suite. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ruby-activerecord.py` | Validate the AR-discipline manifest against the JSON Schema. | Pre-commit; CI on every methodology PR. |

## Related

- [[ruby-rails]]
- [[ruby-rails-patterns]]
- [[decomposition-rails]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (model count, hot path, batch size) to a rule from `01-core-rules.xml`. Use it before extracting a Query Object or optimising a query.
