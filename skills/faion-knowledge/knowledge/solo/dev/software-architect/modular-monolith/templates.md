# Modular Monolith Templates

Copy-paste templates for module structure, configuration, and common patterns.

## Python/Django Templates

### Module Structure

```
module_name/
├── __init__.py          # Public API exports
├── api.py               # Public interface
├── models.py            # Domain models
├── services.py          # Business logic
├── repository.py        # Data access
├── events.py            # Domain events
├── handlers.py          # Event handlers
├── exceptions.py        # Module exceptions
└── tests/
    ├── __init__.py
    ├── test_services.py
    └── test_api.py
```

### Module Public API (`__init__.py`)

```python
"""
Orders Module - Public API

This module handles order management including creation,
fulfillment, and cancellation.
"""

from .api import (
    # Service
    OrderService,
    # DTOs
    OrderDTO,
    OrderItemDTO,
    CreateOrderRequest,
    OrderStatus,
    # Exceptions
    OrderNotFoundError,
    InsufficientStockError,
)
from .events import (
    OrderCreatedEvent,
    OrderCompletedEvent,
    OrderCancelledEvent,
)

__all__ = [
    # Service
    "OrderService",
    # DTOs
    "OrderDTO",
    "OrderItemDTO",
    "CreateOrderRequest",
    "OrderStatus",
    # Exceptions
    "OrderNotFoundError",
    "InsufficientStockError",
    # Events
    "OrderCreatedEvent",
    "OrderCompletedEvent",
    "OrderCancelledEvent",
]
```

### Service Interface (`api.py`)

```python
"""
Orders Module - Public Service Interface

Other modules should ONLY use this interface.
"""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional, Protocol
from uuid import UUID


# ============================================================
# Enums
# ============================================================

class OrderStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


# ============================================================
# DTOs (Data Transfer Objects)
# ============================================================

@dataclass(frozen=True)
class OrderItemDTO:
    """Read-only order item data."""
    product_id: str
    product_name: str
    quantity: int
    unit_price: float
    total_price: float


@dataclass(frozen=True)
class OrderDTO:
    """Read-only order data."""
    id: str
    user_id: str
    status: OrderStatus
    items: list[OrderItemDTO]
    total_amount: float
    created_at: datetime
    updated_at: datetime


@dataclass(frozen=True)
class CreateOrderRequest:
    """Request to create a new order."""
    user_id: str
    items: list[dict]  # [{"product_id": str, "quantity": int}]
    shipping_address_id: Optional[str] = None


# ============================================================
# Service Interface
# ============================================================

class OrderService(Protocol):
    """
    Public interface for Order module.

    Usage:
        from orders import OrderService

        order = order_service.create_order(request)
        order = order_service.get_order(order_id)
    """

    def create_order(self, request: CreateOrderRequest) -> OrderDTO:
        """Create a new order."""
        ...

    def get_order(self, order_id: str) -> Optional[OrderDTO]:
        """Get order by ID. Returns None if not found."""
        ...

    def get_user_orders(
        self,
        user_id: str,
        status: Optional[OrderStatus] = None,
        limit: int = 50
    ) -> list[OrderDTO]:
        """Get orders for a user, optionally filtered by status."""
        ...

    def cancel_order(self, order_id: str, reason: str) -> OrderDTO:
        """Cancel an order. Raises OrderNotFoundError if not found."""
        ...

    def complete_order(self, order_id: str) -> OrderDTO:
        """Mark order as completed."""
        ...


# ============================================================
# Exceptions
# ============================================================

class OrderError(Exception):
    """Base exception for Order module."""
    pass


class OrderNotFoundError(OrderError):
    """Order with given ID does not exist."""
    def __init__(self, order_id: str):
        self.order_id = order_id
        super().__init__(f"Order not found: {order_id}")


class InsufficientStockError(OrderError):
    """Not enough stock to fulfill order."""
    def __init__(self, product_id: str, requested: int, available: int):
        self.product_id = product_id
        self.requested = requested
        self.available = available
        super().__init__(
            f"Insufficient stock for {product_id}: "
            f"requested {requested}, available {available}"
        )
```

