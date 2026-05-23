---
slug: blurred-roles-team-evolution
tier: pro
group: product
domain: pm
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Diagnoses a product team's role overlap (PM/eng/design/data/AI) as a Venn diagram with ownership gaps and duplications; output is a team-evolution report with hire/restructure recommendations.
content_id: "1d8b4083f2347f46"
complexity: medium
produces: report
est_tokens: 5400
tags: [pm, pro, report, team, roles, scale-up]
---
# Blurred Roles and Team Evolution

## Summary

**One-sentence:** Diagnoses a product team's role overlap (PM/eng/design/data/AI) as a Venn diagram with ownership gaps and duplications; output is a team-evolution report with hire/restructure recommendations.

**One-paragraph:** Diagnoses a product team's role overlap (PM/eng/design/data/AI) as a Venn diagram with ownership gaps and duplications; output is a team-evolution report with hire/restructure recommendations. The methodology pins the artefact shape, anchors every non-trivial field to evidence, and routes the operator via a decision tree that always terminates either on an applicable rule or on `skip-this-methodology`. Apply when preconditions hold; skip via the tree otherwise.

**Ефективно для:**

- Post-Series-A scale-up: who owns what when PM, eng-lead, and design-lead overlap.
- AI-era role drift: PM doing prompt engineering, eng doing user research — diagnose drift.
- Hiring plan input: report says 'no one owns X' or 'two people duplicate Y'.
- Quarterly team review: track ownership gaps over time.

## Applies If (ALL must hold)

- Team has ≥4 people with overlapping responsibilities.
- Role drift symptoms observed (missed handoffs, duplicated work, orphaned decisions).
- Leadership has authority to restructure or hire.
- Team is willing to be candid in interviews / surveys.

## Skip If (ANY kills it)

- Team < 4 — every role gap is obvious without methodology.
- Leadership cannot restructure — diagnosis without action is theatre.
- Team will not be candid — diagnosis will be noise.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Org chart | roles + reports-to | HR |
| Responsibility map | Notion / RACI doc | PM ops |
| Interview transcripts | 1:1 anonymised notes | team |
| Recent decision log | last 30 days of product decisions + decider | PM |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/product/AGENTS.md` | Parent group context (vocabulary, neighbouring methodologies) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥6 testable rules with rationale + source incl. `skip-this-methodology` | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid + invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom / root-cause / fix | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end with decision gates | ~900 |
| `content/05-examples.xml` | reference | Full worked example end-to-end | ~900 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion(ref=rule-id) | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-blurred-roles-and-team-evolution` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/artefact-skeleton.md` | Markdown skeleton conforming to the output contract |
| `templates/artefact-instance.json` | JSON instance of a filled artefact |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-blurred-roles-team-evolution.py` | Validate produced artefact against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- Parent: `pro/product/AGENTS.md`
- [[competitive-positioning]]
- [[ai-feature-spec-contract]]
- [[annual-roadmap-vs-quarterly-okr-stitch]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
