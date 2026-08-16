# Data Modeling

## Summary

**One-sentence:** Build any persistent schema in three sequential passes: conceptual (entities/relationships) → logical (attributes, keys, 3NF, tech-agnostic) → physical (tables, types, indexes, engine-specific).

**One-paragraph:** Data modeling is a three-pass discipline: conceptual (business terms only), logical (attributes + cardinality + 3NF, still tech-agnostic), physical (engine-specific types, indexes, partitions). Output is a schema spec at each level + migration plan, blocking the common failure of jumping straight to DDL.

**Ефективно для:**

- паст-готова основа для повторюваної задачі — без винаходу велосипеда.
- контракт виходу пинить за схемою — downstream-агент може спожити без re-derive.
- rule-set + decision tree відсіюють варіанти, де методологія НЕ підходить.
- validator-скрипт ловить дрейф артефакту до того, як він потрапить у downstream.
- версіонована, з named-owner — артефакт не стає folklore через 6 місяців.

## Applies If (ALL must hold)

- Designing a new schema OR migrating > 5 tables.
- Workload has cross-entity queries with > 3 joins, OR data growth > 100M rows in 12 months.
- Domain experts available for the conceptual pass.

## Skip If (ANY kills it)

- Tiny app with < 5 tables and < 100K rows; build straight to DDL.
- ORM-generated schema with no analytics or hot-path query.
- Throwaway prototype.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Domain glossary | spreadsheet/markdown | domain expert |
| Top 10 queries by frequency | list with SLO | tech lead |
| Chosen DB engine | name + version | database-selection output |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/dev/software-architect/database-selection` | Provides the engine the physical pass targets. |
| `solo/dev/software-architect/arch-pattern-ddd` | Conceptual pass shares aggregates. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 8 testable rules + skip-this-methodology fallback | ~1200 |
| `content/02-output-contract.xml` | essential | JSON Schema for the 3-pass spec + valid/invalid examples | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom + root-cause + fix | ~800 |
| `content/04-procedure.xml` | deep | 6-step procedure: glossary → conceptual → logical → physical → indexes → migration | ~900 |
| `content/05-examples.xml` | medium | Worked example: 3-pass schema for an Ordering bounded context | ~700 |
| `content/06-decision-tree.xml` | essential | Root-question → branches → conclusion(ref=rule-id) | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-conceptual` | sonnet | Per-aggregate entity-relationship synthesis. |
| `design-indexes` | sonnet | Per-query index plan. |
| `audit-cross-team` | opus | Spot inconsistent term usage across teams. |

## Templates

| File | Purpose |
|------|---------|
| `templates/schema-3-pass.md.j2` | Three-pass schema spec: conceptual + logical + physical. |
| `templates/schema-3-pass.md` | Three-pass schema spec: conceptual + logical + physical. Generated from `templates/schema-3-pass.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/pg-standard-table.sql` | PostgreSQL standard 3NF table skeleton with PK + audit columns + indexes. |
| `templates/pg-junction-table.sql` | PostgreSQL many-to-many junction table with composite PK + FK cascade rules. |
| `templates/mongo-schema.js` | MongoDB collection schema with `$jsonSchema` validator + indexes. |
| `templates/cassandra-table.cql` | Cassandra/ScyllaDB wide-row table: one-table-per-query + partition + clustering keys. |
| `templates/data-vault-hub.sql` | Data Vault 2.0 hub table skeleton with business-key + load-date + record-source. |
| `templates/scd-type2.sql` | Slowly-Changing-Dimension Type 2 table with effective_from/effective_to + current flag. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-data-modeling.py` | Validate the output artefact against the schema in `content/02-output-contract.xml`. | After subagent returns, before downstream consumer reads. |

## Related

- [[database-selection]]
- [[arch-pattern-ddd]]
- [[caching-architecture]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (precondition pass, named owner, input reachability) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it when in doubt about whether this methodology applies or which variant rule to enforce.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/pg-standard-table.sql`