### Domain Events (`events.py`)

```python
"""
Orders Module - Domain Events

Events published by this module for other modules to consume.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any
from uuid import UUID, uuid4


@dataclass(frozen=True)
class DomainEvent:
    """Base class for all domain events."""
    event_id: UUID = field(default_factory=uuid4)
    occurred_at: datetime = field(default_factory=datetime.utcnow)
    version: int = 1


@dataclass(frozen=True)
class OrderCreatedEvent(DomainEvent):
    """Published when a new order is created."""
    order_id: str
    user_id: str
    items: list[dict]  # [{"product_id": str, "quantity": int, "price": float}]
    total_amount: float


@dataclass(frozen=True)
class OrderCompletedEvent(DomainEvent):
    """Published when an order is marked as completed."""
    order_id: str
    user_id: str
    completed_at: datetime = field(default_factory=datetime.utcnow)


@dataclass(frozen=True)
class OrderCancelledEvent(DomainEvent):
    """Published when an order is cancelled."""
    order_id: str
    user_id: str
    reason: str
    cancelled_at: datetime = field(default_factory=datetime.utcnow)
```

### Event Bus (`shared/events.py`)

```python
"""
Shared Event Bus for in-process communication.

Usage:
    # Publishing
    event_bus.publish(OrderCreatedEvent(...))

    # Subscribing
    @event_bus.subscribe(OrderCreatedEvent)
    def handle_order_created(event: OrderCreatedEvent):
        # Handle event
        pass
"""

from collections import defaultdict
from typing import Any, Callable, Type, TypeVar
import logging

logger = logging.getLogger(__name__)

T = TypeVar("T")


class EventBus:
    """Simple in-memory event bus."""

    def __init__(self):
        self._handlers: dict[Type, list[Callable]] = defaultdict(list)

    def subscribe(self, event_type: Type[T]) -> Callable:
        """Decorator to subscribe a handler to an event type."""
        def decorator(handler: Callable[[T], Any]) -> Callable[[T], Any]:
            self._handlers[event_type].append(handler)
            return handler
        return decorator

    def publish(self, event: Any) -> None:
        """Publish an event to all registered handlers."""
        event_type = type(event)
        handlers = self._handlers.get(event_type, [])

        logger.info(f"Publishing {event_type.__name__} to {len(handlers)} handlers")

        for handler in handlers:
            try:
                handler(event)
            except Exception as e:
                logger.exception(
                    f"Error handling {event_type.__name__} in {handler.__name__}: {e}"
                )
                # Continue with other handlers

    def publish_all(self, events: list[Any]) -> None:
        """Publish multiple events."""
        for event in events:
            self.publish(event)


# Global event bus instance
event_bus = EventBus()
```

### import-linter Configuration (`.importlinter`)

```ini
[importlinter]
root_package = src
include_external_packages = False

# Module independence - modules cannot import from each other directly
[importlinter:contract:module-independence]
name = Module Independence
type = independence
modules =
    src.users
    src.orders
    src.payments
    src.inventory
    src.notifications

# Shared package can be imported by all
[importlinter:contract:shared-allowed]
name = Shared is available to all
type = layers
layers =
    src.users
    src.orders
    src.payments
    src.inventory
    src.notifications
    src.shared

# Clean architecture layers within modules
[importlinter:contract:clean-layers]
name = Clean Architecture Layers
type = layers
layers =
    src.*.api
    src.*.services
    src.*.repository
    src.*.models
containers =
    src.users
    src.orders
    src.payments
```

### Django Settings for Schema Separation

```python
# config/settings.py

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'app_db',
        'USER': 'app_user',
        'PASSWORD': 'app_password',
        'HOST': 'localhost',
        'PORT': '5432',
        'OPTIONS': {
            'options': '-c search_path=public'
        }
    }
}

# Database routers for schema separation
DATABASE_ROUTERS = ['config.routers.ModuleRouter']

# Module to schema mapping
MODULE_SCHEMAS = {
    'users': 'users',
    'orders': 'orders',
    'payments': 'payments',
    'inventory': 'inventory',
}

# config/routers.py
class ModuleRouter:
    """Route database operations to correct schema."""

    def db_for_read(self, model, **hints):
        return 'default'

    def db_for_write(self, model, **hints):
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        # Only allow relations within same module
        return obj1._meta.app_label == obj2._meta.app_label

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        return True
```

