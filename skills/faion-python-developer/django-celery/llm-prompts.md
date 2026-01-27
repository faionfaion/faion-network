# LLM Prompts for Django Celery Development

Effective prompts for LLM-assisted Celery development.

## Table of Contents

1. [Task Generation](#1-task-generation)
2. [Configuration](#2-configuration)
3. [Error Handling](#3-error-handling)
4. [Testing](#4-testing)
5. [Workflows](#5-workflows)
6. [Debugging](#6-debugging)
7. [Performance](#7-performance)
8. [Production](#8-production)

---

## 1. Task Generation

### Basic Task with Retry

```
Create a Celery task for Django 5.x with:
- Task name: {app_name}.{task_name}
- Purpose: {describe what the task does}
- Input parameters: {list parameters with types}
- Retry on: ConnectionError, TimeoutError
- Max retries: 3
- Exponential backoff with jitter
- Soft time limit: 5 minutes
- Returns dict with status and relevant data
- Proper logging
- Import models inside the function to avoid circular imports

Use @shared_task decorator with bind=True.
Include docstring with Args and Returns.
```

### Idempotent Task

```
Create an idempotent Celery task that:
- Performs: {describe action}
- Entity: {model name} with ID parameter
- Idempotency check: {describe how to check if already done}
- Uses database flag/timestamp to track completion
- Safe to retry multiple times without side effects
- Returns status indicating if action was performed or skipped

Include atomic database operations where needed.
```

### Task with Progress Tracking

```
Create a Celery task that processes a list of items with:
- Progress reporting via self.update_state()
- State: 'PROGRESS' with meta containing:
  - current: items processed
  - total: total items
  - percent: completion percentage
  - errors: error count
- Continues processing on individual item failures
- Logs errors but doesn't fail entire task
- Returns summary with processed/errors/total counts
```

### Long-Running Task

```
Create a long-running Celery task for {describe operation} that:
- Has soft_time_limit of {N} seconds
- Has time_limit of {N+60} seconds
- Catches SoftTimeLimitExceeded for graceful cleanup
- Saves partial progress before timeout
- Can be resumed from where it left off
- Updates status in database for monitoring
```

---

## 2. Configuration

### Initial Setup

```
Generate Celery configuration for a Django {version} project with:
- Broker: {Redis/RabbitMQ} at {url}
- Result backend: {Redis/Django DB}
- JSON serialization only (security)
- Timezone: UTC
- Task tracking enabled
- Late acknowledgment (acks_late)
- Reject on worker lost

Include:
1. config/celery.py with Celery app setup
2. config/__init__.py update
3. Relevant settings.py entries
4. Requirements packages with versions
```

### Task Routing Setup

```
Configure Celery task routing for:
- High priority queue: {list task patterns}
- Low priority queue: {list task patterns}
- Email queue: {list task patterns}
- Report queue (slow tasks): {list task patterns}

Include:
1. Queue definitions using Kombu
2. Task routes configuration
3. Worker startup commands for each queue
4. Docker compose service for each worker type
```

### Beat Schedule Configuration

```
Create Celery Beat schedule for these periodic tasks:

1. {task_name}: Every {interval}
   - Task path: {full.task.path}
   - Arguments: {kwargs if any}

2. {task_name}: Daily at {time}
   - Task path: {full.task.path}

3. {task_name}: Every Monday at {time}
   - Task path: {full.task.path}

Use crontab for specific times, float for intervals.
Include django-celery-beat DatabaseScheduler configuration.
```

### Production Settings

```
Generate production Celery settings for:
- Expected task volume: {N} tasks/minute
- Average task duration: {N} seconds
- Workload type: {CPU-bound/I/O-bound/mixed}
- Number of servers: {N}
- Memory per server: {N} GB

Include:
- Worker pool type and concurrency
- Prefetch multiplier
- Connection pool settings
- Memory leak prevention (max_tasks_per_child)
- Broker transport options
- Result expiration
```

---

## 3. Error Handling

### Retry Strategy

```
Design a retry strategy for a Celery task that calls {external service} with:
- Transient errors: {list error types to retry}
- Permanent errors: {list error types to NOT retry}
- Rate limit errors: respect Retry-After header
- Max retries: {N}
- Initial delay: {N} seconds
- Max delay: {N} seconds
- Exponential backoff with jitter

Include error classification and appropriate handling for each type.
```

### Dead Letter Queue

```
Implement a dead letter queue pattern for Celery tasks:
- Move failed tasks (after max retries) to DLQ
- Store: task name, args, kwargs, exception, traceback
- Allow manual retry from DLQ
- Alerting when DLQ reaches threshold
- Cleanup old DLQ entries after {N} days

Use Django model to store failed tasks.
Include admin interface for DLQ management.
```

### Circuit Breaker

```
Implement circuit breaker pattern for Celery task calling {external API}:
- Closed state: normal operation
- Open state: fail fast after {N} consecutive failures
- Half-open state: allow single test request after {N} seconds
- Track failure/success counts in Redis
- Raise CircuitOpenError when circuit is open
- Auto-recovery when API becomes available
```

---

## 4. Testing

### Unit Test Template

```
Generate pytest unit tests for this Celery task:

{paste task code}

Include tests for:
1. Successful execution with expected result
2. Entity not found handling
3. Retry on {specific exception}
4. Idempotency (if applicable)
5. Edge cases: {list specific cases}

Use unittest.mock to mock:
- Database queries
- External API calls
- Other Celery tasks

Don't use celery_worker fixture for unit tests.
```

### Integration Test

```
Generate pytest integration tests for Celery task with actual worker:
- Task: {task path}
- Fixtures needed: celery_session_app, celery_session_worker
- Test database state changes
- Test async result retrieval
- Timeout: 10 seconds for result.get()

Use TransactionTestCase if modifying database.
Include cleanup in fixtures.
```

### Mock Task in View Test

```
Generate test for Django view that triggers Celery task:
- View: {view path/name}
- Task triggered: {task path}
- HTTP method: {GET/POST}
- Request data: {describe payload}

Mock the task's delay/delay_on_commit method.
Verify task was called with correct arguments.
Verify response contains task_id or appropriate message.
```

---

## 5. Workflows

### Task Chain

```
Create a Celery chain workflow for {process name}:

Step 1: {task_name}
- Input: {params}
- Output: {what it returns}

Step 2: {task_name}
- Input: result from step 1
- Output: {what it returns}

Step 3: {task_name}
- Input: result from step 2
- Output: {what it returns}

Include:
- Individual task definitions
- Chain composition
- Error handling callback
- State tracking in database
- Ability to resume from failed step
```

### Parallel Processing (Group)

```
Create a Celery group workflow that:
- Processes {N} items in parallel
- Each item task: {describe processing}
- Collects all results
- Handles individual failures without failing group
- Reports progress across all tasks
- Has overall timeout of {N} seconds

Include group composition and result handling.
```

### Chord (Parallel + Callback)

```
Create a Celery chord workflow for {use case}:

Parallel tasks (header):
- Task: {task_name}
- Items to process: {describe items}
- Each task returns: {describe output}

Callback task (body):
- Receives: list of all parallel task results
- Aggregates: {describe aggregation}
- Stores result in: {database/cache/file}
- Notifies: {user/system}

Include error handling for partial failures.
```

### Fan-out Pattern

```
Create fan-out notification system that sends to multiple channels:
- User ID as input
- Channels: email, SMS, push notification, in-app
- Each channel has its own task
- Channels are called in parallel
- Respect user's channel preferences
- Return summary of which channels succeeded/failed

Include channel preference checking and graceful degradation.
```

---

## 6. Debugging

### Task Not Running

```
Debug Celery task that's not executing:

Symptoms:
- Task is called with delay()
- No errors in logs
- Task never appears in Flower
- {any other symptoms}

Environment:
- Broker: {Redis/RabbitMQ}
- Django version: {version}
- Celery version: {version}
- Running in: {Docker/systemd/manual}

Provide checklist of things to verify:
1. Worker connectivity
2. Task discovery
3. Queue configuration
4. Serialization issues
5. Common misconfigurations
```

### Task Stuck/Timeout

```
Debug Celery task that's stuck or timing out:

Task: {task path}
Symptoms:
- Task starts but never completes
- Logs show: {relevant log lines}
- Timeout after: {N} seconds
- Worker behavior: {hanging/high CPU/normal}

Provide:
1. Diagnostic steps
2. Common causes for this pattern
3. How to add debugging to the task
4. Monitoring queries to run
```

### Memory Leak Investigation

```
Debug memory leak in Celery worker:

Symptoms:
- Worker memory grows over time
- Currently at {N} GB after {N} hours
- Affects tasks: {list suspected tasks}
- Pool type: {prefork/gevent}

Provide:
1. Memory profiling approach
2. Common leak patterns in Celery
3. Task-level fixes
4. Worker configuration to mitigate
5. Monitoring setup
```

---

## 7. Performance

### Optimize Task

```
Optimize this Celery task for performance:

{paste task code}

Current issues:
- Processing {N} items takes {N} seconds
- High memory usage: {N} MB
- Database queries: {N} queries

Target:
- Processing time: {target}
- Memory: {target}

Suggest:
1. Batch processing improvements
2. Query optimization
3. Memory-efficient iteration
4. Parallel processing opportunities
5. Caching strategies
```

### Scaling Strategy

```
Design Celery scaling strategy for:

Current load:
- Tasks/minute: {N}
- Peak tasks/minute: {N}
- Task types: {CPU-bound/I/O-bound percentage}

Current infrastructure:
- Workers: {N}
- Concurrency: {N} per worker
- Pool: {prefork/gevent}

Constraints:
- Budget: {describe}
- Latency requirements: {N} seconds max

Provide:
1. Worker count and configuration
2. Queue separation strategy
3. Autoscaling configuration
4. Monitoring metrics to track
5. Cost optimization
```

### Rate Limiting Design

```
Design rate limiting for task calling {external API}:

API limits:
- {N} requests per {period}
- Burst: {N} requests
- Rate limit response: {HTTP code/header}

Requirements:
- Never exceed API limits
- Fair distribution across tasks
- Handle rate limit responses gracefully
- Queue overflow strategy

Implement using:
- Celery rate_limit option
- Redis-based distributed counter
- Exponential backoff on 429
```

---

## 8. Production

### Deployment Checklist

```
Generate production deployment checklist for Celery with:

Infrastructure:
- Broker: {Redis/RabbitMQ}
- Workers: {N} servers
- Beat: single instance
- Flower: for monitoring

Requirements:
- Zero-downtime deploys
- Graceful worker shutdown
- Task draining before restart
- Rollback capability

Include:
1. Pre-deployment checks
2. Deployment steps
3. Post-deployment verification
4. Rollback procedure
5. Monitoring alerts to configure
```

### Docker Production Setup

```
Generate production Docker setup for Celery:

Services needed:
- Redis (broker + result backend)
- Worker (CPU-bound tasks)
- Worker-IO (I/O-bound tasks)
- Beat scheduler
- Flower monitoring

Requirements:
- Health checks
- Resource limits
- Log aggregation
- Secrets management
- Auto-restart on failure

Generate:
1. docker-compose.yml
2. Dockerfile
3. Entrypoint scripts
4. Health check endpoints
```

### Monitoring Setup

```
Design monitoring setup for Celery in production:

Metrics to track:
- Task success/failure rates
- Task latency (p50, p95, p99)
- Queue depth
- Worker status
- Memory usage

Alerting rules for:
- Task failure rate > {N}%
- Queue depth > {N}
- Worker offline
- Task timeout
- Memory threshold

Stack:
- {Prometheus/Datadog/New Relic}
- {Grafana/native dashboards}

Include:
1. Flower configuration with prometheus_metrics
2. Prometheus scrape config
3. Key Grafana dashboard panels
4. Alert rules with thresholds
```

### Incident Response

```
Create incident response runbook for Celery issues:

Scenario: {describe incident type}
- Symptoms: {what alerts/symptoms trigger this}
- Impact: {user/system impact}

Runbook should include:
1. Triage steps (first 5 minutes)
2. Diagnostic commands to run
3. Common root causes
4. Immediate mitigation steps
5. Full resolution procedures
6. Post-incident tasks

Use actual commands and queries, not placeholders.
```

---

## Prompt Engineering Tips

### Effective Prompts

1. **Specify versions**: Always mention Django and Celery versions
2. **Describe context**: Explain what the task does and why
3. **Mention constraints**: Time limits, rate limits, error handling needs
4. **Provide examples**: Show expected input/output
5. **List edge cases**: Help LLM understand failure scenarios

### Template Structure

```
Task: {what you want}

Context:
- Django version: {X.Y}
- Celery version: {X.Y}
- Broker: {Redis/RabbitMQ}
- Purpose: {why this task exists}

Requirements:
- {list specific requirements}
- {error handling needs}
- {performance requirements}

Constraints:
- {time limits}
- {rate limits}
- {dependencies}

Expected behavior:
- Input: {describe}
- Output: {describe}
- On error: {describe}

Please include:
- Complete code with imports
- Docstrings
- Type hints
- Error handling
- Logging
```

### Anti-patterns to Avoid

When reviewing LLM-generated code, watch for:

| Anti-pattern | Why Bad | Fix |
|--------------|---------|-----|
| `task_always_eager=True` | Not realistic testing | Use celery_worker fixture |
| Passing ORM objects to tasks | Serialization issues | Pass IDs, fetch in task |
| No idempotency | Duplicate execution | Add completion checks |
| Ignoring results | Can't track failures | Enable result backend |
| Sync I/O in gevent worker | Blocks event loop | Use async libraries |
| No time limits | Tasks run forever | Set soft_time_limit |
| Hardcoded retry delays | No backoff | Use retry_backoff=True |

---

## Quick Reference

### Common Task Options

```python
@shared_task(
    name='explicit.task.name',
    bind=True,                    # Pass self
    max_retries=3,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_jitter=True,
    soft_time_limit=300,
    time_limit=360,
    rate_limit='10/m',
    ignore_result=False,
    acks_late=True,
)
```

### Common Commands

```bash
# Worker commands
celery -A config worker --loglevel=INFO
celery -A config worker -Q queue1,queue2
celery -A config worker --pool=gevent -c 100

# Beat commands
celery -A config beat --scheduler django_celery_beat.schedulers:DatabaseScheduler

# Inspection commands
celery -A config inspect active
celery -A config inspect scheduled
celery -A config inspect reserved

# Management commands
celery -A config purge
celery -A config control shutdown
```

---

*Celery 5.4+ | Django 5.x*
