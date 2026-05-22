---
slug: csharp-xunit-testing
tier: pro
group: dev
domain: backend
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Comprehensive testing methodology for.
content_id: "5d14054eaeb54db5"
tags: [xunit, testing, dotnet, moq, integration-tests]
---
# xUnit Testing (.NET)

## Summary

**One-sentence:** Comprehensive testing methodology for.

**One-paragraph:** Comprehensive testing methodology for .NET applications using xUnit, Moq, FluentAssertions, and WebApplicationFactory. Covers unit tests (controller + service layers), data-driven [Theory] cases, and integration tests against a real in-process HTTP host. One [Fact] or [Theory] per branch is the testable rule; constructor injection replaces setup methods.

## Applies If (ALL must hold)

- Writing unit tests for ASP.NET Core controllers, services, validators, or domain logic on .NET 6+ projects standardized on xUnit + Moq.
- Writing integration tests for API endpoints with real HTTP semantics, auth, and DI replacement.
- Backfilling characterization tests on legacy .NET code before refactoring.
- Property-based testing with FsCheck.Xunit when invariants matter (parsers, validators).
- Generating tests from a coverage report (coverlet JSON) to fill uncovered branches.

## Skip If (ANY kills it)

- Project uses MSTest or NUnit and migration is out of scope — adapt, don't add a second framework.
- UI testing for Blazor or MAUI — use bUnit or platform-specific test runners instead.
- Pure performance benchmarking — use BenchmarkDotNet; timing assertions in xUnit are unreliable.
- End-to-end HTTP across multiple deployed services — use Playwright/Postman/k6, not WebApplicationFactory.

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

- parent skill: `pro/dev/backend-enterprise/`
