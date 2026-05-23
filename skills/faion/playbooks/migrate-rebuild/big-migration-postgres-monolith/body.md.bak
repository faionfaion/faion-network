# Big migration: Postgres major or monolith-to-services

**Playbook slug:** `big-migration-postgres-monolith`
**Tier:** geek
**Complexity:** deep
**Persona:** P6 — Product-Dev Team

## Intent

Cross-quarter migration completes with zero data loss, proven rollback, bounded dual-stack window, and clean post-migration audit.

## Scope

A multi-quarter migration (Postgres major upgrade, monolith-to-services decomposition, or equivalent) goes from "we should probably do this" to "post-migration audit clean." The team builds a pre-migration baseline, proves dual-write / shadow-read, executes a cutover from a tagged runbook, and runs the post-migration audit. Risk register is alive throughout. All squads are informed at each gate.

### What this playbook covers

A six-stage chain front-loaded with strategy and backups, because migrations fail in those stages even when the engineering itself is competent. The chain enforces a *prove-reversibility-first* rule: no cutover step runs until the restore drill is green inside 30 days. The dual-stack stage is the longest by elapsed time — that is intentional, parity evidence is the most expensive thing to collect after the fact.

### Non-goals

- Greenfield architecture — assumes an existing production system
- Routine feature delivery — covered by `rfc-to-production-feature-delivery`
- Vendor selection / licence procurement — handled by separate procurement track

### Prerequisites

- Business case approved with explicit cost-of-doing-nothing
- Backup + restore tested in last 90 days
- Observability stack in place (metrics, logs, traces)
- On-call rotation able to absorb cutover window

## Success criteria

The playbook is done when:
- Strategy current/future/gap analysis docs published
- Pre-migration baseline captured (perf, correctness, cost)
- Dual-write + shadow-read evidence collected for ≥2 weeks
- Cutover runbook executed end-to-end with sign-offs
- Post-migration audit clean (functional + perf + cost)
- Lessons-learned doc + risk register closed

## Stages

### Stage 1: Strategy + scope

**Intent:** Current/future state + gap analysis turn intuition into a written change strategy.

**Methodologies in chain:**
- `strategy-analysis-current-state` → `pro/ba/business-analyst/strategy-analysis-current-state`
- `strategy-analysis-future-state` → `pro/ba/business-analyst/strategy-analysis-future-state`
- `strategy-analysis-gap-analysis` → `pro/ba/business-analyst/strategy-analysis-gap-analysis`
- `strategy-analysis-change-strategy` → `pro/ba/business-analyst/strategy-analysis-change-strategy`
- `wbs-creation` → `pro/pm/pm-traditional/wbs-creation`
- `risk-management` → `pro/pm/pm-traditional/risk-management`
- `risk-register` → `pro/pm/pm-traditional/risk-register`

**Decision gate:**
> Advance when change-strategy is signed off and risk register is reviewed across all impacted squads.

### Stage 2: Architecture + boundaries

**Intent:** Service boundaries, quality attributes, and reliability/observability baselines defined.

**Methodologies in chain:**
- `microservices-architecture` → `pro/dev/software-architect/microservices-architecture`
- `event-driven-architecture` → `pro/dev/software-architect/event-driven-architecture`
- `quality-attributes-analysis` → `pro/dev/software-architect/quality-attributes-analysis`
- `reliability-architecture` → `pro/dev/software-architect/reliability-architecture`
- `observability-architecture` → `pro/dev/software-architect/observability-architecture`
- `microservices-design` → `pro/dev/code-quality/microservices-design`
- `ddd-aggregates` → `pro/dev/software-developer/ddd-aggregates`
- `ddd-anti-corruption-layer` → `pro/dev/software-developer/ddd-anti-corruption-layer`
- `microservices-service-boundaries` → `pro/dev/software-developer/microservices-service-boundaries`
- `microservices-inter-service-comm` → `pro/dev/software-developer/microservices-inter-service-comm`
- `microservices-circuit-breaker` → `pro/dev/software-developer/microservices-circuit-breaker`
- `microservices-saga-pattern` → `pro/dev/software-developer/microservices-saga-pattern`

