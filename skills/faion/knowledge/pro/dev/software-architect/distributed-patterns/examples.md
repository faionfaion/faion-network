# Distributed Patterns Examples

Real-world examples of distributed patterns in production systems across different domains.

---

## Example 1: E-commerce Order Processing

### Scenario

Online marketplace processing orders with multiple services: Order, Payment, Inventory, Shipping, Notification.

### Pattern: Orchestration Saga with Outbox

```
                    +-------------------+
                    | Order Orchestrator|
                    +-------------------+
                            |
        +-------------------+-------------------+
        |           |           |           |
        v           v           v           v
    +-------+  +--------+  +---------+  +--------+
    | Order |  | Payment|  |Inventory|  |Shipping|
    +-------+  +--------+  +---------+  +--------+
```

### Saga Steps and Compensations

| Step | Action | Compensation |
|------|--------|--------------|
| 1 | Create Order (PENDING) | Cancel Order |
| 2 | Reserve Inventory | Release Inventory |
| 3 | Process Payment | Refund Payment |
| 4 | Confirm Inventory | (already reserved) |
| 5 | Create Shipment | Cancel Shipment |
| 6 | Update Order (CONFIRMED) | - |
| 7 | Send Notification | - |

### Implementation (Python/FastAPI with Temporal)

```python
# saga_workflow.py
from temporalio import workflow
from datetime import timedelta

@workflow.defn
class OrderSagaWorkflow:
    @workflow.run
    async def run(self, order: OrderInput) -> OrderResult:
        # Step 1: Create order
        order_id = await workflow.execute_activity(
            create_order,
            order,
            start_to_close_timeout=timedelta(seconds=30),
        )

        try:
            # Step 2: Reserve inventory
            reservation_id = await workflow.execute_activity(
                reserve_inventory,
                ReserveInventoryInput(order_id=order_id, items=order.items),
                start_to_close_timeout=timedelta(seconds=30),
            )

            # Step 3: Process payment
            payment_id = await workflow.execute_activity(
                process_payment,
                PaymentInput(order_id=order_id, amount=order.total),
                start_to_close_timeout=timedelta(seconds=60),
            )

            # Step 4: Confirm inventory (commit reservation)
            await workflow.execute_activity(
                confirm_inventory,
                ConfirmInventoryInput(reservation_id=reservation_id),
                start_to_close_timeout=timedelta(seconds=30),
            )

            # Step 5: Create shipment
            shipment_id = await workflow.execute_activity(
                create_shipment,
                ShipmentInput(order_id=order_id, address=order.address),
                start_to_close_timeout=timedelta(seconds=30),
            )

            # Step 6: Confirm order
            await workflow.execute_activity(
                confirm_order,
                ConfirmOrderInput(order_id=order_id),
                start_to_close_timeout=timedelta(seconds=10),
            )

            # Step 7: Send notification (fire-and-forget)
            await workflow.execute_activity(
                send_notification,
                NotificationInput(
                    user_id=order.user_id,
                    type="ORDER_CONFIRMED",
                    order_id=order_id
                ),
                start_to_close_timeout=timedelta(seconds=10),
            )

            return OrderResult(order_id=order_id, status="CONFIRMED")

        except Exception as e:
            # Compensation: reverse in opposite order
            await self._compensate(order_id, reservation_id, payment_id)
            raise

    async def _compensate(
        self,
        order_id: str,
        reservation_id: str | None,
        payment_id: str | None
    ):
        # Compensation must be idempotent
        if payment_id:
            await workflow.execute_activity(
                refund_payment,
                RefundInput(payment_id=payment_id),
                start_to_close_timeout=timedelta(seconds=60),
            )

        if reservation_id:
            await workflow.execute_activity(
                release_inventory,
                ReleaseInventoryInput(reservation_id=reservation_id),
                start_to_close_timeout=timedelta(seconds=30),
            )

        await workflow.execute_activity(
            cancel_order,
            CancelOrderInput(order_id=order_id),
            start_to_close_timeout=timedelta(seconds=30),
        )
```

