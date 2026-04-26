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
