# Agent Integration — Django Models

## When to use
- Generating a new Django app's `models/` package using the BaseModel (UUID + timestamps) pattern.
- Refactoring legacy ad-hoc models to the canonical `BaseModel` + `Meta.indexes` shape.
- Adding ForeignKey relations and choosing the right `on_delete` policy.
- Introducing per-app `constants.py` with `TextChoices` enums.
- Auto-generating migrations after model edits and reviewing them for destructive changes.
- Adding Django 5 `db_default` / generated fields on existing schemas.

## When NOT to use
- Async ORM workflows (`.asave()`, `.aget()`) — README does not cover async manager patterns.
- Multi-database routing, sharding, or replicas — out of scope.
- Heavy use of `JSONField` / `ArrayField` for document-style data — pattern assumes relational shape.
- ML feature stores or analytical schemas — wrong abstraction.
- Tenant isolation (`django-tenants`, schema-per-tenant) — needs additional methodology.

## Where it fails / limitations
- BaseModel uses both an integer PK (implicit `id`) AND a `uid = UUIDField(unique=True)` — agents often forget which to expose externally; the README does not state the rule. Pin in prompt.
- ForeignKey examples don't show `related_name` or `related_query_name`; agents leave them as defaults, leading to clashing reverse accessors when models share a parent.
- `Meta.indexes` example is single-column composite; agents copy-paste without revisiting whether a partial / functional index would be better.
- Django 5 `db_default=Now()` requires Postgres 12+ / SQLite 3.38+; agents won't check the project's DB and may emit migrations that fail on prod.
- No discussion of soft-delete, audit log, or row-level history — agents will invent inconsistent implementations.

## Agentic workflow
Treat model changes as `propose-diff → migration-review → test`. Have one subagent draft the model edit, a second run `manage.py makemigrations --dry-run --check` and inspect the auto-generated migration file for destructive ops (`RemoveField`, `AlterField` on PKs, `RenameField`). A third subagent writes/updates a pytest fixture covering the new field's choices and constraints. Never let a single agent both edit models and generate migrations without a review gate.

### Recommended subagents
- `faion-sdd-executor-agent` — for SDD-tracked model tasks (spec → design → impl → migration → test).
- General-purpose subagent restricted to `apps/<name>/models/` and `apps/<name>/constants.py` — narrow blast radius.
- `password-scrubber-agent` — sweep before commit if seed data or fixtures might leak credentials.

### Prompt pattern
```
You are editing apps/<app>/models/<model>.py.
Constraints: extend BaseModel (UUID+timestamps); FK on_delete must be explicit; choices live in apps/<app>/constants.py as TextChoices.
After edit: run `python manage.py makemigrations --dry-run` and paste the planned migration.
Stop and ask before running with --no-dry-run if any field is removed/renamed.
```

```
Add an index for the query <pattern>. Use Meta.indexes; name it <app>_<model>_<cols>_idx.
Do not drop other indexes. Output the migration plan only.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `python manage.py makemigrations` | Generate migration from model diff | https://docs.djangoproject.com/en/stable/ref/django-admin/#makemigrations |
| `python manage.py sqlmigrate <app> <num>` | Preview SQL of a migration | docs.djangoproject.com |
| `python manage.py showmigrations` | Status of applied migrations | docs.djangoproject.com |
| `django-extensions` `graph_models` | Render ER diagram from models | https://django-extensions.readthedocs.io/ |
| `django-migration-linter` | Detect destructive / blocking migrations | https://github.com/3YOURMIND/django-migration-linter |
| `ruff` (with `DJ` rules) | Django-specific lint rules | https://docs.astral.sh/ruff/rules/#flake8-django-dj |
| `mypy` + `django-stubs` | Static typing for ORM | https://github.com/typeddjango/django-stubs |
| `factory_boy` | Test factories per model | https://factoryboy.readthedocs.io/ |
| `pytest-django` | DB fixtures, transactions | https://pytest-django.readthedocs.io/ |
| `pgcli` / `psql` | Inspect resulting schema | https://www.pgcli.com/ |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Postgres (managed: RDS, Cloud SQL, Neon, Supabase) | SaaS | Yes | Default; supports `db_default(Now())`. |
| `django-simple-history` | OSS | Yes | Audit trail per model — drop-in mixin. |
| `django-safedelete` | OSS | Yes | Soft-delete missing from base methodology. |
| `django-model-utils` | OSS | Yes | `TimeStampedModel`, `StatusModel` — orthogonal to BaseModel. |
| Sentry / Rollbar | SaaS | Yes | Catch ORM exceptions in handlers. |
| Atlas / dbmate | OSS | Caution | Alternative migration drivers — only if leaving Django migrations entirely. |

## Templates & scripts
See `templates.md` and `examples.md`. One useful pre-commit script — refuses commits that touch a model without producing a migration:

```bash
#!/usr/bin/env bash
# scripts/check-migrations.sh
set -euo pipefail
changed=$(git diff --cached --name-only -- 'apps/*/models/*.py' 'apps/*/models.py' || true)
[[ -z "$changed" ]] && exit 0
out=$(python manage.py makemigrations --dry-run --check 2>&1) || {
  echo "Models changed but migration not staged:"; echo "$out"; exit 1
}
```

## Best practices
- Always supply `on_delete=` explicitly — `PROTECT` for "don't lose data", `CASCADE` only for owned children, `SET_NULL` for optional refs.
- Add `related_name=` on every FK; if a reverse accessor is not needed, use `related_name='+'`.
- Put `Meta.ordering` only on small / paginated models; on large tables it adds an `ORDER BY` that hurts performance.
- Combine `Meta.indexes` with a real EXPLAIN against representative data — don't add indexes speculatively.
- Use `models.UniqueConstraint(fields=[...], name='...')` over `unique_together` (deprecated path).
- Use `TextChoices` for fixed enums; reference them through a constants module so admin/forms/serializers all share one source.
- Never edit applied migration files; create a new migration to alter or drop instead.

## AI-agent gotchas
- Agents may switch the PK to UUID by replacing `id` with `uid` — the README's pattern keeps integer PK + indexed UUID. Re-state this in the prompt or it will produce an irreversible migration.
- `auto_now=True` / `auto_now_add=True` are silently ignored by `bulk_create` and `update()`. Agents writing batch jobs often miss this.
- `db_default` and `default` look interchangeable but produce different migrations and apply at different layers (DB vs Python). Agents conflate them.
- LLMs love adding `unique=True` on `email` / `username` without a `db_index=False` — Postgres makes uniqueness an index, so explicit `db_index=True` is redundant; agents add both.
- Human-in-loop checkpoint: review every generated migration's `operations = [...]` before `migrate`. Especially watch for `AlterField` that changes column type — Postgres may rewrite the table.
- Agents often add new choice values to `TextChoices` and forget the migration — choices are stored in DB enums only if you opt into them; otherwise just code-level.
- Do not let an agent run `migrate --fake` autonomously; it desyncs the migration graph from schema.

## References
- https://docs.djangoproject.com/en/stable/topics/db/models/
- https://docs.djangoproject.com/en/stable/ref/models/fields/
- https://docs.djangoproject.com/en/5.0/releases/5.0/
- https://docs.djangoproject.com/en/stable/topics/migrations/
- https://github.com/3YOURMIND/django-migration-linter
- https://docs.astral.sh/ruff/rules/#flake8-django-dj