### Outbox Implementation for Order Service

```python
# models.py
from sqlalchemy import Column, String, DateTime, JSON
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Outbox(Base):
    __tablename__ = "outbox"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    aggregate_type = Column(String(100), nullable=False)
    aggregate_id = Column(String(100), nullable=False)
    event_type = Column(String(100), nullable=False)
    payload = Column(JSON, nullable=False)
    created_at = Column(DateTime, server_default="now()")
    published_at = Column(DateTime, nullable=True)

# order_service.py
from sqlalchemy.orm import Session

class OrderService:
    def create_order(self, db: Session, order_data: OrderCreate) -> Order:
        # Create order in same transaction as outbox entry
        order = Order(**order_data.dict(), status="PENDING")
        db.add(order)

        # Add event to outbox (same transaction!)
        outbox_entry = Outbox(
            aggregate_type="Order",
            aggregate_id=str(order.id),
            event_type="OrderCreated",
            payload={
                "order_id": str(order.id),
                "user_id": order.user_id,
                "items": order_data.items,
                "total": order_data.total,
            }
        )
        db.add(outbox_entry)

        db.commit()
        return order
```

### Key Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Saga type | Orchestration | Complex flow, need visibility |
| Event publishing | Outbox pattern | Atomic with DB, reliable |
| Orchestrator | Temporal | Durable execution, retries |
| Compensation order | Reverse | Ensures consistency |

---

## Example 2: Banking Transfer System

### Scenario

Inter-account money transfer requiring strong consistency for core ledger operations.

### Pattern: Hybrid 2PC + Saga

Use 2PC for core ledger updates, Saga for auxiliary services (notifications, audit).

### Architecture

```
                     Transfer Service
                            |
            +---------------+---------------+
            |                               |
     [2PC: Core Ledger]           [Saga: Auxiliary]
            |                               |
    +-------+-------+              +--------+--------+
    |               |              |        |        |
Debit Account  Credit Account  AML Check  Audit   Notify
```

### 2PC for Core Transfer (Go)

```go
// transfer_service.go
package transfer

import (
    "context"
    "database/sql"
)

type TransferService struct {
    db *sql.DB
}

func (s *TransferService) ExecuteTransfer(
    ctx context.Context,
    fromAccount, toAccount string,
    amount decimal.Decimal,
) error {
    // Start 2PC transaction
    tx, err := s.db.BeginTx(ctx, &sql.TxOptions{
        Isolation: sql.LevelSerializable,
    })
    if err != nil {
        return fmt.Errorf("begin transaction: %w", err)
    }
    defer tx.Rollback()

    // Phase 1: Prepare - Verify and lock accounts

    // Debit source account (with lock)
    var sourceBalance decimal.Decimal
    err = tx.QueryRowContext(ctx, `
        SELECT balance FROM accounts
        WHERE id = $1
        FOR UPDATE
    `, fromAccount).Scan(&sourceBalance)
    if err != nil {
        return fmt.Errorf("lock source account: %w", err)
    }

    if sourceBalance.LessThan(amount) {
        return ErrInsufficientFunds
    }

    // Lock destination account
    _, err = tx.ExecContext(ctx, `
        SELECT 1 FROM accounts
        WHERE id = $1
        FOR UPDATE
    `, toAccount)
    if err != nil {
        return fmt.Errorf("lock destination account: %w", err)
    }

    // Phase 2: Commit - Execute updates

    // Debit
    _, err = tx.ExecContext(ctx, `
        UPDATE accounts
        SET balance = balance - $1,
            updated_at = NOW()
        WHERE id = $2
    `, amount, fromAccount)
    if err != nil {
        return fmt.Errorf("debit: %w", err)
    }

    // Credit
    _, err = tx.ExecContext(ctx, `
        UPDATE accounts
        SET balance = balance + $1,
            updated_at = NOW()
        WHERE id = $2
    `, amount, toAccount)
    if err != nil {
        return fmt.Errorf("credit: %w", err)
    }

    // Record transaction
    _, err = tx.ExecContext(ctx, `
        INSERT INTO transactions
        (id, from_account, to_account, amount, status, created_at)
        VALUES ($1, $2, $3, $4, 'COMPLETED', NOW())
    `, uuid.New(), fromAccount, toAccount, amount)
    if err != nil {
        return fmt.Errorf("record transaction: %w", err)
    }

    // Write to outbox for saga continuation
    _, err = tx.ExecContext(ctx, `
        INSERT INTO outbox
        (id, aggregate_type, aggregate_id, event_type, payload)
        VALUES ($1, 'Transfer', $2, 'TransferCompleted', $3)
    `, uuid.New(), transferID, payload)
    if err != nil {
        return fmt.Errorf("write outbox: %w", err)
    }

    // Commit 2PC
    if err = tx.Commit(); err != nil {
        return fmt.Errorf("commit: %w", err)
    }

    return nil
}
```

