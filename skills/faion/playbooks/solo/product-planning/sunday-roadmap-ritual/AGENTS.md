---
slug: sunday-roadmap-ritual
tier: solo
group: product-planning
persona: P1
goal: operate-ritual
complexity: light
version: 0.1.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion
summary: Friday-clear backlog → Monday-morning task primed with prompt and acceptance.
content_id: 66d035a5a0adeec4
methodology_refs:
  - mistake-memory
  - pattern-memory
  - reflexion-learning
  - feature-prioritization-rice
  - feature-prioritization-moscow
  - backlog-management
  - outcome-based-roadmaps
  - writing-specifications
---

# Sunday roadmap and week-shaping ritual

**Playbook slug:** `sunday-roadmap-ritual`  
**Tier:** solo  
**Complexity:** light  
**Persona:** P1 — Solo SaaS Builder

## Intent

Friday-clear backlog → Monday-morning task primed with prompt and acceptance.

## Scope

Solo founder runs a 60-minute Sunday ritual: top 3 outcomes for the week chosen, single-tasked file/board updated, no-go items deferred, Monday-morning first task primed with prompt + acceptance. Exit artifact is a week-plan note + Monday task ready to start.

### What this playbook covers

This is a structured chain of existing faion methodologies adapted for a single-operator SaaS founder. It assumes no team, no SRE rotation, no co-founder. Every stage ends with an explicit decision gate so the operator can tell whether to advance, iterate, or kill — solo founders drift fastest where stages don't end cleanly.

### Non-goals

- Multi-week roadmap rewrite — that's quarterly
- Backlog grooming of >10 items — keep it tight

### Prerequisites

- Existing backlog file or board with current items
- Friday-closeout completed (week reflection done)

## Success criteria

The playbook is done when:
- Top 3 outcomes written with acceptance criteria
- Monday task primed with prompt + spec
- No-go items explicitly deferred (not abandoned)
- Ritual completed in ≤60 minutes

## Stages

### Stage 1: Review

**Intent:** What happened last week, what shifted in priorities.

**Tasks:**
- Read last week's outcomes vs actuals
- Update mistake-memory if relevant
- Pull new signals from inbox + analytics

**Methodologies in chain:**
- `mistake-memory` → `solo/sdd/sdd/mistake-memory`
- `pattern-memory` → `solo/sdd/sdd/pattern-memory`
- `reflexion-learning` → `solo/sdd/sdd/reflexion-learning`

**Outputs:**
- Last-week review notes

**Decision gate:**
> Advance when last week is closed. Don't start planning if last week isn't reflected on.

### Stage 2: Prioritise

**Intent:** Pick top 3 outcomes for the week using RICE or MoSCoW.

**Tasks:**
- List candidate outcomes
- Score against revenue-relevance filter
- Cut to 3

**Methodologies in chain:**
- `feature-prioritization-rice` → `solo/product/product-manager/feature-prioritization-rice`
- `feature-prioritization-moscow` → `solo/product/product-manager/feature-prioritization-moscow`
- `backlog-management` → `solo/product/product-operations/backlog-management`
- `outcome-based-roadmaps` → `solo/product/product-planning/outcome-based-roadmaps`

**Outputs:**
- Top 3 outcomes list

**Decision gate:**
> Advance when list is exactly 3. Refuse 4+ — single-operator constraint.

### Stage 3: Spec

**Intent:** Write acceptance criteria for the Monday task.

**Tasks:**
- Pick Monday's first task
- Write 1-paragraph spec + acceptance
- Prime AI prompt if applicable

**Methodologies in chain:**
- `writing-specifications` → `solo/sdd/sdd/writing-specifications`

**Outputs:**
- Monday spec.md
- AI prompt ready

**Decision gate:**
> Advance when Monday task is start-ready. No 'I'll figure it out Monday'.

## Common pitfalls

- Picking 5+ outcomes 'just in case' — guarantees at least 2 will slip
- Skipping review — repeats last week's mistakes

## Quality checklist (self-review)

- Could I finish all 3 outcomes if half the week disappeared?
- Is Monday's first task start-ready, or am I still thinking about it?

## Related playbooks

- `friday-bug-bash-triage`
- `solo-founder-operating-system`

## Known gaps

The following methodologies are referenced or implied by this playbook but do not yet exist in the knowledge base. They are tracked in the manifest `gaps[]` array and block publication until resolved (BLOCK policy).
- **solo-weekly-cadence-template** (tier `solo`, blocks stage 2) — Prioritise stage needs ready-to-fill weekly template
- **rice-for-one-person-cheatsheet** (tier `solo`, blocks stage 2) — Solo-scale RICE differs from team RICE — needs cheatsheet

## CLI usage

```
faion get-content sunday-roadmap-ritual --format md       # human-readable rendering
faion get-content sunday-roadmap-ritual --format context  # agent-optimised context bundle
faion get-content sunday-roadmap-ritual --format json     # raw structured form
```
