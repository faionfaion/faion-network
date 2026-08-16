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

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[csharp-dotnet]] | Umbrella for service layout that drives test layout. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 10 rules: one-fact-per-branch, constructor-injection, fluentassertions-not-assert, async-task-return, class-fixture-required, theory-for-params, precise-mock-matchers, webapplicationfactory-for-integration, testcontainers-for-db, coverage-gate-in-ci | 1800 |
| `content/02-output-contract.xml` | essential | JSON Schema for the test-plan manifest incl. per-class fixture + per-method naming and return shape, with valid/invalid examples | 1100 |
| `content/03-failure-modes.xml` | essential | 8 antipatterns: setup-teardown-hangover, thread-sleep-in-tests, shared-mutable-fixture, assert-equals-on-collections, inmemory-db-pretending-to-be-postgres, async-void-test, parallel-state-collision, web-factory-program-not-public | 1300 |
| `content/04-procedure.xml` | essential | 6-step procedure: scaffold test project → unit tests with Moq → integration tests with WAF → Testcontainers data layer → property tests → coverage gate | 1100 |
| `content/05-examples.xml` | essential | Program shim, service unit test, controller integration test with a substituted DbContext, final manifest | 1300 |
| `content/06-decision-tree.xml` | essential | Layer router + flat defect router mapping signals to a rule from 01-core-rules.xml | 1000 |

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
| `templates/service-test.cs` | Service unit test with precise Moq matchers, `Verify`, `[Theory]` rows and FluentAssertions. |
| `templates/test-app-factory.cs` | Derived `WebApplicationFactory` substituting the DbContext with SQLite-in-memory, plus the test class using it. |
| `templates/ProgramPartial.cs` | The `public partial class Program { }` shim `WebApplicationFactory<Program>` needs. |
| `templates/run-tests-with-coverage.sh` | CI wrapper that runs tests + emits coverlet JSON + enforces thresholds. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-csharp-xunit-testing.py` | Validate the test-plan manifest against the JSON Schema. | Pre-commit; CI on every methodology PR. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[csharp-dotnet]]
- [[csharp-entity-framework]]
- [[csharp-dotnet-patterns]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (layer under test, branch count, persistence dependency) to a rule from `01-core-rules.xml`. Use it before authoring or refactoring a test class.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/controller-test.cs`

```csharp
// Controller unit test skeleton using xUnit + Moq + FluentAssertions
// Replace: TService, TController, TDto, CreateDto, RouteValues as needed

using FluentAssertions;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Logging;
using Moq;
using Xunit;

namespace MyApp.Tests.Controllers;

public class ExampleControllerTests
{
    private readonly Mock<IExampleService> _mockService;
    private readonly ExampleController _controller;

    public ExampleControllerTests()
    {
        _mockService = new Mock<IExampleService>();
        _controller = new ExampleController(
            _mockService.Object,
            Mock.Of<ILogger<ExampleController>>()
        );
    }

    [Fact]
    public async Task GetById_WhenFound_ReturnsOkWithDto()
    {
        // Arrange
        var dto = new ExampleDto { Id = 1, Name = "Test" };
        _mockService.Setup(s => s.GetByIdAsync(1)).ReturnsAsync(dto);

        // Act
        var result = await _controller.GetById(1);

        // Assert
        var ok = Assert.IsType<OkObjectResult>(result.Result);
        ok.Value.Should().BeEquivalentTo(dto);
    }

    [Fact]
    public async Task GetById_WhenNotFound_ReturnsNotFound()
    {
        _mockService.Setup(s => s.GetByIdAsync(999)).ReturnsAsync((ExampleDto?)null);
        var result = await _controller.GetById(999);
        Assert.IsType<NotFoundResult>(result.Result);
    }

    [Theory]
    [InlineData("", "Name is required")]
    [InlineData("x", "Name too short")]
    public async Task Create_WithInvalidName_ReturnsBadRequest(string name, string expectedError)
    {
        var dto = new CreateExampleDto { Name = name };
        var result = await _controller.Create(dto);
        var bad = Assert.IsType<BadRequestObjectResult>(result.Result);
        bad.Value?.ToString().Should().Contain(expectedError);
    }
}
```

### `templates/integration-test.cs`

```csharp
// Integration test skeleton using WebApplicationFactory
// Requires: public partial class Program {} in Program.cs (minimal hosting)
// Requires: Respawn NuGet for DB reset between tests

using Microsoft.AspNetCore.Mvc.Testing;
using System.Net;
using System.Net.Http.Json;
using Xunit;

namespace MyApp.Tests.Integration;

[Collection("Integration")]
public class ExampleApiTests : IClassFixture<WebApplicationFactory<Program>>
{
    private readonly HttpClient _client;

    public ExampleApiTests(WebApplicationFactory<Program> factory)
    {
        _client = factory.CreateClient();
    }

    [Fact]
    public async Task GetList_ReturnsSuccessWithJsonContentType()
    {
        var response = await _client.GetAsync("/api/v1/examples");
        response.EnsureSuccessStatusCode();
        Assert.Equal("application/json; charset=utf-8",
            response.Content.Headers.ContentType?.ToString());
    }

    [Fact]
    public async Task Create_WithValidData_ReturnsCreated()
    {
        var dto = new CreateExampleDto { Name = "Integration Test" };
        var response = await _client.PostAsJsonAsync("/api/v1/examples", dto);
        Assert.Equal(HttpStatusCode.Created, response.StatusCode);

        var created = await response.Content.ReadFromJsonAsync<ExampleDto>();
        Assert.NotNull(created);
        Assert.Equal("Integration Test", created.Name);
    }
}

// Tag DB-touching tests to prevent parallel execution
[CollectionDefinition("Integration", DisableParallelization = true)]
public class IntegrationCollection { }
```

