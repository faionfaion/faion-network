# Design Pattern Examples

Practical examples of design pattern implementations across different domains.

## Creational Patterns

### Factory Method: Payment Processor

**Problem:** Application needs to support multiple payment providers (Stripe, PayPal, Square).

```python
# Python implementation
from abc import ABC, abstractmethod
from typing import Protocol

class PaymentProcessor(Protocol):
    def process(self, amount: float) -> dict: ...
    def refund(self, transaction_id: str) -> dict: ...

class StripeProcessor:
    def process(self, amount: float) -> dict:
        # Stripe-specific implementation
        return {"provider": "stripe", "status": "success", "amount": amount}

    def refund(self, transaction_id: str) -> dict:
        return {"provider": "stripe", "status": "refunded", "id": transaction_id}

class PayPalProcessor:
    def process(self, amount: float) -> dict:
        return {"provider": "paypal", "status": "success", "amount": amount}

    def refund(self, transaction_id: str) -> dict:
        return {"provider": "paypal", "status": "refunded", "id": transaction_id}

class PaymentProcessorFactory:
    _processors = {
        "stripe": StripeProcessor,
        "paypal": PayPalProcessor,
    }

    @classmethod
    def create(cls, provider: str) -> PaymentProcessor:
        if provider not in cls._processors:
            raise ValueError(f"Unknown provider: {provider}")
        return cls._processors[provider]()

# Usage
processor = PaymentProcessorFactory.create("stripe")
result = processor.process(99.99)
```

### Builder: Query Builder

**Problem:** Build complex database queries with optional clauses.

```typescript
// TypeScript implementation
class QueryBuilder {
    private table: string = '';
    private columns: string[] = ['*'];
    private whereClauses: string[] = [];
    private orderByClause: string = '';
    private limitValue: number | null = null;
    private offsetValue: number | null = null;

    from(table: string): QueryBuilder {
        this.table = table;
        return this;
    }

    select(...columns: string[]): QueryBuilder {
        this.columns = columns.length > 0 ? columns : ['*'];
        return this;
    }

    where(condition: string): QueryBuilder {
        this.whereClauses.push(condition);
        return this;
    }

    orderBy(column: string, direction: 'ASC' | 'DESC' = 'ASC'): QueryBuilder {
        this.orderByClause = `${column} ${direction}`;
        return this;
    }

    limit(value: number): QueryBuilder {
        this.limitValue = value;
        return this;
    }

    offset(value: number): QueryBuilder {
        this.offsetValue = value;
        return this;
    }

    build(): string {
        let query = `SELECT ${this.columns.join(', ')} FROM ${this.table}`;

        if (this.whereClauses.length > 0) {
            query += ` WHERE ${this.whereClauses.join(' AND ')}`;
        }
        if (this.orderByClause) {
            query += ` ORDER BY ${this.orderByClause}`;
        }
        if (this.limitValue !== null) {
            query += ` LIMIT ${this.limitValue}`;
        }
        if (this.offsetValue !== null) {
            query += ` OFFSET ${this.offsetValue}`;
        }

        return query;
    }
}

// Usage
const query = new QueryBuilder()
    .from('users')
    .select('id', 'name', 'email')
    .where('status = "active"')
    .where('created_at > "2024-01-01"')
    .orderBy('created_at', 'DESC')
    .limit(10)
    .offset(20)
    .build();
// SELECT id, name, email FROM users WHERE status = "active" AND created_at > "2024-01-01" ORDER BY created_at DESC LIMIT 10 OFFSET 20
```

## Structural Patterns

### Decorator: Middleware Pipeline

**Problem:** Add cross-cutting concerns (logging, auth, caching) to HTTP handlers.

