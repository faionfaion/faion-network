# ASP.NET Core Patterns

## Summary

**One-sentence:** Produces a layered ASP.NET Core 8/9 service: feature folders, IXService interfaces, EF Core repos, AutoMapper, ProblemDetails.

**One-paragraph:** Produces a layered ASP.NET Core 8/9 service: feature folders, IXService interfaces, EF Core repos, AutoMapper, ProblemDetails. Mechanism: typed input → bounded transformation → contract-checked output. The artefact carries owner + version + last_reviewed so downstream consumers can verify freshness.

**Ефективно для:**

- Новий ASP.NET Core 8/9 API з feature folders і чіткими шарами controller/service/repo.
- Async-by-default з CancellationToken прокинутим до DB layer.
- ProblemDetails (RFC 7807) як єдиний error contract.

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

| Methodology | Why |
|-------------|-----|
| [[audit-grade-api-design]] | API contract defines the controller surface |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules + rationale + source | 1200 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom + root-cause + fix | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure with input/action/output per step | 1000 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → conclusion(ref=rule-id) | 600 |

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

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-csharp-aspnet-core.py` | Validate output against 02-output-contract JSON Schema; exit 0 on pass, 1 on fail with violation list | After subagent returns, before downstream consumer reads; pre-commit |

## Related

- [[csharp-background-services]]
- [[audit-grade-api-design]]

## Decision tree

See `content/06-decision-tree.xml`. The tree routes observable signals (input shape, evidence quality, scope, stakes) to a concrete action; every leaf references a rule id from `01-core-rules.xml` so the chosen action is grounded in a testable rule. Use it when in doubt about which variant of the methodology to apply.
