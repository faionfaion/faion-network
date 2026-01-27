# Architectural Patterns: Implementation Examples

Real-world implementations of Clean, Hexagonal, Onion, and DDD patterns.

## Example 1: E-Commerce Order System

### Clean Architecture Implementation

```
ecommerce/
├── src/
│   ├── domain/
│   │   ├── entities/
│   │   │   ├── Order.ts
│   │   │   ├── OrderItem.ts
│   │   │   └── Customer.ts
│   │   ├── value-objects/
│   │   │   ├── Money.ts
│   │   │   ├── Address.ts
│   │   │   └── OrderStatus.ts
│   │   ├── repositories/
│   │   │   └── IOrderRepository.ts
│   │   └── events/
│   │       └── OrderPlaced.ts
│   │
│   ├── application/
│   │   ├── use-cases/
│   │   │   ├── PlaceOrder.ts
│   │   │   ├── CancelOrder.ts
│   │   │   └── GetOrderHistory.ts
│   │   ├── dto/
│   │   │   ├── PlaceOrderRequest.ts
│   │   │   └── OrderResponse.ts
│   │   └── interfaces/
│   │       ├── IPaymentService.ts
│   │       └── IInventoryService.ts
│   │
│   ├── infrastructure/
│   │   ├── persistence/
│   │   │   ├── PostgresOrderRepository.ts
│   │   │   └── models/
│   │   │       └── OrderModel.ts
│   │   ├── payment/
│   │   │   └── StripePaymentService.ts
│   │   ├── inventory/
│   │   │   └── ExternalInventoryService.ts
│   │   └── messaging/
│   │       └── KafkaEventPublisher.ts
│   │
│   └── presentation/
│       ├── api/
│       │   ├── OrderController.ts
│       │   └── routes.ts
│       └── middleware/
│           └── errorHandler.ts
│
└── tests/
    ├── unit/
    │   ├── domain/
    │   │   └── Order.test.ts
    │   └── application/
    │       └── PlaceOrder.test.ts
    └── integration/
        └── OrderController.test.ts
```

#### Domain Entity: Order.ts

```typescript
// src/domain/entities/Order.ts

import { Money } from '../value-objects/Money';
import { OrderStatus } from '../value-objects/OrderStatus';
import { OrderItem } from './OrderItem';
import { OrderPlaced } from '../events/OrderPlaced';

export class Order {
  private readonly id: string;
  private readonly customerId: string;
  private items: OrderItem[];
  private status: OrderStatus;
  private readonly events: DomainEvent[] = [];

  constructor(
    id: string,
    customerId: string,
    items: OrderItem[],
    status: OrderStatus = OrderStatus.PENDING
  ) {
    if (items.length === 0) {
      throw new Error('Order must have at least one item');
    }
    this.id = id;
    this.customerId = customerId;
    this.items = items;
    this.status = status;
  }

  get total(): Money {
    return this.items.reduce(
      (sum, item) => sum.add(item.subtotal),
      Money.zero()
    );
  }

  place(): void {
    if (this.status !== OrderStatus.PENDING) {
      throw new Error('Can only place pending orders');
    }
    this.status = OrderStatus.PLACED;
    this.events.push(new OrderPlaced(this.id, this.customerId, this.total));
  }

  cancel(): void {
    if (this.status === OrderStatus.SHIPPED) {
      throw new Error('Cannot cancel shipped orders');
    }
    this.status = OrderStatus.CANCELLED;
  }

  pullEvents(): DomainEvent[] {
    const events = [...this.events];
    this.events.length = 0;
    return events;
  }
}
```

#### Use Case: PlaceOrder.ts

```typescript
// src/application/use-cases/PlaceOrder.ts

import { IOrderRepository } from '../../domain/repositories/IOrderRepository';
import { IPaymentService } from '../interfaces/IPaymentService';
import { IInventoryService } from '../interfaces/IInventoryService';
import { Order } from '../../domain/entities/Order';
import { PlaceOrderRequest } from '../dto/PlaceOrderRequest';
import { OrderResponse } from '../dto/OrderResponse';

export class PlaceOrder {
  constructor(
    private readonly orderRepository: IOrderRepository,
    private readonly paymentService: IPaymentService,
    private readonly inventoryService: IInventoryService
  ) {}

  async execute(request: PlaceOrderRequest): Promise<OrderResponse> {
    // 1. Validate inventory
    await this.inventoryService.reserveItems(request.items);

    // 2. Create order
    const order = new Order(
      this.generateId(),
      request.customerId,
      request.items.map(item => new OrderItem(item.productId, item.quantity, item.price))
    );

    // 3. Process payment
    await this.paymentService.charge(request.customerId, order.total);

    // 4. Place order (changes status, raises event)
    order.place();

    // 5. Persist
    await this.orderRepository.save(order);

    // 6. Return DTO
    return OrderResponse.fromOrder(order);
  }

  private generateId(): string {
    return crypto.randomUUID();
  }
}
```

