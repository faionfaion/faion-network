# Agent Integration — xUnit Testing (.NET)

## When to use
- ASP.NET Core / .NET class library projects — xUnit is the de facto default in modern templates.
- Controller / minimal-API tests via `WebApplicationFactory<Program>` for in-process integration.
- Service / domain unit tests using Moq, NSubstitute, or `FakeItEasy`.
- Property-based tests (FsCheck.Xunit) and theory-based parametric tests with `[Theory]` + `[InlineData]`.
- CI gates with coverage thresholds via `coverlet.collector` + ReportGenerator.

## When NOT to use
- BDD-flavored prose specs preferred — SpecFlow / Reqnroll integrate but xUnit isn't the showcase format.
- Browser end-to-end — use Playwright .NET / Selenium harnesses instead.
- Performance benchmarks — use `BenchmarkDotNet`, not xUnit timing assertions.
- Microbenchmarks of allocations / GC behavior — same as above.
- Tests that need a shared mutable singleton across the entire run — xUnit isolates classes by default; use `IClassFixture<T>` / `ICollectionFixture<T>` deliberately.

## Where it fails / limitations
- xUnit creates a new test class instance per test method by design. Agents that initialize expensive deps in the constructor pay the cost N times — must use `IClassFixture<T>` for shared setup.
- `[Theory]` with class data: complex generators are hard to debug; `MemberData` parameters that aren't `IEnumerable<object[]>` produce confusing errors.
- `WebApplicationFactory<Program>` requires `public partial class Program;` at the bottom of `Program.cs`. Without it the test host can't find the entry point — message is opaque.
- In-memory DB providers (`UseInMemoryDatabase`) silently skip relational constraints; tests pass that would fail in Postgres/SQL Server. Prefer SQLite-in-memory or Testcontainers.
- Async test methods that return `void` (instead of `Task`) are silently swallowed by xUnit.
- Parallel test execution is on by default at the assembly level — shared static state (caches, `HttpClient` singletons in tests) causes flakes.

## Agentic workflow
A subagent generates a test class adjacent to the implementation it covers, picks the appropriate fixture (`IClassFixture<WebApplicationFactory<Program>>` for HTTP tests, plain class for unit tests), and parameterizes via `[Theory]` where the same logic is exercised over many inputs. Quality gates: `dotnet test --collect:"XPlat Code Coverage"`, threshold check via Coverlet, and `dotnet format --verify-no-changes`. The agent must not mark tests `[Skip = "TODO"]` to make CI green.

### Recommended subagents
- `faion-sdd-executor-agent` — locks tests to features as a quality gate.
- `faion-feature-executor` — sequential slice work; tests come with each slice.