```python
# Python implementation
from functools import wraps
from typing import Callable
import time
import logging

def logging_middleware(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        logging.info(f"Request: {request.method} {request.path}")
        start = time.time()
        response = func(request, *args, **kwargs)
        duration = time.time() - start
        logging.info(f"Response: {response.status_code} in {duration:.3f}s")
        return response
    return wrapper

def auth_middleware(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        token = request.headers.get('Authorization')
        if not token or not validate_token(token):
            return Response(status=401, body="Unauthorized")
        return func(request, *args, **kwargs)
    return wrapper

def caching_middleware(ttl: int = 60):
    def decorator(func: Callable) -> Callable:
        cache = {}

        @wraps(func)
        def wrapper(request, *args, **kwargs):
            cache_key = f"{request.method}:{request.path}"
            cached = cache.get(cache_key)

            if cached and time.time() - cached['time'] < ttl:
                return cached['response']

            response = func(request, *args, **kwargs)
            cache[cache_key] = {'response': response, 'time': time.time()}
            return response
        return wrapper
    return decorator

# Usage: Stack decorators to build pipeline
@logging_middleware
@auth_middleware
@caching_middleware(ttl=300)
def get_users(request):
    return Response(status=200, body=fetch_users())
```

### Adapter: Legacy API Integration

**Problem:** Integrate legacy SOAP service with modern REST application.

```typescript
// TypeScript implementation

// Legacy SOAP client interface (what we have)
interface LegacySoapClient {
    executeRequest(xmlPayload: string): Promise<string>;
}

// Modern interface (what we need)
interface UserService {
    getUser(id: string): Promise<User>;
    createUser(data: CreateUserDTO): Promise<User>;
}

interface User {
    id: string;
    name: string;
    email: string;
}

// Adapter: makes SOAP look like REST
class SoapUserServiceAdapter implements UserService {
    constructor(private soapClient: LegacySoapClient) {}

    async getUser(id: string): Promise<User> {
        const xml = `<GetUserRequest><UserId>${id}</UserId></GetUserRequest>`;
        const response = await this.soapClient.executeRequest(xml);
        return this.parseUserResponse(response);
    }

    async createUser(data: CreateUserDTO): Promise<User> {
        const xml = `
            <CreateUserRequest>
                <Name>${data.name}</Name>
                <Email>${data.email}</Email>
            </CreateUserRequest>
        `;
        const response = await this.soapClient.executeRequest(xml);
        return this.parseUserResponse(response);
    }

    private parseUserResponse(xml: string): User {
        // Parse XML to JSON (simplified)
        const parser = new DOMParser();
        const doc = parser.parseFromString(xml, 'text/xml');
        return {
            id: doc.querySelector('UserId')?.textContent || '',
            name: doc.querySelector('Name')?.textContent || '',
            email: doc.querySelector('Email')?.textContent || '',
        };
    }
}

// Usage: rest of application uses UserService interface
const userService: UserService = new SoapUserServiceAdapter(soapClient);
const user = await userService.getUser('123');
```

## Behavioral Patterns

### Strategy: Pricing Calculator

**Problem:** Apply different pricing strategies based on customer type.

```python
# Python implementation
from abc import ABC, abstractmethod
from dataclasses import dataclass
from decimal import Decimal
from typing import Protocol

class PricingStrategy(Protocol):
    def calculate(self, base_price: Decimal, quantity: int) -> Decimal: ...

class RegularPricing:
    def calculate(self, base_price: Decimal, quantity: int) -> Decimal:
        return base_price * quantity

class PremiumPricing:
    """10% discount for premium customers"""
    def calculate(self, base_price: Decimal, quantity: int) -> Decimal:
        subtotal = base_price * quantity
        return subtotal * Decimal('0.90')

class WholesalePricing:
    """Tiered pricing for bulk orders"""
    def calculate(self, base_price: Decimal, quantity: int) -> Decimal:
        if quantity >= 100:
            discount = Decimal('0.70')  # 30% off
        elif quantity >= 50:
            discount = Decimal('0.80')  # 20% off
        elif quantity >= 10:
            discount = Decimal('0.90')  # 10% off
        else:
            discount = Decimal('1.00')
        return base_price * quantity * discount

@dataclass
class Order:
    customer_type: str
    items: list[tuple[str, Decimal, int]]  # (name, price, quantity)

    _strategies = {
        'regular': RegularPricing(),
        'premium': PremiumPricing(),
        'wholesale': WholesalePricing(),
    }

    def calculate_total(self) -> Decimal:
        strategy = self._strategies.get(self.customer_type, RegularPricing())
        total = Decimal('0')
        for name, price, quantity in self.items:
            total += strategy.calculate(price, quantity)
        return total

# Usage
order = Order(
    customer_type='wholesale',
    items=[
        ('Widget', Decimal('10.00'), 100),
        ('Gadget', Decimal('25.00'), 50),
    ]
)
print(f"Total: ${order.calculate_total()}")  # Applies wholesale discounts
```

