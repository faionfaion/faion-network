---
slug: strangler-fig-playbook-vendor
tier: pro
group: dev
domain: software-architect
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "8f3523957ef658db"
summary: End-to-end strangler-fig migration playbook framed for vendor delivery — slice picking, traffic shifting, fallback semantics, exit criteria.
tags: [strangler-fig, migration, legacy, architecture, vendor-delivery, monolith-to-services]
---
# Strangler-Fig Migration Playbook (Vendor Delivery)

## Summary

**One-sentence:** End-to-end strangler-fig migration playbook framed for vendor delivery — slice picking, traffic shifting, fallback semantics, exit criteria.

**One-paragraph:** Existing DDD anti-corruption-layer + microservices content cover the parts; this is the full program guide for an outsource vendor running a 3-6 month legacy-to-modern migration. Mechanism: starts with an inventory of monolith routes/jobs/queues, scores each slice on (a) coupling depth, (b) traffic risk, (c) business priority, picks the first 3 slices, deploys a Mark Fowler-style routing facade in front of the monolith, dual-writes during cutover, monitors error parity for ≥7 days per slice, retires the legacy code path with a documented kill-switch. Built for vendor-client engagements: weekly slice-status reports, contractual exit criteria, fallback-to-legacy SLA. Primary output: strangled production system + a written runbook for in-house team takeover.

## Applies If (ALL must hold)

- legacy monolith in production with documented routes/jobs (you can list them)
- vendor (you) is delivering migration for a client who retains the legacy team
- engagement scoped 3-6 months — long enough for slice cycles, short enough to stay focused
- monolith and target architecture share a deployable environment (can both run in prod)
- there is a measurable business reason for migration (cost, throughput, dev velocity) — not "modernization for its own sake"

## Skip If (ANY kills it)

- greenfield project — no monolith to strangle
- monolith is small enough (&lt; 30 routes / &lt; 50 KLOC) for big-bang rewrite to be safer — use rewrite playbook
- legacy team is fully replaced by the vendor — use full-takeover migration instead
- regulatory mandate requires synchronous cutover (banking core, regulated medical) — strangler-fig adds risk
- no observability stack — strangler-fig is blind without metrics; install observability first

## Prerequisites (must be true before starting)

- inventory of monolith routes/jobs/queues (CSV: name, traffic, dependencies)
- traffic data: requests/sec per route, error rate, p50/p99 latency baselines
- target architecture decision (services + boundaries) approved by client architect
- routing facade technology chosen (nginx + Lua, Envoy, application-layer router, API gateway)
- observability: metrics + structured logs + tracing across both monolith and new services
- a kill-switch design for each slice (config flag, percentage rollout)

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/dev/software-architect/microservices-architecture` | Provides target service boundaries the migration moves into |
| `pro/dev/software-developer/ddd-anti-corruption-layer` | The ACL pattern used at the boundary between monolith and new services |
| `pro/dev/software-architect/observability-architecture` | Required to detect parity violations during cutover |
| `pro/dev/software-architect/architecture-decision-records` | Each slice's cutover decision is recorded as an ADR |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: slice scoring, parity-burn-in, kill-switch per slice, dual-write windowed, exit-criteria contractual | ~950 |
| `content/02-output-contract.xml` | essential | Slice plan schema, cutover record schema, runbook schema, forbidden patterns | ~750 |
| `content/03-failure-modes.xml` | essential | 7 failure modes (big-slice trap, shared-state bleed, monitoring drift, vendor stub-out, partial rollback, dual-write divergence, runbook abandonment) | ~1000 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `slice_score_per_route` | sonnet | Bounded scoring on coupling/traffic/priority axes |
| `cutover_runbook_draft` | sonnet | Step-by-step template with named commands |
| `slice_selection_synthesis` | opus | Cross-route synthesis: which 3 slices minimize coupling damage |
| `parity_burn_in_alert_rule_gen` | sonnet | Generate Prometheus / Datadog rules from error-rate baselines |

## Templates

| File | Purpose |
|------|---------|
| `templates/slice-plan.md` | Per-slice spec: scope, target service, traffic shape, fallback |
| `templates/cutover-runbook.md` | Step-by-step cutover with rollback at each step |
| `templates/weekly-status-report.md` | Client-facing report: slices live, in-progress, blocked |
| `templates/exit-criteria-contract.md` | Contractual definition of "migration complete" per slice |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/score-slices.py` | Score and rank monolith routes by migration value | Before slice picking |
| `scripts/diff-monolith-vs-service.py` | Compare responses between legacy and new for shadow traffic | During parity burn-in |
| `scripts/kill-switch-validate.py` | Test kill-switch revert path before cutover | T-1 day before slice cutover |

## Related

- parent skill: `pro/dev/software-architect/`
- peer methodologies: `microservices-architecture`, `monolith-architecture`, `architecture-decision-records`
- external: [Martin Fowler - StranglerFigApplication](https://martinfowler.com/bliki/StranglerFigApplication.html) · [Sam Newman - Monolith to Microservices (2019)](https://samnewman.io/books/monolith-to-microservices/) · [GitHub - migrating-monoliths](https://github.blog/2020-12-15-scaling-the-github-api-with-a-sharded-replicated-rate-limiter-in-redis/)