## Go Templates

### Module Structure

```
internal/
├── orders/
│   ├── api.go           # Public interface
│   ├── dto.go           # Data transfer objects
│   ├── events.go        # Domain events
│   ├── service.go       # Service implementation
│   ├── repository.go    # Data access
│   ├── handler.go       # HTTP handlers
│   └── internal/        # Private implementation
│       ├── model.go     # Domain models
│       └── validation.go
```

### Module Public API (`api.go`)

```go
// Package orders provides order management functionality.
// Other modules should only use types and functions exported from this file.
package orders

import (
    "context"
    "time"
)

// ============================================================
// DTOs
// ============================================================

// OrderDTO represents order data for cross-module communication.
type OrderDTO struct {
    ID          string         `json:"id"`
    UserID      string         `json:"user_id"`
    Status      OrderStatus    `json:"status"`
    Items       []OrderItemDTO `json:"items"`
    TotalAmount float64        `json:"total_amount"`
    CreatedAt   time.Time      `json:"created_at"`
    UpdatedAt   time.Time      `json:"updated_at"`
}

// OrderItemDTO represents an item in an order.
type OrderItemDTO struct {
    ProductID   string  `json:"product_id"`
    ProductName string  `json:"product_name"`
    Quantity    int     `json:"quantity"`
    UnitPrice   float64 `json:"unit_price"`
    TotalPrice  float64 `json:"total_price"`
}

// CreateOrderRequest contains data for creating a new order.
type CreateOrderRequest struct {
    UserID            string             `json:"user_id"`
    Items             []OrderItemRequest `json:"items"`
    ShippingAddressID string             `json:"shipping_address_id,omitempty"`
}

// OrderItemRequest represents an item request.
type OrderItemRequest struct {
    ProductID string `json:"product_id"`
    Quantity  int    `json:"quantity"`
}

// OrderStatus represents the status of an order.
type OrderStatus string

const (
    OrderStatusPending   OrderStatus = "pending"
    OrderStatusConfirmed OrderStatus = "confirmed"
    OrderStatusShipped   OrderStatus = "shipped"
    OrderStatusDelivered OrderStatus = "delivered"
    OrderStatusCancelled OrderStatus = "cancelled"
)

// ============================================================
// Service Interface
// ============================================================

// Service defines the public interface for the orders module.
type Service interface {
    CreateOrder(ctx context.Context, req CreateOrderRequest) (*OrderDTO, error)
    GetOrder(ctx context.Context, orderID string) (*OrderDTO, error)
    GetUserOrders(ctx context.Context, userID string, status *OrderStatus, limit int) ([]OrderDTO, error)
    CancelOrder(ctx context.Context, orderID string, reason string) (*OrderDTO, error)
    CompleteOrder(ctx context.Context, orderID string) (*OrderDTO, error)
}

// ============================================================
// Errors
// ============================================================

// OrderNotFoundError indicates the order was not found.
type OrderNotFoundError struct {
    OrderID string
}

func (e *OrderNotFoundError) Error() string {
    return "order not found: " + e.OrderID
}

// InsufficientStockError indicates not enough stock.
type InsufficientStockError struct {
    ProductID string
    Requested int
    Available int
}

func (e *InsufficientStockError) Error() string {
    return fmt.Sprintf(
        "insufficient stock for %s: requested %d, available %d",
        e.ProductID, e.Requested, e.Available,
    )
}
```

### Domain Events (`events.go`)

