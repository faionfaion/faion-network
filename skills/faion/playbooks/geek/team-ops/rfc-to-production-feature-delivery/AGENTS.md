---
slug: rfc-to-production-feature-delivery
tier: geek
group: team-ops
persona: P6
goal: build-ship
complexity: deep
version: 0.1.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion
summary: Approved RFC → live production behind a feature flag with telemetry, runbook, and post-launch review scheduled.
content_id: dbb110685666c855
methodology_refs:
  - elicitation-techniques
  - requirements-prioritization
  - requirements-validation
  - acceptance-criteria
  - user-story-mapping
  - use-case-modeling
  - minimum-product-frameworks
  - mlp-planning
  - ai-assisted-specification-writing
  - ai-assisted-specification-writing-alt
  - task-spec-kit-three-step
  - task-agent-drafts-spec-before-coding
  - quality-attributes-analysis
  - event-driven-architecture
  - microservices-architecture
  - clean-architecture
  - domain-driven-design
  - claude-md-creation
  - llm-friendly-architecture
  - kb-agents-md-context-pyramid
  - task-plan-mode-locked-execution
  - task-worktree-runtime-isolation
  - test-tdd-red-green-split-agents
  - lint-precommit-floor
  - lint-ruff-and-biome-as-default
  - gov-conventional-commits-enforced
  - test-consumer-contract-from-spec
  - test-mutation-feedback-loop
  - test-property-based-llm-invariants
  - test-self-healing-locators-audited
  - mr-error-tracker-draft-pr
  - mr-graph-vs-diff-reviewer
  - mr-slash-command-surface
  - gov-sonarqube-ai-code-gate
  - gov-approval-token-signed-jwt
  - requirements-traceability
  - argocd-gitops
  - gitops-progressive-delivery
  - grafana-basics
  - prometheus-monitoring
  - inc-runbook-as-markdown-tagged-steps
  - experimentation-at-scale
  - feedback-management
  - product-analytics
  - continuous-discovery-habits
  - opportunity-solution-trees
---

# RFC → Production: feature delivery

**Playbook slug:** `rfc-to-production-feature-delivery`
**Tier:** geek
**Complexity:** deep
**Persona:** P6 — Product-Dev Team

## Intent

Approved RFC → live production behind a feature flag with telemetry, runbook, and post-launch review scheduled.

## Scope

One product bet travels from an approved RFC to live production. All handoffs (PM brief → BA reqs → Architect design → Dev implementation → QA verification → DevOps deploy → PdM rollout) are auditable. Shipping closes the loop with a feature flag, telemetry, an on-call runbook, and a post-launch review scheduled. The single living artifact under `.aidocs/in-progress/<feature>/` is the unit of work; tracker is the mirror, not the source.

### What this playbook covers

Six explicit stages, each owned by a different role but carrying forward the same artifact. The chain is intentionally heavy: a product-dev team that ships an RFC without explicit gates ends up with under-tested coupling, dark-launch surprises, and on-calls who have never read the runbook. Each gate is auditable — if you can't point at the artifact, the gate did not pass.

### Non-goals

- RFC drafting / approval process — assumed already done upstream
- Quarter-level prioritisation — handled in `quarter-planning-okr-reset`
- Major migrations — see `big-migration-postgres-monolith`

### Prerequisites

- Approved RFC referencing OKR + bet
- Feature flag platform in place
- CI/CD pipeline with progressive delivery + supply-chain scans
- Repo wired with CLAUDE.md + AGENTS.md context pyramid

## Success criteria

The playbook is done when:
- `spec.md + design.md + implementation-plan.md` exist and are coherent
- Acceptance criteria mapped 1:1 to tests (contract + property + mutation)
- Feature behind a flag with dark/ramp/GA states defined
- Telemetry: Grafana dashboards + Prometheus alerts + Sentry/Datadog wiring
- On-call runbook published with tagged steps
- Post-launch review scheduled within 14 days

## Stages

### Stage 1: RFC → spec

**Intent:** PM brief + BA elicitation produce a spec with acceptance criteria.

