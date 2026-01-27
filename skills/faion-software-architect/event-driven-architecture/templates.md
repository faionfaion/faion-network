# Event-Driven Architecture Templates

Ready-to-use templates for event schemas, consumers, producers, and infrastructure.

---

## Event Schema Templates

### CloudEvents Base Template

```json
{
  "specversion": "1.0",
  "id": "{{uuid}}",
  "source": "/{{service-name}}",
  "type": "{{domain}}.{{context}}.{{entity}}.{{action}}",
  "datacontenttype": "application/json",
  "dataschema": "https://{{domain}}/schemas/{{entity}}/{{version}}.json",
  "subject": "{{entity-id}}",
  "time": "{{iso8601-timestamp}}",
  "data": {
    // Event-specific payload
  }
}
```

### Domain Event Template

```json
{
  "specversion": "1.0",
  "id": "evt-{{entity}}-{{uuid}}",
  "source": "/services/{{service-name}}",
  "type": "com.{{company}}.{{domain}}.{{entity}}.{{past-tense-action}}",
  "datacontenttype": "application/json",
  "subject": "{{entity-id}}",
  "time": "2026-01-25T10:30:00.000Z",

  "correlationid": "{{request-correlation-id}}",
  "causationid": "{{causing-event-id}}",

  "data": {
    "entityId": "{{entity-id}}",
    "version": 1,
    "occurredAt": "2026-01-25T10:30:00.000Z",
    // Domain-specific fields
  }
}
```

### Integration Event Template

```json
{
  "specversion": "1.0",
  "id": "int-{{uuid}}",
  "source": "/services/{{source-service}}",
  "type": "{{company}}.integration.{{entity}}.{{action}}",
  "datacontenttype": "application/json",
  "time": "2026-01-25T10:30:00.000Z",

  "correlationid": "{{correlation-id}}",
  "tenantid": "{{tenant-id}}",

  "data": {
    // Minimal data needed for consumers
    // Use IDs, not full objects
    "entityId": "{{entity-id}}",
    "action": "{{action}}",
    "metadata": {}
  }
}
```

---

## Common Event Examples

### Order Events

**OrderCreated**
```json
{
  "specversion": "1.0",
  "id": "evt-order-f47ac10b-58cc",
  "source": "/services/order-service",
  "type": "com.example.orders.order.created",
  "datacontenttype": "application/json",
  "subject": "order-12345",
  "time": "2026-01-25T10:30:00.000Z",
  "correlationid": "req-abc123",
  "data": {
    "orderId": "order-12345",
    "customerId": "cust-789",
    "status": "CREATED",
    "items": [
      {
        "productId": "prod-001",
        "sku": "SKU-ABC",
        "quantity": 2,
        "unitPrice": 29.99,
        "currency": "USD"
      }
    ],
    "totals": {
      "subtotal": 59.98,
      "tax": 5.40,
      "shipping": 9.99,
      "total": 75.37
    },
    "shippingAddress": {
      "line1": "123 Main St",
      "city": "Seattle",
      "state": "WA",
      "postalCode": "98101",
      "country": "US"
    },
    "createdAt": "2026-01-25T10:30:00.000Z"
  }
}
```

**OrderStatusChanged**
```json
{
  "specversion": "1.0",
  "id": "evt-order-status-g58bd21c",
  "source": "/services/order-service",
  "type": "com.example.orders.order.status_changed",
  "subject": "order-12345",
  "time": "2026-01-25T10:35:00.000Z",
  "correlationid": "req-abc123",
  "causationid": "evt-payment-h69ce32d",
  "data": {
    "orderId": "order-12345",
    "previousStatus": "CREATED",
    "newStatus": "PAID",
    "reason": "Payment confirmed",
    "changedAt": "2026-01-25T10:35:00.000Z",
    "changedBy": "payment-service"
  }
}
```

### User Events

