# Distributed Patterns Templates

Copy-paste configurations and code templates for implementing distributed patterns.

---

## 1. Saga Pattern Templates

### 1.1 Temporal Workflow (Python)

```python
# saga_workflow.py
from temporalio import workflow, activity
from temporalio.common import RetryPolicy
from dataclasses import dataclass
from datetime import timedelta
from typing import List
import uuid

# --- Data Classes ---

@dataclass
class SagaStep:
    name: str
    action_activity: str
    compensation_activity: str
    timeout: timedelta = timedelta(seconds=30)

@dataclass
class SagaContext:
    saga_id: str
    correlation_id: str
    completed_steps: List[str]
    compensation_data: dict

# --- Saga Workflow ---

@workflow.defn
class GenericSagaWorkflow:
    """
    Generic saga workflow that executes steps and compensates on failure.
    Customize by defining steps and activities.
    """

    def __init__(self):
        self.context = None
        self.steps: List[SagaStep] = []

    @workflow.run
    async def run(self, input_data: dict, steps: List[SagaStep]) -> dict:
        self.context = SagaContext(
            saga_id=str(uuid.uuid4()),
            correlation_id=input_data.get("correlation_id", str(uuid.uuid4())),
            completed_steps=[],
            compensation_data={},
        )
        self.steps = steps

        try:
            result = {}
            for step in self.steps:
                step_result = await self._execute_step(step, input_data, result)
                result[step.name] = step_result
                self.context.completed_steps.append(step.name)

            return {"status": "COMPLETED", "result": result}

        except Exception as e:
            await self._compensate()
            return {"status": "COMPENSATED", "error": str(e)}

    async def _execute_step(
        self,
        step: SagaStep,
        input_data: dict,
        previous_results: dict
    ) -> dict:
        retry_policy = RetryPolicy(
            initial_interval=timedelta(seconds=1),
            maximum_interval=timedelta(seconds=30),
            backoff_coefficient=2.0,
            maximum_attempts=3,
        )

        return await workflow.execute_activity(
            step.action_activity,
            args=[{
                "saga_id": self.context.saga_id,
                "correlation_id": self.context.correlation_id,
                "input": input_data,
                "previous": previous_results,
            }],
            start_to_close_timeout=step.timeout,
            retry_policy=retry_policy,
        )

    async def _compensate(self):
        """Execute compensations in reverse order."""
        for step_name in reversed(self.context.completed_steps):
            step = next(s for s in self.steps if s.name == step_name)

            try:
                await workflow.execute_activity(
                    step.compensation_activity,
                    args=[{
                        "saga_id": self.context.saga_id,
                        "correlation_id": self.context.correlation_id,
                        "compensation_data": self.context.compensation_data.get(step_name, {}),
                    }],
                    start_to_close_timeout=step.timeout,
                    retry_policy=RetryPolicy(maximum_attempts=5),
                )
            except Exception as e:
                # Log but continue compensation
                workflow.logger.error(f"Compensation failed for {step_name}: {e}")


# --- Activity Definitions ---

@activity.defn
async def create_order(data: dict) -> dict:
    """Example: Create order activity."""
    # Implementation here
    order_id = str(uuid.uuid4())
    return {"order_id": order_id, "status": "CREATED"}

@activity.defn
async def cancel_order(data: dict) -> dict:
    """Example: Cancel order compensation."""
    # Implementation here
    return {"status": "CANCELLED"}

# --- Usage Example ---

ORDER_SAGA_STEPS = [
    SagaStep(
        name="create_order",
        action_activity="create_order",
        compensation_activity="cancel_order",
        timeout=timedelta(seconds=30),
    ),
    SagaStep(
        name="reserve_inventory",
        action_activity="reserve_inventory",
        compensation_activity="release_inventory",
        timeout=timedelta(seconds=30),
    ),
    SagaStep(
        name="process_payment",
        action_activity="process_payment",
        compensation_activity="refund_payment",
        timeout=timedelta(seconds=60),
    ),
    SagaStep(
        name="create_shipment",
        action_activity="create_shipment",
        compensation_activity="cancel_shipment",
        timeout=timedelta(seconds=30),
    ),
]
```

### 1.2 Choreography Saga Events (TypeScript/Kafka)

