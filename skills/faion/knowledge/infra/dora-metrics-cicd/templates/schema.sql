-- purpose: SQL schema for deploys + incidents join
-- consumes: deploy + incident event streams
-- produces: joined table for DORA metrics
-- depends-on: content/01-core-rules.xml
-- token-budget-impact: ~150 tokens when loaded as context

CREATE TABLE IF NOT EXISTS deploys (
    id BIGINT PRIMARY KEY,
    service TEXT NOT NULL,
    env TEXT NOT NULL,
    commit_sha TEXT NOT NULL,
    deployed_at TIMESTAMPTZ NOT NULL
);
