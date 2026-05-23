-- purpose: snapshot storage table DDL
-- consumes: nothing
-- produces: aggregate_snapshots table with schema_version + payload
-- depends-on: content/01-core-rules.xml
-- token-budget-impact: ~100 tokens when loaded as reference

CREATE TABLE IF NOT EXISTS aggregate_snapshots (
    aggregate_type    TEXT NOT NULL,
    stream_id         UUID NOT NULL,
    snapshot_version  BIGINT NOT NULL,
    schema_version    INTEGER NOT NULL,
    payload           JSONB NOT NULL,
    created_at        TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (aggregate_type, stream_id, snapshot_version)
);

CREATE INDEX IF NOT EXISTS idx_aggregate_snapshots_latest
    ON aggregate_snapshots (aggregate_type, stream_id, snapshot_version DESC);
