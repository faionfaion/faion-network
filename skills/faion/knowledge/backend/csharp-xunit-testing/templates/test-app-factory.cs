// purpose: derived WebApplicationFactory that substitutes DbContext with SQLite-in-memory,
//          plus the controller integration test class that consumes it
// consumes: Program assembly + AppDbContext type
// produces: integration test class + reusable test host factory
// depends-on: content/01-core-rules.xml rules class-fixture-required,
//             webapplicationfactory-for-integration, theory-for-params
// token-budget-impact: ~350 tokens when loaded as context

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
