# Django Celery Tasks

Comprehensive guide for asynchronous task processing with Celery 5.4+ and Django 5.x.

## Overview

Celery is a distributed task queue that enables Django applications to execute tasks asynchronously outside the request/response cycle. It handles background processing, scheduled tasks, and distributed workloads.

## When to Use Celery

| Use Case | Why Celery |
|----------|------------|
| Email sending | Avoid blocking HTTP response, handle retries |
| Report generation | Long-running operations shouldn't block users |
| Image/video processing | CPU-intensive, needs separate worker resources |
| External API calls | Handle timeouts, retries, rate limiting |
| Data synchronization | Scheduled batch processing |
| Webhooks processing | Async handling with guaranteed delivery |
| PDF generation | Memory/CPU intensive operations |
| Payment processing | Reliable execution with retry logic |
| Search indexing | Background updates without blocking writes |
| Notification sending | Fan-out to multiple channels |

## When NOT to Use Celery

| Scenario | Alternative |
|----------|-------------|
| Simple cron jobs | `django-crontab` or system cron |
| Real-time updates | WebSockets, Server-Sent Events |
| Simple async I/O | `asyncio` with Django ASGI |
| In-request async | Django 4.1+ async views |
| Task queue < 100/day | Django management commands + cron |

## Architecture

```
Django App  →  Message Broker  →  Celery Workers  →  Results Backend
              (Redis/RabbitMQ)     (prefork/gevent)    (Redis/DB)
```

### Components

| Component | Purpose | Options |
|-----------|---------|---------|
| **Broker** | Message transport | Redis (simple), RabbitMQ (reliable) |
| **Worker** | Task execution | Prefork (CPU), Gevent (I/O) |
| **Backend** | Result storage | Redis (fast), Django DB (persistent) |
| **Beat** | Task scheduling | Periodic tasks, crontab |
| **Flower** | Monitoring | Web dashboard, metrics |

## Key Concepts

### Task States

```
PENDING → STARTED → SUCCESS
                  → FAILURE → RETRY
                  → REVOKED
```

### Execution Pools

| Pool | Best For | Concurrency |
|------|----------|-------------|
| **prefork** | CPU-bound tasks | # CPU cores |
| **gevent** | I/O-bound tasks | 100-1000 |
| **eventlet** | I/O-bound tasks | 100-1000 |
| **solo** | Development/debugging | 1 |

### Canvas Primitives

| Primitive | Description | Use Case |
|-----------|-------------|----------|
| **chain** | Sequential execution | A → B → C |
| **group** | Parallel execution | [A, B, C] |
| **chord** | Group + callback | [A, B, C] → D |
| **map** | Apply to each item | task.map([1,2,3]) |
| **starmap** | Apply with args | task.starmap([(1,2), (3,4)]) |

## Broker Comparison: Redis vs RabbitMQ

| Criteria | Redis | RabbitMQ |
|----------|-------|----------|
| **Setup complexity** | Simple | Moderate |
| **Performance** | High throughput | Moderate |
| **Reliability** | Basic (visibility timeout issues) | Strong (AMQP guarantees) |
| **Message routing** | Basic | Advanced (exchanges, bindings) |
| **Persistence** | Optional | Built-in |
| **Clustering** | Redis Cluster | Native clustering |
| **Monitoring** | Basic | Management UI |
| **Use case** | Development, small-medium scale | Production, mission-critical |

### Recommendation

- **Start with Redis**: Simpler setup, often already in stack for caching
- **Migrate to RabbitMQ**: When needing advanced routing, guaranteed delivery, or large scale
- **Common pattern**: RabbitMQ as broker, Redis as result backend

## Celery 5.4+ Features

### `delay_on_commit()` (Django 5.x)

```python
# BAD: Task might run before transaction commits
@transaction.atomic
def create_order(request):
    order = Order.objects.create(...)
    process_order.delay(order.id)  # Might fail: order not yet committed!

# GOOD: Task runs after transaction commits
@transaction.atomic
def create_order(request):
    order = Order.objects.create(...)
    process_order.delay_on_commit(order.id)  # Safe!
```

### Key Configuration Options

```python
# settings.py
CELERY_BROKER_URL = "redis://localhost:6379/0"
CELERY_RESULT_BACKEND = "redis://localhost:6379/1"

# Performance
CELERY_WORKER_PREFETCH_MULTIPLIER = 1  # Fair scheduling
CELERY_TASK_ACKS_LATE = True  # Acknowledge after completion
CELERY_TASK_REJECT_ON_WORKER_LOST = True  # Requeue on crash

# Reliability
CELERY_TASK_TRACK_STARTED = True
CELERY_RESULT_EXPIRES = 3600  # 1 hour

# Serialization
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_ACCEPT_CONTENT = ["json"]
```

