---
name: db-scaling-read-replicas
description: Scale a PostgreSQL database with PgBouncer connection pooling, read replicas, materialized views, and tenant sharding.
tier: pro
group: backend-systems
status: active
owner: ruslan
last_verified: 2026-05-02
version: 1.0.0
---

## Goal

After this playbook you will have a PostgreSQL scaling stack that routes read queries to replicas via your application driver, pools all connections through PgBouncer in transaction mode, serves hot reports from materialized views, and has a clear decision path to tenant sharding when the primary crosses 1 TB.

## Prerequisites

- PostgreSQL 15+ primary running on a dedicated host (not shared container).
- `psql` and `pgbouncer` packages available on the DB host (Ubuntu: `apt install pgbouncer`).
- Application connects via a Python (psycopg3 / SQLAlchemy 2) or Node.js (`pg` / Prisma) driver — examples below cover both.
- `REPLICATION` privilege granted to the replica user on the primary.
- At least one read replica provisioned (same PostgreSQL major version as primary). Managed services: AWS RDS Multi-AZ read replica, Supabase read replica, Neon branching.
- Agency owner or senior developer with `ALTER SYSTEM` rights on the primary.

## Steps

### 1. Add connection pooling via PgBouncer (transaction mode)

Deploy PgBouncer on the DB host or a sidecar VM. Transaction mode recycles server connections after each statement — the only mode safe for stateless web workers.

Edit `/etc/pgbouncer/pgbouncer.ini`:

```ini
[databases]
myapp = host=127.0.0.1 port=5432 dbname=myapp

[pgbouncer]
listen_addr       = 0.0.0.0
listen_port       = 6432
auth_type         = scram-sha-256
auth_file         = /etc/pgbouncer/userlist.txt
pool_mode         = transaction
max_client_conn   = 500
default_pool_size = 20
reserve_pool_size = 5
server_idle_timeout = 60
log_connections   = 0
log_disconnections = 0
```

Populate `/etc/pgbouncer/userlist.txt` with the scram hash (fetch from pg_authid):

```sql
SELECT '"' || rolname || '" "' || rolpassword || '"'
FROM   pg_authid
WHERE  rolname = 'myapp_user';
```

Reload: `systemctl reload pgbouncer`. Point your app at port `6432` instead of `5432`.

**Transaction mode limits:** `SET` commands, `LISTEN`/`NOTIFY`, `PREPARE`, and advisory locks do NOT survive across pooled connections. Move any session-level `SET` calls into the connection string (e.g., `options=-csearch_path%3Dmyschema`).

### 2. Stream a physical read replica

On the **primary**, enable streaming replication:

```sql
-- postgresql.conf (or ALTER SYSTEM)
ALTER SYSTEM SET wal_level = replica;
ALTER SYSTEM SET max_wal_senders = 5;
ALTER SYSTEM SET wal_keep_size = '256MB';
SELECT pg_reload_conf();

-- Create replication user
CREATE ROLE replicator REPLICATION LOGIN PASSWORD '<strong-password>';
```

In `pg_hba.conf` on the primary:

```
host  replication  replicator  <replica-ip>/32  scram-sha-256
```

On the **replica** host, base-backup and start streaming:

```bash
pg_basebackup -h <primary-ip> -U replicator -D /var/lib/postgresql/15/main \
  -P -Xs -R
# -R writes recovery.conf / standby.signal automatically
systemctl start postgresql
```

Verify lag from the primary:

```sql
SELECT client_addr,
       state,
       pg_wal_lsn_diff(pg_current_wal_lsn(), sent_lsn)  AS send_lag_bytes,
       pg_wal_lsn_diff(sent_lsn, replay_lsn)             AS replay_lag_bytes
FROM   pg_stat_replication;
```

### 3. Route read queries to the replica in your application

**Python — SQLAlchemy 2 with separate engines:**