```typescript
// events.ts
interface SagaEvent {
  eventId: string;
  eventType: string;
  sagaId: string;
  correlationId: string;
  timestamp: string;
  data: Record<string, unknown>;
  metadata: {
    causationId?: string;
    version: number;
  };
}

// Event Types
const EVENTS = {
  // Order Events
  ORDER_CREATED: 'order.created',
  ORDER_CONFIRMED: 'order.confirmed',
  ORDER_CANCELLED: 'order.cancelled',

  // Payment Events
  PAYMENT_PROCESSED: 'payment.processed',
  PAYMENT_FAILED: 'payment.failed',
  PAYMENT_REFUNDED: 'payment.refunded',

  // Inventory Events
  INVENTORY_RESERVED: 'inventory.reserved',
  INVENTORY_RELEASED: 'inventory.released',
  INVENTORY_INSUFFICIENT: 'inventory.insufficient',
} as const;

// event_handler.ts
import { Kafka, Consumer, Producer } from 'kafkajs';

class SagaEventHandler {
  private consumer: Consumer;
  private producer: Producer;

  constructor(kafka: Kafka, groupId: string) {
    this.consumer = kafka.consumer({ groupId });
    this.producer = kafka.producer({ idempotent: true });
  }

  async start(topics: string[]) {
    await this.consumer.connect();
    await this.producer.connect();
    await this.consumer.subscribe({ topics, fromBeginning: false });

    await this.consumer.run({
      eachMessage: async ({ topic, partition, message }) => {
        const event: SagaEvent = JSON.parse(message.value!.toString());
        await this.handleEvent(event);
      },
    });
  }

  private async handleEvent(event: SagaEvent) {
    const handlers: Record<string, (e: SagaEvent) => Promise<void>> = {
      [EVENTS.ORDER_CREATED]: this.handleOrderCreated.bind(this),
      [EVENTS.PAYMENT_PROCESSED]: this.handlePaymentProcessed.bind(this),
      [EVENTS.PAYMENT_FAILED]: this.handlePaymentFailed.bind(this),
      [EVENTS.INVENTORY_RESERVED]: this.handleInventoryReserved.bind(this),
      [EVENTS.INVENTORY_INSUFFICIENT]: this.handleInventoryInsufficient.bind(this),
    };

    const handler = handlers[event.eventType];
    if (handler) {
      await handler(event);
    }
  }

  // Handler implementations
  private async handleOrderCreated(event: SagaEvent) {
    // Reserve inventory when order is created
    await this.publishEvent({
      eventType: 'inventory.reserve_requested',
      sagaId: event.sagaId,
      correlationId: event.correlationId,
      data: {
        orderId: event.data.orderId,
        items: event.data.items,
      },
    });
  }

  private async handleInventoryReserved(event: SagaEvent) {
    // Process payment when inventory is reserved
    await this.publishEvent({
      eventType: 'payment.process_requested',
      sagaId: event.sagaId,
      correlationId: event.correlationId,
      data: {
        orderId: event.data.orderId,
        amount: event.data.amount,
        reservationId: event.data.reservationId,
      },
    });
  }

  private async handlePaymentFailed(event: SagaEvent) {
    // Compensate: release inventory
    await this.publishEvent({
      eventType: 'inventory.release_requested',
      sagaId: event.sagaId,
      correlationId: event.correlationId,
      data: {
        reservationId: event.data.reservationId,
        reason: 'payment_failed',
      },
    });

    // Compensate: cancel order
    await this.publishEvent({
      eventType: 'order.cancel_requested',
      sagaId: event.sagaId,
      correlationId: event.correlationId,
      data: {
        orderId: event.data.orderId,
        reason: 'payment_failed',
      },
    });
  }

  private async publishEvent(params: {
    eventType: string;
    sagaId: string;
    correlationId: string;
    data: Record<string, unknown>;
  }) {
    const event: SagaEvent = {
      eventId: crypto.randomUUID(),
      eventType: params.eventType,
      sagaId: params.sagaId,
      correlationId: params.correlationId,
      timestamp: new Date().toISOString(),
      data: params.data,
      metadata: { version: 1 },
    };

    await this.producer.send({
      topic: 'saga-events',
      messages: [
        {
          key: params.sagaId,
          value: JSON.stringify(event),
        },
      ],
    });
  }
}
```

---

## 2. Circuit Breaker Templates

### 2.1 Resilience4j (Java/Spring Boot)

```yaml
# application.yml
resilience4j:
  circuitbreaker:
    configs:
      default:
        register-health-indicator: true
        sliding-window-type: COUNT_BASED
        sliding-window-size: 10
        minimum-number-of-calls: 5
        failure-rate-threshold: 50
        slow-call-rate-threshold: 50
        slow-call-duration-threshold: 2s
        permitted-number-of-calls-in-half-open-state: 3
        wait-duration-in-open-state: 30s
        automatic-transition-from-open-to-half-open-enabled: true
        record-exceptions:
          - java.io.IOException
          - java.net.SocketTimeoutException
          - java.net.ConnectException
        ignore-exceptions:
          - com.example.BusinessException
      strict:
        failure-rate-threshold: 30
        wait-duration-in-open-state: 60s
    instances:
      paymentService:
        base-config: strict
      inventoryService:
        base-config: default
      notificationService:
        base-config: default
        failure-rate-threshold: 70  # More lenient
```

