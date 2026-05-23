---
slug: internal-rfc-template
tier: geek
group: sdd
domain: sdd
version: 1.1.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: Generates a light-weight Request-for-Comments document for proposals NOT yet decisions — more open than ADR, less heavy than design-doc.
content_id: "59f4c68440bf7e79"
complexity: medium
produces: spec
est_tokens: 3800
tags: ["sdd", "rfc", "proposal", "template", "decision"]
---
# Internal RFC Template

## Summary

**One-sentence:** Generates a light-weight Request-for-Comments document for proposals NOT yet decisions — more open than ADR, less heavy than design-doc.

**One-paragraph:** Internal RFC Template produces a spec that fixes a recurring decision in the sdd domain. It pins the artefact shape, attaches evidence, and blocks unfit inputs via the decision tree. Apply when the preconditions hold; otherwise the decision tree routes you to skip-this-methodology.

**Ефективно для:**

- Запропонувати зміну архітектури без commiting у ADR.
- Зібрати думки команди про новий процес перш ніж писати design-doc.
- Open-ended discussion з фіксованою структурою для відстеження.
- Lightweight pre-mortem перед серйозним рішенням.
- Cross-team alignment коли ще немає одного власника рішення.

## Applies If (ALL must hold)

- Proposal is not yet a decision — author wants feedback.
- Multiple roles need to comment before commitment.
- Scope is larger than a single PR but smaller than a quarter-long initiative.

## Skip If (ANY kills it)

- Decision is already made — use an ADR.
- Scope is a single PR — use the PR description.
- Time pressure < 24h — use a meeting + decision log instead.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Problem statement | Markdown | RFC author |
| Stakeholder list | Markdown / YAML | RFC author |
| Existing related ADRs / RFCs | Markdown links | knowledge base |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| none | This methodology has no upstream dependencies. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules with rationale + source + skip rule | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid + invalid examples | 700 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns (symptom / root-cause / fix) | 600 |
| `content/04-procedure.xml` | essential | 5-step procedure with decision gates | 700 |
| `content/05-examples.xml` | supplemental | One worked example end-to-end | 400 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion ref=rule-id | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-internal-rfc-template` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/RFC-template.md` | Markdown RFC skeleton with required sections + frontmatter |
| `templates/rfc.schema.json` | JSON Schema for RFC frontmatter |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-internal-rfc-template.py` | Validate produced artefact against schema | CI on each artefact change; pre-commit |

## Related

- [[adr-consequence-evidence-binding]]
- [[tech-radar-thoughtworks-style]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal (input shape, infra availability, decision class) and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