### Prompt pattern
```
Add xUnit test class <Name>Tests in tests/<Project>.Tests covering <SUT>. Use Moq for collaborators, AAA layout, [Fact] for one-shot cases, [Theory]+[InlineData] for parametric. For HTTP-touching tests use IClassFixture<WebApplicationFactory<Program>> with overridden DbContext to SQLite-in-memory. Run dotnet test --filter <Name> and report failures.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `dotnet test` | Test runner; supports `--filter`, `--collect`, `--logger` | Built-in |
| `dotnet new xunit` | Scaffold a test project | Built-in |
| `coverlet.collector` | Code coverage in-process | NuGet |
| `coverlet.msbuild` | MSBuild-driven coverage | NuGet |
| `ReportGenerator` | HTML coverage report | `dotnet tool install --global dotnet-reportgenerator-globaltool` |
| `Moq`, `NSubstitute`, `FakeItEasy` | Mocking | NuGet |
| `FluentAssertions` | Readable assertions (`.Should().BeEquivalentTo(...)`) | NuGet |
| `AutoFixture` | Auto-generated test data | NuGet |
| `Verify` | Snapshot testing | NuGet |
| `Testcontainers.PostgreSql/MsSql` | Real DBs in tests | NuGet |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| GitHub Actions `setup-dotnet` + caching | SaaS | Yes | Standard CI for .NET. |
| Azure DevOps / Codecov | SaaS | Yes | Upload `coverage.cobertura.xml`. |
| WireMock.Net | OSS | Yes | HTTP mocking for outgoing calls. |
| Bogus | OSS | Yes | Fake data generator (Faker for .NET). |
| Stryker.NET | OSS | Yes | Mutation testing. |
| Aspire test harness | OSS | Yes | Orchestrates real deps in integration tests (.NET 8+). |
| Sentry / Application Insights | SaaS | Yes | Optional: capture test logs/exceptions for triage. |

## Templates & scripts
See templates.md and README (Controller Tests + Integration Tests). Inline `WebApplicationFactory` override pattern for swapping DB to SQLite-in-memory:

```csharp
public class TestAppFactory : WebApplicationFactory<Program>
{
    protected override void ConfigureWebHost(IWebHostBuilder builder)
    {
        builder.ConfigureServices(services =>
        {
            services.RemoveAll(typeof(DbContextOptions<AppDbContext>));
            var conn = new SqliteConnection("DataSource=:memory:");
            conn.Open();
            services.AddDbContext<AppDbContext>(o => o.UseSqlite(conn));
            using var scope = services.BuildServiceProvider().CreateScope();
            scope.ServiceProvider.GetRequiredService<AppDbContext>().Database.EnsureCreated();
        });
    }
}
```

## Best practices
- AAA (Arrange-Act-Assert) layout, with blank-line separators — easy for both humans and agents to scan.
- Prefer `FluentAssertions` for readable diffs (`actual.Should().BeEquivalentTo(expected)`).
- Use `[Theory]` + `[InlineData]` for boundary tests; `MemberData`/`ClassData` only when generation is non-trivial.
- Avoid `Thread.Sleep`; use `await Task.Delay` only in genuinely time-dependent code, or `TimeProvider` (.NET 8+) abstraction.
- Hide `WebApplicationFactory<Program>` behind a `TestAppFactory` class so all integration tests share configuration — DRY and consistent.
- Per-test database isolation: use Respawn or fresh SQLite-in-memory per test class.
- Run `dotnet test --blame --blame-hang-timeout 60s` in CI to catch hangs.
- Keep coverage threshold realistic (70-85%); chasing 100% via trivial tests degrades quality.

## AI-agent gotchas
- Agents return `async void` from `[Fact]` methods occasionally — exceptions are unobserved and the test "passes". Compiler doesn't warn for tests. Reject `async void` test methods in code review.
- Constructor-initialized resources: agents put `new HttpClient()` in the test class constructor; xUnit creates the class N times → resource exhaustion. Use `IClassFixture` / `IAsyncLifetime`.
- `Moq` `Setup` chains with non-matching argument matchers silently return `default` — leading to false-positive null asserts. Use `It.Is<T>(...)` precisely or strict mocks.
- `WebApplicationFactory<Program>` test fails: usually missing `public partial class Program;`. Pre-flight check should ensure this is present in `Program.cs`.
- Parallel collisions: agents reuse a static `Faker` or shared collection. Add `[CollectionDefinition(DisableParallelization = true)]` only when necessary; better — make shared state per-instance.
- Human checkpoint: review every `[Fact(Skip = "...")]`; agents add these to "fix later" and they rot. CI should fail on skipped tests by default.
- `IDisposable`/`IAsyncDisposable`: agents implement only `IDisposable` for tests that hold async resources, leading to subtle hangs. Prefer `IAsyncLifetime` for async setup/teardown.

## References
- https://xunit.net/docs/getting-started/netcore/cmdline
- https://learn.microsoft.com/aspnet/core/test/integration-tests
- https://github.com/fluentassertions/fluentassertions
- https://github.com/AutoFixture/AutoFixture
- https://stryker-mutator.io/docs/stryker-net
