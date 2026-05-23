-- purpose: Operational metrics warehouse schema
-- consumes: manual ingest or ETL
-- produces: tables: north_star_daily, funnel_events, retention_cohorts
-- depends-on: warehouse (DuckDB / Postgres)
-- token-budget-impact: low

CREATE TABLE IF NOT EXISTS north_star_daily (
  day DATE PRIMARY KEY,
  value NUMERIC NOT NULL,
  notes TEXT
);

CREATE TABLE IF NOT EXISTS funnel_events (
  ts TIMESTAMP NOT NULL,
  user_id TEXT NOT NULL,
  step TEXT NOT NULL,
  meta JSONB
);

CREATE TABLE IF NOT EXISTS retention_cohorts (
  cohort_week TEXT NOT NULL,
  week_offset INT NOT NULL,
  retained INT NOT NULL,
  PRIMARY KEY (cohort_week, week_offset)
);
