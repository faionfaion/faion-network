---
slug: project-from-kickoff-to-client-signoff
tier: pro
group: delivery-ops
persona: P5
goal: TBD
complexity: deep
version: 0.1.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion
summary: Signed SOW to delivered project with measured margin, NPS, and a retainer-or-referral conversation booked.
content_id: 886574453b6d5fc3
methodology_refs:
  - communications-management
  - raci-matrix
  - risk-management
  - risk-register
  - stakeholder-engagement
  - acceptance-criteria
  - elicitation-techniques
  - requirements-documentation
  - requirements-prioritization
  - requirements-traceability
  - schedule-development
  - scope-management
  - scrum-ceremonies
  - kanban-scaled-agile-ceremonies
  - earned-value-management
  - quality-management
  - team-development
  - requirements-validation
  - change-control
  - solution-assessment
  - stakeholder-engagement-advanced
  - benefits-realization
  - lessons-learned
  - project-closure
  - ops-customer-success-metrics
  - ops-upselling-cross-selling
---

# Project from kickoff to client signoff (8-12 weeks)

**Playbook slug:** `project-from-kickoff-to-client-signoff`
**Tier:** pro
**Complexity:** deep
**Persona:** P5 -- Micro-agency founder

## Intent

Signed SOW to delivered project with measured margin, NPS, and a retainer-or-referral conversation booked.

## Scope

A signed SOW becomes a delivered project: kickoff, requirements baseline, delivery in waves, change-controlled scope, final acceptance, retainer-or-referral conversation. Net margin and NPS measured. Exit artifact: closure pack (lessons-learned, NPS, margin row, referral or retainer follow-up scheduled).

### What this playbook covers

This is a structured chain of existing faion methodologies adapted for a 2-3 person agency founder who is also the senior delivery operator. It assumes 1-3 contractors handle the rest. Every stage ends with an explicit decision gate so the operator can tell whether to advance, iterate, or kill -- agency founders drift fastest when client comfort overrides honest staging. Each chained methodology lives in the knowledge base and can be read via `faion get-content <methodology-slug>`. The chain order is intentional: skipping a stage typically surfaces as a billing, retention, or contractor problem two months later.

### Non-goals

- Multi-year transformation programs - out of scope
- Fully software-product delivery - separate playbook

### Prerequisites

- Signed SOW + deposit cleared
- Identified delivery lead (founder or contractor)

## Success criteria

The playbook is done when:
- Kickoff held within 5 working days of signature
- Baselined requirements with traceability to acceptance criteria
- Scope changes processed via change-control with priced CRs
- Final acceptance signed by client
- Closure pack delivered: lessons-learned + NPS + margin
- Retainer-or-referral conversation booked

## Stages

### Stage 1: Kickoff

**Intent:** Set rhythm, RACI, escalation; baseline scope and risks.

**Tasks:**
- Run 60-90 min kickoff meeting
- Publish RACI + comms cadence
- Open risk register

**Methodologies in chain:**
- `communications-management` -> `pro/pm/project-manager/communications-management`
- `raci-matrix` -> `pro/pm/project-manager/raci-matrix`
- `risk-management` -> `pro/pm/project-manager/risk-management`
- `risk-register` -> `pro/pm/project-manager/risk-register`
- `stakeholder-engagement` -> `pro/pm/project-manager/stakeholder-engagement`

**Outputs:**
- Kickoff deck
- Published RACI + cadence
- Risk register v1

**Decision gate:**
> Advance once stakeholders confirmed RACI + cadence in writing.

### Stage 2: Baseline + plan

**Intent:** Lock requirements + acceptance criteria + schedule.

**Tasks:**
- Elicit + document requirements
- Prioritize + traceability-link to AC
- Develop schedule with milestones

**Methodologies in chain:**
- `acceptance-criteria` -> `pro/ba/ba-modeling/acceptance-criteria`
- `elicitation-techniques` -> `pro/ba/business-analyst/elicitation-techniques`
- `requirements-documentation` -> `pro/ba/business-analyst/requirements-documentation`
- `requirements-prioritization` -> `pro/ba/business-analyst/requirements-prioritization`
- `requirements-traceability` -> `pro/ba/business-analyst/requirements-traceability`
- `schedule-development` -> `pro/pm/project-manager/schedule-development`
- `scope-management` -> `pro/pm/project-manager/scope-management`