```sql
-- PostgreSQL standard table template
-- Conventions: snake_case, UUID PK, audit columns, soft delete, updated_at trigger

CREATE EXTENSION IF NOT EXISTS "pgcrypto";  -- for gen_random_uuid()

-- Function: auto-update updated_at on every row change
CREATE OR REPLACE FUNCTION set_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Table: replace {table_name} with singular snake_case noun
CREATE TABLE {table_name} (
    id              UUID        PRIMARY KEY DEFAULT gen_random_uuid(),

    -- Domain columns go here
    -- name         VARCHAR(255) NOT NULL,
    -- status       VARCHAR(30)  NOT NULL DEFAULT 'active',

    -- Soft delete
    deleted_at      TIMESTAMPTZ,                          -- NULL = active

    -- Audit columns
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Trigger: keep updated_at current
CREATE TRIGGER trg_{table_name}_updated_at
    BEFORE UPDATE ON {table_name}
    FOR EACH ROW EXECUTE FUNCTION set_updated_at();

-- Indexes
-- Active rows only (partial index — smaller and faster than full)
CREATE INDEX idx_{table_name}_active
    ON {table_name}(created_at)
    WHERE deleted_at IS NULL;

-- FK index example: idx_{table_name}_{fk_column}
-- CREATE INDEX idx_{table_name}_user_id ON {table_name}(user_id);

-- Constraints
-- ALTER TABLE {table_name} ADD CONSTRAINT ck_{table_name}_status
--     CHECK (status IN ('active', 'inactive', 'archived'));
```

### `templates/pg-junction-table.sql`

```sql
-- PostgreSQL many-to-many junction table template
-- Composite PK, FK constraints, reverse lookup index

-- Example: student_course (Students M:N Courses)
-- Replace {left_table} and {right_table} with the two entity names

CREATE TABLE {left_table}_{right_table} (
    {left_table}_id   UUID        NOT NULL REFERENCES {left_table}(id) ON DELETE CASCADE,
    {right_table}_id  UUID        NOT NULL REFERENCES {right_table}(id) ON DELETE CASCADE,

    -- Optional: attributes of the relationship itself
    -- assigned_at    TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    -- role           VARCHAR(30),

    created_at        TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    PRIMARY KEY ({left_table}_id, {right_table}_id)
);

-- Forward lookup: all {right_table}s for a given {left_table}
-- Covered by the composite PK above (leftmost column = {left_table}_id)

-- Reverse lookup: all {left_table}s for a given {right_table}
CREATE INDEX idx_{left_table}_{right_table}_reverse
    ON {left_table}_{right_table}({right_table}_id, {left_table}_id);

-- Named constraints for clear error messages
ALTER TABLE {left_table}_{right_table}
    ADD CONSTRAINT fk_{left_table}_{right_table}_{left_table}
        FOREIGN KEY ({left_table}_id) REFERENCES {left_table}(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_{left_table}_{right_table}_{right_table}
        FOREIGN KEY ({right_table}_id) REFERENCES {right_table}(id) ON DELETE CASCADE;

-- Concrete example: student_course
-- CREATE TABLE student_course (
--     student_id   UUID NOT NULL REFERENCES student(id) ON DELETE CASCADE,
--     course_id    UUID NOT NULL REFERENCES course(id)  ON DELETE CASCADE,
--     enrolled_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
--     PRIMARY KEY (student_id, course_id)
-- );
-- CREATE INDEX idx_student_course_reverse ON student_course(course_id, student_id);
```

### `templates/mongo-schema.js`

