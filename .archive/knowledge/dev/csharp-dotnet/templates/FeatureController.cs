// purpose: [ApiController] skeleton conforming to 01-core-rules.xml
// consumes: IFeatureService + DTO records
// produces: HTTP controller artefact
// depends-on: content/01-core-rules.xml
// token-budget-impact: ~250 tokens when loaded as reference

using Microsoft.AspNetCore.Mvc;

namespace Faion.Features.Orders;

[ApiController]
[Route("api/[controller]")]
public sealed class OrdersController : ControllerBase
{
    private readonly IOrdersService _service;

    public OrdersController(IOrdersService service) => _service = service;

    [HttpGet("{id:int}")]
    [ProducesResponseType(typeof(OrderResponse), StatusCodes.Status200OK)]
    [ProducesResponseType(StatusCodes.Status404NotFound)]
    public async Task<ActionResult<OrderResponse>> Get(int id, CancellationToken ct)
    {
        var order = await _service.GetAsync(id, ct);
        return order is null ? NotFound() : Ok(order);
    }

    [HttpPost]
    [ProducesResponseType(typeof(OrderResponse), StatusCodes.Status201Created)]
    public async Task<ActionResult<OrderResponse>> Create(CreateOrderRequest req, CancellationToken ct)
    {
        var created = await _service.CreateAsync(req, ct);
        return CreatedAtAction(nameof(Get), new { id = created.Id }, created);
    }
}

public sealed record CreateOrderRequest(string CustomerName, decimal Total);
public sealed record OrderResponse(int Id, string CustomerName, decimal Total);