#### Controller: OrderController.ts

```typescript
// src/presentation/api/OrderController.ts

import { Request, Response } from 'express';
import { PlaceOrder } from '../../application/use-cases/PlaceOrder';
import { PlaceOrderRequest } from '../../application/dto/PlaceOrderRequest';

export class OrderController {
  constructor(private readonly placeOrder: PlaceOrder) {}

  async create(req: Request, res: Response): Promise<void> {
    const request = PlaceOrderRequest.fromBody(req.body);
    const order = await this.placeOrder.execute(request);
    res.status(201).json(order);
  }
}
```

---

### Hexagonal Architecture Implementation

```
ecommerce/
├── src/
│   ├── core/                          # The Hexagon
│   │   ├── domain/
│   │   │   ├── Order.ts
│   │   │   ├── OrderItem.ts
│   │   │   └── value-objects/
│   │   │       ├── Money.ts
│   │   │       └── OrderStatus.ts
│   │   │
│   │   ├── ports/
│   │   │   ├── inbound/               # Primary ports
│   │   │   │   ├── PlaceOrderPort.ts
│   │   │   │   ├── CancelOrderPort.ts
│   │   │   │   └── GetOrderPort.ts
│   │   │   └── outbound/              # Secondary ports
│   │   │       ├── OrderRepository.ts
│   │   │       ├── PaymentGateway.ts
│   │   │       └── InventoryChecker.ts
│   │   │
│   │   └── services/                  # Core services (implement ports)
│   │       └── OrderService.ts
│   │
│   ├── adapters/
│   │   ├── inbound/                   # Primary adapters
│   │   │   ├── rest/
│   │   │   │   ├── OrderController.ts
│   │   │   │   └── routes.ts
│   │   │   ├── graphql/
│   │   │   │   └── OrderResolver.ts
│   │   │   └── cli/
│   │   │       └── OrderCommand.ts
│   │   │
│   │   └── outbound/                  # Secondary adapters
│   │       ├── persistence/
│   │       │   └── PostgresOrderRepository.ts
│   │       ├── payment/
│   │       │   └── StripePaymentAdapter.ts
│   │       └── inventory/
│   │           └── HttpInventoryAdapter.ts
│   │
│   └── config/
│       ├── container.ts               # DI setup
│       └── app.ts                     # Bootstrap
│
└── tests/
    ├── unit/
    │   └── core/
    │       └── OrderService.test.ts
    └── integration/
        └── adapters/
            └── PostgresOrderRepository.test.ts
```

#### Primary Port: PlaceOrderPort.ts

```typescript
// src/core/ports/inbound/PlaceOrderPort.ts

export interface PlaceOrderCommand {
  customerId: string;
  items: Array<{
    productId: string;
    quantity: number;
    price: number;
  }>;
}

export interface PlaceOrderResult {
  orderId: string;
  total: number;
  status: string;
}

export interface PlaceOrderPort {
  execute(command: PlaceOrderCommand): Promise<PlaceOrderResult>;
}
```

#### Secondary Port: OrderRepository.ts

```typescript
// src/core/ports/outbound/OrderRepository.ts

import { Order } from '../../domain/Order';

export interface OrderRepository {
  save(order: Order): Promise<void>;
  findById(id: string): Promise<Order | null>;
  findByCustomerId(customerId: string): Promise<Order[]>;
}
```

#### Core Service: OrderService.ts

```typescript
// src/core/services/OrderService.ts

import { PlaceOrderPort, PlaceOrderCommand, PlaceOrderResult } from '../ports/inbound/PlaceOrderPort';
import { OrderRepository } from '../ports/outbound/OrderRepository';
import { PaymentGateway } from '../ports/outbound/PaymentGateway';
import { InventoryChecker } from '../ports/outbound/InventoryChecker';
import { Order } from '../domain/Order';

export class OrderService implements PlaceOrderPort {
  constructor(
    private readonly orderRepository: OrderRepository,
    private readonly paymentGateway: PaymentGateway,
    private readonly inventoryChecker: InventoryChecker
  ) {}

  async execute(command: PlaceOrderCommand): Promise<PlaceOrderResult> {
    // Check inventory
    await this.inventoryChecker.checkAvailability(command.items);

    // Create domain object
    const order = Order.create(command.customerId, command.items);

    // Process payment
    await this.paymentGateway.charge(command.customerId, order.total);

    // Save
    await this.orderRepository.save(order);

    return {
      orderId: order.id,
      total: order.total.amount,
      status: order.status.value,
    };
  }
}
```

