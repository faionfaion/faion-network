---
slug: api-versioning
tier: solo
group: dev
domain: api-developer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Version REST APIs only for breaking semantic changes; additive changes (new field, new optional input, new endpoint) never require a new version.
content_id: "e31f4452a1dc2292"
tags: [api-versioning, rest-api, breaking-changes, deprecation, backwards-compatibility]
---
# API Versioning

## Summary

**One-sentence:** Version REST APIs only for breaking semantic changes; additive changes (new field, new optional input, new endpoint) never require a new version.

**One-paragraph:** Version REST APIs only for breaking semantic changes; additive changes (new field, new optional input, new endpoint) never require a new version. Use URL path versioning (`/api/v1/`) — cacheable, debuggable, unambiguous. Support N and N-1 simultaneously; emit `Deprecation`, `Sunset`, and `Link: rel=successor-version` headers from deprecated routes; measure per-version traffic before sunsetting.

## Applies If (ALL must hold)

- Public APIs with external consumers you cannot redeploy in lockstep (partners, mobile apps shipped to stores, third-party integrations).
- Major contract changes: renamed/removed fields, changed types, new required inputs.
- Two-team handoffs where producer ships ahead of consumers and needs a bridge.
- Long-tail clients (mobile apps from 2 years ago still hitting prod).
- Migrations: feature-flag-style rollout of v2 alongside v1.

## Skip If (ANY kills it)

- Internal-only API with one consumer redeployed atomically — backward-compat fields beat versions.
- Additive changes (new field, new endpoint, new optional input) — never a new version.
- GraphQL APIs — use `@deprecated` + field evolution + persisted queries instead.
- Tiny app you control end-to-end — versioning ceremony eats cycles you don't have.
- After-the-fact for breaking changes already merged — that is a hotfix, not a `/v2`.

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

- parent skill: `solo/dev/api-developer/`
