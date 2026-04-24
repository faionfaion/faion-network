# Data Modeling Templates

Copy-paste patterns and schema templates for common data modeling scenarios.

## Entity-Relationship Notation

### ERD Box Template

```
┌─────────────────────────────────────┐
│           ENTITY_NAME               │
├─────────────────────────────────────┤
│ PK id                    UUID       │
│    name                  VARCHAR    │
│    description           TEXT       │
│ FK parent_id             UUID       │
│    created_at            TIMESTAMP  │
│    updated_at            TIMESTAMP  │
└─────────────────────────────────────┘
```

### Relationship Symbols

```
One-to-One (1:1)
Entity_A ─────────── Entity_B

One-to-Many (1:N)
Entity_A ─────────<< Entity_B

Many-to-Many (M:N)
Entity_A >>────────<< Entity_B
         (via junction table)

Optional participation (0..1)
Entity_A ○───────── Entity_B

Required participation (1..1)
Entity_A ●───────── Entity_B
```

---

## PostgreSQL Templates

### Standard Table Template

```sql
CREATE TABLE {table_name} (
    -- Primary key
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    -- Business attributes
    {column_name} {data_type} {constraints},

    -- Foreign keys
    {fk_name}_id UUID REFERENCES {ref_table}(id) ON DELETE {action},

    -- Audit columns
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_by UUID REFERENCES users(id),
    updated_by UUID REFERENCES users(id),

    -- Soft delete (optional)
    deleted_at TIMESTAMPTZ
);

-- Indexes
CREATE INDEX idx_{table_name}_{column} ON {table_name}({column});

-- Partial index for soft delete
CREATE INDEX idx_{table_name}_active ON {table_name}(id)
    WHERE deleted_at IS NULL;

-- Updated_at trigger
CREATE TRIGGER set_{table_name}_updated_at
    BEFORE UPDATE ON {table_name}
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
```

### Common Trigger Function

```sql
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
```

### Junction Table Template (M:N)

```sql
CREATE TABLE {table_a}_{table_b} (
    {table_a}_id UUID NOT NULL REFERENCES {table_a}(id) ON DELETE CASCADE,
    {table_b}_id UUID NOT NULL REFERENCES {table_b}(id) ON DELETE CASCADE,

    -- Optional: relationship metadata
    assigned_at TIMESTAMPTZ DEFAULT NOW(),
    assigned_by UUID REFERENCES users(id),

    PRIMARY KEY ({table_a}_id, {table_b}_id)
);

-- Index for reverse lookups
CREATE INDEX idx_{table_a}_{table_b}_reverse
    ON {table_a}_{table_b}({table_b}_id);
```

### Self-Referential Tree Template

```sql
CREATE TABLE {table_name} (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    parent_id UUID REFERENCES {table_name}(id) ON DELETE CASCADE,
    level INT NOT NULL DEFAULT 0,
    path TEXT,  -- Materialized path: '/1/2/3/'
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Index for tree queries
CREATE INDEX idx_{table_name}_parent ON {table_name}(parent_id);
CREATE INDEX idx_{table_name}_path ON {table_name}(path);

-- Recursive CTE for tree traversal
WITH RECURSIVE tree AS (
    SELECT id, name, parent_id, 0 as depth
    FROM {table_name}
    WHERE parent_id IS NULL

    UNION ALL

    SELECT c.id, c.name, c.parent_id, t.depth + 1
    FROM {table_name} c
    JOIN tree t ON c.parent_id = t.id
)
SELECT * FROM tree;
```

### Enum Alternative (Lookup Table)

```sql
-- Instead of PostgreSQL ENUM (hard to modify)
CREATE TABLE {entity}_status (
    code VARCHAR(30) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    sort_order INT DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE
);

INSERT INTO {entity}_status (code, name, sort_order) VALUES
    ('pending', 'Pending', 1),
    ('active', 'Active', 2),
    ('completed', 'Completed', 3),
    ('cancelled', 'Cancelled', 4);

-- Reference in main table
CREATE TABLE {entity} (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    status VARCHAR(30) NOT NULL
        REFERENCES {entity}_status(code)
        DEFAULT 'pending',
    -- other columns
);
```

