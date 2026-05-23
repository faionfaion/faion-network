# Hire-to-productive in 60 days for in-house product roles

**Playbook slug:** `hire-to-productive-60-days-in-house`
**Tier:** geek
**Complexity:** deep
**Persona:** P6 — Product-Dev Team

## Intent

Open req → first owned feature shipped by day 45 in an in-house product team (not agency client engagement).

## Scope

Funnel from job posting → sourcing → structured interview → offer → 30/60-day onboarding tuned for in-house product context. Output: new hire shipping their first owned feature by day 45, fully ramped on the codebase orientation tour, role-specific interview rubric used during hiring, and in-house take-home design (not agency-style "build me a thing").

### What this playbook covers

Four stages that connect hiring funnel to first-owned-feature shipped. The chain is explicit about *in-house ≠ agency*: take-home design, onboarding shape, and feature ownership all differ. Day-45 first owned feature is the load-bearing milestone; day-60 retro is the early retention check.

### Non-goals

- Agency client engagement onboarding — different problem
- Compensation / negotiation — separate workstream
- Performance reviews past day 60 — out of scope

### Prerequisites

- Open req tied to a quarter OKR
- Hiring funnel + technical-interview-process playbooks available
- Codebase has CLAUDE.md + AGENTS.md context pyramid

## Success criteria

The playbook is done when:
- Structured interview run with role-specific rubric
- In-house-style take-home administered (not agency-style)
- 30-day plan executed (orient + ramp)
- 60-day plan executed (own feature)
- First owned feature shipped by day 45
- Day-60 retro between hire + manager + buddy

## Stages

### Stage 1: Open req + structured interview

**Intent:** Funnel → structured interview with role-specific rubric → offer.

**Methodologies in chain:**
- `structured-interview-design` → `pro/comms/hr-recruiter/structured-interview-design`
- `interview-methods` → `pro/comms/hr-recruiter/interview-methods`
- `star-interview-framework` → `pro/comms/hr-recruiter/star-interview-framework`
- `star-interview-method` → `pro/comms/hr-recruiter/star-interview-method`
- `employee-value-proposition` → `pro/comms/hr-recruiter/employee-value-proposition`

**Decision gate:**
> Advance only with a hire decision backed by rubric evidence + bias check.

### Stage 2: Day 1-14 — orient + first PR

**Intent:** Hire is incident-literate, has run the dev loop locally, has merged a small PR.

**Methodologies in chain:**
- `onboarding-30-day` → `pro/comms/hr-recruiter/onboarding-30-day`
- `onboarding` → `pro/comms/hr-recruiter/onboarding`
- `30-60-90-day-plan` → `pro/comms/hr-recruiter/30-60-90-day-plan`

**Decision gate:**
> Advance when 14-day retro passes. Repeating week-1 problems = block.

### Stage 3: Day 15-45 — own a feature

**Intent:** Hire scopes, designs, ships their first owned feature.

**Methodologies in chain:**
- `onboarding-60-90-day` → `pro/comms/hr-recruiter/onboarding-60-90-day`

**Decision gate:**
> Required: shipped feature behind a flag. Half-shipped doesn't count.

### Stage 4: Day 60 — retro + retention

**Intent:** 60-day retro; retention checkpoint; promotion-eligibility decision (later).

**Methodologies in chain:**
- `retention-compliance` → `pro/comms/hr-recruiter/retention-compliance`
- `lessons-learned` → `pro/pm/pm-traditional/lessons-learned`

**Decision gate:**
> Required: written retro. If retention signals are weak, escalate now, not at day 90.

## Common pitfalls

- Agency-style take-home for an in-house role — wrong signal
- 30/60 plan filed but never reviewed — guarantees drift
- Skipping the day-60 retro "because things look fine" — misses early retention signals
- No first owned feature by day 45 — hire learns the team isn't serious about ramp

## Quality checklist (self-review)

- Can the hire describe the team's spec→ship chain end-to-end?
- Did the first owned feature ship through the same gates as everyone else?
- Is the 60-day retro written and shared?

## Related playbooks

- `hire-onboard-product-dev-2-weeks`
- `hiring-screen-take-home-review`
- `adopt-faion-org-wide-overrides`
- `rfc-to-production-feature-delivery`

## Known gaps

The following methodologies are referenced or implied by this playbook but do not yet exist in the knowledge base. They are tracked in the manifest `gaps[]` array and block publication until resolved (BLOCK policy).
- **role-specific-interview-rubrics** (tier `geek`, blocks stage 1) — Structured-interview stage needs per-role rubrics (PM, PdM, Architect, BA, Dev, DevOps, QA)
- **in-house-take-home-design** (tier `geek`, blocks stage 1) — Take-home stage needs an in-house-flavoured design (not agency 'build me a thing')
- **in-house-onboarding-playbook** (tier `geek`, blocks stage 2) — Day 1-14 stage needs an in-house onboarding playbook distinct from client-engagement
- **codebase-orientation-tour-template** (tier `geek`, blocks stage 2) — Day 1-14 stage needs a codebase orientation tour template the buddy walks the hire through

## CLI usage

```
faion get-content hire-to-productive-60-days-in-house --format md       # human-readable rendering
faion get-content hire-to-productive-60-days-in-house --format context  # agent-optimised context bundle
faion get-content hire-to-productive-60-days-in-house --format json     # raw structured form
```
