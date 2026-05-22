---
slug: fixed-price-vs-tm-estimation-with-ai-risk-buffer
tier: pro
group: outsource
persona: P4
goal: govern-decide
complexity: medium
version: 1.0.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion-network
summary: "Fixed-Price vs T&M Estimation with AI Risk Buffer — Given a discovery brief, produce two defensible quotes (fixed-price and T&M) with an explicit AI-leverage adjustment and a regulatory-uncertainty..."
content_id: ecf8e368e10e97f2
methodology_refs:
  - cost-estimation
  - change-control
  - risk-management
  - scope-management
  - work-breakdown-structure
---

# Fixed-Price vs T&M Estimation with AI Risk Buffer

## Context

This playbook covers the synthesis flow for the persona `p4-outsource-specialist`. It applies whenever the trigger described in the scope below appears in the operator's workflow. The output is a written, auditable artefact pack, not a verbal hand-wave.

## Outcome

Given a discovery brief, produce two defensible quotes (fixed-price and T&M) with an explicit AI-leverage adjustment and a regulatory-uncertainty buffer. 'Done' = client receives both options, internal margin model is documented, and post-mortem can replay assumptions.

## Steps

### 1. Scope

Define the scope, exit criteria, and the people who must agree on success.

Tasks:
- Restate the scope outcome for this engagement in one sentence.
- Identify who owns the scope output and who must approve it.
- Produce the scope artefact in the agreed format.

Methodologies:
- `pro/pm/pm-traditional/cost-estimation`

Decision gate: Advance to the next stage when the scope artefact is approved by the named owner; iterate if any blocker remains.

### 2. Discovery

Gather evidence about the current state, stakeholders, constraints, and prior data.

Tasks:
- Restate the discovery outcome for this engagement in one sentence.
- Identify who owns the discovery output and who must approve it.
- Produce the discovery artefact in the agreed format.

Methodologies:
- `pro/pm/project-manager/change-control`

Decision gate: Advance to the next stage when the discovery artefact is approved by the named owner; iterate if any blocker remains.

### 3. Plan

Turn discovery output into a written plan with owners, sequence, and risk reserves.

Tasks:
- Restate the plan outcome for this engagement in one sentence.
- Identify who owns the plan output and who must approve it.
- Produce the plan artefact in the agreed format.

Methodologies:
- `pro/pm/project-manager/cost-estimation`

Decision gate: Advance to the next stage when the plan artefact is approved by the named owner; iterate if any blocker remains.

### 4. Execute

Run the plan in order of dependency; ship each output before moving on.

Tasks:
- Restate the execute outcome for this engagement in one sentence.
- Identify who owns the execute output and who must approve it.
- Produce the execute artefact in the agreed format.

Methodologies:
- `pro/pm/project-manager/risk-management`

Decision gate: Advance to the next stage when the execute artefact is approved by the named owner; iterate if any blocker remains.

### 5. Verify

Check the work against the exit criteria with the people who signed off in Scope.

Tasks:
- Restate the verify outcome for this engagement in one sentence.
- Identify who owns the verify output and who must approve it.
- Produce the verify artefact in the agreed format.

Methodologies:
- `pro/pm/project-manager/scope-management`

Decision gate: Advance to the next stage when the verify artefact is approved by the named owner; iterate if any blocker remains.

### 6. Communicate

Tell every stakeholder what changed, what's next, and what they own.

Tasks:
- Restate the communicate outcome for this engagement in one sentence.
- Identify who owns the communicate output and who must approve it.
- Produce the communicate artefact in the agreed format.

Methodologies:
- `pro/pm/project-manager/work-breakdown-structure`

Decision gate: Advance to the next stage when the communicate artefact is approved by the named owner; iterate if any blocker remains.

## Decision points

- Each stage has a written decision gate; do not advance unless the gate's owner has signed off in the artefact log.
- If a stage gate fails twice, escalate to the playbook's named maintainer before retrying.

## References

- `pro/pm/pm-traditional/cost-estimation` — methodology cited inside the stages above.
- `pro/pm/project-manager/change-control` — methodology cited inside the stages above.
- `pro/pm/project-manager/cost-estimation` — methodology cited inside the stages above.
- `pro/pm/project-manager/risk-management` — methodology cited inside the stages above.
- `pro/pm/project-manager/scope-management` — methodology cited inside the stages above.
- `pro/pm/project-manager/work-breakdown-structure` — methodology cited inside the stages above.