### Audit Log Template

```sql
CREATE TABLE audit_log (
    id BIGSERIAL PRIMARY KEY,
    table_name VARCHAR(100) NOT NULL,
    record_id UUID NOT NULL,
    action VARCHAR(10) NOT NULL CHECK (action IN ('INSERT', 'UPDATE', 'DELETE')),
    old_values JSONB,
    new_values JSONB,
    changed_fields TEXT[],
    user_id UUID,
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_audit_log_table_record ON audit_log(table_name, record_id);
CREATE INDEX idx_audit_log_created ON audit_log(created_at);
CREATE INDEX idx_audit_log_user ON audit_log(user_id);

-- Generic audit trigger
CREATE OR REPLACE FUNCTION audit_trigger_func()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        INSERT INTO audit_log (table_name, record_id, action, new_values)
        VALUES (TG_TABLE_NAME, NEW.id, 'INSERT', to_jsonb(NEW));
        RETURN NEW;
    ELSIF TG_OP = 'UPDATE' THEN
        INSERT INTO audit_log (table_name, record_id, action, old_values, new_values)
        VALUES (TG_TABLE_NAME, NEW.id, 'UPDATE', to_jsonb(OLD), to_jsonb(NEW));
        RETURN NEW;
    ELSIF TG_OP = 'DELETE' THEN
        INSERT INTO audit_log (table_name, record_id, action, old_values)
        VALUES (TG_TABLE_NAME, OLD.id, 'DELETE', to_jsonb(OLD));
        RETURN OLD;
    END IF;
END;
$$ LANGUAGE plpgsql;

-- Apply to table
CREATE TRIGGER audit_{table_name}
    AFTER INSERT OR UPDATE OR DELETE ON {table_name}
    FOR EACH ROW EXECUTE FUNCTION audit_trigger_func();
```

---

## MongoDB Templates

### Document Schema Template

```javascript
// Collection: {collection_name}
{
  "_id": ObjectId("..."),

  // Business fields
  "{field_name}": "{value}",

  // Embedded document
  "{embedded_name}": {
    "subfield1": "value",
    "subfield2": 123
  },

  // Embedded array
  "{items}": [
    { "item_field": "value" }
  ],

  // Reference (when not embedding)
  "{ref_name}_id": ObjectId("..."),

  // Audit fields
  "createdAt": ISODate("2025-01-20T10:00:00Z"),
  "updatedAt": ISODate("2025-01-20T10:00:00Z"),
  "createdBy": ObjectId("..."),
  "updatedBy": ObjectId("..."),

  // Version for optimistic locking
  "__v": 0
}

// Indexes
db.{collection_name}.createIndex({ "{field}": 1 })
db.{collection_name}.createIndex({ "{field1}": 1, "{field2}": -1 })
db.{collection_name}.createIndex({ "{text_field}": "text" })
db.{collection_name}.createIndex({ "{date_field}": 1 }, { expireAfterSeconds: 86400 })

// Schema validation
db.createCollection("{collection_name}", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["field1", "field2"],
      properties: {
        field1: {
          bsonType: "string",
          description: "must be a string and is required"
        },
        field2: {
          bsonType: "int",
          minimum: 0,
          description: "must be a non-negative integer"
        }
      }
    }
  }
})
```

### Aggregation Pipeline Template

