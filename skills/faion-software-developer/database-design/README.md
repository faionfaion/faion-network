# Database Design

Structuring data storage for integrity, performance, and maintainability.

## When to Use

- Starting new projects with persistent data
- Adding features requiring schema changes
- Migrating between database systems
- Performance optimization requiring refactoring
- Scaling applications

## Key Principles

- Normalize first, denormalize for performance (start with 3NF)
- Design for queries (understand access patterns)
- Enforce integrity at database level (constraints, foreign keys)
- Plan for growth (partitioning, sharding)
- Document everything (diagrams, relationships, business rules)

## Entity-Relationship Modeling

```sql
-- E-commerce schema with proper relationships
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE products (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    sku VARCHAR(50) NOT NULL UNIQUE,
    name VARCHAR(255) NOT NULL,
    price DECIMAL(10, 2) NOT NULL CHECK (price >= 0),
    stock_quantity INTEGER NOT NULL DEFAULT 0 CHECK (stock_quantity >= 0),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE orders (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
    status VARCHAR(20) NOT NULL DEFAULT 'pending'
        CHECK (status IN ('pending', 'processing', 'shipped', 'delivered', 'cancelled')),
    total_amount DECIMAL(12, 2) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE order_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_id UUID NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    product_id UUID NOT NULL REFERENCES products(id) ON DELETE RESTRICT,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    unit_price DECIMAL(10, 2) NOT NULL,
    UNIQUE(order_id, product_id)
);
```

## Indexing Strategy

```sql
-- Index based on query patterns
-- Query: Find orders by user, sorted by date
CREATE INDEX idx_orders_user_created ON orders(user_id, created_at DESC);

-- Query: Search products by name
CREATE INDEX idx_products_name_trgm ON products
    USING gin(name gin_trgm_ops);

-- Query: Find pending orders for processing
CREATE INDEX idx_orders_status_pending ON orders(created_at)
    WHERE status = 'pending';

-- Composite index for common join pattern
CREATE INDEX idx_order_items_order_product ON order_items(order_id, product_id);
```

## Soft Deletes

```sql
-- Add soft delete capability
ALTER TABLE users ADD COLUMN deleted_at TIMESTAMP WITH TIME ZONE;

-- Create view for active users
CREATE VIEW active_users AS
SELECT * FROM users WHERE deleted_at IS NULL;

-- Partial index for queries on active records
CREATE INDEX idx_users_email_active ON users(email)
    WHERE deleted_at IS NULL;
```

## Audit Trail

```sql
-- Audit table for tracking changes
CREATE TABLE audit_log (
    id BIGSERIAL PRIMARY KEY,
    table_name VARCHAR(50) NOT NULL,
    record_id UUID NOT NULL,
    action VARCHAR(10) NOT NULL CHECK (action IN ('INSERT', 'UPDATE', 'DELETE')),
    old_data JSONB,
    new_data JSONB,
    changed_by UUID REFERENCES users(id),
    changed_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Trigger function for automatic auditing
CREATE OR REPLACE FUNCTION audit_trigger_func()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        INSERT INTO audit_log(table_name, record_id, action, new_data)
        VALUES (TG_TABLE_NAME, NEW.id, 'INSERT', to_jsonb(NEW));
    ELSIF TG_OP = 'UPDATE' THEN
        INSERT INTO audit_log(table_name, record_id, action, old_data, new_data)
        VALUES (TG_TABLE_NAME, NEW.id, 'UPDATE', to_jsonb(OLD), to_jsonb(NEW));
    ELSIF TG_OP = 'DELETE' THEN
        INSERT INTO audit_log(table_name, record_id, action, old_data)
        VALUES (TG_TABLE_NAME, OLD.id, 'DELETE', to_jsonb(OLD));
    END IF;
    RETURN COALESCE(NEW, OLD);
END;
$$ LANGUAGE plpgsql;

-- Apply to table
CREATE TRIGGER users_audit_trigger
AFTER INSERT OR UPDATE OR DELETE ON users
FOR EACH ROW EXECUTE FUNCTION audit_trigger_func();
```

