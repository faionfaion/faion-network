# Reliability Architecture Examples

Real-world implementations of reliability patterns across different architectures and industries.

---

## Example 1: E-Commerce Platform (High Availability)

### Context
- Traffic: 100K requests/minute, 10x spikes during sales
- SLO: 99.95% availability, p99 latency <500ms
- Critical path: Product catalog, Cart, Checkout

### Architecture Overview

```
                         CloudFlare (CDN + DDoS)
                                  |
                    +-------------+-------------+
                    |                           |
              Route 53 (DNS)              Route 53 (DNS)
              (us-east-1)                 (eu-west-1)
                    |                           |
              +-----+-----+               +-----+-----+
              |           |               |           |
           ALB (AZ-1)  ALB (AZ-2)      ALB (AZ-1)  ALB (AZ-2)
              |           |               |           |
         +----+----+ +----+----+     +----+----+ +----+----+
         | EKS    | | EKS    |     | EKS    | | EKS    |
         | (3 AZ) | | (3 AZ) |     | (3 AZ) | | (3 AZ) |
         +--------+ +--------+     +--------+ +--------+
              |           |               |           |
         +----+----+ +----+----+     +----+----+
         | Aurora  | | ElastiCache|  | Aurora  |
         | Global  | | (Redis)    |  | Replica |
         +--------+ +------------+  +--------+
```

### Reliability Patterns Applied

#### 1. Circuit Breaker for Payment Service

```python
# Python with resilience4j-like pattern
from circuitbreaker import circuit

@circuit(
    failure_threshold=5,
    recovery_timeout=30,
    expected_exception=PaymentServiceError
)
def process_payment(order_id: str, payment_data: dict) -> PaymentResult:
    """Process payment with circuit breaker protection."""
    response = payment_client.charge(
        order_id=order_id,
        amount=payment_data['amount'],
        method=payment_data['method']
    )
    return PaymentResult(
        transaction_id=response.id,
        status=response.status
    )

def checkout(order: Order) -> CheckoutResult:
    try:
        payment = process_payment(order.id, order.payment)
        return CheckoutResult(success=True, payment=payment)
    except CircuitBreakerError:
        # Circuit is open - use fallback
        return queue_for_retry(order)
```

#### 2. Retry with Exponential Backoff for Inventory

```python
import random
import time
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential_jitter,
    retry_if_exception_type
)

@retry(
    stop=stop_after_attempt(4),
    wait=wait_exponential_jitter(
        initial=1,
        max=30,
        jitter=5
    ),
    retry=retry_if_exception_type((TimeoutError, ConnectionError))
)
def reserve_inventory(sku: str, quantity: int) -> ReservationResult:
    """Reserve inventory with retry on transient failures."""
    return inventory_service.reserve(
        sku=sku,
        quantity=quantity,
        timeout=5.0
    )
```

#### 3. Graceful Degradation for Product Recommendations

```python
def get_product_page(product_id: str) -> ProductPage:
    # P0: Critical - Product data (no degradation)
    product = product_service.get(product_id)

    # P1: Important - Reviews (degrade to cached)
    try:
        reviews = review_service.get_for_product(product_id)
    except ServiceUnavailable:
        reviews = cache.get(f"reviews:{product_id}", default=[])

    # P2: Optional - Recommendations (degrade to popular)
    try:
        if feature_flags.is_enabled("personalized_recommendations"):
            recommendations = ml_service.get_recommendations(
                product_id=product_id,
                user_id=current_user.id
            )
        else:
            recommendations = get_popular_products()
    except Exception:
        recommendations = get_popular_products()

    return ProductPage(
        product=product,
        reviews=reviews,
        recommendations=recommendations
    )
```

#### 4. Health Checks

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import asyncio

app = FastAPI()

class HealthStatus(BaseModel):
    status: str
    checks: dict
    version: str

@app.get("/health/live")
async def liveness():
    """Liveness probe - is the process running?"""
    return {"status": "ok"}

