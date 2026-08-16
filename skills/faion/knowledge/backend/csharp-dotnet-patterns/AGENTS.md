# C# .NET Clean Architecture + CQRS Patterns

## Summary

**One-sentence:** Clean Architecture + CQRS for .NET 8/9 — Domain/Application/Infrastructure/API layering with MediatR Commands/Queries, NetArchTest fitness, and DDD aggregate discipline.

**One-paragraph:** Clean Architecture for .NET 8/9 with MediatR/CQRS: Domain (entities, value objects, domain events) → Application (Commands, Queries, Handlers, Validators) → Infrastructure (EF Core, configurations) → API (controllers or Minimal API, composition root only). One Command/Query per folder. Domain behaviour lives in entity methods, not Application handlers. Aggregate collections mutate only via aggregate methods. Architecture fitness — Application MUST NOT reference Infrastructure or EF Core — is enforced by NetArchTest in CI.

**Ефективно для:**

- .NET 8/9 service з 3+ aggregate roots і нетривіальною доменною логікою.
- Multi-team enterprise codebase, де Application/Domain/Infrastructure separation enables parallel work.
- Microservices з event-driven integration — domain events + outbox для cross-aggregate hand-offs.
- Codebases targeting native AOT / containerized deploys — layering trims Infrastructure deps.

## Applies If (ALL must hold)

- .NET 8/9 service with non-trivial domain (3+ aggregate roots, multiple bounded contexts, business rules beyond CRUD).
- Multi-team enterprise codebase where Application/Domain/Infrastructure separation enables parallel work.
- Microservices with event-driven integration — domain events + MediatR Notification pattern for cross-aggregate hand-offs.

## Skip If (ANY kills it)