### Saga for Auxiliary Operations

```go
// transfer_saga.go
func (s *TransferSaga) HandleTransferCompleted(ctx context.Context, event TransferCompletedEvent) error {
    // Step 1: AML/Compliance check (async)
    if err := s.amlService.CheckTransaction(ctx, event.TransferID); err != nil {
        // Flag for review but don't rollback transfer
        s.flagForReview(event.TransferID, err)
    }

    // Step 2: Audit log (must succeed)
    if err := s.auditService.LogTransfer(ctx, AuditEntry{
        TransferID: event.TransferID,
        FromAccount: event.FromAccount,
        ToAccount: event.ToAccount,
        Amount: event.Amount,
        Timestamp: time.Now(),
    }); err != nil {
        // Retry with backoff
        return fmt.Errorf("audit failed: %w", err)
    }

    // Step 3: Notifications (best effort)
    go s.notifyUsers(event)

    return nil
}
```

### Key Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Core transfer | 2PC | Must be atomic, strong consistency |
| Auxiliary services | Saga | Eventually consistent acceptable |
| Notification failure | Ignore | Not critical, can retry manually |
| Audit failure | Retry | Compliance requirement |

---

## Example 3: Real-time Analytics Platform

### Scenario

Processing millions of events per second for real-time dashboards with historical analysis.

### Pattern: Event Sourcing + CQRS

```
                          Event Producers
                                |
                                v
                    +-------------------+
                    |  Kafka (Events)   |
                    +-------------------+
                                |
            +-------------------+-------------------+
            |                   |                   |
            v                   v                   v
    +-------------+     +-------------+     +-------------+
    | Real-time   |     | Historical  |     | Aggregate   |
    | Projection  |     | Projection  |     | Projection  |
    | (Redis)     |     | (ClickHouse)|     | (PostgreSQL)|
    +-------------+     +-------------+     +-------------+
            |                   |                   |
            v                   v                   v
    Dashboard API       Analytics API       Reports API
```

### Event Schema

```json
{
  "event_id": "uuid",
  "event_type": "PageView",
  "aggregate_id": "session-123",
  "aggregate_type": "Session",
  "version": 1,
  "timestamp": "2025-01-25T10:30:00Z",
  "data": {
    "user_id": "user-456",
    "page": "/products/123",
    "referrer": "/home",
    "device": "mobile",
    "country": "US"
  },
  "metadata": {
    "correlation_id": "req-789",
    "causation_id": "event-abc"
  }
}
```

### Event Store (Python/Kafka)