**Tasks:**
- Elicit requirements with stakeholders
- Prioritise + validate against OKRs
- Draft spec.md (AI-assisted) under `.aidocs/in-progress/<feature>/`
- Define acceptance criteria + Definition of Ready

**Methodologies in chain:**
- `elicitation-techniques` → `pro/ba/business-analyst/elicitation-techniques`
- `requirements-prioritization` → `pro/ba/business-analyst/requirements-prioritization`
- `requirements-validation` → `pro/ba/business-analyst/requirements-validation`
- `acceptance-criteria` → `pro/ba/business-analyst/acceptance-criteria`
- `user-story-mapping` → `pro/ba/business-analyst/user-story-mapping`
- `use-case-modeling` → `pro/ba/business-analyst/use-case-modeling`
- `minimum-product-frameworks` → `pro/product/product-manager/minimum-product-frameworks`
- `ai-assisted-specification-writing` → `geek/sdd/sdd-planning/ai-assisted-specification-writing`
- `task-spec-kit-three-step` → `geek/sdlc-ai/task-spec-kit-three-step`
- `task-agent-drafts-spec-before-coding` → `geek/sdlc-ai/task-agent-drafts-spec-before-coding`

**Decision gate:**
> Advance when spec passes Definition of Ready: AC are testable, scope cuts are explicit, dependencies named.

### Stage 2: Architect → design

**Intent:** Architect commits a design.md with quality attributes, boundaries, and reuse decisions.

**Tasks:**
- Run quality-attributes analysis (perf, sec, reliability, observability)
- Decide on microservices/event-driven boundaries where applicable
- Apply clean architecture + DDD principles
- Author CLAUDE.md updates so agents stay LLM-friendly

**Methodologies in chain:**
- `quality-attributes-analysis` → `pro/dev/software-architect/quality-attributes-analysis`
- `event-driven-architecture` → `pro/dev/software-architect/event-driven-architecture`
- `microservices-architecture` → `pro/dev/software-architect/microservices-architecture`
- `clean-architecture` → `pro/dev/code-quality/clean-architecture`
- `domain-driven-design` → `pro/dev/code-quality/domain-driven-design`
- `claude-md-creation` → `geek/dev/code-quality/claude-md-creation`
- `llm-friendly-architecture` → `geek/dev/code-quality/llm-friendly-architecture`
- `kb-agents-md-context-pyramid` → `geek/sdlc-ai/kb-agents-md-context-pyramid`

**Decision gate:**
> Advance when design.md is reviewed in the weekly architectural review and CLAUDE.md/AGENTS.md updates land.

### Stage 3: Dev → implementation

**Intent:** Plan-mode locked, worktree-isolated, red-green-split, contract-tested implementation.

**Tasks:**
- Author implementation-plan.md from spec + design
- Spin worktree per task (runtime isolation)
- Operate in plan-mode then locked execution
- Run TDD red-green-split between agents
- Pre-commit floor + ruff/biome lint gates

**Methodologies in chain:**
- `task-plan-mode-locked-execution` → `geek/sdlc-ai/task-plan-mode-locked-execution`
- `task-worktree-runtime-isolation` → `geek/sdlc-ai/task-worktree-runtime-isolation`
- `test-tdd-red-green-split-agents` → `geek/sdlc-ai/test-tdd-red-green-split-agents`
- `lint-precommit-floor` → `geek/sdlc-ai/lint-precommit-floor`
- `lint-ruff-and-biome-as-default` → `geek/sdlc-ai/lint-ruff-and-biome-as-default`
- `gov-conventional-commits-enforced` → `geek/sdlc-ai/gov-conventional-commits-enforced`

**Decision gate:**
> Advance when implementation matches spec, all gates green, conventional commits enforced.

### Stage 4: QA → verification

**Intent:** Property-based + mutation + contract tests prove the AC. Self-healing locators audited.

**Tasks:**
- Generate contract tests from spec
- Run mutation feedback loop
- Add property-based invariants for LLM-touched paths
- Wire self-healing locators with audit log
- Slash-command surface for reviewers

