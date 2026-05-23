// purpose: Service unit test with Moq + FluentAssertions
// consumes: IOrderRepository (mocked) + IOrdersService
// produces: unit test class
// depends-on: content/01-core-rules.xml
// token-budget-impact: ~250 tokens when loaded as reference

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
