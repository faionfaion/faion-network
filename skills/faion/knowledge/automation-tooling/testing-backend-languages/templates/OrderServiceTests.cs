// purpose: xUnit + Moq + FluentAssertions service test
// consumes: input artefacts described in AGENTS.md ## Prerequisites
// produces: artefact conforming to content/02-output-contract.xml for testing-backend-languages
// depends-on: content/01-core-rules.xml
// token-budget-impact: ~200-1200 tokens when loaded as context

using Moq;
using FluentAssertions;
using Xunit;

public class OrderServiceTests
{
    [Fact]
    public async Task Charge_Marks_Order_As_Charged()
    {
        var repo = new Mock<IOrderRepository>();
        var order = new Order { Amount = 1000 };
        repo.Setup(r => r.SaveAsync(order)).ReturnsAsync(order);
        var svc = new OrderService(repo.Object);

        var result = await svc.ChargeAsync(order);

        result.Status.Should().Be("charged");
    }
}
