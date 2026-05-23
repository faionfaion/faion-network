-- purpose: PostgreSQL DDL with append-only constraints + snapshots table.
-- consumes: see content/02-output-contract.xml inputs
-- produces: artefact conforming to content/02-output-contract.xml (event-sourcing-implementation)
-- depends-on: content/01-core-rules.xml
-- token-budget-impact: small (template is loaded only when an artefact is being authored)
-- append-only events table + per-aggregate version uniqueness
CREATE TABLE events (
    event_id        UUID         PRIMARY KEY,
    aggregate_id    UUID         NOT NULL,
    aggregate_type  TEXT         NOT NULL,
    event_type      TEXT         NOT NULL,
    payload         JSONB        NOT NULL,
    occurred_at     TIMESTAMPTZ  NOT NULL DEFAULT now(),
    version         INTEGER      NOT NULL,
    UNIQUE (aggregate_id, version)
);
CREATE INDEX events_aggregate_idx ON events(aggregate_id, version);
REVOKE UPDATE, DELETE ON events FROM PUBLIC;  -- append-only at grant level

CREATE TABLE snapshots (
    aggregate_id    UUID         NOT NULL,
    version         INTEGER      NOT NULL,
    state           JSONB        NOT NULL,
    captured_at     TIMESTAMPTZ  NOT NULL DEFAULT now(),
    PRIMARY KEY (aggregate_id, version)
);
