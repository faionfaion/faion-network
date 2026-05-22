---
slug: jira-ticket-scoping-session-with-client-pm
tier: pro
group: outsource
persona: P4
goal: TBD
complexity: medium
version: 1.0.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion-network
summary: "JIRA ticket scoping session with client PM — Atomic 30-90 min working session where the offshore senior turns a vague 'we need this feature' line into a ticket with INVEST user story, AC, dependenc..."
content_id: 138dd090d2243add
methodology_refs:
  - elicitation-techniques
  - stakeholder-analysis
  - acceptance-criteria
  - user-story-mapping
  - jira-workflow-management
  - requirements-documentation
  - requirements-prioritization
  - requirements-traceability
---

# JIRA ticket scoping session with client PM

## Context

This playbook covers the atomic flow for the persona `p4-outsource-specialist`. It applies whenever the trigger described in the scope below appears in the operator's workflow. The output is a written, auditable artefact pack, not a verbal hand-wave.

## Outcome

Atomic 30-90 min working session where the offshore senior turns a vague 'we need this feature' line into a ticket with INVEST user story, AC, dependencies, story-points placeholder, and a tagged compliance/security owner if applicable.

## Steps

### 1. Scope

Define the scope, exit criteria, and the people who must agree on success.

Tasks:
- Restate the scope outcome for this engagement in one sentence.
- Identify who owns the scope output and who must approve it.
- Produce the scope artefact in the agreed format.

Methodologies:
- `pro/ba/ba-core/elicitation-techniques`
- `pro/ba/business-analyst/stakeholder-analysis`

Decision gate: Advance to the next stage when the scope artefact is approved by the named owner; iterate if any blocker remains.

### 2. Discovery

Gather evidence about the current state, stakeholders, constraints, and prior data.

Tasks:
- Restate the discovery outcome for this engagement in one sentence.
- Identify who owns the discovery output and who must approve it.
- Produce the discovery artefact in the agreed format.

Methodologies:
- `pro/ba/business-analyst/acceptance-criteria`
- `pro/ba/business-analyst/user-story-mapping`

Decision gate: Advance to the next stage when the discovery artefact is approved by the named owner; iterate if any blocker remains.

### 3. Plan

Turn discovery output into a written plan with owners, sequence, and risk reserves.

Tasks:
- Restate the plan outcome for this engagement in one sentence.
- Identify who owns the plan output and who must approve it.
- Produce the plan artefact in the agreed format.

Methodologies:
- `pro/ba/business-analyst/elicitation-techniques`
- `pro/pm/pm-agile/jira-workflow-management`

Decision gate: Advance to the next stage when the plan artefact is approved by the named owner; iterate if any blocker remains.

### 4. Execute

Run the plan in order of dependency; ship each output before moving on.

Tasks:
- Restate the execute outcome for this engagement in one sentence.
- Identify who owns the execute output and who must approve it.
- Produce the execute artefact in the agreed format.

Methodologies:
- `pro/ba/business-analyst/requirements-documentation`

Decision gate: Advance to the next stage when the execute artefact is approved by the named owner; iterate if any blocker remains.

### 5. Verify

Check the work against the exit criteria with the people who signed off in Scope.

Tasks:
- Restate the verify outcome for this engagement in one sentence.
- Identify who owns the verify output and who must approve it.
- Produce the verify artefact in the agreed format.

Methodologies:
- `pro/ba/business-analyst/requirements-prioritization`

Decision gate: Advance to the next stage when the verify artefact is approved by the named owner; iterate if any blocker remains.

### 6. Communicate

Tell every stakeholder what changed, what's next, and what they own.

Tasks:
- Restate the communicate outcome for this engagement in one sentence.
- Identify who owns the communicate output and who must approve it.
- Produce the communicate artefact in the agreed format.

Methodologies:
- `pro/ba/business-analyst/requirements-traceability`

Decision gate: Advance to the next stage when the communicate artefact is approved by the named owner; iterate if any blocker remains.

## Decision points

- Each stage has a written decision gate; do not advance unless the gate's owner has signed off in the artefact log.
- If a stage gate fails twice, escalate to the playbook's named maintainer before retrying.

## References

- `pro/ba/ba-core/elicitation-techniques` — methodology cited inside the stages above.
- `pro/ba/business-analyst/acceptance-criteria` — methodology cited inside the stages above.
- `pro/ba/business-analyst/elicitation-techniques` — methodology cited inside the stages above.
- `pro/ba/business-analyst/requirements-documentation` — methodology cited inside the stages above.
- `pro/ba/business-analyst/requirements-prioritization` — methodology cited inside the stages above.
- `pro/ba/business-analyst/requirements-traceability` — methodology cited inside the stages above.