```python
from sqlalchemy import create_engine, text

PRIMARY_URL   = "postgresql+psycopg://myapp_user:secret@pgbouncer-host:6432/myapp"
REPLICA_URL   = "postgresql+psycopg://myapp_user:secret@replica-host:6432/myapp"

write_engine = create_engine(PRIMARY_URL, pool_size=5, max_overflow=10)
read_engine  = create_engine(REPLICA_URL, pool_size=10, max_overflow=20,
                              execution_options={"postgresql_readonly": True})

def get_article(article_id: int):
    with read_engine.connect() as conn:
        return conn.execute(
            text("SELECT * FROM articles WHERE id = :id"),
            {"id": article_id},
        ).mappings().one()

def create_article(data: dict):
    with write_engine.begin() as conn:
        conn.execute(text("INSERT INTO articles ..."), data)
```

**Node.js — `pg` pool pair:**

```typescript
import { Pool } from "pg";

const writePool = new Pool({ host: "pgbouncer-host", port: 6432, database: "myapp" });
const readPool  = new Pool({ host: "replica-host",   port: 6432, database: "myapp" });

async function getArticle(id: number) {
  const { rows } = await readPool.query("SELECT * FROM articles WHERE id = $1", [id]);
  return rows[0];
}
```

**Rule:** all `SELECT` that tolerate up to ~100 ms of replica lag go to `read_engine` / `readPool`. Writes and reads that must see their own write go to the primary.

### 4. Cache hot reports with materialized views

Create a materialized view for reports that execute many times per hour but whose data can be 5–60 minutes stale:

```sql
CREATE MATERIALIZED VIEW mv_monthly_revenue AS
SELECT date_trunc('month', created_at) AS month,
       tenant_id,
       SUM(amount_cents) / 100.0       AS revenue_usd,
       COUNT(*)                         AS order_count
FROM   orders
WHERE  status = 'paid'
GROUP  BY 1, 2;

CREATE UNIQUE INDEX ON mv_monthly_revenue (month, tenant_id);
```

Refresh on a schedule (pg_cron, or a cron job):

```sql
-- Install pg_cron once: CREATE EXTENSION pg_cron;
SELECT cron.schedule('refresh-monthly-revenue', '*/15 * * * *',
  $$REFRESH MATERIALIZED VIEW CONCURRENTLY mv_monthly_revenue$$);
```

`CONCURRENTLY` requires the unique index and does not lock reads during refresh. Drop the index and switch to a plain `REFRESH` only if refresh takes longer than the read window.

Read from the view in your report query:

```sql
SELECT month, revenue_usd, order_count
FROM   mv_monthly_revenue
WHERE  tenant_id = $1
ORDER  BY month DESC
LIMIT  12;
```

### 5. Decide when to shard (decision tree)

Use this tree — re-evaluate at each threshold:

```
Primary DB size < 300 GB AND QPS < 5 000 rps
  → single primary + read replicas + PgBouncer  (this playbook, done)

Primary DB size 300 GB–1 TB OR QPS 5 000–20 000 rps
  → add 2nd read replica + partial indexes + partitioning by date/tenant
  → consider Citus columnar extension for analytics tables

Primary DB size > 1 TB OR QPS > 20 000 rps
  → shard by tenant_id: consistent-hashing across N primary shards
  → each shard gets its own PgBouncer + read replica
  → route at app layer (lookup table: tenant_id → shard DSN)
```

### 6. Implement tenant sharding at the app layer

When the single-DB threshold is crossed, add a shard-routing layer. Keep it simple: a small `shard_map` table in a lightweight "global" DB (can be the old primary, now demoted to metadata-only).

```sql
-- In global/metadata DB
CREATE TABLE shard_map (
  tenant_id  BIGINT PRIMARY KEY,
  shard_dsn  TEXT NOT NULL  -- e.g. 'postgresql://shard1-host:6432/myapp'
);
```

Python routing:

```python
import functools
from sqlalchemy import create_engine, text

@functools.lru_cache(maxsize=4096)
def engine_for_tenant(tenant_id: int):
    with global_engine.connect() as conn:
        row = conn.execute(
            text("SELECT shard_dsn FROM shard_map WHERE tenant_id = :t"),
            {"t": tenant_id},
        ).one()
    return create_engine(row.shard_dsn, pool_size=5, max_overflow=5)

def get_orders(tenant_id: int, limit: int = 100):
    eng = engine_for_tenant(tenant_id)
    with eng.connect() as conn:
        return conn.execute(
            text("SELECT * FROM orders WHERE tenant_id = :t LIMIT :l"),
            {"t": tenant_id, "l": limit},
        ).mappings().all()
```

