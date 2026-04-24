# Agent Integration — xUnit Testing (.NET)

## When to use
- Generating unit tests for ASP.NET Core controllers, services, validators, or domain logic where the project is on .NET 6+ and standardized on xUnit + Moq + FluentAssertions.
- Writing integration tests via `WebApplicationFactory<TEntryPoint>` for API endpoints with realistic HTTP semantics, auth, and DI replacement.
- Backfilling characterization tests on legacy .NET code before refactoring; xUnit's `[Theory]` + `[InlineData]`/`MemberData` is well-suited to data-driven coverage.
- Property-based testing with FsCheck.Xunit when invariants matter (parsers, validators, money math).

## When NOT to use
- The project uses MSTest or NUnit and migrating is out of scope — adapt the methodology rather than introducing a second test framework.
- UI testing for Blazor or MAUI — use bUnit or specific UI test runners; xUnit is only the host.
- Pure performance benchmarking — use BenchmarkDotNet, not xUnit timing assertions.
- End-to-end HTTP across multiple deployed services — use Playwright/Postman/k6, not in-process WebApplicationFactory.

## Where it fails / limitations
- `WebApplicationFactory` shares state across `[Fact]`s in the same `IClassFixture`; agents that generate tests assuming isolation will produce flaky cross-test contamination — instruct the agent to seed/reset DB per test or use `Respawn`.
- Moq generates verbose "Expression tree may not contain..." errors when stubbing extension methods or non-virtual members; agents should detect this and recommend wrapping in an interface.
- xUnit runs tests in parallel by default within a collection; database-touching tests need `[Collection("DB")]` or `DisablePerTestCollectionParallelization`.
- LLM tends to assert on `Assert.True(condition)` without messages — produces useless failure output. Force `Assert.Equal(expected, actual)` or FluentAssertions `.Should().Be()`.
- Generated mocks frequently over-specify (`.Verify(... Times.Once)` on calls that are implementation detail), which makes refactoring brittle.

## Agentic workflow
Spawn a Claude subagent per controller/service to generate `<TypeName>Tests.cs` from the SUT and any existing DTOs. The agent reads the source, identifies public methods + branches, emits Arrange-Act-Assert tests using xUnit + Moq, and runs `dotnet test` in a sandboxed worktree to verify they compile and pass before reporting back. Coverage gaps are a separate sonnet pass that reads the `coverlet` JSON output and proposes additional `[Theory]` cases.

### Recommended subagents
- `faion-sdd-executor-agent` — drives the test-write/run/fix loop with quality gates (compile → run → coverage threshold → commit).
- `faion-backend-agent` (referenced in README) — domain-aware test generation when the SUT has rich business rules.
- A custom `dotnet-test-runner` agent scoped to `Bash(dotnet test:*)`, `Read`, `Edit` only — minimal blast radius for the inner test loop.

### Prompt pattern
```
Generate xUnit tests for <path/to/Service.cs>. Use Moq for IRepository,
FluentAssertions for assertions. Cover: happy path, validation failure,
not-found, concurrency conflict. One [Fact] or [Theory] per branch.
Run `dotnet test --filter FullyQualifiedName~<TestClass>` and fix until green.
Do not assert on Moq.Verify unless the call is part of the public contract.
```

