# ASP.NET Core Patterns

## Summary

**One-sentence:** Produces a layered ASP.NET Core 8/9 service: feature folders, IXService interfaces, EF Core repos, AutoMapper, ProblemDetails.

**One-paragraph:** Produces a layered ASP.NET Core 8/9 service: feature folders and IXService interfaces, scoped DbContext, CancellationToken threaded to every EF Core call, ProblemDetails (RFC 7807) from a single global IExceptionHandler, record DTOs mapped at the service boundary, TimeProvider instead of DateTime.UtcNow, AsNoTracking + eager .Include() on reads, keyset pagination, explicit transactions on multi-step writes, and WebApplicationFactory + Testcontainers for integration tests. Mechanism: typed input → bounded transformation → contract-checked output. The artefact carries owner + version + last_reviewed so downstream consumers can verify freshness.

**Ефективно для:**

- Новий ASP.NET Core 8/9 API з feature folders і чіткими шарами controller/service/repo.
- Async-by-default з CancellationToken прокинутим до DB layer.
- ProblemDetails (RFC 7807) як єдиний error contract.
- Ревʼю PR-диффа на captive DbContext, зворотний порядок middleware і повернення tracked-ентіті з сервісу.
- Дисципліна запитів EF Core: AsNoTracking, eager .Include(), keyset-пагінація, явні транзакції.
- Інтеграційні тести на WebApplicationFactory + Testcontainers замість EF InMemory.

## Applies If (ALL must hold)

- New ASP.NET Core 8/9 API with clear controller/service/repository separation.
- Migrating legacy ASP.NET MVC or WCF services to modern Web API.
- Multi-tenant or B2B SaaS in .NET where DI scopes and middleware are central.
- Codebase shared between humans and LLMs — explicit interfaces stabilize completions.

## Skip If (ANY kills it)

- Tiny internal tool or webhook with <10 endpoints — Minimal APIs suffice.
- Microservice that publishes only to a queue — three layers around one method is overkill.
- gRPC-only service — service-method-per-RPC layering is more appropriate.
- App on .NET Framework 4.x — Generic Host, async-by-default, DI assumptions do not hold.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| .NET 8 or 9 SDK | tool | dev environment |
| Feature scope brief | markdown | product |
| Data model decision (EF Core vs Dapper) | markdown | architecture |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[audit-grade-api-design]] | API contract defines the controller surface |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 16 testable rules + skip rule, each with rationale + source | 2200 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) incl. optional `design_profile` + valid/invalid examples + forbidden patterns | 1300 |
| `content/03-failure-modes.xml` | essential | 12 antipatterns with symptom + detector + root-cause + fix | 1400 |
| `content/04-procedure.xml` | essential | 7-step procedure with input/action/output per step | 1300 |
| `content/05-examples.xml` | essential | Controller / service / IExceptionHandler / transaction examples + end-to-end trace | 1400 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → conclusion(ref=rule-id) | 900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-skeleton` | haiku | Mechanical template emission |
| `wire-feature-logic` | sonnet | Per-feature judgment with bounded inputs |
| `audit-output` | sonnet | Verify rules in 01-core-rules.xml hold |

## Templates

| File | Purpose |
|------|---------|
| `templates/dotnet-gate.sh` | CI gate script enforcing async hygiene and coverage threshold |
| `templates/feature-folder-skeleton.cs` | Feature folder skeleton with controller/service/repo/dto |
| `templates/_smoke-test.cs` | Minimum viable feature: Users CRUD with auth + ProblemDetails |
| `templates/problem-details-handler.cs` | .NET 8+ IExceptionHandler mapping domain exceptions to RFC 7807 |
| `templates/prompt-aspnet-slice.txt` | Prompt skeleton for scaffolding one compliant vertical slice |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-csharp-aspnet-core.py` | Validate output against 02-output-contract JSON Schema; exit 0 on pass, 1 on fail with violation list | After subagent returns, before downstream consumer reads; pre-commit |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[csharp-background-services]]
- [[audit-grade-api-design]]

## Decision tree

See `content/06-decision-tree.xml`. The tree routes observable signals (input shape, evidence quality, scope, stakes) to a concrete action; every leaf references a rule id from `01-core-rules.xml` so the chosen action is grounded in a testable rule. Use it when in doubt about which variant of the methodology to apply.
