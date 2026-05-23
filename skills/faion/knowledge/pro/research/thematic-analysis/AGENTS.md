---
slug: thematic-analysis
tier: pro
group: research
domain: research
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Codes interview transcripts into themes via two-pass open + axial coding, with inter-coder reliability check, producing a tagged-insights report wired to a design backlog."
content_id: "19c0c6fefc9049a8"
complexity: deep
produces: report
est_tokens: 4900
tags: ["thematic-analysis", "research", "qualitative", "coding", "pro"]
---
# Thematic Analysis

## Summary

**One-sentence:** Codes interview transcripts into themes via two-pass open + axial coding, with inter-coder reliability check, producing a tagged-insights report wired to a design backlog.

**One-paragraph:** Faion captures interviews and diary studies but had no method for the human craft of coding transcripts and extracting themes. AI assist exists for first-pass tagging but with no underlying methodology to validate or override the LLM coding. This methodology defines the two-pass coding loop (open codes -> axial categories), the dual-coder reliability gate (Cohen's kappa >= 0.6), the saturation rule (no new themes in 3 consecutive transcripts), and the design-backlog hand-off shape. Output is a versioned report keyed to source quotes, with each theme owning a decision/backlog item.

**Ефективно для:**

- паст-готова основа для повторюваної задачі «thematic analysis» — без винаходу велосипеда.
- контракт виходу пинить за схемою — downstream-агент може спожити без re-derive.
- rule-set + decision tree відсіюють варіанти, де методологія НЕ підходить.
- validator-скрипт ловить дрейф артефакту до того, як він потрапить у downstream.
- версіонована, з named-owner — артефакт не стає folklore через 6 місяців.

## Applies If (ALL must hold)

- you have >=5 recorded research interviews or diary entries in transcript form.
- the downstream consumer is a design / product backlog (not an academic paper).
- you have authority to commit time to two coding passes plus a reliability check.

## Skip If (ANY kills it)

- the dataset is <5 transcripts -- pattern detection is statistically unreliable.
- a fresh themes report (<= 90 days old) already covers the same corpus -- update, do not redo.
- the corpus is structured survey data, not open-ended transcripts -- use survey-design analysis instead.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Triggering context for the Thematic Analysis task | recent notes / tickets / interviews | operator's inbox or system of record |
| Named consumer (human or agent) | name + handle | engagement charter |
| Source-of-truth for inputs | doc / dashboard / repo path | system of record |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/research/researcher` | parent role/operating context. |
| `pro/research/research-repository-ops` | where the transcripts and the resulting report are stored. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5+ testable rules with rationale + skip-this-methodology fallback | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) for the artefact + valid/invalid/forbidden examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom + root-cause + fix | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input / action / output / decision-gate | 800 |
| `content/05-examples.xml` | essential | One full worked example end-to-end (anonymised) | 700 |
| `content/06-decision-tree.xml` | essential | Root-question → branches → conclusion(ref=rule-id) | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-inputs-summary` | haiku | Mechanical template fill, bounded transformation. |
| `synthesize-decision` | sonnet | Per-instance judgment against the rubric. |
| `review-for-compliance` | opus | Cross-input synthesis when stakes are high. |

## Templates

| File | Purpose |
|------|---------|
| `templates/thematic-analysis-report.md` | Markdown skeleton: themes section + per-theme quote anchors + backlog table. |
| `templates/codebook.json` | Codebook JSON: open codes + axial categories + kappa log. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-thematic-analysis.py` | Validate the report artefact against the 02-output-contract schema | After subagent returns, before downstream consumer reads |

## Related

- [[service-blueprint]]
- [[win-loss-interview-program]]
- [[user-research-at-scale]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (precondition pass, named owner, input reachability, regulatory regime) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it when in doubt about whether this methodology applies or which variant rule to enforce.
