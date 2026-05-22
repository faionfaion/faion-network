---
slug: quarter-planning-okr-reset
tier: geek
group: team-ops
persona: P6
goal: operate-ritual
complexity: deep
version: 0.1.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion
summary: Quarter closes with stale OKRs and ad-hoc backlog → next quarter starts with published OKRs, top-3 sized bets, RACI, and a populated backlog.
content_id: f94223e8421be5af
methodology_refs:
  - lessons-learned
  - project-closure
  - benefits-realization
  - dora-metrics
  - ba-planning
  - requirements-traceability
  - raci-matrix
  - stakeholder-engagement-advanced
  - communications-management
  - opportunity-solution-trees
  - competitive-positioning
  - continuous-discovery-habits
  - portfolio-strategy
  - cost-estimation
  - methodologies-summary
  - release-planning
  - scope-management
  - wbs-creation
  - resource-management
  - risk-management
  - risk-register
  - change-control
  - quality-attributes-analysis
  - ai-assisted-specification-writing
  - tracker-linear-agent-as-assignee
---

# Quarter planning + OKR reset (end-to-end)

**Playbook slug:** `quarter-planning-okr-reset`
**Tier:** geek
**Complexity:** deep
**Persona:** P6 — Product-Dev Team

## Intent

Quarter closes with stale OKRs and ad-hoc backlog → next quarter starts with published OKRs, top-3 sized bets, RACI, and a populated backlog.

## Scope

A 2-10 person product-dev team closes one quarter and opens the next. Retro + lessons learned land first, then next-quarter OKRs are written, top-3 feature bets are sized and sequenced into a roadmap, capacity is confirmed per squad, and every role (PM, PdM, Architect, BA, Dev leads, DevOps, QA, Growth) knows what they own. Exit artifacts: roadmap doc, OKR sheet, RACI per bet, populated `backlog/` directory.

### What this playbook covers

This is a deep, multi-session sequence that turns the quarter boundary into a forcing function. Teams that skip it drift: backlogs grow into wishlists, OKRs become decoration, and every standup turns into status theater. The chain is intentionally heavy on PM/BA methodologies in the middle stages because the failure mode of product-dev teams is not lack of execution discipline — it is lack of priority discipline. By Stage 5 you have AI-assisted specs, but only because the human disagreements have been resolved upstream.

### Non-goals

- Daily/weekly cadences (covered by `daily-standup-ai-prebrief`, `backlog-grooming-pm-tech-lead`)
- Hiring or org-design — handled in `hire-onboard-product-dev-2-weeks` and `hire-to-productive-60-days-in-house`
- Customer-facing roadmap publishing — internal artifacts only

### Prerequisites

- At least one full quarter of delivery data (DORA metrics + Linear/Jira tickets)
- Documented company-level OKRs to cascade from

## Success criteria

The playbook is done when:
- Quarter-closing retro doc published with lessons-learned synthesis
- Next-quarter team OKRs written, reviewed, signed off
- Top-3 feature bets sized (complexity tag + token estimate) and sequenced on roadmap
- RACI matrix exists per bet, every role named
- `backlog/` populated with spec-ready stories for at least the first two bets
- Squad capacity confirmed against bet sizing
- Risk register refreshed and reviewed

## Stages

### Stage 1: Close the quarter

**Intent:** Retro + lessons learned synthesised before any forward planning.

**Tasks:**
- Pull DORA metrics + delivery data for the closing quarter
- Run a blameless retro with the full team
- Use an AI agent to synthesise lessons learned across tickets, postmortems, mistake-memory
- Publish quarter-closure doc with explicit kept/changed/dropped items

**Methodologies in chain:**
- `lessons-learned` → `pro/pm/pm-traditional/lessons-learned`
- `project-closure` → `pro/pm/pm-traditional/project-closure`
- `benefits-realization` → `pro/pm/pm-traditional/benefits-realization`
- `dora-metrics` → `pro/infra/cicd-engineer/dora-metrics`

**Outputs:** Quarter-closure doc; lessons-learned synthesis.

**Decision gate:**
> Advance only when retro + lessons-learned are written down. If retro is verbal-only, stay in this stage — the next quarter inherits the same mistakes.

### Stage 2: Cascade OKRs

**Intent:** Company OKRs → team OKRs → personal commitments.

**Tasks:**
- Translate the company OKRs into team-scope objectives
- Define 3-5 measurable key results per objective
- Draft RACI per objective
- Validate against capacity reality

**Methodologies in chain:**
- `ba-planning` → `pro/ba/business-analyst/ba-planning`
- `requirements-traceability` → `pro/ba/business-analyst/requirements-traceability`
- `raci-matrix` → `pro/pm/pm-agile/raci-matrix`
- `stakeholder-engagement-advanced` → `pro/pm/project-manager/stakeholder-engagement-advanced`
- `communications-management` → `pro/pm/project-manager/communications-management`

