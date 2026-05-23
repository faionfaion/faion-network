---
slug: lessons-learned
tier: pro
group: pm
domain: pm
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Continuous capture, structured categorisation, and mandatory retrieval of project knowledge so the same mistakes are not repeated; produces a searchable lesson database.
content_id: "28455eb0a8d4949e"
complexity: medium
produces: report
est_tokens: 4900
tags: [lessons-learned, retrospectives, knowledge-management, organizational-learning, continuous-improvement]
---
# Lessons Learned

## Summary

**One-sentence:** Continuous capture, structured categorisation, and mandatory retrieval of project knowledge so the same mistakes are not repeated; produces a searchable lesson database.

**One-paragraph:** Continuous capture, structured categorisation, and mandatory retrieval of project knowledge so the same mistakes are not repeated; produces a searchable lesson database. The methodology applies in pm-traditional contexts where the preconditions in `Applies If` hold and none of the `Skip If` triggers fire. Decision routing lives in `content/06-decision-tree.xml`; testable rules with rationale live in `content/01-core-rules.xml`; the validator at `scripts/validate-lessons-learned.py` enforces the output contract.

**Ефективно для:**

- Programs delivering >3 phases or releases per year.
- Org with project portfolio across multiple PMs.
- Recurring vendor relationships where pattern recognition matters.
- Compliance regimes requiring documented learning loops.

## Applies If (ALL must hold)

- A lesson repository exists (Notion / Confluence / Markdown repo).
- Lessons can be tagged with category (process, technical, vendor, comms, risk).
- Retrieval is mandatory at planning + at risk identification on new work.

## Skip If (ANY kills it)

- Single-project team with no future projects.
- Lessons captured but never read — fix retrieval first.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Lesson repository | Markdown/Notion | PMO |
| Category taxonomy | list of tags | PMO |
| Retrieval triggers | list (planning, risk-id, retro) | PM |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[scrum-ceremonies]] | retro is the source of agile-side lessons |
| [[project-closure]] | closure is the source of waterfall lessons |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules (incl. skip rule) with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid/forbidden examples | 900 |
| `content/03-failure-modes.xml` | essential | Antipatterns with symptom/root-cause/fix triplets | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input/action/output/decision-gate | 800 |
| `content/05-examples.xml` | optional | End-to-end worked example | 700 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-lesson` | sonnet | Judgement: extract reusable lesson vs project-specific note. |
| `validate-lesson` | haiku | Mechanical schema check. |
| `retrieve-for-planning` | haiku | Tag-based query into repository. |

## Templates

| File | Purpose |
|------|---------|
| `templates/lesson-validator.py` | Validator script: required fields, category in taxonomy, retrievability check |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-lessons-learned.py` | Validate the report artefact against the schema in `02-output-contract.xml` | CI on each artefact change; pre-commit |

## Related

- [[scrum-ceremonies]]
- [[project-closure]]
- [[communications-management]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (preconditions, baseline presence, threshold pass/fail) to a concrete action; each leaf references a rule from `01-core-rules.xml`. Use it when in doubt about whether or how to apply this methodology to the case at hand.

