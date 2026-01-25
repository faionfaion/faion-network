# Distributed System Patterns

Patterns for resilience in distributed systems.

## Core Challenges

| Challenge | Pattern |
|-----------|---------|
| Service failure | Circuit Breaker |
| Network issues | Retry, Timeout |
| Cascading failure | Bulkhead |
| Data consistency | Saga |
| Service discovery | Service Registry |

## Circuit Breaker

Prevent cascading failures by failing fast.

```
States:
┌────────┐   failures   ┌────────┐   timeout   ┌───────────┐
│ Closed │────────────▶│  Open  │────────────▶│ Half-Open │
└────────┘              └────────┘              └───────────┘
    ▲                       │                        │
    │                       │ immediate fail         │
    │                       ▼                        │
    └───────────success────────────────────────────┘
```

```python
import time

class CircuitBreaker:
    def __init__(self, failure_threshold=5, reset_timeout=60):
        self.failure_threshold = failure_threshold
        self.reset_timeout = reset_timeout
        self.failures = 0
        self.state = "closed"
        self.last_failure_time = None

    def call(self, func, *args, **kwargs):
        if self.state == "open":
            if time.time() - self.last_failure_time > self.reset_timeout:
                self.state = "half-open"
            else:
                raise Exception("Circuit is open")

        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise e

    def _on_success(self):
        self.failures = 0
        self.state = "closed"

    def _on_failure(self):
        self.failures += 1
        self.last_failure_time = time.time()
        if self.failures >= self.failure_threshold:
            self.state = "open"
```

## Retry with Exponential Backoff

```python
import time
import random

def retry_with_backoff(func, max_retries=3, base_delay=1):
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            if attempt == max_retries - 1:
                raise e
            delay = base_delay * (2 ** attempt)
            jitter = random.uniform(0, delay * 0.1)
            time.sleep(delay + jitter)
```

**Backoff strategies:**
- **Fixed:** Same delay each time
- **Exponential:** 1s, 2s, 4s, 8s...
- **With jitter:** Random variance to prevent thundering herd

## Bulkhead

Isolate failures to prevent cascade.

```
┌─────────────────────────────────────┐
│           Application               │
│  ┌──────────┐     ┌──────────┐     │
│  │ Pool A   │     │ Pool B   │     │
│  │ (Service │     │ (Service │     │
│  │    A)    │     │    B)    │     │
│  └──────────┘     └──────────┘     │
│       │                │           │
└───────│────────────────│───────────┘
        ▼                ▼
   Service A        Service B
   (if fails,       (still works)
    Pool A exhausted)
```

**Implementation:**
- Separate thread pools per dependency
- Separate connection pools
- Kubernetes: Resource limits per pod

## Saga Pattern

Distributed transaction as sequence of local transactions.

### Choreography (Event-based)
```
Order Service          Payment Service         Inventory Service
      │                      │                       │
      │──OrderCreated───────▶│                       │
      │                      │──PaymentCharged──────▶│
      │                      │                       │
      │◀─────────────────────│◀──InventoryReserved──│
      │                      │                       │
   Complete             (compensate if failed)
```

### Orchestration (Central coordinator)
```
              Saga Orchestrator
                     │
    ┌────────────────┼────────────────┐
    │                │                │
    ▼                ▼                ▼
Order Service   Payment Service   Inventory Service
```

**Compensation:** Each step has a compensating action to undo.

## Timeout

Always set timeouts for external calls.

```python
import requests

# Connection timeout: max time to establish connection
# Read timeout: max time to wait for response
response = requests.get(url, timeout=(3.05, 27))

# Async with timeout
import asyncio

async def call_with_timeout():
    try:
        result = await asyncio.wait_for(
            external_call(),
            timeout=5.0
        )
    except asyncio.TimeoutError:
        # Handle timeout
        pass
```

## Rate Limiting

Protect services from overload.

**Algorithms:**
| Algorithm | Description |
|-----------|-------------|
| Token Bucket | Tokens replenish over time |
| Leaky Bucket | Fixed rate output |
| Sliding Window | Count in rolling window |

```python
import time

class TokenBucket:
    def __init__(self, capacity, refill_rate):
        self.capacity = capacity
        self.tokens = capacity
        self.refill_rate = refill_rate
        self.last_refill = time.time()

    def allow_request(self):
        self._refill()
        if self.tokens >= 1:
            self.tokens -= 1
            return True
        return False

    def _refill(self):
        now = time.time()
        elapsed = now - self.last_refill
        self.tokens = min(
            self.capacity,
            self.tokens + elapsed * self.refill_rate
        )
        self.last_refill = now
```

## Service Discovery

Dynamic service location.

```
┌─────────────────────────────────────┐
│         Service Registry            │
│     (Consul, etcd, K8s DNS)         │
└───────────────┬─────────────────────┘
                │
    ┌───────────┼───────────┐
    │           │           │
    ▼           ▼           ▼
Service A   Service B   Service C
(registers) (registers) (registers)
```

**Client-side:** Client queries registry, picks instance
**Server-side:** Load balancer queries registry, routes

## Health Checks

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.get("/ready")
async def ready():
    # Check dependencies
    db_ok = await check_database()
    cache_ok = await check_cache()

    if db_ok and cache_ok:
        return {"status": "ready"}
    return {"status": "not ready"}, 503
```

- **Liveness:** Is the process alive?
- **Readiness:** Can it serve traffic?

## Related

- [microservices-architecture.md](microservices-architecture.md) - Service design
- [event-driven-architecture.md](event-driven-architecture.md) - Async patterns
- [reliability-architecture.md](reliability-architecture.md) - Reliability deep dive
