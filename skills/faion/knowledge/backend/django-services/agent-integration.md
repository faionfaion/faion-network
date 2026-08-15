# Agent Integration — Django Services Architecture

## When to use
- Adding any DB-mutating logic (create/update/delete) — never put it in views or model `save()` overrides
- Coordinating multi-model writes that need a single transactional boundary
- Wrapping outbound API/SMTP/SMS calls so views/serializers stay thin
- Making business logic unit-testable without HTTP or DRF context
- Letting Celery tasks and management commands share one entry point

## When NOT to use
- Pure functions (validation, formatting, calculation) — those go in `utils/`
- Trivial single-model `obj.field = x; obj.save()` callable from one view (pre-extraction overhead)
- Read-only Django queryset chaining — keep on the manager / `objects`
- DRF view-only concerns (permission checks, serializer wiring)

## Where it fails / limitations
- Service-as-class with heavy DI tends to drift toward fake-OO; prefer functions until DI is justified
- `from __future__ import annotations` + lazy imports are required to avoid Django app-loading order errors when services reference models at module top-level
- Functions taking `request` couple business logic to HTTP — pass extracted primitives instead
- LLMs frequently inline DB writes into views; reviewers must enforce the `services/` boundary
- "Fat services" with 200+ line functions hide multiple responsibilities — split by use case, not by model

## Agentic workflow
Drive Django service extraction with a two-phase agent: first a planner reads the view/serializer, identifies side effects, and emits a service contract (signature + business rules); then an implementer writes the `services/<feature>.py` function and rewrites the caller to delegate. A reviewer subagent enforces import direction (`services` may import `models`/`utils`, never `views`/`serializers`) and the keyword-only-args convention.

### Recommended subagents
- `faion-sdd-executor-agent` — plan-then-implement loop with quality gates; ideal for converting fat views to service functions
- `nero-sdd-executor-agent` — same loop wired to NERO project conventions
- A custom `code-reviewer` agent (sonnet) — verifies import boundaries, docstring style, `update_fields=`, transaction wrapping

### Prompt pattern
```
Task: Extract activation logic from apps/inventory/views.py:ActivateItemView into services/.
Constraints:
- Function-style service, keyword-only optional args, Google-style docstring.
- Lazy import of models inside the function body.
- Return the mutated model; raise domain exceptions, never DRF exceptions.
- Wrap multi-write paths in transaction.atomic().
Output: file diff for services/<name>.py + the rewritten view.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `ruff` | Lint + format (E/F/I/B/UP/SIM/DJ/T20) — repo standard | `pip install ruff` · https://docs.astral.sh/ruff/ |
| `mypy` / `pyright` | Type-check service signatures | `pip install mypy` · https://mypy.readthedocs.io |
| `django-stubs` | Type stubs for `Manager`/`QuerySet` | `pip install django-stubs[compatible-mypy]` |
| `pytest-django` | Run service-layer tests without DRF client overhead | `pip install pytest-django` |
| `factory_boy` | Build fixtures for service inputs | https://factoryboy.readthedocs.io |
| `django-extensions` `shell_plus` | Iterate service calls with autoloaded models | `pip install django-extensions` |
| `coverage.py` | Verify services hit ≥90% — they hold the rules | `pip install coverage` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Sentry | SaaS | Yes (REST API + SDK) | Capture domain exceptions raised by services for observability |
| Celery + Redis/Valkey | OSS | Yes | Reuse the same service function from views and tasks |
| Datadog APM / OpenTelemetry | SaaS / OSS | Yes | Auto-trace `services.*` modules; agents can wire decorators |
| pytest-django + GitHub Actions | OSS | Yes | Standard CI loop for service test suites |
| ruff pre-commit hook | OSS | Yes | Repo-wide gate; agents must `ruff check --fix` before commit |

## Templates & scripts
See `templates.md` for the full service module skeleton. Inline starter for an LLM to scaffold a service file from a view:

```python
# services/<feature>.py
from __future__ import annotations
from typing import TYPE_CHECKING
from django.db import transaction

if TYPE_CHECKING:
    from apps.<app>.models import <Model>
    from apps.users.models import User

class <Feature>Error(Exception):
    """Domain error raised by <feature> service."""

@transaction.atomic
def <verb>_<noun>(
    user: "User",
    *,
    <param>: str,
) -> "<Model>":
    """One-line summary.

    Business logic:
    - bullet
    - bullet
    """
    from apps.<app>.models import <Model>
    obj = <Model>.objects.select_for_update().get(<lookup>=<param>)
    # mutate
    obj.save(update_fields=[...])
    return obj
```

## Best practices
- Keep services pure-Python signatures (no `request`, no DRF `Response`, no `HttpResponse`)
- Use keyword-only args (`*,`) for every optional parameter — prevents positional-arg drift across versions
- Always pass `update_fields=` on partial saves; LLMs default to full saves which trigger every signal
- Wrap multi-write paths in `transaction.atomic()`; isolate `select_for_update()` to the service, never the view
- Define a `<Feature>Error` exception per service module so views can map to HTTP cleanly
- Lazy-import models inside the function body to dodge app-loading cycles in larger codebases
- Co-locate service tests in `tests/services/test_<feature>.py` — one file per service module

## AI-agent gotchas
- Agents over-eagerly create classes; require a function-first rule unless DI is needed
- LLMs leak DRF imports (`Response`, `serializers.ValidationError`) into services — block in code review
- `from __future__ import annotations` is mandatory; without it, type aliases of unloaded models crash at import
- Agents forget `update_fields=` and `bulk_*` opportunities; add them as an SDD checklist item
- Human-in-loop checkpoint: any service that issues outbound payments, emails, or destructive deletes must require explicit approval before merge
- Multi-step refactors (view → service) should be one PR per service to keep diffs reviewable

## References
- https://www.dabapps.com/insights/django-models-and-encapsulation/
- https://www.feldroy.com/books/two-scoops-of-django-3-x
- https://www.b-list.org/weblog/2020/mar/16/no-service/ — counterpoint by James Bennett
- https://google.github.io/styleguide/pyguide.html
- https://peps.python.org/pep-3102/
