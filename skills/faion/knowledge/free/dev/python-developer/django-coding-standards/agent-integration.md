# Agent Integration — Django Coding Standards

Methodology codifies HackSoft + Two Scoops conventions for Django 6.x: services for writes, selectors for reads, thin views, TextChoices for enums, validation in models, project layout under `apps/`, `core/`, `config/`. Use this file when an agent scaffolds a Django app, refactors a fat view, or enforces architectural conventions in a code review.

## When to use
- New Django app — scaffold `models.py`, `services.py`, `selectors.py`, `apis.py`, `serializers.py`, `tests/` per HackSoft layout.
- Refactoring fat views/viewsets — pull business logic into services, query logic into selectors.
- Adding a new domain operation — write the service first, then expose via API/admin/management command.
- Replacing magic strings/numbers with `TextChoices` and `constants.py`.
- Enforcing same-shape pattern across team — admin actions, Celery tasks, management commands all call services.
- CI gate: ruff + mypy + custom architecture rules (import-linter, tach) on PRs.

## When NOT to use
- Single-file Django apps (e.g., `core` utility apps with one helper) — full layered structure is overkill.
- Heavily DRF-generic-view codebases that intentionally rely on `ModelViewSet` defaults — services layer adds friction without clear win unless you're also doing TDD.
- Function-style scripts / management commands that orchestrate multiple services — those *call* services, don't replicate the layout.
- Django CMS / Wagtail apps — their conventions diverge (page tree, blocks); HackSoft doesn't map cleanly.
- Codebases where the team hasn't agreed — imposing this top-down without buy-in produces inconsistent half-migrations.

## Where it fails / limitations
- README's "Selectors return querysets, services mutate" rule is clear but agents conflate them when a function reads-then-writes (most realistic operations).
- No guidance on transactions across services — agents either wrap each service in `atomic()` (deadlock risk) or none (data corruption risk).
- `clean()` for multi-field validation is correct but doesn't fire on `Model.objects.create(...)` unless explicitly called — agents assume otherwise and lose validation.
- Service naming `<entity>_<action>` collides when actions span entities (e.g., `order_apply_coupon` vs `coupon_apply_to_order`).
- TextChoices examples don't show `.label` lookup — agents reach for `dict(STATUS_CHOICES).get(...)` instead.
- README does not cover Django Ninja, Django REST Framework alternatives — agents assume DRF; Ninja-based projects need pattern adaptation.
- No discussion of CQRS-like split when reads/writes diverge significantly (read replicas, materialized views).
- Service layer adds boilerplate; agents auto-generate trivial `def x_create(*, name): return X.objects.create(name=name)` services that add no value.

## Agentic workflow
New app: (1) `python manage.py startapp <name>` under `apps/`, (2) replace generated files with HackSoft skeleton (services.py, selectors.py, apis.py), (3) move app to `apps/<name>` and update `apps.py`'s `name` to `apps.<name>`, (4) register in `INSTALLED_APPS`, (5) write models with `clean()` + `TextChoices`, (6) write services keyword-only with explicit transaction boundaries, (7) write selectors returning explicit queryset shapes, (8) write API view that just calls service/selector + serializes, (9) tests per `django-testing` methodology. Refactor fat view: extract write logic into `services.<entity>_<action>(*, ...)`, extract reads into `selectors.<entity>_<query>(...)`, leave view as auth + serialize + return.

### Recommended subagents
- `faion-software-architect` — Decides layering, when to introduce a new app, transaction boundaries.
- `faion-code-agent` — Default for writing/refactoring services, selectors, models.
- `faion-test-agent` — Tests services in isolation; tests selectors with prepared fixtures.
- `faion-api-developer` — Designs the DRF/Ninja API surface that calls services.
- `faion-feature-executor` — Sequential per-task feature build using this layout.
- `faion-sdd-execution` — Quality gates ensure refactor PRs don't bypass services from views.

### Prompt pattern

Scaffold a new app:

```
Create app apps/<name>/ per
free/dev/python-developer/django-coding-standards/README.md.
Files:
  - models.py — model with TextChoices status, clean() validation, BaseModel from core.
  - services.py — keyword-only functions: <entity>_create, <entity>_update, <entity>_archive.
    Each wrapped in transaction.atomic() at boundary; emit Celery .delay AFTER commit (transaction.on_commit).
  - selectors.py — read functions returning explicit QuerySets with select_related/prefetch_related.
  - apis.py — DRF views (or Ninja) calling service/selector and serializing.
  - serializers.py — DRF serializers split into Input / Output.
  - admin.py — minimal ModelAdmin with list_display, search_fields.
  - tests/ — test_models, test_services, test_selectors, test_apis (factories registered).
  - urls.py — wired into config/urls.py.
Constants in constants.py. Cross-app imports aliased.
```

Refactor fat view:

```
Refactor apps/<app>/views.py::<view> per
free/dev/python-developer/django-coding-standards/README.md.
Steps:
  1. Identify write logic → extract to services.py::<entity>_<action> (keyword-only).
  2. Identify queries → extract to selectors.py::<entity>_<query>.
  3. View becomes: parse input (serializer.is_valid), call service/selector, serialize output.
  4. Move transaction.atomic() into the service.
  5. Move Celery .delay into transaction.on_commit hook in service.
  6. Tests for service + selector independently; view test asserts wiring + status codes.
Run pytest; show coverage diff. No behavior change.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `ruff check` | Lint (E/F/I/B/UP/N/S/C4/PT/DJ rules) | https://docs.astral.sh/ruff |
| `ruff format` | Replaces black | same |
| `mypy --strict` + `django-stubs` | Type-check Django ORM | https://github.com/typeddjango/django-stubs |
| `pyright` | Microsoft type checker (faster IDE) | https://microsoft.github.io/pyright |
| `import-linter` | Enforce layer boundaries (apps independent of each other) | https://import-linter.readthedocs.io |
| `tach` | Lighter alt to import-linter | https://github.com/gauge-sh/tach |
| `django-axes` | Brute-force protection (cited in security stack) | https://django-axes.readthedocs.io |
| `django-extensions` | `shell_plus`, `runserver_plus`, model graph generator | https://django-extensions.readthedocs.io |
| `django-debug-toolbar` | Dev profiling, query inspection | https://django-debug-toolbar.readthedocs.io |
| `nplusone` | Detect N+1 queries automatically | https://github.com/jmcarp/nplusone |
| `django-silk` | Request profiler | https://github.com/jazzband/django-silk |
| `pip-audit` / `safety` | Dependency vulnerability scan | https://pypi.org/project/pip-audit |

## Services & apps
| Service | Type | Agent-friendly? | Notes |
|---------|------|-----------------|-------|
| Sentry | SaaS APM | Yes — Django integration | `sentry_sdk.init(...DjangoIntegration())` |
| Datadog APM | SaaS | Yes | `ddtrace-run gunicorn ...` |
| Honeycomb | SaaS observability | Yes | OTel + Django middleware |
| AWS RDS / Aurora | SaaS PG | Yes | psycopg3 driver |
| Heroku / Render / Railway | SaaS PaaS | Yes — buildpack auto-detects Django | Good for solopreneur deploys |
| Fly.io | SaaS PaaS | Yes — `fly launch` | Region-per-region scaling |
| GitHub Codespaces | Dev env | Yes — `.devcontainer/` | Reproducible environments |
| pre-commit.ci | CI hosted hooks | Yes | Auto-fix PRs |

## Templates & scripts

See `templates.md` for full app skeleton. Add this layered-arch lint contract for `import-linter` (≤45 lines):

```ini
# .importlinter — enforce layered architecture per HackSoft.
[importlinter]
root_packages =
    apps
    core
    config

[importlinter:contract:apps-independent]
name = Apps must not import from each other directly
type = independence
modules =
    apps.users
    apps.orders
    apps.catalog
ignore_imports =
    apps.* -> apps.*.models  # FK strings only via apps.get_model

[importlinter:contract:layered]
name = Layered: apis -> services -> selectors / models; never the reverse
type = layers
layers =
    apps.*.apis
    apps.*.services
    apps.*.selectors
    apps.*.models

