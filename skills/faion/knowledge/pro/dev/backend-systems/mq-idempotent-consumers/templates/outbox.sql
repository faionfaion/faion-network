-- purpose: smoke DDL for mq-idempotent-consumers
-- consumes: schema decision
-- produces: outbox table
-- depends-on: scripts/validate-mq-idempotent-consumers.py
-- token-budget-impact: ~250 tokens
-- transactional outbox table
CREATE TABLE IF NOT EXISTS outbox_messages (
    id BIGSERIAL PRIMARY KEY,
    aggregate_type TEXT NOT NULL,
    aggregate_id TEXT NOT NULL,
    event_type TEXT NOT NULL,
    payload JSONB NOT NULL,
    idempotency_key TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    published_at TIMESTAMPTZ
);
CREATE INDEX IF NOT EXISTS outbox_unpublished ON outbox_messages (created_at) WHERE published_at IS NULL;
CREATE UNIQUE INDEX IF NOT EXISTS outbox_idempotency_key ON outbox_messages (idempotency_key);
