// purpose: controller unit test skeleton with Mock<T> and FluentAssertions
// consumes: controller name, service interface, DTO types
// produces: xunit test class conforming to constructor-injection + fluentassertions-not-assert
// depends-on: content/01-core-rules.xml rules constructor-injection, fluentassertions-not-assert
// token-budget-impact: ~400 tokens when loaded as context
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