```java
// CircuitBreakerService.java
import io.github.resilience4j.circuitbreaker.annotation.CircuitBreaker;
import io.github.resilience4j.circuitbreaker.CircuitBreakerRegistry;
import org.springframework.stereotype.Service;

@Service
public class PaymentServiceClient {

    private final WebClient webClient;
    private final CircuitBreakerRegistry circuitBreakerRegistry;

    @CircuitBreaker(name = "paymentService", fallbackMethod = "processPaymentFallback")
    public PaymentResult processPayment(PaymentRequest request) {
        return webClient.post()
            .uri("/api/payments")
            .bodyValue(request)
            .retrieve()
            .bodyToMono(PaymentResult.class)
            .block();
    }

    // Fallback method - same signature + Exception parameter
    public PaymentResult processPaymentFallback(PaymentRequest request, Exception e) {
        log.warn("Payment service unavailable, using fallback", e);

        // Option 1: Return cached/default response
        return PaymentResult.pending(request.getOrderId());

        // Option 2: Queue for later processing
        // paymentQueue.enqueue(request);
        // return PaymentResult.queued(request.getOrderId());
    }

    // Programmatic circuit breaker check
    public boolean isPaymentServiceHealthy() {
        var cb = circuitBreakerRegistry.circuitBreaker("paymentService");
        return cb.getState() != CircuitBreaker.State.OPEN;
    }
}
```

### 2.2 Python Circuit Breaker

```python
# circuit_breaker.py
import time
from enum import Enum
from dataclasses import dataclass, field
from typing import Callable, TypeVar, Generic
from functools import wraps
import threading

T = TypeVar('T')

class CircuitState(Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"

@dataclass
class CircuitBreakerConfig:
    failure_threshold: int = 5
    success_threshold: int = 3
    timeout: float = 30.0
    slow_call_threshold: float = 2.0
    slow_call_rate_threshold: float = 0.5

@dataclass
class CircuitBreakerMetrics:
    total_calls: int = 0
    successful_calls: int = 0
    failed_calls: int = 0
    slow_calls: int = 0
    consecutive_successes: int = 0
    consecutive_failures: int = 0
    last_failure_time: float = 0

class CircuitBreaker(Generic[T]):
    def __init__(self, name: str, config: CircuitBreakerConfig = None):
        self.name = name
        self.config = config or CircuitBreakerConfig()
        self.state = CircuitState.CLOSED
        self.metrics = CircuitBreakerMetrics()
        self._lock = threading.Lock()

    def call(self, func: Callable[..., T], *args, **kwargs) -> T:
        with self._lock:
            if self.state == CircuitState.OPEN:
                if self._should_attempt_reset():
                    self.state = CircuitState.HALF_OPEN
                else:
                    raise CircuitBreakerOpenError(f"Circuit {self.name} is OPEN")

        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            duration = time.time() - start_time
            self._on_success(duration)
            return result
        except Exception as e:
            self._on_failure()
            raise

    def _should_attempt_reset(self) -> bool:
        return (time.time() - self.metrics.last_failure_time) >= self.config.timeout

    def _on_success(self, duration: float):
        with self._lock:
            self.metrics.total_calls += 1
            self.metrics.successful_calls += 1
            self.metrics.consecutive_successes += 1
            self.metrics.consecutive_failures = 0

            if duration > self.config.slow_call_threshold:
                self.metrics.slow_calls += 1

            if self.state == CircuitState.HALF_OPEN:
                if self.metrics.consecutive_successes >= self.config.success_threshold:
                    self._close()

    def _on_failure(self):
        with self._lock:
            self.metrics.total_calls += 1
            self.metrics.failed_calls += 1
            self.metrics.consecutive_failures += 1
            self.metrics.consecutive_successes = 0
            self.metrics.last_failure_time = time.time()

            if self.state == CircuitState.HALF_OPEN:
                self._open()
            elif self.metrics.consecutive_failures >= self.config.failure_threshold:
                self._open()

    def _open(self):
        self.state = CircuitState.OPEN
        # Emit event for monitoring

    def _close(self):
        self.state = CircuitState.CLOSED
        self.metrics.consecutive_successes = 0
        self.metrics.consecutive_failures = 0
        # Emit event for monitoring

class CircuitBreakerOpenError(Exception):
    pass

# Decorator
def circuit_breaker(name: str, config: CircuitBreakerConfig = None):
    cb = CircuitBreaker(name, config)

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return cb.call(func, *args, **kwargs)
        wrapper.circuit_breaker = cb
        return wrapper
    return decorator

# Usage
@circuit_breaker("payment_service", CircuitBreakerConfig(failure_threshold=3))
def call_payment_service(payment_data):
    return requests.post("https://payment.api/charge", json=payment_data)
```

---

## 3. Bulkhead Templates

### 3.1 Resilience4j Bulkhead (Java)

```yaml
# application.yml
resilience4j:
  bulkhead:
    configs:
      default:
        max-concurrent-calls: 25
        max-wait-duration: 100ms
      high-capacity:
        max-concurrent-calls: 100
        max-wait-duration: 50ms
      limited:
        max-concurrent-calls: 10
        max-wait-duration: 200ms
    instances:
      paymentService:
        base-config: default
      inventoryService:
        base-config: high-capacity
      externalApiService:
        base-config: limited

  thread-pool-bulkhead:
    configs:
      default:
        max-thread-pool-size: 20
        core-thread-pool-size: 10
        queue-capacity: 50
        keep-alive-duration: 100ms
    instances:
      reportService:
        max-thread-pool-size: 5
        core-thread-pool-size: 2
        queue-capacity: 10
```

