---
slug: ai-assisted-persona-building
tier: geek
group: ux
domain: ux
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Produces a validated persona report from analytics + interviews + surveys via two-pass clustering (Sonnet broad cluster → Haiku detail refine) with quote grounding + human validation gate.
content_id: "8a4004be71a432bd"
complexity: deep
produces: report
est_tokens: 4900
tags: [personas, user-research, clustering, ai-assisted, validation]
---
# AI-Assisted Persona Building (Two-Pass)

## Summary

**One-sentence:** Produces a validated persona report from analytics + interviews + surveys via two-pass clustering (Sonnet broad cluster → Haiku detail refine) with quote grounding + human validation gate.

**One-paragraph:** Persona building from raw research data is high-effort and human-biased. Two-pass agent clustering reduces effort while preserving rigour: pass 1 (Sonnet) clusters analytics + interview snippets into broad segments; pass 2 (Haiku) refines each cluster with quote grounding + goal extraction. Every persona claim is anchored to a quote citation. A human validation gate blocks publishing until ≥3 stakeholders sign off. Output: persona report with N personas, each with quote evidence + confidence + open questions.

**Ефективно для:** user researcher / PM, що синтезує persons із 50–500 source items (interviews + surveys + analytics) — і потребує quote-grounded + validated report.

## Applies If (ALL must hold)

- Source dataset ≥50 items mixing analytics + interviews + surveys.
- Stakeholder buy-in needed for persona credibility (≥3 reviewers signing off).
- Each persona claim must be anchored to a quote / data point.

## Skip If (ANY kills it)

- Source dataset is <30 items — manual synthesis is faster.
- Personas are speculative (no source data) — see [[ai-persona-building]] for single-pass cheap path.
- Stakeholder validation not feasible — outputs will be ignored.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Interview transcripts | txt/json | research ops |
| Survey results | CSV | research ops |
| Analytics segments | JSON | data team |
| Stakeholder reviewer list | list | PM |

## Assumes Loaded

| Methodology | Why |
|---|---|
| [[ai-interview-analysis]] | Quote extraction from transcripts. |
| [[ai-persona-building]] | Single-pass alternative for cheaper scenarios. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 5 testable rules + rationale + source. | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid / invalid / forbidden examples. | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns (symptom / root-cause / fix). | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end. | ~800 |
| `content/05-examples.xml` | essential | One full worked example end-to-end. | ~700 |
| `content/06-decision-tree.xml` | essential | Routing tree → conclusion(ref=rule-id). | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| `decide-applies` | sonnet | Decision tree application. |
| `produce-report` | sonnet | Structured output composition. |
| `validate-output` | haiku | Schema check. |

## Templates

| File | Purpose |
|---|---|
| `templates/persona-report.json` | JSON skeleton: personas + source_count + passes + stakeholder_reviews + open_questions. |
| `templates/prompt-broad-cluster.txt` | Sonnet prompt for broad clustering. |
| `templates/prompt-refine-cluster.txt` | Haiku prompt for per-cluster refinement. |
| `templates/_smoke-test.json` | Filled time-poor-parent persona example. |

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-ai-assisted-persona-building.py` | Validate the artefact against the output contract. | Pre-commit + CI. |

## Related

- [[ai-interview-analysis]]
- [[ai-persona-building]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals to a rule in `01-core-rules.xml`. Walk it before producing the report; mis-routing leads to producing the wrong artefact shape.