@app.get("/health/ready")
async def readiness():
    """Readiness probe - can we serve traffic?"""
    checks = {}

    # Check database
    try:
        await db.execute("SELECT 1")
        checks["database"] = {"status": "healthy"}
    except Exception as e:
        checks["database"] = {"status": "unhealthy", "error": str(e)}

    # Check Redis
    try:
        await redis.ping()
        checks["cache"] = {"status": "healthy"}
    except Exception as e:
        checks["cache"] = {"status": "unhealthy", "error": str(e)}

    # Check inventory service
    try:
        await inventory_client.health_check()
        checks["inventory"] = {"status": "healthy"}
    except Exception as e:
        checks["inventory"] = {"status": "degraded", "error": str(e)}

    # Overall status
    critical_healthy = all(
        checks[svc]["status"] == "healthy"
        for svc in ["database", "cache"]
    )

    if not critical_healthy:
        raise HTTPException(status_code=503, detail=checks)

    return HealthStatus(
        status="ready",
        checks=checks,
        version=settings.VERSION
    )
```

### Results
- Achieved 99.97% availability (exceeded 99.95% SLO)
- Survived 12x traffic spike during Black Friday
- Zero data loss during regional failover test
- MTTR reduced from 45 minutes to 8 minutes

---

## Example 2: Financial Services API (Zero Downtime)

### Context
- Traffic: 50K transactions/minute
- SLO: 99.99% availability (52.6 min downtime/year max)
- Regulatory: SOC2, PCI-DSS compliant
- Critical: Transaction processing, Account balance

### Architecture

```
                    Global Load Balancer
                           |
          +----------------+----------------+
          |                                 |
     US Region                         EU Region
          |                                 |
    +-----+-----+                     +-----+-----+
    |           |                     |           |
 Primary DB  Secondary DB          Primary DB  Secondary DB
 (Active)    (Sync Replica)        (Active)    (Sync Replica)
    |           |                     |           |
    +-----+-----+                     +-----+-----+
          |                                 |
          +------------ Async Replication --+
```

### Reliability Patterns Applied

#### 1. Synchronous Replication with Automatic Failover

```go
// Go implementation with database/sql and connection pooling
package db

import (
    "context"
    "database/sql"
    "time"

    "github.com/jackc/pgx/v5/pgxpool"
)

type ReplicatedDB struct {
    primary   *pgxpool.Pool
    secondary *pgxpool.Pool
    config    ReplicationConfig
}

type ReplicationConfig struct {
    PrimaryDSN           string
    SecondaryDSN         string
    MaxConnections       int32
    MinConnections       int32
    HealthCheckInterval  time.Duration
    MaxConnLifetime      time.Duration
    MaxConnIdleTime      time.Duration
}

func NewReplicatedDB(cfg ReplicationConfig) (*ReplicatedDB, error) {
    poolConfig, _ := pgxpool.ParseConfig(cfg.PrimaryDSN)
    poolConfig.MaxConns = cfg.MaxConnections
    poolConfig.MinConns = cfg.MinConnections
    poolConfig.HealthCheckPeriod = cfg.HealthCheckInterval
    poolConfig.MaxConnLifetime = cfg.MaxConnLifetime
    poolConfig.MaxConnIdleTime = cfg.MaxConnIdleTime

    primary, err := pgxpool.NewWithConfig(context.Background(), poolConfig)
    if err != nil {
        return nil, err
    }

    // Similar for secondary
    secondaryConfig, _ := pgxpool.ParseConfig(cfg.SecondaryDSN)
    // ... configure secondary pool

    return &ReplicatedDB{
        primary:   primary,
        secondary: secondary,
        config:    cfg,
    }, nil
}

func (db *ReplicatedDB) ExecuteTransaction(ctx context.Context, fn func(tx pgx.Tx) error) error {
    // Attempt on primary
    tx, err := db.primary.Begin(ctx)
    if err != nil {
        // Primary unavailable, check if we can failover
        if db.canFailover() {
            return db.executeOnSecondary(ctx, fn)
        }
        return err
    }
    defer tx.Rollback(ctx)

    if err := fn(tx); err != nil {
        return err
    }

    return tx.Commit(ctx)
}
```

#### 2. Idempotent Transaction Processing

```go
// Idempotency implementation
package transaction

import (
    "context"
    "crypto/sha256"
    "encoding/hex"
    "errors"
    "time"
)

type IdempotencyKey struct {
    Key       string
    CreatedAt time.Time
    Response  []byte
    Status    string
}

