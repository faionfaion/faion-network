-- Schema-per-module isolation in PostgreSQL
-- Each module owns its schema; no cross-schema foreign keys.

CREATE SCHEMA IF NOT EXISTS users;
CREATE SCHEMA IF NOT EXISTS orders;
CREATE SCHEMA IF NOT EXISTS payments;
CREATE SCHEMA IF NOT EXISTS inventory;

-- Optional: enforce isolation at the DB level with separate roles
CREATE ROLE orders_owner;
GRANT ALL ON SCHEMA orders TO orders_owner;
REVOKE ALL ON SCHEMA users FROM orders_owner;
REVOKE ALL ON SCHEMA payments FROM orders_owner;

-- Example: orders schema references users by ID only (no FK to users schema)
CREATE TABLE orders.orders (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,  -- Reference by ID only; no REFERENCES users.accounts(id)
    status VARCHAR(30) NOT NULL DEFAULT 'pending',
    total_amount DECIMAL(12, 2) NOT NULL,
    customer_name VARCHAR(255) NOT NULL,  -- Denormalized at write time
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE orders.order_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_id UUID NOT NULL REFERENCES orders.orders(id) ON DELETE CASCADE,
    product_id UUID NOT NULL,            -- Reference by ID only; no FK to catalog schema
    product_name VARCHAR(255) NOT NULL,  -- Denormalized for order history
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    unit_price DECIMAL(12, 2) NOT NULL,
    total_price DECIMAL(12, 2) NOT NULL
);

CREATE INDEX idx_orders_user_id ON orders.orders(user_id);
CREATE INDEX idx_orders_status ON orders.orders(status);
