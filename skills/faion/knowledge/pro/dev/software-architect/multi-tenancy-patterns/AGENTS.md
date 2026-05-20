---
slug: multi-tenancy-patterns
tier: pro
group: dev
domain: software-architect
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Decision framework for SaaS multi-tenancy isolation — shared-everything vs schema-per-tenant vs DB-per-tenant — with tenant-isolation guarantees, blast-radius math, and migration paths between models.
content_id: "b780fe340e21cee8"
tags: [dev, architecture, multi-tenancy, saas, isolation, schema-per-tenant, db-per-tenant, security]
---

# Multi-Tenancy Patterns

## Summary

**One-sentence:** A decision framework for choosing between SaaS multi-tenancy models (shared-everything / schema-per-tenant / DB-per-tenant / hybrid) based on isolation requirements, blast-radius tolerance, cost economics, and migration paths between models.

**One-paragraph:** Multi-tenant SaaS architects make a high-stakes early decision about tenant isolation. Picking wrong creates either security incidents (over-shared) or operational nightmares (over-isolated). Faion's current content has security-architecture for the isolation question and cost-latency budgeting for the economic question, but no single methodology that connects them with concrete decision criteria + migration paths. Mechanism: a decision matrix mapping (tenant count + isolation requirement + compliance scope + per-tenant noise tolerance + cost ceiling) to one of four canonical models, with quantified blast-radius math and a documented migration path BETWEEN models when assumptions change. Primary output: an ADR-style decision record + the implementation patterns required for the chosen model.

## Applies If (ALL must hold)

- product is multi-tenant SaaS (or moving toward it)
- expected tenant count > 5 AND < 100,000 (above 100k, sharding patterns differ)
- at least one of: compliance constraints, large customer cohort with high security expectations, noisy-neighbor concern
- design decision can still influence the database schema (pre-launch OR pre-major-rewrite)

## Skip If (ANY kills it)

- single-tenant product (one customer = one deployment) — different methodology
- B2C product with one user per account and no cross-tenant primitives — schema decisions are simpler
- already deeply committed to a model with no migration appetite — use the current model's optimization methodology instead
- tenant count expected &lt; 5 lifetime — simpler approach (separate deployments) is fine

## Prerequisites

- expected tenant count + growth curve (5 / 50 / 500 / 5000 / 50000?)
- compliance scope: SOC 2, GDPR, HIPAA, ISO 27001, FedRAMP — each has tenant-isolation implications
- noisy-neighbor tolerance per tenant size class (free / SMB / enterprise) — what perf interference is acceptable
- cost ceiling per tenant (especially for low-ARPU tenants)
- DBA / SRE bandwidth available for the chosen model's operational burden

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/dev/software-architect/security-architecture-foundations` | Tenant-isolation guarantees consume threat-model patterns from this methodology |
| `pro/dev/software-architect/cost-latency-budget` | Per-tenant cost budget feeds the model-choice decision |
| `pro/infra/devops-engineer/sli-slo-definition` | Per-tenant SLOs differ per model (DB-per-tenant typically tightest) |
| `pro/dev/backend-systems/postgres-row-level-security` | Implementation detail for shared-everything model; consume RLS patterns |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: decision-matrix-driven choice, isolation-guarantee-documented, blast-radius-quantified, migration-path-documented, per-tenant-data-residency-explicit | ~1100 |
| `content/02-output-contract.xml` | essential | Multi-tenancy ADR schema + isolation-guarantee contract + forbidden patterns | ~700 |
| `content/03-failure-modes.xml` | essential | 7 failure modes (RLS-bypass, noisy-neighbor cascade, cross-tenant data leak, etc.) with detector + repair | ~1200 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `requirements_collation` | sonnet | Gather compliance + tenant count + isolation needs + cost from stakeholders |
| `model_score_per_option` | opus | Score each model (shared / schema / DB / hybrid) against requirements — synthesis |
| `blast_radius_calc` | sonnet | Quantify failure-mode cost per model for typical incident classes |
| `migration_path_design` | opus | Document the path from current model to target, including data-migration phases |

## Templates

| File | Purpose |
|------|---------|
| `templates/multi-tenancy-adr.md` | ADR template for the multi-tenancy decision |
| `templates/decision-matrix.csv` | Stakeholder-input matrix mapping requirements -&gt; model fit |
| `templates/isolation-guarantee.md` | What the chosen model guarantees + what it does NOT |
| `templates/migration-runbook.md` | Migration runbook template for moving between models |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/score-models.py` | Computes per-model fit score from a requirements input | During the decision process |
| `scripts/audit-tenant-isolation.py` | Validates the runtime that the documented isolation guarantee holds (e.g., tests RLS, schema boundaries) | Quarterly + after any auth/data-access change |

## Related

- parent skill: `pro/dev/software-architect/`
- peer methodologies: `security-architecture-foundations`, `cost-latency-budget`, `postgres-row-level-security`
- external: [AWS SaaS Lens Multi-Tenancy](https://docs.aws.amazon.com/wellarchitected/latest/saas-lens/) · [Microsoft SaaS Patterns](https://learn.microsoft.com/en-us/azure/architecture/guide/multitenant/) · [Postgres RLS Docs](https://www.postgresql.org/docs/current/ddl-rowsecurity.html)
