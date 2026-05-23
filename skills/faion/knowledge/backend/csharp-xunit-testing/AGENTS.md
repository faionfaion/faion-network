# xUnit Testing (.NET)

## Summary

**One-sentence:** xUnit + Moq + FluentAssertions + WebApplicationFactory testing methodology for .NET 6+ services — one Fact/Theory per branch, constructor injection, Testcontainers for the data layer.

**One-paragraph:** Comprehensive testing methodology for .NET applications using xUnit, Moq, FluentAssertions, and `WebApplicationFactory<TEntryPoint>`. Unit tests live next to the SUT (`MyApp.Tests/Features/Users/UserServiceTests.cs`). Integration tests boot the real host with Testcontainers Postgres. Constructor injection replaces `[Setup]`/`[TearDown]`. One `[Fact]` or `[Theory]` per branch. Coverage gate: line ≥ 70 %, branch ≥ 60 %, enforced by Coverlet + ReportGenerator in CI.

**Ефективно для:**

- Unit tests для ASP.NET Core controllers, services, validators on .NET 6+.
- Integration tests for API endpoints with real HTTP semantics, auth, DI replacement.
- Backfilling characterization tests on legacy .NET code before refactoring.
- Property-based testing with FsCheck.Xunit when invariants matter.
- Generating tests from coverage report (coverlet JSON) to fill uncovered branches.

## Applies If (ALL must hold)

- Writing unit tests for ASP.NET Core controllers, services, validators, or domain logic on .NET 6+ projects standardised on xUnit + Moq.
- Writing integration tests for API endpoints with real HTTP semantics, auth, and DI replacement.
- Backfilling characterisation tests on legacy .NET code before refactoring.

## Skip If (ANY kills it)

- Project uses MSTest or NUnit and migration is out of scope — adapt, don't add a second framework.
- UI testing for Blazor or MAUI — use bUnit or platform-specific test runners instead.
- Pure performance benchmarking — use BenchmarkDotNet; timing assertions in xUnit are unreliable.
- End-to-end HTTP across multiple deployed services — use Playwright / Postman / k6, not WebApplicationFactory.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Code under test | C# project | dev |
| Coverage thresholds | YAML config | platform team |
| Container runtime | Docker Engine on dev/CI hosts | platform |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[csharp-dotnet]] | Umbrella for service layout that drives test layout. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 rules: one-fact-per-branch, constructor-injection, fluentassertions-not-assert, webapplicationfactory-for-integration, testcontainers-for-db, coverage-gate-in-ci | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the test-plan manifest + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: setup-teardown-hangover, thread-sleep-in-tests, shared-mutable-fixture, assert-equals-on-collections, in-memory-db-pretending-to-be-postgres | 900 |
| `content/04-procedure.xml` | essential | 6-step procedure: scaffold test project → unit tests with Moq → integration tests with WAF → Testcontainers data layer → property tests → coverage gate | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree mapping observable signals to a rule from 01-core-rules.xml | 700 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `generate-unit-tests` | sonnet | Per-branch test synthesis from production code. |
| `generate-integration-tests` | sonnet | WAF + Testcontainers wiring needs judgment. |
| `fill-coverage-gap` | haiku | Mechanical branch enumeration against coverage JSON. |

## Templates

| File | Purpose |
|------|---------|
| `templates/controller-test.cs` | Controller unit-test skeleton with Moq. |
| `templates/integration-test.cs` | WebApplicationFactory integration-test skeleton. |
| `templates/run-tests-with-coverage.sh` | CI wrapper that runs tests + emits coverlet JSON + enforces thresholds. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-csharp-xunit-testing.py` | Validate the test-plan manifest against the JSON Schema. | Pre-commit; CI on every methodology PR. |

## Related

- [[csharp-dotnet]]
- [[csharp-entity-framework]]
- [[csharp-dotnet-patterns]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (layer under test, branch count, persistence dependency) to a rule from `01-core-rules.xml`. Use it before authoring or refactoring a test class.
