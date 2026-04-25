# Agent Integration — Django Celery

## When to use
- Any Django operation that takes >100ms and isn't critical to the response (email, PDF, image, webhook fan-out)
- Scheduled batch work (nightly aggregations, reminder emails) via Celery Beat
- Retry-with-backoff for flaky third-party APIs (Stripe, Twilio, SendGrid)
- Long-running background flows orchestrated as `chain` / `chord` / `group`
- CPU-intensive work that needs separate worker resources (image, ML inference)

## When NOT to use
- Sub-100/day jobs — `python manage.py` + system cron is simpler
- Hard real-time requirements (<100ms) — use ASGI + WebSocket, not async tasks
- Simple async I/O inside a request — Django 4.1+ async views work
- Tasks that must succeed inline with the user response (payment authorization)
- Tiny apps where running Redis + worker + beat is operational overhead

## Where it fails / limitations
- `task.delay()` inside `@transaction.atomic` runs before commit — task fetches DB row that doesn't exist yet. Must use `delay_on_commit()` (Celery 5.4+) or `transaction.on_commit(lambda: task.delay(...))`
- Redis broker visibility timeout: long tasks (>1h default) get re-delivered → duplicate execution. Configure `BROKER_TRANSPORT_OPTIONS={'visibility_timeout': N}`
- Result backend memory leak: `task.AsyncResult.get()` blocks workers if results aren't expired (`CELERY_RESULT_EXPIRES`)
- `acks_late=True` without idempotency = double-execution on worker crash; agents enable it without idempotency keys
- Celery Beat scheduler in default file mode: leader election is fragile in multi-pod deploys → duplicate cron firing. Use `django-celery-beat` (DB scheduler) or RedBeat
- `chord` callbacks run on a worker different from the group; closing over `self.request` breaks
- Pickle serializer (default in older configs) + JSON serializer mismatch silently swallows complex objects
- `CELERY_TASK_EAGER_PROPAGATES=True` masks bugs in tests by raising synchronously instead of replicating worker behavior
- Tasks that take ORM model instances as args break on retry (instance is stale or deleted) — pass IDs

## Agentic workflow
Agent treats every task as a contract: signature accepts primitives (IDs, strings, ints), is idempotent, has explicit retry policy, and lives in `<app>/tasks.py`. The implementation pass writes the task + a unit test using `CELERY_TASK_ALWAYS_EAGER=True` for happy path, plus an integration test against a real Redis worker for retry/idempotency. A review subagent enforces `delay_on_commit` usage when called from a `transaction.atomic` block, and forbids passing model instances as task args. Beat schedules are codified in `CELERY_BEAT_SCHEDULE` or a `django-celery-beat` migration, never set via the admin UI.

### Recommended subagents
- General-purpose subagent — task implementation + test scaffolding
- `faion-feature-executor` — sequence: write task → write test → wire to caller → assert idempotency
- `faion-sdd-execution` — gates: no model-instance args, no bare `except:`, retry policy declared, idempotency key documented
- Code-review subagent — diff scan for `task.delay(` inside `atomic` blocks; auto-suggest `delay_on_commit`

### Prompt pattern
```
Implement send_order_confirmation(order_id: int):
1. Fetch Order by id; if missing, log warning + return (idempotent no-op).
2. Skip if order.confirmation_sent_at is not null.
3. Call email service; on transient failure raise self.retry(countdown=2**self.request.retries, max_retries=5).
4. On success, atomically update confirmation_sent_at = now().
5. Configure: bind=True, autoretry_for=(EmailGatewayError,), retry_backoff=True, retry_jitter=True.
File: apps/orders/tasks.py.
Test: 4 cases (happy, missing order, already sent, transient retry).
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `celery -A proj worker -l info` | Run worker | https://docs.celeryq.dev/ |
| `celery -A proj beat` | Run scheduler | https://docs.celeryq.dev/en/stable/userguide/periodic-tasks.html |
| `celery -A proj inspect active` / `stats` / `registered` | Live introspection | shipped with celery |
| `celery -A proj events` | Stream task events | shipped with celery |
| `flower` | Web UI for tasks/queues | `pip install flower` |
| `django-celery-beat` | DB-backed periodic tasks | `pip install django-celery-beat` |
| `django-celery-results` | Persist results in Django DB | `pip install django-celery-results` |
| `celery-redbeat` | Redis-backed scheduler with leader election | `pip install celery-redbeat` |
| `celery-once` | Distributed lock to prevent overlapping runs | `pip install celery-once` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Redis (broker + backend) | OSS / managed (Upstash, Redis Cloud, ElastiCache) | Yes | Simplest start; watch visibility timeout |
| RabbitMQ | OSS / managed (CloudAMQP) | Yes | Stronger guarantees, advanced routing |
| Flower | OSS | Yes | Read-only via API; agents poll for stuck tasks |
| Sentry | SaaS | Yes (Celery integration) | Auto-captures task exceptions, attaches `task_id` tag |
| Datadog / New Relic | SaaS | Yes | Trace propagation across `delay_on_commit` boundary works with OTel |
| Prometheus + `celery-prometheus-exporter` | OSS | Yes | Metrics for queue depth, runtime histograms |
| `dramatiq` | OSS (alternative) | Yes | Simpler than Celery if Celery's complexity hurts |

## Templates & scripts
See `templates.md` for full task signatures, retry policies, and Beat schedules. Idempotent task skeleton:

```python
# apps/orders/tasks.py
from celery import shared_task
from celery.utils.log import get_task_logger
from django.db import transaction
from django.utils import timezone
from .models import Order
from .integrations.email import send_email, EmailGatewayError

