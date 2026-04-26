# Agent Integration — Django Models

## When to use
- Adding a new model to an existing Django app — agent applies BaseModel/SoftDeleteModel pattern, writes migration, regenerates admin.
- Refactoring an "anemic" model bloated with business logic into thin model + service-layer functions (HackSoft style).
- Audit pass: scan all models for missing `db_index`, missing `related_name`, wrong `on_delete`, weak validators, missing `Meta.constraints`.
- Designing a model with status/state — convert string literals to `TextChoices`/`IntegerChoices`.
- Migrating Django 4.x → 5.x to adopt `db_default` and `GeneratedField` where it pays off.

## When NOT to use
- ORM-less projects (FastAPI + SQLAlchemy, Flask + SQLAlchemy) — wrong patterns; route to SQLAlchemy methodology.
- Migrating *to* a different ORM (peewee, Tortoise, SQLModel) — these conventions don't translate.
- Quick prototype where Django Admin + auto-generated tables are throwaway — adding BaseModel/UUID is over-engineering.
- Reporting/read-only projects backed by views or external warehouses — don't model them as Django tables.

## Where it fails / limitations
- README's `BaseModel` exposes `uid` AND keeps the auto-increment `id`. Agents leak `id` in serializers because the README never says "always serialize `uid`, never `id`". Restate explicitly.
- `SoftDeleteModel` has a real GDPR pitfall (correctly noted in README) but agents will still default to soft-delete for user data unless told. Add an explicit "no soft delete on PII" rule.
- Service-layer pattern uses `user.full_clean()` then `save()` — but `full_clean()` is not called by `save()` automatically. Agents drop `full_clean()` and validation silently disappears.
- `Manager.from_queryset(QuerySet)()` is the right call shape; agents often miss the trailing `()` and create the `Manager` class object, not an instance, leading to confusing errors.
- `GeneratedField` with `db_persist=False` is a virtual column and doesn't work on all backends (SQLite has limited support). Agents will use it on SQLite and migrations will fail in CI.
- README shows partial indexes (`condition=Q(...)`) without warning that they require PostgreSQL. Agents emit them on a MySQL project.
- Soft delete `delete()` calls `save(update_fields=...)` — bypasses `pre_delete`/`post_delete` signals. Agents that hook signals get silent breakage.
- No mention of `objects = ...` ordering when subclassing `SoftDeleteModel` — if a child model redefines `objects`, the alive-only filter is lost. Agents redefine `objects` naively.
- The `clean()` example raises `ValidationError` but DRF/Ninja will not call `clean()` automatically — agents assume "validation is on the model" and skip serializer-level checks.

## Agentic workflow
Three-phase loop per model: (1) **design** — agent proposes the model, listing fields, indexes, FK on_delete, choices, constraints, abstract base, `Meta.ordering`. Human or sonnet reviewer approves before code; (2) **implement + migrate** — agent writes the model, runs `manage.py makemigrations --dry-run`, then `--check` against the current DB; the **migration file is reviewed by a human before `migrate`**; (3) **integrate** — agent updates serializers/schemas, admin, services, factories, and tests. Never auto-run `makemigrations` + `migrate` in one shot — most of the README's gotchas only manifest at migration time.

### Recommended subagents
- `faion-sdd-executor-agent` — picks up a single-model SDD task end-to-end.
- `faion-feature-executor` — sequential gate with `ruff`, `mypy --strict`, `pytest`, and `manage.py makemigrations --dry-run --check`.
- General-purpose subagent restricted to `apps/<domain>/models/`, `apps/<domain>/services/`, `apps/<domain>/tests/`, and the matching `migrations/` folder; deny writes elsewhere.
- `password-scrubber-agent` — sweep settings and fixture files for secrets before commit.

### Prompt pattern
```
Stack: Django 5.x, PostgreSQL, HackSoft styleguide.
Inherit from core.models.BaseModel (uid + timestamps) or SoftDeleteModel (only if non-PII).
Always: explicit related_name, on_delete chosen from {PROTECT, CASCADE, SET_NULL},
TextChoices/IntegerChoices for enums, db_index where queried, Meta.constraints for invariants.
After writing the model: run `manage.py makemigrations --dry-run --check`. Stop on changes.
```