**Methodologies in chain:**
- `test-consumer-contract-from-spec` → `geek/sdlc-ai/test-consumer-contract-from-spec`
- `test-mutation-feedback-loop` → `geek/sdlc-ai/test-mutation-feedback-loop`
- `test-property-based-llm-invariants` → `geek/sdlc-ai/test-property-based-llm-invariants`
- `test-self-healing-locators-audited` → `geek/sdlc-ai/test-self-healing-locators-audited`
- `mr-graph-vs-diff-reviewer` → `geek/sdlc-ai/mr-graph-vs-diff-reviewer`
- `mr-slash-command-surface` → `geek/sdlc-ai/mr-slash-command-surface`
- `gov-sonarqube-ai-code-gate` → `geek/sdlc-ai/gov-sonarqube-ai-code-gate`
- `gov-approval-token-signed-jwt` → `geek/sdlc-ai/gov-approval-token-signed-jwt`
- `requirements-traceability` → `pro/ba/business-analyst/requirements-traceability`

**Decision gate:**
> Advance when every AC traces to at least one passing test and code gates are green.

### Stage 5: DevOps → deploy

**Intent:** GitOps deploy with progressive rollout behind a flag; telemetry + runbook live.

**Tasks:**
- Wire ArgoCD GitOps pipeline
- Configure progressive delivery
- Add Prometheus alerts + Grafana dashboards
- Publish on-call runbook as markdown tagged steps

**Methodologies in chain:**
- `argocd-gitops` → `pro/infra/cicd-engineer/argocd-gitops`
- `gitops-progressive-delivery` → `pro/infra/cicd-engineer/gitops-progressive-delivery`
- `grafana-basics` → `pro/infra/cicd-engineer/grafana-basics`
- `prometheus-monitoring` → `pro/infra/cicd-engineer/prometheus-monitoring`
- `inc-runbook-as-markdown-tagged-steps` → `geek/sdlc-ai/inc-runbook-as-markdown-tagged-steps`

**Decision gate:**
> Advance when flag is live, dashboards show green telemetry, runbook is committed and discoverable.

### Stage 6: PdM → rollout

**Intent:** Ramp the flag, measure adoption, schedule post-launch review.

**Tasks:**
- Define ramp criteria + experimentation plan
- Wire product analytics on the new path
- Drive feedback loop via PdM's feedback-management methodology
- Schedule post-launch review within 14 days

**Methodologies in chain:**
- `experimentation-at-scale` → `pro/product/product-manager/experimentation-at-scale`
- `feedback-management` → `pro/product/product-manager/feedback-management`
- `product-analytics` → `pro/product/product-manager/product-analytics`
- `continuous-discovery-habits` → `pro/product/product-manager/continuous-discovery-habits`

**Decision gate:**
> Advance once GA criteria are met OR a kill decision is documented. No flag stays dark forever.

## Common pitfalls

- Skipping design.md because spec "feels small" — coupling accidents bite later
- Tests added after merge — defeats traceability
- Deploy without a flag — no rollback path, no ramp
- Telemetry wired after launch — first incident has no dashboards
- Runbook lives in someone's head — fails the bus-factor test

## Quality checklist (self-review)

- Can a new on-call open the runbook and follow it cold?
- Does every AC have a test?
- Is the flag killable in <5 min if telemetry goes red?
- Is the post-launch review on someone's calendar?

## Related playbooks

- `quarter-planning-okr-reset`
- `feature-flag-rollout-decision`
- `sentry-datadog-alert-triage`
- `cross-role-handoff-pm-architect-dev-qa-devops`

## Known gaps

The following methodologies are referenced or implied by this playbook but do not yet exist in the knowledge base. They are tracked in the manifest `gaps[]` array and block publication until resolved (BLOCK policy).
- **rfc-template-product-dev-team** (tier `geek`, blocks stage 1) — RFC → spec stage needs a concrete RFC template tuned for product-dev teams
- **feature-flag-rollout-runbook** (tier `geek`, blocks stage 6) — Rollout stage needs a step-by-step runbook for flag ramp / hold / kill decisions

## CLI usage

```
faion get-content rfc-to-production-feature-delivery --format md       # human-readable rendering
faion get-content rfc-to-production-feature-delivery --format context  # agent-optimised context bundle
faion get-content rfc-to-production-feature-delivery --format json     # raw structured form
```
