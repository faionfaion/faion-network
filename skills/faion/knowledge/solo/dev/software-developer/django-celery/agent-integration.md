# Agent Integration — Django Celery Tasks

## When to use
- Off-loading work that exceeds ~500ms inside an HTTP request (emails, PDF gen, image processing, third-party API calls)
- Scheduled jobs (Celery beat) replacing `cron` for deploy-portable scheduling tied to settings/secrets
- Fan-out workloads (per-user nightly digests, batch notifications) with concurrency limits per queue
- Webhook receivers that must `200 OK` fast and process async
- Retry-with-backoff for flaky upstreams without poisoning the request thread

## When NOT to use
- Sub-second jobs already inside the request — Celery overhead (broker hop + serializer) dominates
- Strict-ordering pipelines with stateful dependencies — use a workflow engine (Prefect, Temporal, Dagster)
- Streaming/exactly-once semantics — Celery is at-least-once; design idempotency or pick Kafka/Redpanda + a stream worker
- Tasks needing mid-flight cancellation across many workers — Celery revoke is best-effort
- Apps already on `django-q2`, `huey`, `dramatiq`, `arq`, RQ — switching costs rarely pay back unless multi-broker / chord workflows are needed

## Where it fails / limitations
- Tasks holding ORM objects across queue serialization deserialize stale; pass IDs, not models
- `result_backend` defaults are heavy; many teams disable results and rely on logs
- Soft/hard time limits don't kill blocking C extensions cleanly; agents misconfigure these and cause zombie workers
- Long-running tasks block worker concurrency slots; mixing fast and slow tasks on one queue starves others
- Beat schedules drift on multi-replica setups without `RedBeat` or equivalent leader election
- Memory leaks: each task should be short and stateless; agents create singleton state in worker memory
- Visibility timeouts (Redis broker) cause duplicate execution if a task runs past the timeout

## Agentic workflow
A task agent first asks: "must this be async?" If yes, generates the task module with idempotency guard, retry policy, time limits, and a paired test that asserts both happy path and retry path. A queue-router agent updates `task_routes` and ensures workers exist for each queue. A monitoring agent integrates Sentry and Flower / OpenTelemetry. Treat any new task as a deploy artifact: it needs a queue, a worker process, and an alert.

### Recommended subagents
- `faion-sdd-executor-agent` — design + implement + verify with idempotency test as quality gate
- A custom `task-auditor` (sonnet) — finds tasks lacking `bind=True`, retry config, time limits, idempotency guards
- A custom `queue-balancer` (haiku) — reads `task_routes` and worker `--queues=` flags, flags mismatches

### Prompt pattern
```
Implement async task:
- Trigger: <event>
- Inputs: pass primitive IDs only, never model instances
- Idempotency: check <field> before side effect
- Retries: exponential backoff, max 5
- Time limits: soft 300s, hard 360s
- Queue: <queue-name>
Output: tasks.py module, test_tasks.py, task_routes patch, worker --queues line.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `celery` | Worker + beat + control commands | `pip install celery` · https://docs.celeryq.dev |
| `celery -A app inspect / control` | Live worker introspection | `celery -A proj inspect active` |
| `flower` | Web dashboard for queues/workers | `pip install flower` · https://flower.readthedocs.io |
| `celery-prometheus-exporter` / `celery-exporter` | Metrics for Prometheus | https://github.com/danihodovic/celery-exporter |
| `redbeat` | Reliable Beat scheduler with Redis-backed leader election | `pip install celery-redbeat` |
| `pytest-celery` | Test fixtures for Celery in CI | https://docs.celeryq.dev/projects/pytest-celery |
| `valkey-cli` / `redis-cli` | Inspect broker queues and DLQs | https://valkey.io |
| `aioamqp` / `rabbitmq-management` | RabbitMQ broker introspection | https://rabbitmq.com |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Redis / Valkey | OSS | Yes | Common broker + result backend for solo deployments |
| RabbitMQ / CloudAMQP | OSS / SaaS | Yes | More robust broker for fan-out and DLQs |
| Amazon SQS | SaaS | Yes | Managed; supported by Celery as broker |
| Sentry | SaaS | Yes | First-class Celery integration; auto-captures task exceptions |
| Flower | OSS | Yes | UI + REST API to inspect/cancel tasks |
| OpenTelemetry-Python | OSS | Yes | Auto-instrument Celery for traces |
| Honeybadger / Bugsnag | SaaS | Yes | Alternatives to Sentry |

## Templates & scripts
See `templates.md` for full task module pattern. Inline systemd unit + supervisor pattern for a single-queue worker:

```ini
# /etc/systemd/system/celery-orders.service
[Unit]
Description=Celery worker (orders queue)
After=network.target redis.service

