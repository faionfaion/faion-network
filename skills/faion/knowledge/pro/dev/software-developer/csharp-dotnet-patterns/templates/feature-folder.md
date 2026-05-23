<!-- purpose: feature-folder layout reference for clean-arch + CQRS .NET solution -->
<!-- consumes: feature spec -->
<!-- produces: directory tree skeleton -->
<!-- depends-on: content/01-core-rules.xml -->
<!-- token-budget-impact: ~150 tokens when loaded as reference -->

# Feature folder layout

```
src/
├── Faion.Domain/
│   └── Orders/
│       ├── Order.cs                 # aggregate, no public setters
│       └── Events/OrderShipped.cs   # domain event record
├── Faion.Application/
│   └── Orders/
│       ├── ShipOrderCommand.cs      # IRequest<ShipOrderResponse>
│       ├── ShipOrderHandler.cs      # IRequestHandler
│       ├── ShipOrderValidator.cs    # AbstractValidator
│       └── ShipOrderResponse.cs     # response record
├── Faion.Infrastructure/
│   └── Orders/OrderRepository.cs    # EF Core impl of IOrderRepository
└── Faion.Web/
    └── Controllers/OrdersController.cs   # one-line mediator dispatch
```

Reference rules:
- `Faion.Domain.csproj` has no PackageReference to EF/AspNetCore.
- `Faion.Web.csproj` references Application + Infrastructure only.
- Validator registered via `AddValidatorsFromAssemblyContaining<ShipOrderValidator>()`.
