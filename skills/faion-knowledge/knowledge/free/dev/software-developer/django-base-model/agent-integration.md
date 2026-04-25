# Agent Integration — Django Base Model Pattern

## When to use
- Bootstrapping a new Django project: define `BaseModel` with `uid: UUIDField`, `created_at`, `updated_at` and have every domain model inherit.
- Adding API surfaces that must never expose auto-increment primary keys (compliance, enumeration-attack hardening).
- Refactoring legacy models to add audit timestamps without changing PK semantics (UUID becomes a secondary unique index).
- Generating REST/GraphQL schemas where the public id is `uid` (UUID) and the DB still uses integer PK for join performance.

## When NOT to use
- Internal-only models you never expose (e.g., M2M through-tables, intermediate analytics rollups) — extra UUID column is dead weight.
- Read-replica DBs where every extra index slows replication.
- Models inheriting from third-party abstract bases (django-mptt, django-polymorphic) that already define their own PK/timestamp scheme — risk of MRO surprises.
- Tables in the multi-millions of rows where adding a UUID column requires an online migration plan you don't have time to implement.

## Where it fails / limitations
- UUIDv4 has poor B-tree index locality; on InnoDB/Postgres heavy inserts hot-spot. Use UUIDv7 (time-ordered) for high-write tables — `uuid.uuid4` from this README is suboptimal at scale.
- `db_index=True` on UUID adds an index per-table; on dozens of tables the cumulative cost is real.
- `ordering = ['-created_at']` at base-model level forces every queryset to sort, which kills planner perf when devs forget to override.
- `auto_now_add` + `auto_now` rely on Python-side time at insert/save — race windows in distributed systems differ from DB `NOW()` (use DB defaults if you care about strict monotonicity).
- Inheriting from `BaseModel` and adding `Meta.ordering` in child silently overrides — unless you set `Meta(BaseModel.Meta)` and call `super`.
- `editable=False` on uid prevents the field appearing in admin forms but not in DRF serializers; agents often expose it as writable by accident.

## Agentic workflow
A code-writing agent always extends `BaseModel` for new models and runs `makemigrations --dry-run` first to verify schema delta. A code-review agent walks `apps/*/models.py` AST and flags any class inheriting from `models.Model` directly that should inherit from `BaseModel`. A migration-review agent inspects each generated migration for index changes (UUID indexes are expensive on existing tables) and gates on a manual approval before deploying. APIs use `lookup_field = "uid"` in DRF viewsets so URLs use UUIDs not PKs.

### Recommended subagents
- `faion-sdd-executor-agent` — owns model creation tasks; constitution.md should include "every domain model extends BaseModel".
- A purpose-built `model-auditor` subagent — scans `models.py` files, ensures inheritance, ensures `Meta.indexes` & `db_table` set.
- A `migration-reviewer` subagent — runs `makemigrations --check` in PRs, summarizes new indexes/columns/SQL.
- `faion-feature-executor` — sequential gating: write model → migration → test → review.

### Prompt pattern
```
Add a new model <Name> in apps/<app>/models.py:
- Inherit from core.models.BaseModel.
- Fields: <list>.
- Add Meta.db_table, Meta.indexes for query patterns.
- Output the model + the migration + a test that creates one.
- Confirm uid is read-only in the DRF serializer.
```
```
Audit apps/*/models.py. List every class that:
(a) inherits models.Model directly (should be BaseModel),
(b) overrides Meta without inheriting BaseModel.Meta,
(c) exposes pk in DRF serializer fields.
Output as JSON list of (file, class, issue).
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `python manage.py makemigrations --dry-run` | Preview schema deltas | Django built-in |
| `python manage.py sqlmigrate <app> <num>` | See raw SQL before apply | Django built-in |
| `django-extensions` `graph_models` | ERD diagrams from BaseModel inheritance | `pip install django-extensions` |
| `django-debug-toolbar` | Detect N+1 / index misuse on uid lookups | `pip install django-debug-toolbar` |
| `factory_boy` / `pytest-factoryboy` | Generate BaseModel subclass instances | `pip install factory_boy pytest-factoryboy` |
| `django-stubs` (mypy plugin) | Type-check model inheritance | `pip install django-stubs` |
| `pgcli` / `psql` | Inspect index size on prod-like data | `pip install pgcli` |
| `pgmigrate` / `django-pg-migrations` | Online schema migration helpers | https://github.com/yandex/pgmigrate |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| GitHub Actions | SaaS | Yes | Run `makemigrations --check` in PR gate. |
| pganalyze | SaaS | Yes | Surfaces UUID-index pathology and write hotspots. |
| Datadog DBM / Honeycomb | SaaS | Yes | Observe slow queries by `uid` vs `id`. |
| Strawberry / Graphene | OSS | Yes | GraphQL — map `uid` to `ID` scalar. |
| DRF | OSS | Yes | `lookup_field='uid'`, `lookup_url_kwarg='uid'`. |

## Templates & scripts
See `templates.md`. Inline upgrade-to-UUIDv7 (when v4 hot-spots become a problem):

```python
# core/models.py — upgrade path: time-ordered UUIDv7 for new rows
import uuid_utils  # pip install uuid-utils
from django.db import models