**Outputs:**
- Baselined requirements
- Acceptance-criteria matrix
- Schedule v1

**Decision gate:**
> Advance only when AC matrix complete and signed by sponsor.

### Stage 3: Deliver in waves

**Intent:** Wave-based delivery with mid-cycle validation gates.

**Tasks:**
- Run 2-3 week delivery waves
- Hold scrum/kanban ceremony cadence
- Earned-value review weekly

**Methodologies in chain:**
- `scrum-ceremonies` -> `pro/pm/pm-agile/scrum-ceremonies`
- `kanban-scaled-agile-ceremonies` -> `pro/pm/pm-agile/kanban-scaled-agile-ceremonies`
- `earned-value-management` -> `pro/pm/project-manager/earned-value-management`
- `quality-management` -> `pro/pm/project-manager/quality-management`
- `team-development` -> `pro/pm/project-manager/team-development`
- `requirements-validation` -> `pro/ba/business-analyst/requirements-validation`

**Outputs:**
- Wave deliverables
- EVM weekly report

**Decision gate:**
> Advance wave when AC pass + sponsor signs the wave note.

### Stage 4: Change control

**Intent:** Every scope change is priced; no quiet drift.

**Tasks:**
- Capture CR with impact analysis
- Price CR + adjust schedule
- Get written approval before exec

**Methodologies in chain:**
- `change-control` -> `pro/pm/project-manager/change-control`
- `solution-assessment` -> `pro/ba/business-analyst/solution-assessment`
- `stakeholder-engagement-advanced` -> `pro/pm/project-manager/stakeholder-engagement-advanced`

**Outputs:**
- CR log
- Updated SOW addenda

**Decision gate:**
> No work on unpriced CRs. No exceptions for 'small' changes.

### Stage 5: Acceptance + close

**Intent:** Final acceptance + closure pack + upsell signal.

**Tasks:**
- Run UAT against AC matrix
- Collect NPS + lessons-learned
- Book retainer or referral conversation

**Methodologies in chain:**
- `benefits-realization` -> `pro/pm/project-manager/benefits-realization`
- `lessons-learned` -> `pro/pm/project-manager/lessons-learned`
- `project-closure` -> `pro/pm/project-manager/project-closure`
- `ops-customer-success-metrics` -> `pro/marketing/gtm-strategist/ops-customer-success-metrics`
- `ops-upselling-cross-selling` -> `pro/marketing/gtm-strategist/ops-upselling-cross-selling`

**Outputs:**
- Acceptance certificate
- Closure pack
- Retainer/referral note

**Decision gate:**
> Required: signed acceptance + closure pack + booked follow-up. Otherwise project is not closed.

## Common pitfalls

- Letting scope drift via Slack without CRs - kills margin invisibly
- Skipping NPS because 'the client seemed happy' - kills referral motion
- Closing the project without booking the next conversation

## Quality checklist (self-review)

- Is every AC mapped to a delivered artifact?
- Did every scope change move through written CR?
- Did I leave the engagement with a planned follow-up?

## Related playbooks

- `quarter-end-retention-review`
- `quarterly-retainer-review-per-client`

## Known gaps

The following methodologies are referenced or implied by this playbook but do not yet exist in the knowledge base. They are tracked in the manifest `gaps[]` array and block publication until resolved (BLOCK policy).

- **agency-kickoff-deck-template** (tier `pro`, blocks stage 1) -- Kickoff stage needs a default kickoff deck template
- **agency-status-report-cadence** (tier `pro`, blocks stage 3) -- Deliver-in-waves stage needs a cadence + format spec for status reports
- **change-request-pricing-rubric** (tier `pro`, blocks stage 4) -- Change-control stage needs a written rubric for CR pricing
- **agency-uat-checklist** (tier `pro`, blocks stage 5) -- Acceptance stage needs a reusable UAT checklist

## CLI usage

```
faion get-content project-from-kickoff-to-client-signoff --format md       # human-readable rendering
faion get-content project-from-kickoff-to-client-signoff --format context  # agent-optimised context bundle
faion get-content project-from-kickoff-to-client-signoff --format json     # raw structured form
```
