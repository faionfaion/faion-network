# Dual-Write Shadow-Read Template

## Summary

**One-sentence:** Produces a migration runbook for dual-write + shadow-read cutovers (Postgres major upgrade, monolith-to-service split, schema rewrite) — write path fan-out, read parity diff, rollback gate, owner — so big-bang migrations stop being heroics.

**One-paragraph:** Produces a migration runbook for dual-write + shadow-read cutovers (Postgres major upgrade, monolith-to-service split, schema rewrite) — write path fan-out, read parity diff, rollback gate, owner — so big-bang migrations stop being heroics. The methodology pins shape + owner + evidence + outcome review so the artefact becomes a reviewable operating tool rather than folklore. Inputs are validated against a JSON schema; outputs are gated by the `## Decision tree` so the agent skips the methodology when preconditions don't hold.

**Ефективно для:** software architects and senior engineers running a high-risk migration who need a reference dual-write + shadow-read pattern with parity-diff gates instead of inventing the playbook mid-cutover.

## Applies If (ALL must hold)

- The change moves data between two stores and cannot be done as one transactional migration with a tested down-migration: a Postgres major upgrade, a monolith-to-service split, a schema rewrite, a datastore swap.
- Every entity type being migrated has a primary key and a monotonic version per row (row version, updated_at, or a change-data-capture log sequence number), so writes can be version-guarded upserts.
- A runtime feature-flag system exists that can flip four independent flags without a deploy.
- Metrics and dashboards can publish dual_write_failures_total, reconciliation_repairs_total and shadow_read_mismatch_ratio per entity type.
- Named people (an architect or DBA) will review the parity gate evidence before reads are flipped and before old-store writes are turned off.

## Skip If (ANY kills it)

- The change fits inside one store as a single transactional migration with a tested down-migration; dual-write and shadow-read machinery adds risk without reducing it.
- The new store is not yet deployable in production (no capacity, no network path), so there is nothing to dual-write to; provision it first.
- The entity types have no version or timestamp column and CDC is unavailable, so writes cannot be made idempotent; add the version column as its own migration first.
- The migration is already past read cutover with the old store decommissioned; the runbook cannot be retrofitted and the remaining work is an incident review.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Entity type inventory | table or aggregate name, primary key, version field per entity | data model / schema |
| Write and read path code | the service code that writes and reads the entities | application repository |
| Feature-flag system | four runtime flags with names and owners | flag service (OpenFeature, LaunchDarkly, internal) |
| Metrics and dashboards | dual_write_failures_total, reconciliation_repairs_total, shadow_read_mismatch_ratio per entity | observability stack |
| Old-store p99 read latency | measured per entity type at runbook time | APM / tracing |
| Named approvers | role:handle for read cutover and for write-to-old off | architecture / DBA on-call |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `[[code-review]]` | Peer methodology that reviews the artefact before merge. |
| `[[incident-decision-template]]` | Peer methodology for incident-time decisions referenced by this artefact. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 8 rules: idempotent fan-out, old store authoritative, reconciliation job, backfill order, parity diff, shadow-read isolation, numeric cutover gate, per-stage rollback flags | ~1950 |
| `content/02-output-contract.xml` | essential | Draft-07 schema for the runbook: entity_types with key, version field, parity exclusions and a numeric gate (ratio under 1, window, minimum comparisons), version-guarded dual write outside the old transaction with retry queue and failure metric, reconciliation job with cadence and repair budget declared before dual-write, backfill after dual-write with the same upsert and count / checksum verification, normalising shadow read returning the old result with bounded timeout and sampling under 100, four runtime flags with reverse order, retention window and rehearsed flip-back, named approvers with gate evaluation once reads flip; valid and invalid examples | ~4750 |
| `content/03-failure-modes.xml` | essential | 7 antipatterns with detector + repair | ~950 |
| `content/04-procedure.xml` | recommended | 9 steps: entity types and gates, version-guarded dual write, reconciliation, dual-write then backfill with verification, four flags and reverse order, sampled shadow reads, gate evaluation and read flip with approver, retention window and flip-back rehearsal, validate and file | ~2050 |
| `content/05-examples.xml` | recommended | Complete Postgres 13 to 16 runbook after read cutover with notes on every non-obvious value, plus the first draft breaking all eight rules and what the validator and architect say | ~2600 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion(ref=rule-id) | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Parse inputs + check preconditions | haiku | Mechanical schema parse. |
| Author the artefact body | sonnet | Bounded synthesis from typed inputs. |
| Review for compliance + cross-cutting impact | opus | Cross-input judgement when stakes are high. |
| Outcome-review synthesis at cadence | opus | Did the artefact change behaviour? |

## Templates

| File | Purpose |
|------|---------|
| `templates/skeleton.md.j2` | Markdown skeleton of the artefact with all required sections. |
| `templates/skeleton.md` | Markdown skeleton of the artefact with all required sections. Generated from `templates/skeleton.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/_smoke-test.json` | Minimum-viable filled JSON instance, parseable by the validator. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-dual-write-shadow-read-template.py` | Validate an artefact JSON against the output-contract schema + cross-field rules. | Pre-merge of the artefact PR + weekly staleness scan. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[code-review]] — gates the artefact before merge.
- [[incident-decision-template]] — sibling 2-minute decision record.
- [[regression-test-first-bugfix-workflow]] — sibling workflow that pins red-test-first discipline.

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` first checks whether preconditions hold (named trigger + named owner + typed inputs). If yes, it routes between the full artefact form and a minimal-record fallback when the trigger is below the materiality threshold. If preconditions don't hold, the conclusion is to skip this methodology and route the work upstream.
