# C# .NET Clean Architecture + CQRS Patterns

## Summary

**One-sentence:** Clean Architecture + CQRS for .NET 8/9 — Domain/Application/Infrastructure/API layering with MediatR Commands/Queries, NetArchTest fitness, and DDD aggregate discipline.

**One-paragraph:** Clean Architecture for .NET 8/9 with MediatR/CQRS: Domain (entities, value objects, domain events) → Application (Commands, Queries, Handlers, Validators) → Infrastructure (EF Core, configurations) → API (controllers or Minimal API, composition root only). One Command/Query per folder. Domain behaviour lives in entity methods, not Application handlers. Aggregate collections mutate only via aggregate methods. Architecture fitness — Application MUST NOT reference Infrastructure or EF Core — is enforced by NetArchTest in CI.

**Ефективно для:**

- .NET 8/9 service з 3+ aggregate roots і нетривіальною доменною логікою.
- Multi-team enterprise codebase, де Application/Domain/Infrastructure separation enables parallel work.
- Microservices з event-driven integration — domain events + outbox для cross-aggregate hand-offs.
- Codebases targeting native AOT / containerized deploys — layering trims Infrastructure deps.

## Applies If (ALL must hold)

- .NET 8/9 service with non-trivial domain (3+ aggregate roots, multiple bounded contexts, business rules beyond CRUD).
- Multi-team enterprise codebase where Application/Domain/Infrastructure separation enables parallel work.
- Microservices with event-driven integration — domain events + MediatR Notification pattern for cross-aggregate hand-offs.

## Skip If (ANY kills it)

- Simple CRUD apps (<20 endpoints, no business rules) — four projects are pure overhead.
- Lambda/Functions with cold-start budget — DI graph + MediatR add 100-300ms startup; use Minimal API + direct DbContext.
- Teams unfamiliar with DDD — the pattern's value depends on rich domain models; without that you get a layered anaemic codebase.
- Pure read-side services (reporting, dashboards) — CQRS is overkill; one project with `SELECT` queries is fine.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Bounded-context map | text or diagram | DDD workshop |
| Aggregate / entity list | Markdown table | domain modelling |
| Use-case catalogue | command/query list | product / BA |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[csharp-dotnet]] | Umbrella covering CancellationToken plumbing + DI lifetimes. |
| [[csharp-entity-framework]] | Infrastructure layer EF Core patterns. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 rules: layer-direction, behaviour-in-entities, one-command-per-folder, validators-on-commands, outbox-for-cross-aggregate, mediatr-reserved-for-cross-cutting | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the layered-solution manifest + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 7 antipatterns: anaemic-regression, layer-leakage, in-transaction-domain-events, mediatr-overuse, collection-mutated-outside-aggregate, ignore-query-filters-leak, async-void-handler | 900 |
| `content/04-procedure.xml` | essential | 6-step procedure: solution skeleton → Domain → Application → Infrastructure → API → NetArchTest gate | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree mapping observable signals to a rule from 01-core-rules.xml | 700 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-solution` | sonnet | Multi-project generation with layer references. |
| `add-command-handler` | sonnet | Light judgment on validator scope + handler boundaries. |
| `enforce-arch-fitness` | haiku | Mechanical NetArchTest verification. |
| `design-domain-event-flow` | opus | Tx-vs-outbox reasoning across aggregates. |

## Templates

| File | Purpose |
|------|---------|
| `templates/arch-tests.cs` | NetArchTest fitness suite enforcing layer direction. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-csharp-dotnet-patterns.py` | Validate the layered-solution manifest against the JSON Schema. | Pre-commit; CI on every methodology PR. |

## Related

- [[csharp-dotnet]]
- [[csharp-entity-framework]]
- [[csharp-xunit-testing]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (domain richness, team count, deploy target, CRUD ratio) to a rule from `01-core-rules.xml`. Use it before scaffolding to decide whether Clean Architecture or a flatter layout fits.