type TransactionService struct {
    db              *ReplicatedDB
    idempotencyRepo IdempotencyRepository
}

func (s *TransactionService) ProcessTransaction(
    ctx context.Context,
    idempotencyKey string,
    request TransactionRequest,
) (*TransactionResponse, error) {
    // Check for existing idempotency key
    existing, err := s.idempotencyRepo.Get(ctx, idempotencyKey)
    if err == nil && existing != nil {
        // Already processed - return cached response
        return deserializeResponse(existing.Response)
    }

    // Lock the idempotency key
    lock, err := s.idempotencyRepo.Lock(ctx, idempotencyKey, 30*time.Second)
    if err != nil {
        return nil, errors.New("concurrent request in progress")
    }
    defer lock.Release()

    // Process transaction
    response, err := s.executeTransaction(ctx, request)
    if err != nil {
        return nil, err
    }

    // Store idempotency record
    s.idempotencyRepo.Store(ctx, IdempotencyKey{
        Key:       idempotencyKey,
        CreatedAt: time.Now(),
        Response:  serializeResponse(response),
        Status:    "completed",
    })

    return response, nil
}

func GenerateIdempotencyKey(accountID string, amount int64, reference string) string {
    data := fmt.Sprintf("%s:%d:%s", accountID, amount, reference)
    hash := sha256.Sum256([]byte(data))
    return hex.EncodeToString(hash[:])
}
```

#### 3. Rate Limiting with Graceful Degradation

```go
package ratelimit

import (
    "context"
    "time"

    "github.com/go-redis/redis_rate/v10"
)

type TieredRateLimiter struct {
    limiter *redis_rate.Limiter
    tiers   map[string]RateTier
}

type RateTier struct {
    RequestsPerSecond int
    BurstSize         int
    Priority          int
}

func (r *TieredRateLimiter) Allow(ctx context.Context, clientID string, tier string) (bool, error) {
    tierConfig, ok := r.tiers[tier]
    if !ok {
        tierConfig = r.tiers["default"]
    }

    result, err := r.limiter.Allow(ctx, clientID, redis_rate.PerSecond(tierConfig.RequestsPerSecond))
    if err != nil {
        // Redis unavailable - fail open for critical tiers
        if tierConfig.Priority <= 1 { // P0, P1
            return true, nil
        }
        return false, err
    }

    return result.Allowed > 0, nil
}

// Usage in middleware
func RateLimitMiddleware(limiter *TieredRateLimiter) gin.HandlerFunc {
    return func(c *gin.Context) {
        clientID := c.GetHeader("X-Client-ID")
        tier := c.GetHeader("X-Rate-Tier")

        allowed, err := limiter.Allow(c.Request.Context(), clientID, tier)
        if err != nil {
            // Log but don't fail for critical paths
            log.Error("Rate limiter error", "error", err)
        }

        if !allowed {
            c.AbortWithStatusJSON(429, gin.H{
                "error": "rate_limit_exceeded",
                "retry_after": 1,
            })
            return
        }

        c.Next()
    }
}
```

#### 4. Circuit Breaker with Observability

```go
package circuit

import (
    "context"
    "time"

    "github.com/sony/gobreaker"
    "go.opentelemetry.io/otel"
    "go.opentelemetry.io/otel/metric"
)

type ObservableCircuitBreaker struct {
    cb              *gobreaker.CircuitBreaker
    stateGauge      metric.Int64ObservableGauge
    successCounter  metric.Int64Counter
    failureCounter  metric.Int64Counter
}

func NewObservableCircuitBreaker(name string, settings gobreaker.Settings) *ObservableCircuitBreaker {
    meter := otel.Meter("circuit-breaker")

    stateGauge, _ := meter.Int64ObservableGauge(
        "circuit_breaker_state",
        metric.WithDescription("Current state of circuit breaker (0=closed, 1=half-open, 2=open)"),
    )

    successCounter, _ := meter.Int64Counter(
        "circuit_breaker_success_total",
        metric.WithDescription("Total successful calls through circuit breaker"),
    )

    failureCounter, _ := meter.Int64Counter(
        "circuit_breaker_failure_total",
        metric.WithDescription("Total failed calls through circuit breaker"),
    )

    settings.OnStateChange = func(name string, from, to gobreaker.State) {
        log.Info("Circuit breaker state change",
            "name", name,
            "from", from.String(),
            "to", to.String(),
        )
    }

    return &ObservableCircuitBreaker{
        cb:             gobreaker.NewCircuitBreaker(settings),
        stateGauge:     stateGauge,
        successCounter: successCounter,
        failureCounter: failureCounter,
    }
}