```java
// BulkheadService.java
@Service
public class ApiAggregatorService {

    @Bulkhead(name = "paymentService", type = Bulkhead.Type.SEMAPHORE)
    @CircuitBreaker(name = "paymentService")
    public PaymentStatus getPaymentStatus(String paymentId) {
        return paymentClient.getStatus(paymentId);
    }

    @Bulkhead(name = "reportService", type = Bulkhead.Type.THREADPOOL)
    public CompletableFuture<Report> generateReport(ReportRequest request) {
        return reportService.generate(request);
    }

    // Fallback for bulkhead rejection
    public PaymentStatus getPaymentStatusFallback(String paymentId, BulkheadFullException e) {
        log.warn("Bulkhead full for payment service");
        return PaymentStatus.unknown(paymentId);
    }
}
```

### 3.2 Python Semaphore Bulkhead

```python
# bulkhead.py
import asyncio
from dataclasses import dataclass
from typing import TypeVar, Callable, Awaitable
from functools import wraps
import time

T = TypeVar('T')

@dataclass
class BulkheadConfig:
    max_concurrent_calls: int = 25
    max_wait_duration: float = 0.1  # seconds

class BulkheadFullException(Exception):
    pass

class SemaphoreBulkhead:
    def __init__(self, name: str, config: BulkheadConfig = None):
        self.name = name
        self.config = config or BulkheadConfig()
        self._semaphore = asyncio.Semaphore(self.config.max_concurrent_calls)
        self._metrics = {
            "available_permits": self.config.max_concurrent_calls,
            "rejected_calls": 0,
            "successful_calls": 0,
        }

    async def execute(self, func: Callable[..., Awaitable[T]], *args, **kwargs) -> T:
        try:
            acquired = await asyncio.wait_for(
                self._semaphore.acquire(),
                timeout=self.config.max_wait_duration,
            )
        except asyncio.TimeoutError:
            self._metrics["rejected_calls"] += 1
            raise BulkheadFullException(f"Bulkhead {self.name} is full")

        try:
            self._metrics["available_permits"] -= 1
            result = await func(*args, **kwargs)
            self._metrics["successful_calls"] += 1
            return result
        finally:
            self._semaphore.release()
            self._metrics["available_permits"] += 1

    @property
    def metrics(self):
        return self._metrics.copy()

def bulkhead(name: str, config: BulkheadConfig = None):
    bh = SemaphoreBulkhead(name, config)

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            return await bh.execute(func, *args, **kwargs)
        wrapper.bulkhead = bh
        return wrapper
    return decorator

# Usage
@bulkhead("external_api", BulkheadConfig(max_concurrent_calls=10))
async def call_external_api(data):
    async with aiohttp.ClientSession() as session:
        async with session.post("https://api.external.com/data", json=data) as resp:
            return await resp.json()
```

---

## 4. Outbox Pattern Templates

### 4.1 PostgreSQL Outbox Table

```sql
-- migrations/001_create_outbox.sql
CREATE TABLE IF NOT EXISTS outbox (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    aggregate_type VARCHAR(100) NOT NULL,
    aggregate_id VARCHAR(100) NOT NULL,
    event_type VARCHAR(100) NOT NULL,
    payload JSONB NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    published_at TIMESTAMPTZ,
    retry_count INT DEFAULT 0,
    last_error TEXT,
    CONSTRAINT outbox_unique_event UNIQUE (aggregate_type, aggregate_id, event_type, created_at)
);

CREATE INDEX idx_outbox_unpublished ON outbox (created_at)
    WHERE published_at IS NULL;

CREATE INDEX idx_outbox_aggregate ON outbox (aggregate_type, aggregate_id);

-- Cleanup job (run periodically)
-- DELETE FROM outbox WHERE published_at IS NOT NULL AND published_at < NOW() - INTERVAL '7 days';
```

### 4.2 Outbox Publisher (Python)

```python
# outbox_publisher.py
import asyncio
import json
from datetime import datetime
from typing import List
import asyncpg
from aiokafka import AIOKafkaProducer

class OutboxPublisher:
    def __init__(
        self,
        db_pool: asyncpg.Pool,
        kafka_producer: AIOKafkaProducer,
        topic: str,
        batch_size: int = 100,
        poll_interval: float = 1.0,
    ):
        self.db_pool = db_pool
        self.producer = kafka_producer
        self.topic = topic
        self.batch_size = batch_size
        self.poll_interval = poll_interval
        self._running = False

    async def start(self):
        self._running = True
        while self._running:
            try:
                await self._process_batch()
            except Exception as e:
                print(f"Outbox publisher error: {e}")
            await asyncio.sleep(self.poll_interval)

    async def stop(self):
        self._running = False

    async def _process_batch(self):
        async with self.db_pool.acquire() as conn:
            # Fetch unpublished messages with FOR UPDATE SKIP LOCKED
            rows = await conn.fetch("""
                SELECT id, aggregate_type, aggregate_id, event_type, payload, created_at
                FROM outbox
                WHERE published_at IS NULL
                ORDER BY created_at
                LIMIT $1
                FOR UPDATE SKIP LOCKED
            """, self.batch_size)

            if not rows:
                return

            published_ids = []
            for row in rows:
                try:
                    # Publish to Kafka
                    message = {
                        "event_id": str(row["id"]),
                        "aggregate_type": row["aggregate_type"],
                        "aggregate_id": row["aggregate_id"],
                        "event_type": row["event_type"],
                        "payload": row["payload"],
                        "timestamp": row["created_at"].isoformat(),
                    }

                    await self.producer.send_and_wait(
                        self.topic,
                        key=f"{row['aggregate_type']}:{row['aggregate_id']}".encode(),
                        value=json.dumps(message).encode(),
                    )
                    published_ids.append(row["id"])

                except Exception as e:
                    # Mark failed, increment retry count
                    await conn.execute("""
                        UPDATE outbox
                        SET retry_count = retry_count + 1, last_error = $1
                        WHERE id = $2
                    """, str(e), row["id"])

            # Mark as published
            if published_ids:
                await conn.execute("""
                    UPDATE outbox
                    SET published_at = NOW()
                    WHERE id = ANY($1)
                """, published_ids)

# Usage
async def main():
    db_pool = await asyncpg.create_pool("postgresql://...")
    producer = AIOKafkaProducer(bootstrap_servers="localhost:9092")
    await producer.start()

    publisher = OutboxPublisher(db_pool, producer, "domain-events")
    await publisher.start()
```