```python
# event_store.py
from confluent_kafka import Producer, Consumer
from dataclasses import dataclass
import json

@dataclass
class Event:
    event_id: str
    event_type: str
    aggregate_id: str
    aggregate_type: str
    version: int
    timestamp: str
    data: dict
    metadata: dict

class EventStore:
    def __init__(self, bootstrap_servers: str, topic: str):
        self.producer = Producer({
            'bootstrap.servers': bootstrap_servers,
            'enable.idempotence': True,  # Exactly-once semantics
            'acks': 'all',
        })
        self.topic = topic

    def append(self, event: Event) -> None:
        key = f"{event.aggregate_type}:{event.aggregate_id}"
        value = json.dumps({
            'event_id': event.event_id,
            'event_type': event.event_type,
            'aggregate_id': event.aggregate_id,
            'aggregate_type': event.aggregate_type,
            'version': event.version,
            'timestamp': event.timestamp,
            'data': event.data,
            'metadata': event.metadata,
        })

        self.producer.produce(
            self.topic,
            key=key.encode(),
            value=value.encode(),
            on_delivery=self._delivery_callback,
        )
        self.producer.flush()

    def _delivery_callback(self, err, msg):
        if err:
            raise Exception(f"Event delivery failed: {err}")
```

### Real-time Projection (Redis)

```python
# realtime_projection.py
import redis
from datetime import datetime, timedelta

class RealtimeProjection:
    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client

    def handle_page_view(self, event: Event):
        """Update real-time metrics on each page view."""
        data = event.data
        timestamp = datetime.fromisoformat(event.timestamp)
        minute_bucket = timestamp.strftime("%Y-%m-%d-%H-%M")

        pipe = self.redis.pipeline()

        # Active users (sliding window)
        pipe.sadd(f"active_users:{minute_bucket}", data['user_id'])
        pipe.expire(f"active_users:{minute_bucket}", 3600)

        # Page views counter
        pipe.hincrby(f"pageviews:{minute_bucket}", data['page'], 1)
        pipe.expire(f"pageviews:{minute_bucket}", 3600)

        # Real-time dashboard counters
        pipe.incr("stats:total_pageviews")
        pipe.hincrby("stats:pageviews_by_device", data['device'], 1)
        pipe.hincrby("stats:pageviews_by_country", data['country'], 1)

        # Top pages (sorted set)
        pipe.zincrby("top_pages:hourly", 1, data['page'])

        pipe.execute()

    def get_dashboard_stats(self) -> dict:
        """Get current dashboard statistics."""
        now = datetime.utcnow()

        # Count active users in last 5 minutes
        active_users = set()
        for i in range(5):
            minute = (now - timedelta(minutes=i)).strftime("%Y-%m-%d-%H-%M")
            users = self.redis.smembers(f"active_users:{minute}")
            active_users.update(users)

        return {
            'active_users': len(active_users),
            'total_pageviews': int(self.redis.get("stats:total_pageviews") or 0),
            'pageviews_by_device': self.redis.hgetall("stats:pageviews_by_device"),
            'top_pages': self.redis.zrevrange("top_pages:hourly", 0, 9, withscores=True),
        }
```

### Historical Projection (ClickHouse)

```python
# historical_projection.py
from clickhouse_driver import Client

class HistoricalProjection:
    def __init__(self, clickhouse_client: Client):
        self.client = clickhouse_client

    def handle_page_view(self, event: Event):
        """Insert event into ClickHouse for historical analysis."""
        data = event.data

        self.client.execute(
            """
            INSERT INTO pageviews (
                event_id, timestamp, user_id, page,
                referrer, device, country
            ) VALUES
            """,
            [(
                event.event_id,
                event.timestamp,
                data['user_id'],
                data['page'],
                data.get('referrer'),
                data['device'],
                data['country'],
            )]
        )

    def get_analytics(
        self,
        start_date: str,
        end_date: str,
        group_by: str = 'day'
    ) -> list:
        """Get historical analytics."""
        return self.client.execute(
            f"""
            SELECT
                toStartOf{group_by.capitalize()}(timestamp) as period,
                count() as pageviews,
                uniq(user_id) as unique_users,
                topK(10)(page) as top_pages
            FROM pageviews
            WHERE timestamp BETWEEN %(start)s AND %(end)s
            GROUP BY period
            ORDER BY period
            """,
            {'start': start_date, 'end': end_date}
        )
```

