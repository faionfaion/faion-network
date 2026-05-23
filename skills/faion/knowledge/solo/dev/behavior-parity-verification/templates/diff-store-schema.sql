-- purpose: Postgres DDL for the parity_diffs sampler write target.
-- consumes: nothing — applied to the shadow store before sampler starts.
-- produces: parity_diffs table ready for diff inserts and cluster grouping.
-- depends-on: PostgreSQL 14+ (JSONB, generated columns).
-- token-budget-impact: ~150 tokens when loaded as context.

CREATE TABLE IF NOT EXISTS parity_diffs (
    id                BIGSERIAL PRIMARY KEY,
    scope             TEXT NOT NULL,
    ramp_stage        SMALLINT NOT NULL CHECK (ramp_stage BETWEEN 1 AND 4),
    sampled_at        TIMESTAMPTZ NOT NULL DEFAULT now(),
    input_fingerprint TEXT NOT NULL,
    legacy_hash       TEXT NOT NULL,
    new_hash          TEXT NOT NULL,
    diff_json         JSONB NOT NULL,
    cluster_id        TEXT,
    redaction_applied BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE INDEX IF NOT EXISTS idx_parity_diffs_scope_stage  ON parity_diffs (scope, ramp_stage);
CREATE INDEX IF NOT EXISTS idx_parity_diffs_cluster      ON parity_diffs (cluster_id) WHERE cluster_id IS NOT NULL;
CREATE INDEX IF NOT EXISTS idx_parity_diffs_sampled_at   ON parity_diffs (sampled_at);

COMMENT ON COLUMN parity_diffs.redaction_applied IS 'MUST be true on insert. PII redaction precedes persistence.';