**UserRegistered**
```json
{
  "specversion": "1.0",
  "id": "evt-user-reg-a1b2c3d4",
  "source": "/services/auth-service",
  "type": "com.example.users.user.registered",
  "subject": "user-456",
  "time": "2026-01-25T14:00:00.000Z",
  "data": {
    "userId": "user-456",
    "email": "user@example.com",
    "emailVerified": false,
    "registrationMethod": "email",
    "referralCode": "REF-XYZ",
    "acceptedTermsVersion": "2026.1",
    "registeredAt": "2026-01-25T14:00:00.000Z"
  }
}
```

**UserProfileUpdated**
```json
{
  "specversion": "1.0",
  "id": "evt-user-profile-e5f6g7h8",
  "source": "/services/user-service",
  "type": "com.example.users.profile.updated",
  "subject": "user-456",
  "time": "2026-01-25T15:30:00.000Z",
  "data": {
    "userId": "user-456",
    "changedFields": ["displayName", "avatarUrl"],
    "changes": {
      "displayName": {
        "old": "John",
        "new": "John Doe"
      },
      "avatarUrl": {
        "old": null,
        "new": "https://cdn.example.com/avatars/user-456.jpg"
      }
    },
    "updatedAt": "2026-01-25T15:30:00.000Z"
  }
}
```

### Payment Events

**PaymentProcessed**
```json
{
  "specversion": "1.0",
  "id": "evt-payment-h69ce32d",
  "source": "/services/payment-service",
  "type": "com.example.payments.payment.processed",
  "subject": "payment-789",
  "time": "2026-01-25T10:35:00.000Z",
  "correlationid": "req-abc123",
  "data": {
    "paymentId": "payment-789",
    "orderId": "order-12345",
    "customerId": "cust-789",
    "amount": {
      "value": 75.37,
      "currency": "USD"
    },
    "method": "CREDIT_CARD",
    "provider": "stripe",
    "providerTransactionId": "pi_3ABC123",
    "status": "SUCCEEDED",
    "processedAt": "2026-01-25T10:35:00.000Z"
  }
}
```

---

## Producer Templates

### Python (Kafka)

```python
from kafka import KafkaProducer
from datetime import datetime, timezone
import json
import uuid

class EventProducer:
    def __init__(self, bootstrap_servers: list[str], service_name: str):
        self.service_name = service_name
        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            key_serializer=lambda k: k.encode('utf-8') if k else None,
            acks='all',  # Wait for all replicas
            retries=3,
            retry_backoff_ms=100
        )

    def create_event(
        self,
        event_type: str,
        subject: str,
        data: dict,
        correlation_id: str = None,
        causation_id: str = None
    ) -> dict:
        """Create a CloudEvents-compliant event."""
        event = {
            "specversion": "1.0",
            "id": f"evt-{uuid.uuid4()}",
            "source": f"/services/{self.service_name}",
            "type": event_type,
            "datacontenttype": "application/json",
            "subject": subject,
            "time": datetime.now(timezone.utc).isoformat(),
            "data": data
        }

        if correlation_id:
            event["correlationid"] = correlation_id
        if causation_id:
            event["causationid"] = causation_id

        return event

    def publish(
        self,
        topic: str,
        event: dict,
        key: str = None
    ):
        """Publish event to Kafka topic."""
        future = self.producer.send(
            topic,
            value=event,
            key=key or event.get("subject")
        )
        # Block until sent (or timeout)
        future.get(timeout=10)

    def publish_async(
        self,
        topic: str,
        event: dict,
        key: str = None,
        on_success=None,
        on_error=None
    ):
        """Publish event asynchronously with callbacks."""
        future = self.producer.send(
            topic,
            value=event,
            key=key or event.get("subject")
        )

        if on_success:
            future.add_callback(on_success)
        if on_error:
            future.add_errback(on_error)

    def close(self):
        self.producer.flush()
        self.producer.close()


# Usage
producer = EventProducer(
    bootstrap_servers=['kafka:9092'],
    service_name='order-service'
)

event = producer.create_event(
    event_type='com.example.orders.order.created',
    subject='order-12345',
    data={
        'orderId': 'order-12345',
        'customerId': 'cust-789',
        'items': [...]
    },
    correlation_id='req-abc123'
)

producer.publish('orders.created', event)
```