```javascript
db.{collection}.aggregate([
  // Stage 1: Filter
  { $match: { status: "active" } },

  // Stage 2: Lookup (join)
  {
    $lookup: {
      from: "related_collection",
      localField: "related_id",
      foreignField: "_id",
      as: "related"
    }
  },

  // Stage 3: Unwind array
  { $unwind: { path: "$related", preserveNullAndEmptyArrays: true } },

  // Stage 4: Group
  {
    $group: {
      _id: "$category",
      total: { $sum: "$amount" },
      count: { $sum: 1 },
      avg: { $avg: "$amount" }
    }
  },

  // Stage 5: Sort
  { $sort: { total: -1 } },

  // Stage 6: Project
  {
    $project: {
      _id: 0,
      category: "$_id",
      total: 1,
      count: 1,
      average: { $round: ["$avg", 2] }
    }
  },

  // Stage 7: Limit
  { $limit: 10 }
])
```

---

## Cassandra/ScyllaDB Templates

### Table Template

```cql
CREATE TABLE {keyspace}.{table_name} (
    -- Partition key
    {partition_column} {type},

    -- Clustering columns
    {clustering_column} {type},

    -- Regular columns
    {column_name} {type},

    -- Static columns (per partition)
    {static_column} {type} STATIC,

    -- Collection types
    {list_column} LIST<{type}>,
    {set_column} SET<{type}>,
    {map_column} MAP<{key_type}, {value_type}>,

    PRIMARY KEY (({partition_columns}), {clustering_columns})
) WITH CLUSTERING ORDER BY ({clustering_column} DESC)
  AND default_time_to_live = {seconds}
  AND gc_grace_seconds = 864000
  AND compaction = {
    'class': 'LeveledCompactionStrategy',
    'sstable_size_in_mb': 160
  };
```

### Time-Series Pattern

```cql
-- Partition by sensor and day, cluster by time
CREATE TABLE sensor_readings (
    sensor_id TEXT,
    date DATE,
    reading_time TIMESTAMP,
    value DOUBLE,
    unit TEXT,
    metadata MAP<TEXT, TEXT>,
    PRIMARY KEY ((sensor_id, date), reading_time)
) WITH CLUSTERING ORDER BY (reading_time DESC)
  AND default_time_to_live = 2592000;  -- 30 days
```

### User-Defined Type (UDT)

```cql
CREATE TYPE address (
    street TEXT,
    city TEXT,
    state TEXT,
    postal_code TEXT,
    country TEXT
);

CREATE TABLE customers (
    customer_id UUID PRIMARY KEY,
    name TEXT,
    billing_address FROZEN<address>,
    shipping_addresses LIST<FROZEN<address>>
);
```

---

## Neo4j Templates

### Node and Relationship Creation

```cypher
// Create node
CREATE (n:{Label} {
  id: '{id}',
  name: '{name}',
  {property}: {value},
  createdAt: datetime()
})

// Create relationship
MATCH (a:{LabelA} {id: '{id_a}'})
MATCH (b:{LabelB} {id: '{id_b}'})
CREATE (a)-[r:{RELATIONSHIP_TYPE} {
  since: datetime(),
  weight: 1.0
}]->(b)

// Merge (create if not exists)
MERGE (n:{Label} {id: '{id}'})
ON CREATE SET n.createdAt = datetime()
ON MATCH SET n.updatedAt = datetime()
SET n.name = '{name}'
```

### Index and Constraint Templates

```cypher
// Unique constraint (creates index automatically)
CREATE CONSTRAINT {label}_id_unique IF NOT EXISTS
FOR (n:{Label})
REQUIRE n.id IS UNIQUE;

// Node key constraint (composite unique)
CREATE CONSTRAINT {label}_composite IF NOT EXISTS
FOR (n:{Label})
REQUIRE (n.field1, n.field2) IS NODE KEY;

// Existence constraint
CREATE CONSTRAINT {label}_name_exists IF NOT EXISTS
FOR (n:{Label})
REQUIRE n.name IS NOT NULL;

// Index for search
CREATE INDEX {label}_name IF NOT EXISTS
FOR (n:{Label})
ON (n.name);

// Composite index
CREATE INDEX {label}_composite IF NOT EXISTS
FOR (n:{Label})
ON (n.field1, n.field2);

// Full-text index
CREATE FULLTEXT INDEX {label}_search IF NOT EXISTS
FOR (n:{Label})
ON EACH [n.name, n.description];
```