### Observer: Event System

**Problem:** Notify multiple components when order status changes.

```typescript
// TypeScript implementation
type EventHandler<T> = (data: T) => void;

class EventEmitter<Events extends Record<string, any>> {
    private handlers: Map<keyof Events, Set<EventHandler<any>>> = new Map();

    on<K extends keyof Events>(event: K, handler: EventHandler<Events[K]>): () => void {
        if (!this.handlers.has(event)) {
            this.handlers.set(event, new Set());
        }
        this.handlers.get(event)!.add(handler);

        // Return unsubscribe function
        return () => this.handlers.get(event)?.delete(handler);
    }

    emit<K extends keyof Events>(event: K, data: Events[K]): void {
        this.handlers.get(event)?.forEach(handler => handler(data));
    }
}

// Define event types
interface OrderEvents {
    'order.created': { orderId: string; customerId: string; total: number };
    'order.paid': { orderId: string; paymentId: string };
    'order.shipped': { orderId: string; trackingNumber: string };
    'order.delivered': { orderId: string; deliveredAt: Date };
}

// Create typed event bus
const orderEvents = new EventEmitter<OrderEvents>();

// Subscribe handlers
orderEvents.on('order.created', (data) => {
    console.log(`Email: Order ${data.orderId} confirmation sent`);
});

orderEvents.on('order.created', (data) => {
    console.log(`Analytics: New order tracked, total: $${data.total}`);
});

orderEvents.on('order.shipped', (data) => {
    console.log(`SMS: Order ${data.orderId} shipped, tracking: ${data.trackingNumber}`);
});

// Emit events
orderEvents.emit('order.created', {
    orderId: 'ORD-123',
    customerId: 'CUST-456',
    total: 99.99
});
```

### State: Order Workflow

**Problem:** Order behavior changes based on current status.