## Production Considerations

### Scaling Strategy

| Workload | Worker Config |
|----------|---------------|
| CPU-intensive | `--pool=prefork --concurrency=4` (# cores) |
| I/O-intensive | `--pool=gevent --concurrency=100` |
| Mixed | Separate workers per queue type |

### High Availability

1. **Multiple workers**: Distribute across servers
2. **Queue separation**: Critical vs background tasks
3. **Broker HA**: Redis Sentinel or RabbitMQ clustering
4. **Monitoring**: Flower + Prometheus/Grafana

### Common Issues

| Issue | Solution |
|-------|----------|
| Memory leaks | `--max-tasks-per-child=1000` |
| Task pile-up | Increase workers, add rate limiting |
| Visibility timeout | Increase `CELERY_BROKER_TRANSPORT_OPTIONS` |
| Result backend full | Set `CELERY_RESULT_EXPIRES` |

## LLM Usage Tips

### Effective Prompting

When asking LLMs about Celery:

1. **Specify versions**: "Using Celery 5.4+ with Django 5.x"
2. **Describe context**: "I have CPU-bound image processing tasks"
3. **Mention broker**: "Using Redis as broker and backend"
4. **State constraints**: "Need exactly-once semantics"

### Common LLM Tasks

- Generate task definitions with proper retry logic
- Create Celery configuration for specific use cases
- Design task routing for mixed workloads
- Write tests for Celery tasks
- Debug task failures and timeout issues
- Implement task chaining workflows

### Anti-patterns LLMs Might Suggest

| Anti-pattern | Why Bad | Better Approach |
|--------------|---------|-----------------|
| `task_always_eager=True` in tests | Not realistic | Use `celery_worker` fixture |
| Sync calls in async tasks | Blocks event loop | Use async libraries |
| Large objects in task args | Serialization overhead | Pass IDs, fetch in task |
| Ignoring task results | Can't track failures | Enable result backend |
| No idempotency | Duplicate execution | Design idempotent tasks |

## Directory Contents

| File | Purpose |
|------|---------|
| [checklist.md](checklist.md) | Step-by-step integration guide |
| [examples.md](examples.md) | Real-world task implementations |
| [templates.md](templates.md) | Copy-paste task templates |
| [llm-prompts.md](llm-prompts.md) | Effective prompts for LLM-assisted development |

## External Resources

### Official Documentation

- [Celery Documentation](https://docs.celeryq.dev/en/stable/) - Complete reference
- [Django Integration](https://docs.celeryq.dev/en/stable/django/first-steps-with-django.html) - Setup guide
- [Canvas Workflows](https://docs.celeryq.dev/en/stable/userguide/canvas.html) - Task composition
- [Periodic Tasks](https://docs.celeryq.dev/en/main/userguide/periodic-tasks.html) - Celery Beat
- [Testing](https://docs.celeryq.dev/en/stable/userguide/testing.html) - Testing patterns

### Django Extensions

- [django-celery-beat](https://django-celery-beat.readthedocs.io/) - Database-backed periodic tasks
- [django-celery-results](https://django-celery-results.readthedocs.io/) - Store results in Django ORM
- [Flower](https://flower.readthedocs.io/) - Real-time monitoring

### Articles and Guides

- [TestDriven.io: Django and Celery](https://testdriven.io/guides/django-celery/) - Comprehensive guide
- [Blueshoe: Django Celery in Production](https://www.blueshoe.io/blog/django-celery-in-production/) - Production patterns
- [Celery Best Practices](https://denibertovic.com/posts/celery-best-practices/) - Time-tested advice
- [Celery Task Retries and Errors](https://blog.gitguardian.com/celery-tasks-retries-errors/) - Error handling

### Video Resources

- [Real Python: Celery with Django](https://realpython.com/asynchronous-tasks-with-django-and-celery/) - Tutorial
- [PyCon: Celery in Production](https://www.youtube.com/results?search_query=pycon+celery) - Conference talks

## Related Skills

- [django-services/](../django-services/) - Service layer patterns
- [python-async/](../python-async/) - Async patterns
- [django-testing.md](../django-testing.md) - Testing strategies

---

*Celery 5.4+ | Django 5.x | Redis/RabbitMQ*
