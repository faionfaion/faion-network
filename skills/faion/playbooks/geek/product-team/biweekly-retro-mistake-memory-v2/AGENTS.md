---
slug: biweekly-retro-mistake-memory-v2
tier: geek
group: product-team
persona: p6-product-dev-team
goal: operate-ritual
complexity: light
version: 1.0.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion-network
summary: "Team runs a 45-min retro at sprint close. Inputs are not opinions only — also: AI-aggregated mistake-memory entries since last retro, alert volume, on-call load, PR-cycle time. Outputs are 2-3 conc..."
content_id: d051fcac2f109f18
methodology_refs:
  - dora-metrics
  - scrum-ceremonies
  - team-development
  - value-stream-management
  - mistake-memory
  - quality-gates-confidence
  - reflexion-learning
---

# Bi-weekly retro with mistake-memory feedback

## Context

Team runs a 45-min retro at sprint close. Inputs are not opinions only — also: AI-aggregated mistake-memory entries since last retro, alert volume, on-call load, PR-cycle time. Outputs are 2-3 concrete experiments for the next sprint, each with an owner.

## Outcome

By the end of this playbook, the operator has run the 3 stages below and produced the written decision artefact in the final stage.

Success criteria:

- All 3 stages have written outputs in the project record
- Each stage's decision gate was answered before advancing (yes / no in writing)
- Final stage produced the required written decision artifact
- Every methodology reference loaded cleanly via `faion get-content`

## Steps

### 1. Collect Signal

Make the bad signal visible.

Tasks:
- Pull mistake-memory entries since last retro
- Pull incident postmortems and missed AC
- Pull anonymous team-feedback entries

Outputs:
- mistake-memory digest
- postmortem digest
- feedback digest

Decision gate: Advance only when all three sources are gathered.

### 2. Run the Retro

Honest > polite, but always blameless.

Tasks:
- Walk through what worked, what didn't, surprises
- Pick top-3 patterns to act on next 2 weeks
- Assign owners for each pattern

Outputs:
- what-worked / what-didn't / surprises notes
- top-3 patterns
- pattern owners

Decision gate: Advance when each pattern has an owner and a measurable signal.

### 3. Update the System, Not Just the Doc

Memory is only useful if it changes behaviour.

Tasks:
- Update SOPs, checklists, or tooling per the patterns
- Add or modify ruff/ESLint rules where pattern is mechanical
- Communicate the changes to the team

Outputs:
- updated docs/checklists/tools
- rule diffs
- team comms

Decision gate: Required output: at least one written behaviour change deployed.

## Decision points

- Stage 1 (Collect Signal): Advance only when all three sources are gathered.
- Stage 2 (Run the Retro): Advance when each pattern has an owner and a measurable signal.
- Stage 3 (Update the System, Not Just the Doc): Required output: at least one written behaviour change deployed.

## References

- `dora-metrics`
- `scrum-ceremonies`
- `team-development`
- `value-stream-management`
- `mistake-memory`
- `quality-gates-confidence`
- `reflexion-learning`

Gaps (status: draft until empty):
- `retro-action-success-criteria-template` (see `gaps[]` in `playbook.yaml`)
- `anti-theater-retro-guardrails` (see `gaps[]` in `playbook.yaml`)
