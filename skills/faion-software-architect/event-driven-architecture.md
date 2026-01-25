# Event-Driven Architecture

Asynchronous, loosely coupled systems using events.

## What is Event-Driven?

Systems communicate through events rather than direct calls.

```
Producer ──Event──▶ Broker ──Event──▶ Consumer(s)
```

## Event Types

### Domain Events
Something that happened in the business domain.
```
OrderPlaced, PaymentReceived, UserRegistered
```

### Integration Events
Events for cross-service communication.
```
OrderPlacedIntegrationEvent (contains only needed data)
```

### Commands
Request to do something (different from event).
```
PlaceOrder, ProcessPayment (imperative)
```

## Patterns

### Pub/Sub (Publish-Subscribe)
```
Publisher ──▶ Topic ──▶ Subscriber A
                   ──▶ Subscriber B
                   ──▶ Subscriber C
```
- One-to-many
- Subscribers are decoupled
- Use: Notifications, broadcasts

### Event Sourcing
Store events as source of truth, derive state.

```
Events:             Current State:
─────────────       ─────────────
OrderCreated    →   Order {
ItemAdded       →     items: [A, B],
ItemAdded       →     status: shipped,
OrderShipped    →     ...
                    }
```

**Benefits:**
- Complete audit trail
- Time travel (rebuild state at any point)
- Debug by replaying events

**Challenges:**
- Schema evolution
- Event store scaling
- Eventual consistency

### CQRS (Command Query Responsibility Segregation)

Separate read and write models.

```
        Commands                    Queries
            │                          │
            ▼                          ▼
    ┌───────────────┐          ┌───────────────┐
    │ Write Model   │          │  Read Model   │
    │ (normalized)  │──events─▶│ (denormalized)│
    └───────────────┘          └───────────────┘
            │                          │
            ▼                          ▼
       Write DB                   Read DB
```

**Benefits:**
- Optimize read/write independently
- Scale reads separately
- Different data models for different needs

### Saga Pattern

Distributed transactions via event choreography.

```
Order Service          Payment Service         Inventory Service
      │                      │                       │
      │──OrderCreated───────▶│                       │
      │                      │──PaymentCharged──────▶│
      │                      │                       │
      │◀─────────────────────│◀──InventoryReserved──│
      │                      │                       │
   Complete              (if fails: compensate)
```

**Compensation:** If step fails, publish compensating events to undo previous steps.

## Message Brokers

| Broker | Best For |
|--------|----------|
| Kafka | High throughput, event streaming, replay |
| RabbitMQ | Complex routing, traditional messaging |
| AWS SQS | Simple queuing, AWS ecosystem |
| Redis Pub/Sub | Low latency, ephemeral messages |
| NATS | Lightweight, cloud-native |

## Event Design

### Event Structure
```json
{
  "eventId": "uuid",
  "eventType": "OrderPlaced",
  "timestamp": "2024-01-15T10:30:00Z",
  "version": 1,
  "source": "order-service",
  "correlationId": "request-uuid",
  "data": {
    "orderId": "123",
    "customerId": "456",
    "items": [...]
  }
}
```

### Event Naming
```
Past tense (something happened):
✅ OrderPlaced, PaymentReceived, UserCreated

Not imperative:
❌ PlaceOrder, ReceivePayment, CreateUser
```

### Idempotency
Events may be delivered multiple times. Handle duplicates.

```python
def handle_order_placed(event):
    if already_processed(event.event_id):
        return  # Skip duplicate

    process(event)
    mark_processed(event.event_id)
```

## Delivery Guarantees

| Guarantee | Meaning | Use Case |
|-----------|---------|----------|
| At-most-once | May lose messages | Metrics, logs |
| At-least-once | May duplicate | Most business events |
| Exactly-once | No loss, no duplicates | Financial (hard to achieve) |

## Best Practices

1. **Events are immutable** - Never modify published events
2. **Include correlation ID** - Trace across services
3. **Version events** - Schema evolution
4. **Keep events small** - Reference IDs, not full objects
5. **Handle out-of-order** - Events may arrive out of sequence
6. **Dead letter queue** - Handle failed processing

## Anti-patterns

| Anti-pattern | Problem |
|--------------|---------|
| Event as command | Coupling producer to consumer |
| Too large events | Performance, coupling |
| Missing correlation | Can't trace flows |
| Ignoring ordering | Race conditions |

## Related

- [microservices-architecture.md](microservices-architecture.md) - Service context
- [distributed-patterns.md](distributed-patterns.md) - Resilience
- [serverless-architecture.md](serverless-architecture.md) - Event triggers