```go
package orders

import (
    "time"

    "github.com/google/uuid"
)

// ============================================================
// Events
// ============================================================

// OrderCreatedEvent is published when a new order is created.
type OrderCreatedEvent struct {
    EventID     string               `json:"event_id"`
    OccurredAt  time.Time            `json:"occurred_at"`
    Version     int                  `json:"version"`
    OrderID     string               `json:"order_id"`
    UserID      string               `json:"user_id"`
    Items       []OrderItemEventData `json:"items"`
    TotalAmount float64              `json:"total_amount"`
}

// OrderItemEventData represents item data in events.
type OrderItemEventData struct {
    ProductID string  `json:"product_id"`
    Quantity  int     `json:"quantity"`
    Price     float64 `json:"price"`
}

// NewOrderCreatedEvent creates a new OrderCreatedEvent.
func NewOrderCreatedEvent(orderID, userID string, items []OrderItemEventData, total float64) OrderCreatedEvent {
    return OrderCreatedEvent{
        EventID:     uuid.New().String(),
        OccurredAt:  time.Now().UTC(),
        Version:     1,
        OrderID:     orderID,
        UserID:      userID,
        Items:       items,
        TotalAmount: total,
    }
}

// OrderCompletedEvent is published when an order is completed.
type OrderCompletedEvent struct {
    EventID     string    `json:"event_id"`
    OccurredAt  time.Time `json:"occurred_at"`
    Version     int       `json:"version"`
    OrderID     string    `json:"order_id"`
    UserID      string    `json:"user_id"`
    CompletedAt time.Time `json:"completed_at"`
}

// OrderCancelledEvent is published when an order is cancelled.
type OrderCancelledEvent struct {
    EventID     string    `json:"event_id"`
    OccurredAt  time.Time `json:"occurred_at"`
    Version     int       `json:"version"`
    OrderID     string    `json:"order_id"`
    UserID      string    `json:"user_id"`
    Reason      string    `json:"reason"`
    CancelledAt time.Time `json:"cancelled_at"`
}
```

### Event Bus (`shared/events/bus.go`)

```go
package events

import (
    "context"
    "log/slog"
    "reflect"
    "sync"
)

// Handler is a function that handles an event.
type Handler func(ctx context.Context, event any) error

// Bus is an in-memory event bus.
type Bus struct {
    mu       sync.RWMutex
    handlers map[reflect.Type][]Handler
    logger   *slog.Logger
}

// NewBus creates a new event bus.
func NewBus(logger *slog.Logger) *Bus {
    return &Bus{
        handlers: make(map[reflect.Type][]Handler),
        logger:   logger,
    }
}

// Subscribe registers a handler for an event type.
func (b *Bus) Subscribe(eventType any, handler Handler) {
    b.mu.Lock()
    defer b.mu.Unlock()

    t := reflect.TypeOf(eventType)
    b.handlers[t] = append(b.handlers[t], handler)
}

// Publish sends an event to all registered handlers.
func (b *Bus) Publish(ctx context.Context, event any) error {
    b.mu.RLock()
    handlers := b.handlers[reflect.TypeOf(event)]
    b.mu.RUnlock()

    eventName := reflect.TypeOf(event).Name()
    b.logger.Info("Publishing event",
        "event", eventName,
        "handlers", len(handlers),
    )

    for _, handler := range handlers {
        if err := handler(ctx, event); err != nil {
            b.logger.Error("Handler failed",
                "event", eventName,
                "error", err,
            )
            // Continue with other handlers
        }
    }

    return nil
}
```

## Java/Spring Modulith Templates

### Module Structure

```
src/main/java/com/example/
├── orders/
│   ├── package-info.java         # @ApplicationModule
│   ├── OrdersApi.java            # Public interface
│   ├── OrderDto.java             # DTOs
│   ├── OrderEvents.java          # Events
│   ├── internal/
│   │   ├── Order.java            # Domain model
│   │   ├── OrderService.java     # Implementation
│   │   └── OrderRepository.java  # Data access
│   └── OrdersEventListener.java  # Event handlers
```

### Module Definition (`package-info.java`)

```java
/**
 * Orders module - handles order management.
 *
 * Public API:
 * - OrdersApi: Service interface
 * - OrderDto: Data transfer object
 * - OrderEvents: Domain events
 *
 * Allowed dependencies: shared
 */
@org.springframework.modulith.ApplicationModule(
    allowedDependencies = {"shared", "shared::events"}
)
package com.example.orders;
```

