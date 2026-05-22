---
slug: adopt-faion-org-wide-overrides-v2
tier: geek
group: product-team
persona: p6-product-dev-team
goal: migrate-rebuild
complexity: deep
version: 1.0.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion-network
summary: All 2-10 devs reference the same playbook set; company-specific overlays (security policy, ADR template, RFC format, internal tech-radar) cleanly shadow faion defaults without forking the corpus
content_id: ac470b6ba488fa50
methodology_refs:
  - kb-agents-md-context-pyramid
  - kb-versioned-agent-memory-files
  - onboarding-30-day
  - team-development
  - design-doc-structure
  - architecture-decision-records
---

# Adopt faion org-wide and override with company patterns

## Context

All 2-10 devs reference the same playbook set; company-specific overlays (security policy, ADR template, RFC format, internal tech-radar) cleanly shadow faion defaults without forking the corpus

## Outcome

By the end of this playbook, the operator has run the 4 stages below and produced the written decision artefact in the final stage.

Success criteria:

- All 4 stages have written outputs in the project record
- Each stage's decision gate was answered before advancing (yes / no in writing)
- Final stage produced the required written decision artifact
- Every methodology reference loaded cleanly via `faion get-content`

## Steps

### 1. Pilot the Adoption

One squad before everyone.

Tasks:
- Pick a single squad to pilot Faion across SDD + playbooks
- Install Faion plugin + CLI in their workflows
- Pick the 3 workflows where Faion will be measured

Outputs:
- pilot squad confirmed
- Faion install verified
- 3 pilot workflows

Decision gate: Advance only when the pilot squad is using Faion daily for 1 week.

### 2. Define Company Overrides

Where company standards diverge from Faion defaults.

Tasks:
- List company conventions that override Faion (linters, formats, naming)
- Encode them as company-local skills / playbooks layered on top of Faion
- Document the override registry

Outputs:
- override list
- company overlay skills
- override registry

Decision gate: Advance when overrides are encoded and not just described.

### 3. Roll Out Org-Wide

Sequence by squad; no big-bang.

Tasks:
- Roll out squad-by-squad with the same install runbook
- Train each squad on the override registry
- Surface adoption metrics weekly

Outputs:
- per-squad rollout log
- training records
- weekly adoption metrics

Decision gate: Advance only when ≥80% of squads are on the same install + overrides.

### 4. Measure & Iterate

Adoption without value is theatre.

Tasks:
- Measure cycle-time, escape-rate, and dev-satisfaction deltas
- Iterate overrides where Faion default + company default conflict
- Decide: deepen / hold / unwind

Outputs:
- delta metrics
- override iterations
- deepen/hold/unwind memo

Decision gate: Required output: a written go-forward decision with data.

## Decision points

- Stage 1 (Pilot the Adoption): Advance only when the pilot squad is using Faion daily for 1 week.
- Stage 2 (Define Company Overrides): Advance when overrides are encoded and not just described.
- Stage 3 (Roll Out Org-Wide): Advance only when ≥80% of squads are on the same install + overrides.
- Stage 4 (Measure & Iterate): Required output: a written go-forward decision with data.

## References

- `kb-agents-md-context-pyramid`
- `kb-versioned-agent-memory-files`
- `onboarding-30-day`
- `team-development`
- `design-doc-structure`
- `architecture-decision-records`

Gaps (status: draft until empty):
- `team-methodology-overlay-mechanism` (see `gaps[]` in `playbook.yaml`)
- `company-prompt-library-pattern` (see `gaps[]` in `playbook.yaml`)
- `team-charter-working-agreement` (see `gaps[]` in `playbook.yaml`)
- `role-cheatsheet-generator` (see `gaps[]` in `playbook.yaml`)
