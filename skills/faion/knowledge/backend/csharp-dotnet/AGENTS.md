# C# .NET Core Backend Development

## Summary

**One-sentence:** Greenfield ASP.NET Core 8/9 service umbrella — controllers, services, EF Core, xUnit, BackgroundService — with DI lifetimes, CancellationToken plumbing, and feature folders.

**One-paragraph:** Greenfield ASP.NET Core 8/9 services integrate layered controller/service/repository architecture, Entity Framework Core for data access, xUnit for unit and integration testing, and BackgroundService for async work. All async methods accept CancellationToken. Configure DI to register DbContext as scoped, hosted services as singleton, and resolve scoped dependencies inside background services via `IServiceProvider.CreateScope()`. Use AutoMapper to project entities to DTOs. Return ProblemDetails for errors. Organize by feature folders (`Features/Users/`) not technical layers. This umbrella aggregates sibling methodologies (`csharp-aspnet-core`, `csharp-entity-framework`, `csharp-xunit-testing`, `csharp-background-services`) — edits should land in those subdirs for module coherence.

**Ефективно для:**

- Greenfield ASP.NET Core 8/9 service: REST/gRPC API, EF Core data layer, xUnit tests, BackgroundService for async work.
- Brownfield .NET Framework → .NET 8 migration — agent needs one map of patterns across controllers, EF, tests, hosted services.
- Internal enterprise APIs where DI, options pattern, and configuration binding are part of the contract.
- Code reviews that must enforce CancellationToken plumbing and DI lifetime correctness across the codebase.

## Applies If (ALL must hold)

- Greenfield ASP.NET Core 8/9 service: REST/gRPC API, EF Core data layer, xUnit tests, BackgroundService for async work.
- Brownfield .NET Framework → .NET 8 migration where the agent needs a single map of patterns covering controllers, EF, tests, and hosted services.
- Internal enterprise APIs where DI, options pattern, and configuration binding are part of the contract.

## Skip If (ANY kills it)

- Tiny CLI utilities — `dotnet new console` is enough; agents should not impose Controller/Service/Repository on a 200-line script.
- Highly dynamic plugin systems — F# or scripting is a better fit; .NET reflection-heavy plugin loading trips up codegen.
- Functional/event-sourced cores — use F# or a CQRS framework (MediatR + Marten/EventStore) directly; this umbrella's Repository pattern fights that grain.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| API contract / endpoint list | OpenAPI YAML or Markdown | product / API design |
| Entity model | ERD or Markdown table | data modelling |
| Target .NET version | `8.0` / `9.0` | platform team |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[csharp-aspnet-core]] | Sub-module for controller/middleware patterns. |
| [[csharp-entity-framework]] | Sub-module for EF Core data layer. |
| [[csharp-xunit-testing]] | Sub-module for testing layering. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules: cancellation-token-plumbing, di-lifetimes, no-sync-over-async, ef-asnotracking-on-reads, problemdetails-errors, feature-folder-layout | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the produced project skeleton + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 7 antipatterns with symptom/root-cause/fix (async void, sync-over-async, scoped-in-singleton, missing-await, migrations-on-shared-db, mapperly-non-partial, automapper-misregistered) | 900 |
| `content/04-procedure.xml` | essential | 6-step procedure: scaffold → DI → controllers/services → EF layer → tests → BackgroundService | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree mapping observable signals to a rule from 01-core-rules.xml | 700 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-project` | sonnet | Multi-file generation with judgment on feature folders. |
| `add-controller-action` | sonnet | Layered code with CancellationToken plumbing. |
| `review-async-discipline` | haiku | Mechanical scan for sync-over-async + missing CancellationToken. |
| `design-background-service` | opus | DI lifetime trap reasoning. |

## Templates

| File | Purpose |
|------|---------|
| `templates/Program.cs` | Minimal-hosting Program.cs with DI registration, ProblemDetails, hosted services. |
| `templates/FeatureController.cs` | REST controller skeleton with CancellationToken on every action. |
| `templates/BackgroundProcessor.cs` | BackgroundService skeleton that resolves scoped deps via `IServiceScopeFactory`. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-csharp-dotnet.py` | Validate the project-skeleton manifest against the JSON Schema in 02-output-contract.xml. | Pre-commit; CI on every methodology PR. |

## Related

- [[csharp-aspnet-core]]
- [[csharp-entity-framework]]
- [[csharp-xunit-testing]]
- [[csharp-background-services]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (service vs CLI, request shape, dependency lifetimes, async-vs-sync IO) to a concrete rule from `01-core-rules.xml`. Use it when in doubt about whether the methodology applies and which layering rule wins.
