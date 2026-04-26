-- ops-store/schema.sql — canonical Product Ops data schema.
-- Intended to be dbt-modelled afterwards. Each table maps to one source domain.
-- All cross-system IDs (Productboard, Jira, Linear) stored in source column.

create table feature (
  id           text primary key,        -- canonical ID (e.g. PB-123)
  source       text,                    -- productboard | jira | linear | github
  title        text,
  owner        text,
  status       text,
  target_date  date,
  outcome      text,                    -- referenced outcome statement
  metric       text,                    -- primary success metric
  updated_at   timestamptz
);

create table release (
  id                   text primary key,
  name                 text,
  ships_on             date,
  scope_feature_ids    text[],          -- references feature.id[]
  readiness_score      numeric,
  updated_at           timestamptz
);

create table risk (
  id           serial primary key,
  feature_id   text references feature(id),
  kind         text,                    -- scope | dependency | resource | market
  severity     int,                     -- 1-5
  opened_at    timestamptz,
  closed_at    timestamptz,
  note         text
);

create table metric_kpi (
  id                text primary key,
  name              text,
  definition_sql    text,               -- canonical SQL; never re-derive from prose
  owner             text,
  target            numeric,
  current           numeric,
  last_computed     timestamptz
);