Cache eviction: call `engine_for_tenant.cache_clear()` after updating `shard_map`.

Cross-shard queries (e.g., global analytics) run against a dedicated reporting replica that aggregates all shards via `postgres_fdw`, or use a separate OLAP store (ClickHouse, BigQuery).

## Verify

**PgBouncer pool stats:**

```bash
psql -h pgbouncer-host -p 6432 -U pgbouncer pgbouncer -c "SHOW POOLS;"
```

Confirms `cl_active` < `max_client_conn`, `sv_active` < `default_pool_size`.

**Replica lag under load:**

```sql
-- Run on primary while app is active
SELECT client_addr,
       write_lag,
       flush_lag,
       replay_lag
FROM   pg_stat_replication;
```

Target: `replay_lag` < 500 ms under normal write load.

**Materialized view freshness:**

```sql
SELECT schemaname, matviewname, last_refresh
FROM   pg_matviews
WHERE  matviewname = 'mv_monthly_revenue';
```

`last_refresh` should be within the cron interval (15 min).

**Read routing confirmation (Python):**

```python
with read_engine.connect() as conn:
    row = conn.execute(text("SELECT inet_server_addr()")).scalar()
    assert row == "<replica-ip>", f"Expected replica, got {row}"
```

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `ERROR: prepared statement already exists` | PREPARE used over pooled connection in transaction mode | Switch to extended query protocol (psycopg3 default) or disable server-side PREPARE in the ORM (`prepared_statement_cache_size=0` in SQLAlchemy) |
| `SET` in connection setup has no effect | PgBouncer transaction mode discards session state after each txn | Move `search_path` / `timezone` into the connection DSN: `options=-ctimezone%3DUTC` |
| Replica lag spikes to minutes under bulk inserts | WAL volume exceeds `max_wal_size` on replica | Increase `max_wal_size` on replica; throttle bulk inserts with `pg_sleep` between batches |
| `REFRESH MATERIALIZED VIEW` blocks reads | Missing unique index; non-concurrent refresh | Add `CREATE UNIQUE INDEX` then switch to `REFRESH MATERIALIZED VIEW CONCURRENTLY` |
| `lru_cache` returns stale shard DSN after tenant migration | Cache not cleared after `shard_map` update | Call `engine_for_tenant.cache_clear()` or use TTL-based cache (e.g., `cachetools.TTLCache`) |
| PgBouncer returns `ERROR: max_client_conn reached` | Too many simultaneous application threads | Raise `max_client_conn` (PgBouncer side) or reduce connection concurrency in app (smaller thread pool) |

## Next

- Add connection health checks and automatic failover: promote a replica to primary using `pg_promote()` + a watchdog process or Patroni.
- Partition large tables by `created_at` range (`PARTITION BY RANGE`) to enable partition pruning before adding a second read replica.
- Graduate analytics workloads to ClickHouse or BigQuery when `mv_monthly_revenue` refresh takes more than 2 minutes — that is the signal that OLAP queries no longer belong in PostgreSQL.

## References

- [knowledge/pro/dev/backend-systems/database-design](../../../knowledge/pro/dev/backend-systems/database-design) — covers normalization trade-offs, index strategy, and denormalization patterns that determine which tables are safe to route to replicas vs. must stay on the primary.
- [knowledge/pro/dev/backend-systems/caching-write-patterns](../../../knowledge/pro/dev/backend-systems/caching-write-patterns) — write-through and write-behind patterns applied here to materialized view refresh strategy (Step 4).
- [knowledge/pro/dev/backend-systems/caching-in-memory](../../../knowledge/pro/dev/backend-systems/caching-in-memory) — underpins the `lru_cache` shard-routing layer in Step 6 and its eviction requirements.