## Migration Strategy

```python
# Alembic migration example
"""Add user preferences table

Revision ID: a1b2c3d4e5f6
Revises: 9z8y7x6w5v4u
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    op.create_table(
        'user_preferences',
        sa.Column('id', postgresql.UUID(), primary_key=True),
        sa.Column('user_id', postgresql.UUID(), nullable=False),
        sa.Column('theme', sa.String(20), default='light'),
        sa.Column('notifications_enabled', sa.Boolean(), default=True),
        sa.Column('language', sa.String(5), default='en'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.UniqueConstraint('user_id')
    )
    op.create_index('idx_user_prefs_user', 'user_preferences', ['user_id'])

def downgrade():
    op.drop_table('user_preferences')
```

## Partitioning

```sql
-- Range partitioning by created_at
CREATE TABLE orders_partitioned (
    id UUID,
    user_id UUID,
    status VARCHAR(20),
    total_amount DECIMAL(12, 2),
    created_at TIMESTAMP WITH TIME ZONE
) PARTITION BY RANGE (created_at);

-- Create partitions
CREATE TABLE orders_2024_q1 PARTITION OF orders_partitioned
    FOR VALUES FROM ('2024-01-01') TO ('2024-04-01');

CREATE TABLE orders_2024_q2 PARTITION OF orders_partitioned
    FOR VALUES FROM ('2024-04-01') TO ('2024-07-01');

-- Index on each partition
CREATE INDEX idx_orders_2024_q1_user ON orders_2024_q1(user_id);
```

## Denormalization for Performance

```sql
-- Add computed columns to avoid joins
ALTER TABLE orders ADD COLUMN user_email VARCHAR(255);

-- Maintain with trigger
CREATE OR REPLACE FUNCTION sync_user_email()
RETURNS TRIGGER AS $$
BEGIN
    NEW.user_email := (SELECT email FROM users WHERE id = NEW.user_id);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER orders_sync_email
BEFORE INSERT OR UPDATE ON orders
FOR EACH ROW EXECUTE FUNCTION sync_user_email();
```

## Materialized Views

```sql
-- Aggregate data for reporting
CREATE MATERIALIZED VIEW order_stats AS
SELECT
    DATE_TRUNC('day', created_at) AS order_date,
    COUNT(*) AS total_orders,
    SUM(total_amount) AS total_revenue,
    AVG(total_amount) AS avg_order_value
FROM orders
WHERE status = 'delivered'
GROUP BY DATE_TRUNC('day', created_at);

-- Index for fast queries
CREATE INDEX idx_order_stats_date ON order_stats(order_date);

-- Refresh strategy
REFRESH MATERIALIZED VIEW CONCURRENTLY order_stats;
```

## Anti-patterns

- God tables (50+ columns for everything)
- Missing foreign keys (relying on app logic)
- Over-indexing (index on every column)
- EAV abuse for structured data
- No constraints (missing CHECK, NOT NULL, UNIQUE)
- Storing computed values that can become stale
- VARCHAR(255) everywhere without considering requirements


## Agent Selection

| Task | Model | Rationale |
|------|-------|-----------|
| Implementation setup | haiku | Applying standard methodology patterns |
| Design decisions | sonnet | Trade-offs analysis |
| Complex scenarios | opus | Novel or complex solutions |
## Sources

- [PostgreSQL Documentation](https://www.postgresql.org/docs/current/)
- [PostgreSQL Partitioning](https://www.postgresql.org/docs/current/ddl-partitioning.html)
- [Use The Index, Luke](https://use-the-index-luke.com/)
- [Alembic Tutorial](https://alembic.sqlalchemy.org/en/latest/tutorial.html)
- [PostgreSQL Indexing](https://www.postgresql.org/docs/current/indexes.html)
