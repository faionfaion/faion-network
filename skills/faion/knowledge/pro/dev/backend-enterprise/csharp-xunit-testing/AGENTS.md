# xUnit Testing (.NET)

## Summary

Comprehensive testing methodology for .NET applications using xUnit, Moq, FluentAssertions,
and WebApplicationFactory. Covers unit tests (controller + service layers), data-driven
`[Theory]` cases, and integration tests against a real in-process HTTP host. One `[Fact]`
or `[Theory]` per branch is the testable rule; constructor injection replaces setup methods.

## Why

xUnit creates a new class instance per test, making the constructor the natural setup
point and eliminating shared-state bugs. `WebApplicationFactory<TEntryPoint>` spins up a
real ASP.NET Core pipeline without a listening socket, giving integration tests realistic
HTTP semantics (auth, DI, routing) at unit-test speed. FluentAssertions produces readable
failure messages that reduce debugging overhead compared to raw `Assert.Equal`.

## When To Use

- Writing unit tests for ASP.NET Core controllers, services, validators, or domain logic
  on .NET 6+ projects standardized on xUnit + Moq.
- Writing integration tests for API endpoints with real HTTP semantics, auth, and DI replacement.
- Backfilling characterization tests on legacy .NET code before refactoring.
- Property-based testing with FsCheck.Xunit when invariants matter (parsers, validators).
- Generating tests from a coverage report (`coverlet` JSON) to fill uncovered branches.

## When NOT To Use

- Project uses MSTest or NUnit and migration is out of scope — adapt, don't add a second framework.
- UI testing for Blazor or MAUI — use bUnit or platform-specific test runners instead.
- Pure performance benchmarking — use BenchmarkDotNet; timing assertions in xUnit are unreliable.
- End-to-end HTTP across multiple deployed services — use Playwright/Postman/k6, not WebApplicationFactory.

## Content

| File | What's inside |
|------|---------------|
| `content/01-unit-tests.xml` | Controller unit test patterns: Arrange-Act-Assert, Moq setup, result-type assertions. |
| `content/02-integration-tests.xml` | WebApplicationFactory integration tests, test isolation, parallel collection rules. |
| `content/03-rules-and-gotchas.xml` | Agent-critical rules: async Task, Moq limits, shared state, coverage loop. |

## Templates

| File | Purpose |
|------|---------|
| `templates/controller-test.cs` | `[Fact]` + `[Theory]` skeleton for a controller under test with Moq. |
| `templates/integration-test.cs` | `IClassFixture<WebApplicationFactory<Program>>` integration test skeleton. |
| `templates/run-tests-with-coverage.sh` | Agent entry point: run tests, collect coverlet output, report line coverage. |
