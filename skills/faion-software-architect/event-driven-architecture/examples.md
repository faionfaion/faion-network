# Event-Driven Architecture Examples

Real-world architecture examples and case studies.

---

## Example 1: E-Commerce Order Processing

### Context

An e-commerce platform processing orders across multiple services: orders, inventory, payments, shipping, and notifications.

### Architecture Overview

```
                         ┌──────────────┐
                         │   API GW     │
                         └──────┬───────┘
                                │
                         ┌──────▼───────┐
                         │ Order Service │
                         └──────┬───────┘
                                │
                    ┌───────────▼───────────┐
                    │      Kafka Cluster     │
                    │  ┌─────────────────┐  │
                    │  │ orders.created  │  │
                    │  │ orders.updated  │  │
                    │  │ payments.done   │  │
                    │  │ inventory.rsrvd │  │
                    │  └─────────────────┘  │
                    └───────────┬───────────┘
           ┌────────────────────┼────────────────────┐
           │                    │                    │
    ┌──────▼──────┐     ┌───────▼──────┐    ┌───────▼───────┐
    │  Payment    │     │  Inventory   │    │ Notification  │
    │  Service    │     │   Service    │    │   Service     │
    └─────────────┘     └──────────────┘    └───────────────┘
```

### Event Flow: Order Placement

```
1. Customer places order
   → POST /api/orders

2. Order Service
   → Validates order
   → Stores order (status: PENDING)
   → Publishes: OrderCreated

3. Payment Service (consumes OrderCreated)
   → Processes payment
   → Publishes: PaymentProcessed OR PaymentFailed

4. Inventory Service (consumes PaymentProcessed)
   → Reserves inventory
   → Publishes: InventoryReserved OR InventoryInsufficient

5. Order Service (consumes InventoryReserved)
   → Updates order (status: CONFIRMED)
   → Publishes: OrderConfirmed

6. Notification Service (consumes OrderConfirmed)
   → Sends confirmation email
   → Sends push notification
```

### Saga Implementation (Choreography)

```
Happy Path:
OrderCreated → PaymentProcessed → InventoryReserved → OrderConfirmed

Failure at Payment:
OrderCreated → PaymentFailed → OrderCancelled

Failure at Inventory:
OrderCreated → PaymentProcessed → InventoryInsufficient
            → PaymentRefunded → OrderCancelled
```

### Key Events

**OrderCreated**
```json
{
  "specversion": "1.0",
  "id": "evt-ord-001-abc123",
  "source": "/services/order-service",
  "type": "com.ecommerce.orders.order.created",
  "time": "2026-01-25T10:30:00Z",
  "datacontenttype": "application/json",
  "data": {
    "orderId": "ORD-2026-001",
    "customerId": "CUST-789",
    "items": [
      {"sku": "PROD-001", "quantity": 2, "price": 29.99},
      {"sku": "PROD-002", "quantity": 1, "price": 49.99}
    ],
    "totalAmount": 109.97,
    "shippingAddress": {
      "street": "123 Main St",
      "city": "Seattle",
      "country": "US"
    }
  }
}
```

**PaymentProcessed**
```json
{
  "specversion": "1.0",
  "id": "evt-pay-001-def456",
  "source": "/services/payment-service",
  "type": "com.ecommerce.payments.payment.processed",
  "time": "2026-01-25T10:30:05Z",
  "data": {
    "paymentId": "PAY-2026-001",
    "orderId": "ORD-2026-001",
    "amount": 109.97,
    "currency": "USD",
    "method": "CREDIT_CARD",
    "transactionRef": "TXN-XYZ-789"
  }
}
```

### Consumer Example (Python)

```python
from kafka import KafkaConsumer
import json

class OrderEventConsumer:
    def __init__(self):
        self.consumer = KafkaConsumer(
            'orders.created',
            bootstrap_servers=['kafka:9092'],
            group_id='payment-service',
            auto_offset_reset='earliest',
            enable_auto_commit=False
        )
        self.processed_events = set()

    def handle_order_created(self, event):
        event_id = event['id']

        # Idempotency check
        if event_id in self.processed_events:
            return

        order_data = event['data']

        # Process payment
        payment_result = self.process_payment(
            order_id=order_data['orderId'],
            amount=order_data['totalAmount']
        )

        # Publish result event
        if payment_result.success:
            self.publish_payment_processed(order_data, payment_result)
        else:
            self.publish_payment_failed(order_data, payment_result)

        # Mark as processed
        self.processed_events.add(event_id)
        self.consumer.commit()
```

