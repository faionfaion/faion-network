# Subcontractor task brief generation

**Playbook slug:** `subcontractor-task-brief-generation`
**Tier:** pro
**Complexity:** light
**Persona:** P5 -- Micro-agency founder

## Intent

New task to self-contained contractor brief with context, definition of done, deliverable format, escalation path.

## Scope

Founder produces a self-contained brief for each new task handed to a contractor. Output: brief with context, definition of done, deliverable format, escalation path. Exit artifact: brief pinned in shared workspace + accepted by contractor in writing.

### What this playbook covers

This is a structured chain of existing faion methodologies adapted for a 2-3 person agency founder who is also the senior delivery operator. It assumes 1-3 contractors handle the rest. Every stage ends with an explicit decision gate so the operator can tell whether to advance, iterate, or kill -- agency founders drift fastest when client comfort overrides honest staging. Each chained methodology lives in the knowledge base and can be read via `faion get-content <methodology-slug>`. The chain order is intentional: skipping a stage typically surfaces as a billing, retention, or contractor problem two months later.

### Non-goals

- Full project plan - task-level brief only
- Long-form spec - concise, structured brief

### Prerequisites

- Contractor signed + onboarded
- Brief template pinned in shared workspace

## Success criteria

The playbook is done when:
- Brief includes context, AC, deliverable format, escalation
- Contractor accepts brief in writing
- Definition of done explicit (verifiable)
- Brief fits one screen

## Stages

### Stage 1: Frame context

**Intent:** Why now, where it fits, what the client cares about.

**Tasks:**
- Write 3-line context
- Link parent project + sponsor
- Flag any constraints (budget, brand, legal)

**Methodologies in chain:**
- `ops-contractor-basics` -> `pro/marketing/gtm-strategist/ops-contractor-basics`
- `ops-contractor-management` -> `pro/marketing/gtm-strategist/ops-contractor-management`

**Outputs:**
- Context block

**Decision gate:**
> Advance once context fits 3 lines without losing meaning.

### Stage 2: Definition of done

**Intent:** Verifiable acceptance criteria.

**Tasks:**
- Write 3-7 acceptance criteria
- Specify deliverable format + location
- Specify review cadence

**Methodologies in chain:**
- `acceptance-criteria` -> `pro/ba/business-analyst/acceptance-criteria`
- `requirements-documentation` -> `pro/ba/business-analyst/requirements-documentation`

**Outputs:**
- AC list
- Deliverable format spec

**Decision gate:**
> Advance only if AC are testable by someone else.

### Stage 3: RACI + escalation

**Intent:** Owner + decision rights + when to escalate.

**Tasks:**
- Tag responsible + accountable
- Define decision authority
- Set escalation trigger

**Methodologies in chain:**
- `raci-matrix` -> `pro/pm/project-manager/raci-matrix`
- `team-development` -> `pro/pm/project-manager/team-development`

**Outputs:**
- RACI line
- Escalation path

**Decision gate:**
> Advance with named owner + escalation written.

### Stage 4: Hand over + log

**Intent:** Contractor accepts in writing; brief logged.

**Tasks:**
- Share brief in agreed channel
- Ask contractor to confirm in writing
- Log brief in task tracker

**Methodologies in chain:**
- `feedback` -> `solo/comms/communicator/feedback`

**Outputs:**
- Acceptance comment
- Logged brief

**Decision gate:**
> Required: written acceptance before work begins.

## Common pitfalls

- Briefing via Slack DM with no AC - rework guaranteed
- Skipping escalation rules - contractor sits on blockers
- Letting briefs balloon past one screen - nobody reads it

## Quality checklist (self-review)

- Could a different contractor execute this brief without me?
- Are AC testable by someone else?
- Did I get a written acceptance?

## Related playbooks

- `daily-contractor-standup`
- `hire-and-onboard-a-new-contractor`

## Known gaps

The following methodologies are referenced or implied by this playbook but do not yet exist in the knowledge base. They are tracked in the manifest `gaps[]` array and block publication until resolved (BLOCK policy).

- **contractor-brief-template-self-contained** (tier `pro`, blocks stage 1) -- Frame-context stage needs a self-contained brief template
- **definition-of-done-library** (tier `pro`, blocks stage 2) -- Definition-of-done stage needs a reusable AC library by deliverable type

## CLI usage

```
faion get-content subcontractor-task-brief-generation --format md       # human-readable rendering
faion get-content subcontractor-task-brief-generation --format context  # agent-optimised context bundle
faion get-content subcontractor-task-brief-generation --format json     # raw structured form
```
