---
slug: php-eloquent
tier: pro
group: dev
domain: dev
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Use Eloquent (Laravel's ActiveRecord ORM) idiomatically: query scopes, eager loading, mass-assignment guards, attribute casting, and explicit transactions.
content_id: "20906c4347c5fc36"
complexity: medium
produces: code
est_tokens: 5200
tags: [laravel, eloquent, orm, php, active-record]
---
# PHP Eloquent ORM Patterns

## Summary

**One-sentence:** Use Eloquent (Laravel's ActiveRecord ORM) idiomatically: query scopes, eager loading, mass-assignment guards, attribute casting, and explicit transactions.

**One-paragraph:** Eloquent is a productive ORM but easy to misuse — N+1 queries via lazy loading inside loops, mass-assignment vulnerabilities from unguarded `Model::create`, hidden side effects from observers, and lost data integrity when transactions are absent. Use query scopes for reusable WHERE logic, `with()` / `load()` for eager loading, `$fillable` / `$guarded` for mass-assignment safety, `$casts` for attribute typing, and `DB::transaction` for multi-write consistency.

**Ефективно для:**

- Laravel 10/11/12 проєкти з Eloquent — потрібен ідіоматичний read/write pattern.
- Refactor де N+1 queries вбивають latency (виявлено Telescope/Debugbar).
- Greenfield models — щоб одразу мати $fillable + $casts + scopes.
- Audit mass-assignment vulnerabilities у legacy code.

## Applies If (ALL must hold)

- Laravel project using Eloquent (Active Record models).
- Models have associations (hasMany / belongsTo / morphMany).
- Performance matters (organic traffic / paid acquisition).
- Team uses Eloquent in services (not raw query builder everywhere).

## Skip If (ANY kills it)

- Project standardized on Doctrine (data mapper) instead of Eloquent — different methodology.
- Read-only reports queries where Query Builder is more direct.
- Trivial app with 1-2 models and no associations.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Model + migration | Eloquent class + migration file | domain model |
| Query usage map | list of Model::query() call sites | code scan |
| Debugbar/Telescope output | N+1 detection report | dev tools |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[php-laravel]] | Laravel basics (services, providers) assumed. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: fillable-or-guarded-required, casts-for-typed-attrs, eager-load-in-services, scope-for-reused-where, tx-for-multi-write | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for code + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix | 900 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | 900 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `harden-model` | sonnet | Templated $fillable + $casts. |
| `design-scopes` | opus | Naming scopes is domain-judgment. |
| `detect-n-plus-one` | haiku | Mechanical scan of foreach + relation access. |

## Templates

| File | Purpose |
|------|---------|
| `templates/Order.php` | Eloquent model with $fillable, $casts, scopes, and typed relations |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-php-eloquent.py` | Validate the Eloquent model artefact against the schema | Pre-commit + CI |
| `scripts/eloquent-n-plus-one-audit.sh` | Lint missing ->with() before foreach over Eloquent collections | Pre-commit + CI |

## Related

- [[php-laravel]]
- [[php-laravel-patterns]]
- [[php-laravel-queues]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, stack, runtime, scale, etc.) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