#### Primary Adapter: OrderController.ts

```typescript
// src/adapters/inbound/rest/OrderController.ts

import { Request, Response } from 'express';
import { PlaceOrderPort } from '../../../core/ports/inbound/PlaceOrderPort';

export class OrderController {
  constructor(private readonly placeOrderPort: PlaceOrderPort) {}

  async placeOrder(req: Request, res: Response): Promise<void> {
    const result = await this.placeOrderPort.execute({
      customerId: req.body.customerId,
      items: req.body.items,
    });
    res.status(201).json(result);
  }
}
```

#### Secondary Adapter: PostgresOrderRepository.ts

```typescript
// src/adapters/outbound/persistence/PostgresOrderRepository.ts

import { Pool } from 'pg';
import { OrderRepository } from '../../../core/ports/outbound/OrderRepository';
import { Order } from '../../../core/domain/Order';

export class PostgresOrderRepository implements OrderRepository {
  constructor(private readonly pool: Pool) {}

  async save(order: Order): Promise<void> {
    const client = await this.pool.connect();
    try {
      await client.query('BEGIN');
      await client.query(
        'INSERT INTO orders (id, customer_id, total, status) VALUES ($1, $2, $3, $4)',
        [order.id, order.customerId, order.total.amount, order.status.value]
      );
      // Save items...
      await client.query('COMMIT');
    } catch (error) {
      await client.query('ROLLBACK');
      throw error;
    } finally {
      client.release();
    }
  }

  async findById(id: string): Promise<Order | null> {
    const result = await this.pool.query(
      'SELECT * FROM orders WHERE id = $1',
      [id]
    );
    if (result.rows.length === 0) return null;
    return this.toDomain(result.rows[0]);
  }

  private toDomain(row: any): Order {
    // Map database row to domain object
    return Order.reconstitute(row.id, row.customer_id, row.total, row.status);
  }
}
```

---

## Example 2: DDD Bounded Contexts

Multi-context e-commerce system with explicit boundaries.

```
ecommerce/
├── src/
│   ├── shared-kernel/                 # Shared across contexts
│   │   ├── domain/
│   │   │   ├── Money.ts
│   │   │   └── UserId.ts
│   │   └── infrastructure/
│   │       └── EventBus.ts
│   │
│   ├── contexts/
│   │   ├── ordering/                  # Ordering bounded context
│   │   │   ├── domain/
│   │   │   │   ├── aggregates/
│   │   │   │   │   └── Order/
│   │   │   │   │       ├── Order.ts
│   │   │   │   │       ├── OrderItem.ts
│   │   │   │   │       └── OrderId.ts
│   │   │   │   ├── events/
│   │   │   │   │   ├── OrderPlaced.ts
│   │   │   │   │   └── OrderShipped.ts
│   │   │   │   └── repositories/
│   │   │   │       └── IOrderRepository.ts
│   │   │   ├── application/
│   │   │   │   ├── commands/
│   │   │   │   │   └── PlaceOrder.ts
│   │   │   │   └── event-handlers/
│   │   │   │       └── OnPaymentReceived.ts
│   │   │   └── infrastructure/
│   │   │       └── PostgresOrderRepository.ts
│   │   │
│   │   ├── inventory/                 # Inventory bounded context
│   │   │   ├── domain/
│   │   │   │   ├── aggregates/
│   │   │   │   │   └── Stock/
│   │   │   │   │       ├── Stock.ts
│   │   │   │   │       └── StockMovement.ts
│   │   │   │   └── events/
│   │   │   │       └── StockReserved.ts
│   │   │   ├── application/
│   │   │   │   └── commands/
│   │   │   │       └── ReserveStock.ts
│   │   │   └── infrastructure/
│   │   │       └── PostgresStockRepository.ts
│   │   │
│   │   └── payments/                  # Payments bounded context
│   │       ├── domain/
│   │       │   ├── aggregates/
│   │       │   │   └── Payment/
│   │       │   │       ├── Payment.ts
│   │       │   │       └── PaymentStatus.ts
│   │       │   └── events/
│   │       │       └── PaymentCompleted.ts
│   │       ├── application/
│   │       │   └── commands/
│   │       │       └── ProcessPayment.ts
│   │       └── infrastructure/
│   │           └── StripePaymentGateway.ts
│   │
│   └── api/                           # API composition layer
│       ├── controllers/
│       │   └── CheckoutController.ts
│       └── composition/
│           └── CheckoutSaga.ts        # Orchestrates contexts
│
└── tests/
    ├── contexts/
    │   ├── ordering/
    │   ├── inventory/
    │   └── payments/
    └── integration/
        └── checkout.test.ts
```

