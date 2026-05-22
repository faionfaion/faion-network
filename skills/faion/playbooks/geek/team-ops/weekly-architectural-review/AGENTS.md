---
slug: weekly-architectural-review
tier: geek
group: team-ops
persona: P6
goal: TBD
complexity: medium
version: 0.1.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion
summary: Risk of architectural drift → 45-min weekly review with explicit pattern-promotion + ADR queue + design-doc updates.
content_id: dc002af7e4870be2
methodology_refs:
  - mr-graph-vs-diff-reviewer
  - cloud-architecture
  - distributed-patterns
  - observability-architecture
  - quality-attributes-analysis
  - pattern-memory
  - mistake-memory
  - tech-debt-management
  - design-docs-patterns
  - architecture-decision-records
  - architecture-decision-records-sdd
---

# Weekly architectural review (45 min)

**Playbook slug:** `weekly-architectural-review`
**Tier:** geek
**Complexity:** medium
**Persona:** P6 — Product-Dev Team

## Intent

Risk of architectural drift → 45-min weekly review with explicit pattern-promotion + ADR queue + design-doc updates.

## Scope

Architect + 2-3 senior engineers walk the week's significant PRs and open RFCs. Goal: spot drift early (cross-service coupling, layering violations, missed reuse), promote good patterns to team `patterns.md`, queue ADRs for decisions worth memorialising. 45-minute hard stop. Output is a written set of queued ADRs + pattern-promotions + design-doc deltas.

### What this playbook covers

Three stages: rank PRs by architectural impact, walk the top of the list, queue ADRs. The 45-minute hard stop is the discipline. Drift accumulates when reviews drift into PR-level critique; this playbook explicitly stays at the architectural altitude (boundaries, layering, reuse, observability), with pattern + mistake memory carrying knowledge forward.

Attendance is small by design: architect + 2-3 senior engineers. Bigger rooms drift into debate; smaller rooms miss reuse opportunities. The graph-vs-diff reviewer is the load-bearing tool — diff-only reviews miss most architectural signal (a 3-line change can introduce a circular dependency across services). Always carry the caller/callee graph into the room.

Pattern promotions and ADR queue entries leave the room as commits or PRs, not as verbal agreements. If patterns.md doesn't change this week, the review either covered nothing significant — or it failed to capture what mattered. Both are worth investigating in the next biweekly retro.

### Non-goals

- PR-level review — see `pr-review-with-junior-mentoring`
- Cross-quarter strategy — see `quarter-planning-okr-reset`
- Incident postmortems — see `incident-postmortem-preventive-backlog`

### Prerequisites

- Graph-vs-diff reviewer tooling in place
- patterns.md + mistakes.md in repo
- ADR convention adopted by team

## Success criteria

The playbook is done when:
- Significant PRs walked with architectural lens
- Drift signals flagged with owner
- Pattern-promotions appended to patterns.md
- ADR queue updated
- design-docs-patterns updates queued where needed

## Stages

### Stage 1: Rank + walk

**Intent:** Rank the week's PRs by architectural impact; walk the top of the list.

**Methodologies in chain:**
- `mr-graph-vs-diff-reviewer` → `geek/sdlc-ai/mr-graph-vs-diff-reviewer`
- `cloud-architecture` → `pro/dev/software-architect/cloud-architecture`
- `distributed-patterns` → `pro/dev/software-architect/distributed-patterns`
- `observability-architecture` → `pro/dev/software-architect/observability-architecture`
- `quality-attributes-analysis` → `pro/dev/software-architect/quality-attributes-analysis`

**Decision gate:**
> Advance once the top 5-10 are walked. Don't extend the session to cover bottom-of-list items.

### Stage 2: Spot drift + promote patterns

**Intent:** Flag drift; promote what we want repeated; queue ADRs for decisions.

**Methodologies in chain:**
- `pattern-memory` → `solo/sdd/sdd/pattern-memory`
- `mistake-memory` → `solo/sdd/sdd/mistake-memory`
- `tech-debt-management` → `solo/dev/code-quality/tech-debt-management`
- `design-docs-patterns` → `solo/sdd/sdd/design-docs-patterns`

**Decision gate:**
> Advance when each drift signal has an owner. Unassigned drift evaporates by next review.

### Stage 3: Queue ADRs

**Intent:** Decisions worth memorialising land in the ADR queue.

**Methodologies in chain:**
- `architecture-decision-records` → `solo/dev/software-architect/architecture-decision-records`
- `architecture-decision-records-sdd` → `solo/sdd/sdd/architecture-decision-records`

**Decision gate:**
> Required output: queued ADRs with owners. Verbal agreement = drift in 2 weeks.

## Common pitfalls

- Review drifts into PR-level critique — wrong altitude
- Patterns promoted without writing them down — repeat next week
- ADRs noted in chat — lost by next sprint
- Session extends to 90 min — kills attendance

## Quality checklist (self-review)

- Did we update patterns.md or mistakes.md this week?
- Did we hold the 45-minute stop?
- Does every queued ADR have an owner?

## Related playbooks

- `pr-review-with-junior-mentoring`
- `rfc-to-production-feature-delivery`
- `biweekly-retro-mistake-memory`

## Known gaps

The following methodologies are referenced or implied by this playbook but do not yet exist in the knowledge base. They are tracked in the manifest `gaps[]` array and block publication until resolved (BLOCK policy).
- **architectural-impact-pr-ranking** (tier `geek`, blocks stage 1) — Rank stage needs a scoring rubric for architectural impact of PRs
- **weekly-arch-review-agenda-template** (tier `geek`, blocks stage 2) — Drift stage needs a written agenda template so the 45-min stop holds

## CLI usage

```
faion get-content weekly-architectural-review --format md       # human-readable rendering
faion get-content weekly-architectural-review --format context  # agent-optimised context bundle
faion get-content weekly-architectural-review --format json     # raw structured form
```
