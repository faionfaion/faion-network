# JIRA ticket scoping session with client PM

**Persona:** P4 Outsource Specialist · **Tier:** pro · **Complexity:** medium · **Angle:** atomic

## Why this playbook exists

30-90 min working session → turns vague 'we need this feature' into a ticket with INVEST user story, AC, dependencies, story-points placeholder, compliance/security owner tagged.

Atomic working session run by the offshore senior with the client PM. Output: a JIRA ticket meeting Definition of Ready — INVEST user story, acceptance criteria, dependencies, story-points placeholder, compliance/security owner tagged if applicable. Live shared-screen drafting, not async ping-pong.

Most outsource seniors improvise this flow — fine at one engagement, costly across five. This playbook fixes the chain: explicit stages, explicit decision-gates, written artifacts at every step, AI agents on a leash, no silent work absorption.

## How to run it

Walk the stages in order. Each stage has a decision-gate; do not advance until the gate condition is met in writing. A stranger should be able to read the artifacts and understand both *what* you did and *why* you advanced. Atomic stages are designed to be completed in a single sitting; deep stages span multiple sessions.

## Stage map

### Stage 1 — Frame

**Intent:** Surface the actual business need behind the feature ask.

**Tasks**
- Active-listening pass: client PM speaks first, you summarise
- Stakeholder-analysis: who benefits, who blocks
- Five-whys until the user-story role is real
- Pull existing requirements traceability if any

**Outputs**
- Written user-story candidate
- Stakeholder note

**Decision gate**

Advance only when user-story passes INVEST self-check.

### Stage 2 — Draft live

**Intent:** Co-edit the ticket on a shared screen; no async back-and-forth.

**Tasks**
- Use user-story-mapping to place the ticket in context
- Write AC: happy + 2 sad paths
- Document required vs nice-to-have inside the ticket
- Apply requirements-documentation patterns
- Apply requirements-prioritization

**Outputs**
- Draft ticket with AC + scope

**Decision gate**

Advance only when client PM agrees AC live, not after the call.

### Stage 3 — Tag dependencies + DoR

**Intent:** Make the ticket actionable without follow-up.

**Tasks**
- Tag dependencies with named owners
- Set story-points placeholder for poker
- Tag compliance/security owner if applicable
- Walk JIRA workflow status to 'Ready'
- Check Definition of Ready end-to-end

**Outputs**
- Ticket at status: Ready
- Dependencies + owners attached

**Decision gate**

Done when the ticket survives a 60-second Definition-of-Ready check.

## Common pitfalls

- Writing AC after the session — context evaporates inside 30 minutes
- Skipping the sad paths — every bug here costs a sprint
- Not tagging compliance owner — surprise audit follow-up later

## Quality checklist

- Did client PM agree AC live, on shared screen?
- Could a dev pick this up in a sprint without pinging anyone?
- Did I tag every regulatory owner the ticket touches?

## Related playbooks

- `adr-write-up-client-architecture`
- `story-points-estimation-poker`

## Gaps

These methodologies are referenced in the chain above but not yet materialised. They block promotion of this playbook from `draft` to `published`.

- `live-ticket-drafting-shared-screen-pattern` (blocks stage 2)
- `definition-of-ready-checklist-outsource` (blocks stage 3)