func (ocb *ObservableCircuitBreaker) Execute(
    ctx context.Context,
    fn func() (interface{}, error),
) (interface{}, error) {
    result, err := ocb.cb.Execute(fn)

    if err != nil {
        ocb.failureCounter.Add(ctx, 1)
    } else {
        ocb.successCounter.Add(ctx, 1)
    }

    return result, err
}
```

### Results
- Achieved 99.993% availability (4.6 min downtime in year)
- Zero transactions lost during 3 regional failovers
- P99 latency maintained at 120ms under 2x normal load
- Passed all regulatory audits

---

## Example 3: Real-Time Data Platform (High Throughput)

### Context
- Throughput: 1M events/second ingestion
- SLO: 99.9% availability, <10s end-to-end latency
- Use case: Real-time analytics, fraud detection

### Architecture

```
Producers (IoT, Apps, Services)
          |
          v
    +-----+-----+
    |  Kafka    |  (3 brokers, RF=3)
    |  Cluster  |
    +-----+-----+
          |
    +-----+-----+-----+
    |           |     |
    v           v     v
Stream      Stream   Stream
Processor   Processor Processor
(Flink)     (Flink)   (Flink)
    |           |     |
    v           v     v
    +-----+-----+-----+
          |
          v
    +-----+-----+
    | ClickHouse |  (Distributed)
    |  Cluster   |
    +-----+-----+
          |
          v
    Query API
```

### Reliability Patterns Applied

#### 1. Kafka Producer with Retries and Idempotence

```java
// Java Kafka producer configuration
import org.apache.kafka.clients.producer.*;
import java.util.Properties;

public class ReliableKafkaProducer {

    private final KafkaProducer<String, byte[]> producer;

    public ReliableKafkaProducer(String bootstrapServers) {
        Properties props = new Properties();

        // Connection
        props.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, bootstrapServers);
        props.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG,
            "org.apache.kafka.common.serialization.StringSerializer");
        props.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG,
            "org.apache.kafka.common.serialization.ByteArraySerializer");

        // Reliability settings
        props.put(ProducerConfig.ACKS_CONFIG, "all");  // Wait for all replicas
        props.put(ProducerConfig.ENABLE_IDEMPOTENCE_CONFIG, true);  // Exactly-once
        props.put(ProducerConfig.RETRIES_CONFIG, Integer.MAX_VALUE);
        props.put(ProducerConfig.MAX_IN_FLIGHT_REQUESTS_PER_CONNECTION, 5);

        // Batching for throughput
        props.put(ProducerConfig.BATCH_SIZE_CONFIG, 32768);  // 32KB
        props.put(ProducerConfig.LINGER_MS_CONFIG, 5);  // Wait up to 5ms
        props.put(ProducerConfig.COMPRESSION_TYPE_CONFIG, "lz4");

        // Timeouts
        props.put(ProducerConfig.REQUEST_TIMEOUT_MS_CONFIG, 30000);
        props.put(ProducerConfig.DELIVERY_TIMEOUT_MS_CONFIG, 120000);

        this.producer = new KafkaProducer<>(props);
    }

    public CompletableFuture<RecordMetadata> sendAsync(
            String topic,
            String key,
            byte[] value) {

        CompletableFuture<RecordMetadata> future = new CompletableFuture<>();

        ProducerRecord<String, byte[]> record = new ProducerRecord<>(topic, key, value);

        producer.send(record, (metadata, exception) -> {
            if (exception != null) {
                future.completeExceptionally(exception);
            } else {
                future.complete(metadata);
            }
        });

        return future;
    }

    public void sendWithRetry(
            String topic,
            String key,
            byte[] value,
            int maxRetries) {

        int attempt = 0;
        Exception lastException = null;

        while (attempt < maxRetries) {
            try {
                sendAsync(topic, key, value).get(30, TimeUnit.SECONDS);
                return;
            } catch (Exception e) {
                lastException = e;
                attempt++;

                // Exponential backoff with jitter
                long delay = (long) (Math.pow(2, attempt) * 100 + Math.random() * 100);
                Thread.sleep(Math.min(delay, 10000));
            }
        }

        throw new RuntimeException("Failed after " + maxRetries + " attempts", lastException);
    }
}
```

#### 2. Flink Checkpoint Configuration for Exactly-Once

```java
// Flink job with checkpointing for fault tolerance
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.streaming.api.CheckpointingMode;
import org.apache.flink.runtime.state.hashmap.HashMapStateBackend;

