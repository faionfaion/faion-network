---
slug: csharp-xunit-testing
tier: pro
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: xUnit is the de facto standard test framework for modern.
content_id: "5d14054eaeb54db5"
tags: [csharp, xunit, testing, moq, unit-testing]
---
# xUnit Testing for .NET

## Summary

**One-sentence:** xUnit is the de facto standard test framework for modern.

**One-paragraph:** xUnit is the de facto standard test framework for modern .NET applications. Write controller tests via WebApplicationFactory, service unit tests using Moq, and integration tests with AAA (Arrange-Act-Assert) layout. Parameterize tests with [Theory] and [InlineData], and enforce test isolation via IClassFixture for shared resources. Measure coverage with coverlet.collector and use FluentAssertions for readable diffs.

## Applies If (ALL must hold)

- ASP.NET Core / .NET class library projects — xUnit is the de facto default in modern templates.
- Controller / minimal-API tests via WebApplicationFactory for in-process integration.
- Service / domain unit tests using Moq, NSubstitute, or FakeItEasy.
- Property-based tests (FsCheck.Xunit) and theory-based parametric tests with [Theory] + [InlineData].
- CI gates with coverage thresholds via coverlet.collector + ReportGenerator.

## Skip If (ANY kills it)

- BDD-flavored prose specs preferred — SpecFlow / Reqnroll integrate but xUnit isn't the showcase format.
- Browser end-to-end — use Playwright .NET / Selenium harnesses instead.
- Performance benchmarks — use BenchmarkDotNet, not xUnit timing assertions.
- Microbenchmarks of allocations / GC behavior — use BenchmarkDotNet.
- Tests that need a shared mutable singleton across the entire run — xUnit isolates classes by default; use IClassFixture / ICollectionFixture deliberately.

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

- parent skill: `pro/dev/software-developer/`
