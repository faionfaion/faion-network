---
slug: weekly-architectural-review-v2
tier: geek
group: product-team
persona: p6-product-dev-team
goal: operate-ritual
complexity: medium
version: 1.0.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion-network
summary: "Architect + 2-3 senior engineers walk the week's significant PRs + open RFCs. Goal: spot drift early (cross-service coupling, layering violations, missed reuse), promote good patterns to team patte..."
content_id: 403ac907a7f07767
methodology_refs:
  - mr-graph-vs-diff-reviewer
  - cloud-architecture
  - distributed-patterns
  - observability-architecture
  - quality-attributes-analysis
  - tech-debt-management
  - architecture-decision-records
  - design-docs-patterns
  - mistake-memory
  - pattern-memory
---

# Weekly architectural review (45 min)

## Context

Architect + 2-3 senior engineers walk the week's significant PRs + open RFCs. Goal: spot drift early (cross-service coupling, layering violations, missed reuse), promote good patterns to team patterns.md, queue ADRs.

## Outcome

By the end of this playbook, the operator has run the 3 stages below and produced the written decision artefact in the final stage.

Success criteria:

- All 3 stages have written outputs in the project record
- Each stage's decision gate was answered before advancing (yes / no in writing)
- Final stage produced the required written decision artifact
- Every methodology reference loaded cleanly via `faion get-content`

## Steps

### 1. Triage Topics

Pick what's worth 45 minutes.

Tasks:
- Collect RFCs, ADRs, and tech-debt items needing decision
- Cut to ≤2 topics for the 45-minute slot
- Send the pre-read 24h in advance

Outputs:
- topic backlog
- agenda with ≤2 topics
- pre-read sent

Decision gate: Advance only when the agenda is locked and pre-read is delivered.

### 2. Run the Review

Time-boxed; outcomes not vibes.

Tasks:
- Each topic gets a presenter and a written proposal
- Discuss tradeoffs; reach a decision or schedule follow-up
- Capture the decision and the rationale on the spot

Outputs:
- per-topic decision
- rationale log
- follow-ups list

Decision gate: Advance when every topic has a written outcome.

### 3. Publish Decisions

Decisions belong in ADRs, not chat.

Tasks:
- Convert every decision into an ADR or RFC update
- Share with engineering at large
- Schedule any implementation kickoffs

Outputs:
- ADR updates
- share log
- implementation kickoffs

Decision gate: Required output: every decision lives in an ADR or RFC.

## Decision points

- Stage 1 (Triage Topics): Advance only when the agenda is locked and pre-read is delivered.
- Stage 2 (Run the Review): Advance when every topic has a written outcome.
- Stage 3 (Publish Decisions): Required output: every decision lives in an ADR or RFC.

## References

- `mr-graph-vs-diff-reviewer`
- `cloud-architecture`
- `distributed-patterns`
- `observability-architecture`
- `quality-attributes-analysis`
- `tech-debt-management`
- `architecture-decision-records`
- `design-docs-patterns`
- `mistake-memory`
- `pattern-memory`

Gaps (status: draft until empty):
- `architectural-impact-pr-ranking` (see `gaps[]` in `playbook.yaml`)
- `weekly-arch-review-agenda-template` (see `gaps[]` in `playbook.yaml`)