```javascript
// MongoDB document schema template
// Demonstrates embedded vs referenced patterns and schema validation

// -------------------------------------------------------------------
// EMBEDDED: use when child data is only accessed via parent
//           and the sub-document set is bounded and small (<100 items)
// -------------------------------------------------------------------
db.createCollection("order", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["userId", "status", "items", "totalAmount", "createdAt"],
      properties: {
        _id:         { bsonType: "objectId" },
        userId:      { bsonType: "objectId", description: "Reference to user collection" },
        status: {
          bsonType: "string",
          enum: ["pending", "confirmed", "shipped", "delivered", "cancelled"],
        },
        totalAmount: { bsonType: "decimal", minimum: 0 },
        // Embedded sub-documents — items are never queried independently
        items: {
          bsonType: "array",
          minItems: 1,
          items: {
            bsonType: "object",
            required: ["productId", "productName", "quantity", "unitPrice"],
            properties: {
              productId:   { bsonType: "objectId" },
              productName: { bsonType: "string" },   // denormalized at write time
              quantity:    { bsonType: "int", minimum: 1 },
              unitPrice:   { bsonType: "decimal", minimum: 0 },
            },
          },
        },
        createdAt:   { bsonType: "date" },
        updatedAt:   { bsonType: "date" },
      },
    },
  },
  validationLevel: "strict",
  validationAction: "error",
});

// Indexes for order
db.order.createIndex({ userId: 1, createdAt: -1 });         // orders by user, newest first
db.order.createIndex({ status: 1, createdAt: -1 });         // orders by status queue
db.order.createIndex({ "items.productId": 1 });             // reverse lookup: orders containing product


// -------------------------------------------------------------------
// REFERENCED: use when the related document is large, shared,
//             queried independently, or grows without bound
// -------------------------------------------------------------------
db.createCollection("product", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["sku", "name", "price", "isActive"],
      properties: {
        _id:      { bsonType: "objectId" },
        sku:      { bsonType: "string" },
        name:     { bsonType: "string" },
        price:    { bsonType: "decimal", minimum: 0 },
        isActive: { bsonType: "bool" },
        // Flexible attributes: use for truly variable fields only
        attributes: { bsonType: "object" },
        createdAt:  { bsonType: "date" },
        updatedAt:  { bsonType: "date" },
      },
    },
  },
});

db.product.createIndex({ sku: 1 }, { unique: true });
db.product.createIndex({ name: "text" });                   // full-text search
db.product.createIndex({ isActive: 1, price: 1 });          // active products by price
```

### `templates/cassandra-table.cql`

```cypher
-- Cassandra / ScyllaDB table template
-- Design: one table per query; partition key in every WHERE clause

-- -------------------------------------------------------------------
-- Query-first pattern example
-- Query: "Get last N events for a user, in reverse chronological order"
-- -------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS app.user_event_by_user (
    -- Partition key: determines which node stores the row
    -- Avoid hot partitions: bucket by time if single user generates >100k rows/day
    user_id     UUID,
    -- For high-volume users, add a time bucket: (user_id, event_month)

    -- Clustering columns: define sort order within the partition
    occurred_at TIMESTAMP,
    event_id    UUID,

    -- Payload columns
    event_type  TEXT,
    metadata    MAP<TEXT, TEXT>,

    PRIMARY KEY ((user_id), occurred_at, event_id)
)
WITH CLUSTERING ORDER BY (occurred_at DESC, event_id ASC)
AND  default_time_to_live = 7776000  -- 90 days TTL; remove if retention is indefinite
AND  compaction = {
    'class': 'org.apache.cassandra.db.compaction.TimeWindowCompactionStrategy',
    'compaction_window_unit': 'DAYS',
    'compaction_window_size': 1
}
AND  compression = {
    'sstable_compression': 'org.apache.cassandra.io.compress.LZ4Compressor'
};

-- -------------------------------------------------------------------
-- Second table for a DIFFERENT query on the same logical data
-- Query: "Get all users who triggered a specific event type today"
-- This cannot reuse the table above — model a new table.
-- -------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS app.user_event_by_type (
    event_type  TEXT,
    event_date  DATE,           -- time bucket to bound partition size
    occurred_at TIMESTAMP,
    event_id    UUID,
    user_id     UUID,
    metadata    MAP<TEXT, TEXT>,

    PRIMARY KEY ((event_type, event_date), occurred_at, event_id)
)
WITH CLUSTERING ORDER BY (occurred_at DESC, event_id ASC)
AND  default_time_to_live = 2592000  -- 30 days
AND  compaction = {
    'class': 'org.apache.cassandra.db.compaction.TimeWindowCompactionStrategy',
    'compaction_window_unit': 'DAYS',
    'compaction_window_size': 1
};

-- -------------------------------------------------------------------
-- Materialized view (ScyllaDB / Cassandra 3+)
-- Alternative to a second table when the data is identical.
-- NOTE: MV have known performance caveats; prefer manual dual-write for
-- high-throughput tables.
-- -------------------------------------------------------------------
-- CREATE MATERIALIZED VIEW IF NOT EXISTS app.user_event_by_type_mv
-- AS SELECT * FROM app.user_event_by_user
-- WHERE event_type IS NOT NULL AND event_date IS NOT NULL
--   AND occurred_at IS NOT NULL AND event_id IS NOT NULL
-- PRIMARY KEY ((event_type, event_date), occurred_at, event_id)
-- WITH CLUSTERING ORDER BY (occurred_at DESC, event_id ASC);
```