### 4.3 Debezium CDC Configuration

```json
// debezium-connector.json
{
  "name": "outbox-connector",
  "config": {
    "connector.class": "io.debezium.connector.postgresql.PostgresConnector",
    "database.hostname": "postgres",
    "database.port": "5432",
    "database.user": "debezium",
    "database.password": "${file:/secrets/db-password}",
    "database.dbname": "orders",
    "database.server.name": "orders-db",
    "plugin.name": "pgoutput",
    "publication.name": "outbox_publication",
    "table.include.list": "public.outbox",
    "tombstones.on.delete": "false",
    "transforms": "outbox",
    "transforms.outbox.type": "io.debezium.transforms.outbox.EventRouter",
    "transforms.outbox.table.fields.additional.placement": "aggregate_type:header:aggregateType",
    "transforms.outbox.route.by.field": "aggregate_type",
    "transforms.outbox.route.topic.replacement": "events.${routedByValue}",
    "key.converter": "org.apache.kafka.connect.storage.StringConverter",
    "value.converter": "org.apache.kafka.connect.json.JsonConverter",
    "value.converter.schemas.enable": "false"
  }
}
```

---

## 5. Idempotency Templates

### 5.1 Redis-based Idempotency (Python/FastAPI)

```python
# idempotency.py
from fastapi import Header, HTTPException, Request, Response
from functools import wraps
import redis
import json
import hashlib
from datetime import timedelta

class IdempotencyMiddleware:
    def __init__(
        self,
        redis_client: redis.Redis,
        ttl: timedelta = timedelta(hours=24),
    ):
        self.redis = redis_client
        self.ttl = ttl

    async def process_request(
        self,
        idempotency_key: str,
        request_hash: str,
    ) -> dict | None:
        """
        Returns cached response if exists, None otherwise.
        Raises HTTPException if key is being processed or payload mismatch.
        """
        # Check for existing response
        cached = self.redis.get(f"idempotency:{idempotency_key}")
        if cached:
            data = json.loads(cached)
            if data.get("request_hash") != request_hash:
                raise HTTPException(
                    status_code=422,
                    detail="Idempotency key reused with different payload"
                )
            return data.get("response")

        # Try to acquire lock
        acquired = self.redis.set(
            f"lock:{idempotency_key}",
            "processing",
            nx=True,
            ex=30,  # 30 second lock
        )
        if not acquired:
            raise HTTPException(
                status_code=409,
                detail="Request with this idempotency key is being processed"
            )

        return None

    async def cache_response(
        self,
        idempotency_key: str,
        request_hash: str,
        response: dict,
        status_code: int,
    ):
        """Cache response if not a server error."""
        # Don't cache 5xx errors
        if status_code >= 500:
            self.redis.delete(f"lock:{idempotency_key}")
            return

        self.redis.setex(
            f"idempotency:{idempotency_key}",
            self.ttl,
            json.dumps({
                "request_hash": request_hash,
                "response": response,
                "status_code": status_code,
            }),
        )
        self.redis.delete(f"lock:{idempotency_key}")

    def release_lock(self, idempotency_key: str):
        self.redis.delete(f"lock:{idempotency_key}")


def idempotent(redis_client: redis.Redis, ttl: timedelta = timedelta(hours=24)):
    """Decorator for idempotent endpoints."""
    middleware = IdempotencyMiddleware(redis_client, ttl)

    def decorator(func):
        @wraps(func)
        async def wrapper(
            *args,
            idempotency_key: str = Header(..., alias="Idempotency-Key"),
            request: Request,
            **kwargs
        ):
            # Hash request body
            body = await request.body()
            request_hash = hashlib.sha256(body).hexdigest()

            try:
                # Check for cached response
                cached = await middleware.process_request(idempotency_key, request_hash)
                if cached:
                    return cached

                # Execute handler
                result = await func(*args, **kwargs)

                # Cache response
                response_data = result.dict() if hasattr(result, 'dict') else result
                await middleware.cache_response(
                    idempotency_key,
                    request_hash,
                    response_data,
                    200,
                )

                return result

            except HTTPException:
                middleware.release_lock(idempotency_key)
                raise
            except Exception as e:
                middleware.release_lock(idempotency_key)
                raise

        return wrapper
    return decorator

# Usage
@app.post("/payments")
@idempotent(redis_client)
async def create_payment(payment: PaymentRequest):
    # Process payment
    return PaymentResponse(...)
```