log = get_task_logger(__name__)

@shared_task(
    bind=True,
    autoretry_for=(EmailGatewayError,),
    retry_backoff=True,
    retry_jitter=True,
    max_retries=5,
    acks_late=True,
)
def send_order_confirmation(self, order_id: int) -> None:
    order = Order.objects.filter(pk=order_id).first()
    if order is None:
        log.warning("order %s missing; skipping", order_id)
        return
    if order.confirmation_sent_at is not None:
        return
    send_email(to=order.email, template="order_confirmation", ctx={"order": order.id})
    with transaction.atomic():
        Order.objects.filter(pk=order.pk, confirmation_sent_at__isnull=True).update(
            confirmation_sent_at=timezone.now()
        )
```

## Best practices
- Pass IDs, not model instances; rehydrate inside the task to defeat staleness and pickle issues
- Make every task idempotent — re-running it must be safe (use a sent_at timestamp or a UUID idempotency key)
- Use `delay_on_commit()` from any code touching a transaction; never call `delay()` inside `@transaction.atomic`
- Configure per-task time limits: `task_time_limit` (hard) and `task_soft_time_limit` (catchable) — kill stuck workers
- Separate queues by SLA (`fast`, `slow`, `email`, `webhooks`) and pin worker concurrency per queue
- Beat schedule lives in version-controlled config (`CELERY_BEAT_SCHEDULE` dict or a fixture loaded into `django-celery-beat`); never set via admin
- Use `acks_late=True` only with idempotent tasks — pairs with `task_reject_on_worker_lost=True`
- Result backend default `CELERY_RESULT_EXPIRES = 3600`; raise only when actively reading results — otherwise let them expire
- Test with `CELERY_TASK_ALWAYS_EAGER=True` for unit tests, real Redis for integration tests of retry behavior

## AI-agent gotchas
- Agents pass model instances (`task.delay(order)`) — pickles fine, fails in retry. Lock with a lint rule: any task arg must be JSON-serializable primitives or pydantic models.
- LLMs trained on pre-5.4 docs emit `transaction.on_commit(lambda: task.delay(...))` boilerplate; modern code uses `task.delay_on_commit(...)`. Both work; prefer the modern form for readability.
- `bind=True` adds `self` as first arg; agents copy-paste a `bind=True` task body without using `self.retry` and silently lose retry capability
- Eager mode in tests masks broker bugs (visibility timeout, serializer mismatch); add at least one integration test against real Redis
- Beat with file scheduler in containers: schedule resets on every redeploy → some tasks miss their slot. Use `django-celery-beat` or RedBeat.
- Human-in-loop required when: introducing a new queue, changing visibility timeout, modifying Beat schedule of business-critical tasks (billing, reconciliation)
- Agents wire Flower behind public ingress without auth — admin endpoint exposes task payloads. Always require basic-auth or VPN-only.
- Token waste: do not feed full Celery docs into context; cite specific options by name and let the agent look them up

## References
- Celery docs: https://docs.celeryq.dev/en/stable/
- Celery 5.4 release notes (`delay_on_commit`): https://docs.celeryq.dev/en/stable/history/whatsnew-5.4.html
- `django-celery-beat`: https://django-celery-beat.readthedocs.io/
- `celery-redbeat`: https://github.com/sibson/redbeat
- `celery-once`: https://github.com/cameronmaske/celery-once
- HackSoft Celery guide: https://www.hacksoft.io/blog/celery-best-practices
- Sentry Celery integration: https://docs.sentry.io/platforms/python/integrations/celery/
- Flower: https://flower.readthedocs.io/