**Decision gate:**
> Advance when boundaries are testable in a spike and the rejected patterns are written down with rationale.

### Stage 3: Backups + reversibility

**Intent:** Proven backups + verified restore + rollback plan before any cutover.

**Methodologies in chain:**
- `backup-database-postgres` → `pro/infra/cicd-engineer/backup-database-postgres`
- `backup-database-mysql-mongo` → `pro/infra/cicd-engineer/backup-database-mysql-mongo`
- `backup-kubernetes-velero` → `pro/infra/cicd-engineer/backup-kubernetes-velero`
- `backup-verification-dr` → `pro/infra/cicd-engineer/backup-verification-dr`
- `backup-strategies` → `pro/infra/devops-engineer/backup-strategies`
- `argocd-gitops` → `pro/infra/cicd-engineer/argocd-gitops`
- `gitops-progressive-delivery` → `pro/infra/cicd-engineer/gitops-progressive-delivery`

**Decision gate:**
> Refuse to advance without a proven restore inside the last 30 days.

### Stage 4: Dual-stack + shadow-read

**Intent:** Run old and new side-by-side; capture parity evidence.

**Methodologies in chain:**
- `test-consumer-contract-from-spec` → `geek/sdlc-ai/test-consumer-contract-from-spec`
- `test-golden-master-legacy-rewrite` → `geek/sdlc-ai/test-golden-master-legacy-rewrite`
- `test-property-based-llm-invariants` → `geek/sdlc-ai/test-property-based-llm-invariants`
- `dora-metrics` → `pro/infra/cicd-engineer/dora-metrics`

**Decision gate:**
> Advance when parity is within target band on production traffic shape and open deltas have owners.

### Stage 5: Cutover

**Intent:** Tagged runbook executes end-to-end; comms loop closes.

**Methodologies in chain:**
- `inc-runbook-as-markdown-tagged-steps` → `geek/sdlc-ai/inc-runbook-as-markdown-tagged-steps`
- `communications-management` → `pro/pm/pm-traditional/communications-management`
- `change-control` → `pro/pm/pm-traditional/change-control`

**Decision gate:**
> Required: every tagged step has a 'done' marker. Skipped steps = block-and-investigate.

### Stage 6: Post-audit + lessons

**Intent:** Audit verifies the new state; lessons close the loop.

**Methodologies in chain:**
- `lessons-learned` → `pro/pm/pm-traditional/lessons-learned`
- `project-closure` → `pro/pm/pm-traditional/project-closure`

**Decision gate:**
> Required outputs: audit + lessons-learned. Migrations without retros teach nothing to the next one.

## Common pitfalls

- Skipping the restore drill — backups that don't restore aren't backups
- Dual-stack with no parity report — flying blind
- Cutover runbook in a wiki nobody reads — fails the bus-factor test
- Comms only after the fact — surprises customers and on-call

## Quality checklist (self-review)

- Can I restore last night's backup into a new cluster from cold steel?
- Did parity hold across all critical paths under real traffic shape?
- Do I have a written rollback that someone other than the migration lead can execute?

## Related playbooks

- `rfc-to-production-feature-delivery`
- `incident-postmortem-preventive-backlog`
- `soc2-gdpr-audit-prep`

## Known gaps

The following methodologies are referenced or implied by this playbook but do not yet exist in the knowledge base. They are tracked in the manifest `gaps[]` array and block publication until resolved (BLOCK policy).
- **strangler-pattern-checklist-product-dev-team** (tier `geek`, blocks stage 2) — Architecture stage references strangler-fig moves but lacks a written checklist
- **dual-write-shadow-read-template** (tier `geek`, blocks stage 4) — Dual-stack stage needs a concrete dual-write + shadow-read template

## CLI usage

```
faion get-content big-migration-postgres-monolith --format md       # human-readable rendering
faion get-content big-migration-postgres-monolith --format context  # agent-optimised context bundle
faion get-content big-migration-postgres-monolith --format json     # raw structured form
```
