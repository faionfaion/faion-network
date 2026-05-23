# Trello Kanban

## Summary

**One-sentence:** Visual kanban on Trello with 5-7 WIP-encoded lists, 8-12 closed-list labels, custom-field story points, Butler-rule automation documented in constitution.md, and cached IDs + rate-limited REST API for agent writes.

**One-paragraph:** Trello is the lowest-friction visual kanban for a 1-5 person solo or near-solo team. Cognitive load stays manageable when lists are ≤7 (Backlog → Ready → In Dev (WIP:3) → Review (WIP:2) → QA → Done), labels are ≤12 in a fixed type/priority/modifier taxonomy, and Butler rules handle mechanical transitions. Agents must cache board/list/label IDs (Trello writes need IDs, not names), respect the 100 req / 10s rate limit, and remember Butler triggers fire on UI events only — not on API-driven moves.

**Ефективно для:**

- Solo or 1-5 person team needing a low-friction visual board.
- Non-technical stakeholders updating cards without training.
- Pre-MVP prototyping where flexibility beats structure.
- Agents automating card moves while respecting rate-limits and Butler boundaries.

## Applies If (ALL must hold)

- Team of 1-5 people needing a visual board with minimal setup overhead.
- Stakeholders are non-technical and need to update the board without training.
- Rapid prototyping or pre-MVP phases where flexibility beats structure.
- Budget constraints: Trello Free covers up to ~10 boards (1 Power-Up per board).
- No cross-repository code traceability needed.

## Skip If (ANY kills it)

- Team is already on GitHub — GitHub Projects has native code integration.
- Complex dependency tracking needed — Trello has no native dependency visualisation.
- OKR or goal tracking required — Trello has no goals layer; use ClickUp or Linear.
- Velocity metrics or burndown charts needed regularly — requires premium Power-Ups.
- More than ~10 boards under Free plan.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Trello board + API key + token | env vars | platform |
| List ID map (Backlog, In Dev, Review, QA, Done) | YAML / constitution.md | PM |
| Label taxonomy (≤12 closed list) | YAML | PM |
| Custom-fields Power-Up enabled (story points, sprint, component) | board config | PM |
| Butler rules documented in constitution.md | markdown | PM |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[notion-pm]] | Alternative tool — decision-tree compares them. |
| [[reporting-dashboards]] | Trello query patterns inform fetch step. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 rules: ≤7 lists with WIP, ≤12 labels, custom fields not titles, archive don't delete, cached IDs, rate-limit 100/10s | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 for board config artefact + valid/invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: id-by-name on every write, Butler-fires-on-API-move assumption, label bloat, data in card titles | ~700 |
| `content/04-procedure.xml` | essential | 5-step procedure: lists+WIP → labels → custom fields → Butler → API integration | ~800 |
| `content/06-decision-tree.xml` | essential | Routing tree → rule from 01-core-rules.xml | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `board_scaffold` | sonnet | List + label layout decision. |
| `api_integration` | sonnet | Cache IDs + rate-limit handling. |
| `butler_documentation` | haiku | Mechanical translation of Butler rules to constitution.md. |

## Templates

| File | Purpose |
|------|---------|
| `templates/card-feature.md` | Feature card description template |
| `templates/card-bug.md` | Bug card description template |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-trello-kanban.py` | Validate board config artefact against 02-output-contract schema | Pre-publish gate |

## Related

- [[notion-pm]]
- [[reporting-dashboards]]
- [[status-report-templates-by-audience]]

## Decision tree

See `content/06-decision-tree.xml`. The tree routes by team size, code-traceability need, list count, label count, ID caching, and rate-limit observance onto a rule from `content/01-core-rules.xml`.
