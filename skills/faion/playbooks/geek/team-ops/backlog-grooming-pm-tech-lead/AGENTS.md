---
slug: backlog-grooming-pm-tech-lead
tier: geek
group: team-ops
persona: P6
goal: TBD
complexity: medium
version: 0.1.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion
summary: Open backlog of mixed maturity → top-of-backlog spec-ready (AC + complexity tag) each week in 1 hour.
content_id: a2c48ebe4f04761c
methodology_refs:
  - backlog-management
  - backlog-grooming-roadmapping
  - backlog-grooming-roadmapping-sdd
  - acceptance-criteria
  - user-story-mapping
  - task-creation-principles
  - impl-plan-100k-rule
  - task-creation-parallelization
  - quality-gates-confidence
  - tech-debt-management
---

# Backlog grooming with PM + tech lead (weekly)

**Playbook slug:** `backlog-grooming-pm-tech-lead`
**Tier:** geek
**Complexity:** medium
**Persona:** P6 — Product-Dev Team

## Intent

Open backlog of mixed maturity → top-of-backlog spec-ready (AC + complexity tag) each week in 1 hour.

## Scope

Weekly 1-hour grooming session: PM brings business priorities, tech lead brings tech-debt + capacity reality. Goal: only the top of the backlog is spec-ready (acceptance criteria + estimated complexity), everything else stays untouched. AI agent splits oversized items into sub-tasks. Tech-debt has a fixed slot quota per cycle. Session ends with a written grooming-decisions log.

### What this playbook covers

Three tight stages: walk the top of the backlog with maturity tags, make spec-ready, balance and log. The session is intentionally bounded to one hour — grooming sessions that drift past 90 minutes are a signal that maturity work belongs to async pre-reads, not the meeting.

The hour is co-owned: PM brings prioritisation pressure, tech lead brings capacity reality and the tech-debt slot quota. Either-only sessions fail. Below the spec-ready line, items stay dormant on purpose — grooming dormant items is theatre that absorbs hours without producing claimable work. AI agents split anything oversized at the top, but they don't decide priority; that's a human call rooted in OKRs and tech-debt accumulation rate.

The grooming-decisions log is the durable output. Without it, every week the same two arguments repeat (which feature is highest priority, how much tech-debt slot quota is "enough") and the same hour evaporates.

### Non-goals

- Sprint planning — see `sprint-planning-sdd-task-expansion`
- Quarter-level prioritisation — see `quarter-planning-okr-reset`
- Day-to-day triage — see `daily-standup-ai-prebrief`

### Prerequisites

- Backlog exists with at least 10 items beyond current sprint
- Tech-debt register tagged in tracker
- AI agent able to propose task splits from spec

## Success criteria

The playbook is done when:
- Top of backlog spec-ready (AC + complexity tag)
- Oversized items split
- Tech-debt slot quota respected
- Grooming-decisions log appended

## Stages

### Stage 1: Walk the backlog

**Intent:** Cover top-N items; classify maturity.

**Methodologies in chain:**
- `backlog-management` → `solo/product/product-operations/backlog-management`
- `backlog-grooming-roadmapping` → `solo/sdd/sdd-planning/backlog-grooming-roadmapping`
- `backlog-grooming-roadmapping-sdd` → `solo/sdd/sdd/backlog-grooming-roadmapping`

**Decision gate:**
> Advance once every top-N item has a maturity tag. Don't groom below the line — that's pretend-work.

### Stage 2: Make spec-ready

**Intent:** Top-of-backlog items become spec-ready: AC + complexity tag.

**Methodologies in chain:**
- `acceptance-criteria` → `pro/ba/business-analyst/acceptance-criteria`
- `user-story-mapping` → `pro/ba/business-analyst/user-story-mapping`
- `task-creation-principles` → `solo/sdd/sdd-planning/task-creation-principles`
- `impl-plan-100k-rule` → `solo/sdd/sdd-planning/impl-plan-100k-rule`
- `task-creation-parallelization` → `solo/sdd/sdd/task-creation-parallelization`
- `quality-gates-confidence` → `solo/sdd/sdd/quality-gates-confidence`

**Decision gate:**
> Advance when each spec-ready item has AC + complexity tag. Don't promote anything without both.

### Stage 3: Balance the slate + log decisions

**Intent:** Honour tech-debt quota; write grooming-decisions log.

**Methodologies in chain:**
- `tech-debt-management` → `solo/dev/code-quality/tech-debt-management`

**Decision gate:**
> Required: written log. Verbal-only grooming guarantees next week's session repeats the same arguments.

## Common pitfalls

- Grooming below the line — wastes session on items nobody will pick up
- Tech-debt quota slips — accumulates into a quarter-end crisis
- Oversized items left whole — sprint planning blocks on them
- Decisions stay verbal — same debates repeat weekly

## Quality checklist (self-review)

- Can a dev claim the top item and start without re-asking what 'done' means?
- Did we close at least one tech-debt slot this week?
- Did the session end in 1 hour?

## Related playbooks

- `quarter-planning-okr-reset`
- `sprint-planning-sdd-task-expansion`
- `daily-standup-ai-prebrief`

## Known gaps

The following methodologies are referenced or implied by this playbook but do not yet exist in the knowledge base. They are tracked in the manifest `gaps[]` array and block publication until resolved (BLOCK policy).
- **pm-tech-lead-grooming-agenda** (tier `geek`, blocks stage 1) — Walk-the-backlog stage needs a fixed weekly agenda template
- **tech-debt-slot-quota-policy** (tier `geek`, blocks stage 3) — Balance stage needs a written tech-debt slot quota policy so it's not negotiated weekly

## CLI usage

```
faion get-content backlog-grooming-pm-tech-lead --format md       # human-readable rendering
faion get-content backlog-grooming-pm-tech-lead --format context  # agent-optimised context bundle
faion get-content backlog-grooming-pm-tech-lead --format json     # raw structured form
```
