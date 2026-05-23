---
slug: user-research-at-scale
tier: pro
group: research
domain: research
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: 9-stage AI-augmented research-ops pipeline (intake -> sampling -> instrumentation -> collection -> transcription -> coding -> synthesis -> review -> publish) with frozen codebook + N>=500/wk capacity + HITL gates.
content_id: "7ef86f3a7a26bab5"
complexity: deep
produces: report
est_tokens: 6800
tags: [user-research, research-ops, qualitative-analysis, ai-augmented-research]
---
# User Research at Scale

## Summary

**One-sentence:** 9-stage AI-augmented research-ops pipeline (intake -> sampling -> instrumentation -> collection -> transcription -> coding -> synthesis -> review -> publish) with frozen codebook + N>=500/wk capacity + HITL gates.

**One-paragraph:** Operates at N>=500 interview sessions/week or >=50 unmoderated tests, running a 9-stage AI-augmented pipeline: intake, sampling, instrumentation, collection, transcription, coding (frozen codebook + proposed_codes overflow channel), synthesis, review, publish. Human-in-the-loop checkpoints gate publication; codebook drift is bounded by the proposed_codes channel; PII handling forced through ZDR endpoints.

**Ефективно для:**

- N >= 500 сесій/тиждень або >= 50 unmoderated tests - manual coding не масштабується.
- Continuous discovery: weekly pulse a-la Teresa Torres з high volume.
- Multi-team product orgs з паралельними studies (research-as-platform).
- Localization: одне дослідження у 5+ мовах.
- Survey + behavior + interview triangulation - один researcher не прочитає все.

## Applies If (ALL must hold)

- N>=500 sessions/week or >=50 unmoderated tests where manual coding is the bottleneck.
- Continuous discovery teams needing a weekly pulse.
- Product orgs with multiple teams running parallel studies (research-as-platform).
- Localisation at scale (same study across 5+ languages).
- Survey + behavior + interview triangulation where one researcher cannot read everything.

## Skip If (ANY kills it)

- Small N (<10 deep interviews) - AI noise overwhelms signal.
- Strategic generative discovery where pattern recognition beats throughput.
- Sensitive / regulated topics (health, finance, minors) requiring manual consent chains.
- Early-stage startups with <100 users - no scale problem yet.
- Studies where rapport, body language, or longitudinal trust is the data.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Frozen codebook | YAML | research lead |
| Sampling plan | spreadsheet | research-ops |
| ZDR-eligible LLM endpoint | config | infrastructure / vendor |
| Transcription provider | Otter / Fireflies / Looppanel API | research-ops |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[continuous-discovery]] | supplies the weekly cadence that this pipeline feeds |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules + skip gate | ~1200 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns (symptom/root-cause/fix) | ~900 |
| `content/04-procedure.xml` | essential | 8-step procedure end-to-end | ~900 |
| `content/05-examples.xml` | essential | Worked example trace | ~900 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule id | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `intake-classify` | haiku | Classify incoming requests by study type + segment + tier. |
| `sampling-plan` | sonnet | Stratified sampling design + recruit batch sizes. |
| `transcription` | haiku | Mechanical transcript via vendor API. |
| `coding-frozen-book` | sonnet | Apply frozen codebook; route novel themes to proposed_codes. |
| `synthesis` | opus | Cross-study pattern recognition + weekly synthesis. |
| `hitl-gate` | human | Human review checkpoint before publish. |

## Templates

| File | Purpose |
|------|---------|
| `templates/codebook.yaml` | Frozen codebook with proposed_codes overflow channel |
| `templates/code-batch.sh` | Bash launcher: coding-frozen-book agent over a batch of transcripts |
| `templates/research-ops-report.md` | Weekly research-ops report skeleton |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-user-research-at-scale.py` | Validate the artefact against `content/02-output-contract.xml` schema | CI on each artefact change; pre-commit |

## Related

- [[continuous-discovery]]
- [[persona-building]]
- [[survey-design]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals onto a rule id from `content/01-core-rules.xml`, so the agent can decide in one read whether to run the methodology, halt, or route elsewhere. Use it whenever the inputs feel ambiguous.