### Key Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Event store | Kafka | High throughput, ordering, retention |
| Real-time store | Redis | Sub-millisecond reads |
| Historical store | ClickHouse | Columnar, fast aggregations |
| Projections | Multiple | Optimized for query patterns |
| Exactly-once | Kafka idempotence | Accurate counts |

---

## Example 4: Microservices with Full Resilience

### Scenario

API Gateway calling multiple microservices with varying reliability.

### Pattern: Circuit Breaker + Bulkhead + Retry

```
            +----------------+
            |  API Gateway   |
            +----------------+
                    |
    +---------------+---------------+
    |               |               |
    v               v               v
+--------+     +--------+     +--------+
|Product |     | Price  |     | Review |
|Service |     | Service|     | Service|
|(stable)|     |(flaky) |     |(slow)  |
+--------+     +--------+     +--------+
```

### Resilience4j Configuration (Spring Boot)

```yaml
# application.yml
resilience4j:
  circuitbreaker:
    configs:
      default:
        register-health-indicator: true
        sliding-window-type: COUNT_BASED
        sliding-window-size: 10
        failure-rate-threshold: 50
        slow-call-rate-threshold: 50
        slow-call-duration-threshold: 2s
        permitted-number-of-calls-in-half-open-state: 3
        wait-duration-in-open-state: 30s
        automatic-transition-from-open-to-half-open-enabled: true
    instances:
      productService:
        base-config: default
        failure-rate-threshold: 30
      priceService:
        base-config: default
        failure-rate-threshold: 60
        slow-call-duration-threshold: 1s
      reviewService:
        base-config: default
        failure-rate-threshold: 70
        slow-call-duration-threshold: 3s

  bulkhead:
    configs:
      default:
        max-concurrent-calls: 25
        max-wait-duration: 100ms
    instances:
      productService:
        max-concurrent-calls: 50
      priceService:
        max-concurrent-calls: 20
      reviewService:
        max-concurrent-calls: 10  # Slow service, limit impact

  retry:
    configs:
      default:
        max-attempts: 3
        wait-duration: 500ms
        enable-exponential-backoff: true
        exponential-backoff-multiplier: 2
        retry-exceptions:
          - java.io.IOException
          - java.net.SocketTimeoutException
    instances:
      priceService:
        max-attempts: 5  # Flaky, more retries

  ratelimiter:
    configs:
      default:
        limit-for-period: 100
        limit-refresh-period: 1s
        timeout-duration: 0
    instances:
      reviewService:
        limit-for-period: 50  # Protect slow service
```

### Service Client (Java/Spring)

```java
// ProductAggregatorService.java
@Service
public class ProductAggregatorService {

    private final ProductServiceClient productClient;
    private final PriceServiceClient priceClient;
    private final ReviewServiceClient reviewClient;

    @CircuitBreaker(name = "productService", fallbackMethod = "getProductFallback")
    @Bulkhead(name = "productService")
    @Retry(name = "productService")
    public Product getProduct(String productId) {
        return productClient.getProduct(productId);
    }

    @CircuitBreaker(name = "priceService", fallbackMethod = "getPriceFallback")
    @Bulkhead(name = "priceService")
    @Retry(name = "priceService")
    public Price getPrice(String productId) {
        return priceClient.getPrice(productId);
    }

    @CircuitBreaker(name = "reviewService", fallbackMethod = "getReviewsFallback")
    @Bulkhead(name = "reviewService")
    @RateLimiter(name = "reviewService")
    public List<Review> getReviews(String productId) {
        return reviewClient.getReviews(productId);
    }

    // Fallback methods
    public Product getProductFallback(String productId, Exception e) {
        log.warn("Product service unavailable, returning cached", e);
        return cacheService.getCachedProduct(productId)
            .orElse(Product.unavailable(productId));
    }

    public Price getPriceFallback(String productId, Exception e) {
        log.warn("Price service unavailable, returning cached", e);
        return cacheService.getCachedPrice(productId)
            .orElse(Price.unavailable());
    }

    public List<Review> getReviewsFallback(String productId, Exception e) {
        log.warn("Review service unavailable", e);
        return Collections.emptyList();  // Non-critical, return empty
    }

    // Aggregate with graceful degradation
    public ProductDetails getProductDetails(String productId) {
        CompletableFuture<Product> productFuture =
            CompletableFuture.supplyAsync(() -> getProduct(productId));
        CompletableFuture<Price> priceFuture =
            CompletableFuture.supplyAsync(() -> getPrice(productId));
        CompletableFuture<List<Review>> reviewsFuture =
            CompletableFuture.supplyAsync(() -> getReviews(productId));

        return CompletableFuture.allOf(productFuture, priceFuture, reviewsFuture)
            .thenApply(v -> ProductDetails.builder()
                .product(productFuture.join())
                .price(priceFuture.join())
                .reviews(reviewsFuture.join())
                .build())
            .join();
    }
}
```

