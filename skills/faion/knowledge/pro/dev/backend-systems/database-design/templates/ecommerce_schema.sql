-- purpose: Legacy template for the database-design methodology.
-- consumes: inputs declared in database-design/AGENTS.md prerequisites.
-- produces: working code/config aligned with content/01-core-rules.xml.
-- depends-on: content/02-output-contract.xml schema for output shape.
-- token-budget-impact: ~600 tokens when loaded as reference.
-- E-commerce schema: PostgreSQL 14+
-- PK strategy: UUID (gen_random_uuid). Prefer UUIDv7 at scale.
-- All timestamps: TIMESTAMPTZ (UTC always).

CREATE EXTENSION IF NOT EXISTS pg_trgm;  -- for GIN text search

-- Users
CREATE TABLE users (
    id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email         VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at    TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at    TIMESTAMPTZ NOT NULL DEFAULT now(),
    deleted_at    TIMESTAMPTZ          -- soft delete
);

CREATE INDEX idx_users_email_active ON users(email)
    WHERE deleted_at IS NULL;

CREATE VIEW active_users AS
    SELECT * FROM users WHERE deleted_at IS NULL;

-- Products
CREATE TABLE products (
    id             UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    sku            VARCHAR(50) NOT NULL UNIQUE,
    name           TEXT NOT NULL,
    price          NUMERIC(10, 2) NOT NULL CHECK (price >= 0),
    stock_quantity INTEGER NOT NULL DEFAULT 0 CHECK (stock_quantity >= 0),
    created_at     TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_products_name_trgm ON products
    USING gin(name gin_trgm_ops);

-- Orders
CREATE TABLE orders (
    id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id      UUID NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
    status       VARCHAR(20) NOT NULL DEFAULT 'pending'
                     CHECK (status IN ('pending', 'processing', 'shipped', 'delivered', 'cancelled')),
    total_amount NUMERIC(12, 2) NOT NULL CHECK (total_amount >= 0),
    created_at   TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_orders_user_created   ON orders(user_id, created_at DESC);
CREATE INDEX idx_orders_pending        ON orders(created_at) WHERE status = 'pending';

-- Order items
CREATE TABLE order_items (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_id    UUID NOT NULL REFERENCES orders(id)   ON DELETE CASCADE,
    product_id  UUID NOT NULL REFERENCES products(id) ON DELETE RESTRICT,
    quantity    INTEGER NOT NULL CHECK (quantity > 0),
    unit_price  NUMERIC(10, 2) NOT NULL CHECK (unit_price >= 0),
    UNIQUE (order_id, product_id)
);

CREATE INDEX idx_order_items_order ON order_items(order_id);