[importlinter:contract:no-views-write]
name = Views must not import django.db.transaction directly
type = forbidden
source_modules = apps.*.apis apps.*.views
forbidden_modules = django.db.transaction
```

## Best practices
- **Keyword-only service args** — `def order_create(*, user, items):`. Forces call sites to be readable, prevents arg-order bugs at refactor time.
- **One transaction boundary per service.** `with transaction.atomic(): ...` at the top of the service body. Don't nest from views.
- **`transaction.on_commit(lambda: task.delay(id))`** for Celery dispatch from services — prevents tasks running on rolled-back data.
- **Selectors return querysets, not lists** — caller decides materialization. Apply `.select_related()` / `.prefetch_related()` at selector level.
- **Validation lives in `Model.clean()` for multi-field rules**, in field validators for single-field rules. Always call `full_clean()` in services if you bypass forms/serializers.
- **`TextChoices` over raw strings** — `OrderStatus.PENDING` not `"pending"`. Migrations stay friendly to renames.
- **`constants.py` for thresholds**, not hardcoded literals scattered across the app.
- **Same pattern everywhere**: admin actions, management commands, Celery tasks, views all call services. No business logic in views or signals.
- **Signals for cross-cutting only** — auditing, denormalized cache invalidation. Never put core domain logic in signals.
- **Ban direct cross-app imports** with `import-linter` independence contract; force string FKs and `apps.get_model`.
- **`select_related` for FKs / OneToOne, `prefetch_related` for M2M / reverse FK / GFK**. Don't blanket apply — measure.

## AI-agent gotchas
- **`Model.objects.create()` skips `clean()`** — only `Model.full_clean()` then `save()` runs validation. Agents trust `clean()` to fire and ship invalid data.
- **`transaction.atomic()` inside an already-atomic block** is a savepoint, not a no-op — exception inside re-raises but only rolls back the inner block. Subtle when nested across services.
- **`select_related` on nullable FK** loads NULLs as outer joins — agents profile and miss the join cost.
- **Service that returns a model and a list of side effects** — agents return tuples; better to return the model and emit events via `transaction.on_commit`.
- **Services calling other services**: nested calls are fine, but each starts its own transaction unless the outer wraps explicitly. Agents miss this and lose atomicity.
- **`TextChoices` integer values** vs string values — once chosen, can't switch without data migration.
- **Mixing service signature styles** (some keyword-only, some positional) breaks `inspect.signature`-based tooling (Celery autodiscovery, FastAPI-style DI).
- **`apps.get_model('users', 'User')` returns `Any`** — chains of operations on it lose type narrowing entirely.
- **Generic DRF `ModelViewSet`** auto-creates the full CRUD without a service — agents add a service after the fact and end up with parallel paths.
- **Selector returning `.first()` or `.get()`** — error semantics differ; pick consistently per project (return `None` vs raise `DoesNotExist`).
- **`signals.post_save` doing real work** breaks tests that bypass the model layer (e.g., bulk_create); agents debug for hours.
- **Importing a model at module level in `services.py` for an app whose `models.py` imports `services.py`** — circular at import time. Use `apps.get_model` or string FK.
- **`ForeignKey(..., on_delete=CASCADE)`** can wipe data agents didn't expect; default to `PROTECT` or `SET_NULL` and only choose CASCADE deliberately.

## References
- README: `./README.md`
- Sibling: `../django-imports/`, `../django-quality/`, `../django-testing/`, `../django-models/`, `../django-api/`
- HackSoft Django Styleguide: https://github.com/HackSoftware/Django-Styleguide
- Two Scoops of Django: https://www.feldroy.com/two-scoops-of-django
- Django docs (6.0): https://docs.djangoproject.com/en/6.0/
- django-stubs: https://github.com/typeddjango/django-stubs
- import-linter: https://import-linter.readthedocs.io
- nplusone: https://github.com/jmcarp/nplusone
- django-silk: https://github.com/jazzband/django-silk
- HackSoft service patterns: https://github.com/HackSoftware/Django-Styleguide#services
- HackSoft selectors: https://github.com/HackSoftware/Django-Styleguide#selectors