```
Audit pass on apps/<domain>/models.py:
1) flag any FK without related_name or with on_delete=CASCADE on user-referencing tables;
2) flag any CharField(choices=[...]) using raw tuples instead of TextChoices;
3) flag any field used in filter/order_by without db_index or composite Index;
4) propose Meta.constraints for cross-field invariants.
Output a numbered list. Do NOT modify code.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `manage.py makemigrations` / `migrate` / `sqlmigrate` | Migration lifecycle | https://docs.djangoproject.com/en/5.2/topics/migrations/ |
| `manage.py check` / `--deploy` | Static project checks | https://docs.djangoproject.com/en/5.2/ref/checks/ |
| `manage.py shell_plus` (django-extensions) | REPL with auto-imported models | https://django-extensions.readthedocs.io/ |
| `manage.py graph_models` | Generate ER diagram from models | https://django-extensions.readthedocs.io/en/latest/graph_models.html |
| `django-stubs` + `mypy` | Static typing for Django | https://github.com/typeddjango/django-stubs |
| `django-debug-toolbar` / `silk` / `nplusone` | Detect N+1 and slow queries | https://django-debug-toolbar.readthedocs.io/ , https://github.com/jmcarp/nplusone |
| `factory_boy` / `model_bakery` | Test factories for models | https://factoryboy.readthedocs.io/ , https://model-bakery.readthedocs.io/ |
| `django-migration-linter` | Block unsafe migrations in CI | https://github.com/3YOURMIND/django-migration-linter |
| `pytest-django` | pytest integration | https://pytest-django.readthedocs.io/ |
| `ruff` (`DJ` rules) | Django-specific lint | https://docs.astral.sh/ruff/rules/#flake8-django-dj |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| PostgreSQL | OSS | Yes | Required for partial indexes, `GeneratedField(db_persist=True)`, `JSONField` features. |
| Sentry | SaaS | Yes | Captures `ValidationError`, slow ORM queries via performance monitoring. |
| Redis (django-redis) | OSS | Yes | Cache + lock backend for `select_for_update` alternatives. |
| OpenTelemetry | OSS | Yes | `opentelemetry-instrumentation-django` traces ORM calls. |
| pgAnalyze / pgHero | SaaS / OSS | Yes | Index recommendations agents can act on. |
| django-silk | OSS | Yes | Per-request SQL profile; agents can parse JSON exports. |

## Templates & scripts
Pre-commit guard: fail when a model defines an FK without `related_name` or uses raw choices tuples.

```bash
#!/usr/bin/env bash
# scripts/django-model-lint.sh
set -euo pipefail
python - <<'PY'
import ast, pathlib, sys
fails = []
for p in pathlib.Path("apps").rglob("models.py"):
    tree = ast.parse(p.read_text())
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            f = getattr(node.func, "attr", "")
            if f == "ForeignKey":
                kwargs = {kw.arg for kw in node.keywords}
                if "related_name" not in kwargs:
                    fails.append(f"{p}:{node.lineno} ForeignKey missing related_name")
            if f == "CharField":
                for kw in node.keywords:
                    if kw.arg == "choices" and isinstance(kw.value, ast.List):
                        fails.append(f"{p}:{node.lineno} CharField uses raw choices, use TextChoices")
for f in fails: print(f)
sys.exit(1 if fails else 0)
PY
```

For BaseModel/SoftDelete scaffolds, see `templates.md`.

## Best practices
- Always add `related_name` — auto-generated `<model>_set` confuses agents and breaks reverse lookups when models are renamed.
- Index every field used in `filter()`/`order_by()`/`distinct()` paths that hit production traffic; combine into composite indexes when both fields appear together.
- Choose `on_delete` deliberately: `PROTECT` for user/account refs (delete is an event, not silent cascade), `CASCADE` only for child rows that have no meaning without parent, `SET_NULL` for assignees/handlers.
- Wrap long-running migrations behind `RunPython.noop` reverse + a feature flag; agents will write irreversible migrations otherwise.
- Pin DB engine in `Meta` comments when using engine-specific features (partial index, `GeneratedField` persistence).
- Keep models in a `models/` package once you exceed ~3 models per app — avoids merge conflicts.
- Always run `manage.py check --deploy` before merging migration PRs.
- Add `select_related`/`prefetch_related` defaults at the QuerySet/Manager level for the common access pattern, not per-call.

## AI-agent gotchas
- Agents inherit from `models.Model` instead of the project `BaseModel`, breaking `uid`/timestamps consistency. Pin BaseModel in the prompt.
- Agents skip `full_clean()` in services and lose model-level validation. Always require `full_clean()` before `save()` in services.
- Agents call `model.delete()` on a `SoftDeleteModel` thinking it hard-deletes; it soft-deletes. Conversely, they call `hard_delete()` on PII expecting soft-delete. Document the data class on each model.
- Agents add `db_index=True` everywhere "for performance" — bloats writes. Require justification in PR description.
- Agents emit migrations with `--name auto` defaults that are unparseable later. Force `manage.py makemigrations <app> -n descriptive_name`.
- Agents reorder fields in a model to "clean it up" — Django generates pointless `AlterField` migrations. Lock field order in code review.
- Agents add `class Meta: ordering = [...]` deeply, then upstream code paginates by primary key — silently mismatched ordering causes duplicate/skipped rows. Audit `ordering` whenever pagination changes.
- Agents copy `GeneratedField` examples from the README onto SQLite/MySQL projects. Pin the DB engine in the prompt.
- Human-in-loop checkpoint: review every generated migration file. Migrations are forever in production.

## References
- https://docs.djangoproject.com/en/5.2/topics/db/models/
- https://docs.djangoproject.com/en/5.2/topics/db/managers/
- https://docs.djangoproject.com/en/5.2/ref/models/indexes/
- https://docs.djangoproject.com/en/5.2/ref/models/options/
- https://github.com/HackSoftware/Django-Styleguide
- https://docs.djangoproject.com/en/5.2/releases/5.0/
- https://github.com/3YOURMIND/django-migration-linter
- https://django-model-utils.readthedocs.io/