### 5.2 Database-based Idempotency (Go)

```go
// idempotency.go
package idempotency

import (
    "context"
    "crypto/sha256"
    "database/sql"
    "encoding/hex"
    "encoding/json"
    "errors"
    "time"
)

var (
    ErrDuplicateRequest = errors.New("duplicate request with different payload")
    ErrRequestInProgress = errors.New("request is being processed")
)

type Store struct {
    db  *sql.DB
    ttl time.Duration
}

type IdempotencyRecord struct {
    Key          string
    RequestHash  string
    Response     []byte
    StatusCode   int
    CreatedAt    time.Time
    ProcessedAt  *time.Time
}

func NewStore(db *sql.DB, ttl time.Duration) *Store {
    return &Store{db: db, ttl: ttl}
}

func (s *Store) CheckAndLock(ctx context.Context, key string, requestBody []byte) (*IdempotencyRecord, error) {
    requestHash := hashBody(requestBody)

    tx, err := s.db.BeginTx(ctx, nil)
    if err != nil {
        return nil, err
    }
    defer tx.Rollback()

    // Check existing record
    var record IdempotencyRecord
    err = tx.QueryRowContext(ctx, `
        SELECT key, request_hash, response, status_code, created_at, processed_at
        FROM idempotency_keys
        WHERE key = $1
        FOR UPDATE
    `, key).Scan(
        &record.Key, &record.RequestHash, &record.Response,
        &record.StatusCode, &record.CreatedAt, &record.ProcessedAt,
    )

    if err == nil {
        // Record exists
        if record.RequestHash != requestHash {
            return nil, ErrDuplicateRequest
        }
        if record.ProcessedAt != nil {
            return &record, nil // Return cached response
        }
        return nil, ErrRequestInProgress
    }

    if !errors.Is(err, sql.ErrNoRows) {
        return nil, err
    }

    // Create new record (locked)
    _, err = tx.ExecContext(ctx, `
        INSERT INTO idempotency_keys (key, request_hash, created_at)
        VALUES ($1, $2, $3)
    `, key, requestHash, time.Now())
    if err != nil {
        return nil, err
    }

    return tx.Commit(), nil
}

func (s *Store) SaveResponse(ctx context.Context, key string, response interface{}, statusCode int) error {
    responseBytes, err := json.Marshal(response)
    if err != nil {
        return err
    }

    // Don't cache 5xx errors
    if statusCode >= 500 {
        _, err = s.db.ExecContext(ctx, `DELETE FROM idempotency_keys WHERE key = $1`, key)
        return err
    }

    _, err = s.db.ExecContext(ctx, `
        UPDATE idempotency_keys
        SET response = $1, status_code = $2, processed_at = $3
        WHERE key = $4
    `, responseBytes, statusCode, time.Now(), key)
    return err
}

func (s *Store) ReleaseLock(ctx context.Context, key string) error {
    _, err := s.db.ExecContext(ctx, `DELETE FROM idempotency_keys WHERE key = $1`, key)
    return err
}

func hashBody(body []byte) string {
    hash := sha256.Sum256(body)
    return hex.EncodeToString(hash[:])
}

// SQL Schema
/*
CREATE TABLE idempotency_keys (
    key VARCHAR(255) PRIMARY KEY,
    request_hash VARCHAR(64) NOT NULL,
    response JSONB,
    status_code INT,
    created_at TIMESTAMPTZ NOT NULL,
    processed_at TIMESTAMPTZ
);

CREATE INDEX idx_idempotency_cleanup ON idempotency_keys (created_at)
    WHERE processed_at IS NOT NULL;
*/
```

---

## 6. Retry Templates

### 6.1 Exponential Backoff with Jitter