### Common Query Patterns

```cypher
// Breadth-first traversal with depth limit
MATCH (start:{Label} {id: '{id}'})-[*1..3]-(connected)
RETURN DISTINCT connected

// Shortest path
MATCH path = shortestPath(
  (a:{Label} {id: '{id_a}'})-[*]-(b:{Label} {id: '{id_b}'})
)
RETURN path

// Aggregation with relationship filtering
MATCH (n:{Label})-[r:{RELATIONSHIP}]->(m)
WHERE r.weight > 0.5
WITH n, COUNT(m) as connections, SUM(r.weight) as totalWeight
RETURN n.name, connections, totalWeight
ORDER BY connections DESC
LIMIT 10

// Collect into list
MATCH (u:User)-[:PURCHASED]->(p:Product)
RETURN u.name, COLLECT(p.name) as products
```

---

## TimescaleDB Templates

### Hypertable Creation

```sql
-- Create regular table
CREATE TABLE {table_name} (
    time TIMESTAMPTZ NOT NULL,
    {device_id} {type} NOT NULL,
    {metric_name} DOUBLE PRECISION,
    {quality} INT DEFAULT 100
);

-- Convert to hypertable
SELECT create_hypertable(
    '{table_name}',
    'time',
    chunk_time_interval => INTERVAL '1 day',
    create_default_indexes => TRUE
);

-- Add additional indexes
CREATE INDEX idx_{table_name}_{device} ON {table_name}({device_id}, time DESC);
```

### Continuous Aggregate Template

```sql
CREATE MATERIALIZED VIEW {view_name}
WITH (timescaledb.continuous) AS
SELECT
    time_bucket('{interval}', time) AS bucket,
    {group_columns},
    AVG({metric}) AS avg_{metric},
    MIN({metric}) AS min_{metric},
    MAX({metric}) AS max_{metric},
    COUNT(*) AS sample_count
FROM {table_name}
GROUP BY bucket, {group_columns}
WITH NO DATA;

-- Add refresh policy
SELECT add_continuous_aggregate_policy('{view_name}',
    start_offset => INTERVAL '3 days',
    end_offset => INTERVAL '1 hour',
    schedule_interval => INTERVAL '1 hour'
);
```

### Retention and Compression

```sql
-- Retention policy (drop old data)
SELECT add_retention_policy('{table_name}', INTERVAL '{retention_period}');

-- Compression settings
ALTER TABLE {table_name} SET (
    timescaledb.compress,
    timescaledb.compress_segmentby = '{segment_columns}',
    timescaledb.compress_orderby = 'time DESC'
);

-- Compression policy (compress old chunks)
SELECT add_compression_policy('{table_name}', INTERVAL '{compress_after}');

-- Manual compression (if needed)
SELECT compress_chunk(c.chunk_name)
FROM timescaledb_information.chunks c
WHERE c.hypertable_name = '{table_name}'
  AND c.range_end < NOW() - INTERVAL '7 days'
  AND NOT c.is_compressed;
```

---

## Data Vault 2.0 Templates

### Hub Template

```sql
CREATE TABLE hub_{business_concept} (
    {concept}_hk CHAR(32) PRIMARY KEY,          -- Hash key (MD5)
    {concept}_bk VARCHAR({length}) NOT NULL,    -- Business key
    load_dts TIMESTAMPTZ NOT NULL,
    record_source VARCHAR(100) NOT NULL
);

CREATE UNIQUE INDEX idx_hub_{concept}_bk ON hub_{concept}({concept}_bk);
```

### Link Template

