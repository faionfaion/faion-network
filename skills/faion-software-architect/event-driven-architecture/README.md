# Event-Driven Architecture

Asynchronous, loosely coupled systems using events for inter-service communication.

## Overview

Event-driven architecture (EDA) enables systems to communicate through events rather than direct synchronous calls. This approach provides loose coupling, independent scalability, and resilience.

```
Producer ──Event──> Broker ──Event──> Consumer(s)
```

**Key Benefits:**
- Loose coupling between services
- Independent scaling of producers/consumers
- Better fault tolerance and resilience
- Event replay and audit capabilities
- Natural fit for microservices

---

## Core Patterns

### Pub/Sub (Publish-Subscribe)

One-to-many event distribution where publishers emit events to topics and multiple subscribers consume independently.

```
Publisher ──> Topic ──> Subscriber A
                   ──> Subscriber B
                   ──> Subscriber C
```

**Use Cases:**
- Notifications and broadcasts
- Fan-out processing
- Event distribution to multiple bounded contexts

**Characteristics:**
- Publishers don't know subscribers
- Subscribers receive all matching events
- Events are typically transient (unless persisted)

---

### Event Sourcing

Store state changes as a sequence of immutable events. Current state is derived by replaying events.

```
Events:              Current State:
────────────         ────────────────
OrderCreated     →   Order {
ItemAdded        →     items: [A, B],
ItemAdded        →     status: "shipped",
PaymentReceived  →     total: 150.00
OrderShipped     →   }
```

**Benefits:**
- Complete audit trail (every change recorded)
- Time travel (rebuild state at any point)
- Debug by replaying events
- Natural event-driven integration

**Challenges:**
- Schema evolution complexity
- Event store scaling
- Eventual consistency
- Snapshot management for performance

**When to Use:**
- Audit requirements (financial, healthcare, legal)
- Complex domain with business events
- Need for temporal queries
- Event replay capabilities needed

**When to Avoid:**
- Simple CRUD applications
- Strong consistency requirements
- Team unfamiliar with the pattern

---

### CQRS (Command Query Responsibility Segregation)

Separate read and write models optimized for their specific purposes.

```
        Commands                    Queries
            |                          |
            v                          v
    +───────────────+          +───────────────+
    │ Write Model   │          │  Read Model   │
    │ (normalized)  │──events─>│ (denormalized)│
    +───────────────+          +───────────────+
            |                          |
            v                          v
       Write DB                   Read DB
```

**Benefits:**
- Optimize read/write independently
- Scale reads and writes separately
- Different data models for different needs
- Natural fit with event sourcing

**Trade-offs:**
- Eventual consistency between models
- Increased complexity
- More infrastructure to manage

**Best Practices:**
- Start small (one bounded context)
- Implement versioning strategy for events
- Design for idempotency
- Plan for eventual consistency

---

### Saga Pattern

Manage distributed transactions across multiple services without 2PC (two-phase commit).

#### Choreography-Based Saga

Services communicate via events without central coordination.

```
Order Service         Payment Service        Inventory Service
      │                      │                       │
      │──OrderCreated───────>│                       │
      │                      │──PaymentCharged──────>│
      │                      │                       │
      │<─────────────────────│<──InventoryReserved───│
      │                      │                       │
   Complete              (if fails: emit compensating event)
```

**Pros:** No single point of failure, simpler for few participants
**Cons:** Hard to track, complex with many services

#### Orchestration-Based Saga

Central orchestrator coordinates the saga steps.

```
         Orchestrator
              │
    ┌─────────┼─────────┐
    │         │         │
    v         v         v
 Order    Payment   Inventory
Service   Service    Service
```

**Pros:** Easier to understand, centralized monitoring
**Cons:** Single point of failure, orchestrator complexity

**Compensation:** Each step must have a compensating transaction to undo if later steps fail.

| Step | Action | Compensation |
|------|--------|--------------|
| 1 | Create Order | Cancel Order |
| 2 | Reserve Inventory | Release Inventory |
| 3 | Charge Payment | Refund Payment |
| 4 | Ship Order | Cancel Shipment |

**Frameworks:**
- Axon Framework (Java/Spring Boot)
- Eventuate Tram Saga (Java)
- Camunda (BPMN-based)
- Apache Camel (Saga EIP)
- Temporal.io (workflow orchestration)

---

## Message Broker Comparison