def uuid7() -> uuid_utils.UUID:
    return uuid_utils.uuid7()

class BaseModel(models.Model):
    uid = models.UUIDField(default=uuid7, editable=False, unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        get_latest_by = "created_at"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{type(self).__name__}({self.uid})"
```

```python
# tests/test_base_model.py
import pytest
from apps.users.models import User

@pytest.mark.django_db
def test_user_has_uid_and_timestamps():
    u = User.objects.create(email="x@y.z", name="x")
    assert u.uid is not None
    assert u.created_at and u.updated_at
    assert u.created_at <= u.updated_at
```

## Best practices
- Always abstract: `abstract = True` in BaseModel.Meta. Otherwise Django creates a redundant table.
- Index `created_at` (you'll filter on it constantly); UUID is unique-indexed already.
- Store integer `id` as PK for joins; UUID `uid` as the public identifier. Don't make UUID the PK unless you've measured.
- DRF: `lookup_field = "uid"`, `lookup_url_kwarg = "uid"`, and `Meta.fields` exclude `id`.
- Admin: use `readonly_fields = ('uid', 'created_at', 'updated_at')`.
- For high-write tables (events, logs), prefer UUIDv7 (`uuid_utils.uuid7()`) over v4 — index locality matters at scale.
- Keep `BaseModel.Meta.ordering` minimal; some queries (analytics) shouldn't pay sort cost — override at child level.
- Define `__str__` on every model (Base provides default); `repr` for debugging.
- Pair with `django-simple-history` or audit-log app if you need full history beyond `updated_at`.
- Consider a `BaseSoftDeletableModel(BaseModel)` for soft-delete patterns; don't shove `deleted_at` into the global base.

## AI-agent gotchas
- LLMs forget `class Meta: abstract = True` and ship a real `BaseModel` table — caught by `makemigrations` but only if the agent actually runs it. Make it a CI gate.
- LLMs override `Meta` in child classes without `class Meta(BaseModel.Meta)`, losing ordering/indexes. Lint with a custom AST check or `django-stubs`.
- LLMs expose `id` (PK) and `uid` both in DRF — defeating the purpose of UUID. Audit serializers explicitly.
- LLMs use `default=uuid.uuid4()` (called once at import time, all rows get same UUID) instead of `default=uuid.uuid4` (callable). This is a common copy-paste bug. Catch with a unit test that creates 2 rows.
- LLMs apply `BaseModel` to through-tables and intermediate models, ballooning index count. Rule: only domain entities, not link tables.
- Migration squash: agents squashing migrations sometimes drop the UUID `unique=True` constraint and re-add without backfilling — corrupting prod. Never auto-squash.
- Time-zone bugs: `auto_now_add` returns aware/naive depending on `USE_TZ`. Agents writing tests with `datetime.now()` (naive) get inequality errors.
- DRF `URLPathRouter` defaults to PK lookup; agent must explicitly switch to UUID lookup or the API uses `id` despite all the model effort.
- UUIDs in URLs are 36 chars — agents writing tests with hardcoded UUIDs sometimes truncate them; use factory_boy fixtures to generate fresh UUIDs.

## References
- https://docs.djangoproject.com/en/stable/topics/db/models/#abstract-base-classes — official abstract model docs
- https://docs.djangoproject.com/en/stable/ref/models/fields/#uuidfield — UUIDField reference
- https://uuid7.com/ — UUIDv7 spec & rationale
- https://www.percona.com/blog/store-uuid-optimized-way/ — UUID storage perf in MySQL/Postgres
- https://github.com/HackSoftware/Django-Styleguide — recommends BaseModel pattern
- https://realpython.com/manage-multiple-django-settings/ — adjacent: settings layout for multi-env
- https://django-extensions.readthedocs.io/en/latest/graph_models.html — model graph for review
