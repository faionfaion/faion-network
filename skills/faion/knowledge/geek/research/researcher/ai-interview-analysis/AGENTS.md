---
slug: ai-interview-analysis
tier: geek
group: research
domain: research
version: 1.1.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: Analyzes a single interview transcript into a structured artefact (highlights, codes, contradictions, follow-up questions) with quoted evidence + researcher verification.
content_id: "210db41c7c7a24fa"
complexity: medium
produces: report
est_tokens: 5000
tags: [interview, analysis, highlights, follow-up, ai-research]
---
# AI-Assisted Single-Interview Analysis

## Summary

**One-sentence:** Analyzes a single interview transcript into a structured artefact (highlights, codes, contradictions, follow-up questions) with quoted evidence + researcher verification.

**One-paragraph:** Analyzes a single interview transcript into a structured artefact (highlights, codes, contradictions, follow-up questions) with quoted evidence + researcher verification. The methodology is testable end-to-end: each artefact it produces conforms to the JSON Schema in `content/02-output-contract.xml`, every claim in the body resolves to a rule in `content/01-core-rules.xml`, and the decision-tree in `content/06-decision-tree.xml` routes observable inputs to the right rule.

**Ефективно для:**

- Швидкий аналіз свіжого інтерв'ю за 15 хв замість години ручної роботи.
- Виявлення contradictions у відповідях респондента (signal vs noise).
- Follow-up questions для наступного інтерв'ю в cohort.
- Highlight reel з timestamp/line range для звіту.

## Applies If (ALL must hold)

- Транскрипт єдиного інтерв'ю з speaker labels.
- Research question + interview guide доступні.
- Researcher верифікує результат перед використанням.

## Skip If (ANY kills it)

- Multi-interview synthesis — використовуй interview-note-synthesis-ai замість.
- PII/sensitive без redaction policy.
- Інтерв'ю < 15 хв — ручний нотатник швидший.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| transcript | Markdown with speaker labels | interview platform |
| interview guide | list of intended questions | PI |
| research question | one sentence | PI |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| _none_ | This methodology does not require upstream context. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns (symptom/root-cause/fix) | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure (input/action/output/decision-gate) | 900 |
| `content/05-examples.xml` | essential | One worked example end-to-end | 700 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule in 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| classify-input | sonnet | Light judgment; identifies branch in decision tree. |
| draft-output | sonnet | Drafting the output artefact per schema. |
| validate-output | haiku | Mechanical schema validation via script. |

## Templates

| File | Purpose |
|------|---------|
| `templates/analysis-report.md` | Single-interview analysis report skeleton |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ai-interview-analysis.py` | Validate output artefact against schema in 02-output-contract.xml | CI on each artefact change; pre-commit |

## Related

- [[interview-note-synthesis-ai]]
- [[ai-coding-of-qualitative-data-protocol]]
- [[ai-assisted-persona-building]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from the question "Is this a single-interview analysis (not multi-interview synthesis)?" and routes observable input signals to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Apply it whenever the input shape changes or before scaling a pilot run.