| Broker | Throughput | Latency | Best For |
|--------|------------|---------|----------|
| **Kafka** | 10M+ msg/s | Low at scale | Event streaming, replay, high throughput |
| **Pulsar** | 4M+ msg/s | Low | Multi-tenancy, streaming + queuing |
| **RabbitMQ** | 1M msg/s | Very low (small scale) | Complex routing, traditional messaging |
| **AWS SQS** | 300K msg/s | Variable | Serverless, AWS-native, simple queuing |
| **Redis Streams** | Very high | Sub-ms | Low latency, ephemeral events |
| **NATS** | High | Very low | Lightweight, cloud-native |

### Apache Kafka

**Architecture:** Distributed commit log with partitioned topics
**Delivery:** Pull-based (consumers pull from brokers)

**Strengths:**
- Highest throughput (15x faster than RabbitMQ)
- Strong ordering guarantees per partition
- Event replay (configurable retention)
- Extensive ecosystem (Kafka Streams, Connect, ksqlDB)
- De facto standard for Spark, Flink integration

**Considerations:**
- Operational complexity (ZooKeeper/KRaft)
- Higher learning curve
- Overkill for simple use cases

**Use When:**
- High-volume event streaming
- Event sourcing requirements
- Real-time analytics pipelines
- Strong ordering needed

### Apache Pulsar

**Architecture:** Compute-storage separation (BookKeeper for storage)
**Delivery:** Both push and pull

**Strengths:**
- Native multi-tenancy
- Unified streaming and queuing
- Tiered storage (hot/cold data)
- Geo-replication built-in

**Considerations:**
- More complex architecture
- Smaller ecosystem than Kafka
- Steeper operational learning curve

**Use When:**
- Multi-tenant SaaS platforms
- Need both streaming and queuing
- Geo-distributed deployments

### RabbitMQ

**Architecture:** Traditional message broker (AMQP)
**Delivery:** Push-based

**Strengths:**
- Flexible routing (exchanges, bindings)
- Multiple protocols (AMQP, MQTT, STOMP)
- Lower latency at small scale
- Simpler operations
- Mature and well-documented

**Considerations:**
- Messages removed after consumption
- Limited replay capability
- Doesn't scale as well for streaming

**Use When:**
- Complex routing requirements
- Traditional request-reply patterns
- Smaller scale messaging
- Multiple protocol support needed

### AWS SQS/SNS

**Architecture:** Fully managed cloud service
**Delivery:** Pull (SQS) / Push (SNS)

**Strengths:**
- Zero operations (serverless)
- Auto-scaling
- AWS ecosystem integration
- Cost-effective for variable loads

**Considerations:**
- At-least-once delivery only
- Limited ordering (FIFO queues exist but limited)
- AWS lock-in
- Less flexibility than self-managed

**Use When:**
- AWS-native applications
- Serverless architectures
- Simple decoupling needs
- Minimize operational burden

---

## Event Schema Design

### CloudEvents Standard