```sql
CREATE TABLE link_{concept_a}_{concept_b} (
    {concept_a}_{concept_b}_hk CHAR(32) PRIMARY KEY,
    {concept_a}_hk CHAR(32) NOT NULL REFERENCES hub_{concept_a}({concept_a}_hk),
    {concept_b}_hk CHAR(32) NOT NULL REFERENCES hub_{concept_b}({concept_b}_hk),
    load_dts TIMESTAMPTZ NOT NULL,
    record_source VARCHAR(100) NOT NULL
);

CREATE INDEX idx_link_{a}_{b}_{a} ON link_{concept_a}_{concept_b}({concept_a}_hk);
CREATE INDEX idx_link_{a}_{b}_{b} ON link_{concept_a}_{concept_b}({concept_b}_hk);
```

### Satellite Template

```sql
CREATE TABLE sat_{hub_or_link}_{descriptor} (
    {parent}_hk CHAR(32) NOT NULL,
    load_dts TIMESTAMPTZ NOT NULL,
    load_end_dts TIMESTAMPTZ DEFAULT '9999-12-31 23:59:59',
    hash_diff CHAR(32) NOT NULL,
    record_source VARCHAR(100) NOT NULL,

    -- Descriptive attributes
    {attribute1} {type},
    {attribute2} {type},

    PRIMARY KEY ({parent}_hk, load_dts)
);

CREATE INDEX idx_sat_{descriptor}_current
    ON sat_{hub_or_link}_{descriptor}({parent}_hk)
    WHERE load_end_dts = '9999-12-31 23:59:59';
```

### Hash Key Generation

```sql
-- Standard hash key function
CREATE OR REPLACE FUNCTION generate_hash_key(business_key TEXT)
RETURNS CHAR(32) AS $$
BEGIN
    RETURN MD5(UPPER(TRIM(business_key)));
END;
$$ LANGUAGE plpgsql IMMUTABLE;

-- Composite hash key
CREATE OR REPLACE FUNCTION generate_composite_hash_key(
    key1 TEXT, key2 TEXT
) RETURNS CHAR(32) AS $$
BEGIN
    RETURN MD5(
        UPPER(TRIM(COALESCE(key1, ''))) || '|' ||
        UPPER(TRIM(COALESCE(key2, '')))
    );
END;
$$ LANGUAGE plpgsql IMMUTABLE;

-- Hash diff for change detection
CREATE OR REPLACE FUNCTION generate_hash_diff(VARIADIC attrs TEXT[])
RETURNS CHAR(32) AS $$
BEGIN
    RETURN MD5(array_to_string(attrs, '|'));
END;
$$ LANGUAGE plpgsql IMMUTABLE;
```

---

## SCD Type 2 Templates

### Dimension Table with SCD Type 2

```sql
CREATE TABLE dim_{entity} (
    {entity}_sk BIGSERIAL PRIMARY KEY,          -- Surrogate key
    {entity}_id VARCHAR({length}) NOT NULL,     -- Natural/business key

    -- Attributes
    {attribute1} {type},
    {attribute2} {type},

    -- SCD Type 2 tracking
    valid_from TIMESTAMPTZ NOT NULL,
    valid_to TIMESTAMPTZ NOT NULL DEFAULT '9999-12-31 23:59:59',
    is_current BOOLEAN NOT NULL DEFAULT TRUE,

    -- Audit
    hash_key CHAR(32),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_dim_{entity}_id ON dim_{entity}({entity}_id);
CREATE INDEX idx_dim_{entity}_current ON dim_{entity}({entity}_id)
    WHERE is_current = TRUE;
CREATE INDEX idx_dim_{entity}_valid ON dim_{entity}(valid_from, valid_to);
```

### SCD Type 2 Merge Procedure

