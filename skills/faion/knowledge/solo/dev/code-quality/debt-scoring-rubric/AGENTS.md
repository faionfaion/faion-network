---
slug: debt-scoring-rubric
tier: solo
group: dev
domain: dev
version: 1.0.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Produces a ranked debt-register artefact by scoring each item on 5 factors (User-Impact × Change-Frequency × Fragility × Blast-Radius / Fix-Cost) with confidence band and defensible anchors.
content_id: "c0dcc1add6f06b45"
complexity: medium
produces: rubric
est_tokens: 4200
tags: [tech-debt, scoring, prioritization, architecture-debt, design-debt]
---

# Debt Scoring Rubric

## Summary

**One-sentence:** Five-factor scoring rubric (User-Impact × Change-Frequency × Fragility × Blast-Radius / Fix-Cost) that produces a single numeric debt score per item, defensible to PMs and the org.

**One-paragraph:** Solves the recurring "we know we have debt but can't defend the sprint scope" problem. Mechanism: each debt item is scored 1-5 on five factors with explicit anchors per score; the rubric returns score = (User-Impact × Change-Frequency × Fragility × Blast-Radius) / Fix-Cost, plus a confidence band. Items above the team's prioritization threshold enter the next debt sprint; below-threshold items are logged in the register with the score so they can be re-evaluated later. Primary output: a ranked debt list with score, confidence, and a one-line "what changes if we pay this".

**Ефективно для:**

- Solo dev defending "I need a debt sprint" to a non-technical client.
- Outsource lead presenting a debt-register prioritization to a steering committee.
- AI-assisted debt audit — the rubric anchors LLM scoring to observable metrics.
- Quarterly debt grooming: rescore once + re-rank.

## Applies If (ALL must hold)

- Team / individual maintains an existing codebase / design system / infrastructure.
- At least 5 candidate debt items collected (single-item scoring is overhead).
- Prioritization audience is a PM / client / stakeholder who needs a defensible ranking.
- Debt category ∈ {architecture, code, test, design, infra, dependency, documentation}.

## Skip If (ANY kills it)

- Greenfield project &lt; 3 months old — no debt baseline.
- Single-developer experiment with no production users — score has no business meaning.
- Urgent security / compliance debt — separate must-do classification, not a scored ranking.
- &gt; 100 candidate items — triage first via tech-debt-management.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Candidate debt items list | CSV / Markdown | author + grooming session |
| Change-frequency data | git log | repo |
| Fragility data (bug counts per area) | tracker export | tracker |
| Blast-radius data (service map / dep graph) | YAML / diagram | infra |
| User-impact anchor calibration | doc | stakeholder agreement |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/dev/code-quality/tech-debt-management` | Defines payoff strategies + CI gates the score feeds. |
| `solo/dev/blast-radius-scoring-rubric` | Blast-radius factor shares its 1/3/5 anchors. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5+ rules: factor definitions, 1-5 anchor scale, formula, confidence band, defensibility, run + skip | 1400 |
| `content/02-output-contract.xml` | essential | JSON Schema for the debt-register + valid/invalid + forbidden | 800 |
| `content/03-failure-modes.xml` | essential | 6 LLM/agent failure modes when applying the rubric | 900 |
| `content/04-procedure.xml` | medium | 5-step procedure: collect → anchor → score → cross-check → publish | 700 |
| `content/06-decision-tree.xml` | essential | Tree: items ≥ 5? anchors calibrated? per-item scored? threshold met? → verdict | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `metric_extraction_per_item` | haiku | Pull change-frequency / bug-count from existing stores. |
| `per-factor_scoring` | sonnet | Bounded judgment per anchor; can read code context. |
| `cross-item_ranking_review` | opus | Catch over-anchoring drift across the whole list. |

## Templates

| File | Purpose |
|------|---------|
| `templates/debt-scoring-rubric.json` | JSON Schema for the debt-register artefact. |
| `templates/anchor-calibration.md` | 1-5 anchor definitions per factor, signed off by stakeholder. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-debt-scoring-rubric.py` | Validate a debt-register JSON against schema + formula consistency. | After scoring session; before publishing the register. |

## Related

- [[code-quality/tech-debt-management]] — payoff strategies the score feeds.
- [[blast-radius-scoring-rubric]] — shares the blast factor.
- external: [Martin Fowler — TechnicalDebtQuadrant](https://martinfowler.com/bliki/TechnicalDebtQuadrant.html) · [Adam Tornhill — Your Code as a Crime Scene] · [Google SRE workbook — toil and tech debt]

## Decision tree

See `content/06-decision-tree.xml`. The tree first verifies anchor calibration is signed off by the stakeholder. It then walks per-item: all 5 factors scored with evidence? formula computed correctly? confidence band assigned? Aggregate: items above threshold flagged for next sprint. Leaves emit `publish-register`, `block-missing-anchors`, `block-formula-mismatch`, or `block-no-evidence`. Each leaf references a rule in `01-core-rules.xml`.
