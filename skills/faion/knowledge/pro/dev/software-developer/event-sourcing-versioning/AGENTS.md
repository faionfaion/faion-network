---
slug: event-sourcing-versioning
tier: pro
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Once an event class is published (consumed by any downstream system), its field contract is immutable.
content_id: "93b319a707c74c86"
tags: [event-sourcing, event-versioning, upcaster, gdpr, event-catalog]
---
# Event Sourcing — Event Versioning and GDPR

## Summary

**One-sentence:** Once an event class is published (consumed by any downstream system), its field contract is immutable.

**One-paragraph:** Once an event class is published (consumed by any downstream system), its field contract is immutable. Breaking changes require an upcaster and a version bump committed to the event catalog. PII in events must be crypto-shredded or moved to a mutable side table to satisfy GDPR right-to-erasure.

## Applies If (ALL must hold)

- Any event class that has been consumed by more than one system (projection, saga, external subscriber) — version it from day one.
- Systems processing personal data (names, addresses, payment tokens, health records) — apply PII strategy before publishing the first event.
- Teams adopting a schema registry (Apicurio, Confluent) — event catalog is the local complement.
- When adding a new field to a published event class (always backward-compatible with default value) or removing/renaming one (requires upcaster).

## Skip If (ANY kills it)

- Internal events consumed only by the same aggregate's own projection and never published externally — version overhead may not be warranted, but keep PII strategy regardless.
- Pre-PMF systems with zero external consumers — establish the pattern early but do not over-engineer the catalog tooling.

## Prerequisites

- TBD — list concrete input artifacts and where they come from

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `TBD/path` | TBD — what upstream output this consumes |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules migrated from v1 methodology | ~800 |
| `content/02-output-contract.xml` | essential | Output schema (stub — fill from v1 patterns) | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns migrated from v1 methodology | ~800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| TBD | sonnet | TBD |

## Templates

| File | Purpose |
|------|---------|
| TBD | TBD |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| TBD | TBD | TBD |

## Related

- parent skill: `pro/dev/software-developer/`