**Outputs:** Team OKR sheet; RACI per objective.

**Decision gate:**
> Advance when each KR has a numeric target AND a named owner. Reject vague verbs ("improve", "explore") — they belong in mission, not OKRs.

### Stage 3: Pick the bets

**Intent:** Choose top-3 feature bets that ladder to OKRs — kill the rest for the quarter.

**Tasks:**
- Run opportunity-solution-tree workshop
- Score candidates by impact × confidence × cost
- Confirm competitive positioning context
- Size each bet (complexity tag + token estimate, no time estimates)

**Methodologies in chain:**
- `opportunity-solution-trees` → `pro/ux/user-researcher/opportunity-solution-trees`
- `competitive-positioning` → `pro/product/product-manager/competitive-positioning`
- `continuous-discovery-habits` → `pro/product/product-manager/continuous-discovery-habits`
- `portfolio-strategy` → `pro/product/product-manager/portfolio-strategy`
- `cost-estimation` → `pro/pm/pm-traditional/cost-estimation`
- `methodologies-summary` → `pro/product/product-manager/methodologies-summary`

**Outputs:** Sized bet list; killed-candidates list with rationale.

**Decision gate:**
> Advance once exactly 3 bets are sized and the rejected candidates are documented. More than 3 = no priorities at all.

### Stage 4: Sequence + size

**Intent:** Bets become a quarter roadmap with capacity confirmation.

**Tasks:**
- Sequence bets by dependency + value flow
- Confirm squad capacity vs sized work
- Define WBS-style breakdown for the first two bets
- Refresh risk register

**Methodologies in chain:**
- `release-planning` → `pro/product/product-manager/release-planning`
- `scope-management` → `pro/pm/pm-traditional/scope-management`
- `wbs-creation` → `pro/pm/pm-traditional/wbs-creation`
- `resource-management` → `pro/pm/pm-traditional/resource-management`
- `risk-management` → `pro/pm/pm-traditional/risk-management`
- `risk-register` → `pro/pm/pm-traditional/risk-register`
- `change-control` → `pro/pm/pm-traditional/change-control`
- `quality-attributes-analysis` → `pro/dev/software-architect/quality-attributes-analysis`

**Outputs:** Quarter roadmap doc; refreshed risk register.

**Decision gate:**
> Advance when sized work fits inside confirmed capacity with explicit buffer. If overcommit, cut scope here, not mid-quarter.

### Stage 5: Populate the backlog

**Intent:** Spec-ready stories land in `backlog/` for the first two bets with AI-assisted spec writing.

**Tasks:**
- Use AI-assisted spec writing to draft initial spec.md per bet
- Define acceptance criteria + Definition of Ready
- Wire tracker handoff (Linear agent as assignee where possible)

**Methodologies in chain:**
- `ai-assisted-specification-writing` → `geek/sdd/sdd-planning/ai-assisted-specification-writing`
- `tracker-linear-agent-as-assignee` → `geek/sdlc-ai/tracker-linear-agent-as-assignee`

**Outputs:** Spec drafts in `backlog/`; tracker mirror per bet.

**Decision gate:**
> Advance when at least the first two bets have spec.md drafts plus acceptance criteria — promotion to `todo/` happens later under backlog-grooming and sprint-planning playbooks.

## Common pitfalls

- OKRs written before retro — repeats last quarter's mistakes
- More than 3 bets — guarantees nothing finishes
- Sizing in hours/days — violates No-Time-Estimates rule, surfaces fake precision
- Skipping risk register refresh — old risks linger and surprise mid-quarter

## Quality checklist (self-review)

- Can every dev point to their bet and its KR in one sentence?
- Did we cut at least one candidate that "felt important"?
- Are the top-2 bets spec-ready in `backlog/`?

## Related playbooks

- `quarterly-okr-cascade-weekly-review`
- `backlog-grooming-pm-tech-lead`
- `sprint-planning-sdd-task-expansion`
- `biweekly-retro-mistake-memory`

## Known gaps

The following methodologies are referenced or implied by this playbook but do not yet exist in the knowledge base. They are tracked in the manifest `gaps[]` array and block publication until resolved (BLOCK policy).
- **okr-cascade-template-product-dev-team** (tier `geek`, blocks stage 2) — Cascade stage needs a concrete company→team→personal OKR template tuned for product-dev teams
- **ai-assisted-quarter-retro-synthesis** (tier `geek`, blocks stage 1) — Quarter-close retro lacks a prompt + workflow for AI-assisted synthesis across tickets, postmortems, mistake-memory

## CLI usage

```
faion get-content quarter-planning-okr-reset --format md       # human-readable rendering
faion get-content quarter-planning-okr-reset --format context  # agent-optimised context bundle
faion get-content quarter-planning-okr-reset --format json     # raw structured form
```
