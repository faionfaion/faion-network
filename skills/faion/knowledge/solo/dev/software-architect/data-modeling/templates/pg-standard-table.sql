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
