# Cohort Implementation

## Summary

**One-sentence:** Generates the SQL + warehouse config for weekly retention cohorts (signup-week x week-N) with event-table schema and chart spec.

**One-paragraph:** Generates the SQL + warehouse config for weekly retention cohorts (signup-week x week-N) with event-table schema and chart spec. Use it when team має warehouse + event-table (snowflake / bigquery / postgres). The methodology pins the artefact shape via JSON Schema in `content/02-output-contract.xml`, so a downstream agent can validate the output mechanically rather than by prose review.

**Ефективно для:**

- Team має warehouse + event-table (Snowflake / BigQuery / Postgres).
- Потрібен weekly retention curve по cohort + visual chart.
- Stable user_id у events, не anonymous distinct_id.
- Готовність змінити SQL контракт коли event schema еволюціонує.

## Applies If (ALL must hold)

- A warehouse (BigQuery, Snowflake, Postgres or Redshift) holds a users table with signup timestamps and an events table with per-user events, built with dbt or equivalent.
- Events and users carry a stable post-identification `user_id`, resolved in staging before this model reads them.
- Signup and event timestamps are stored in UTC or convertible to UTC columns with a known source zone.
- One event can be named as "came back" for this product and a fixed set of day offsets is agreed.
- The team will run a full backfill whenever the retention event or the offsets change.

## Skip If (ANY kills it)

- No warehouse or no event table: use the analytics vendor's built-in cohort report instead.
- Events carry only `distinct_id`, device or cookie ids: resolve identity in staging first; cohorts on anonymous ids under-report retention.
- Timestamps exist only in local time with no source zone: add UTC columns before truncating to cohort weeks.
- The question is which event predicts retention: that is activation-framework's D30 validation; this methodology implements the curve for an already chosen event.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Staging users model | `stg_users` with `user_id`, `signup_ts_utc` | dbt staging layer |
| Staging events model | `stg_events` with `user_id`, `event_type`, `event_ts_utc`, identity resolved | dbt staging layer |
| Retention event and offsets | event name; integer day offsets (template: 1, 7, 14, 30, 60, 90) | growth team decision |
| Warehouse engine | one of bigquery, snowflake, postgres, redshift | data platform |
| Data cutoff date | YYYY-MM-DD of the latest complete data | the reporting run |
| `templates/cohort-retention-weekly.sql`, `templates/schema.yml` | dbt model and tests skeletons | this methodology |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `pro/marketing/growth-marketer/AGENTS.md` | Parent skill vocabulary + neighbouring methodologies |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 9 rules: Monday UTC cohort week, stable user_id, retention event declared once, fixed day offsets with test, events after signup only, full-cohort denominator, immature cells null, incremental key and 90-day lookback, settings declare engine and event | 1900 |
| `content/02-output-contract.xml` | essential | Draft-07 schema of the cohort config: settings (engine, event, offsets, Monday, UTC), sources with user_id and UTC columns, incremental model with composite key, partition, lookback and Monday-UTC expression, dbt tests, chart spec with cutoff and null immature cells, computed cells; valid and invalid configs; 8 forbidden patterns | ~3650 |
| `content/03-failure-modes.xml` | essential | 3+ antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | 7 steps: confirm sources and identity, declare event and offsets once, write the incremental model, wire the tests, set the chart spec and denominator, backfill and validate, version any event change | ~1500 |
| `content/05-examples.xml` | recommended | Complete BigQuery config (login at 1 / 7 / 14 / 30 / 60 / 90, 90-day lookback, tests, May 4 cutoff, five cells with one immature) with a note per value, plus the config as usually written and what the validator prints | ~1850 |
| `content/06-decision-tree.xml` | essential | Decision tree: observable signals -> rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `gather-inputs` | haiku | Mechanical extraction from upstream artefacts |
| `apply-rules` | sonnet | Apply `01-core-rules.xml` + decision tree against state |
| `synthesise-output` | sonnet | Final artefact authoring matching `02-output-contract.xml` |
| `validate-output` | haiku | Run `scripts/validate-cohort-implementation.py` against the artefact |

## Templates

| File | Purpose |
|------|---------|
| `templates/cohort-implementation.config.yaml` | YAML config skeleton matching the contract: settings, sources, incremental model, tests, chart spec, cells |
| `templates/cohort-implementation.example.json` | Example output JSON conforming to 02-output-contract.xml |
| `templates/_smoke-test.json` | Minimum viable filled-in artefact for the validator self-test |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-cohort-implementation.py` | Validate produced artefact against `02-output-contract.xml` schema | After `synthesise-output`, before commit/publish |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- parent skill: `pro/marketing/growth-marketer/`
- [[ab-testing-setup]]
- [[north-star-metric]]
- [[activation-framework]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (artefact shape, freshness, scope) to either a `run-the-methodology` conclusion or a `skip-this-methodology` conclusion, with every leaf referencing a rule id from `01-core-rules.xml`. Use it when the operator is unsure whether this methodology applies to the current task.