```python
# Python implementation
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

class OrderState(ABC):
    @abstractmethod
    def pay(self, order: 'Order') -> None: ...

    @abstractmethod
    def ship(self, order: 'Order') -> None: ...

    @abstractmethod
    def deliver(self, order: 'Order') -> None: ...

    @abstractmethod
    def cancel(self, order: 'Order') -> None: ...

class PendingState(OrderState):
    def pay(self, order: 'Order') -> None:
        order.paid_at = datetime.now()
        order._state = PaidState()

    def ship(self, order: 'Order') -> None:
        raise ValueError("Cannot ship unpaid order")

    def deliver(self, order: 'Order') -> None:
        raise ValueError("Cannot deliver unpaid order")

    def cancel(self, order: 'Order') -> None:
        order.cancelled_at = datetime.now()
        order._state = CancelledState()

class PaidState(OrderState):
    def pay(self, order: 'Order') -> None:
        raise ValueError("Order already paid")

    def ship(self, order: 'Order') -> None:
        order.shipped_at = datetime.now()
        order._state = ShippedState()

    def deliver(self, order: 'Order') -> None:
        raise ValueError("Cannot deliver before shipping")

    def cancel(self, order: 'Order') -> None:
        # Process refund
        order.cancelled_at = datetime.now()
        order._state = CancelledState()

class ShippedState(OrderState):
    def pay(self, order: 'Order') -> None:
        raise ValueError("Order already paid")

    def ship(self, order: 'Order') -> None:
        raise ValueError("Order already shipped")

    def deliver(self, order: 'Order') -> None:
        order.delivered_at = datetime.now()
        order._state = DeliveredState()

    def cancel(self, order: 'Order') -> None:
        raise ValueError("Cannot cancel shipped order")

class DeliveredState(OrderState):
    def pay(self, order: 'Order') -> None:
        raise ValueError("Order already paid")

    def ship(self, order: 'Order') -> None:
        raise ValueError("Order already delivered")

    def deliver(self, order: 'Order') -> None:
        raise ValueError("Order already delivered")

    def cancel(self, order: 'Order') -> None:
        raise ValueError("Cannot cancel delivered order")

class CancelledState(OrderState):
    def pay(self, order: 'Order') -> None:
        raise ValueError("Order is cancelled")

    def ship(self, order: 'Order') -> None:
        raise ValueError("Order is cancelled")

    def deliver(self, order: 'Order') -> None:
        raise ValueError("Order is cancelled")

    def cancel(self, order: 'Order') -> None:
        raise ValueError("Order already cancelled")

@dataclass
class Order:
    id: str
    items: list
    _state: OrderState = field(default_factory=PendingState)
    paid_at: Optional[datetime] = None
    shipped_at: Optional[datetime] = None
    delivered_at: Optional[datetime] = None
    cancelled_at: Optional[datetime] = None

    def pay(self) -> None:
        self._state.pay(self)

    def ship(self) -> None:
        self._state.ship(self)

    def deliver(self) -> None:
        self._state.deliver(self)

    def cancel(self) -> None:
        self._state.cancel(self)

    @property
    def status(self) -> str:
        return self._state.__class__.__name__.replace('State', '')

# Usage
order = Order(id='ORD-123', items=['Widget', 'Gadget'])
print(order.status)  # Pending
order.pay()
print(order.status)  # Paid
order.ship()
print(order.status)  # Shipped
order.deliver()
print(order.status)  # Delivered
```

## Distributed System Patterns

### Circuit Breaker: Resilient HTTP Client

```python
# Python implementation
import time
from enum import Enum
from dataclasses import dataclass, field
from typing import Callable, TypeVar, Generic

T = TypeVar('T')

class CircuitState(Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"

@dataclass
class CircuitBreaker(Generic[T]):
    failure_threshold: int = 5
    recovery_timeout: float = 30.0
    half_open_max_calls: int = 3

    _state: CircuitState = field(default=CircuitState.CLOSED, init=False)
    _failure_count: int = field(default=0, init=False)
    _last_failure_time: float = field(default=0, init=False)
    _half_open_calls: int = field(default=0, init=False)

    def call(self, func: Callable[[], T], fallback: Callable[[], T] | None = None) -> T:
        if self._state == CircuitState.OPEN:
            if time.time() - self._last_failure_time >= self.recovery_timeout:
                self._state = CircuitState.HALF_OPEN
                self._half_open_calls = 0
            elif fallback:
                return fallback()
            else:
                raise CircuitOpenError("Circuit is open")

        try:
            result = func()
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            if fallback:
                return fallback()
            raise

    def _on_success(self) -> None:
        if self._state == CircuitState.HALF_OPEN:
            self._half_open_calls += 1
            if self._half_open_calls >= self.half_open_max_calls:
                self._state = CircuitState.CLOSED
                self._failure_count = 0
        elif self._state == CircuitState.CLOSED:
            self._failure_count = 0

    def _on_failure(self) -> None:
        self._failure_count += 1
        self._last_failure_time = time.time()

        if self._state == CircuitState.HALF_OPEN:
            self._state = CircuitState.OPEN
        elif self._failure_count >= self.failure_threshold:
            self._state = CircuitState.OPEN

class CircuitOpenError(Exception):
    pass

# Usage
breaker = CircuitBreaker(failure_threshold=3, recovery_timeout=60)

def fetch_user(user_id: str) -> dict:
    return breaker.call(
        func=lambda: http_client.get(f"/users/{user_id}"),
        fallback=lambda: {"id": user_id, "name": "Unknown", "cached": True}
    )
```