---

## Example 2: Financial Trading Platform

### Context

A trading platform with real-time market data, order matching, and settlement.

### Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                    Market Data Feeds                     │
└────────────────────────┬────────────────────────────────┘
                         │
              ┌──────────▼──────────┐
              │   Kafka (Streams)   │
              │   market.prices     │
              │   market.orderbook  │
              └──────────┬──────────┘
                         │
    ┌────────────────────┼────────────────────┐
    │                    │                    │
┌───▼───────┐    ┌───────▼──────┐    ┌───────▼───────┐
│  Pricing  │    │   Trading    │    │   Analytics   │
│  Engine   │    │   Engine     │    │    Service    │
└───────────┘    └──────┬───────┘    └───────────────┘
                        │
              ┌─────────▼─────────┐
              │   Kafka (Orders)  │
              │   orders.new      │
              │   orders.matched  │
              │   orders.filled   │
              └─────────┬─────────┘
                        │
         ┌──────────────┼──────────────┐
         │              │              │
  ┌──────▼─────┐ ┌──────▼─────┐ ┌──────▼─────┐
  │ Settlement │ │   Risk     │ │ Compliance │
  │  Service   │ │  Service   │ │  Service   │
  └────────────┘ └────────────┘ └────────────┘
```

### Event Sourcing for Orders

```
Order Aggregate Events:

1. OrderSubmitted(orderId, symbol, side, qty, price, timestamp)
2. OrderValidated(orderId, timestamp)
3. OrderAccepted(orderId, exchangeOrderId, timestamp)
4. OrderPartiallyFilled(orderId, filledQty, fillPrice, timestamp)
5. OrderFilled(orderId, totalFilledQty, avgPrice, timestamp)
6. OrderCancelled(orderId, reason, timestamp)
7. OrderRejected(orderId, reason, timestamp)

Rebuild State:
events.reduce((state, event) => apply(state, event), initialState)
```

### Order State Machine

```
            ┌──────────────┐
            │  SUBMITTED   │
            └──────┬───────┘
                   │ validated
            ┌──────▼───────┐
            │  VALIDATED   │───rejected──┐
            └──────┬───────┘             │
                   │ accepted            │
            ┌──────▼───────┐             │
   ┌────────│   ACCEPTED   │─────────────┤
   │        └──────┬───────┘             │
   │               │ partially_filled    │
   │        ┌──────▼───────┐             │
   │        │PARTIALLY_FILL│             │
   │        └──────┬───────┘             │
   │               │ filled              │
   │        ┌──────▼───────┐      ┌──────▼───────┐
   │        │    FILLED    │      │   REJECTED   │
   │        └──────────────┘      └──────────────┘
   │
   │ cancelled
   │        ┌──────────────┐
   └───────>│  CANCELLED   │
            └──────────────┘
```

### CQRS Implementation

**Write Model (Event Store)**
```
┌─────────────────────────────────────────────────────┐
│ Event Store                                         │
├───────────┬────────────────┬───────────┬───────────┤
│ stream_id │ event_type     │ data      │ timestamp │
├───────────┼────────────────┼───────────┼───────────┤
│ ORD-001   │ OrderSubmitted │ {...}     │ 10:30:00  │
│ ORD-001   │ OrderValidated │ {...}     │ 10:30:01  │
│ ORD-001   │ OrderAccepted  │ {...}     │ 10:30:02  │
│ ORD-001   │ OrderFilled    │ {...}     │ 10:30:05  │
└───────────┴────────────────┴───────────┴───────────┘
```

**Read Models (Projections)**

```
Order Summary View:
┌───────────┬────────┬──────┬───────┬─────────┬──────────┐
│ order_id  │ symbol │ side │ qty   │ status  │ avg_fill │
├───────────┼────────┼──────┼───────┼─────────┼──────────┤
│ ORD-001   │ AAPL   │ BUY  │ 100   │ FILLED  │ 185.50   │
└───────────┴────────┴──────┴───────┴─────────┴──────────┘