### `templates/run-tests-with-coverage.sh`

```bash
# run-tests-with-coverage.sh — agent entry point for test + coverage loop
# Usage: bash run-tests-with-coverage.sh <test-project-path> [threshold]
# Example: bash run-tests-with-coverage.sh MyApp.Tests/ 80
set -euo pipefail

PROJ="${1:?test project path required}"
THRESHOLD="${2:-80}"

dotnet test "$PROJ" \
  --collect:"XPlat Code Coverage" \
  --results-directory ./TestResults \
  --logger "trx;LogFileName=test_results.trx" \
  /p:Threshold="$THRESHOLD" /p:ThresholdType=line /p:ThresholdStat=total

COV=$(find TestResults -name 'coverage.cobertura.xml' | head -1)
if [[ -z "$COV" ]]; then
  echo "No coverage file found" >&2; exit 1
fi

reportgenerator \
  -reports:"$COV" \
  -targetdir:./coverage \
  -reporttypes:JsonSummary

jq '.summary.linecoverage' coverage/Summary.json
```

### `templates/service-test.cs`

```csharp
using FluentAssertions;
using Moq;

namespace Faion.Tests;

public sealed class OrdersServiceTests
{
    private readonly Mock<IOrderRepository> _repo = new();
    private readonly OrdersService _svc;

    public OrdersServiceTests()
    {
        _svc = new OrdersService(_repo.Object);
    }

    [Fact]
    public async Task GetAsync_ExistingOrder_ReturnsDto()
    {
        _repo.Setup(r => r.GetAsync(It.Is<int>(id => id == 1), It.IsAny<CancellationToken>()))
             .ReturnsAsync(new Order(1, "Alice", 10m));

        var result = await _svc.GetAsync(1, CancellationToken.None);

        result.Should().BeEquivalentTo(new OrderResponse(1, "Alice", 10m));
        _repo.Verify(r => r.GetAsync(1, It.IsAny<CancellationToken>()), Times.Once);
    }

    [Theory]
    [InlineData(0)]
    [InlineData(-5)]
    public async Task GetAsync_NonPositiveId_Throws(int id)
    {
        var act = () => _svc.GetAsync(id, CancellationToken.None);
        await act.Should().ThrowAsync<ArgumentOutOfRangeException>();
    }
}

public interface IOrderRepository { Task<Order?> GetAsync(int id, CancellationToken ct); }
public sealed record Order(int Id, string CustomerName, decimal Total);
public sealed record OrderResponse(int Id, string CustomerName, decimal Total);
public sealed class OrdersService
{
    private readonly IOrderRepository _r;
    public OrdersService(IOrderRepository r) => _r = r;
    public async Task<OrderResponse?> GetAsync(int id, CancellationToken ct)
    {
        if (id <= 0) throw new ArgumentOutOfRangeException(nameof(id));
        var o = await _r.GetAsync(id, ct);
        return o is null ? null : new OrderResponse(o.Id, o.CustomerName, o.Total);
    }
}
```


### `templates/test-app-factory.cs`

```csharp
using System.Net;
using System.Net.Http.Json;
using FluentAssertions;
using Microsoft.AspNetCore.Mvc.Testing;
using Microsoft.Data.Sqlite;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.DependencyInjection;

namespace Faion.Tests;

public sealed class OrdersControllerTests : IClassFixture<TestAppFactory>
{
    private readonly HttpClient _client;

    public OrdersControllerTests(TestAppFactory factory) => _client = factory.CreateClient();

    [Fact]
    public async Task Get_ExistingId_Returns200()
    {
        var response = await _client.GetAsync("/api/orders/1");
        response.StatusCode.Should().Be(HttpStatusCode.OK);
        var dto = await response.Content.ReadFromJsonAsync<OrderResponse>();
        dto.Should().BeEquivalentTo(new OrderResponse(1, "Alice", 10m));
    }

    [Theory]
    [InlineData(0, HttpStatusCode.NotFound)]
    [InlineData(99, HttpStatusCode.NotFound)]
    public async Task Get_MissingId_Returns404(int id, HttpStatusCode expected)
    {
        var response = await _client.GetAsync($"/api/orders/{id}");
        response.StatusCode.Should().Be(expected);
    }
}

public sealed class TestAppFactory : WebApplicationFactory<Program>
{
    private readonly SqliteConnection _conn = new("DataSource=:memory:");

    protected override void ConfigureWebHost(IWebHostBuilder builder)
    {
        _conn.Open();
        builder.ConfigureServices(services =>
        {
            services.RemoveAll<DbContextOptions<AppDbContext>>();
            services.AddDbContext<AppDbContext>(opt => opt.UseSqlite(_conn));
        });
    }
}

public sealed record OrderResponse(int Id, string CustomerName, decimal Total);
```


### `templates/ProgramPartial.cs`

```csharp
public partial class Program { }
```
