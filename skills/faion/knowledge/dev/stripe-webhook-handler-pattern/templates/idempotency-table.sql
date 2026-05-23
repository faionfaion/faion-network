-- purpose: Postgres schema for event-id idempotency table.
-- consumes: see content/02-output-contract.xml inputs for stripe-webhook-handler-pattern
-- produces: artefact conforming to content/02-output-contract.xml
-- depends-on: content/01-core-rules.xml + content/04-procedure.xml
-- token-budget-impact: ~200-700 tokens when loaded as context

CREATE TABLE IF NOT EXISTS stripe_events (
    event_id TEXT PRIMARY KEY,
    event_type TEXT NOT NULL,
    received_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    processed_at TIMESTAMPTZ,
    payload JSONB NOT NULL
);

CREATE INDEX IF NOT EXISTS ix_stripe_events_type_received
    ON stripe_events (event_type, received_at DESC);
