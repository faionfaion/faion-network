# Quarter planning + OKR reset (end-to-end)

## Context

Quarter closes with retro + lessons learned, next-quarter OKRs published, top 3 feature bets sized + sequenced into roadmap, capacity confirmed per squad, and every role (PM, PdM, Architect, BA, Dev leads, DevOps, QA, Growth) knows what they own. Output is a roadmap doc, OKR sheet, RACI per bet, and a populated backlog under `backlog/`.

## Outcome

By the end of this playbook, the operator has run the 5 stages below and produced the written decision artefact in the final stage.

Success criteria:

- All 5 stages have written outputs in the project record
- Each stage's decision gate was answered before advancing (yes / no in writing)
- Final stage produced the required written decision artifact
- Every methodology reference loaded cleanly via `faion get-content`

## Steps

### 1. Close Last Quarter

Score what actually happened.

Tasks:
- Score every key result with evidence on a 0.0-1.0 scale
- Run a 60-min retro on what dragged outcomes
- Write a 1-page quarter close memo

Outputs:
- scored OKRs
- retro notes
- close memo

Decision gate: Advance only when the close memo is published to the team.

### 2. Pick Quarterly Outcomes

≤3 outcomes, not 10.

Tasks:
- Draft outcome candidates from strategy + retro signal
- Cut to 3 maximum; tie each to a business metric
- Pre-allocate capacity per outcome

Outputs:
- candidate list
- 3 chosen outcomes
- capacity allocation

Decision gate: Advance when 3 outcomes are signed off by leadership.

### 3. Define KRs

Each outcome gets 2-4 measurable KRs.

Tasks:
- Write 2-4 leading-indicator KRs per outcome
- Validate that every KR has a data source and an owner
- Stress-test KRs against ambition vs realism

Outputs:
- KR set
- owner + source per KR
- ambition-vs-realism notes

Decision gate: Advance only when every KR is measurable and owned.

### 4. Plan First 4 Weeks

Don't wait for week 5 to start moving.

Tasks:
- Translate each KR into the first 4 weeks of work
- Sequence dependencies; flag risks
- Set the weekly OKR check-in cadence

Outputs:
- 4-week plan per KR
- dependency + risk log
- weekly cadence on calendar

Decision gate: Advance when week-1 work is in the tracker.

### 5. Communicate

All-hands + per-team write-ups.

Tasks:
- Run the all-hands OKR kickoff
- Each team writes how their work maps to the OKRs
- Pin the OKR doc + dashboard in shared space

Outputs:
- all-hands deck
- team-mapping docs
- pinned OKR dashboard

Decision gate: Required output: every team has a written mapping to the OKRs.

## Decision points

- Stage 1 (Close Last Quarter): Advance only when the close memo is published to the team.
- Stage 2 (Pick Quarterly Outcomes): Advance when 3 outcomes are signed off by leadership.
- Stage 3 (Define KRs): Advance only when every KR is measurable and owned.
- Stage 4 (Plan First 4 Weeks): Advance when week-1 work is in the tracker.
- Stage 5 (Communicate): Required output: every team has a written mapping to the OKRs.

## References

- `ai-assisted-specification-writing`
- `tracker-linear-agent-as-assignee`
- `ba-planning`
- `requirements-traceability`
- `quality-attributes-analysis`
- `dora-metrics`
- `raci-matrix`
- `benefits-realization`
- `change-control`
- `cost-estimation`
- `lessons-learned`
- `project-closure`
- `resource-management`
- `risk-management`
- `risk-register`
- `scope-management`
- `wbs-creation`
- `communications-management`
- `stakeholder-engagement-advanced`
- `competitive-positioning`
- `continuous-discovery-habits`
- `methodologies-summary`
- `portfolio-strategy`
- `release-planning`
- `opportunity-solution-trees`

Gaps (status: draft until empty):
- `okr-cascade-template-product-dev-team` (see `gaps[]` in `playbook.yaml`)
- `ai-assisted-quarter-retro-synthesis` (see `gaps[]` in `playbook.yaml`)