[Service]
Type=simple
User=app
EnvironmentFile=/etc/app/celery.env
WorkingDirectory=/srv/app
ExecStart=/srv/app/.venv/bin/celery -A config worker \
  -Q orders -n orders@%%h \
  --concurrency=4 --max-tasks-per-child=200 \
  --soft-time-limit=300 --time-limit=360 \
  --without-gossip --without-mingle
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
```

```python
# Idempotent task pattern
@shared_task(bind=True, max_retries=5, autoretry_for=(requests.RequestException,),
             retry_backoff=True, retry_backoff_max=600, retry_jitter=True,
             soft_time_limit=300, time_limit=360, name="emails.send_welcome")
def send_welcome(self, user_id: int) -> bool:
    from apps.users.models import User
    user = User.objects.only("id", "email", "welcome_email_sent").get(pk=user_id)
    if user.welcome_email_sent:
        return False
    send_email(user.email, "Welcome!")
    User.objects.filter(pk=user_id, welcome_email_sent=False).update(welcome_email_sent=True)
    return True
```

## Best practices
- Pass primitive IDs, never model instances; tasks fetch fresh state to avoid stale serialized objects
- Every side-effecting task is idempotent: check-then-act with a DB-level guard (`UPDATE ... WHERE not_done=true`)
- Always set `soft_time_limit` and `time_limit` (soft fires `SoftTimeLimitExceeded`, hard SIGKILLs) — defaults are dangerous
- Set `--max-tasks-per-child=N` to recycle workers and dodge slow memory leaks
- Route by workload class: `emails`, `webhooks`, `reports`. One queue = one SLA
- Use `acks_late=True` and `task_reject_on_worker_lost=True` for tasks that must not lose work on worker crash
- Disable result backend unless you actually consume results; reduces broker pressure
- Beat: use `RedBeat` or `django-celery-beat` with leader election; never run multiple naive beat processes
- Monitor queue depth and task age, not just success rate; agents should alert on backlog growth

## AI-agent gotchas
- Agents pass `User` instance into `.delay(user)`; pickling fails or worker uses stale data — enforce primitive args
- LLMs forget `bind=True` and try `self.retry()` without it — task crashes on retry
- Agents pick `delay()` for time-sensitive jobs without confirming a worker for that queue runs in production
- "I added a beat schedule" with no leader election → duplicate executions in HA — require RedBeat
- Agents add chains/chords without considering broker memory; deeply nested chords stall on Redis broker
- Time-limit agents skip: long-running tasks then block worker slots indefinitely
- Human-in-loop checkpoint: tasks that send to many users (`User.objects.all().iterator()`) must require explicit approval; otherwise a typo fan-outs to everyone
- Agents tend to inline secrets into task code; require env-var indirection so workers reload via systemd EnvironmentFile

## References
- https://docs.celeryq.dev
- https://docs.celeryq.dev/en/stable/django/first-steps-with-django.html
- https://denibertovic.com/posts/celery-best-practices/
- https://docs.celeryq.dev/en/stable/userguide/tasks.html#retrying
- https://flower.readthedocs.io
- https://github.com/sibson/redbeat
- https://docs.sentry.io/platforms/python/integrations/celery/
- https://www.cloudamqp.com/blog/celery-and-rabbitmq-tutorial.html