```
Read coverlet.json. Find lines in <Service.cs> with hit count 0.
For each uncovered branch, emit one new [Theory] case with InlineData.
Re-run dotnet test; report final line + branch coverage.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `dotnet test` | Run xUnit tests, filter, collect coverage | bundled with .NET SDK |
| `coverlet.collector` | Cross-platform coverage (lcov, opencover, json) | `dotnet add package coverlet.collector` |
| `dotnet-reportgenerator-globaltool` | Convert coverage to HTML | `dotnet tool install -g dotnet-reportgenerator-globaltool` |
| `Stryker.NET` | Mutation testing for .NET | `dotnet tool install -g dotnet-stryker` |
| `Respawn` | Reset DB between integration tests | `dotnet add package Respawn` |
| `Verify.Xunit` | Snapshot testing | `dotnet add package Verify.Xunit` |
| `Bogus` | Realistic test data | `dotnet add package Bogus` |
| `Testcontainers` | Real Postgres/Redis/etc. in tests | `dotnet add package Testcontainers.PostgreSql` |
| `dotnet-format` | Format generated test files | `dotnet tool install -g dotnet-format` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| GitHub Actions `dotnet test` | SaaS CI | Yes | Standard `setup-dotnet` + `dotnet test --collect:"XPlat Code Coverage"`. |
| Codecov / Coveralls | SaaS | Yes | Upload lcov/opencover; agents can post PR comments via GH API. |
| Azure DevOps Test Plans | SaaS | Partial | Useful for human QA; less agent-friendly than raw `dotnet test`. |
| SonarCloud / SonarQube | SaaS / OSS | Yes | Consumes opencover; agent can fail PR on coverage drop. |
| Stryker dashboard | SaaS | Yes | Mutation score over time; CLI uploads JSON. |

## Templates & scripts
See `templates.md` for `[Fact]` / `[Theory]` skeletons and `WebApplicationFactory` setup. Helper script for an agent loop:

```bash
#!/usr/bin/env bash
# run-tests-with-coverage.sh - agent entry point
set -euo pipefail
PROJ="${1:?test project path}"
dotnet test "$PROJ" \
  --collect:"XPlat Code Coverage" \
  --results-directory ./TestResults \
  --logger "trx;LogFileName=test_results.trx" \
  /p:Threshold=80 /p:ThresholdType=line /p:ThresholdStat=total
COV=$(find TestResults -name 'coverage.cobertura.xml' | head -1)
reportgenerator -reports:"$COV" -targetdir:./coverage -reporttypes:JsonSummary
jq '.summary.linecoverage' coverage/Summary.json
```

## Best practices
- One assertion concept per test; multiple `Assert.Equal` for the same logical claim is fine, but split when claims diverge.
- Prefer constructor injection in test classes over `[Fact]` setup methods — xUnit creates a new instance per test, so the constructor IS the setup.
- Use `IClassFixture<T>` for expensive setup (DB, WebApplicationFactory); `ICollectionFixture` only when sharing across classes.
- Replace `DateTime.UtcNow` with an `IClock` interface before generating tests — otherwise tests are non-deterministic and agents will produce flaky `Assert.Equal` on timestamps.
- Snapshot tests (`Verify`) excel for large DTO/JSON outputs; instruct agents to use them instead of dozens of `Assert.Equal` lines.
- Tag slow integration tests with `[Trait("Category", "Integration")]` and run them in a separate CI stage.

## AI-agent gotchas
- Agents auto-generate `_mock.Setup(...)` for every dependency call, including ones the SUT may not actually invoke; require the agent to verify by reading the SUT first, not by guessing from method signatures.
- Generated `[Theory]` data sometimes duplicates the same logical case in multiple `InlineData` rows — add a dedup pass.
- LLMs default to `async void` test methods on older patterns; xUnit requires `async Task` — pin this in the prompt.
- WebApplicationFactory tests need `Program.cs` to be `public partial class Program {}` for .NET 6+ minimal hosting; agent should detect and add a `internal class Program` workaround or the `<InternalsVisibleTo>` entry.
- Human-in-loop checkpoint: review any test that uses `Thread.Sleep` or polling — these are almost always wrong; use `TaskCompletionSource` or `IHostApplicationLifetime` instead.
- When using Testcontainers, agents forget to add `IAsyncLifetime` for setup/teardown — container leaks across runs.

## References
- xUnit docs: https://xunit.net/docs/getting-started/netcore/cmdline
- ASP.NET Core integration tests: https://learn.microsoft.com/aspnet/core/test/integration-tests
- FluentAssertions: https://fluentassertions.com/introduction
- Stryker.NET: https://stryker-mutator.io/docs/stryker-net/introduction/
- Testcontainers for .NET: https://dotnet.testcontainers.org/
- Mark Seemann, "Unit Testing Patterns" (Pluralsight) — for non-brittle Moq usage