#### Context Map

```
┌─────────────────────────────────────────────────────────────┐
│                    E-Commerce System                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   ┌──────────────┐      events      ┌──────────────┐       │
│   │   Ordering   │◀────────────────▶│   Payments   │       │
│   │   Context    │                  │   Context    │       │
│   │              │                  │              │       │
│   │ - Order      │                  │ - Payment    │       │
│   │ - OrderItem  │                  │              │       │
│   └──────────────┘                  └──────────────┘       │
│          │                                 │               │
│          │ events                          │ events        │
│          ▼                                 ▼               │
│   ┌──────────────┐                                         │
│   │  Inventory   │                                         │
│   │   Context    │                                         │
│   │              │                                         │
│   │ - Stock      │                                         │
│   └──────────────┘                                         │
│                                                             │
│   ┌─────────────────────────────────────────────────────┐  │
│   │                   Shared Kernel                      │  │
│   │   Money, UserId, EventBus                           │  │
│   └─────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘

Relationship Types:
- Ordering ←→ Payments: Partnership (events)
- Ordering → Inventory: Customer-Supplier (events)
```

---

## Example 3: Onion Architecture (.NET)

```
ECommerce/
├── src/
│   ├── ECommerce.Domain/              # Innermost
│   │   ├── Entities/
│   │   │   ├── Order.cs
│   │   │   └── Customer.cs
│   │   ├── ValueObjects/
│   │   │   ├── Money.cs
│   │   │   └── Address.cs
│   │   └── Interfaces/
│   │       └── IOrderRepository.cs
│   │
│   ├── ECommerce.Domain.Services/     # Domain services
│   │   └── OrderPricingService.cs
│   │
│   ├── ECommerce.Application/         # Application services
│   │   ├── Services/
│   │   │   └── OrderApplicationService.cs
│   │   ├── DTOs/
│   │   │   └── OrderDto.cs
│   │   └── Interfaces/
│   │       └── IEmailService.cs
│   │
│   ├── ECommerce.Infrastructure/      # Outermost
│   │   ├── Persistence/
│   │   │   ├── OrderRepository.cs
│   │   │   └── ECommerceDbContext.cs
│   │   ├── Email/
│   │   │   └── SmtpEmailService.cs
│   │   └── DependencyInjection/
│   │       └── ServiceCollectionExtensions.cs
│   │
│   └── ECommerce.WebApi/              # Presentation
│       ├── Controllers/
│       │   └── OrdersController.cs
│       └── Program.cs
│
└── tests/
    ├── ECommerce.Domain.Tests/
    ├── ECommerce.Application.Tests/
    └── ECommerce.WebApi.Tests/
```

---

## Testing Strategy by Pattern

### Clean Architecture Testing

| Layer | Test Type | Dependencies Mocked |
|-------|-----------|---------------------|
| Domain | Unit | None (pure) |
| Application | Unit | Repositories, External Services |
| Infrastructure | Integration | Real database (testcontainers) |
| Presentation | Integration | Full application (in-memory) |

### Hexagonal Testing

| Component | Test Type | Approach |
|-----------|-----------|----------|
| Domain | Unit | Direct instantiation |
| Core Services | Unit | Mock all ports |
| Primary Adapters | Integration | Mock core services |
| Secondary Adapters | Integration | Real dependencies (testcontainers) |

### DDD Testing

| Component | Test Type | Scope |
|-----------|-----------|-------|
| Aggregate | Unit | Aggregate invariants |
| Domain Service | Unit | Cross-aggregate logic |
| Application Service | Integration | Full use case |
| Context Integration | E2E | Cross-context flow |

---

## Key Takeaways

1. **Domain isolation is paramount:** All patterns share the principle of protecting domain logic
2. **Explicit boundaries:** Whether layers, ports, or contexts, boundaries should be explicit
3. **Dependency direction:** Always inward toward the domain
4. **Testability:** Isolated domain enables comprehensive unit testing
5. **Evolution:** Start with Clean Architecture, add DDD concepts as complexity grows