```sql
CREATE OR REPLACE PROCEDURE upsert_dim_{entity}(
    p_{entity}_id VARCHAR,
    p_{attribute1} {type},
    p_{attribute2} {type}
)
LANGUAGE plpgsql AS $$
DECLARE
    v_hash_key CHAR(32);
    v_existing_hash CHAR(32);
BEGIN
    -- Generate hash of incoming attributes
    v_hash_key := MD5(
        COALESCE(p_{attribute1}::TEXT, '') || '|' ||
        COALESCE(p_{attribute2}::TEXT, '')
    );

    -- Get existing hash
    SELECT hash_key INTO v_existing_hash
    FROM dim_{entity}
    WHERE {entity}_id = p_{entity}_id
      AND is_current = TRUE;

    -- If no change, exit
    IF v_existing_hash = v_hash_key THEN
        RETURN;
    END IF;

    -- Close existing record
    UPDATE dim_{entity}
    SET valid_to = NOW(),
        is_current = FALSE,
        updated_at = NOW()
    WHERE {entity}_id = p_{entity}_id
      AND is_current = TRUE;

    -- Insert new version
    INSERT INTO dim_{entity} (
        {entity}_id,
        {attribute1},
        {attribute2},
        valid_from,
        is_current,
        hash_key
    ) VALUES (
        p_{entity}_id,
        p_{attribute1},
        p_{attribute2},
        NOW(),
        TRUE,
        v_hash_key
    );
END;
$$;
```

---

## Index Templates

### B-Tree Index (Default)

```sql
-- Single column
CREATE INDEX idx_{table}_{column} ON {table}({column});

-- Multi-column (composite) - order matters!
CREATE INDEX idx_{table}_{col1}_{col2} ON {table}({col1}, {col2});

-- Descending order
CREATE INDEX idx_{table}_{column}_desc ON {table}({column} DESC);

-- Partial index (filtered)
CREATE INDEX idx_{table}_active ON {table}({column})
    WHERE is_active = TRUE;

-- Covering index (includes additional columns)
CREATE INDEX idx_{table}_covering ON {table}({filter_col})
    INCLUDE ({select_col1}, {select_col2});
```

### Specialized Indexes

```sql
-- Full-text search (PostgreSQL)
CREATE INDEX idx_{table}_search ON {table}
    USING GIN (to_tsvector('english', {text_column}));

-- JSONB index
CREATE INDEX idx_{table}_jsonb ON {table}
    USING GIN ({jsonb_column});

-- JSONB path index
CREATE INDEX idx_{table}_jsonb_path ON {table}
    USING GIN (({jsonb_column} -> 'specific_key'));

-- Array index
CREATE INDEX idx_{table}_array ON {table}
    USING GIN ({array_column});

-- Range index (BRIN - for sorted data like timestamps)
CREATE INDEX idx_{table}_time_brin ON {table}
    USING BRIN ({timestamp_column});
```

---

## Naming Conventions

### Tables

```
Singular nouns: user, product, order
Snake_case: order_item, user_profile
No prefixes like tbl_
```

### Columns

```
Snake_case: first_name, created_at
Foreign keys: {referenced_table}_id
Booleans: is_, has_, can_ prefix
Timestamps: _at suffix (created_at, updated_at)
```

### Indexes

```
Pattern: idx_{table}_{columns}
Examples:
  idx_orders_user_id
  idx_orders_status_created
  idx_products_active
```

### Constraints

```
Primary key: pk_{table}
Foreign key: fk_{table}_{referenced}
Unique: uq_{table}_{columns}
Check: ck_{table}_{description}
```

### Example Naming

```sql
-- Consistent naming example
CREATE TABLE order_items (
    id UUID PRIMARY KEY,                           -- pk_order_items
    order_id UUID REFERENCES orders(id),           -- fk_order_items_orders
    product_id UUID REFERENCES products(id),       -- fk_order_items_products
    quantity INT NOT NULL CHECK (quantity > 0),    -- ck_order_items_quantity
    unit_price DECIMAL(10,2) NOT NULL,
    is_gift BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_order_items_order ON order_items(order_id);
CREATE INDEX idx_order_items_product ON order_items(product_id);
CREATE UNIQUE INDEX uq_order_items_order_product ON order_items(order_id, product_id);
```
