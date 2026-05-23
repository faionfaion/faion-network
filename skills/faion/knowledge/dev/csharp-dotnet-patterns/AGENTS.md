# C# .NET Patterns

## Summary

**One-sentence:** Clean architecture + CQRS-with-MediatR + rich domain model patterns for .NET 8 services; rejects anaemic models, public setters, and entity leakage.

**One-paragraph:** Layered .NET solutions slip into anaemic-domain + service-locator + entity-leak antipatterns when scaling beyond one team. This methodology pins clean-architecture boundaries (Domain — Application — Infrastructure — Web), CQRS via MediatR (one handler per command/query, no service classes), and Bean Validation at the API edge. Public setters on entities are forbidden; behaviour lives on aggregates per `[[ddd-aggregates]]`. Output: a feature folder structured per the contract in `02-output-contract.xml`.

**Ефективно для:**

- Multi-team .NET solutions where layer boundaries decay over time.
- CQRS-style services with explicit command/query split.
- Codebases adopting MediatR/FastEndpoints for handler dispatch.
- Domain-rich projects where invariants must live on the entity.
- AI-generated code review — antipatterns catch agent regressions.

## Applies If (ALL must hold)

- .NET 8+ project with clean-architecture intent (separate Domain/Application/Infrastructure projects).
- MediatR (or equivalent) installed for CQRS dispatch.
- DDD vocabulary already shared across the team.
- Reviewers willing to enforce no-public-setter discipline.

## Skip If (ANY kills it)

- CRUD prototype with no behaviour worth encapsulating.
- Single-developer hobby project — overhead exceeds benefit.
- Team rejects MediatR; route to bare ASP.NET Core feature folder per `[[csharp-dotnet]]`.
- Legacy .NET Framework codebase — migrate to .NET 8 first.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Feature spec | Markdown | ticket / SDD task |
| Existing solution layout | .sln + project graph | repo |
| Ubiquitous language glossary | Markdown | domain owner |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[csharp-dotnet]] | Base ASP.NET Core conventions this layers on. |
| [[ddd-aggregates]] | Aggregate root + invariant rules referenced by the patterns. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: clean-arch-layers, cqrs-handler-per-message, rich-domain-no-setters, edge-validation, no-entity-in-api | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for feature folder + valid/invalid examples | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: anaemic-domain, controller-with-logic, entity-as-dto, mediatr-hallucination | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure: split layers → command + handler → aggregate behaviour → DTOs → tests | ~700 |
| `content/06-decision-tree.xml` | essential | Routing tree on team-size + behaviour-richness → rule | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `partition-into-layers` | sonnet | Judgment on boundaries. |
| `write-handler-and-aggregate` | sonnet | C# scaffolding. |
| `review-for-antipatterns` | sonnet | Pattern-match against failure modes. |

## Templates

| File | Purpose |
|------|---------|
| `templates/Handler.cs` | MediatR `IRequestHandler` skeleton |
| `templates/Aggregate.cs` | Aggregate root with no public setters |
| `templates/feature-folder.md` | Folder layout reference |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-csharp-dotnet-patterns.py` | Validate feature-folder spec against schema | Pre-commit on spec artefact |

## Related

- [[csharp-dotnet]]
- [[ddd-aggregates]]
- [[ddd-value-objects]]
- [[cqrs-pattern]]
- parent skill: `pro/dev/software-developer/`

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (team size, behaviour richness, CQRS adoption) to a rule from `01-core-rules.xml`. Use it whenever a new feature joins the .NET solution to decide whether clean-architecture + CQRS layering is justified or whether a flat feature folder per `[[csharp-dotnet]]` is enough.