```python
# retry.py
import asyncio
import random
from typing import TypeVar, Callable, Awaitable, Type
from functools import wraps

T = TypeVar('T')

class RetryConfig:
    def __init__(
        self,
        max_attempts: int = 3,
        base_delay: float = 1.0,
        max_delay: float = 60.0,
        exponential_base: float = 2.0,
        jitter: str = "full",  # "full", "equal", "decorrelated"
        retryable_exceptions: tuple = (Exception,),
    ):
        self.max_attempts = max_attempts
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.exponential_base = exponential_base
        self.jitter = jitter
        self.retryable_exceptions = retryable_exceptions

def calculate_delay(attempt: int, config: RetryConfig, prev_delay: float = 0) -> float:
    """Calculate delay with jitter."""
    exp_delay = config.base_delay * (config.exponential_base ** attempt)
    capped_delay = min(exp_delay, config.max_delay)

    if config.jitter == "full":
        return random.uniform(0, capped_delay)
    elif config.jitter == "equal":
        return capped_delay / 2 + random.uniform(0, capped_delay / 2)
    elif config.jitter == "decorrelated":
        return min(config.max_delay, random.uniform(config.base_delay, prev_delay * 3))
    else:
        return capped_delay

def retry(config: RetryConfig = None):
    """Retry decorator with exponential backoff."""
    config = config or RetryConfig()

    def decorator(func: Callable[..., Awaitable[T]]) -> Callable[..., Awaitable[T]]:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> T:
            last_exception = None
            prev_delay = config.base_delay

            for attempt in range(config.max_attempts):
                try:
                    return await func(*args, **kwargs)
                except config.retryable_exceptions as e:
                    last_exception = e
                    if attempt == config.max_attempts - 1:
                        raise

                    delay = calculate_delay(attempt, config, prev_delay)
                    prev_delay = delay
                    await asyncio.sleep(delay)

            raise last_exception

        return wrapper
    return decorator

# Usage
@retry(RetryConfig(
    max_attempts=5,
    base_delay=0.5,
    retryable_exceptions=(ConnectionError, TimeoutError),
))
async def call_external_service(data):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data, timeout=10) as resp:
            return await resp.json()
```

---

## 7. Leader Election Templates

### 7.1 etcd Leader Election (Go)

```go
// leader_election.go
package election

import (
    "context"
    "log"
    "time"

    clientv3 "go.etcd.io/etcd/client/v3"
    "go.etcd.io/etcd/client/v3/concurrency"
)

type LeaderElector struct {
    client   *clientv3.Client
    session  *concurrency.Session
    election *concurrency.Election
    isLeader bool
    nodeID   string
}

func NewLeaderElector(endpoints []string, nodeID string, ttl int) (*LeaderElector, error) {
    client, err := clientv3.New(clientv3.Config{
        Endpoints:   endpoints,
        DialTimeout: 5 * time.Second,
    })
    if err != nil {
        return nil, err
    }

    session, err := concurrency.NewSession(client, concurrency.WithTTL(ttl))
    if err != nil {
        return nil, err
    }

    election := concurrency.NewElection(session, "/service/leader")

    return &LeaderElector{
        client:   client,
        session:  session,
        election: election,
        nodeID:   nodeID,
    }, nil
}

func (le *LeaderElector) Campaign(ctx context.Context) error {
    log.Printf("Node %s: Campaigning for leadership...", le.nodeID)

    if err := le.election.Campaign(ctx, le.nodeID); err != nil {
        return err
    }

    le.isLeader = true
    log.Printf("Node %s: Became leader!", le.nodeID)
    return nil
}

func (le *LeaderElector) Resign(ctx context.Context) error {
    if !le.isLeader {
        return nil
    }

    log.Printf("Node %s: Resigning leadership...", le.nodeID)
    le.isLeader = false
    return le.election.Resign(ctx)
}

func (le *LeaderElector) GetLeader(ctx context.Context) (string, error) {
    resp, err := le.election.Leader(ctx)
    if err != nil {
        return "", err
    }
    if len(resp.Kvs) == 0 {
        return "", nil
    }
    return string(resp.Kvs[0].Value), nil
}

func (le *LeaderElector) IsLeader() bool {
    return le.isLeader
}

func (le *LeaderElector) Close() {
    le.session.Close()
    le.client.Close()
}

// Usage
func main() {
    elector, err := NewLeaderElector(
        []string{"localhost:2379"},
        "node-1",
        10, // TTL in seconds
    )
    if err != nil {
        log.Fatal(err)
    }
    defer elector.Close()

    ctx, cancel := context.WithCancel(context.Background())
    defer cancel()

    // Campaign for leadership
    go func() {
        if err := elector.Campaign(ctx); err != nil {
            log.Printf("Campaign failed: %v", err)
        }
    }()

    // Run leader-only tasks when elected
    for {
        if elector.IsLeader() {
            // Perform leader tasks
            runScheduledJobs()
        }
        time.Sleep(time.Second)
    }
}
```

### 7.2 Redis Leader Election (Python)