### Monitoring Metrics

```java
// MetricsConfig.java
@Configuration
public class MetricsConfig {

    @Bean
    public MeterRegistryCustomizer<MeterRegistry> metricsCustomizer() {
        return registry -> {
            // Circuit breaker state
            CircuitBreakerRegistry.ofDefaults()
                .getAllCircuitBreakers()
                .forEach(cb -> {
                    Gauge.builder("circuit_breaker_state", cb,
                        c -> c.getState().getOrder())
                        .tag("name", cb.getName())
                        .register(registry);
                });

            // Bulkhead available permits
            BulkheadRegistry.ofDefaults()
                .getAllBulkheads()
                .forEach(bh -> {
                    Gauge.builder("bulkhead_available", bh,
                        b -> b.getMetrics().getAvailableConcurrentCalls())
                        .tag("name", bh.getName())
                        .register(registry);
                });
        };
    }
}
```

---

## Example 5: Idempotent Payment API

### Scenario

Payment processing API that must handle duplicate requests safely.

### Pattern: Idempotency Key + Response Caching

### Implementation (Python/FastAPI)

```python
# idempotency.py
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
import redis
import hashlib
import json
from datetime import timedelta

app = FastAPI()
redis_client = redis.Redis(host='localhost', port=6379, db=0)

IDEMPOTENCY_TTL = timedelta(hours=24)

class PaymentRequest(BaseModel):
    amount: float
    currency: str
    recipient_id: str

class PaymentResponse(BaseModel):
    payment_id: str
    status: str
    amount: float
    currency: str

def get_idempotency_lock(key: str) -> bool:
    """Try to acquire lock for idempotency key."""
    return redis_client.set(
        f"lock:{key}",
        "processing",
        nx=True,  # Only set if not exists
        ex=30,    # 30 second lock timeout
    )

def release_idempotency_lock(key: str):
    redis_client.delete(f"lock:{key}")

def get_cached_response(key: str) -> PaymentResponse | None:
    cached = redis_client.get(f"idempotency:{key}")
    if cached:
        return PaymentResponse(**json.loads(cached))
    return None

def cache_response(key: str, response: PaymentResponse, status_code: int):
    """Cache successful response. Don't cache 5xx errors."""
    if status_code < 500:
        redis_client.setex(
            f"idempotency:{key}",
            IDEMPOTENCY_TTL,
            json.dumps({
                "payment_id": response.payment_id,
                "status": response.status,
                "amount": response.amount,
                "currency": response.currency,
                "_status_code": status_code,
            })
        )

@app.post("/payments", response_model=PaymentResponse)
async def create_payment(
    payment: PaymentRequest,
    idempotency_key: str = Header(..., alias="Idempotency-Key"),
):
    # Step 1: Check for cached response
    cached = get_cached_response(idempotency_key)
    if cached:
        return cached  # Return same response for duplicate request

    # Step 2: Acquire lock for this idempotency key
    if not get_idempotency_lock(idempotency_key):
        # Another request is processing with same key
        raise HTTPException(
            status_code=409,
            detail="Request with this idempotency key is being processed"
        )

    try:
        # Step 3: Verify request payload matches (optional security check)
        payload_hash = hashlib.sha256(
            payment.json().encode()
        ).hexdigest()

        stored_hash = redis_client.get(f"payload:{idempotency_key}")
        if stored_hash and stored_hash.decode() != payload_hash:
            raise HTTPException(
                status_code=422,
                detail="Idempotency key reused with different payload"
            )

        redis_client.setex(
            f"payload:{idempotency_key}",
            IDEMPOTENCY_TTL,
            payload_hash
        )

        # Step 4: Process payment
        payment_result = await process_payment(payment)

        response = PaymentResponse(
            payment_id=payment_result.id,
            status=payment_result.status,
            amount=payment.amount,
            currency=payment.currency,
        )

        # Step 5: Cache response AFTER successful processing
        cache_response(idempotency_key, response, 200)

        return response

    finally:
        # Always release lock
        release_idempotency_lock(idempotency_key)


async def process_payment(payment: PaymentRequest) -> PaymentResult:
    """Actual payment processing logic."""
    # Database transaction to create payment
    async with database.transaction():
        payment_record = await db.payments.create(
            amount=payment.amount,
            currency=payment.currency,
            recipient_id=payment.recipient_id,
            status="PENDING",
        )

        # Call payment provider
        provider_result = await payment_provider.charge(
            amount=payment.amount,
            currency=payment.currency,
        )

        # Update status
        await db.payments.update(
            id=payment_record.id,
            status="COMPLETED" if provider_result.success else "FAILED",
            provider_reference=provider_result.reference,
        )

        return PaymentResult(
            id=payment_record.id,
            status=payment_record.status,
        )
```