public class FraudDetectionJob {

    public static void main(String[] args) throws Exception {
        StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();

        // Checkpointing configuration
        env.enableCheckpointing(60000);  // Checkpoint every 60 seconds
        env.getCheckpointConfig().setCheckpointingMode(CheckpointingMode.EXACTLY_ONCE);
        env.getCheckpointConfig().setMinPauseBetweenCheckpoints(30000);
        env.getCheckpointConfig().setCheckpointTimeout(300000);  // 5 minutes
        env.getCheckpointConfig().setMaxConcurrentCheckpoints(1);
        env.getCheckpointConfig().setTolerableCheckpointFailureNumber(3);

        // State backend (use RocksDB for large state)
        env.setStateBackend(new HashMapStateBackend());

        // Restart strategy
        env.setRestartStrategy(RestartStrategies.exponentialDelayRestart(
            Time.milliseconds(1000),   // Initial delay
            Time.milliseconds(60000),  // Max delay
            2.0,                       // Backoff multiplier
            Time.hours(1),             // Reset backoff after
            0.1                        // Jitter
        ));

        // Job logic
        env
            .addSource(createKafkaSource())
            .keyBy(event -> event.getUserId())
            .process(new FraudDetectionFunction())
            .addSink(createAlertSink());

        env.execute("Fraud Detection");
    }
}
```

#### 3. ClickHouse Distributed Queries with Timeouts

```sql
-- ClickHouse distributed table configuration
CREATE TABLE events_distributed ON CLUSTER '{cluster}'
(
    event_id UUID,
    user_id String,
    event_type String,
    event_time DateTime64(3),
    properties String,
    INDEX idx_user (user_id) TYPE bloom_filter GRANULARITY 1
)
ENGINE = Distributed(
    '{cluster}',
    'analytics',
    'events_local',
    xxHash64(user_id)
);

-- Query with timeout and sampling for degradation
SELECT
    user_id,
    count() as event_count,
    uniq(event_type) as unique_events
FROM events_distributed
SAMPLE 0.1  -- 10% sample for fast approximate results
WHERE event_time >= now() - INTERVAL 1 HOUR
GROUP BY user_id
HAVING event_count > 100
SETTINGS
    max_execution_time = 30,
    max_memory_usage = 10000000000,
    distributed_group_by_no_merge = 1;
```

#### 4. Dead Letter Queue for Failed Events

```python
# Python consumer with DLQ handling
from confluent_kafka import Consumer, Producer, KafkaError
import json
import logging

