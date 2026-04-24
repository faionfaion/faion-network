# Reliability Architecture Templates

Copy-paste configurations and code templates for implementing reliability patterns.

---

## Table of Contents

1. [Circuit Breaker](#circuit-breaker)
2. [Retry with Exponential Backoff](#retry-with-exponential-backoff)
3. [Timeout Configuration](#timeout-configuration)
4. [Health Checks (Kubernetes)](#health-checks-kubernetes)
5. [Rate Limiting](#rate-limiting)
6. [Graceful Shutdown](#graceful-shutdown)
7. [SLO Configuration](#slo-configuration)
8. [Chaos Engineering](#chaos-engineering)
9. [Disaster Recovery](#disaster-recovery)

---

## Circuit Breaker

### Python (tenacity + custom)

```python
# circuit_breaker.py
import time
import threading
from enum import Enum
from typing import Callable, TypeVar, Generic
from dataclasses import dataclass
from functools import wraps

T = TypeVar('T')

class CircuitState(Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"

@dataclass
class CircuitBreakerConfig:
    failure_threshold: int = 5
    success_threshold: int = 3
    timeout_seconds: float = 30.0
    failure_window_seconds: float = 60.0

class CircuitBreaker:
    def __init__(self, config: CircuitBreakerConfig = None):
        self.config = config or CircuitBreakerConfig()
        self.state = CircuitState.CLOSED
        self.failures = []
        self.successes = 0
        self.last_failure_time = 0
        self._lock = threading.Lock()

    def _is_failure_window_expired(self) -> bool:
        if not self.failures:
            return True
        oldest = self.failures[0]
        return time.time() - oldest > self.config.failure_window_seconds

    def _record_failure(self):
        now = time.time()
        with self._lock:
            self.failures.append(now)
            # Remove old failures outside window
            cutoff = now - self.config.failure_window_seconds
            self.failures = [f for f in self.failures if f > cutoff]

            if len(self.failures) >= self.config.failure_threshold:
                self.state = CircuitState.OPEN
                self.last_failure_time = now

    def _record_success(self):
        with self._lock:
            if self.state == CircuitState.HALF_OPEN:
                self.successes += 1
                if self.successes >= self.config.success_threshold:
                    self.state = CircuitState.CLOSED
                    self.failures = []
                    self.successes = 0

    def _should_allow_request(self) -> bool:
        with self._lock:
            if self.state == CircuitState.CLOSED:
                return True

            if self.state == CircuitState.OPEN:
                if time.time() - self.last_failure_time > self.config.timeout_seconds:
                    self.state = CircuitState.HALF_OPEN
                    self.successes = 0
                    return True
                return False

            # HALF_OPEN - allow limited requests
            return True

    def call(self, func: Callable[[], T]) -> T:
        if not self._should_allow_request():
            raise CircuitBreakerOpenError(f"Circuit is OPEN")

        try:
            result = func()
            self._record_success()
            return result
        except Exception as e:
            self._record_failure()
            raise

class CircuitBreakerOpenError(Exception):
    pass

# Decorator usage
def circuit_breaker(config: CircuitBreakerConfig = None):
    cb = CircuitBreaker(config)

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return cb.call(lambda: func(*args, **kwargs))
        wrapper.circuit_breaker = cb
        return wrapper
    return decorator

# Example usage
@circuit_breaker(CircuitBreakerConfig(
    failure_threshold=5,
    success_threshold=3,
    timeout_seconds=30
))
def call_payment_service(payment_data: dict):
    response = requests.post(
        "https://payment.example.com/charge",
        json=payment_data,
        timeout=5.0
    )
    response.raise_for_status()
    return response.json()
```

### Go (gobreaker)

```go
// circuit_breaker.go
package reliability

import (
    "context"
    "errors"
    "time"

    "github.com/sony/gobreaker"
)

// CircuitBreakerConfig holds configuration for circuit breakers
type CircuitBreakerConfig struct {
    Name               string
    MaxRequests        uint32        // Max requests in half-open state
    Interval           time.Duration // Cyclic period for clearing counts
    Timeout            time.Duration // Period of open state
    FailureThreshold   uint32        // Failures to trip
    SuccessThreshold   uint32        // Successes to close
}

// DefaultCircuitBreakerConfig returns sensible defaults
func DefaultCircuitBreakerConfig(name string) CircuitBreakerConfig {
    return CircuitBreakerConfig{
        Name:             name,
        MaxRequests:      3,
        Interval:         60 * time.Second,
        Timeout:          30 * time.Second,
        FailureThreshold: 5,
        SuccessThreshold: 3,
    }
}

// NewCircuitBreaker creates a configured circuit breaker
func NewCircuitBreaker(cfg CircuitBreakerConfig) *gobreaker.CircuitBreaker {
    settings := gobreaker.Settings{
        Name:        cfg.Name,
        MaxRequests: cfg.MaxRequests,
        Interval:    cfg.Interval,
        Timeout:     cfg.Timeout,

        ReadyToTrip: func(counts gobreaker.Counts) bool {
            return counts.ConsecutiveFailures >= cfg.FailureThreshold
        },

        OnStateChange: func(name string, from, to gobreaker.State) {
            log.Printf("Circuit breaker %s: %s -> %s", name, from, to)
        },
    }

    return gobreaker.NewCircuitBreaker(settings)
}

// ServiceClient wraps HTTP client with circuit breaker
type ServiceClient struct {
    httpClient *http.Client
    cb         *gobreaker.CircuitBreaker
    baseURL    string
}

func NewServiceClient(baseURL string, cbConfig CircuitBreakerConfig) *ServiceClient {
    return &ServiceClient{
        httpClient: &http.Client{Timeout: 10 * time.Second},
        cb:         NewCircuitBreaker(cbConfig),
        baseURL:    baseURL,
    }
}

func (c *ServiceClient) Call(ctx context.Context, path string, body []byte) ([]byte, error) {
    result, err := c.cb.Execute(func() (interface{}, error) {
        req, err := http.NewRequestWithContext(ctx, "POST", c.baseURL+path, bytes.NewReader(body))
        if err != nil {
            return nil, err
        }

        resp, err := c.httpClient.Do(req)
        if err != nil {
            return nil, err
        }
        defer resp.Body.Close()

        if resp.StatusCode >= 500 {
            return nil, errors.New("server error")
        }

        return io.ReadAll(resp.Body)
    })

    if err != nil {
        return nil, err
    }
    return result.([]byte), nil
}
```

### Java (Resilience4j)

```java
// CircuitBreakerService.java
import io.github.resilience4j.circuitbreaker.CircuitBreaker;
import io.github.resilience4j.circuitbreaker.CircuitBreakerConfig;
import io.github.resilience4j.circuitbreaker.CircuitBreakerRegistry;

import java.time.Duration;
import java.util.function.Supplier;

public class CircuitBreakerService {

    private final CircuitBreakerRegistry registry;

    public CircuitBreakerService() {
        CircuitBreakerConfig config = CircuitBreakerConfig.custom()
            .failureRateThreshold(50)                     // 50% failure rate trips
            .slowCallRateThreshold(50)                    // 50% slow calls trips
            .slowCallDurationThreshold(Duration.ofSeconds(2))
            .waitDurationInOpenState(Duration.ofSeconds(30))
            .permittedNumberOfCallsInHalfOpenState(5)
            .minimumNumberOfCalls(10)
            .slidingWindowType(CircuitBreakerConfig.SlidingWindowType.COUNT_BASED)
            .slidingWindowSize(20)
            .build();

        this.registry = CircuitBreakerRegistry.of(config);
    }

    public <T> T executeWithCircuitBreaker(
            String name,
            Supplier<T> supplier,
            Supplier<T> fallback) {

        CircuitBreaker cb = registry.circuitBreaker(name);

        return CircuitBreaker.decorateSupplier(cb, supplier)
            .recover(throwable -> fallback.get())
            .get();
    }
}

// Usage
public class PaymentService {
    private final CircuitBreakerService cbService;
    private final PaymentClient paymentClient;

    public PaymentResult processPayment(PaymentRequest request) {
        return cbService.executeWithCircuitBreaker(
            "payment-service",
            () -> paymentClient.charge(request),
            () -> PaymentResult.pending("Circuit breaker open, queued for retry")
        );
    }
}
```

---

## Retry with Exponential Backoff

### Python (tenacity)

```python
# retry_config.py
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential_jitter,
    retry_if_exception_type,
    before_sleep_log,
    after_log,
)
import logging

logger = logging.getLogger(__name__)

# Standard retry configuration
def create_retry_decorator(
    max_attempts: int = 4,
    initial_wait: float = 1.0,
    max_wait: float = 30.0,
    jitter: float = 5.0,
    retryable_exceptions: tuple = (TimeoutError, ConnectionError),
):
    return retry(
        stop=stop_after_attempt(max_attempts),
        wait=wait_exponential_jitter(
            initial=initial_wait,
            max=max_wait,
            jitter=jitter,
        ),
        retry=retry_if_exception_type(retryable_exceptions),
        before_sleep=before_sleep_log(logger, logging.WARNING),
        after=after_log(logger, logging.DEBUG),
    )

# Pre-configured decorators
retry_api_call = create_retry_decorator(
    max_attempts=4,
    initial_wait=1.0,
    max_wait=30.0,
    retryable_exceptions=(TimeoutError, ConnectionError, requests.exceptions.RequestException),
)

retry_database = create_retry_decorator(
    max_attempts=3,
    initial_wait=0.5,
    max_wait=10.0,
    retryable_exceptions=(OperationalError, InterfaceError),
)

# Usage
@retry_api_call
def fetch_user_data(user_id: str) -> dict:
    response = requests.get(
        f"https://api.example.com/users/{user_id}",
        timeout=5.0
    )
    response.raise_for_status()
    return response.json()

# Custom retry with callback
from tenacity import Retrying, RetryError

def fetch_with_callback(url: str, on_retry=None):
    for attempt in Retrying(
        stop=stop_after_attempt(4),
        wait=wait_exponential_jitter(initial=1, max=30),
        retry=retry_if_exception_type((TimeoutError, ConnectionError)),
    ):
        with attempt:
            if on_retry and attempt.retry_state.attempt_number > 1:
                on_retry(attempt.retry_state.attempt_number)
            return requests.get(url, timeout=5.0).json()
```

### Go (native)

```go
// retry.go
package reliability

import (
    "context"
    "math"
    "math/rand"
    "time"
)

// RetryConfig configures retry behavior
type RetryConfig struct {
    MaxAttempts     int
    InitialDelay    time.Duration
    MaxDelay        time.Duration
    Multiplier      float64
    JitterFactor    float64
    RetryableErrors []error
}

// DefaultRetryConfig returns sensible defaults
func DefaultRetryConfig() RetryConfig {
    return RetryConfig{
        MaxAttempts:  4,
        InitialDelay: 1 * time.Second,
        MaxDelay:     30 * time.Second,
        Multiplier:   2.0,
        JitterFactor: 0.1,
    }
}

// RetryWithBackoff executes fn with exponential backoff
func RetryWithBackoff[T any](
    ctx context.Context,
    cfg RetryConfig,
    fn func() (T, error),
) (T, error) {
    var result T
    var lastErr error

    for attempt := 0; attempt < cfg.MaxAttempts; attempt++ {
        select {
        case <-ctx.Done():
            return result, ctx.Err()
        default:
        }

        result, lastErr = fn()
        if lastErr == nil {
            return result, nil
        }

        if !isRetryable(lastErr, cfg.RetryableErrors) {
            return result, lastErr
        }

        if attempt < cfg.MaxAttempts-1 {
            delay := calculateDelay(attempt, cfg)
            time.Sleep(delay)
        }
    }

    return result, lastErr
}

func calculateDelay(attempt int, cfg RetryConfig) time.Duration {
    // Exponential backoff: initial * multiplier^attempt
    delay := float64(cfg.InitialDelay) * math.Pow(cfg.Multiplier, float64(attempt))

    // Cap at max delay
    if delay > float64(cfg.MaxDelay) {
        delay = float64(cfg.MaxDelay)
    }

    // Add jitter
    jitter := delay * cfg.JitterFactor * (rand.Float64()*2 - 1) // -jitter to +jitter
    delay += jitter

    return time.Duration(delay)
}

func isRetryable(err error, retryableErrors []error) bool {
    if len(retryableErrors) == 0 {
        return true // Retry all errors if none specified
    }
    for _, re := range retryableErrors {
        if errors.Is(err, re) {
            return true
        }
    }
    return false
}

// Usage
func FetchUserWithRetry(ctx context.Context, userID string) (*User, error) {
    cfg := DefaultRetryConfig()
    cfg.MaxAttempts = 3

    return RetryWithBackoff(ctx, cfg, func() (*User, error) {
        return userClient.GetUser(ctx, userID)
    })
}
```

### TypeScript (native)

```typescript
// retry.ts
interface RetryConfig {
  maxAttempts: number;
  initialDelayMs: number;
  maxDelayMs: number;
  multiplier: number;
  jitterFactor: number;
  retryableErrors?: (new (...args: any[]) => Error)[];
}

const defaultConfig: RetryConfig = {
  maxAttempts: 4,
  initialDelayMs: 1000,
  maxDelayMs: 30000,
  multiplier: 2,
  jitterFactor: 0.1,
};

function sleep(ms: number): Promise<void> {
  return new Promise(resolve => setTimeout(resolve, ms));
}

function calculateDelay(attempt: number, config: RetryConfig): number {
  let delay = config.initialDelayMs * Math.pow(config.multiplier, attempt);
  delay = Math.min(delay, config.maxDelayMs);

  // Add jitter
  const jitter = delay * config.jitterFactor * (Math.random() * 2 - 1);
  return delay + jitter;
}

function isRetryable(error: Error, config: RetryConfig): boolean {
  if (!config.retryableErrors || config.retryableErrors.length === 0) {
    return true;
  }
  return config.retryableErrors.some(ErrorClass => error instanceof ErrorClass);
}

export async function retryWithBackoff<T>(
  fn: () => Promise<T>,
  config: Partial<RetryConfig> = {}
): Promise<T> {
  const cfg = { ...defaultConfig, ...config };
  let lastError: Error;

  for (let attempt = 0; attempt < cfg.maxAttempts; attempt++) {
    try {
      return await fn();
    } catch (error) {
      lastError = error as Error;

      if (!isRetryable(lastError, cfg)) {
        throw lastError;
      }

      if (attempt < cfg.maxAttempts - 1) {
        const delay = calculateDelay(attempt, cfg);
        console.log(`Retry attempt ${attempt + 1}, waiting ${delay}ms`);
        await sleep(delay);
      }
    }
  }

  throw lastError!;
}

// Usage
const user = await retryWithBackoff(
  () => fetchUser(userId),
  {
    maxAttempts: 3,
    initialDelayMs: 500,
  }
);
```

---

## Timeout Configuration

### Python (httpx/aiohttp)

```python
# timeout_config.py
import httpx
from dataclasses import dataclass
from typing import Optional

@dataclass
class TimeoutConfig:
    connect: float = 5.0      # Connection establishment
    read: float = 30.0        # Response read
    write: float = 30.0       # Request write
    pool: float = 10.0        # Connection pool wait

    def to_httpx(self) -> httpx.Timeout:
        return httpx.Timeout(
            connect=self.connect,
            read=self.read,
            write=self.write,
            pool=self.pool,
        )

# Service-specific timeout configurations
TIMEOUT_CONFIGS = {
    "default": TimeoutConfig(),
    "fast_api": TimeoutConfig(connect=3.0, read=10.0, write=10.0, pool=5.0),
    "file_upload": TimeoutConfig(connect=5.0, read=300.0, write=300.0, pool=30.0),
    "database": TimeoutConfig(connect=3.0, read=30.0, write=30.0, pool=5.0),
    "external_api": TimeoutConfig(connect=5.0, read=60.0, write=30.0, pool=10.0),
}

class TimeoutAwareClient:
    def __init__(self, base_url: str, timeout_profile: str = "default"):
        self.timeout = TIMEOUT_CONFIGS.get(timeout_profile, TIMEOUT_CONFIGS["default"])
        self.client = httpx.AsyncClient(
            base_url=base_url,
            timeout=self.timeout.to_httpx(),
        )

    async def get(self, path: str, **kwargs) -> httpx.Response:
        return await self.client.get(path, **kwargs)

    async def post(self, path: str, **kwargs) -> httpx.Response:
        return await self.client.post(path, **kwargs)

# Context manager for temporary timeout override
from contextlib import asynccontextmanager

@asynccontextmanager
async def override_timeout(client: httpx.AsyncClient, timeout: TimeoutConfig):
    original = client.timeout
    try:
        client.timeout = timeout.to_httpx()
        yield
    finally:
        client.timeout = original

# Usage
async def upload_large_file(client: TimeoutAwareClient, file_path: str):
    async with override_timeout(client.client, TIMEOUT_CONFIGS["file_upload"]):
        with open(file_path, "rb") as f:
            return await client.post("/upload", files={"file": f})
```

### Go (context with deadline)

```go
// timeout.go
package reliability

import (
    "context"
    "net/http"
    "time"
)

// TimeoutConfig holds timeout values
type TimeoutConfig struct {
    Connect     time.Duration
    Request     time.Duration
    IdleConn    time.Duration
    KeepAlive   time.Duration
    TLSHandshake time.Duration
}

// DefaultTimeoutConfig returns sensible defaults
func DefaultTimeoutConfig() TimeoutConfig {
    return TimeoutConfig{
        Connect:      5 * time.Second,
        Request:      30 * time.Second,
        IdleConn:     90 * time.Second,
        KeepAlive:    30 * time.Second,
        TLSHandshake: 10 * time.Second,
    }
}

// NewHTTPClient creates a configured HTTP client
func NewHTTPClient(cfg TimeoutConfig) *http.Client {
    transport := &http.Transport{
        DialContext: (&net.Dialer{
            Timeout:   cfg.Connect,
            KeepAlive: cfg.KeepAlive,
        }).DialContext,
        TLSHandshakeTimeout: cfg.TLSHandshake,
        IdleConnTimeout:     cfg.IdleConn,
        MaxIdleConns:        100,
        MaxConnsPerHost:     100,
        MaxIdleConnsPerHost: 100,
    }

    return &http.Client{
        Transport: transport,
        Timeout:   cfg.Request,
    }
}

// WithTimeout creates a context with timeout for a specific operation
func WithTimeout(parent context.Context, timeout time.Duration) (context.Context, context.CancelFunc) {
    return context.WithTimeout(parent, timeout)
}

// TimeoutBudget manages timeout budget across call chain
type TimeoutBudget struct {
    deadline time.Time
}

func NewTimeoutBudget(ctx context.Context, total time.Duration) (*TimeoutBudget, context.Context, context.CancelFunc) {
    deadline := time.Now().Add(total)
    ctx, cancel := context.WithDeadline(ctx, deadline)
    return &TimeoutBudget{deadline: deadline}, ctx, cancel
}

func (tb *TimeoutBudget) Remaining() time.Duration {
    return time.Until(tb.deadline)
}

func (tb *TimeoutBudget) Allocate(portion float64) time.Duration {
    remaining := tb.Remaining()
    if remaining <= 0 {
        return 0
    }
    return time.Duration(float64(remaining) * portion)
}

// Usage
func ProcessOrder(ctx context.Context, order Order) error {
    // Total budget: 10 seconds
    budget, ctx, cancel := NewTimeoutBudget(ctx, 10*time.Second)
    defer cancel()

    // Validate: 20% of budget
    validateCtx, validateCancel := context.WithTimeout(ctx, budget.Allocate(0.2))
    defer validateCancel()
    if err := validateOrder(validateCtx, order); err != nil {
        return err
    }

    // Reserve inventory: 30% of budget
    inventoryCtx, inventoryCancel := context.WithTimeout(ctx, budget.Allocate(0.3))
    defer inventoryCancel()
    if err := reserveInventory(inventoryCtx, order); err != nil {
        return err
    }

    // Process payment: 50% of budget
    paymentCtx, paymentCancel := context.WithTimeout(ctx, budget.Allocate(0.5))
    defer paymentCancel()
    return processPayment(paymentCtx, order)
}
```

---

## Health Checks (Kubernetes)

### Kubernetes Deployment YAML

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-server
  labels:
    app: api-server
spec:
  replicas: 3
  selector:
    matchLabels:
      app: api-server
  template:
    metadata:
      labels:
        app: api-server
    spec:
      containers:
      - name: api
        image: api-server:v1.2.3
        ports:
        - containerPort: 8080
          name: http

        # Startup probe - for slow-starting apps
        startupProbe:
          httpGet:
            path: /health/startup
            port: http
          initialDelaySeconds: 5
          periodSeconds: 5
          failureThreshold: 30  # 30 * 5 = 150s max startup time
          timeoutSeconds: 3

        # Liveness probe - is the process alive?
        livenessProbe:
          httpGet:
            path: /health/live
            port: http
          initialDelaySeconds: 0  # Start immediately after startup succeeds
          periodSeconds: 15
          failureThreshold: 3
          timeoutSeconds: 3
          successThreshold: 1

        # Readiness probe - can it serve traffic?
        readinessProbe:
          httpGet:
            path: /health/ready
            port: http
          initialDelaySeconds: 0
          periodSeconds: 5
          failureThreshold: 3
          timeoutSeconds: 3
          successThreshold: 2  # Require 2 consecutive successes

        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "1000m"

        env:
        - name: DB_HOST
          valueFrom:
            secretKeyRef:
              name: db-credentials
              key: host
```

### Python Health Endpoint (FastAPI)

```python
# health.py
from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel
from typing import Optional, Dict
import asyncio
import time

app = FastAPI()

class HealthCheck(BaseModel):
    status: str
    latency_ms: Optional[float] = None
    error: Optional[str] = None

class HealthResponse(BaseModel):
    status: str
    checks: Dict[str, HealthCheck]
    version: str
    uptime_seconds: float

START_TIME = time.time()
VERSION = "1.2.3"

async def check_database() -> HealthCheck:
    start = time.time()
    try:
        await db.execute("SELECT 1")
        return HealthCheck(
            status="healthy",
            latency_ms=(time.time() - start) * 1000
        )
    except Exception as e:
        return HealthCheck(status="unhealthy", error=str(e))

async def check_redis() -> HealthCheck:
    start = time.time()
    try:
        await redis.ping()
        return HealthCheck(
            status="healthy",
            latency_ms=(time.time() - start) * 1000
        )
    except Exception as e:
        return HealthCheck(status="unhealthy", error=str(e))

async def check_external_api() -> HealthCheck:
    start = time.time()
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://api.example.com/health",
                timeout=3.0
            )
            if response.status_code == 200:
                return HealthCheck(
                    status="healthy",
                    latency_ms=(time.time() - start) * 1000
                )
            return HealthCheck(status="degraded", error=f"Status {response.status_code}")
    except Exception as e:
        return HealthCheck(status="degraded", error=str(e))

@app.get("/health/live")
async def liveness():
    """Liveness probe - is the process running?"""
    return {"status": "ok"}

@app.get("/health/startup")
async def startup():
    """Startup probe - has the application initialized?"""
    # Check that essential components are ready
    if not db.is_connected():
        raise HTTPException(status_code=503, detail="Database not connected")
    return {"status": "ok"}

@app.get("/health/ready", response_model=HealthResponse)
async def readiness(response: Response):
    """Readiness probe - can it serve traffic?"""
    # Run all checks concurrently
    db_check, redis_check, api_check = await asyncio.gather(
        check_database(),
        check_redis(),
        check_external_api(),
    )

    checks = {
        "database": db_check,
        "redis": redis_check,
        "external_api": api_check,
    }

    # Critical dependencies must be healthy
    critical_healthy = all(
        checks[name].status == "healthy"
        for name in ["database", "redis"]
    )

    overall_status = "ready" if critical_healthy else "not_ready"

    if not critical_healthy:
        response.status_code = 503

    return HealthResponse(
        status=overall_status,
        checks=checks,
        version=VERSION,
        uptime_seconds=time.time() - START_TIME,
    )
```

### Go Health Endpoint

```go
// health.go
package health

import (
    "context"
    "encoding/json"
    "net/http"
    "sync"
    "time"
)

type HealthCheck struct {
    Status    string  `json:"status"`
    LatencyMs float64 `json:"latency_ms,omitempty"`
    Error     string  `json:"error,omitempty"`
}

type HealthResponse struct {
    Status        string                  `json:"status"`
    Checks        map[string]HealthCheck  `json:"checks"`
    Version       string                  `json:"version"`
    UptimeSeconds float64                 `json:"uptime_seconds"`
}

type HealthService struct {
    db        *sql.DB
    redis     *redis.Client
    startTime time.Time
    version   string
}

func NewHealthService(db *sql.DB, redis *redis.Client, version string) *HealthService {
    return &HealthService{
        db:        db,
        redis:     redis,
        startTime: time.Now(),
        version:   version,
    }
}

func (h *HealthService) LivenessHandler(w http.ResponseWriter, r *http.Request) {
    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(map[string]string{"status": "ok"})
}

func (h *HealthService) ReadinessHandler(w http.ResponseWriter, r *http.Request) {
    ctx, cancel := context.WithTimeout(r.Context(), 5*time.Second)
    defer cancel()

    var wg sync.WaitGroup
    checks := make(map[string]HealthCheck)
    var mu sync.Mutex

    // Check database
    wg.Add(1)
    go func() {
        defer wg.Done()
        check := h.checkDatabase(ctx)
        mu.Lock()
        checks["database"] = check
        mu.Unlock()
    }()

    // Check Redis
    wg.Add(1)
    go func() {
        defer wg.Done()
        check := h.checkRedis(ctx)
        mu.Lock()
        checks["redis"] = check
        mu.Unlock()
    }()

    wg.Wait()

    // Determine overall status
    criticalHealthy := checks["database"].Status == "healthy" &&
                       checks["redis"].Status == "healthy"

    status := "ready"
    httpStatus := http.StatusOK
    if !criticalHealthy {
        status = "not_ready"
        httpStatus = http.StatusServiceUnavailable
    }

    response := HealthResponse{
        Status:        status,
        Checks:        checks,
        Version:       h.version,
        UptimeSeconds: time.Since(h.startTime).Seconds(),
    }

    w.Header().Set("Content-Type", "application/json")
    w.WriteHeader(httpStatus)
    json.NewEncoder(w).Encode(response)
}

func (h *HealthService) checkDatabase(ctx context.Context) HealthCheck {
    start := time.Now()
    err := h.db.PingContext(ctx)
    latency := float64(time.Since(start).Milliseconds())

    if err != nil {
        return HealthCheck{Status: "unhealthy", Error: err.Error(), LatencyMs: latency}
    }
    return HealthCheck{Status: "healthy", LatencyMs: latency}
}

func (h *HealthService) checkRedis(ctx context.Context) HealthCheck {
    start := time.Now()
    err := h.redis.Ping(ctx).Err()
    latency := float64(time.Since(start).Milliseconds())

    if err != nil {
        return HealthCheck{Status: "unhealthy", Error: err.Error(), LatencyMs: latency}
    }
    return HealthCheck{Status: "healthy", LatencyMs: latency}
}
```

---

## Rate Limiting

### Python (Redis-based)

```python
# rate_limiter.py
import redis
import time
from typing import Tuple

class RateLimiter:
    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client

    def is_allowed(
        self,
        key: str,
        limit: int,
        window_seconds: int
    ) -> Tuple[bool, int, int]:
        """
        Sliding window rate limiter.
        Returns: (allowed, remaining, reset_seconds)
        """
        now = time.time()
        window_start = now - window_seconds

        pipe = self.redis.pipeline()

        # Remove old entries
        pipe.zremrangebyscore(key, 0, window_start)

        # Count current entries
        pipe.zcard(key)

        # Add new entry
        pipe.zadd(key, {str(now): now})

        # Set expiry
        pipe.expire(key, window_seconds)

        results = pipe.execute()
        current_count = results[1]

        if current_count >= limit:
            # Get oldest entry to calculate reset time
            oldest = self.redis.zrange(key, 0, 0, withscores=True)
            if oldest:
                reset_at = int(oldest[0][1] + window_seconds - now)
            else:
                reset_at = window_seconds
            return False, 0, reset_at

        remaining = limit - current_count - 1
        return True, remaining, window_seconds


class TieredRateLimiter:
    """Rate limiter with different tiers."""

    TIERS = {
        "free": {"limit": 100, "window": 3600},      # 100/hour
        "basic": {"limit": 1000, "window": 3600},    # 1000/hour
        "pro": {"limit": 10000, "window": 3600},     # 10000/hour
        "enterprise": {"limit": 100000, "window": 3600},  # 100000/hour
    }

    def __init__(self, redis_client: redis.Redis):
        self.limiter = RateLimiter(redis_client)

    def check(self, user_id: str, tier: str = "free") -> Tuple[bool, dict]:
        config = self.TIERS.get(tier, self.TIERS["free"])
        key = f"ratelimit:{tier}:{user_id}"

        allowed, remaining, reset = self.limiter.is_allowed(
            key,
            config["limit"],
            config["window"]
        )

        headers = {
            "X-RateLimit-Limit": str(config["limit"]),
            "X-RateLimit-Remaining": str(remaining),
            "X-RateLimit-Reset": str(reset),
        }

        return allowed, headers


# FastAPI middleware
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware

class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, limiter: TieredRateLimiter):
        super().__init__(app)
        self.limiter = limiter

    async def dispatch(self, request: Request, call_next):
        # Get user info
        user_id = request.headers.get("X-User-ID", request.client.host)
        tier = request.headers.get("X-Rate-Tier", "free")

        allowed, headers = self.limiter.check(user_id, tier)

        if not allowed:
            raise HTTPException(
                status_code=429,
                detail="Rate limit exceeded",
                headers=headers
            )

        response = await call_next(request)

        # Add rate limit headers
        for key, value in headers.items():
            response.headers[key] = value

        return response
```

---

## Graceful Shutdown

### Python (FastAPI/Uvicorn)

```python
# graceful_shutdown.py
import signal
import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
import logging

logger = logging.getLogger(__name__)

class GracefulShutdown:
    def __init__(self):
        self.shutdown_event = asyncio.Event()
        self.active_requests = 0
        self._lock = asyncio.Lock()

    async def increment(self):
        async with self._lock:
            self.active_requests += 1

    async def decrement(self):
        async with self._lock:
            self.active_requests -= 1

    async def wait_for_shutdown(self, timeout: float = 30.0):
        """Wait for active requests to complete."""
        start = asyncio.get_event_loop().time()

        while True:
            async with self._lock:
                if self.active_requests == 0:
                    break

            if asyncio.get_event_loop().time() - start > timeout:
                logger.warning(f"Shutdown timeout, {self.active_requests} requests still active")
                break

            await asyncio.sleep(0.1)

shutdown_handler = GracefulShutdown()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting up...")
    await db.connect()
    await redis.connect()

    yield

    # Shutdown
    logger.info("Shutting down...")

    # Stop accepting new requests
    shutdown_handler.shutdown_event.set()

    # Wait for active requests to complete
    await shutdown_handler.wait_for_shutdown(timeout=30.0)

    # Close connections
    await db.disconnect()
    await redis.disconnect()

    logger.info("Shutdown complete")

app = FastAPI(lifespan=lifespan)

# Middleware to track active requests
@app.middleware("http")
async def track_requests(request, call_next):
    if shutdown_handler.shutdown_event.is_set():
        return Response(
            content="Service shutting down",
            status_code=503,
            headers={"Connection": "close"}
        )

    await shutdown_handler.increment()
    try:
        return await call_next(request)
    finally:
        await shutdown_handler.decrement()
```

### Go (graceful shutdown)

```go
// graceful_shutdown.go
package main

import (
    "context"
    "log"
    "net/http"
    "os"
    "os/signal"
    "sync/atomic"
    "syscall"
    "time"
)

type Server struct {
    httpServer     *http.Server
    activeRequests int64
    shuttingDown   int32
}

func NewServer(addr string, handler http.Handler) *Server {
    s := &Server{}

    // Wrap handler to track requests
    trackedHandler := http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        if atomic.LoadInt32(&s.shuttingDown) == 1 {
            w.Header().Set("Connection", "close")
            http.Error(w, "Service shutting down", http.StatusServiceUnavailable)
            return
        }

        atomic.AddInt64(&s.activeRequests, 1)
        defer atomic.AddInt64(&s.activeRequests, -1)

        handler.ServeHTTP(w, r)
    })

    s.httpServer = &http.Server{
        Addr:         addr,
        Handler:      trackedHandler,
        ReadTimeout:  15 * time.Second,
        WriteTimeout: 15 * time.Second,
        IdleTimeout:  60 * time.Second,
    }

    return s
}

func (s *Server) Run() error {
    // Start server in goroutine
    go func() {
        log.Printf("Server starting on %s", s.httpServer.Addr)
        if err := s.httpServer.ListenAndServe(); err != http.ErrServerClosed {
            log.Fatalf("Server error: %v", err)
        }
    }()

    // Wait for shutdown signal
    quit := make(chan os.Signal, 1)
    signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)
    <-quit

    log.Println("Shutdown signal received")
    return s.Shutdown(30 * time.Second)
}

func (s *Server) Shutdown(timeout time.Duration) error {
    // Mark as shutting down
    atomic.StoreInt32(&s.shuttingDown, 1)

    // Wait for active requests with timeout
    ctx, cancel := context.WithTimeout(context.Background(), timeout)
    defer cancel()

    // Gracefully shutdown HTTP server
    if err := s.httpServer.Shutdown(ctx); err != nil {
        log.Printf("HTTP server shutdown error: %v", err)
    }

    // Wait for in-flight requests
    deadline := time.Now().Add(timeout)
    for time.Now().Before(deadline) {
        if atomic.LoadInt64(&s.activeRequests) == 0 {
            break
        }
        time.Sleep(100 * time.Millisecond)
    }

    active := atomic.LoadInt64(&s.activeRequests)
    if active > 0 {
        log.Printf("Warning: %d requests still active after shutdown", active)
    }

    log.Println("Shutdown complete")
    return nil
}

func main() {
    mux := http.NewServeMux()
    mux.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
        time.Sleep(5 * time.Second) // Simulate work
        w.Write([]byte("OK"))
    })

    server := NewServer(":8080", mux)
    if err := server.Run(); err != nil {
        log.Fatal(err)
    }
}
```

---

## SLO Configuration

### Prometheus SLO Rules

```yaml
# slo_rules.yaml
groups:
- name: slo-api-availability
  interval: 30s
  rules:
  # SLI: Request success rate
  - record: sli:api_requests:availability
    expr: |
      sum(rate(http_requests_total{status!~"5.."}[5m]))
      /
      sum(rate(http_requests_total[5m]))

  # SLO: 99.9% availability (30-day window)
  - record: slo:api_availability:target
    expr: 0.999

  # Error budget remaining
  - record: slo:api_availability:error_budget_remaining
    expr: |
      1 - (
        (1 - sli:api_requests:availability)
        /
        (1 - slo:api_availability:target)
      )

  # Alert: Error budget burn rate too high
  - alert: SLOBudgetBurnHigh
    expr: |
      (
        (1 - sli:api_requests:availability)
        /
        (1 - slo:api_availability:target)
      ) > 0.02
    for: 5m
    labels:
      severity: warning
    annotations:
      summary: "API availability error budget burning too fast"
      description: "Current burn rate will exhaust error budget before end of window"

- name: slo-api-latency
  interval: 30s
  rules:
  # SLI: P99 latency
  - record: sli:api_requests:latency_p99
    expr: |
      histogram_quantile(0.99,
        sum(rate(http_request_duration_seconds_bucket[5m])) by (le)
      )

  # SLO: P99 latency < 500ms
  - record: slo:api_latency_p99:target_seconds
    expr: 0.5

  # Alert: Latency SLO breach
  - alert: SLOLatencyBreach
    expr: sli:api_requests:latency_p99 > slo:api_latency_p99:target_seconds
    for: 5m
    labels:
      severity: warning
    annotations:
      summary: "API P99 latency exceeds SLO target"
      description: "P99 latency {{ $value }}s exceeds 500ms target"
```

### Grafana SLO Dashboard (JSON)

```json
{
  "title": "SLO Dashboard",
  "panels": [
    {
      "title": "Availability SLI (30d)",
      "type": "gauge",
      "targets": [
        {
          "expr": "sli:api_requests:availability * 100",
          "legendFormat": "Availability %"
        }
      ],
      "fieldConfig": {
        "defaults": {
          "thresholds": {
            "steps": [
              {"color": "red", "value": 0},
              {"color": "yellow", "value": 99},
              {"color": "green", "value": 99.9}
            ]
          },
          "min": 95,
          "max": 100,
          "unit": "percent"
        }
      }
    },
    {
      "title": "Error Budget Remaining",
      "type": "gauge",
      "targets": [
        {
          "expr": "slo:api_availability:error_budget_remaining * 100",
          "legendFormat": "Budget %"
        }
      ],
      "fieldConfig": {
        "defaults": {
          "thresholds": {
            "steps": [
              {"color": "red", "value": 0},
              {"color": "yellow", "value": 25},
              {"color": "green", "value": 50}
            ]
          },
          "min": 0,
          "max": 100,
          "unit": "percent"
        }
      }
    },
    {
      "title": "P99 Latency vs SLO",
      "type": "timeseries",
      "targets": [
        {
          "expr": "sli:api_requests:latency_p99 * 1000",
          "legendFormat": "P99 Latency"
        },
        {
          "expr": "slo:api_latency_p99:target_seconds * 1000",
          "legendFormat": "SLO Target"
        }
      ],
      "fieldConfig": {
        "defaults": {
          "unit": "ms"
        }
      }
    }
  ]
}
```

---

## Chaos Engineering

### LitmusChaos Experiment (Kubernetes)

```yaml
# pod-delete-experiment.yaml
apiVersion: litmuschaos.io/v1alpha1
kind: ChaosEngine
metadata:
  name: api-pod-delete
  namespace: production
spec:
  appinfo:
    appns: production
    applabel: "app=api-server"
    appkind: deployment
  chaosServiceAccount: litmus-admin
  experiments:
  - name: pod-delete
    spec:
      components:
        env:
        - name: TOTAL_CHAOS_DURATION
          value: "60"
        - name: CHAOS_INTERVAL
          value: "10"
        - name: FORCE
          value: "false"
        - name: PODS_AFFECTED_PERC
          value: "30"
      probe:
      - name: "check-api-health"
        type: "httpProbe"
        mode: "Continuous"
        runProperties:
          probeTimeout: 5
          interval: 5
          retry: 3
        httpProbe/inputs:
          url: "http://api-server.production.svc:8080/health/ready"
          method:
            get:
              criteria: "=="
              responseCode: "200"
---
# Network latency experiment
apiVersion: litmuschaos.io/v1alpha1
kind: ChaosEngine
metadata:
  name: api-network-latency
  namespace: production
spec:
  appinfo:
    appns: production
    applabel: "app=api-server"
    appkind: deployment
  chaosServiceAccount: litmus-admin
  experiments:
  - name: pod-network-latency
    spec:
      components:
        env:
        - name: NETWORK_INTERFACE
          value: "eth0"
        - name: NETWORK_LATENCY
          value: "200"  # 200ms added latency
        - name: TOTAL_CHAOS_DURATION
          value: "120"
        - name: CONTAINER_RUNTIME
          value: "containerd"
```

### Gremlin Attack (API)

```python
# gremlin_chaos.py
import requests
from datetime import datetime, timedelta

class GremlinClient:
    def __init__(self, api_key: str, team_id: str):
        self.api_key = api_key
        self.team_id = team_id
        self.base_url = "https://api.gremlin.com/v1"

    def run_cpu_attack(
        self,
        target_tags: dict,
        cpu_percent: int = 80,
        duration_seconds: int = 300,
    ) -> str:
        """Run CPU stress attack."""
        payload = {
            "command": {
                "type": "cpu",
                "args": ["-c", str(cpu_percent), "-l", str(duration_seconds)]
            },
            "target": {
                "type": "Exact",
                "exact": {
                    "tags": target_tags
                }
            }
        }

        response = requests.post(
            f"{self.base_url}/attacks/new",
            headers={
                "Authorization": f"Key {self.api_key}",
                "Content-Type": "application/json"
            },
            json=payload
        )
        response.raise_for_status()
        return response.json()["guid"]

    def run_latency_attack(
        self,
        target_tags: dict,
        latency_ms: int = 200,
        duration_seconds: int = 300,
        port: int = 8080,
    ) -> str:
        """Run network latency attack."""
        payload = {
            "command": {
                "type": "latency",
                "args": [
                    "-l", str(duration_seconds),
                    "-m", str(latency_ms),
                    "-p", f"^{port}",
                    "-h", "^api"
                ]
            },
            "target": {
                "type": "Exact",
                "exact": {
                    "tags": target_tags
                }
            }
        }

        response = requests.post(
            f"{self.base_url}/attacks/new",
            headers={
                "Authorization": f"Key {self.api_key}",
                "Content-Type": "application/json"
            },
            json=payload
        )
        response.raise_for_status()
        return response.json()["guid"]

    def halt_attack(self, attack_guid: str):
        """Stop a running attack."""
        requests.delete(
            f"{self.base_url}/attacks/{attack_guid}",
            headers={"Authorization": f"Key {self.api_key}"}
        )


# Usage in chaos test
def run_chaos_experiment():
    client = GremlinClient(
        api_key=os.environ["GREMLIN_API_KEY"],
        team_id=os.environ["GREMLIN_TEAM_ID"]
    )

    # Record baseline metrics
    baseline = get_current_metrics()

    # Run attack
    attack_id = client.run_latency_attack(
        target_tags={"service": "api", "env": "staging"},
        latency_ms=200,
        duration_seconds=300
    )

    try:
        # Wait for attack to complete
        time.sleep(300)

        # Compare metrics during attack
        attack_metrics = get_current_metrics()

        # Verify SLOs were maintained
        assert attack_metrics["availability"] >= 0.999, "Availability SLO violated"
        assert attack_metrics["latency_p99"] < 0.7, "Latency SLO violated (expected <700ms with 200ms added)"

    finally:
        client.halt_attack(attack_id)
```

---

## Disaster Recovery

### AWS Multi-Region DR with Terraform

```hcl
# dr_infrastructure.tf

# Primary region
provider "aws" {
  alias  = "primary"
  region = "us-east-1"
}

# DR region
provider "aws" {
  alias  = "dr"
  region = "us-west-2"
}

# Aurora Global Database (Multi-Region)
resource "aws_rds_global_cluster" "main" {
  global_cluster_identifier = "app-global-db"
  engine                    = "aurora-postgresql"
  engine_version            = "15.4"
  database_name             = "app"
  storage_encrypted         = true
}

# Primary cluster
resource "aws_rds_cluster" "primary" {
  provider = aws.primary

  cluster_identifier        = "app-db-primary"
  engine                    = aws_rds_global_cluster.main.engine
  engine_version            = aws_rds_global_cluster.main.engine_version
  global_cluster_identifier = aws_rds_global_cluster.main.id
  database_name             = "app"
  master_username           = var.db_username
  master_password           = var.db_password

  backup_retention_period = 7
  preferred_backup_window = "03:00-04:00"

  enabled_cloudwatch_logs_exports = ["postgresql"]
}

# DR cluster (read replica, can be promoted)
resource "aws_rds_cluster" "dr" {
  provider = aws.dr

  cluster_identifier        = "app-db-dr"
  engine                    = aws_rds_global_cluster.main.engine
  engine_version            = aws_rds_global_cluster.main.engine_version
  global_cluster_identifier = aws_rds_global_cluster.main.id

  # No credentials needed for replica
  skip_final_snapshot = true
}

# Route 53 health check for primary
resource "aws_route53_health_check" "primary" {
  fqdn              = aws_lb.primary.dns_name
  port              = 443
  type              = "HTTPS"
  resource_path     = "/health/ready"
  failure_threshold = 3
  request_interval  = 10

  tags = {
    Name = "primary-health-check"
  }
}

# Route 53 failover routing
resource "aws_route53_record" "api" {
  zone_id = var.route53_zone_id
  name    = "api.example.com"
  type    = "A"

  failover_routing_policy {
    type = "PRIMARY"
  }

  set_identifier = "primary"
  health_check_id = aws_route53_health_check.primary.id

  alias {
    name                   = aws_lb.primary.dns_name
    zone_id                = aws_lb.primary.zone_id
    evaluate_target_health = true
  }
}

resource "aws_route53_record" "api_dr" {
  zone_id = var.route53_zone_id
  name    = "api.example.com"
  type    = "A"

  failover_routing_policy {
    type = "SECONDARY"
  }

  set_identifier = "secondary"

  alias {
    name                   = aws_lb.dr.dns_name
    zone_id                = aws_lb.dr.zone_id
    evaluate_target_health = true
  }
}

# S3 Cross-Region Replication for backups
resource "aws_s3_bucket" "backups_primary" {
  provider = aws.primary
  bucket   = "app-backups-primary"
}

resource "aws_s3_bucket" "backups_dr" {
  provider = aws.dr
  bucket   = "app-backups-dr"
}

resource "aws_s3_bucket_replication_configuration" "backups" {
  provider = aws.primary
  bucket   = aws_s3_bucket.backups_primary.id

  role = aws_iam_role.replication.arn

  rule {
    id     = "replicate-all"
    status = "Enabled"

    destination {
      bucket        = aws_s3_bucket.backups_dr.arn
      storage_class = "STANDARD_IA"
    }
  }
}
```

### DR Runbook Template (Markdown)

```markdown
# Disaster Recovery Runbook: Primary Region Failure

## Overview
- **Scenario**: Complete failure of us-east-1 region
- **RTO Target**: 15 minutes
- **RPO Target**: 5 minutes (async replication lag)

## Pre-requisites
- [ ] DR infrastructure provisioned in us-west-2
- [ ] DNS failover configured in Route 53
- [ ] Database replica in sync (check replication lag)
- [ ] Latest backups verified

## Incident Detection
1. CloudWatch alarm: `PrimaryRegionUnhealthy`
2. Route 53 health check failing for >3 checks
3. Multiple customer reports of service unavailability

## Failover Procedure

### Phase 1: Assess (5 minutes)
1. [ ] Confirm primary region is unreachable
2. [ ] Check AWS Service Health Dashboard
3. [ ] Verify DR region health
4. [ ] Check database replication lag: `aws rds describe-global-clusters`
5. [ ] Notify incident commander

### Phase 2: Failover (5 minutes)
1. [ ] Promote DR database cluster:
   ```bash
   aws rds failover-global-cluster \
     --global-cluster-identifier app-global-db \
     --target-db-cluster-identifier app-db-dr
   ```

2. [ ] Verify DNS failover has occurred:
   ```bash
   dig api.example.com
   # Should return DR region ALB IP
   ```

3. [ ] Scale up DR EKS cluster:
   ```bash
   kubectl scale deployment api-server --replicas=10 -n production
   ```

### Phase 3: Verify (5 minutes)
1. [ ] Health check: `curl https://api.example.com/health/ready`
2. [ ] Smoke test critical paths:
   - [ ] User authentication
   - [ ] Order creation
   - [ ] Payment processing
3. [ ] Monitor error rates in Grafana
4. [ ] Verify no data loss by checking latest transactions

## Post-Failover
1. [ ] Update status page
2. [ ] Notify customers
3. [ ] Schedule post-incident review
4. [ ] Plan failback procedure

## Failback Procedure (After Primary Recovery)
1. Wait for primary region to fully recover
2. Re-establish replication from current primary (DR) to old primary
3. Verify replication is caught up
4. Schedule maintenance window for failback
5. Perform controlled failback during low-traffic period

## Contacts
- **Incident Commander**: @oncall-ic
- **Platform Team**: @platform-team
- **Database Team**: @dba-team
- **AWS Support**: Case #XXXXX

## Revision History
| Date | Version | Changes |
|------|---------|---------|
| 2025-01-15 | 1.0 | Initial version |
```

---

## Template Index

| Section | Templates |
|---------|-----------|
| Circuit Breaker | Python, Go, Java (Resilience4j) |
| Retry | Python (tenacity), Go (native), TypeScript |
| Timeout | Python (httpx), Go (context) |
| Health Checks | Kubernetes YAML, Python (FastAPI), Go |
| Rate Limiting | Python (Redis-based) |
| Graceful Shutdown | Python (FastAPI), Go |
| SLO Configuration | Prometheus rules, Grafana dashboard |
| Chaos Engineering | LitmusChaos (K8s), Gremlin (API) |
| Disaster Recovery | Terraform (AWS multi-region), Runbook |