### Public API (`OrdersApi.java`)

```java
package com.example.orders;

import java.util.List;
import java.util.Optional;

/**
 * Public interface for the Orders module.
 * Other modules should only depend on this interface.
 */
public interface OrdersApi {

    /**
     * Creates a new order.
     *
     * @param request The order creation request
     * @return The created order
     * @throws InsufficientStockException if stock is not available
     */
    OrderDto createOrder(CreateOrderRequest request);

    /**
     * Gets an order by ID.
     *
     * @param orderId The order ID
     * @return The order, or empty if not found
     */
    Optional<OrderDto> getOrder(String orderId);

    /**
     * Gets orders for a user.
     *
     * @param userId The user ID
     * @param status Optional status filter
     * @param limit Maximum number of orders to return
     * @return List of orders
     */
    List<OrderDto> getUserOrders(String userId, OrderStatus status, int limit);

    /**
     * Cancels an order.
     *
     * @param orderId The order ID
     * @param reason The cancellation reason
     * @return The cancelled order
     * @throws OrderNotFoundException if order not found
     */
    OrderDto cancelOrder(String orderId, String reason);

    /**
     * Marks an order as completed.
     *
     * @param orderId The order ID
     * @return The completed order
     */
    OrderDto completeOrder(String orderId);
}
```

### DTOs (`OrderDto.java`)

```java
package com.example.orders;

import java.math.BigDecimal;
import java.time.Instant;
import java.util.List;

/**
 * Order data transfer object.
 * Immutable record for cross-module communication.
 */
public record OrderDto(
    String id,
    String userId,
    OrderStatus status,
    List<OrderItemDto> items,
    BigDecimal totalAmount,
    Instant createdAt,
    Instant updatedAt
) {}

public record OrderItemDto(
    String productId,
    String productName,
    int quantity,
    BigDecimal unitPrice,
    BigDecimal totalPrice
) {}

public record CreateOrderRequest(
    String userId,
    List<OrderItemRequest> items,
    String shippingAddressId
) {}

public record OrderItemRequest(
    String productId,
    int quantity
) {}

public enum OrderStatus {
    PENDING,
    CONFIRMED,
    SHIPPED,
    DELIVERED,
    CANCELLED
}
```

### Events (`OrderEvents.java`)

```java
package com.example.orders;

import java.math.BigDecimal;
import java.time.Instant;
import java.util.List;
import java.util.UUID;

/**
 * Domain events published by the Orders module.
 */
public final class OrderEvents {

    private OrderEvents() {}

    /**
     * Published when a new order is created.
     */
    public record OrderCreated(
        UUID eventId,
        Instant occurredAt,
        String orderId,
        String userId,
        List<OrderItemData> items,
        BigDecimal totalAmount
    ) {
        public OrderCreated(String orderId, String userId, List<OrderItemData> items, BigDecimal totalAmount) {
            this(UUID.randomUUID(), Instant.now(), orderId, userId, items, totalAmount);
        }
    }

    /**
     * Published when an order is completed.
     */
    public record OrderCompleted(
        UUID eventId,
        Instant occurredAt,
        String orderId,
        String userId
    ) {
        public OrderCompleted(String orderId, String userId) {
            this(UUID.randomUUID(), Instant.now(), orderId, userId);
        }
    }

    /**
     * Published when an order is cancelled.
     */
    public record OrderCancelled(
        UUID eventId,
        Instant occurredAt,
        String orderId,
        String userId,
        String reason
    ) {
        public OrderCancelled(String orderId, String userId, String reason) {
            this(UUID.randomUUID(), Instant.now(), orderId, userId, reason);
        }
    }

    public record OrderItemData(
        String productId,
        int quantity,
        BigDecimal price
    ) {}
}
```

### Event Publisher

