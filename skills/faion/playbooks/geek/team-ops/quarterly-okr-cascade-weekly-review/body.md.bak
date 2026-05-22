# Quarterly OKR cascade, weekly review, post-quarter retro

**Playbook slug:** `quarterly-okr-cascade-weekly-review`
**Tier:** geek
**Complexity:** medium
**Persona:** P6 — Product-Dev Team

## Intent

Disconnected OKRs → cascaded company → team → personal OKRs with weekly check-ins and a quarterly blameless retro.

## Scope

Company OKR cascades to team OKR cascades to personal OKR. Weekly check-ins happen in 1:1s. A mid-quarter pivot gate decides whether to carry OKRs forward or rewrite. End-of-quarter blameless retro closes the loop. Output: every dev knows what their work ladders to, and the team has explicit carry-over rules.

### What this playbook covers

Four stages: cascade, weekly cadence, mid-quarter pivot gate, retro + carry-over. The chain refuses two common OKR failures — *inertia* (OKRs that don't get re-decided when they stop making sense) and *theater* (status-green-everything until the quarter ends red). The mid-quarter pivot gate is the load-bearing piece: in writing, with a verdict per OKR.

### Non-goals

- Setting the OKRs themselves — see `quarter-planning-okr-reset`
- Performance reviews — out of scope
- Daily/weekly delivery cadences — see `daily-standup-ai-prebrief` and `backlog-grooming-pm-tech-lead`

### Prerequisites

- Company OKRs published
- Team OKRs in place (from `quarter-planning-okr-reset`)
- 1:1 cadence wired between manager and each direct

## Success criteria

The playbook is done when:
- Personal OKRs cascaded for every dev
- Weekly check-in template used consistently
- Mid-quarter pivot gate evaluated
- Carry-over rules applied at quarter close
- Blameless retro doc published

## Stages

### Stage 1: Cascade to personal

**Intent:** Team OKRs → personal OKRs in every 1:1.

**Methodologies in chain:**
- `okr-setting` → `solo/product/product-planning/okr-setting`
- `reporting-basics` → `pro/pm/pm-agile/reporting-basics`

**Decision gate:**
> Advance only when each dev has 1-3 personal OKRs traceable to team OKRs.

### Stage 2: Weekly check-in cadence

**Intent:** OKR progress reviewed weekly in 1:1; status doesn't drift.

**Methodologies in chain:**
- `reporting-basics` → `pro/pm/pm-agile/reporting-basics`
- `reflexion-learning` → `solo/sdd/sdd/reflexion-learning`

**Decision gate:**
> Skip the check-in once = drift. Two skips = the cadence is dead.

### Stage 3: Mid-quarter pivot gate

**Intent:** At ~6 weeks: keep / revise / kill each OKR.

**Methodologies in chain:**
- `okr-setting` → `solo/product/product-planning/okr-setting`

**Decision gate:**
> Required: written keep/revise/kill verdict per OKR. Inertia = death of OKRs.

### Stage 4: Quarter close — retro + carry-over

**Intent:** Blameless retro + explicit carry-over rules.

**Methodologies in chain:**
- `reflexion-learning` → `solo/sdd/sdd/reflexion-learning`
- `mistake-memory` → `solo/sdd/sdd/mistake-memory`

**Decision gate:**
> Required: retro published before next-quarter OKRs land. Otherwise the next quarter repeats the same misses.

## Common pitfalls

- Personal OKRs don't ladder to team OKRs — confusion + drift
- Weekly check-ins skipped "just this week" — cadence dies fast
- No mid-quarter pivot gate — bad OKRs run to quarter end
- Carry-over rules implicit — last-minute disputes at quarter close

## Quality checklist (self-review)

- Can every dev name their personal OKRs and their lift to team OKRs?
- Did we hold a mid-quarter pivot decision in writing?
- Did the blameless retro happen before the next-quarter OKRs?

## Related playbooks

- `quarter-planning-okr-reset`
- `biweekly-retro-mistake-memory`
- `backlog-grooming-pm-tech-lead`

## Known gaps

The following methodologies are referenced or implied by this playbook but do not yet exist in the knowledge base. They are tracked in the manifest `gaps[]` array and block publication until resolved (BLOCK policy).
- **okr-cascade-multi-level** (tier `geek`, blocks stage 1) — Cascade stage needs a multi-level template (company → team → personal) with traceability
- **personal-okr-1on1-template** (tier `geek`, blocks stage 1) — Cascade stage needs a 1:1-shaped template for personal OKRs
- **okr-weekly-check-in-template** (tier `geek`, blocks stage 2) — Weekly check-in stage needs a structured template (status + blocker + ask)
- **mid-quarter-pivot-gate** (tier `geek`, blocks stage 3) — Pivot stage needs explicit keep/revise/kill rubric
- **blameless-retrospective-facilitation** (tier `geek`, blocks stage 4) — Retro stage needs a facilitation guide tuned for blameless tone
- **okr-carry-over-rules** (tier `geek`, blocks stage 4) — Quarter-close stage needs explicit carry-over rules so last-minute debates don't happen

## CLI usage

```
faion get-content quarterly-okr-cascade-weekly-review --format md       # human-readable rendering
faion get-content quarterly-okr-cascade-weekly-review --format context  # agent-optimised context bundle
faion get-content quarterly-okr-cascade-weekly-review --format json     # raw structured form
```
