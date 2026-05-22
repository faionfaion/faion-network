---
slug: hiring-screen-contractor-audition
tier: pro
group: hr-ops
persona: P5
goal: TBD
complexity: medium
version: 0.1.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion
summary: New contractor candidate to hire / reject / shortlist decision in under a week with paid trial result.
content_id: 18c6f78358f37cf2
methodology_refs:
  - acceptance-criteria
  - ops-contractor-basics
  - structured-interview-design
  - interview-methods
  - star-interview-framework
  - onboarding
  - 30-60-90-day-plan
---

# Hiring screen / contractor audition

**Playbook slug:** `hiring-screen-contractor-audition`
**Tier:** pro
**Complexity:** medium
**Persona:** P5 -- Micro-agency founder

## Intent

New contractor candidate to hire / reject / shortlist decision in under a week with paid trial result.

## Scope

Founder evaluates a new contractor candidate in under a week. Output: hire / reject / shortlist decision with paid trial result. Exit artifact: rubric score + written decision + paid trial deliverable.

### What this playbook covers

This is a structured chain of existing faion methodologies adapted for a 2-3 person agency founder who is also the senior delivery operator. It assumes 1-3 contractors handle the rest. Every stage ends with an explicit decision gate so the operator can tell whether to advance, iterate, or kill -- agency founders drift fastest when client comfort overrides honest staging. Each chained methodology lives in the knowledge base and can be read via `faion get-content <methodology-slug>`. The chain order is intentional: skipping a stage typically surfaces as a billing, retention, or contractor problem two months later.

### Non-goals

- Long multi-month hiring pipeline - atomic ritual
- Unpaid 'test projects' - never asked

### Prerequisites

- Role brief + rubric ready
- Paid trial budget allocated (4-8h equivalent)

## Success criteria

The playbook is done when:
- Trial completed and scored
- 30-min synthesis interview held
- Decision (hire / reject / shortlist) within 7 days of trial
- Written feedback sent to candidate

## Stages

### Stage 1: Issue trial

**Intent:** Paid task that mirrors actual work, scoped to 4-8h.

**Tasks:**
- Pick task from paid-trial library
- Specify AC + deliverable format
- Confirm rate + timing in writing

**Methodologies in chain:**
- `acceptance-criteria` -> `pro/ba/business-analyst/acceptance-criteria`
- `ops-contractor-basics` -> `pro/marketing/gtm-strategist/ops-contractor-basics`

**Outputs:**
- Issued trial brief
- Payment terms confirmed

**Decision gate:**
> Advance when trial brief accepted in writing.

### Stage 2: Score against rubric

**Intent:** Structured scoring, no vibes.

**Tasks:**
- Score deliverable on rubric
- Capture written feedback
- Tag risks (comms, quality, timing)

**Methodologies in chain:**
- `structured-interview-design` -> `pro/comms/hr-recruiter/structured-interview-design`
- `interview-methods` -> `pro/comms/hr-recruiter/interview-methods`
- `star-interview-framework` -> `pro/comms/hr-recruiter/star-interview-framework`

**Outputs:**
- Rubric scores
- Risk tags

**Decision gate:**
> Advance only once rubric scored and feedback drafted.

### Stage 3: Synthesis interview

**Intent:** 30 min: behavior + comms + escalation reflexes.

**Tasks:**
- Walk through trial deliverable with candidate
- Probe communication + escalation behaviors
- Confirm availability + rate

**Methodologies in chain:**
- `interview-methods` -> `pro/comms/hr-recruiter/interview-methods`
- `onboarding` -> `pro/comms/hr-recruiter/onboarding`
- `30-60-90-day-plan` -> `pro/comms/hr-recruiter/30-60-90-day-plan`

**Outputs:**
- Interview notes

**Decision gate:**
> Advance once interview complete.

### Stage 4: Decide + send feedback

**Intent:** Decision + written feedback within 7 days.

**Tasks:**
- Apply decision rule
- Send written feedback (hire / reject / shortlist)
- Trigger contract or shortlist note

**Methodologies in chain:**
- (no resolved methodologies -- see gaps below)

**Outputs:**
- Decision doc
- Feedback sent

**Decision gate:**
> Required: written decision + feedback within 7 days of trial completion.

## Common pitfalls

- Skipping paid trial 'because they have a great portfolio'
- Scoring on vibes - no rubric, no signal
- Ghosting rejected candidates - kills your referral channel

## Quality checklist (self-review)

- Did the trial mirror actual work?
- Could a different person score the rubric the same way?
- Did I send feedback to every candidate?

## Related playbooks

- `hire-and-onboard-a-new-contractor`
- `subcontractor-task-brief-generation`

## Known gaps

The following methodologies are referenced or implied by this playbook but do not yet exist in the knowledge base. They are tracked in the manifest `gaps[]` array and block publication until resolved (BLOCK policy).

- **contractor-audition-rubric** (tier `pro`, blocks stage 2) -- Score-against-rubric stage needs an explicit audition rubric
- **paid-trial-task-library** (tier `pro`, blocks stage 1) -- Issue-trial stage needs a library of paid trial tasks by role
- **hiring-funnel** (tier `pro`, blocks stage 1) -- Issue-trial stage references hiring-funnel playbook not yet ported to v2 manifest
- **technical-interview-process** (tier `pro`, blocks stage 3) -- Synthesis-interview stage references technical-interview-process playbook not yet ported to v2 manifest
- **onboarding-30-60-90** (tier `pro`, blocks stage 4) -- Decide stage references onboarding-30-60-90 playbook not yet ported to v2 manifest

## CLI usage

```
faion get-content hiring-screen-contractor-audition --format md       # human-readable rendering
faion get-content hiring-screen-contractor-audition --format context  # agent-optimised context bundle
faion get-content hiring-screen-contractor-audition --format json     # raw structured form
```