- Simple CRUD apps (<20 endpoints, no business rules) — four projects are pure overhead.
- Lambda/Functions with cold-start budget — DI graph + MediatR add 100-300ms startup; use Minimal API + direct DbContext.
- Teams unfamiliar with DDD — the pattern's value depends on rich domain models; without that you get a layered anaemic codebase.
- Pure read-side services (reporting, dashboards) — CQRS is overkill; one project with `SELECT` queries is fine.
- Solo codebases: adopt the layer direction and the aggregate discipline, but the mediator pipeline costs more than it returns with one author.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Bounded-context map | text or diagram | DDD workshop |
| Aggregate / entity list | Markdown table | domain modelling |
| Use-case catalogue | command/query list | product / BA |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[csharp-dotnet]] | Umbrella covering CancellationToken plumbing + DI lifetimes. |
| [[csharp-entity-framework]] | Infrastructure layer EF Core patterns. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 17 rules: layer-direction, behaviour-in-entities, one-command-per-folder, validators-on-commands, outbox-for-cross-aggregate, mediatr-reserved-for-cross-cutting, cqrs-record-request-per-handler, rich-domain-no-setters, no-entity-in-api, no-iqueryable-from-application, dbcontext-behind-interface, pipeline-behaviour-order, composition-root-per-layer, pin-bus-and-mapper-versions, result-for-expected-failures, domain-events-raised-and-cleared, integration-test-per-feature | 2600 |
| `content/02-output-contract.xml` | essential | JSON Schema for the layered-solution manifest incl. per-use-case naming + layer_refs + pipeline order, with valid/invalid examples | 1200 |
| `content/03-failure-modes.xml` | essential | 14 antipatterns: anaemic-regression, layer-leakage, in-transaction-domain-events, mediatr-overuse, collection-mutated-outside-aggregate, ignore-query-filters-leak, async-void-handler, controller-with-logic, entity-as-dto, mediatr-hallucination, public-setters-regression, domain-events-never-dispatched, pipeline-order-by-accident, overstubbed-bus-tests | 1700 |
| `content/04-procedure.xml` | essential | 7-step procedure: solution skeleton → Domain → Application → Infrastructure → API → tests → NetArchTest gate | 1200 |
| `content/05-examples.xml` | essential | Solution tree, aggregate, command/validator/handler quartet, pipeline registration + one-line controller, final manifest | 1500 |
| `content/06-decision-tree.xml` | essential | Scope gate on domain richness + flat defect router mapping signals to a rule from 01-core-rules.xml | 1100 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-solution` | sonnet | Multi-project generation with layer references. |
| `add-command-handler` | sonnet | Light judgment on validator scope + handler boundaries. |
| `enforce-arch-fitness` | haiku | Mechanical NetArchTest verification. |
| `design-domain-event-flow` | opus | Tx-vs-outbox reasoning across aggregates. |

## Templates

| File | Purpose |
|------|---------|
| `templates/arch-tests.cs` | NetArchTest fitness suite enforcing layer direction. |
| `templates/dotnet-cleanarch-lint.sh` | Grep-level lint for the checks NetArchTest cannot see (public setters, entities returned from controllers, commands without validators, `Handle` without a token). |
| `templates/Aggregate.cs` | Aggregate root with private setters, intention-revealing methods and domain events. |
| `templates/Handler.cs` | Record command + FluentValidation validator + single MediatR handler. |
| `templates/feature-folder.md.j2` | Feature-folder layout reference for the four-project solution. |
| `templates/feature-folder.md` | Feature-folder layout reference for the four-project solution. Generated from `templates/feature-folder.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-csharp-dotnet-patterns.py` | Validate the layered-solution manifest against the JSON Schema. | Pre-commit; CI on every methodology PR. |

## Known limits

- **MediatR and AutoMapper became commercial** (v12+ / v10+, paid above $1M revenue, announced 2024). Decide the bus and the mapper before adoption; `Mediator` and Mapperly are the source-generated free equivalents.
- **Pipeline ordering is invisible** — `IPipelineBehavior<,>` order follows DI registration order, so a mis-registration silently disables validation rather than failing.
- **Owned types (`OwnsOne`) leak into queries** — EF Core 8 partly fixed this; on EF Core 6/7 they double the JOINs and break `AsNoTracking` projections. Verify the generated SQL.
- **Controller bloat returns** — teams move logic into commands but keep mapping, auth and header parsing inline. Enforce a line-count budget on actions.
- **Minimal API + mediator loses the OpenAPI metadata** controllers get for free; it surfaces at Swagger/NSwag integration time.

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[csharp-dotnet]]
- [[csharp-entity-framework]]
- [[csharp-xunit-testing]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (domain richness, team count, deploy target, CRUD ratio) to a rule from `01-core-rules.xml`. Use it before scaffolding to decide whether Clean Architecture or a flatter layout fits.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/arch-tests.cs`

```csharp
// tests/MyApp.ArchitectureTests/LayerTests.cs
// Run via: dotnet test — required CI gate, not optional.
using NetArchTest.Rules;
using Xunit;

public class LayerTests
{
    private const string Domain         = "MyApp.Domain";
    private const string Application    = "MyApp.Application";
    private const string Infrastructure = "MyApp.Infrastructure";
    private const string Api            = "MyApp.Api";

    [Fact]
    public void Domain_does_not_reference_outer_layers() =>
        Assert.True(Types.InAssembly(typeof(MyApp.Domain.Entities.User).Assembly)
            .Should().NotHaveDependencyOnAny(
                Application, Infrastructure, Api,
                "Microsoft.EntityFrameworkCore", "MediatR", "AutoMapper")
            .GetResult().IsSuccessful);

    [Fact]
    public void Application_does_not_reference_infrastructure() =>
        Assert.True(Types.InAssembly(typeof(MyApp.Application.DependencyInjection).Assembly)
            .Should().NotHaveDependencyOn(Infrastructure)
            .GetResult().IsSuccessful);

    [Fact]
    public void Handlers_live_in_Application() =>
        Assert.True(Types.InCurrentDomain()
            .That().ImplementInterface(typeof(MediatR.IRequestHandler<,>))
            .Should().ResideInNamespace(Application)
            .GetResult().IsSuccessful);
}
```

### `templates/Aggregate.cs`