Position View:
┌────────────┬────────┬───────────┬──────────────┐
│ account_id │ symbol │ position  │ avg_cost     │
├────────────┼────────┼───────────┼──────────────┤
│ ACC-001    │ AAPL   │ 500       │ 182.30       │
└────────────┴────────┴───────────┴──────────────┘

Daily Activity View:
┌────────┬───────────┬────────┬──────────┬────────────┐
│ date   │ account   │ trades │ volume   │ pnl        │
├────────┼───────────┼────────┼──────────┼────────────┤
│ Jan 25 │ ACC-001   │ 15     │ 125,000  │ +2,340.00  │
└────────┴───────────┴────────┴──────────┴────────────┘
```

---

## Example 3: IoT Sensor Data Platform

### Context

Processing millions of IoT sensor readings for monitoring, alerting, and analytics.

### Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│             IoT Devices (Millions)                      │
│   [Sensor] [Sensor] [Sensor] [Sensor] [Sensor]         │
└────────────────────────┬────────────────────────────────┘
                         │ MQTT
              ┌──────────▼──────────┐
              │    MQTT Broker      │
              │    (EMQX/HiveMQ)    │
              └──────────┬──────────┘
                         │
              ┌──────────▼──────────┐
              │ Kafka Connect       │
              │ (MQTT Source)       │
              └──────────┬──────────┘
                         │
              ┌──────────▼──────────┐
              │      Kafka          │
              │ sensors.raw         │
              │ sensors.validated   │
              │ sensors.enriched    │
              │ alerts.triggered    │
              └──────────┬──────────┘
                         │
    ┌────────────────────┼────────────────────┐
    │                    │                    │
┌───▼────────┐   ┌───────▼──────┐   ┌────────▼───────┐
│  Flink     │   │   Alerting   │   │   Time-Series  │
│ Processing │   │   Service    │   │      DB        │
│ (enrich)   │   │              │   │  (TimescaleDB) │
└────────────┘   └──────────────┘   └────────────────┘
```

### Event Schema: Sensor Reading

```json
{
  "specversion": "1.0",
  "id": "sensor-reading-abc123",
  "source": "/devices/sensor-001",
  "type": "com.iot.sensors.reading.received",
  "time": "2026-01-25T10:30:00.123Z",
  "datacontenttype": "application/json",
  "subject": "temperature",
  "data": {
    "deviceId": "sensor-001",
    "sensorType": "temperature",
    "value": 23.5,
    "unit": "celsius",
    "location": {
      "lat": 47.6062,
      "lon": -122.3321,
      "zone": "warehouse-a"
    },
    "batteryLevel": 87,
    "signalStrength": -65
  }
}
```

### Stream Processing (Flink)

```java
DataStream<SensorReading> readings = env
    .addSource(new KafkaSource<>("sensors.raw"))
    .filter(r -> r.isValid())
    .keyBy(r -> r.getDeviceId())
    .window(TumblingEventTimeWindows.of(Time.minutes(1)))
    .aggregate(new AverageAggregate())
    .map(avg -> enrichWithMetadata(avg))
    .addSink(new KafkaSink<>("sensors.enriched"));

// Alert detection
readings
    .keyBy(r -> r.getDeviceId())
    .process(new ThresholdAlertFunction())
    .addSink(new KafkaSink<>("alerts.triggered"));
```

### Partitioning Strategy

```
Topic: sensors.raw
Partitions: 100
Key: deviceId (ensures ordering per device)

Partition assignment:
  hash(deviceId) % 100 = partition

This ensures:
- All readings from one device go to same partition
- Ordering preserved per device
- Parallel processing across devices
```

---

## Example 4: Saga Orchestration (Order Fulfillment)

### Context

Complex order fulfillment with multiple steps requiring compensation on failure.

### Orchestrator Implementation