### TypeScript (Node.js + KafkaJS)

```typescript
import { Kafka, Producer, ProducerRecord } from 'kafkajs';
import { v4 as uuidv4 } from 'uuid';

interface CloudEvent<T = unknown> {
  specversion: string;
  id: string;
  source: string;
  type: string;
  datacontenttype: string;
  subject: string;
  time: string;
  correlationid?: string;
  causationid?: string;
  data: T;
}

class EventProducer {
  private producer: Producer;
  private serviceName: string;

  constructor(brokers: string[], serviceName: string) {
    const kafka = new Kafka({
      clientId: serviceName,
      brokers
    });
    this.producer = kafka.producer({
      idempotent: true,
      maxInFlightRequests: 5
    });
    this.serviceName = serviceName;
  }

  async connect(): Promise<void> {
    await this.producer.connect();
  }

  createEvent<T>(
    eventType: string,
    subject: string,
    data: T,
    correlationId?: string,
    causationId?: string
  ): CloudEvent<T> {
    return {
      specversion: '1.0',
      id: `evt-${uuidv4()}`,
      source: `/services/${this.serviceName}`,
      type: eventType,
      datacontenttype: 'application/json',
      subject,
      time: new Date().toISOString(),
      ...(correlationId && { correlationid: correlationId }),
      ...(causationId && { causationid: causationId }),
      data
    };
  }

  async publish<T>(
    topic: string,
    event: CloudEvent<T>,
    key?: string
  ): Promise<void> {
    const record: ProducerRecord = {
      topic,
      messages: [
        {
          key: key || event.subject,
          value: JSON.stringify(event),
          headers: {
            'ce-type': event.type,
            'ce-source': event.source,
            'ce-id': event.id
          }
        }
      ]
    };

    await this.producer.send(record);
  }

  async disconnect(): Promise<void> {
    await this.producer.disconnect();
  }
}

// Usage
const producer = new EventProducer(
  ['kafka:9092'],
  'order-service'
);

await producer.connect();

const event = producer.createEvent(
  'com.example.orders.order.created',
  'order-12345',
  {
    orderId: 'order-12345',
    customerId: 'cust-789',
    items: []
  },
  'req-abc123'
);

await producer.publish('orders.created', event);
```

---

## Consumer Templates

### Python (Kafka)

```python
from kafka import KafkaConsumer
from abc import ABC, abstractmethod
import json
import logging

logger = logging.getLogger(__name__)

class EventHandler(ABC):
    @abstractmethod
    def handle(self, event: dict) -> None:
        pass

class EventConsumer:
    def __init__(
        self,
        bootstrap_servers: list[str],
        group_id: str,
        topics: list[str],
        handlers: dict[str, EventHandler]
    ):
        self.consumer = KafkaConsumer(
            *topics,
            bootstrap_servers=bootstrap_servers,
            group_id=group_id,
            auto_offset_reset='earliest',
            enable_auto_commit=False,
            value_deserializer=lambda v: json.loads(v.decode('utf-8'))
        )
        self.handlers = handlers
        self.processed_ids: set[str] = set()  # In-memory (use Redis in prod)
        self.running = True

    def is_duplicate(self, event_id: str) -> bool:
        """Check if event was already processed."""
        return event_id in self.processed_ids

    def mark_processed(self, event_id: str) -> None:
        """Mark event as processed."""
        self.processed_ids.add(event_id)
        # In production: store in Redis/database with TTL

    def process_event(self, event: dict) -> None:
        """Process a single event."""
        event_id = event.get('id')
        event_type = event.get('type')

        # Idempotency check
        if self.is_duplicate(event_id):
            logger.info(f"Skipping duplicate event: {event_id}")
            return

        # Find handler
        handler = self.handlers.get(event_type)
        if not handler:
            logger.warning(f"No handler for event type: {event_type}")
            return

        try:
            handler.handle(event)
            self.mark_processed(event_id)
        except Exception as e:
            logger.error(f"Error processing event {event_id}: {e}")
            raise

    def run(self) -> None:
        """Main consumer loop."""
        logger.info("Starting consumer...")

        while self.running:
            messages = self.consumer.poll(timeout_ms=1000)

            for topic_partition, records in messages.items():
                for record in records:
                    try:
                        self.process_event(record.value)
                        self.consumer.commit()
                    except Exception as e:
                        logger.error(f"Failed to process: {e}")
                        # Send to DLQ or retry

    def stop(self) -> None:
        self.running = False
        self.consumer.close()


# Example handler
class OrderCreatedHandler(EventHandler):
    def __init__(self, inventory_service):
        self.inventory_service = inventory_service

    def handle(self, event: dict) -> None:
        data = event['data']
        order_id = data['orderId']
        items = data['items']

        # Reserve inventory
        for item in items:
            self.inventory_service.reserve(
                product_id=item['productId'],
                quantity=item['quantity'],
                order_id=order_id
            )


# Usage
handlers = {
    'com.example.orders.order.created': OrderCreatedHandler(inventory_service)
}

consumer = EventConsumer(
    bootstrap_servers=['kafka:9092'],
    group_id='inventory-service',
    topics=['orders.created'],
    handlers=handlers
)

consumer.run()
```

