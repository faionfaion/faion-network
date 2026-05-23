// purpose: WebApplicationFactory<Program> controller integration test
// consumes: Program assembly + DbContext type
// produces: integration test class
// depends-on: content/01-core-rules.xml
// token-budget-impact: ~300 tokens when loaded as reference

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