```python
# redis_leader.py
import asyncio
import uuid
from datetime import timedelta
import redis.asyncio as redis

class RedisLeaderElection:
    def __init__(
        self,
        redis_client: redis.Redis,
        key: str,
        node_id: str = None,
        ttl: timedelta = timedelta(seconds=30),
        renew_interval: timedelta = timedelta(seconds=10),
    ):
        self.redis = redis_client
        self.key = f"leader:{key}"
        self.node_id = node_id or str(uuid.uuid4())
        self.ttl = ttl
        self.renew_interval = renew_interval
        self._is_leader = False
        self._running = False

    async def start(self):
        """Start leader election loop."""
        self._running = True
        while self._running:
            try:
                await self._try_acquire_leadership()
            except Exception as e:
                print(f"Leader election error: {e}")
                self._is_leader = False
            await asyncio.sleep(self.renew_interval.total_seconds())

    async def stop(self):
        """Stop and release leadership."""
        self._running = False
        if self._is_leader:
            await self._release_leadership()

    async def _try_acquire_leadership(self):
        """Try to acquire or renew leadership."""
        # Try to set if not exists (acquire)
        acquired = await self.redis.set(
            self.key,
            self.node_id,
            nx=True,
            ex=self.ttl,
        )

        if acquired:
            self._is_leader = True
            return

        # Check if we already hold leadership
        current_leader = await self.redis.get(self.key)
        if current_leader and current_leader.decode() == self.node_id:
            # Renew our leadership
            await self.redis.expire(self.key, self.ttl)
            self._is_leader = True
        else:
            self._is_leader = False

    async def _release_leadership(self):
        """Release leadership if we hold it."""
        # Only delete if we are the current leader
        script = """
        if redis.call("get", KEYS[1]) == ARGV[1] then
            return redis.call("del", KEYS[1])
        else
            return 0
        end
        """
        await self.redis.eval(script, 1, self.key, self.node_id)
        self._is_leader = False

    @property
    def is_leader(self) -> bool:
        return self._is_leader

    async def get_current_leader(self) -> str | None:
        leader = await self.redis.get(self.key)
        return leader.decode() if leader else None

# Usage
async def main():
    redis_client = redis.Redis(host='localhost', port=6379)

    election = RedisLeaderElection(
        redis_client,
        key="my-service",
        ttl=timedelta(seconds=30),
        renew_interval=timedelta(seconds=10),
    )

    # Start election in background
    asyncio.create_task(election.start())

    # Main loop
    while True:
        if election.is_leader:
            print("I am the leader, running scheduled jobs...")
            await run_scheduled_jobs()
        await asyncio.sleep(1)
```

---

## 8. Rate Limiting Templates

### 8.1 Token Bucket (Redis)

```python
# rate_limiter.py
import time
import redis

class TokenBucketRateLimiter:
    def __init__(
        self,
        redis_client: redis.Redis,
        key_prefix: str,
        capacity: int,
        refill_rate: float,  # tokens per second
    ):
        self.redis = redis_client
        self.key_prefix = key_prefix
        self.capacity = capacity
        self.refill_rate = refill_rate

    def allow_request(self, identifier: str, tokens: int = 1) -> tuple[bool, dict]:
        """
        Check if request is allowed and consume tokens.
        Returns (allowed, info_dict).
        """
        key = f"{self.key_prefix}:{identifier}"
        now = time.time()

        # Lua script for atomic token bucket
        script = """
        local key = KEYS[1]
        local capacity = tonumber(ARGV[1])
        local refill_rate = tonumber(ARGV[2])
        local now = tonumber(ARGV[3])
        local requested = tonumber(ARGV[4])

        local bucket = redis.call('HGETALL', key)
        local tokens = capacity
        local last_refill = now

        if #bucket > 0 then
            tokens = tonumber(bucket[2])
            last_refill = tonumber(bucket[4])

            -- Refill tokens
            local elapsed = now - last_refill
            local refill = elapsed * refill_rate
            tokens = math.min(capacity, tokens + refill)
        end

        local allowed = 0
        if tokens >= requested then
            tokens = tokens - requested
            allowed = 1
        end

        redis.call('HMSET', key, 'tokens', tokens, 'last_refill', now)
        redis.call('EXPIRE', key, 3600)

        return {allowed, tokens, capacity}
        """

        result = self.redis.eval(
            script, 1, key,
            self.capacity, self.refill_rate, now, tokens
        )

        allowed = bool(result[0])
        remaining = int(result[1])

        return allowed, {
            "allowed": allowed,
            "remaining": remaining,
            "limit": self.capacity,
            "reset_at": now + (self.capacity - remaining) / self.refill_rate,
        }

# FastAPI middleware
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse

app = FastAPI()
rate_limiter = TokenBucketRateLimiter(
    redis.Redis(),
    "api_rate_limit",
    capacity=100,  # 100 requests
    refill_rate=10,  # 10 per second
)

@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    # Use IP or API key as identifier
    identifier = request.client.host

    allowed, info = rate_limiter.allow_request(identifier)

    if not allowed:
        return JSONResponse(
            status_code=429,
            content={"detail": "Rate limit exceeded"},
            headers={
                "X-RateLimit-Limit": str(info["limit"]),
                "X-RateLimit-Remaining": str(info["remaining"]),
                "Retry-After": str(int(info["reset_at"] - time.time())),
            },
        )

    response = await call_next(request)
    response.headers["X-RateLimit-Limit"] = str(info["limit"])
    response.headers["X-RateLimit-Remaining"] = str(info["remaining"])
    return response
```

---

## Summary: Quick Reference

| Pattern | Template File Section | Primary Use Case |
|---------|----------------------|------------------|
| Saga (Temporal) | 1.1 | Complex workflows |
| Saga (Choreography) | 1.2 | Event-driven microservices |
| Circuit Breaker | 2.x | External service calls |
| Bulkhead | 3.x | Resource isolation |
| Outbox | 4.x | Reliable event publishing |
| Idempotency | 5.x | Safe API retries |
| Retry | 6.1 | Transient failures |
| Leader Election | 7.x | Singleton services |
| Rate Limiting | 8.1 | API protection |
