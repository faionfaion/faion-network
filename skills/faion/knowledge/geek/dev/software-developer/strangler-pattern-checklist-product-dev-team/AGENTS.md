---
slug: strangler-pattern-checklist-product-dev-team
tier: geek
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-network]
content_id: "616b81de4012a27d"
summary: Team-execution checklist for big migrations (Postgres major, monolith-to-services, region migration) — legacy contract freeze, ACL rollout, traffic-shift gates, sunset criteria — distinct from the pattern essay.
tags: [strangler, migration, product-dev-team, postgres-major, monolith-to-services, geek, dev]
---
# Strangler Pattern Checklist — Product Dev Team

## Summary

**One-sentence:** A team-execution checklist for big strangler-pattern migrations (Postgres major upgrade, monolith-to-services split, region/cloud migration), covering legacy contract freeze, anti-corruption-layer (ACL) rollout, traffic-shift gates, and explicit sunset criteria.

**One-paragraph:** Microservices design and the strangler pattern are described conceptually in `pro/dev/software-developer/strangler-fig-migration-pattern`. This methodology operates one level down: the actual ordered checklist a 4-12-engineer product team works against during a multi-month migration. It enumerates the gates — legacy frozen, ACL deployed, shadow read in green for 7 days, traffic shift to 1% then 10% then 50%, observed error budget intact, then sunset — and makes each one a binary owner-and-date row. Drives the migration from PM-by-Gantt to PM-by-checkbox, with engineering owning the gates rather than negotiating per-week deadline slips.

## Applies If (ALL must hold)

- Product team of 4-12 engineers running a migration projected to last ≥6 weeks.
- Migration crosses a data store boundary (DB major upgrade, schema move, store change) OR a service boundary (extraction, region split).
- The team owns both the legacy and the new stack (no third-party legacy that prevents an ACL).
- Production observability is mature enough to compare legacy vs new on latency, error rate, and business metrics.

## Skip If (ANY kills it)

- Migration is single-developer scope → use the pattern essay alone; the checklist is overkill.
- No write traffic to migrate (read-only data set) → shadow-read alone suffices, traffic-shift gates collapse to a redirect.
- Migration is forced by a vendor end-of-life within 4 weeks → emergency upgrade playbook applies, not this checklist.
- Team has no production observability — stand up the observability layer FIRST (separate effort), then run this checklist.

## Prerequisites

- An ACL spec: input/output contract between legacy and new for every operation in scope.
- An observability dashboard comparing legacy and new on latency p50/p95/p99, error rate, business success rate (e.g. signup conversion).
- A traffic-shift mechanism: weighted DNS, load balancer routing, feature flag, or middleware-level switch.
- A migration RUN-BOOK with named on-call for the migration window.

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/dev/software-developer/strangler-fig-migration-pattern` | The pattern essay; this is the team-execution complement. |
| `geek/dev/software-developer/dual-write-shadow-read-template` | The exact shape of the shadow-read gate. |
| `geek/dev/software-developer/multi-region-failover-pattern-pack` | Useful when migration crosses regions. |
| `geek/dev/software-developer/incident-decision-template` | Drives rollback decisions when a gate trips. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: legacy contract frozen, ACL covers 100% of traffic, shadow read green ≥7 days, traffic shift in stages with auto-rollback, sunset criteria written before cutover | ~1300 |

## Related

- parent skill: `geek/dev/software-developer/`
- peer methodologies: `dual-write-shadow-read-template`, `multi-region-failover-pattern-pack`, `incident-decision-template`, `fitness-function-suite-bootstrap`
- external: [Fowler — StranglerFigApplication](https://martinfowler.com/bliki/StranglerFigApplication.html) · [Stripe Database Migration retrospective](https://stripe.com/blog) · [Shopify monolith decomposition blog](https://shopify.engineering/)
