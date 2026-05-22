---
slug: ruby-rails-patterns
tier: pro
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Rails service object pattern: extract multi-step business workflows from fat controllers into app/services/BoundedContext/ActionService classes with a single call method that returns a ServiceResult (success/failure).
content_id: "57dfcf0e2bccf665"
tags: [rails, service-objects, patterns, refactoring, transactions]
---
# Rails Patterns (Service Objects)

## Summary

**One-sentence:** Rails service object pattern: extract multi-step business workflows from fat controllers into app/services/BoundedContext/ActionService classes with a single call method that returns a ServiceResult (success/failure).

**One-paragraph:** Rails service object pattern: extract multi-step business workflows from fat controllers into app/services/BoundedContext/ActionService classes with a single call method that returns a ServiceResult (success/failure).

## Applies If (ALL must hold)

- Controllers that have grown past ~100 lines and need workflow extraction
- Multi-step business operations (signup, checkout, refund) that span multiple models in one transaction
- Replacing fat-model callbacks when side effects have become unmanageable
- Standardizing controller response shapes: every action maps `ServiceResult` → HTTP status

## Skip If (ANY kills it)

- Trivial CRUD where a `before_action` + `model.save` already does the job — service objects add indirection without value
- Pure data-access logic — that belongs in Query Objects or scopes, not services
- One-off rake tasks or scripts — plain Ruby objects without the result wrapper are fine

## Prerequisites

- TBD — list concrete input artifacts and where they come from

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `TBD/path` | TBD — what upstream output this consumes |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules migrated from v1 methodology | ~800 |
| `content/02-output-contract.xml` | essential | Output schema (stub — fill from v1 patterns) | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns migrated from v1 methodology | ~800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| TBD | sonnet | TBD |

## Templates

| File | Purpose |
|------|---------|
| TBD | TBD |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| TBD | TBD | TBD |

## Related

- parent skill: `pro/dev/software-developer/`