### TypeScript (Node.js + KafkaJS)

```typescript
import { Kafka, Consumer, EachMessagePayload } from 'kafkajs';

interface CloudEvent<T = unknown> {
  specversion: string;
  id: string;
  source: string;
  type: string;
  subject: string;
  time: string;
  data: T;
}

type EventHandler<T = unknown> = (event: CloudEvent<T>) => Promise<void>;

class EventConsumer {
  private consumer: Consumer;
  private handlers: Map<string, EventHandler> = new Map();
  private processedIds: Set<string> = new Set();

  constructor(brokers: string[], groupId: string) {
    const kafka = new Kafka({
      clientId: `${groupId}-client`,
      brokers
    });
    this.consumer = kafka.consumer({ groupId });
  }

  registerHandler<T>(eventType: string, handler: EventHandler<T>): void {
    this.handlers.set(eventType, handler as EventHandler);
  }

  async subscribe(topics: string[]): Promise<void> {
    await this.consumer.connect();

    for (const topic of topics) {
      await this.consumer.subscribe({ topic, fromBeginning: true });
    }
  }

  private isDuplicate(eventId: string): boolean {
    return this.processedIds.has(eventId);
  }

  private markProcessed(eventId: string): void {
    this.processedIds.add(eventId);
    // In production: use Redis with TTL
  }

  async run(): Promise<void> {
    await this.consumer.run({
      eachMessage: async ({ topic, partition, message }: EachMessagePayload) => {
        const event = JSON.parse(message.value!.toString()) as CloudEvent;

        // Idempotency check
        if (this.isDuplicate(event.id)) {
          console.log(`Skipping duplicate: ${event.id}`);
          return;
        }

        const handler = this.handlers.get(event.type);
        if (!handler) {
          console.warn(`No handler for: ${event.type}`);
          return;
        }

        try {
          await handler(event);
          this.markProcessed(event.id);
        } catch (error) {
          console.error(`Error processing ${event.id}:`, error);
          throw error; // Will trigger retry or DLQ
        }
      }
    });
  }

  async disconnect(): Promise<void> {
    await this.consumer.disconnect();
  }
}

// Usage
interface OrderData {
  orderId: string;
  customerId: string;
  items: Array<{ productId: string; quantity: number }>;
}

const consumer = new EventConsumer(['kafka:9092'], 'inventory-service');

consumer.registerHandler<OrderData>(
  'com.example.orders.order.created',
  async (event) => {
    const { orderId, items } = event.data;

    for (const item of items) {
      await inventoryService.reserve(
        item.productId,
        item.quantity,
        orderId
      );
    }
  }
);

await consumer.subscribe(['orders.created']);
await consumer.run();
```

