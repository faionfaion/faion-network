# 1On1 Template Managers

## Summary

**One-sentence:** Produces a manager 1:1 template (agenda + carry-forward + growth check-in + action items) with named owner + last_reviewed so 1:1s become reviewable artefacts.

**One-paragraph:** Produces a manager 1:1 template (agenda + carry-forward + growth check-in + action items) with named owner + last_reviewed so 1:1s become reviewable artefacts. The methodology is anchored to a single named consumer (a PM, EM, portfolio owner, or downstream agent) and a fixed-shape artefact that downstream review can sign off without re-deriving reasoning. Inputs are explicit, evidence is anchored, and the artefact carries `version`, `owner`, and `last_reviewed` so it remains a living operating tool rather than folklore. Outputs that fail the contract are rejected at validation time, not at executive review.

**Ефективно для:** EM/PM-у — щоб 1:1 з кожним інженером був документований, з actions і next-review, а не 'просто розмова'.

## Applies If (ALL must hold)

- Manager owns ≥3 direct reports.
- 1:1 cadence is in place (weekly / biweekly).
- Manager has a private notes space (Notion / Obsidian / Logseq / shared HR).
- At least one direct report has flagged 'growth path unclear'.

## Skip If (ANY kills it)

- Manager owns < 3 direct reports — single-page memo is cheaper.
- Org mandates a different 1:1 template — comply.
- Reports refuse documented 1:1s — respect; do not impose.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Notes space | Notion / Obsidian / Logseq | manager |
| 1:1 calendar slots | calendar | manager + reports |
| Prior 1:1 notes (if any) | files | manager |
| Growth-plan reference | ladder doc | engineering-ladder-and-growth-plan output |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/pm/engineering-ladder-and-growth-plan` | Growth-plan reference the 1:1 attaches to. |
| `geek/pm/project-manager/cross-role-handoff-protocol` | Handoff vocabulary the 1:1 uses. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules every application enforces | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples + self-check | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns with symptom / root-cause / fix | ~900 |
| `content/06-decision-tree.xml` | essential | Root question → branches → conclusions (rule refs) | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-1on1-page` | haiku | Template fill from attendee + last 1:1 notes. |
| `carry-forward-extract` | sonnet | Bounded judgement: which prior actions remain open. |
| `growth-narrative` | opus | Per-engineer narrative across cycles. |

## Templates

| File | Purpose |
|------|---------|
| `templates/skeleton.md` | 1:1 Markdown skeleton: header (date, attendee, last_reviewed) + agenda + carry-forward + growth + actions + next-review. |
| `templates/header.yaml` | Frontmatter contract: owner, version, last_reviewed for the produced artefact. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-1on1-template-managers.py` | Validate produced artefact against the JSON Schema in `02-output-contract.xml`. | Pre-merge and on every artefact refresh. |

## Related

- [[engineering-ladder-and-growth-plan]]
- [[cross-role-handoff-protocol]]
- [[exception-driven-standup-protocol]]

## Decision tree

The mandatory decision tree at `content/06-decision-tree.xml` Decides whether to adopt the template (≥3 reports + cadence + notes space), block (no notes space), or skip (≤2 reports). Run before the first 1:1 of the new cycle.