```csharp
namespace Faion.Domain.Orders;

public sealed class Order
{
    private readonly List<object> _events = new();

    public int Id { get; private set; }
    public string CustomerName { get; private set; } = "";
    public OrderStatus Status { get; private set; } = OrderStatus.Pending;
    public string? Carrier { get; private set; }
    public DateTime? ShippedAt { get; private set; }

    public IReadOnlyList<object> Events => _events.AsReadOnly();

    private Order() { }

    public Order(string customerName)
    {
        if (string.IsNullOrWhiteSpace(customerName))
            throw new ArgumentException("customer name required", nameof(customerName));
        CustomerName = customerName;
        Status = OrderStatus.Pending;
    }

    public void Ship(string carrier, DateTime when)
    {
        if (Status != OrderStatus.Pending)
            throw new InvalidOperationException($"cannot ship order in state {Status}");
        if (string.IsNullOrWhiteSpace(carrier))
            throw new ArgumentException("carrier required", nameof(carrier));
        Status = OrderStatus.Shipped;
        Carrier = carrier;
        ShippedAt = when;
        _events.Add(new OrderShipped(Id, carrier, when));
    }

    public void Cancel()
    {
        if (Status == OrderStatus.Shipped)
            throw new InvalidOperationException("cannot cancel shipped order");
        Status = OrderStatus.Cancelled;
        _events.Add(new OrderCancelled(Id));
    }
}

public enum OrderStatus { Pending, Shipped, Cancelled }
public sealed record OrderShipped(int OrderId, string Carrier, DateTime ShippedAt);
public sealed record OrderCancelled(int OrderId);
```

### `templates/Handler.cs`

```csharp
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
```

### `templates/feature-folder.md.j2`

````jinja
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
````

### `templates/dotnet-cleanarch-lint.sh`

```bash
set -euo pipefail
root="${1:?usage: dotnet-cleanarch-lint.sh SOLUTION_ROOT}"
fail=0

echo "# .NET Clean Arch lint ($root)"

echo "## Controllers returning Domain entities (no-entity-in-api)"
grep -rEn 'public async Task<(User|Order|Product|Organization|Post)>' "$root/src" \
  --include='*Controller.cs' | tee /tmp/da.ctrl-ent || true
[[ -s /tmp/da.ctrl-ent ]] && fail=1

echo "## Aggregates with public setters other than Id (rich-domain-no-setters)"
grep -rEn 'public (string|int|Guid|DateTime|decimal|bool) \w+ \{ get; set; \}' \
  "$root"/src/*.Domain --include='*.cs' | grep -v 'Id { get;' \
  | tee /tmp/da.pub-set || true
[[ -s /tmp/da.pub-set ]] && fail=1

echo "## Domain project referencing EF Core or AspNetCore (layer-direction)"
grep -rEn 'Microsoft\.(EntityFrameworkCore|AspNetCore)' "$root"/src/*.Domain \
  --include='*.csproj' | tee /tmp/da.dom-leak || true
[[ -s /tmp/da.dom-leak ]] && fail=1

echo "## Application project referencing AspNetCore or EF Core (layer-direction)"
grep -rEn 'Microsoft\.(AspNetCore|EntityFrameworkCore)' "$root"/src/*.Application \
  --include='*.csproj' | tee /tmp/da.app-leak || true
[[ -s /tmp/da.app-leak ]] && fail=1

echo "## Handlers reading HttpContext (dbcontext-behind-interface)"
grep -rEn 'IHttpContextAccessor|HttpContext' "$root"/src/*.Application --include='*.cs' \
  | tee /tmp/da.http-in-app || true
[[ -s /tmp/da.http-in-app ]] && fail=1

echo "## Handle methods without a CancellationToken (cqrs-record-request-per-handler)"
grep -rEn 'Task<[^>]+> Handle\([^)]*\)' "$root/src" --include='*Handler.cs' \
  | grep -v 'CancellationToken' | tee /tmp/da.no-ct || true
[[ -s /tmp/da.no-ct ]] && fail=1

echo "## Commands missing a FluentValidation Validator (validators-on-commands)"
find "$root/src" -name '*Command.cs' | while read -r f; do
  base="${f%Command.cs}"
  [[ -f "${base}CommandValidator.cs" ]] || echo "missing validator: $f"
done | tee /tmp/da.no-val || true
[[ -s /tmp/da.no-val ]] && fail=1

exit "$fail"
```
