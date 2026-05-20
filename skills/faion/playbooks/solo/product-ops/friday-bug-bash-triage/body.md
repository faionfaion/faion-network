# Friday bug-bash and tech-debt triage hour

**Playbook slug:** `friday-bug-bash-triage`  
**Tier:** solo  
**Complexity:** light  
**Persona:** P1 — Solo SaaS Builder

## Intent

Open bug tracker + sprawling debt list → grouped, severity-tagged, top-3 resolved or queued.

## Scope

60-minute Friday ritual: Sentry / GitHub issues grouped, severity-tagged, top-3 fixed or queued, debt list updated with one decision per item (fix now / accept / kill). Exit artifact is clean tracker view + updated debt log.

### What this playbook covers

This is a structured chain of existing faion methodologies adapted for a single-operator SaaS founder. It assumes no team, no SRE rotation, no co-founder. Every stage ends with an explicit decision gate so the operator can tell whether to advance, iterate, or kill — solo founders drift fastest where stages don't end cleanly.

### Non-goals

- Major refactors — debt items get queued, not executed
- Customer-facing comms — separate inbox-sweep playbook

### Prerequisites

- Issue tracker exists (GitHub, Linear, or similar)
- Sentry/logging in place (monitoring-logging complete)

## Success criteria

The playbook is done when:
- All open issues have severity tag
- Top 3 issues either fixed or scheduled with owner
- Debt log: every item has decision (fix-now / accept / kill)
- Ritual completed in ≤60 minutes

## Stages

### Stage 1: Group

**Intent:** Cluster bugs by theme; surface duplicates.

**Tasks:**
- Pull open issues + Sentry events
- Tag by theme + severity
- Merge duplicates

**Methodologies in chain:**
- `logging-patterns` → `solo/dev/automation-tooling/logging-patterns`
- `feedback-management` → `solo/product/product-operations/feedback-management`
- `backlog-management` → `solo/product/product-operations/backlog-management`

**Outputs:**
- Grouped issue list

**Decision gate:**
> Advance when every issue has theme + severity. Refuse to skip — solo founders accumulate noise fast.

### Stage 2: Decide

**Intent:** One decision per item: fix now, accept, or kill.

**Tasks:**
- Score top items against impact + effort
- Write decision per item
- Update debt log

**Methodologies in chain:**
- `tech-debt-basics` → `free/dev/code-quality/tech-debt-basics`
- `tech-debt-management` → `solo/dev/code-quality/tech-debt-management`
- `technical-debt` → `solo/dev/software-developer/technical-debt`
- `technical-debt-management` → `solo/product/product-operations/technical-debt-management`
- `refactoring-patterns` → `free/dev/code-quality/refactoring-patterns`
- `architecture-decision-records` → `solo/sdd/sdd/architecture-decision-records`

**Outputs:**
- Debt log with decisions

**Decision gate:**
> Advance when every top-10 item has a decision. No 'maybe later'.

### Stage 3: Ship

**Intent:** Fix the top-3 chosen items inside the hour.

**Tasks:**
- Pick 3 with highest impact-per-effort
- Ship with feature flag if risky
- Push to staging

**Methodologies in chain:**
- `feature-flags` → `solo/dev/software-developer/feature-flags`

**Outputs:**
- 3 fixes shipped

**Decision gate:**
> Required output: 3 PRs merged. Defer remainder to next week's bash.

## Common pitfalls

- Trying to fix all of them — guarantees nothing ships
- Leaving items without decision — they rot in the backlog

## Quality checklist (self-review)

- Did every item I touched get a decision, or did I leave some 'open'?
- Are the 3 I fixed actually high-impact, or just easy?

## Related playbooks

- `sunday-roadmap-ritual`
- `deploy-day-staging-to-prod`

## Known gaps

The following methodologies are referenced or implied by this playbook but do not yet exist in the knowledge base. They are tracked in the manifest `gaps[]` array and block publication until resolved (BLOCK policy).
- **solo-bug-triage-rubric** (tier `solo`, blocks stage 2) — Decide stage needs rubric tailored to one-operator severity calls
- **sentry-alert-routing-for-solos** (tier `solo`, blocks stage 1) — Group stage needs Sentry routing config to cut noise at the source

## CLI usage

```
faion get-content friday-bug-bash-triage --format md       # human-readable rendering
faion get-content friday-bug-bash-triage --format context  # agent-optimised context bundle
faion get-content friday-bug-bash-triage --format json     # raw structured form
```
