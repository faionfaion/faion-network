# Pair Programming

## Summary

**One-sentence:** Plans a pair session: picks style (driver-navigator / ping-pong / strong-style), sets 15-30 min role swap, defines agent's optional third role.

**One-paragraph:** Two developers sharing a workstation accelerate knowledge transfer and reduce bus-factor — but only with discipline: role swap interval, named style, single shared workstation (or shared cursor). This methodology emits a session plan: style choice, swap interval, agent role (test-writer / hint-provider / silent), retrospective metric (commit hygiene, defects-found). Output is the plan and post-session report.

**Ефективно для:**

- Onboarding: новачок як navigator, senior як driver — pace матерію за дні замість тижнів.
- Tricky algorithm / debug: дві голови ловлять помилки, які одна пропускає.
- Ping-pong TDD: один пише тест, інший — реалізацію — деталі балансом.
- Solo + agent: people-cost мінімальний; агент як silent navigator з пропозиціями.

## Applies If (ALL must hold)

- Two engineers available for ≥60 min focused work.
- Topic merits more than one viewpoint (debug / design / TDD).
- Workstation supports shared editing (Live Share / Tuple / shared screen).

## Skip If (ANY kills it)

- Pure clerical task (bumping deps).
- Async teams — pair needs synchronous time.
- One participant is mentally checked-out — pair without engagement is wasted.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Topic | Markdown | session brief |
| Both participants | list of 2 | calendar |
| Style choice | enum | decision tree below |
| Agent role (optional) | enum | session policy |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| none | Standalone — no upstream artefacts required. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: swap-interval, named-style, shared-workstation, agent-silent-by-default, retro-required | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema for session plan + retro | 700 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns: silent-passenger, agent-spam, no-retro | 600 |
| `content/04-procedure.xml` | essential | 5-step pair-session procedure | 700 |
| `content/06-decision-tree.xml` | essential | Topic + style routing tree | 400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `plan_session` | haiku | Template-fill; deterministic. |
| `agent_during_session` | sonnet | Silent-by-default; reactive only. |
| `draft_retro` | sonnet | Synthesises metrics + lessons. |

## Templates

| File | Purpose |
|------|---------|
| `templates/pingpong-prompt.txt` | Agent prompt for ping-pong TDD style |
| `templates/strong-style-prompt.txt` | Agent prompt for strong-style enforcement |
| `templates/pair-journal.sh` | Shell that logs swap timestamps + commit moments |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-pair-programming.py` | Validate session plan + retro | Before session start; after end |

## Related

- - [[mob-programming]] — 3-4 person variant of the same family.
- - [[code-review]] — pair-produced PR still goes through review.

## Decision tree

See `content/06-decision-tree.xml`. Branches on topic shape: TDD-shaped → ping-pong; debug-shaped → driver-navigator; teaching-shaped → strong-style. Leaves reference rules from 01-core-rules.xml.
