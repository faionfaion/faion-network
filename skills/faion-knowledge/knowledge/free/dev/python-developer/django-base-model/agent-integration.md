# Agent Integration — Django Base Model Pattern

## When to use

- Bootstrapping a new Django project: define `BaseModel`, `TimestampMixin`, `SoftDeleteMixin`, manager/queryset patterns once at the start.
- Refactoring a legacy Django app where every model duplicates `created_at`, `updated_at`, ad-hoc soft-delete flags, or auto-increment IDs leak through APIs.
- Adding UUIDs to public APIs without rewriting primary keys (the `uid` separate-field pattern).
- Introducing soft-delete to a domain that needs an "undo" (orders, posts, accounts) — done as one migration plus manager swap.
- Adding audit trail (`django-simple-history`) to compliance-relevant models.
- Multi-tenant SaaS migration: introducing `TenantAwareModel` + middleware-driven tenant scoping.
- Code review of new models: ensuring they inherit from the right base, use the right `on_delete`, and don't reinvent timestamps.

## When NOT to use

- Tiny one-off scripts or admin commands that don't define new models.
- Models for ephemeral data (cache, signed tokens, throwaway joins) where timestamps and soft delete add noise.
- Tables managed outside Django (`managed = False` for legacy DB views) — the base model's `Meta.abstract = True` doesn't combine cleanly with `managed = False`.
- Performance-critical analytical tables where every byte counts; adding a 16-byte UUID + indexes per row is wasteful.
- When introducing PostgreSQL UUID v7 / k-sortable IDs — the README's UUID v4 advice is partially obsolete; reassess before applying.
- Mixing this pattern in a repo that already standardised on `django-model-utils`'s `TimeStampedModel` etc. — pick one set of bases.

## Where it fails / limitations

- **UUID v4 + clustered PK** = index fragmentation on Postgres/MySQL (the README warns but agents still skip the warning). Default `id` PK + separate indexed `uid` column is the safer compromise; UUID-as-PK only after you've proved you need it.
- **Soft delete + `unique=True`** is hard. A `deleted_at IS NULL` partial unique index is needed; agents that just add `unique=True` will hit constraint violations after a "delete" + recreate.
- **Soft-delete + reverse relations + cascading** silently breaks: child rows with `on_delete=CASCADE` get hard-deleted even when the parent is soft-deleted. Either override `delete()` deeply or rethink with `on_delete=PROTECT/SET_NULL`.
- **Multi-manager misuse.** `objects = SoftDeleteManager()` makes Django pick `objects` as default; admin screens, generic views, `dumpdata` all silently exclude soft-deleted rows. `all_objects` must be the second manager *and* the project must opt into it where needed.
- **TenantManager via thread-local middleware** breaks Celery/cron jobs that don't run inside the request cycle. Tasks must explicitly `with tenant_context(tenant): …` or queries leak across tenants.
- **GeneratedField in SQLite** does not support `db_persist=True`; cross-DB code requires `db_persist=False` on SQLite or DB-specific overrides.
- **`db_default=Now()`** ignores Django's `auto_now_add` and only fires on direct SQL inserts; bulk-create paths bypass it.
- **`HistoricalRecords(inherit=True)`** balloons table count (one history table per child); on a 100-model project that's 100 extra tables.
- **Mixin order matters.** Putting `SoftDeleteMixin` after `TimestampMixin` in some setups masks the `delete()` override. Put behaviour-overriding mixins first.

## Agentic workflow

Drive base-model adoption as a sequence of typed migrations: (1) introduce `BaseModel` and mixins under `core/models.py`, (2) migrate one app at a time, generating `add_uid` + `backfill_uid` + `make_uid_unique` migrations, (3) flip APIs to expose `uid` instead of `id`, (4) finally introduce soft-delete only where there's a product-level "undo" requirement. Validate every step with `python manage.py check`, `makemigrations --dry-run`, and a regression test that loads via fixture and checks public API surface. The agent never rewrites a model in place — always migrate via a Django data migration with a backfill.

### Recommended subagents

- `faion-python-developer` — Owns Django model code; produces `core/models.py`, mixins, manager classes, and per-app migrations.
- `faion-software-architect` — Decides which mixins apply per domain (which models need soft-delete, audit, tenant scoping); records as ADRs.
- `faion-backend-developer` — Validates ORM behaviour, FK cascades, query plans (`EXPLAIN`), and partial-index design for soft-delete uniqueness.
- `faion-sdd-executor-agent` — Runs the migration sequence as SDD tasks with explicit gates: `manage.py migrate --plan` clean, tests green, no regression in API responses.
- `faion-code-quality` — Ensures new models inherit the chosen base; flags rogue `created_at = DateTimeField(auto_now_add=True)` duplications at review.
- General-purpose `Task` subagent — Runs the per-app migration generation when the pattern is mechanical.

### Prompt pattern

Generate a base-model migration:

```
For app "<app>", apply BaseModel pattern:
1. Add nullable `uid = UUIDField(default=uuid.uuid4)` migration.
2. Data migration to backfill nulls.
3. Migration making `uid` non-null + unique + db_index=True.
4. Update model to inherit BaseModel from core.models.
Output: 3 migration files + diff of models.py. No prod fixtures touched.
Run: python manage.py makemigrations --dry-run && manage.py migrate --plan.
```

Soft-delete adoption:

```
Add SoftDeleteMixin to <Model>:
- override Manager: objects = SoftDeleteManager(); all_objects = AllObjectsManager().
- replace `unique=True` with `UniqueConstraint(fields=[...], condition=Q(deleted_at__isnull=True))`.
- audit reverse relations: any on_delete=CASCADE child becomes orphaned in soft-delete; convert to PROTECT or override delete().
- update admin: register with `all_objects` so deleted rows are visible.
- write regression tests: delete then list; restore; hard_delete; bulk_delete.
```

## CLI tools

| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `python manage.py makemigrations` | Generate schema/data migrations | bundled with Django |
| `python manage.py migrate --plan` | Validate migration order before applying | bundled |
| `python manage.py sqlmigrate` | Inspect generated SQL before running | bundled |
| `django-extensions` (`shell_plus`, `graph_models`) | Visualize the inheritance + relations | https://django-extensions.readthedocs.io |
| `django-model-utils` | Battle-tested mixins (TimeStamped, SoftDeletable, StatusModel) | https://django-model-utils.readthedocs.io |
| `django-simple-history` | Auto history tables for audit trail | https://django-simple-history.readthedocs.io |
| `django-soft-delete` | Drop-in soft-delete utilities | https://pypi.org/project/django-soft-delete/ |
| `django-tenants` | PostgreSQL schema-per-tenant multi-tenancy | https://django-tenants.readthedocs.io |
| `django-tenant-schemas` (legacy) | Older tenant pattern; only for migration off | https://django-tenant-schemas.readthedocs.io |
| `pgcli` | Inspect partial indexes / constraints for soft-delete | https://www.pgcli.com |
| `django-stubs` | Type-check the inheritance chain | https://github.com/typeddjango/django-stubs |
| `django-upgrade` | Modernise old patterns when migrating to new bases | https://github.com/adamchainz/django-upgrade |
| `factory-boy` | Test factories that respect base-model defaults | https://factoryboy.readthedocs.io |

## Services & apps

| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| PostgreSQL (RDS / Cloud SQL / Neon / Supabase) | SaaS | Yes — REST/CLI | Required for `db_default`, `GeneratedField(db_persist=True)`, partial unique indexes |
| MySQL 8+ (Cloud SQL / RDS / PlanetScale) | SaaS | Yes — REST/CLI | Slightly different `GeneratedField` semantics; verify before adopting |
| SQLite + Litestream | OSS | Yes — CLI | Avoid `db_persist=True`; `db_default=Now()` works in SQLite ≥3.38 |
| AWS DMS / `pg_dump` / `pg_restore` | SaaS/OSS | Yes — CLI | For large backfills (`uid` columns on big tables, off-peak) |
| Sentry | SaaS | Yes — REST | Watch for `IntegrityError` spikes during backfill rollout |
| Datadog APM | SaaS | Yes — REST/agent | Catch query-plan regressions after partial-index additions |
| Postgres `pg_repack` (RDS / Cloud SQL extension) | OSS | Yes — CLI | Rebuild large tables after adding `uid` + index without long locks |
| `django-simple-history` admin | OSS | Yes — admin pages | Manual audit; agents can't easily replay history programmatically |
| `pgaudit` / `RDS Performance Insights` | SaaS | Yes — REST/CLI | Validate that soft-delete partial indexes are being used |

## Templates & scripts

See `templates.md` for full base-model snippets. Inline data-migration template for adding `uid` to an existing table (≤30 lines):

```python
# apps/<app>/migrations/00XX_add_uid.py
from django.db import migrations, models
import uuid

def gen_uids(apps, schema_editor):
    Model = apps.get_model("<app>", "<Model>")
    batch = []
    for obj in Model.objects.filter(uid__isnull=True).iterator(chunk_size=2000):
        obj.uid = uuid.uuid4()
        batch.append(obj)
        if len(batch) >= 2000:
            Model.objects.bulk_update(batch, ["uid"])
            batch.clear()
    if batch:
        Model.objects.bulk_update(batch, ["uid"])

class Migration(migrations.Migration):
    dependencies = [("<app>", "00XX_prev")]
    operations = [
        migrations.AddField("<Model>", "uid",
            models.UUIDField(default=uuid.uuid4, null=True, editable=False)),
        migrations.RunPython(gen_uids, migrations.RunPython.noop),
        migrations.AlterField("<Model>", "uid",
            models.UUIDField(default=uuid.uuid4, unique=True, editable=False, db_index=True)),
    ]
```

Soft-delete partial unique index (PostgreSQL):

