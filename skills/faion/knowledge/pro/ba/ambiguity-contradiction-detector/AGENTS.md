---
slug: ambiguity-contradiction-detector
tier: pro
group: ba
domain: ba
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Scans a requirements doc against a closed checklist (vague quantifiers / undefined terms / contradictory ACs / missing edge-cases / unowned decisions) and emits a per-finding report with severity, evidence quote, and remediation owner.
content_id: "92dd4f0ca880ce08"
complexity: medium
produces: report
est_tokens: 5100
tags: [ba, requirements, ambiguity, contradiction, review]
---
# Ambiguity and Contradiction Detector

## Summary

**One-sentence:** Scans a requirements doc against a closed checklist (vague quantifiers / undefined terms / contradictory ACs / missing edge-cases / unowned decisions) and emits a per-finding report with severity, evidence quote, and remediation owner.

**One-paragraph:** Scans a requirements doc against a closed checklist (vague quantifiers / undefined terms / contradictory ACs / missing edge-cases / unowned decisions) and emits a per-finding report with severity, evidence quote, and remediation owner. The methodology pins the artefact shape, ties every conclusion to a rule, and routes the operator via a decision tree that always terminates either on an applicable rule or on `skip-this-methodology`. Apply when preconditions hold; skip via the tree otherwise.

**Ефективно для:**

- Pre-handoff review: BA → eng — ambiguous requirements cause rework loops.
- Multi-stakeholder requirements (sponsor + ops + legal + eng) — contradictions inevitable.
- Regulated build: contradiction in requirements blocks audit signoff.
- Re-validation: 90-day old doc — ambiguity drift since approval.

## Applies If (ALL must hold)

- Requirements doc length ≥2 pages.
- Doc enters handoff (BA → eng / BA → audit) or re-validation window.
- Doc owner is reachable and accountable for remediation.
- Closed-checklist categories cover the doc's content shape.

## Skip If (ANY kills it)

- Doc length ≤1 page — overhead exceeds value.
- Doc passed prior detector run within last 7 days.
- Research spike with no handoff intent.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Requirements doc | Markdown / Confluence / Word | BA owner |
| Closed-checklist categories | YAML | BA core team |
| Owner roster for remediation | Markdown / org chart | BA lead |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/ba/AGENTS.md` | Parent domain context (vocabulary, neighbouring methodologies) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules with rationale + source + skip rule | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid + invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns (symptom / root-cause / fix) | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end with decision gates | ~900 |
| `content/05-examples.xml` | essential | Worked example end-to-end (input → output) | ~700 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion(ref=rule-id) | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-ambiguity-contradiction-detector` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/report.md` | Markdown report skeleton — finding rows with severity + evidence + owner |
| `templates/report-instance.json` | JSON instance of a filled report (machine-readable mirror) |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ambiguity-contradiction-detector.py` | Validate produced artefact against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- Parent: `pro/ba/AGENTS.md`
- [[ai-user-story-decomposition]]
- [[ba-governance]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
