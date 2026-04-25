# Agent Integration — Dev Methodologies Architecture

## When to use
- Drafting backend architecture for a new service: choosing DB schema layout, ORM access patterns, cache strategy, queue/worker split, auth model.
- Reviewing an existing service for N+1 queries, missing indexes, blocking I/O, ad-hoc auth, or unstructured logging.
- Generating migration scripts (Alembic / Django / knex) and verifying they are backward compatible (expand-then-contract for CD).
- Standardizing API response envelopes across a polyglot codebase.

## When NOT to use
- Frontend / UI architecture — this set is backend-only (DB, API, cache, queue, observability).
- Greenfield prototyping where the cost of patterns exceeds the value (one-off scripts, throwaway demos).
- Replacement for a real DBA on high-stakes schema design (sharding, multi-region, ACID-vs-BASE trade-offs).
- When the hosting platform already prescribes patterns (e.g. Supabase, Firebase) — defer to platform conventions.

## Where it fails / limitations
- The README is a high-level catalogue — it does not include capacity numbers, index-type trade-offs, isolation-level guidance, or vendor-specific quirks.
- "Caching strategies" table omits invalidation, stampede, and dog-pile concerns; agents must add those checks.
- Auth section lists patterns but not threats — agents should pair with a security checklist before coding auth flows.
- "Database HA Setup" is a single ASCII sketch; real HA needs synchronous-replica decisions, failover rehearsal, split-brain handling.
- N+1 example is Django-flavoured; SQLAlchemy / TypeORM / Prisma have different prefetch primitives that are NOT one-to-one.

## Agentic workflow
Drive this with a single planner subagent that reads `README.md`, then delegates each pattern (migrations, queries, ORM, cache, queue, auth, logging) to a focused executor that produces a diff, runs the project's typecheck + linter + tests, and reports back. Keep agents read-only on production data — execute migrations and EXPLAIN ANALYZE only on a disposable replica or local DB. For multi-pattern refactors, force a checkpoint after each pattern (commit + run tests) so a regression is bisectable.

### Recommended subagents
- `general-purpose` — broad pattern application, multi-file edits, autonomous research of unfamiliar ORM idioms.
- `faion-sdd-executor-agent` — when the architecture work is captured as SDD tasks under `.aidocs/in-progress/`.
- `faion-code-agent` (referenced inline in the methodology) — pattern-by-pattern implementation; pin to Sonnet for normal work, Opus only for cache/queue trade-off decisions.
- `faion-devops-agent` (referenced for HA setup) — replica topology, failover, connection-pool sizing.

### Prompt pattern
```
Read solo/dev/automation-tooling/dev-methodologies-architecture/README.md.
Audit <service-path> against each pattern. For every gap, produce a unified
diff, the migration order, and the rollback. Do not touch prod DSNs.
```
```
Apply <pattern-name> to <module>. Use the project ORM idioms in
backend-developer/python-developer skills, not the README's Django snippet
verbatim. Add tests proving N+1 is gone (assert query count).
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| Alembic | Python schema migrations | `pip install alembic` · alembic.sqlalchemy.org |
| Django `makemigrations` / `migrate` | Django ORM migrations | bundled with Django |
| `psql \timing` + `EXPLAIN (ANALYZE, BUFFERS)` | Query plan + cost inspection | bundled with Postgres |
| `pgbadger` | Postgres slow-log analyzer | https://pgbadger.darold.net/ |
| `pt-online-schema-change` | MySQL online schema change | Percona Toolkit |
| `redis-cli --bigkeys` / `--memkeys` | Cache hot-key inspection | bundled with Redis |
| `celery inspect` / `flower` | Queue health + worker introspection | `pip install celery flower` |
| `structlog` + `python-json-logger` | Structured logging | pip |
| `keycloak-admin-cli` / `auth0 deploy` | Manage OAuth2/IdP config from code | vendor docs |
| `oha` / `wrk` | Cheap HTTP load probe to validate cache wins | github.com/hatoo/oha |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Postgres + pgvector | OSS | Yes | Stable EXPLAIN format, well-tooled CLIs, easy for agents to parse. |
| PgBouncer / Pgpool | OSS | Yes | Connection pooling layer; agents can edit pool config and reload. |
| Redis / Valkey / KeyDB | OSS | Yes | Cache + queue back-end; trivial CLI for agents. |
| Celery / RQ / Sidekiq | OSS | Yes | Stable queue inspection; events stream for agents. |
| Auth0 / Clerk / Supabase Auth | SaaS | Partial | Provide Management API; agents must keep secrets out of repo. |
| Keycloak | OSS | Yes | Full admin CLI/REST; deployable from code. |
| Datadog / Grafana Cloud / Honeycomb | SaaS | Yes | Logging/metrics targets; structured fields land cleanly. |
| AWS RDS Proxy / Cloud SQL Proxy | SaaS | Partial | Agents can configure, but credential rotation needs human approval. |
| PlanetScale / Neon | SaaS | Yes | Branching DBs ideal for agent-driven schema rehearsal. |

## Templates & scripts
See `templates.md` and `examples.md` for full snippets. The minimum invocation an agent should always run after a pattern change:

```bash
# Postgres: prove the index is used and N+1 is gone
psql "$DSN" -c "EXPLAIN (ANALYZE, BUFFERS) <suspected-slow-query>;"
pytest -q --maxfail=1 -k "queries_count or n_plus_one"
ruff check . && mypy <service>
```

## Best practices
- Treat every schema change as expand → migrate data → contract; never combine in one deploy if the service is on CD.
- Log a query-count assertion in tests for hot endpoints — it catches ORM regressions far cheaper than profiling later.
- For cache-aside, always pair set+get with a documented TTL, jitter, and a single-flight guard against stampede.
- Centralize the API response envelope in one module + Pydantic/TypedDict; failure to do so leaks shape-drift across endpoints.
- For background jobs, store idempotency keys + `created_at` so agents can re-drive failed jobs without duplication.
- Structured logs: `event` (snake_case verb), `actor`, `object`, `latency_ms`, `correlation_id` — make the field set a code-reviewable contract.

## AI-agent gotchas
- Agents tend to grab the README's Django prefetch example and paste it into SQLAlchemy/Prisma code — verify the ORM before applying.
- Auth changes must be human-approved: token signing keys, OAuth client secrets, password-hash parameters. Never let an autonomous agent rotate prod secrets.
- Cache invalidation is the classic agent failure: an agent will "fix" a stale read by lowering TTL instead of fixing write-through. Insist on a write-path fix.
- Migrations: agents may write a single migration that drops + recreates a column. Force a two-step expand-contract review.
- DB HA: never let an agent promote a replica autonomously. Require human-in-loop for any failover or topology change.
- "Optimize this query" prompts can produce indexes that explode write throughput. Always require an EXPLAIN before AND after on representative data volume.

## References
- Martin Kleppmann, Designing Data-Intensive Applications.
- Postgres docs: https://www.postgresql.org/docs/current/using-explain.html
- Alembic: https://alembic.sqlalchemy.org/
- structlog: https://www.structlog.org/
- OWASP ASVS (auth controls): https://owasp.org/www-project-application-security-verification-standard/
- Celery best practices: https://docs.celeryq.dev/
- Sibling methodology: `solo/dev/automation-tooling/dev-methodologies-practices/`