### `templates/data-vault-hub.sql`

```sql
-- Data Vault 2.0: Hub, Link, Satellite DDL templates
-- Engine: PostgreSQL; replace schema prefix as needed

-- -------------------------------------------------------------------
-- HUB: one row per unique business key
-- Stores the business key; descriptive attributes go in Satellites
-- -------------------------------------------------------------------
CREATE TABLE dv.hub_customer (
    hub_customer_hk  BYTEA        PRIMARY KEY,  -- MD5/SHA1 of business key
    customer_number  VARCHAR(50)  NOT NULL,      -- the business key
    load_dts         TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
    record_source    VARCHAR(100) NOT NULL        -- source system identifier
);

-- Hash key generation (consistent with other hubs):
-- hub_customer_hk = MD5(UPPER(TRIM(customer_number)))::BYTEA
-- Or using pgcrypto: digest(upper(trim(customer_number)), 'md5')

CREATE UNIQUE INDEX uq_hub_customer_bk ON dv.hub_customer(customer_number);
CREATE INDEX idx_hub_customer_load_dts ON dv.hub_customer(load_dts);


-- -------------------------------------------------------------------
-- LINK: one row per unique relationship between hubs
-- -------------------------------------------------------------------
CREATE TABLE dv.lnk_customer_order (
    lnk_customer_order_hk  BYTEA       PRIMARY KEY,  -- MD5 of composite BK
    hub_customer_hk        BYTEA       NOT NULL REFERENCES dv.hub_customer(hub_customer_hk),
    hub_order_hk           BYTEA       NOT NULL,     -- references hub_order
    load_dts               TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    record_source          VARCHAR(100) NOT NULL
);

CREATE INDEX idx_lnk_co_customer ON dv.lnk_customer_order(hub_customer_hk);
CREATE INDEX idx_lnk_co_order    ON dv.lnk_customer_order(hub_order_hk);

-- Hash key for link: MD5(customer_hk || order_hk) — concatenate hub HKs


-- -------------------------------------------------------------------
-- SATELLITE: one row per change to descriptive attributes
-- Attached to a hub (or link); tracks full history
-- -------------------------------------------------------------------
CREATE TABLE dv.sat_customer_details (
    hub_customer_hk  BYTEA        NOT NULL REFERENCES dv.hub_customer(hub_customer_hk),
    load_dts         TIMESTAMPTZ  NOT NULL DEFAULT NOW(),

    -- End-dating: NULL = current row; set by the next load
    load_end_dts     TIMESTAMPTZ,

    -- Change detection: hash of all attribute values
    hash_diff        BYTEA        NOT NULL,

    record_source    VARCHAR(100) NOT NULL,

    -- Descriptive attributes (volatile data)
    first_name       VARCHAR(255),
    last_name        VARCHAR(255),
    email            VARCHAR(255),
    phone            VARCHAR(50),
    country_code     CHAR(2),

    PRIMARY KEY (hub_customer_hk, load_dts)
);

-- Active record lookup
CREATE INDEX idx_sat_customer_active
    ON dv.sat_customer_details(hub_customer_hk, load_end_dts)
    WHERE load_end_dts IS NULL;

-- Change detection: only INSERT if hash_diff differs from latest row
-- SELECT hash_diff FROM dv.sat_customer_details
-- WHERE hub_customer_hk = $hk AND load_end_dts IS NULL;


-- -------------------------------------------------------------------
-- POINT-IN-TIME (PIT) table — optional performance helper
-- Pre-join satellite snapshots to avoid correlated subqueries
-- -------------------------------------------------------------------
CREATE TABLE dv.pit_customer (
    hub_customer_hk        BYTEA       NOT NULL,
    snapshot_dts           TIMESTAMPTZ NOT NULL,

    -- One HK per satellite that participates in this PIT
    sat_customer_details_hk BYTEA,
    sat_customer_details_ldts TIMESTAMPTZ,

    PRIMARY KEY (hub_customer_hk, snapshot_dts)
);
```

