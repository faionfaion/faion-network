---
slug: ai-interview-analysis
tier: geek
group: ux
domain: ux
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Produces a cross-interview themes report from raw audio/video transcripts using AI transcription + per-interview coding + cross-interview synthesis with quote-grounded themes.
content_id: "210db41c7c7a24fa"
complexity: deep
produces: report
est_tokens: 4900
tags: [interviews, transcripts, qualitative-research, theme-extraction, ai-assisted]
---
# AI Interview Analysis

## Summary

**One-sentence:** Produces a cross-interview themes report from raw audio/video transcripts using AI transcription + per-interview coding + cross-interview synthesis with quote-grounded themes.

**One-paragraph:** Manual interview analysis costs ~4–6 hours per interview. AI transcription + agent-driven coding compresses this to ~30 min, but raw output is noisy. This methodology pipelines: (1) Whisper / Deepgram transcription, (2) per-interview thematic coding with quote anchors, (3) cross-interview theme synthesis with frequency + confidence, (4) human spot-check on a 10 % sample. Output: themes report with theme list, supporting quotes per theme, occurrence count, confidence label.

**Ефективно для:** user researcher із 10+ interviews, що потребує крос-інтерв'ю themes за день замість тижня.

## Applies If (ALL must hold)

- ≥5 interview transcripts to analyse together.
- Quote-grounded themes are required (not free-text summaries).
- Budget for AI transcription provider available.

## Skip If (ANY kills it)

- Single interview — manual analysis is faster.
- Transcripts unavailable + audio not transcribable (poor quality / dialect).
- Stakeholders distrust agent-coded themes without human spot-check capacity.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Raw audio / video | mp3 / mp4 / wav | research ops |
| Interview script | markdown | research |
| Speaker labels mapping | JSON | research |
| Theme taxonomy seed (optional) | YAML | research |

## Assumes Loaded

| Methodology | Why |
|---|---|
| [[ai-assisted-persona-building]] | Downstream consumer of themes. |
| [[synthetic-users]] | Pre-validation companion for early ideation. |

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
| `templates/themes-report.json` | JSON skeleton: themes + interview_count + provider + spot_check_pct + open_questions. |
| `templates/prompt-code-interview.txt` | Agent prompt for per-interview coding. |
| `templates/prompt-synthesise-themes.txt` | Agent prompt for cross-interview synthesis. |
| `templates/_smoke-test.json` | Filled 30-second attention threshold theme example. |

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-ai-interview-analysis.py` | Validate the artefact against the output contract. | Pre-commit + CI. |

## Related

- [[ai-assisted-persona-building]]
- [[synthetic-users]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals to a rule in `01-core-rules.xml`. Walk it before producing the report; mis-routing leads to producing the wrong artefact shape.