[CloudEvents](https://cloudevents.io/) is a CNCF graduated specification for describing event data in a common format.

**Required Attributes:**
| Attribute | Type | Description |
|-----------|------|-------------|
| `specversion` | String | CloudEvents spec version (e.g., "1.0") |
| `id` | String | Unique event identifier |
| `source` | URI | Context origin identifier |
| `type` | String | Event type (e.g., "com.example.order.created") |

**Optional Attributes:**
| Attribute | Type | Description |
|-----------|------|-------------|
| `datacontenttype` | String | Content type of data (e.g., "application/json") |
| `dataschema` | URI | Schema for data attribute |
| `subject` | String | Subject of event in context of source |
| `time` | Timestamp | Event timestamp (RFC 3339) |

**Example CloudEvent:**
```json
{
  "specversion": "1.0",
  "id": "A234-1234-1234",
  "source": "/orders/order-service",
  "type": "com.example.order.created",
  "datacontenttype": "application/json",
  "dataschema": "https://example.com/schemas/order.json",
  "subject": "order-12345",
  "time": "2026-01-25T10:30:00Z",
  "data": {
    "orderId": "order-12345",
    "customerId": "cust-789",
    "items": [
      {"sku": "ITEM-001", "quantity": 2}
    ],
    "total": 99.99
  }
}
```

### Event Naming Conventions

**Use past tense** (something happened):
- `OrderCreated`, `PaymentReceived`, `UserRegistered`
- `order.created`, `payment.received`, `user.registered`

**Not imperative** (commands are different):
- Avoid: `CreateOrder`, `ProcessPayment`, `RegisterUser`

**Type Hierarchy:**
```
{reverse-domain}.{bounded-context}.{aggregate}.{event}
com.example.orders.order.created
com.example.payments.payment.charged
com.example.inventory.stock.reserved
```

### Event Versioning

**Strategies:**
1. **URL/Type versioning:** `com.example.order.created.v2`
2. **Header versioning:** `event-version: 2`
3. **Schema registry:** Confluent Schema Registry, AWS Glue

**Compatibility Rules:**
- **Backward:** New schema reads old data
- **Forward:** Old schema reads new data
- **Full:** Both directions compatible

**Schema Evolution Best Practices:**
- Add optional fields (backward compatible)
- Never remove required fields
- Use default values for new fields
- Version schemas explicitly

---

## Delivery Guarantees

| Guarantee | Description | Use Case |
|-----------|-------------|----------|
| **At-most-once** | May lose messages | Metrics, non-critical logs |
| **At-least-once** | May duplicate | Most business events |
| **Exactly-once** | No loss, no duplicates | Financial transactions (hard to achieve) |

### Idempotency

Events may be delivered multiple times. Implement idempotent handlers:

```python
def handle_order_created(event):
    if already_processed(event.id):
        return  # Skip duplicate

    process_order(event.data)
    mark_processed(event.id)
```

**Techniques:**
- Deduplication table with event IDs
- Idempotency keys in database operations
- Conditional writes (optimistic locking)
- Natural idempotency (PUT vs POST semantics)

---

## Best Practices

### Event Design

1. **Events are immutable** - Never modify published events
2. **Include correlation ID** - Trace requests across services
3. **Version events** - Plan for schema evolution
4. **Keep events small** - Reference IDs, not full objects
5. **Self-describing** - Include type and schema information

### Processing

1. **Handle out-of-order** - Events may arrive in different order
2. **Implement idempotency** - Handle duplicate delivery
3. **Use dead letter queues** - Handle failed processing
4. **Monitor consumer lag** - Detect processing bottlenecks
5. **Design compensating actions** - For saga rollbacks

### Operations

1. **Schema registry** - Manage event schemas centrally
2. **Observability** - Structured logging, distributed tracing
3. **Circuit breakers** - Prevent cascading failures
4. **Backpressure handling** - Manage consumer overload
5. **Retention policies** - Balance storage vs replay needs

---

## Anti-Patterns

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| Event as command | Coupling producer to consumer | Separate events and commands |
| Too large events | Performance, tight coupling | Use references, not full objects |
| Missing correlation | Can't trace flows | Always include correlation ID |
| Ignoring ordering | Race conditions, inconsistency | Handle out-of-order or use partitioning |
| No schema management | Breaking changes | Use schema registry |
| Synchronous mindset | Blocking on event response | Embrace eventual consistency |

---

## Related Resources

### Key References

- [Event-Driven Architecture - Martin Fowler](https://martinfowler.com/articles/201701-event-driven.html)
- [Microservices Patterns - Chris Richardson](https://microservices.io/patterns/data/event-sourcing.html)
- [CloudEvents Specification](https://cloudevents.io/)
- [Saga Pattern - microservices.io](https://microservices.io/patterns/data/saga.html)
- [CQRS - Martin Fowler](https://martinfowler.com/bliki/CQRS.html)

### Books

- "Designing Data-Intensive Applications" - Martin Kleppmann
- "Building Event-Driven Microservices" - Adam Bellemare
- "Microservices Patterns" - Chris Richardson
- "Enterprise Integration Patterns" - Hohpe & Woolf

### Framework Documentation

- [Apache Kafka Documentation](https://kafka.apache.org/documentation/)
- [Apache Pulsar Documentation](https://pulsar.apache.org/docs/)
- [RabbitMQ Documentation](https://www.rabbitmq.com/documentation.html)
- [Axon Framework](https://docs.axoniq.io/)
- [Temporal.io](https://docs.temporal.io/)

---

## Related Skills

| Skill | Relationship |
|-------|--------------|
| [microservices-architecture](../microservices-architecture/) | Service decomposition context |
| [distributed-patterns](../distributed-patterns.md) | Resilience patterns |
| [api-design](../api-design.md) | Sync vs async APIs |
| [system-design-process](../system-design-process/) | Overall architecture design |

---

## Files in This Methodology

| File | Purpose |
|------|---------|
| [README.md](README.md) | This guide - EDA overview and patterns |
| [checklist.md](checklist.md) | EDA design and implementation checklist |
| [examples.md](examples.md) | Architecture examples and case studies |
| [templates.md](templates.md) | Event schemas, consumer templates |
| [llm-prompts.md](llm-prompts.md) | Prompts for EDA design assistance |