### `templates/scd-type2.sql`

```sql
-- SCD Type 2 dimension table with upsert procedure
-- Full history: one row per version; valid_from/valid_to/is_current pattern
-- Engine: PostgreSQL

CREATE TABLE dim_customer (
    surrogate_key   BIGSERIAL    PRIMARY KEY,
    customer_nk     VARCHAR(50)  NOT NULL,  -- natural/business key

    -- SCD Type 2 versioning columns
    valid_from      TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
    valid_to        TIMESTAMPTZ,            -- NULL = current record
    is_current      BOOLEAN      NOT NULL DEFAULT TRUE,

    -- Change hash: MD5 of all tracked attributes for change detection
    hash_diff       TEXT         NOT NULL,

    -- Dimension attributes (tracked for history)
    first_name      VARCHAR(255),
    last_name       VARCHAR(255),
    email           VARCHAR(255),
    country_code    CHAR(2),
    tier            VARCHAR(30),

    -- ETL audit columns
    load_dts        TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
    record_source   VARCHAR(100) NOT NULL
);

-- Indexes
CREATE INDEX idx_dim_customer_nk_current
    ON dim_customer(customer_nk)
    WHERE is_current = TRUE;

CREATE UNIQUE INDEX uq_dim_customer_nk_current
    ON dim_customer(customer_nk)
    WHERE is_current = TRUE;  -- enforce single current record per natural key

CREATE INDEX idx_dim_customer_valid
    ON dim_customer(customer_nk, valid_from, valid_to);


-- -------------------------------------------------------------------
-- Upsert procedure: call once per source row on each ETL run
-- Handles: no change (skip), attribute change (expire + insert), new (insert)
-- -------------------------------------------------------------------
CREATE OR REPLACE PROCEDURE upsert_dim_customer(
    p_customer_nk   VARCHAR(50),
    p_first_name    VARCHAR(255),
    p_last_name     VARCHAR(255),
    p_email         VARCHAR(255),
    p_country_code  CHAR(2),
    p_tier          VARCHAR(30),
    p_record_source VARCHAR(100)
)
LANGUAGE plpgsql AS $$
DECLARE
    v_hash_diff TEXT;
    v_existing  RECORD;
    v_now       TIMESTAMPTZ := NOW();
BEGIN
    -- Compute hash of all tracked attributes
    v_hash_diff := MD5(
        COALESCE(p_first_name,   '') ||
        COALESCE(p_last_name,    '') ||
        COALESCE(p_email,        '') ||
        COALESCE(p_country_code, '') ||
        COALESCE(p_tier,         '')
    );

    -- Find current record (if any)
    SELECT * INTO v_existing
    FROM dim_customer
    WHERE customer_nk = p_customer_nk AND is_current = TRUE;

    IF NOT FOUND THEN
        -- New natural key: insert first version
        INSERT INTO dim_customer (
            customer_nk, first_name, last_name, email, country_code, tier,
            hash_diff, valid_from, valid_to, is_current, record_source
        ) VALUES (
            p_customer_nk, p_first_name, p_last_name, p_email, p_country_code, p_tier,
            v_hash_diff, v_now, NULL, TRUE, p_record_source
        );

    ELSIF v_existing.hash_diff <> v_hash_diff THEN
        -- Attributes changed: expire current row and insert new version
        UPDATE dim_customer
        SET    valid_to   = v_now,
               is_current = FALSE
        WHERE  surrogate_key = v_existing.surrogate_key;

        INSERT INTO dim_customer (
            customer_nk, first_name, last_name, email, country_code, tier,
            hash_diff, valid_from, valid_to, is_current, record_source
        ) VALUES (
            p_customer_nk, p_first_name, p_last_name, p_email, p_country_code, p_tier,
            v_hash_diff, v_now, NULL, TRUE, p_record_source
        );
    END IF;
    -- If hash is unchanged: no action needed
END;
$$;

-- Usage:
-- CALL upsert_dim_customer('C-1001', 'John', 'Doe', 'john@example.com', 'US', 'gold', 'crm-system');
```
