# Health Checks and Auto-Heal LLM Prompts

## Design Health Check System

```
Design a health check and auto-heal system for my platform.

Services:
[LIST with types, e.g.:
- nero-core: Celery workers (check via celery inspect ping)
- nero-channel-web: FastAPI (check via HTTP /health)
- nero-channel-tg: Python bot (check via systemd is-active)
- PostgreSQL: Docker (check via pg_isready)
- Redis: Docker (check via redis-cli ping)
- RabbitMQ: Docker (check via rabbitmq-diagnostics)
]

Requirements:
- Check interval: [e.g., 60 seconds]
- Auto-restart on failure (with cooldown)
- Max restarts per hour: [e.g., 3]
- Alert on persistent failure (Telegram/email)
- Don't restart during deployment

Provide:
1. Health check script (bash) for manual checks
2. Auto-heal watcher (Python) for continuous monitoring
3. systemd service for the watcher
4. Alert integration (Telegram or email)
5. Dashboard/status endpoint idea
6. Testing: how to simulate failures
```

## Implement Health Endpoint

```
Implement a /health endpoint for my [FRAMEWORK] application.

Framework: [FastAPI / Django / Express / etc.]
Dependencies to check:
- Database: [PostgreSQL/MySQL, connection pool or direct]
- Cache: [Redis, connection method]
- Message broker: [RabbitMQ/Kafka, if applicable]
- External APIs: [list, if applicable]

Requirements:
- /health: Full health check with dependency status
- /health/live: Simple liveness (200 OK, no dependency checks)
- Response includes: status, version, uptime, check details with latency
- Return 200 for healthy, 503 for degraded/unhealthy
- Checks complete within 5 seconds
- No authentication required
- Support "degraded" state (some deps down but service functional)

Provide:
1. Complete endpoint code
2. Dependency check functions (async if applicable)
3. Response schema/format
4. Integration with the application (router setup)
5. Example healthy and degraded responses
```

## Debug Failing Health Checks

```
My health check is reporting failures. Help me investigate.

Service: [NAME]
Health check type: [HTTP /health, systemd is-active, celery ping, etc.]
Error: [PASTE error message or describe behavior]

Recent changes:
[LIST any recent deployments, config changes, etc.]

Server state:
- Memory: [free -h output]
- Disk: [df -h output]
- Load: [uptime output]

Please:
1. What could cause this specific type of health check failure?
2. Diagnostic commands to run
3. How to check if the dependency is actually down vs health check is broken
4. Immediate fix (restart, config change, etc.)
5. Root cause investigation steps
6. How to prevent this in the future
```

## Auto-Heal Pattern Design

```
Design an auto-heal pattern for my platform that handles these failure modes:

Failure modes:
1. Service crashes (exit code != 0)
2. Service hangs (process alive but not responding)
3. Dependency down (Redis/PostgreSQL unavailable)
4. Memory exhaustion (OOM)
5. Disk full
6. Network issues

For each failure mode:
- How to detect it
- What action to take
- What NOT to do (avoid making it worse)
- When to alert vs auto-fix
- Recovery verification

Architecture decisions:
- Should the watcher be a separate process or systemd features?
- WatchdogSec vs external watcher: when to use each?
- How to handle cascading failures (one service down causes others to fail)
- How to handle deployment (don't auto-heal during deploy)

Provide the watcher implementation with all failure modes handled.
```

## systemd Watchdog Configuration

```
Configure systemd watchdog for my services.

Services:
[LIST with language/framework, e.g.:
- nero-channel-web: Python FastAPI with uvicorn
- nero-core: Python Celery workers
- nero-channel-tg: Python asyncio bot
]

For each service:
1. Appropriate WatchdogSec value
2. Service file configuration (Type=notify, Restart policy)
3. Application code to send watchdog notifications
4. How to test the watchdog (simulate a hang)

Questions:
- Can uvicorn/celery send WATCHDOG=1 natively?
- If not, how to add watchdog support (background task)?
- What happens when watchdog triggers? (SIGABRT, SIGKILL?)
- How to tune WatchdogSec (too short = false positives)
```

## Monitoring and Alerting Setup

```
Set up monitoring and alerting for my VPS.

What to monitor:
1. Service health (up/down status)
2. Memory usage (total and per-service)
3. Disk usage
4. CPU load
5. Queue depth (RabbitMQ messages)
6. Response time (API latency)
7. Error rate (application errors)

Alerting channels:
- Primary: [Telegram / Email / Slack]
- When to alert: [thresholds for each metric]
- Alert fatigue: how to avoid too many alerts

Constraints:
- Solo developer, single VPS
- Don't want to run Prometheus/Grafana (too heavy)
- Simple bash scripts or lightweight solution

Provide:
1. Monitoring scripts for each metric
2. Cron schedule for each check
3. Alert script with rate limiting
4. Simple status page/dashboard idea
5. Log-based monitoring (what to grep for)
```

## Circuit Breaker Implementation

```
Implement a circuit breaker for my service's dependency calls.

Service: [NAME]
Dependencies with circuit breakers needed:
[LIST, e.g.:
- Claude API (external, can be slow or rate-limited)
- PostgreSQL (local, usually reliable)
- Redis (local, usually reliable)
]

Requirements:
- States: closed (normal), open (blocking calls), half-open (testing)
- Configurable failure threshold and recovery timeout
- Per-dependency circuit breakers
- Logging when state changes
- Fallback behavior when circuit is open

Language: Python (async if applicable)

Provide:
1. CircuitBreaker class implementation
2. How to wrap dependency calls
3. Configuration values for each dependency
4. Monitoring/logging integration
5. Testing the circuit breaker
```