---

## Saga Templates

### Saga State Machine (Python)

```python
from enum import Enum
from dataclasses import dataclass, field
from typing import Callable, Optional, Any
from datetime import datetime
import uuid

class SagaStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    COMPENSATING = "compensating"
    FAILED = "failed"

@dataclass
class SagaStep:
    name: str
    execute: Callable[[dict], Any]
    compensate: Optional[Callable[[dict], Any]] = None
    timeout_seconds: int = 30

@dataclass
class SagaState:
    saga_id: str
    saga_type: str
    status: SagaStatus
    payload: dict
    current_step_index: int = 0
    completed_steps: list[str] = field(default_factory=list)
    compensation_data: dict = field(default_factory=dict)
    error: Optional[str] = None
    started_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

class SagaOrchestrator:
    def __init__(self, saga_type: str, steps: list[SagaStep], store):
        self.saga_type = saga_type
        self.steps = steps
        self.store = store

    def start(self, payload: dict) -> str:
        """Start a new saga instance."""
        saga_id = str(uuid.uuid4())
        state = SagaState(
            saga_id=saga_id,
            saga_type=self.saga_type,
            status=SagaStatus.IN_PROGRESS,
            payload=payload
        )
        self.store.save(state)
        self._execute_current_step(state)
        return saga_id

    def _execute_current_step(self, state: SagaState) -> None:
        """Execute the current step in the saga."""
        if state.current_step_index >= len(self.steps):
            self._complete_saga(state)
            return

        step = self.steps[state.current_step_index]

        try:
            result = step.execute(state.payload)

            # Store compensation data if provided
            if result:
                state.compensation_data[step.name] = result

            state.completed_steps.append(step.name)
            state.current_step_index += 1
            state.updated_at = datetime.utcnow()
            self.store.save(state)

            # Continue to next step
            self._execute_current_step(state)

        except Exception as e:
            self._handle_failure(state, step.name, str(e))

    def _handle_failure(self, state: SagaState, step_name: str, error: str) -> None:
        """Handle step failure and start compensation."""
        state.status = SagaStatus.COMPENSATING
        state.error = f"Failed at {step_name}: {error}"
        state.updated_at = datetime.utcnow()
        self.store.save(state)

        self._compensate(state)

    def _compensate(self, state: SagaState) -> None:
        """Execute compensating transactions in reverse order."""
        for step_name in reversed(state.completed_steps):
            step = next((s for s in self.steps if s.name == step_name), None)

            if step and step.compensate:
                try:
                    compensation_data = state.compensation_data.get(step_name, {})
                    step.compensate({**state.payload, **compensation_data})
                except Exception as e:
                    # Log but continue compensating
                    print(f"Compensation failed for {step_name}: {e}")

        state.status = SagaStatus.FAILED
        state.updated_at = datetime.utcnow()
        self.store.save(state)

    def _complete_saga(self, state: SagaState) -> None:
        """Mark saga as completed."""
        state.status = SagaStatus.COMPLETED
        state.updated_at = datetime.utcnow()
        self.store.save(state)


# Usage: Order Fulfillment Saga
def reserve_inventory(payload: dict) -> dict:
    # Reserve inventory
    reservation_id = inventory_service.reserve(
        payload['items'],
        payload['order_id']
    )
    return {'reservation_id': reservation_id}

def release_inventory(payload: dict) -> None:
    # Compensate: release reserved inventory
    inventory_service.release(payload['reservation_id'])

def charge_payment(payload: dict) -> dict:
    # Process payment
    payment_id = payment_service.charge(
        payload['customer_id'],
        payload['amount']
    )
    return {'payment_id': payment_id}

def refund_payment(payload: dict) -> None:
    # Compensate: refund payment
    payment_service.refund(payload['payment_id'])

def create_shipment(payload: dict) -> dict:
    # Create shipment
    shipment_id = shipping_service.create(
        payload['order_id'],
        payload['shipping_address']
    )
    return {'shipment_id': shipment_id}

def cancel_shipment(payload: dict) -> None:
    # Compensate: cancel shipment
    shipping_service.cancel(payload['shipment_id'])


# Define saga
order_fulfillment_saga = SagaOrchestrator(
    saga_type='order_fulfillment',
    steps=[
        SagaStep(
            name='reserve_inventory',
            execute=reserve_inventory,
            compensate=release_inventory
        ),
        SagaStep(
            name='charge_payment',
            execute=charge_payment,
            compensate=refund_payment
        ),
        SagaStep(
            name='create_shipment',
            execute=create_shipment,
            compensate=cancel_shipment
        )
    ],
    store=saga_store
)

# Start saga
saga_id = order_fulfillment_saga.start({
    'order_id': 'order-12345',
    'customer_id': 'cust-789',
    'items': [...],
    'amount': 99.99,
    'shipping_address': {...}
})
```

