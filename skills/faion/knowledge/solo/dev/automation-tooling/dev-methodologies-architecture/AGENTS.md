---
slug: dev-methodologies-architecture
tier: solo
group: dev
domain: sdd
version: 1.0.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Applies backend architecture patterns incrementally: DB schema design, ORM query optimisation, caching, background jobs, API envelopes, auth, structured logging.
content_id: "a243f4eef28f1591"
complexity: medium
produces: rubric
est_tokens: 4300
tags: [architecture, orm-optimisation, caching, background-jobs, structured-logging]
---
# Dev Methodologies — Architecture

## Summary

**One-sentence:** Applies backend architecture patterns incrementally: DB schema design, ORM query optimisation, caching, background jobs, API envelopes, auth, structured logging.

**One-paragraph:** Applies backend architecture patterns incrementally: DB schema design, ORM query optimisation, caching, background jobs, API envelopes, auth, structured logging. Decision tree, output contract, failure modes, and a procedure (when complexity ≥ medium) live under `content/`. Templates in `templates/` start with a 5-line `__faion_header__` block; the validator script in `scripts/` is stdlib-only with `--help` and `--self-test`.

**Ефективно для:**

- Greenfield or expanding backend service that needs an architectural baseline.
- Refactoring an existing service that lacks consistent envelope/auth/logging patterns.
- Owner can commit + test after each pattern; incremental adoption is feasible.
- Output produces `rubric` matching the schema in `content/02-output-contract.xml`.

## Applies If (ALL must hold)

- Greenfield or expanding backend service that needs an architectural baseline.
- Refactoring an existing service that lacks consistent envelope/auth/logging patterns.
- Owner can commit + test after each pattern; incremental adoption is feasible.

## Skip If (ANY kills it)

- Pure frontend or batch-only service — backend patterns do not apply.
- Existing architecture is fine; this would only churn working code.
- No tests in place — patterns must ride on a test safety net.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| ORM and migration tool | Django / SQLAlchemy / Prisma | team |
| Cache infra | Redis or Memcached | infra |
| Background job runner | Celery / RQ / SQS / similar | infra |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[practices-backend-languages]] | language-specific patterns sit beneath the architecture |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 testable rules (incl. skip-this-methodology) with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid example + invalid example + forbidden traits | 900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns with symptom + root-cause + fix | 800 |
| `content/04-procedure.xml` | essential | 5-step end-to-end procedure with input/action/output per step | 900 |
| `content/06-decision-tree.xml` | essential | Root question + observable branches → conclusion(ref=rule-id); skip leaf always reachable | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `audit-existing` | sonnet | Rubric scoring against patterns. |
| `apply-pattern` | sonnet | Implement one pattern per PR. |
| `test-after-each` | haiku | Smoke tests on each PR. |

## Templates

| File | Purpose |
|------|---------|
| `templates/api_envelope.py` | Standard API response envelope: data + meta + errors |
| `templates/structured_logger.py` | Structured JSON logger with request_id correlation |
| `templates/_smoke-test.py` | Minimum viable filled-in artefact for sanity-checking the schema. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-dev-methodologies-architecture.py` | Validate the produced artefact against the schema in `content/02-output-contract.xml`. | Pre-commit; CI on each artefact change; `--self-test` in dev. |

## Related

- [[logging-patterns]]
- [[feature-flags-core-implementation]]
- [[best-practices-2026]]

## Decision tree

See `content/06-decision-tree.xml`. Root question: *Is the service backend AND has tests AND can iterate per pattern?* The tree's purpose is to route an input through observable signals to a conclusion that references a rule from `content/01-core-rules.xml`; the skip-this-methodology branch is always reachable so an inappropriate caller exits cleanly.
