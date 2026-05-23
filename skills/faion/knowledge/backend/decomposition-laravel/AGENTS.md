# Laravel Decomposition Patterns

## Summary

**One-sentence:** LLM-friendly Laravel decomposition — Action + DTO + FormRequest + Resource + Policy, one verb per Action, controllers ≤150 lines, enforced by a structural lint.

**One-paragraph:** LLM-friendly code organisation for Laravel using Action + DTO + FormRequest + Resource + Policy. One Action = one verb (`CreateUserAction`); DTOs derive from FormRequests via readonly constructor promotion (PHP 8.1+); controllers stay under 150 lines and only call Actions; Resources list fields explicitly; Policies handle authorization. File-size budgets (Controller ≤150, Action ≤100, DTO ≤40) and namespace whitelist (`App\Actions`, `App\DTOs`, `App\Policies`, `App\Http\Resources`) are enforced by `templates/decomp-lint.sh` in CI.

**Ефективно для:**

- Greenfield Laravel projects where LLM agents must extend the codebase without re-reading 500-line controllers.
- Refactoring legacy "fat controller / fat model" apps before letting agents touch them.
- Multi-developer or multi-agent parallel work where separate Actions avoid merge collisions.
- SDD-driven projects: one task = one Action class.

## Applies If (ALL must hold)

- Greenfield Laravel project where LLM agents must extend the codebase without re-reading 500-line controllers.
- Refactoring legacy "fat controller / fat model" apps before letting agents touch them.
- Multi-developer or multi-agent parallel work where separate feature Actions avoid merge collisions.

## Skip If (ANY kills it)

- Tiny CRUD admin tools (<20 endpoints) — Action/DTO ceremony costs more than the readability gain.
- Prototype phase where the domain is unstable — locking shapes into DTOs slows discovery.
- Teams without PHP 8.1+ — readonly constructor promotion is load-bearing for the DTO pattern.
- Codebases already using a consistent pattern (e.g., pure Service-class style) — mixing styles is worse than picking one.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Use-case catalogue | Markdown verb list | product / BA |
| Allowed-namespace policy | text | ADR |
| File-size budgets | YAML | platform |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[php-laravel]] | Sub-module covering controller / service / queue patterns. |
| [[laravel-patterns]] | Sibling on Service-class layer when needed. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 rules: one-verb-per-action, dto-readonly-from-formrequest, controllers-only-call-actions, explicit-resource-fields, namespace-whitelist, action-returns-result | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the structural-lint manifest + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 6 antipatterns: pattern-collapse, dto-drift, resource-field-leak, action-void-return, manager-coordinator-handler, action-calling-action | 900 |
| `content/04-procedure.xml` | essential | 5-step procedure: namespace scaffolding → Action per verb → DTO + FormRequest pair → Resource fields → Policy + lint | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree mapping observable signals to a rule from 01-core-rules.xml | 700 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `extract-action-from-controller` | sonnet | Reading legacy controller + extracting verb logic. |
| `generate-dto-from-formrequest` | sonnet | Field mapping requires judgment. |
| `run-decomp-lint` | haiku | Mechanical file-size + namespace check. |

## Templates

| File | Purpose |
|------|---------|
| `templates/decomp-lint.sh` | Structural-lint script enforcing file-size budgets + namespace whitelist. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-decomposition-laravel.py` | Validate the structural-lint manifest against the JSON Schema. | Pre-commit; CI on every methodology PR. |

## Related

- [[php-laravel]]
- [[laravel-patterns]]
- [[php-laravel-patterns]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (endpoint count, PHP version, prototype-vs-product, agent involvement) to a rule from `01-core-rules.xml`. Use it before adopting or skipping the decomposition convention.