```python
from enum import Enum
from dataclasses import dataclass
from typing import Optional

class SagaStep(Enum):
    RESERVE_INVENTORY = 1
    PROCESS_PAYMENT = 2
    CREATE_SHIPMENT = 3
    SEND_NOTIFICATION = 4

class SagaStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    COMPENSATING = "compensating"
    FAILED = "failed"

@dataclass
class SagaState:
    saga_id: str
    order_id: str
    status: SagaStatus
    current_step: SagaStep
    completed_steps: list[SagaStep]
    failed_step: Optional[SagaStep] = None
    error_message: Optional[str] = None

class OrderFulfillmentSaga:
    def __init__(self, saga_store, event_publisher):
        self.saga_store = saga_store
        self.event_publisher = event_publisher

        self.steps = [
            SagaStep.RESERVE_INVENTORY,
            SagaStep.PROCESS_PAYMENT,
            SagaStep.CREATE_SHIPMENT,
            SagaStep.SEND_NOTIFICATION
        ]

        self.compensations = {
            SagaStep.RESERVE_INVENTORY: self.release_inventory,
            SagaStep.PROCESS_PAYMENT: self.refund_payment,
            SagaStep.CREATE_SHIPMENT: self.cancel_shipment,
            SagaStep.SEND_NOTIFICATION: None  # No compensation needed
        }

    def start(self, order_id: str) -> str:
        saga_id = generate_saga_id()
        state = SagaState(
            saga_id=saga_id,
            order_id=order_id,
            status=SagaStatus.IN_PROGRESS,
            current_step=self.steps[0],
            completed_steps=[]
        )
        self.saga_store.save(state)
        self.execute_step(state)
        return saga_id

    def execute_step(self, state: SagaState):
        step = state.current_step

        # Publish command for current step
        if step == SagaStep.RESERVE_INVENTORY:
            self.event_publisher.publish(
                "inventory.commands.reserve",
                {"sagaId": state.saga_id, "orderId": state.order_id}
            )
        elif step == SagaStep.PROCESS_PAYMENT:
            self.event_publisher.publish(
                "payment.commands.process",
                {"sagaId": state.saga_id, "orderId": state.order_id}
            )
        # ... other steps

    def on_step_completed(self, saga_id: str, step: SagaStep):
        state = self.saga_store.get(saga_id)
        state.completed_steps.append(step)

        next_step_index = self.steps.index(step) + 1

        if next_step_index < len(self.steps):
            state.current_step = self.steps[next_step_index]
            self.saga_store.save(state)
            self.execute_step(state)
        else:
            state.status = SagaStatus.COMPLETED
            self.saga_store.save(state)
            self.event_publisher.publish(
                "orders.saga.completed",
                {"sagaId": saga_id, "orderId": state.order_id}
            )

    def on_step_failed(self, saga_id: str, step: SagaStep, error: str):
        state = self.saga_store.get(saga_id)
        state.status = SagaStatus.COMPENSATING
        state.failed_step = step
        state.error_message = error
        self.saga_store.save(state)

        # Start compensation in reverse order
        self.compensate(state)

    def compensate(self, state: SagaState):
        # Compensate completed steps in reverse order
        for step in reversed(state.completed_steps):
            compensation = self.compensations.get(step)
            if compensation:
                compensation(state)

        state.status = SagaStatus.FAILED
        self.saga_store.save(state)
        self.event_publisher.publish(
            "orders.saga.failed",
            {
                "sagaId": state.saga_id,
                "orderId": state.order_id,
                "failedStep": state.failed_step.name,
                "error": state.error_message
            }
        )
```

### Saga State Machine

```
                    start
                      │
                      ▼
            ┌─────────────────┐
            │  RESERVE_INV    │──fail──┐
            └────────┬────────┘        │
                     │ success         │
                     ▼                 │
            ┌─────────────────┐        │
            │ PROCESS_PAYMENT │──fail──┤
            └────────┬────────┘        │
                     │ success         │
                     ▼                 │
            ┌─────────────────┐        │
            │ CREATE_SHIPMENT │──fail──┤
            └────────┬────────┘        │
                     │ success         │
                     ▼                 │
            ┌─────────────────┐        │
            │SEND_NOTIFICATION│        │
            └────────┬────────┘        │
                     │                 │
                     ▼                 ▼
            ┌─────────────┐    ┌───────────────┐
            │  COMPLETED  │    │ COMPENSATING  │
            └─────────────┘    └───────┬───────┘
                                       │
                                       ▼
                               ┌───────────────┐
                               │    FAILED     │
                               └───────────────┘
```

---

## Example 5: Real-Time Analytics Dashboard

### Context

Real-time metrics aggregation for a SaaS platform dashboard.

### Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Application Services                  │
│   [Auth] [API] [Workers] [Billing] [Notifications]      │
└────────────────────────┬────────────────────────────────┘
                         │ Events
              ┌──────────▼──────────┐
              │      Kafka          │
              │ app.events.raw      │
              └──────────┬──────────┘
                         │
              ┌──────────▼──────────┐
              │  Kafka Streams /    │
              │      ksqlDB         │
              └──────────┬──────────┘
                         │
         ┌───────────────┼───────────────┐
         │               │               │
  ┌──────▼─────┐  ┌──────▼─────┐  ┌──────▼─────┐
  │   Redis    │  │   Druid    │  │ PostgreSQL │
  │ (real-time)│  │ (OLAP)     │  │ (persist)  │
  └──────┬─────┘  └──────┬─────┘  └────────────┘
         │               │
         └───────┬───────┘
                 │
          ┌──────▼──────┐
          │  Dashboard  │
          │   (React)   │
          └─────────────┘
```

### ksqlDB Aggregations

```sql
-- Create stream from Kafka topic
CREATE STREAM app_events (
    event_id VARCHAR,
    event_type VARCHAR,
    user_id VARCHAR,
    tenant_id VARCHAR,
    timestamp TIMESTAMP,
    properties MAP<VARCHAR, VARCHAR>
) WITH (
    KAFKA_TOPIC='app.events.raw',
    VALUE_FORMAT='JSON'
);

-- Real-time active users per tenant (tumbling window)
CREATE TABLE active_users_by_tenant AS
SELECT
    tenant_id,
    COUNT_DISTINCT(user_id) AS active_users,
    WINDOWSTART AS window_start,
    WINDOWEND AS window_end
FROM app_events
WINDOW TUMBLING (SIZE 1 MINUTE)
GROUP BY tenant_id
EMIT CHANGES;

-- API request rate (hopping window for smoother metrics)
CREATE TABLE api_request_rate AS
SELECT
    tenant_id,
    COUNT(*) AS request_count,
    WINDOWSTART AS window_start
FROM app_events
WHERE event_type = 'api.request'
WINDOW HOPPING (SIZE 5 MINUTES, ADVANCE BY 1 MINUTE)
GROUP BY tenant_id
EMIT CHANGES;

-- Error rate calculation
CREATE TABLE error_rate_by_tenant AS
SELECT
    tenant_id,
    SUM(CASE WHEN event_type LIKE '%.error' THEN 1 ELSE 0 END) AS error_count,
    COUNT(*) AS total_count,
    (SUM(CASE WHEN event_type LIKE '%.error' THEN 1 ELSE 0 END) * 100.0 / COUNT(*)) AS error_rate
FROM app_events
WINDOW TUMBLING (SIZE 5 MINUTES)
GROUP BY tenant_id
EMIT CHANGES;
```

### WebSocket Updates to Dashboard

```typescript
// Backend: Push updates via WebSocket
class MetricsWebSocketHandler {
  constructor(private ksqlClient: KsqlDBClient) {}

  async streamToClient(ws: WebSocket, tenantId: string) {
    const query = `
      SELECT * FROM active_users_by_tenant
      WHERE tenant_id = '${tenantId}'
      EMIT CHANGES;
    `;

    const stream = await this.ksqlClient.streamQuery(query);

    for await (const row of stream) {
      ws.send(JSON.stringify({
        type: 'active_users',
        data: {
          activeUsers: row.active_users,
          windowStart: row.window_start,
          windowEnd: row.window_end
        }
      }));
    }
  }
}

// Frontend: React hook for real-time metrics
function useRealtimeMetrics(tenantId: string) {
  const [metrics, setMetrics] = useState<Metrics | null>(null);

  useEffect(() => {
    const ws = new WebSocket(`wss://api.example.com/metrics/${tenantId}`);

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setMetrics(prev => ({
        ...prev,
        [data.type]: data.data
      }));
    };

    return () => ws.close();
  }, [tenantId]);

  return metrics;
}
```

---

## Summary: Pattern Application

| Example | Patterns Used | Key Technologies |
|---------|---------------|------------------|
| E-Commerce | Pub/Sub, Saga (Choreography) | Kafka, Python |
| Trading | Event Sourcing, CQRS | Kafka, Event Store |
| IoT | Stream Processing, Partitioning | Kafka, Flink, MQTT |
| Saga Orchestration | Saga (Orchestration) | Python, State Machine |
| Analytics | Stream Aggregation | Kafka, ksqlDB, WebSocket |
