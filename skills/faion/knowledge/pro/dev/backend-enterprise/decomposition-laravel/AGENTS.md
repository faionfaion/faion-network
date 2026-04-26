# Laravel Decomposition Patterns

## Summary

LLM-friendly code organization for Laravel using the Action + DTO + Form Request + Resource + Policy pattern. One Action = one verb; DTOs derive from Form Requests; controllers stay under 80 lines. Requires PHP 8.1+ for readonly constructor promotion. File size budgets (Controller ≤150, Action ≤100, DTO ≤40 lines) are enforced by the structural lint script.

## Why

Fat controllers (500+ lines) cause merge collisions when multiple agents edit the same file and make it impossible for LLMs to reason about boundaries. Small, single-purpose Action classes map 1:1 to SDD tasks and are independently testable. DTO `fromRequest()` decouples the Action from HTTP so it can be reused from queue jobs and console commands.

## When To Use

- Greenfield Laravel project where LLM agents must extend the codebase without re-reading 500-line controllers.
- Refactoring legacy "fat controller / fat model" apps before letting agents touch them.
- Multi-developer or multi-agent parallel work where separate feature Actions avoid merge collisions.
- SDD-driven projects: one task = one Action class.

## When NOT To Use

- Tiny CRUD admin tools (&lt;20 endpoints) — Action/DTO ceremony costs more than the readability gain.
- Prototype phase where the domain is unstable — locking shapes into DTOs slows discovery.
- Teams without PHP 8.1+ — readonly constructor promotion is load-bearing for the DTO pattern.
- Codebases already using a consistent pattern (e.g., pure Service-class style) — mixing styles is worse than picking one.

## Content

| File | What's inside |
|------|---------------|
| `content/01-action-dto.xml` | Action and DTO patterns with DB::transaction, fromRequest, and return-entity rule. |
| `content/02-controller-pattern.xml` | Thin controller using Action injection, authorize(), and Resource wrapping. |
| `content/03-rules-and-gotchas.xml` | File size guidelines, AI-agent gotchas, and enforcement rules. |

## Templates

| File | Purpose |
|------|---------|
| `templates/decomp-lint.sh` | Structural lint: fail CI if any Controller/Model/Action/Service/DTO exceeds its size budget. |