---

## Infrastructure Templates

### Docker Compose (Kafka + Schema Registry)

```yaml
version: '3.8'

services:
  zookeeper:
    image: confluentinc/cp-zookeeper:7.5.0
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181
      ZOOKEEPER_TICK_TIME: 2000
    ports:
      - "2181:2181"

  kafka:
    image: confluentinc/cp-kafka:7.5.0
    depends_on:
      - zookeeper
    ports:
      - "9092:9092"
      - "29092:29092"
    environment:
      KAFKA_BROKER_ID: 1
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: PLAINTEXT:PLAINTEXT,PLAINTEXT_HOST:PLAINTEXT
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://kafka:29092,PLAINTEXT_HOST://localhost:9092
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
      KAFKA_GROUP_INITIAL_REBALANCE_DELAY_MS: 0
      KAFKA_AUTO_CREATE_TOPICS_ENABLE: "false"

  schema-registry:
    image: confluentinc/cp-schema-registry:7.5.0
    depends_on:
      - kafka
    ports:
      - "8081:8081"
    environment:
      SCHEMA_REGISTRY_HOST_NAME: schema-registry
      SCHEMA_REGISTRY_KAFKASTORE_BOOTSTRAP_SERVERS: kafka:29092
      SCHEMA_REGISTRY_LISTENERS: http://0.0.0.0:8081

  kafka-ui:
    image: provectuslabs/kafka-ui:latest
    depends_on:
      - kafka
      - schema-registry
    ports:
      - "8080:8080"
    environment:
      KAFKA_CLUSTERS_0_NAME: local
      KAFKA_CLUSTERS_0_BOOTSTRAPSERVERS: kafka:29092
      KAFKA_CLUSTERS_0_SCHEMAREGISTRY: http://schema-registry:8081

  # Initialize topics
  kafka-init:
    image: confluentinc/cp-kafka:7.5.0
    depends_on:
      - kafka
    entrypoint: ["/bin/sh", "-c"]
    command: |
      "
      # Wait for Kafka to be ready
      kafka-topics --bootstrap-server kafka:29092 --list

      # Create topics
      kafka-topics --bootstrap-server kafka:29092 --create --if-not-exists --topic orders.created --partitions 6 --replication-factor 1
      kafka-topics --bootstrap-server kafka:29092 --create --if-not-exists --topic orders.updated --partitions 6 --replication-factor 1
      kafka-topics --bootstrap-server kafka:29092 --create --if-not-exists --topic payments.processed --partitions 6 --replication-factor 1
      kafka-topics --bootstrap-server kafka:29092 --create --if-not-exists --topic inventory.reserved --partitions 6 --replication-factor 1
      kafka-topics --bootstrap-server kafka:29092 --create --if-not-exists --topic dlq.orders --partitions 3 --replication-factor 1

      echo 'Topics created successfully'
      "
```

### Kubernetes (Kafka Strimzi Operator)

