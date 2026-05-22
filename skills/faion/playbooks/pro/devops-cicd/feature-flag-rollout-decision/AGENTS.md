---
slug: feature-flag-rollout-decision
tier: pro
group: devops-cicd
persona: P6
goal: TBD
complexity: medium
version: 0.1.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion
summary: Drifting feature flags → weekly tech-lead+PM review with explicit per-flag verdict (dark / ramp / GA / kill).
content_id: 52f7b553e94abd28
methodology_refs:
  - feature-flags-types-lifecycle
  - feature-flags-core-implementation
  - trunk-based-feature-flags
  - feature-flags-rollout-targeting
  - feature-flags-services-testing
  - release-planning
  - quality-gates-confidence
---

# Feature flag rollout decision (weekly)

**Playbook slug:** `feature-flag-rollout-decision`
**Tier:** pro
**Complexity:** medium
**Persona:** P6 — Product-Dev Team

## Intent

Drifting feature flags → weekly tech-lead+PM review with explicit per-flag verdict (dark / ramp / GA / kill).

## Scope

Tech lead + PM review every open feature flag once a week. For each flag, the verdict is one of: keep dark / ramp / GA / kill. Decision criteria are explicit (SLO impact, error rate, adoption metric, business intent). Flags that drift out of lifecycle get auto-flagged for deletion. The session ends with a written log of decisions and a flag-killswitch list.

### What this playbook covers

Three stages: inventory, apply criteria, write verdicts. The whole point is to refuse the most common feature-flag failure mode — flags that nobody decides on and that quietly accumulate as code rot and operational liability. The decision-log discipline is non-negotiable: weekly verdicts in writing, with the signals that supported them.

The session is co-owned by the PM (business intent + adoption goals) and the tech lead (capacity, SLO impact, dependencies). Single-owner reviews fail: PM-only reviews ignore reliability, tech-lead-only reviews ignore the business clock. Bring both. Hold the meeting to 30 minutes — any flag that needs longer is not a flag-decision problem, it's a missing-spec problem and belongs in grooming or RFC review.

The output (decision log + killed-flags schedule) is the load-bearing artefact: agents that pick up the codebase next week need to read the verdicts, not infer them.

### Non-goals

- Flag implementation choice — covered by `feature-flags-*` methodologies
- Feature delivery — see `rfc-to-production-feature-delivery`
- Engineering of the kill-switch — assumed already implemented

### Prerequisites

- Flag inventory tracked in version control
- SLO + error-rate metrics wired per flag
- Trunk-based + flag-aware development discipline

## Success criteria

The playbook is done when:
- Every open flag carries a verdict each week
- Drifting flags flagged for deletion
- Decision log appended with reasoning
- Killswitch path verified for any GA-pending flag

## Stages

### Stage 1: Inventory + classify

**Intent:** List flags by lifecycle stage; spot drift.

**Methodologies in chain:**
- `feature-flags-types-lifecycle` → `solo/dev/automation-tooling/feature-flags-types-lifecycle`
- `feature-flags-core-implementation` → `solo/dev/automation-tooling/feature-flags-core-implementation`
- `trunk-based-feature-flags` → `solo/dev/automation-tooling/trunk-based-feature-flags`

**Decision gate:**
> Advance once every flag is mapped to one of: dark / ramp / GA-pending / drifting.

### Stage 2: Apply decision criteria

**Intent:** Walk SLO + error + adoption + business-intent signals per flag.

**Methodologies in chain:**
- `feature-flags-rollout-targeting` → `solo/dev/automation-tooling/feature-flags-rollout-targeting`
- `feature-flags-services-testing` → `solo/dev/automation-tooling/feature-flags-services-testing`
- `release-planning` → `pro/product/product-manager/release-planning`
- `quality-gates-confidence` → `solo/sdd/sdd/quality-gates-confidence`

**Decision gate:**
> Advance when each flag has at least one quantitative signal supporting the proposed verdict. No vibes-only decisions.

### Stage 3: Verdict + commit

**Intent:** Write the verdict per flag; remove dead flags.

**Methodologies in chain:**
- `feature-flags-types-lifecycle` → `solo/dev/automation-tooling/feature-flags-types-lifecycle`
- `feature-flags-core-implementation` → `solo/dev/automation-tooling/feature-flags-core-implementation`

**Decision gate:**
> Required: written verdict per flag. Unresolved flags carry forward but must be tagged 'unresolved-prev-week'.

## Common pitfalls

- Flags marked "GA" but the killswitch was never tested — discovers at first incident
- Dark flags accumulate quarter-over-quarter — code rot
- Decisions live in head-of-lead — bus-factor failure
- Kill verdicts that aren't scheduled — flag never actually disappears

## Quality checklist (self-review)

- Can I name every open flag's owner and lifecycle stage?
- Did any flag get killed this week?
- Was the kill-switch on any GA-pending flag verified inside 24h?

## Related playbooks

- `rfc-to-production-feature-delivery`
- `backlog-grooming-pm-tech-lead`
- `sprint-planning-sdd-task-expansion`

## Known gaps

The following methodologies are referenced or implied by this playbook but do not yet exist in the knowledge base. They are tracked in the manifest `gaps[]` array and block publication until resolved (BLOCK policy).
- **feature-flag-weekly-review-template** (tier `pro`, blocks stage 3) — Verdict stage needs a written weekly-review template (agenda + decision log shape)
- **flag-killswitch-decision-criteria** (tier `pro`, blocks stage 2) — Criteria stage needs an explicit kill-switch rubric so weekly decisions are repeatable

## CLI usage

```
faion get-content feature-flag-rollout-decision --format md       # human-readable rendering
faion get-content feature-flag-rollout-decision --format context  # agent-optimised context bundle
faion get-content feature-flag-rollout-decision --format json     # raw structured form
```