### Saga: Distributed Transaction

```typescript
// TypeScript implementation
interface SagaStep<T> {
    name: string;
    execute: () => Promise<T>;
    compensate: (result: T) => Promise<void>;
}

class SagaOrchestrator {
    private completedSteps: { step: SagaStep<any>; result: any }[] = [];

    async execute<T>(steps: SagaStep<T>[]): Promise<Map<string, T>> {
        const results = new Map<string, T>();

        try {
            for (const step of steps) {
                console.log(`Executing: ${step.name}`);
                const result = await step.execute();
                this.completedSteps.push({ step, result });
                results.set(step.name, result);
            }
            return results;
        } catch (error) {
            console.log(`Failed at step, starting compensation`);
            await this.compensate();
            throw error;
        }
    }

    private async compensate(): Promise<void> {
        // Compensate in reverse order
        for (const { step, result } of this.completedSteps.reverse()) {
            try {
                console.log(`Compensating: ${step.name}`);
                await step.compensate(result);
            } catch (compError) {
                console.error(`Compensation failed for ${step.name}:`, compError);
                // Log for manual intervention
            }
        }
    }
}

// Usage: Order creation saga
const createOrderSaga: SagaStep<any>[] = [
    {
        name: 'reserveInventory',
        execute: async () => {
            const reservationId = await inventoryService.reserve(items);
            return { reservationId };
        },
        compensate: async (result) => {
            await inventoryService.cancelReservation(result.reservationId);
        },
    },
    {
        name: 'processPayment',
        execute: async () => {
            const paymentId = await paymentService.charge(customerId, total);
            return { paymentId };
        },
        compensate: async (result) => {
            await paymentService.refund(result.paymentId);
        },
    },
    {
        name: 'createOrder',
        execute: async () => {
            const orderId = await orderService.create(orderData);
            return { orderId };
        },
        compensate: async (result) => {
            await orderService.cancel(result.orderId);
        },
    },
];

const saga = new SagaOrchestrator();
const results = await saga.execute(createOrderSaga);
```

## Anti-Pattern Examples

### God Object (Anti-Pattern)

```python
# ANTI-PATTERN: Don't do this
class UserManager:
    def create_user(self, data): ...
    def update_user(self, id, data): ...
    def delete_user(self, id): ...
    def send_email(self, user_id, message): ...
    def process_payment(self, user_id, amount): ...
    def generate_report(self, user_id): ...
    def validate_address(self, address): ...
    def calculate_shipping(self, address): ...
    def apply_discount(self, user_id, code): ...
    # ... 50 more methods

# SOLUTION: Split by responsibility
class UserService:
    def create(self, data): ...
    def update(self, id, data): ...
    def delete(self, id): ...

class EmailService:
    def send(self, recipient, message): ...

class PaymentService:
    def process(self, user_id, amount): ...

class ShippingService:
    def calculate(self, address): ...
    def validate_address(self, address): ...
```

### Distributed Monolith (Anti-Pattern)

```typescript
// ANTI-PATTERN: Tightly coupled microservices
class OrderService {
    async createOrder(data: OrderData): Promise<Order> {
        // Direct synchronous calls to other services
        const user = await userService.getUser(data.userId);  // Sync call
        const inventory = await inventoryService.check(data.items);  // Sync call
        const payment = await paymentService.process(data);  // Sync call

        // If any service is down, entire operation fails
        // Services can't be deployed independently
        // Shared database between services
    }
}

// SOLUTION: Event-driven, loose coupling
class OrderService {
    async createOrder(data: OrderData): Promise<Order> {
        // Create order with pending status
        const order = await this.repository.create({
            ...data,
            status: 'pending'
        });

        // Publish event, let other services react
        await this.eventBus.publish('order.created', {
            orderId: order.id,
            items: data.items,
            customerId: data.userId
        });

        return order;
    }
}
```

---

*Design Pattern Examples v1.0*