class ReliableConsumer:
    def __init__(self, config: dict):
        self.consumer = Consumer({
            'bootstrap.servers': config['bootstrap_servers'],
            'group.id': config['group_id'],
            'auto.offset.reset': 'earliest',
            'enable.auto.commit': False,
            'max.poll.interval.ms': 300000,
            'session.timeout.ms': 45000,
        })

        self.dlq_producer = Producer({
            'bootstrap.servers': config['bootstrap_servers'],
            'acks': 'all',
            'retries': 10,
        })

        self.dlq_topic = config['dlq_topic']
        self.max_retries = 3

    def process_messages(self, topic: str, handler):
        self.consumer.subscribe([topic])

        while True:
            msg = self.consumer.poll(1.0)

            if msg is None:
                continue

            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                logging.error(f"Consumer error: {msg.error()}")
                continue

            # Process with retries
            success = self._process_with_retry(msg, handler)

            if not success:
                # Send to DLQ
                self._send_to_dlq(msg)

            # Commit offset
            self.consumer.commit(msg)

    def _process_with_retry(self, msg, handler) -> bool:
        for attempt in range(self.max_retries):
            try:
                handler(msg.value())
                return True
            except Exception as e:
                logging.warning(f"Processing failed (attempt {attempt + 1}): {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
        return False

    def _send_to_dlq(self, original_msg):
        dlq_message = {
            'original_topic': original_msg.topic(),
            'original_partition': original_msg.partition(),
            'original_offset': original_msg.offset(),
            'original_timestamp': original_msg.timestamp()[1],
            'original_key': original_msg.key().decode() if original_msg.key() else None,
            'original_value': original_msg.value().decode(),
            'error_time': datetime.utcnow().isoformat(),
            'retry_count': self.max_retries,
        }

        self.dlq_producer.produce(
            self.dlq_topic,
            key=original_msg.key(),
            value=json.dumps(dlq_message).encode(),
        )
        self.dlq_producer.flush()
```

### Results
- Ingestion: 1.2M events/second sustained
- End-to-end latency: p99 < 8 seconds
- Zero message loss during broker failures
- Automatic recovery within 2 minutes for node failures

---

## Example 4: Multi-Region SaaS Application

### Context
- Users: Global distribution (US, EU, APAC)
- SLO: 99.95% regional, 99.99% global
- Data residency: EU data must stay in EU

### Architecture

```
               Global CDN (CloudFlare)
                        |
        +---------------+---------------+
        |               |               |
   US-EAST          EU-WEST         APAC-SOUTH
        |               |               |
   +----+----+     +----+----+     +----+----+
   | App     |     | App     |     | App     |
   | Cluster |     | Cluster |     | Cluster |
   +----+----+     +----+----+     +----+----+
        |               |               |
   +----+----+     +----+----+     +----+----+
   | Aurora  |     | Aurora  |     | Aurora  |
   | Global  |<--->| Primary |<--->| Replica |
   | Replica |     | (EU)    |     |         |
   +---------+     +---------+     +---------+
```

### Reliability Patterns Applied

#### 1. Geo-Routing with Failover

```typescript
// TypeScript edge function for geo-routing
import { getClientInfo } from '@vercel/edge';

interface RegionConfig {
  primary: string;
  fallback: string[];
  healthEndpoint: string;
}

const REGIONS: Record<string, RegionConfig> = {
  'US': {
    primary: 'https://us-east.api.example.com',
    fallback: ['https://us-west.api.example.com', 'https://eu-west.api.example.com'],
    healthEndpoint: '/health/ready',
  },
  'EU': {
    primary: 'https://eu-west.api.example.com',
    fallback: ['https://eu-central.api.example.com'],
    healthEndpoint: '/health/ready',
  },
  'APAC': {
    primary: 'https://apac-south.api.example.com',
    fallback: ['https://apac-east.api.example.com', 'https://us-west.api.example.com'],
    healthEndpoint: '/health/ready',
  },
};

const regionHealth: Map<string, { healthy: boolean; lastCheck: number }> = new Map();

async function checkHealth(url: string): Promise<boolean> {
  try {
    const response = await fetch(url, {
      method: 'GET',
      signal: AbortSignal.timeout(3000),
    });
    return response.ok;
  } catch {
    return false;
  }
}

export default async function middleware(request: Request) {
  const { geo } = getClientInfo(request);
  const continent = geo?.continent || 'US';

  const regionConfig = REGIONS[continent] || REGIONS['US'];

  // Try primary first
  const primaryHealthy = await isRegionHealthy(regionConfig.primary, regionConfig.healthEndpoint);

  if (primaryHealthy) {
    return Response.redirect(regionConfig.primary + request.url);
  }

  // Try fallbacks
  for (const fallback of regionConfig.fallback) {
    const fallbackHealthy = await isRegionHealthy(fallback, regionConfig.healthEndpoint);
    if (fallbackHealthy) {
      return Response.redirect(fallback + request.url);
    }
  }

  // All regions down - return error page
  return new Response('Service temporarily unavailable', { status: 503 });
}

async function isRegionHealthy(baseUrl: string, healthEndpoint: string): Promise<boolean> {
  const cached = regionHealth.get(baseUrl);
  const now = Date.now();

  // Cache health status for 10 seconds
  if (cached && now - cached.lastCheck < 10000) {
    return cached.healthy;
  }

  const healthy = await checkHealth(baseUrl + healthEndpoint);
  regionHealth.set(baseUrl, { healthy, lastCheck: now });

  return healthy;
}
```

#### 2. Data Residency Compliance

```python
# Django middleware for data residency
from django.conf import settings
from django.http import HttpResponseForbidden

class DataResidencyMiddleware:
    """Ensure data residency compliance by routing to correct region."""

    REGION_MAPPING = {
        'EU': ['eu-west-1', 'eu-central-1'],
        'US': ['us-east-1', 'us-west-2'],
        'APAC': ['ap-south-1', 'ap-southeast-1'],
    }

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get user's data residency requirement
        user = getattr(request, 'user', None)
        if user and hasattr(user, 'data_residency'):
            required_region = user.data_residency
            current_region = settings.AWS_REGION

            # Check if current region is allowed
            allowed_regions = self.REGION_MAPPING.get(required_region, [])

            if current_region not in allowed_regions:
                # Log violation
                logger.warning(
                    f"Data residency violation: User {user.id} "
                    f"requires {required_region} but request served from {current_region}"
                )

                # Redirect to correct region
                correct_endpoint = self.get_regional_endpoint(required_region)
                return HttpResponseRedirect(correct_endpoint + request.path)

        return self.get_response(request)

    def get_regional_endpoint(self, region: str) -> str:
        endpoints = {
            'EU': 'https://eu.api.example.com',
            'US': 'https://us.api.example.com',
            'APAC': 'https://apac.api.example.com',
        }
        return endpoints.get(region, endpoints['US'])
```

#### 3. Global Database Read/Write Routing

```python
# Database router for global deployment
class GlobalDatabaseRouter:
    """Route reads to nearest replica, writes to primary."""

    def __init__(self):
        self.write_db = 'primary'
        self.read_replicas = {
            'us-east': 'replica_us',
            'eu-west': 'replica_eu',
            'ap-south': 'replica_apac',
        }

    def db_for_read(self, model, **hints):
        # Get current region from thread local
        current_region = get_current_region()

        # Route to nearest replica
        return self.read_replicas.get(current_region, 'primary')

    def db_for_write(self, model, **hints):
        # Always write to primary
        return self.write_db

    def allow_relation(self, obj1, obj2, **hints):
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        return db == self.write_db


# Usage with read-after-write consistency
class UserService:
    def update_user(self, user_id: int, data: dict) -> User:
        # Write to primary
        with transaction.atomic(using='primary'):
            user = User.objects.using('primary').get(id=user_id)
            for key, value in data.items():
                setattr(user, key, value)
            user.save()

        # Read back from primary for consistency
        # (replica might have replication lag)
        return User.objects.using('primary').get(id=user_id)

    def get_user(self, user_id: int, require_fresh: bool = False) -> User:
        if require_fresh:
            return User.objects.using('primary').get(id=user_id)

        # Normal read from replica
        return User.objects.get(id=user_id)
```

### Results
- Global availability: 99.97%
- Regional availability: 99.95%+ for all regions
- Data residency: 100% compliance verified by audit
- Regional failover time: < 30 seconds

---

## Summary: Pattern Usage by Industry

| Pattern | E-Commerce | Financial | Real-Time Data | Multi-Region SaaS |
|---------|------------|-----------|----------------|-------------------|
| Circuit Breaker | Yes | Yes | Limited | Yes |
| Retry with Backoff | Yes | Yes | Yes | Yes |
| Bulkhead | Yes | Yes | Yes | Yes |
| Graceful Degradation | Yes | Limited | Yes | Yes |
| Idempotency | Yes | Critical | Yes | Yes |
| Multi-Region | Optional | Required | Optional | Required |
| Exactly-Once | For payments | Critical | Yes | For writes |
| DLQ | Yes | Yes | Yes | Yes |

## Key Takeaways

1. **Start with SLOs**: Define targets before implementing patterns
2. **Layer defenses**: Combine multiple patterns for defense in depth
3. **Test failures**: Chaos engineering validates your reliability
4. **Monitor everything**: You can't improve what you don't measure
5. **Document runbooks**: Faster MTTR through prepared responses
