-- purpose: checkpoint table DDL used by every projection
-- consumes: nothing
-- produces: projection_checkpoint table
-- depends-on: content/01-core-rules.xml
-- token-budget-impact: ~50 tokens when loaded as reference

CREATE TABLE IF NOT EXISTS projection_checkpoint (
    name             TEXT PRIMARY KEY,
    stream_position  BIGINT NOT NULL,
    updated_at       TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
