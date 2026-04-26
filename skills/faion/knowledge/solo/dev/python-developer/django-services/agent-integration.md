# Agent Integration — Django Services

## When to use
- Implementing CREATE/UPDATE/DELETE flows that touch ≥2 models or invoke external APIs
- Replacing fat-model logic (model methods doing email + payment + audit log)
- Wrapping side-effecting operations behind `@transaction.atomic` boundaries
- Building a testable surface for business rules (no Django request/response in tests)
- Layering DRF: serializers validate input, views delegate to services, services own writes

## When NOT to use
- Simple property calculations (use `@property` on the model)
- Pure querysets / chained filters (use a custom manager)
- Read-only, permission-aware fetches (use a selector, not a service)
- Trivial CRUD with single-model writes — direct ORM call is shorter

## Where it fails / limitations
- Agents accumulate dozens of `services/foo_services.py` modules; without a clear naming + re-export policy, discoverability tanks
- `*` keyword-only args silently break callers when a new required field is added — type-checker catches if pyright/mypy is wired, agents often skip it
- `transaction.atomic` over an outer service that calls inner services nests savepoints — surprising rollback semantics
- Signals (`post_save`) running inside a service's atomic block fire on commit; agents test with `transaction.on_commit` and forget that pytest's `TransactionTestCase` is needed
- Services that call `requests.post(...)` inside `atomic` block the DB transaction during network I/O — classic latency bug
- DRF `ModelSerializer.create()` temptation to call services from the serializer — couples serializer to write logic; agents do this from tutorials
- Type-hints for `User` collide between `auth.get_user_model()` (runtime) and `settings.AUTH_USER_MODEL` (string-typed) — agents emit broken hints

## Agentic workflow
Agent works at service granularity: one PR = one new service or one refactor of an existing service. The implementation pass writes the service + matching pytest covering happy path, validation failure, and external-failure rollback. A review subagent then asserts: (1) keyword-only args, (2) typed return, (3) `@transaction.atomic` only when ≥2 writes, (4) external I/O wrapped with `transaction.on_commit` for post-commit triggers. Selectors stay separate — services never read for read's sake.

### Recommended subagents
- General-purpose subagent — service implementation + pytest
- `faion-feature-executor` — sequence: write service → write tests → run pytest → run pyright
- `faion-sdd-execution` — gates: 90% coverage on services package, ruff DJ + B rules, no `print`
- Code-review subagent — PR diff scan for serializer→service calls, missing keyword-only `*`, raw `Exception` swallows

### Prompt pattern
```
Implement order_cancel(*, order: Order, reason: str, actor: User) -> Order:
1. Guard: order.status must be in {PENDING, PROCESSING}; else raise ValidationError.
2. Wrap in transaction.atomic.
3. Mark order.status = CANCELLED, persist; create AuditLog row.
4. on_commit: enqueue refund_payment.delay(order.id) and email task.
5. Return refreshed order.
Tests: 3 cases (happy, invalid status, payment refund failure rolls back AuditLog? no — refund happens post-commit).
File: apps/orders/services/order_services.py.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `pytest-django` | Run tests inside Django context | `pip install pytest-django` |
| `pytest-cov` | Coverage with branch tracking | `pip install pytest-cov` |
| `pyright` / `mypy` + `django-stubs` | Type-check service signatures | `pip install pyright django-stubs` |
| `ruff` (`DJ`, `B`, `SIM` groups) | Django + bugbear lint | `pip install ruff` |
| `factory_boy` | Realistic test fixtures | `pip install factory_boy` |
| `pytest-mock` | Mock external services per-test | `pip install pytest-mock` |
| `django-test-migrations` | Verify migrations alongside service changes | `pip install django-test-migrations` |
| `freezegun` | Deterministic timestamps in service tests | `pip install freezegun` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| HackSoft Django Styleguide | OSS docs | Yes | Canonical service + selector pattern reference |
| Sentry | SaaS | Yes | Service-layer raises bubble cleanly with `Sentry.set_tag('service', 'order_create')` |
| Celery | OSS | Yes | Services enqueue tasks via `task.delay_on_commit(...)` for safety |
| Datadog / New Relic | SaaS | Yes | Custom span per service via `tracer.wrap()` decorator |
| Stripe / Twilio / SendGrid | SaaS APIs | Yes | Side-effects belong in services, not views; mock SDKs in tests |
| `django-fsm` / `viewflow` | OSS | Yes | Encode state transitions inside service guards |
| `pydantic` | OSS | Yes | Use for service input DTOs when DRF serializer is overkill |

## Templates & scripts
See `templates.md` for keyword-only service signatures, error mapping, and DRF integration. Inline test pattern:

```python
# tests/services/test_order_services.py
import pytest
from apps.orders.services import order_cancel