### Client Usage

```python
# client_example.py
import httpx
import uuid

async def create_payment_safely(amount: float, recipient: str):
    """Create payment with idempotency."""
    idempotency_key = str(uuid.uuid4())  # Generate once per logical operation

    async with httpx.AsyncClient() as client:
        for attempt in range(3):
            try:
                response = await client.post(
                    "https://api.example.com/payments",
                    json={
                        "amount": amount,
                        "currency": "USD",
                        "recipient_id": recipient,
                    },
                    headers={
                        "Idempotency-Key": idempotency_key,  # Same key for retries
                    },
                    timeout=30.0,
                )

                if response.status_code == 200:
                    return response.json()
                elif response.status_code == 409:
                    # Concurrent request, wait and retry
                    await asyncio.sleep(1)
                    continue
                else:
                    response.raise_for_status()

            except httpx.TimeoutException:
                # Safe to retry with same idempotency key
                continue

    raise Exception("Payment failed after retries")
```

---

## Summary: Pattern Selection by Use Case

| Use Case | Primary Pattern | Supporting Patterns |
|----------|-----------------|---------------------|
| E-commerce orders | Saga (Orchestration) | Outbox, Idempotency |
| Banking transfers | 2PC (core) + Saga (auxiliary) | Audit logging |
| Real-time analytics | Event Sourcing + CQRS | Multiple projections |
| API resilience | Circuit Breaker | Bulkhead, Retry, Rate Limit |
| Payment processing | Idempotency | Response caching |
| Distributed coordination | Leader Election | Consensus (Raft) |
| High-throughput messaging | Outbox + CDC | Idempotent consumers |

---

## Anti-patterns to Avoid

| Anti-pattern | Problem | Solution |
|--------------|---------|----------|
| Distributed transactions everywhere | Latency, coupling | Use Saga with eventual consistency |
| Synchronous saga steps | Blocking, slow | Use async events where possible |
| Missing compensation | Inconsistent state | Design compensation for every step |
| Non-idempotent operations | Duplicates on retry | Implement idempotency keys |
| Unbounded retries | Resource exhaustion | Use circuit breaker + max retries |
| Single bulkhead | Cascading failures | Isolate per dependency |
| Ignoring ordering | Race conditions | Use ordered processing (Kafka partitions) |