```yaml
# kafka-cluster.yaml
apiVersion: kafka.strimzi.io/v1beta2
kind: Kafka
metadata:
  name: event-cluster
  namespace: kafka
spec:
  kafka:
    version: 3.6.0
    replicas: 3
    listeners:
      - name: plain
        port: 9092
        type: internal
        tls: false
      - name: tls
        port: 9093
        type: internal
        tls: true
    config:
      offsets.topic.replication.factor: 3
      transaction.state.log.replication.factor: 3
      transaction.state.log.min.isr: 2
      default.replication.factor: 3
      min.insync.replicas: 2
      inter.broker.protocol.version: "3.6"
    storage:
      type: jbod
      volumes:
        - id: 0
          type: persistent-claim
          size: 100Gi
          deleteClaim: false
    resources:
      requests:
        memory: 4Gi
        cpu: "1"
      limits:
        memory: 8Gi
        cpu: "2"
  zookeeper:
    replicas: 3
    storage:
      type: persistent-claim
      size: 10Gi
      deleteClaim: false
  entityOperator:
    topicOperator: {}
    userOperator: {}
---
# kafka-topics.yaml
apiVersion: kafka.strimzi.io/v1beta2
kind: KafkaTopic
metadata:
  name: orders-created
  namespace: kafka
  labels:
    strimzi.io/cluster: event-cluster
spec:
  partitions: 12
  replicas: 3
  config:
    retention.ms: 604800000  # 7 days
    cleanup.policy: delete
---
apiVersion: kafka.strimzi.io/v1beta2
kind: KafkaTopic
metadata:
  name: dlq-orders
  namespace: kafka
  labels:
    strimzi.io/cluster: event-cluster
spec:
  partitions: 6
  replicas: 3
  config:
    retention.ms: 2592000000  # 30 days
    cleanup.policy: delete
```

---

## JSON Schema Templates

### Order Event Schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://example.com/schemas/order-created.v1.json",
  "title": "OrderCreated",
  "description": "Event emitted when an order is created",
  "type": "object",
  "properties": {
    "specversion": {
      "type": "string",
      "const": "1.0"
    },
    "id": {
      "type": "string",
      "format": "uuid"
    },
    "source": {
      "type": "string",
      "format": "uri-reference"
    },
    "type": {
      "type": "string",
      "const": "com.example.orders.order.created"
    },
    "time": {
      "type": "string",
      "format": "date-time"
    },
    "data": {
      "$ref": "#/$defs/OrderData"
    }
  },
  "required": ["specversion", "id", "source", "type", "time", "data"],
  "$defs": {
    "OrderData": {
      "type": "object",
      "properties": {
        "orderId": {
          "type": "string",
          "pattern": "^order-[a-zA-Z0-9]+$"
        },
        "customerId": {
          "type": "string"
        },
        "items": {
          "type": "array",
          "items": {
            "$ref": "#/$defs/OrderItem"
          },
          "minItems": 1
        },
        "totals": {
          "$ref": "#/$defs/OrderTotals"
        }
      },
      "required": ["orderId", "customerId", "items", "totals"]
    },
    "OrderItem": {
      "type": "object",
      "properties": {
        "productId": { "type": "string" },
        "sku": { "type": "string" },
        "quantity": { "type": "integer", "minimum": 1 },
        "unitPrice": { "type": "number", "minimum": 0 }
      },
      "required": ["productId", "quantity", "unitPrice"]
    },
    "OrderTotals": {
      "type": "object",
      "properties": {
        "subtotal": { "type": "number", "minimum": 0 },
        "tax": { "type": "number", "minimum": 0 },
        "shipping": { "type": "number", "minimum": 0 },
        "total": { "type": "number", "minimum": 0 }
      },
      "required": ["subtotal", "total"]
    }
  }
}
```

---

## Summary

| Template Type | Purpose |
|---------------|---------|
| Event Schemas | CloudEvents-compliant event structure |
| Producer (Python/TS) | Event publishing with retries |
| Consumer (Python/TS) | Idempotent event handling |
| Saga Orchestrator | Distributed transaction management |
| Docker Compose | Local development environment |
| Kubernetes | Production deployment |
| JSON Schema | Event validation |