@pytest.mark.django_db(transaction=True)
def test_order_cancel_happy(order_factory, user_factory, mocker):
    order = order_factory(status="PENDING")
    actor = user_factory(is_staff=True)
    refund = mocker.patch("apps.orders.services.order_services.refund_payment.delay")
    result = order_cancel(order=order, reason="user request", actor=actor)
    assert result.status == "CANCELLED"
    refund.assert_called_once_with(order.id)

@pytest.mark.django_db
def test_order_cancel_invalid_status(order_factory, user_factory):
    order = order_factory(status="DELIVERED")
    with pytest.raises(ValidationError):
        order_cancel(order=order, reason="x", actor=user_factory())
```

## Best practices
- Service signature is `def <entity>_<action>(*, ...) -> <ReturnType>:` — keyword-only and typed
- Wrap in `@transaction.atomic` only when there are ≥2 writes that must succeed together; otherwise let the caller decide
- Use `transaction.on_commit(callable)` for any side effect that should not happen on rollback (Celery tasks, webhook fires)
- Raise Django's `ValidationError` for input/state violations, custom `DomainError` subclasses for domain rules — map both at the view layer
- Services accept domain inputs (User, Order objects), not request/serializer instances — keeps them testable without an HTTP context
- Tests run with `pytest.mark.django_db(transaction=True)` only when verifying `on_commit` behavior; otherwise it's slower for no gain
- One module per bounded entity (`order_services.py`, `payment_services.py`); re-export the public API in `services/__init__.py`
- Docstring every service: 1-line purpose + Args + Returns + Raises — feeds future agent context

## AI-agent gotchas
- LLMs default to positional args and skip the leading `*` — enforce with ruff `RET` / pyright reportMissingTypeArgument
- Agents call services from inside DRF `ModelSerializer.create()` because tutorials show it; correct pattern: view → service, serializer is for I/O only
- `transaction.atomic` decorator stacking — agents wrap an inner service that's already wrapped, creating savepoints with surprising rollback. Document the rule: only outermost service in a flow is atomic.
- Mocking ORM is anti-pattern; agents mock `Order.objects.create` to avoid DB. Use real DB + factory_boy.
- Async views + sync ORM: agents add `async def` to a service, then call sync ORM inside — must use `sync_to_async` wrapper or stay sync
- Human-in-loop required when: changing service signatures used by ≥3 views, introducing new external API integration, modifying transaction boundaries
- Token waste: do not paste full models.py into context for service edits; just the model + manager being touched
- Agents over-create `<verb>_helper()` private functions inside services; if it's reusable, promote to a separate service; if not, inline

## References
- HackSoft Django Styleguide (Services + Selectors): https://github.com/HackSoftware/Django-Styleguide
- Two Scoops of Django, chapters on business logic separation
- Django docs `transaction.atomic` + `on_commit`: https://docs.djangoproject.com/en/5.0/topics/db/transactions/
- pytest-django: https://pytest-django.readthedocs.io/
- factory_boy + Django: https://factoryboy.readthedocs.io/en/stable/orms.html#django
- `django-fsm`: https://github.com/viewflow/django-fsm
- Cosmic Python (architectural patterns translatable to Django): https://www.cosmicpython.com/
