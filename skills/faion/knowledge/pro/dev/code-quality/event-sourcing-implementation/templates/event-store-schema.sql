-- Event store schema for PostgreSQL event sourcing implementation

-- Core events table
CREATE TABLE events (
    id           BIGSERIAL    PRIMARY KEY,
    event_id     UUID         NOT NULL UNIQUE,
    stream_id    VARCHAR(255) NOT NULL,
    version      INTEGER      NOT NULL,
    event_type   VARCHAR(255) NOT NULL,
    event_data   JSONB        NOT NULL,
    metadata     JSONB        NOT NULL DEFAULT '{}',
    occurred_at  TIMESTAMP    NOT NULL,
    created_at   TIMESTAMP    NOT NULL DEFAULT NOW(),

    -- Optimistic concurrency: concurrent appends to same version fail
    CONSTRAINT events_stream_version_unique UNIQUE (stream_id, version)
);

CREATE INDEX events_stream_id_idx   ON events(stream_id);
CREATE INDEX events_event_type_idx  ON events(event_type);
CREATE INDEX events_occurred_at_idx ON events(occurred_at);

-- Snapshots table (one snapshot per stream, UPSERT)
CREATE TABLE snapshots (
    stream_id   VARCHAR(255) PRIMARY KEY,
    version     INTEGER      NOT NULL,
    state       JSONB        NOT NULL,
    created_at  TIMESTAMP    NOT NULL
);

-- Example projection: order details read model
CREATE TABLE order_details (
    order_id     UUID         PRIMARY KEY,
    customer_id  UUID         NOT NULL,
    status       VARCHAR(50)  NOT NULL,
    created_at   TIMESTAMP    NOT NULL,
    placed_at    TIMESTAMP,
    shipped_at   TIMESTAMP,
    delivered_at TIMESTAMP
);

CREATE TABLE order_items (
    id           BIGSERIAL      PRIMARY KEY,
    order_id     UUID           NOT NULL REFERENCES order_details(order_id),
    product_id   UUID           NOT NULL,
    product_name VARCHAR(255)   NOT NULL,
    quantity     INTEGER        NOT NULL,
    unit_price   DECIMAL(10, 2) NOT NULL
);
