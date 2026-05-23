// purpose: MediatR IRequestHandler skeleton per cqrs-handler-per-message rule
// consumes: ShipOrderCommand + repository
// produces: handler artefact in Application layer
// depends-on: content/01-core-rules.xml
// token-budget-impact: ~200 tokens when loaded as reference

using MediatR;
using FluentValidation;

namespace Faion.Application.Orders;

public sealed record ShipOrderCommand(int OrderId, string Carrier) : IRequest<ShipOrderResponse>;
public sealed record ShipOrderResponse(int OrderId, string Status, DateTime ShippedAt);

public sealed class ShipOrderValidator : AbstractValidator<ShipOrderCommand>
{
    public ShipOrderValidator()
    {
        RuleFor(x => x.OrderId).GreaterThan(0);
        RuleFor(x => x.Carrier).NotEmpty().MaximumLength(50);
    }
}

public sealed class ShipOrderHandler : IRequestHandler<ShipOrderCommand, ShipOrderResponse>
{
    private readonly IOrderRepository _orders;
    private readonly IUnitOfWork _uow;

    public ShipOrderHandler(IOrderRepository orders, IUnitOfWork uow)
    {
        _orders = orders;
        _uow = uow;
    }

    public async Task<ShipOrderResponse> Handle(ShipOrderCommand req, CancellationToken ct)
    {
        var order = await _orders.GetAsync(req.OrderId, ct)
            ?? throw new InvalidOperationException($"order {req.OrderId} not found");
        order.Ship(req.Carrier, DateTime.UtcNow);
        await _uow.SaveChangesAsync(ct);
        return new ShipOrderResponse(order.Id, "Shipped", DateTime.UtcNow);
    }
}

public interface IOrderRepository { Task<Order?> GetAsync(int id, CancellationToken ct); }
public interface IUnitOfWork { Task SaveChangesAsync(CancellationToken ct); }
public sealed class Order { public int Id { get; } public void Ship(string c, DateTime when) { } }