```java
package com.example.orders.internal;

import com.example.orders.OrderEvents.*;
import org.springframework.context.ApplicationEventPublisher;
import org.springframework.stereotype.Component;

@Component
class OrderEventPublisher {

    private final ApplicationEventPublisher events;

    OrderEventPublisher(ApplicationEventPublisher events) {
        this.events = events;
    }

    void publishOrderCreated(Order order) {
        var items = order.getItems().stream()
            .map(i -> new OrderItemData(i.getProductId(), i.getQuantity(), i.getPrice()))
            .toList();

        events.publishEvent(new OrderCreated(
            order.getId(),
            order.getUserId(),
            items,
            order.getTotalAmount()
        ));
    }

    void publishOrderCompleted(Order order) {
        events.publishEvent(new OrderCompleted(order.getId(), order.getUserId()));
    }

    void publishOrderCancelled(Order order, String reason) {
        events.publishEvent(new OrderCancelled(order.getId(), order.getUserId(), reason));
    }
}
```

### Modularity Tests

```java
package com.example;

import org.junit.jupiter.api.Test;
import org.springframework.modulith.core.ApplicationModules;
import org.springframework.modulith.docs.Documenter;

class ModularityTests {

    ApplicationModules modules = ApplicationModules.of(Application.class);

    @Test
    void verifyModularity() {
        modules.verify();
    }

    @Test
    void generateDocumentation() {
        new Documenter(modules)
            .writeModulesAsPlantUml()
            .writeIndividualModulesAsPlantUml();
    }
}
```

## Database Migration Templates

### PostgreSQL Schema Setup

```sql
-- Create schemas for each module
CREATE SCHEMA IF NOT EXISTS users;
CREATE SCHEMA IF NOT EXISTS orders;
CREATE SCHEMA IF NOT EXISTS payments;
CREATE SCHEMA IF NOT EXISTS inventory;

-- Grant appropriate permissions
GRANT USAGE ON SCHEMA users TO app_user;
GRANT USAGE ON SCHEMA orders TO app_user;
GRANT USAGE ON SCHEMA payments TO app_user;
GRANT USAGE ON SCHEMA inventory TO app_user;

-- Example: Users schema
CREATE TABLE users.accounts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    name VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_users_accounts_email ON users.accounts(email);

-- Example: Orders schema
CREATE TABLE orders.orders (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,  -- Reference by ID, no FK to users schema
    status VARCHAR(50) NOT NULL DEFAULT 'pending',
    total_amount DECIMAL(12, 2) NOT NULL,
    shipping_address JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE orders.order_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_id UUID NOT NULL REFERENCES orders.orders(id) ON DELETE CASCADE,
    product_id UUID NOT NULL,  -- Reference by ID, no FK to catalog
    product_name VARCHAR(255) NOT NULL,  -- Denormalized
    quantity INTEGER NOT NULL,
    unit_price DECIMAL(12, 2) NOT NULL,
    total_price DECIMAL(12, 2) NOT NULL
);

CREATE INDEX idx_orders_user_id ON orders.orders(user_id);
CREATE INDEX idx_orders_status ON orders.orders(status);
CREATE INDEX idx_order_items_order_id ON orders.order_items(order_id);
```

### Outbox Pattern Table

```sql
-- Outbox table for reliable event publishing
CREATE TABLE shared.outbox (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    aggregate_type VARCHAR(100) NOT NULL,
    aggregate_id VARCHAR(100) NOT NULL,
    event_type VARCHAR(100) NOT NULL,
    payload JSONB NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    processed_at TIMESTAMP WITH TIME ZONE,
    error TEXT
);

CREATE INDEX idx_outbox_unprocessed
    ON shared.outbox(created_at)
    WHERE processed_at IS NULL;
```

## Docker Compose Template

```yaml
# docker-compose.yml
version: '3.8'

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://app_user:app_password@db:5432/app_db
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - db
      - redis

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: app_user
      POSTGRES_PASSWORD: app_password
      POSTGRES_DB: app_db
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./migrations/init.sql:/docker-entrypoint-initdb.d/init.sql
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
```

## CI Configuration Template

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_USER: test_user
          POSTGRES_PASSWORD: test_password
          POSTGRES_DB: test_db
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install import-linter pytest

      - name: Check module boundaries
        run: lint-imports

      - name: Run tests
        run: pytest --cov=src

      - name: Upload coverage
        uses: codecov/codecov-action@v4
```
