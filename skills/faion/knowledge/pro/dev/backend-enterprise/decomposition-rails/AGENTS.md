# Rails Decomposition Patterns

## Summary

LLM-friendly code organization for Rails 7+ using Service Objects, Query Objects, Serializers, and Policies. One Service = one verb (`Users::CreateService#call`). Services return the domain entity or a Result monad — never void. File size budgets (Controller/Model ≤150, Service ≤100, Query ≤80 lines) are enforced by the structural lint script.

## Why

Fat models (500+ lines) and fat controllers (400+ lines) cause merge collisions when multiple agents edit in parallel, and make LLMs unable to reason about boundaries without loading the entire file. Service Objects map 1:1 to SDD tasks, are independently testable, and can be reused from queue jobs and console commands.

## When To Use

- Greenfield Rails 7+ app where LLM agents must work in small files (50-150 LOC) without fat models.
- Refactoring legacy Rails monoliths before safe agent edits are possible.
- Multi-developer or multi-agent teams with parallel work on User, Order, Billing domains.
- SDD-driven projects: one task = one Service Object.

## When NOT To Use

- Tiny Rails apps (&lt;20 controllers) — scope + thin controllers cover it; service-object ceremony costs more.
- Codebases on Trailblazer/Hanami/dry-rb — they have their own decomposition idioms; mixing produces incoherence.
- Rails Engines for shared internal libs — engine boundaries apply, not service objects.
- Hot paths (background jobs >1k/s) — service-object indirection adds GC pressure; use PORO or direct AR.
- Prototype phase where domain is unstable — locking shapes into service+form objects slows discovery.

## Content

| File | What's inside |
|------|---------------|
| `content/01-service-query-object.xml` | Service Object #call pattern with transaction, and Query Object with fluent builder. |
| `content/02-controller-pattern.xml` | Thin controller delegating to Service/Query with Serializer wrapping. |
| `content/03-rules-and-gotchas.xml` | File size guidelines and AI-agent gotchas for Rails decomposition. |

## Templates

| File | Purpose |
|------|---------|
| `templates/decomp-rails-lint.sh` | Structural lint: fail CI if Controller/Model/Service/Query/Serializer/Policy exceeds its size budget. |
