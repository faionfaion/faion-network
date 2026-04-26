# Agent Integration — Django Coding Standards

## When to use
- Bootstrapping a new Django app and wiring `apps/`, `core/`, `config/settings/{base,development,production}.py` skeleton.
- Refactoring a Django repo where business logic has metastasized into views or model save methods.
- Code-review subagent enforcing the "fat services, thin views" rule on every PR.
- Onboarding a multi-app project: agents need a deterministic import-aliasing convention to stop circular imports.
- Generating service-layer scaffolds + matching unit tests from a feature spec.

## When NOT to use
- Single-file Django scripts, management commands that are genuinely 10 lines.
- Async-first stacks (FastAPI/Litestar) — patterns here assume Django request-response and ORM transactions.
- Greenfield prototypes where you want speed over structure for the first day.
- Heavy DDD / hexagonal architecture projects — those need a richer pattern set than this baseline.

## Where it fails / limitations
- Doesn't address Django Channels / async views — the service-layer pattern needs adaptation for `async def`.
- Service functions can swell into "god services" without further decomposition (use cases + repositories).
- `update_fields=[...]` discipline is fragile — easy for an agent to forget when adding a new column.
- The `from apps.x import models as x_models` alias rule fights IDE auto-import; agents need explicit prompting.
- Views vs ViewSets — guide implies APIView style; DRF ViewSet projects need a parallel example.

## Agentic workflow
Use a setup subagent to lay down the `config/`, `apps/`, `core/` tree and `pyproject.toml` ruff config in one pass; then use a feature subagent that generates `models.py` → `services/<feature>.py` → `views/<feature>.py` → `serializers.py` in dependency order. A reviewer subagent enforces: no `Model.objects` calls inside views, no cross-app `from apps.x.models import` (only aliased), every service function has type hints + docstring + `update_fields` on save.

### Recommended subagents
- `faion-sdd-executor-agent` — runs the spec→implementation cycle with quality gates (ruff, pytest, coverage).
- A `django-reviewer` subagent (custom) — single responsibility: grep for anti-patterns, return blocking findings.
- `password-scrubber-agent` — sanity check for accidentally hardcoded credentials in `settings/development.py`.

### Prompt pattern
```
Implement feature <X> in app `<app>`. Constraints:
1. Business logic ONLY in `apps/<app>/services/<feature>.py`.
2. View calls service; never the ORM directly.
3. Cross-app imports use alias: `from apps.users import models as user_models`.
4. Every service function: type hints, keyword-only args after `*`, docstring with Raises.
5. Every `.save()` includes `update_fields`.
```

```
Review diff. Flag: ORM calls in views/, bare except, magic strings (must be TextChoices), missing update_fields, cross-app non-aliased imports.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `ruff` | Lint + format (replaces black/isort/flake8) with `DJ` ruleset | https://docs.astral.sh/ruff/rules/#flake8-django-dj |
| `mypy` + `django-stubs` | Static type checking with Django plugin | https://github.com/typeddjango/django-stubs |
| `django-upgrade` | Auto-rewrite to current Django idioms | https://github.com/adamchainz/django-upgrade |
| `djhtml` | Format Django templates | https://github.com/rtts/djhtml |
| `pip-audit` / `safety` | Dependency CVE scan | https://pypi.org/project/pip-audit/ |
| `python manage.py check --deploy` | Built-in production audit | Django docs |
| `bandit` | Python security linter | https://bandit.readthedocs.io |
| `pre-commit` | Hook orchestrator | https://pre-commit.com |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Sentry | SaaS | yes | Capture `ValidationError` stack traces from services; agents query via `sentry-cli`. |
| GitHub Actions | SaaS | yes | Matrix run of `ruff`, `mypy`, `pytest` on every PR. |
| readthedocs / mkdocs-material | OSS | yes | Render service-layer docstrings into reference docs. |
| CodeRabbit / Sourcery | SaaS | yes | AI review augments human reviewer subagent. |
| Cookiecutter Django | OSS | yes | Project template encoding many of these standards out of the box. |

## Templates & scripts
See `templates.md` for `services/<feature>.py`, `views/<feature>.py`, `constants.py` skeletons. Inline ruff config aligned with this methodology:

```toml
# pyproject.toml
[tool.ruff]
target-version = "py311"
line-length = 100

[tool.ruff.lint]
select = ["E", "F", "I", "B", "UP", "SIM", "DJ", "T20", "RUF", "PT"]
ignore = ["E501"]

[tool.ruff.lint.isort]
known-first-party = ["apps", "core", "config"]
section-order = ["future", "standard-library", "third-party", "first-party", "local-folder"]

[tool.ruff.lint.per-file-ignores]
"**/migrations/*.py" = ["E", "F", "UP"]
"**/tests/*.py" = ["S101"]  # allow assert
```

## Best practices
- Settings split: `base.py` is the only file with secrets-free defaults; `development.py`/`production.py` only override. Never import the other way.
- `core/models.py` defines `BaseModel(TimeStampedModel, UUIDPrimaryKeyModel)`; every domain model inherits from it — agents can rely on `created_at`/`updated_at` being present.
- Service function returns the entity, never an HTTP `Response`. Keeps services callable from management commands, Celery tasks, tests.
- Use `Model.objects.select_for_update()` inside `transaction.atomic()` for state transitions (e.g., `activate_user_item`).
- Keep `apps/<app>/api/` separate from `apps/<app>/admin.py` and `apps/<app>/services/` — three different consumers of the same models.
- TextChoices with explicit values (`'pending'`) not auto values; lets you reorder enum without DB churn.
- Forbid `from django.contrib.auth.models import User` — always `get_user_model()` or `settings.AUTH_USER_MODEL`. Easy LLM mistake.

## AI-agent gotchas
- LLMs love putting validation in `Model.clean()` — fine for forms, useless for DRF API flows. Steer to serializer + service.
- When generating `serializers.py`, agents include `password` in `Meta.fields` and forget `extra_kwargs = {'password': {'write_only': True}}`. Add to prompt.
- `request.user` references in services break testability — pass `user: User` explicitly.
- Agents will silently catch `Exception:` on `Model.objects.get()` instead of `Model.DoesNotExist`. Lint with `B902`/custom rule or a reviewer pass.
- Migrations are agent-blind: prompt must say "if a model field changed, run `python manage.py makemigrations <app>` and include the migration file in the diff".
- Human-in-loop: review every new migration manually before merge; agents can produce data-loss migrations (e.g., dropping a column they "thought" was unused).
- Beware `@transaction.atomic` decorator on a function that also enqueues a Celery task — task fires before commit. Use `transaction.on_commit(lambda: task.delay(...))`.

## References
- https://docs.djangoproject.com/en/stable/ — Django docs
- https://www.feldroy.com/books/two-scoops-of-django-3-x — Two Scoops of Django (services/forms patterns)
- https://github.com/HackSoftware/Django-Styleguide — HackSoft Django Styleguide (the closest published equivalent of this methodology)
- https://docs.astral.sh/ruff/rules/#flake8-django-dj — `DJ` ruleset reference
- https://django-stubs.readthedocs.io/ — typing for Django
- https://github.com/cookiecutter/cookiecutter-django — opinionated template
