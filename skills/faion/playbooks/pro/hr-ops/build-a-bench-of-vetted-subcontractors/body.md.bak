# Build a bench of vetted subcontractors without becoming an agency-of-agencies

**Playbook slug:** `build-a-bench-of-vetted-subcontractors`
**Tier:** pro
**Complexity:** deep
**Persona:** P5 -- Micro-agency founder

## Intent

Stand up a 5-10 person freelance bench callable within 48h, with audition flow, rate card, IP boilerplate, quality-bar mechanism.

## Scope

Stand up a 5-10 person freelance bench you can call within 48h, with a documented audition flow, rate card, NDA/IP boilerplate, and quality-bar mechanism. Goal: deliver 2x revenue with no W-2 hires and without becoming a body shop. Exit artifact: bench tier-list + paperwork pack + activation runbook.

### What this playbook covers

This is a structured chain of existing faion methodologies adapted for a 2-3 person agency founder who is also the senior delivery operator. It assumes 1-3 contractors handle the rest. Every stage ends with an explicit decision gate so the operator can tell whether to advance, iterate, or kill -- agency founders drift fastest when client comfort overrides honest staging. Each chained methodology lives in the knowledge base and can be read via `faion get-content <methodology-slug>`. The chain order is intentional: skipping a stage typically surfaces as a billing, retention, or contractor problem two months later.

### Non-goals

- Hiring W-2 employees - bench is contractor-only
- Sub-contracting to other agencies - direct freelancers only

### Prerequisites

- Productized or repeatable service lines
- Standard contractor + IP paperwork in place

## Success criteria

The playbook is done when:
- 5-10 contractors vetted via paid audition
- Tiered bench (preferred / approved / on-trial)
- NDA + IP boilerplate signed by each
- Activation SLA 48h or less for a Tier-1 contractor
- Quality-bar review cadence in place

## Stages

### Stage 1: Define the bench shape

**Intent:** How many, what tiers, what rates, what coverage.

**Tasks:**
- List service lines requiring bench coverage
- Define tier criteria + rates
- Set bench size target

**Methodologies in chain:**
- `resource-management` -> `pro/pm/project-manager/resource-management`
- `ops-contractor-basics` -> `pro/marketing/gtm-strategist/ops-contractor-basics`
- `ops-contractor-management` -> `pro/marketing/gtm-strategist/ops-contractor-management`

**Outputs:**
- Bench tier map
- Rate card

**Decision gate:**
> Advance with explicit tier map + rate card.

### Stage 2: Source + audition

**Intent:** Paid audition for every candidate, structured rubric.

**Tasks:**
- Post role in 3 channels
- Issue paid trial
- Score against rubric

**Methodologies in chain:**
- `recruiting-process` -> `pro/comms/hr-recruiter/recruiting-process`
- `star-interview-framework` -> `pro/comms/hr-recruiter/star-interview-framework`
- `structured-interview-design` -> `pro/comms/hr-recruiter/structured-interview-design`

**Outputs:**
- Auditioned candidates
- Decisions per candidate

**Decision gate:**
> Advance once 5+ candidates passed audition.

### Stage 3: Paper + onboard

**Intent:** NDA + IP + classification + tax setup.

**Tasks:**
- Sign IP + NDA boilerplate
- Run worker-classification self-audit
- Onboard with bench runbook

**Methodologies in chain:**
- `onboarding` -> `pro/comms/hr-recruiter/onboarding`
- `ops-legal-basics` -> `pro/marketing/gtm-strategist/ops-legal-basics`

**Outputs:**
- Signed paperwork
- Classification audit

**Decision gate:**
> Advance only with all paperwork on file.

### Stage 4: Activation + quality bar

**Intent:** 48h activation SLA + quarterly quality bar review.

**Tasks:**
- Test 48h activation drill
- Set quarterly quality review
- Tier-down / tier-up based on results

**Methodologies in chain:**
- (no resolved methodologies -- see gaps below)

**Outputs:**
- Activation drill log
- Quality-bar review schedule

**Decision gate:**
> Required: 48h activation works in test AND review cadence on calendar.

## Common pitfalls

- Stacking the bench with friends - quality bar erodes silently
- Skipping IP boilerplate - kills enterprise resale potential
- Treating bench as static - never reviewing tiers leaves dead weight

## Quality checklist (self-review)

- Did I run a 48h activation drill, not just plan it?
- Are tiers honest, or are they vibes?
- Is the IP / classification paperwork airtight?

## Related playbooks

- `hire-and-onboard-a-new-contractor`
- `hiring-screen-contractor-audition`

## Known gaps

The following methodologies are referenced or implied by this playbook but do not yet exist in the knowledge base. They are tracked in the manifest `gaps[]` array and block publication until resolved (BLOCK policy).

- **contractor-audition-flow** (tier `pro`, blocks stage 2) -- Source-and-audition stage needs a documented end-to-end audition flow
- **bench-management-tiering** (tier `pro`, blocks stage 1) -- Define-the-bench-shape stage needs a bench tier-management framework
- **agency-ip-nda-boilerplate** (tier `pro`, blocks stage 3) -- Paper-and-onboard stage needs reusable IP + NDA boilerplate
- **worker-misclassification-self-audit** (tier `pro`, blocks stage 3) -- Paper-and-onboard stage needs a worker-classification self-audit tool

## CLI usage

```
faion get-content build-a-bench-of-vetted-subcontractors --format md       # human-readable rendering
faion get-content build-a-bench-of-vetted-subcontractors --format context  # agent-optimised context bundle
faion get-content build-a-bench-of-vetted-subcontractors --format json     # raw structured form
```