```python
class Meta:
    constraints = [
        models.UniqueConstraint(
            fields=["tenant", "slug"],
            condition=models.Q(deleted_at__isnull=True),
            name="uq_<model>_slug_alive",
        ),
    ]
```

## Best practices

- **Keep `id` (BigAutoField) as PK; expose `uid` (UUIDField) externally.** Faster joins, smaller indexes, hides enumeration. Only switch to UUID PK with a measured reason.
- **Index `uid`** explicitly (`db_index=True` or unique). Lookups by `uid` without an index force seq scans on large tables.
- **All admin/list views must use `all_objects`** if soft-delete is enabled — surface deleted rows to admins, hide from public managers.
- **Replace every `unique=True`** on a soft-deletable model with a partial `UniqueConstraint(condition=Q(deleted_at__isnull=True))`.
- **Mixin order: behaviour-overriding mixins first** (`SoftDeleteMixin` before `TimestampMixin`). Document the order in `core/models.py`.
- **`on_delete` defaults**: `PROTECT` for parent rows you don't want to lose, `CASCADE` only when child has no meaning without parent, `SET_NULL` for surviving content with detached author.
- **Generate migrations per app** even when the change spans many — keeps deploy ordering and rollback options open.
- **Backfill in chunks** (`iterator(chunk_size=2000)`, `bulk_update`) inside `RunPython`; never load full table to memory.
- **`HistoricalRecords` selectively.** Audit only models needed for compliance; not every entity. Otherwise you double the table count.
- **Tenant scoping is a property of the manager, not the model alone.** Always pair `TenantAwareModel` with explicit `with tenant_context(...)` in tasks/cron.
- **Document base-model contract** in `core/AGENTS.md`: what every model must inherit and what optional mixins exist.

## AI-agent gotchas

- **Switching PK to UUID retroactively** is destructive and pretends to be a 5-line change. Reject any migration that drops/recreates `id`. Always go via separate `uid` column.
- **Agents add `unique=True` and forget partial-index requirement** when soft-delete is enabled — leads to `IntegrityError` after restore.
- **Default `objects` shadowing.** Agents put `objects = SoftDeleteManager()` first and lose access to deleted rows everywhere — including admin and `loaddata`. Always preserve `all_objects` and update admin.
- **CASCADE through soft-delete** silently hard-deletes children. Force a checklist: list every reverse relation and decide CASCADE/PROTECT/SET_NULL per edge.
- **Tenant context leaks** in Celery tasks because `get_current_tenant()` reads thread-local set by middleware. Agents that "just call `Model.objects.all()`" return cross-tenant rows. Force explicit context.
- **`db_default=Now()` confused with `auto_now_add=True`.** They behave differently for `bulk_create`, `update`, raw SQL. Pick one and document in the base model.
- **`GeneratedField(db_persist=True)`** generates SQL that errors on SQLite. Agents that ship SQLite-targeted dev DBs will see migration errors only in CI. Test on the prod DB engine.
- **`HistoricalRecords(inherit=True)`** combined with abstract base + 100 child models silently creates 100 extra tables. Reviewers should always count migrations.
- **`.delete()` semantic flip.** Once `SoftDeleteMixin` is in, `Model.objects.filter(...).delete()` no longer hits the row-level override (Django QuerySet `delete()` bypasses it). Agents must override the QuerySet too.
- **`objects.update()` bypasses signals and `save()`** — soft-delete logic that lives in `delete()` won't run; agents who write "set deleted_at via update" miss that the queryset path needs its own override.
- **`uid` as URL param** without a length-validating regex lets `/users/<uid:uuid>/` accept any string. Use Django's `uuid` path converter, not `<str:uid>`.
- **Mass-rename of `id` references** to `uid` in templates/serializers without migration creates dead URL routes. Migrate views + URL conf in the same PR.

## References

- Methodology README: `./README.md`
- Django model field reference: https://docs.djangoproject.com/en/5.2/ref/models/fields/
- Django Meta options: https://docs.djangoproject.com/en/5.2/ref/models/options/
- Django constraints (partial unique): https://docs.djangoproject.com/en/5.2/ref/models/constraints/
- Django 5.x `db_default`: https://docs.djangoproject.com/en/5.2/ref/models/fields/#django.db.models.Field.db_default
- Django 5.x `GeneratedField`: https://docs.djangoproject.com/en/5.2/ref/models/fields/#generatedfield
- django-model-utils: https://django-model-utils.readthedocs.io
- django-simple-history: https://django-simple-history.readthedocs.io
- django-tenants: https://django-tenants.readthedocs.io
- django-soft-delete: https://pypi.org/project/django-soft-delete/
- django-stubs: https://github.com/typeddjango/django-stubs
- factory-boy: https://factoryboy.readthedocs.io
- UUID v7 RFC: https://datatracker.ietf.org/doc/html/rfc9562
- Postgres `pg_repack`: https://reorg.github.io/pg_repack/
- "Avoid UUID v4 PKs": https://andyatkinson.com/avoid-uuid-version-4-primary-keys
