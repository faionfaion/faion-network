# ActiveRecord Patterns for Rails

## Summary

**One-sentence:** Rails ActiveRecord methodology — composable Query Objects, named scopes (no default_scope), eager-load at the controller boundary, find_each for bulk, Bullet + Prosopite N+1 gates in CI.

**One-paragraph:** Patterns for Rails 7+ ActiveRecord. Query Objects accept a relation in the constructor (default `Model.all`), chain methods that return `self`, and expose a terminal `results` returning the relation (never an array). Named scopes (`scope :active`) replace `default_scope`. Eager-loading happens at the controller boundary via `.includes`/`.preload`/`.eager_load`. Bulk iteration uses `find_each` / `in_batches`. CI gates N+1 with Bullet (development) + Prosopite (CI), and runs `n_plus_one_query` middleware in feature specs.

**Ефективно для:**

- Rails apps where models exceed ~150 lines and inline `where` chains scatter across controllers.
- Multi-tenant Rails apps where scopes + tenant-aware queries must be enforced consistently.
- Measured ORM hot paths (>30 % of request time in AR) — Query Objects + eager loading measurably improve.
- LLM-driven feature work where each AR query must be reviewable in isolation.
- Codebases adopting Trailblazer / dry-rb partials — Query Objects play nicely as ingest.

## Applies If (ALL must hold)

- Rails 7+ app on Ruby 3.1+.
- Codebase has ≥5 models with meaningful relations.
- Performance-sensitive endpoints in the hot path.

## Skip If (ANY kills it)

- Simple CRUD admin (Rails Admin / ActiveAdmin) — the framework manages queries.
- Rails apps under 1k LOC — direct AR scope blocks + thin controllers are fine.
- Read-replicas or sharded DBs needing raw `connected_to(role: :reading)` — query-object DSL hides the switch.
- Background workers operating on enqueued IDs via `find_each` — no benefit from a chained query object.
- Reporting / analytics — drop to `ActiveRecord::Base.connection.execute` with explicit SQL.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Model list | Markdown | data modelling |
| Filter taxonomy | Markdown | product / BA |
| N+1 gate config | YAML | platform |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[ruby-rails]] | Umbrella for controller / service layering. |
| [[decomposition-rails]] | Service / Query / Form decomposition. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 10 rules: query-object-relation-chain, named-scopes-no-default-scope, eager-load-at-boundary, find-each-for-bulk, no-arel-string-injection, n-plus-one-gate-in-ci, transaction-block-multi-write, enum-for-status, no-time-now, counter-cache-for-counts | 1800 |
| `content/02-output-contract.xml` | essential | JSON Schema for the AR-discipline manifest + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 8 antipatterns: default-scope-invisible, query-object-god-class, view-triggered-query, all-each-memory-blowup, scope-on-query-object-bypassed, missing-transaction, magic-status-strings, time-now-timezone-bug | 1400 |
| `content/04-procedure.xml` | essential | 7-step procedure: identify hot path → extract Query Object → eager-load at boundary → find_each for bulk → N+1 gate → enum + counter_cache → transactions and timezone lint | 1100 |
| `content/05-examples.xml` | essential | Worked Order hardening + the hardened model shape in Ruby | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree mapping observable signals to a rule from 01-core-rules.xml | 800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `extract-query-object` | sonnet | Composition design + chain shape needs judgment. |
| `audit-n-plus-one` | haiku | Mechanical scan with `ar-budget.sh`. |
| `design-bulk-job` | opus | `find_each` vs explicit batch SQL trade-off. |

## Templates

| File | Purpose |
|------|---------|
| `templates/ar-budget.sh` | CI helper running Prosopite N+1 assertions across the request spec suite. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ruby-activerecord.py` | Validate the AR-discipline manifest against the JSON Schema. | Pre-commit; CI on every methodology PR. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[ruby-rails]]
- [[ruby-rails-patterns]]
- [[decomposition-rails]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (model count, hot path, batch size) to a rule from `01-core-rules.xml`. Use it before extracting a Query Object or optimising a query.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/ar-budget.sh`

```bash
# ar-budget.sh — fail CI on N+1 or queries over per-spec budget.
# Usage: ar-budget.sh [BUDGET]
# Requires: bullet and prosopite gems in test group.
set -euo pipefail
BUDGET="${1:-15}"
export BULLET=true PROSOPITE=true
LOG=$(mktemp)
bundle exec rspec --format documentation 2>&1 | tee "$LOG"
ruby -e '
budget = ARGV[0].to_i
log = File.read(ARGV[1])
fails = []
log.scan(/^(.+?_spec\.rb:\d+).*?queries:\s*(\d+)/m) do |loc, n|
  fails << [loc, n.to_i] if n.to_i > budget
end
nplus1 = log.scan(/USE eager loading detected.*$/).length \
  + log.scan(/Prosopite::NPlusOneQueriesError/).length
unless fails.empty? && nplus1.zero?
  puts "FAIL: #{nplus1} N+1, #{fails.size} budget breaches"
  fails.each { |loc, n| puts "  #{loc}: #{n} queries (>#{budget})" }
  exit 1
end
puts "OK: zero N+1, all specs within #{budget} queries"
' "$BUDGET" "$LOG"
bundle exec rake lol_dba:missing_indexes || true
```
