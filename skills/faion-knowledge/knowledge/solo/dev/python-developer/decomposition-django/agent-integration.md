# Agent Integration — Decomposition (Django)

## When to use
- Django app where `models.py` exceeds ~300 lines or `views.py` exceeds ~200 lines
- Migrating a fat-model codebase to services + selectors layout (HackSoft pattern)
- Splitting a monolithic Django project by bounded context (DDD per-domain apps)
- Preparing a codebase for AI-assisted refactoring — small focused files improve agent reliability
- Onboarding a new team where current `apps/foo/views.py` mixes auth, queries, business logic, and serialization

## When NOT to use
- One-shot scripts, admin command tools, or proof-of-concept apps
- Apps with a single model and ≤5 endpoints — premature decomposition adds friction
- Codebases in maintenance-only mode where churn risk outweighs clarity gain
- Teams without test coverage to validate the refactor — break + freeze is the result

## Where it fails / limitations
- Circular imports explode when `services/` imports models that import signals that import services. Agents miss this until runtime.
- `__init__.py` re-exports get stale silently when adding new service modules; `services/foo.py` exists but is unreachable from `services` package
- Selector functions returning querysets vs lists vs evaluated data — inconsistency leaks `LIMIT 1` calls into N+1 territory
- Migrations: splitting `models.py` into `models/` package requires zero-op migration (rename via `db_table` Meta) — easy to corrupt schema state
- Domain-driven decomposition fights Django's `app_label` constraints; cross-app FKs require explicit `related_name` policy
- Agents propose `core/` apps that grow into a god-app — same problem, different filename
- HackSoft + DRF: serializer.create()/update() temptation to call services from serializers couples the two — skipping the view layer

## Agentic workflow
Run decomposition in tracked phases: agent first emits a refactor plan (file map: old → new) and a migration test asserting `python manage.py check && pytest` stays green. Only after sign-off does the agent execute moves, one model/service at a time, committing per logical unit. A code-review subagent enforces ruff `I` (isort) and import-order rules, and runs `django-test-migrations` to verify migrations are reversible.

### Recommended subagents
- General-purpose subagent — file moves, import rewrites, package `__init__.py` updates
- `faion-feature-executor` — phased plan execution with per-step pytest gate
- `faion-sdd-execution` — quality gates: ruff DJ rules, no circular imports (`pylint --disable=all --enable=cyclic-import`), test coverage delta
- Code-review subagent — reads each PR diff, verifies single-purpose-file rule and that no business logic landed back in views

### Prompt pattern
```
Decomposition plan for apps/orders:
1. Inventory: list (file, line range, responsibility) for models.py, views.py.
2. Output proposed layout: models/, services/, selectors/, views/.
3. Map every existing function/class → new location.
4. List all import sites that need rewriting (grep across repo).
5. Output reversible migration commands + a 1-paragraph rollback plan.
STOP. Do not execute until I approve the plan.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `ruff check --select I,DJ` | Import sorting + Django-specific lint | `pip install ruff` |
| `pyright` / `mypy` | Type checks across split modules catch breakage | `pip install pyright` |
| `import-linter` | Enforce architectural boundaries (`services` cannot import `views`) | `pip install import-linter` |
| `django-test-migrations` | Test forward + backward migration safety | `pip install django-test-migrations` |
| `pylint` (cyclic-import) | Cycle detection | `pip install pylint` |
| `vulture` | Dead-code detection post-refactor | `pip install vulture` |
| `rope` / `bowler` | Programmatic refactors / move-symbol | `pip install rope bowler` |
| `pyproject-flake8` | Same lint config across CI/local | included with ruff |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| HackSoft Django Styleguide | OSS docs | Yes | Reference text for services + selectors patterns |
| Cookiecutter-Django | OSS template | Yes | Generates a layout close to HackSoft for new projects |
| Sentry | SaaS | Yes | Surfaces import-time errors after refactor (post-deploy) |
| Datadog APM | SaaS | Yes | Confirms decomposition didn't tank query-per-view counts |
| GitHub Actions / GitLab CI | SaaS | Yes | Run `import-linter` + `django-test-migrations` per PR |

## Templates & scripts
See `templates.md` for full HackSoft layout, `services/__init__.py` re-exports, and `selectors/` patterns. Inline boundary check via `import-linter`:

```ini
# .importlinter
[importlinter]
root_packages = apps

[importlinter:contract:domain-isolation]
name = Services cannot import views/serializers
type = forbidden
source_modules =
    apps.orders.services
    apps.users.services
forbidden_modules =
    apps.orders.views
    apps.users.views
    apps.orders.serializers
    apps.users.serializers

[importlinter:contract:layered]
name = Layer order
type = layers
layers =
    apps.orders.views
    apps.orders.serializers
    apps.orders.services
    apps.orders.selectors
    apps.orders.models
```

## Best practices
- Move one bounded context at a time; never mix "split models.py" with "rename app" in a single commit
- Re-exports in `__init__.py` are explicit (`from .user_services import user_create`), never `from .user_services import *`
- Keep models thin: properties, simple validators, custom managers — no business logic, no external API calls
- Selectors return iterables (`Iterable[Order]` typed) and never mutate — agents must enforce this in PR review
- Services are keyword-only functions (`def order_create(*, user, items)`) — kills positional-arg drift
- `core/` shared app reserved for true cross-cutting (auth utilities, base mixins); not a dumping ground
- Each new app gets a `CLAUDE.md` describing its bounded context + service inventory — feeds future agent runs
- Coverage rule: services + selectors >90% line coverage; views can be lower because they delegate

## AI-agent gotchas
- Agents copy a function from `views.py` into `services/` and forget to delete the original — duplication compiles
- Imports get rewritten file-by-file; agent finishes one file with broken state. Use `ruff check --fix` after each move and pytest after each batch.
- LLMs love to invent a `helpers.py` or `utils.py` per app — these become the next thing to decompose. Ban early in CLAUDE.md.
- HackSoft's "fat services, thin views" reads as "put everything in services" to LLMs; stress that **read-only** logic goes to selectors, not services
- Agents misuse `transaction.atomic` decorator on every service function; use only when actually composing writes — wraps single-write ops in a no-op
- Migrations after model split: agent runs `makemigrations` and gets a misleading "no changes" — must inspect for `db_table` continuity
- Human-in-loop required when: introducing a new bounded-context app boundary, adding cross-app FKs, splitting `models.py` into `models/` package
- Don't paste the entire app into context — feed the file inventory + the specific module being moved

## References
- HackSoft Django Styleguide: https://github.com/HackSoftware/Django-Styleguide
- Two Scoops of Django (Greenfeld) — decomposition principles
- `import-linter`: https://import-linter.readthedocs.io/
- Cookiecutter-Django: https://cookiecutter-django.readthedocs.io/
- Django app/project layout debate (Mozilla, Lincoln Loop guides): https://docs.djangoproject.com/en/5.0/topics/apps/
- `django-test-migrations`: https://github.com/wemake-services/django-test-migrations
- DDD with Django (Cosmic Python book): https://www.cosmicpython.com/
