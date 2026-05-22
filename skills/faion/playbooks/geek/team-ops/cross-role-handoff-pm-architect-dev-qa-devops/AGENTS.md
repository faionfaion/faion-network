---
slug: cross-role-handoff-pm-architect-dev-qa-devops
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
summary: Five fragmented handoffs → one living artifact carries a feature through PM / Architect / Dev / QA / DevOps with DoR/DoD gates.
content_id: 96caf5d8f3054caf
methodology_refs:
  - writing-design-documents
  - backlog-grooming-roadmapping
  - architecture-decision-records
  - task-spec-kit-three-step
  - test-tdd-red-green-split-agents
  - code-review
  - inc-runbook-as-markdown-tagged-steps
---

# Cross-role handoff: PM → Architect → Dev → QA → DevOps in one loop

**Playbook slug:** `cross-role-handoff-pm-architect-dev-qa-devops`
**Tier:** geek
**Complexity:** deep
**Persona:** P6 — Product-Dev Team

## Intent

Five fragmented handoffs → one living artifact carries a feature through PM / Architect / Dev / QA / DevOps with DoR/DoD gates.

## Scope

A feature moves through 5 roles with a single living artifact (spec + design + test-plan + runbook). Each role inherits prior context and emits a delta. Handoffs are blocked if Definition-of-Ready is not met; sign-offs are required at Definition-of-Done. QA acceptance and on-call handoff are explicit ceremonies, not implicit assumptions.

### What this playbook covers

Five stages, each named for the handoff it enforces. The chain enforces *single artifact, multiple deltas*: there is one feature folder, every role appends, none forks. DoR is the entry gate; DoD signoff is the exit gate. Without these, the "single artifact" rule degrades back into 5 disconnected docs.

### Non-goals

- RFC drafting — see `rfc-to-production-feature-delivery` (broader playbook)
- Release-train coordination across multiple teams — separate playbook
- Customer-facing comms — see `incident-postmortem-preventive-backlog`

### Prerequisites

- Single feature directory under `.aidocs/in-progress/<feature>/`
- Roles named for the feature: PM, Architect, Dev lead, QA lead, DevOps
- `test-tdd-red-green-split-agents` available

## Success criteria

The playbook is done when:
- Single living artifact with deltas per role
- DoR met before each handoff
- DoD signed off at each ceremony
- QA acceptance signoff recorded
- On-call handoff completed with runbook walk
- Release-train coordination documented if cross-team

## Stages

### Stage 1: PM → Architect

**Intent:** PM brief becomes spec; Architect inherits + extends with design.

**Methodologies in chain:**
- `writing-design-documents` → `solo/sdd/sdd/writing-design-documents`
- `backlog-grooming-roadmapping` → `solo/sdd/sdd/backlog-grooming-roadmapping`
- `architecture-decision-records` → `solo/sdd/sdd/architecture-decision-records`
- `task-spec-kit-three-step` → `geek/sdlc-ai/task-spec-kit-three-step`

**Decision gate:**
> Advance only after Definition of Ready is signed off. Missing AC = block.

### Stage 2: Architect → Dev

**Intent:** Design becomes implementation-plan + worktrees + TDD split.

**Methodologies in chain:**
- `test-tdd-red-green-split-agents` → `geek/sdlc-ai/test-tdd-red-green-split-agents`
- `code-review` → `free/dev/code-quality/code-review`

**Decision gate:**
> Advance when implementation matches design + first tests are red.

### Stage 3: Dev → QA

**Intent:** Implementation delta + tests handed off to QA for acceptance signoff.

**Methodologies in chain:**
- `code-review` → `free/dev/code-quality/code-review`
- `test-tdd-red-green-split-agents` → `geek/sdlc-ai/test-tdd-red-green-split-agents`

**Decision gate:**
> Required: QA signoff. Implicit "looks fine" is not a signoff.

### Stage 4: QA → DevOps

**Intent:** Tested artifact handed off to DevOps with runbook + observability checklist.

**Methodologies in chain:**
- `inc-runbook-as-markdown-tagged-steps` → `geek/sdlc-ai/inc-runbook-as-markdown-tagged-steps`

**Decision gate:**
> Advance only when runbook is committed AND a fresh on-call has read it.

### Stage 5: DevOps → on-call handoff

**Intent:** Production release + on-call rotation absorbs the new path.

**Methodologies in chain:**
- `inc-runbook-as-markdown-tagged-steps` → `geek/sdlc-ai/inc-runbook-as-markdown-tagged-steps`

**Decision gate:**
> Required: on-call ack. Silent handoff = paging surprise.

## Common pitfalls

- Skipping DoR — handoff happens with incomplete context, work re-bounces
- Implicit QA signoff — bugs ship as "I assumed this was tested"
- Runbook handed to DevOps after deploy — first incident has no playbook
- On-call handoff in chat without ack — paging is the lesson

## Quality checklist (self-review)

- Is there ONE artifact, or multiple drifting copies?
- Did every handoff carry a written DoD signoff?
- Did the on-call rotation actually read the runbook?

## Related playbooks

- `rfc-to-production-feature-delivery`
- `sprint-planning-sdd-task-expansion`
- `incident-postmortem-preventive-backlog`

## Known gaps

The following methodologies are referenced or implied by this playbook but do not yet exist in the knowledge base. They are tracked in the manifest `gaps[]` array and block publication until resolved (BLOCK policy).
- **definition-of-ready-template** (tier `geek`, blocks stage 1) — PM → Architect stage needs a written DoR template enforced at handoff
- **definition-of-done-template** (tier `geek`, blocks stage 2) — Architect → Dev stage needs a written DoD template enforced at handoff
- **handoff-protocol-template** (tier `geek`, blocks stage 1) — Every handoff stage needs a generic protocol template (delta format, ack mechanism)
- **qa-acceptance-signoff-template** (tier `geek`, blocks stage 3) — Dev → QA stage needs an explicit acceptance signoff template
- **release-train-coordination** (tier `geek`, blocks stage 5) — DevOps → on-call stage needs cross-team release-train coordination when multiple squads ship together
- **on-call-handoff-protocol** (tier `geek`, blocks stage 5) — On-call handoff stage needs a written protocol with explicit acknowledgement step

## CLI usage

```
faion get-content cross-role-handoff-pm-architect-dev-qa-devops --format md       # human-readable rendering
faion get-content cross-role-handoff-pm-architect-dev-qa-devops --format context  # agent-optimised context bundle
faion get-content cross-role-handoff-pm-architect-dev-qa-devops --format json     # raw structured form
```
