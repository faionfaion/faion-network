---
slug: ads-budget-optimization
tier: pro
group: marketing
domain: marketing
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Allocates budgets via efficiency-ratio + 70-20-10 rule (70% scale / 20% optimize / 10% test) and emits a monthly reallocation spec with scale-up + scale-down triggers.
content_id: "30e7885c8800916a"
complexity: medium
produces: spec
est_tokens: 5300
tags: ["marketing", "ppc", "budget", "allocation", "efficiency", "pro"]
---
# Ads Budget Optimization

## Summary

**One-sentence:** Allocates budgets via efficiency-ratio + 70-20-10 rule (70% scale / 20% optimize / 10% test) and emits a monthly reallocation spec with scale-up + scale-down triggers.

**One-paragraph:** Most paid-ads teams cut underperformers prematurely and double scaling-campaigns recklessly. This methodology imposes 70-20-10 budget discipline (70% scaling winners / 20% optimizing mid / 10% test reserve), efficiency-ratio based reallocation (ROAS / CPA / target multiple), and explicit step-rules (no > 20% budget change per week unless evidence). Output: monthly allocation spec + weekly review template + cross-channel reallocation rules.

**Ефективно для:**

- Multi-campaign PPC manager шукає reallocation framework без premature cuts.
- Заміна gut-feel allocation на 70-20-10 + efficiency-ratio rules.
- Scale-up discipline: ніяких > 20% budget jumps без evidence.
- Cross-platform reallocation: Meta vs. Google vs. LinkedIn based on ratio.

## Applies If (ALL must hold)

- Multi-campaign or multi-channel program (>= 3 campaigns OR 2 platforms).
- Spend >= $3k/month total.
- Conversion tracking accurate (variance < 15% per ads-attribution-models methodology).
- Weekly or monthly review meeting in place.

## Skip If (ANY kills it)

- Single-campaign account — no reallocation surface.
- Conversion tracking unreliable — allocate based on broken data is worse than steady-state.
- Spend < $1k/mo — allocation overhead exceeds value.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Inputs source-of-truth | system / dashboard / transcript | operator-managed |
| Prior artefact (if any) | Markdown / JSON / YAML | prior cycle |
| Named consumer for output | team contact / agent task | operator-managed |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/marketing/AGENTS.md` | parent group context (vocabulary, neighbours) |
| [[learnings-database-schema]] | shared cumulative-knowledge substrate (if available) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | >=5 testable rules with rationale + source | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid + forbidden patterns | ~1000 |
| `content/03-failure-modes.xml` | essential | >=3 antipatterns (symptom/root-cause/fix) | ~900 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with inputs / actions / outputs / decision-gates | ~1100 |
| `content/05-examples.xml` | essential | One end-to-end worked example | ~900 |
| `content/06-decision-tree.xml` | essential | Decision tree mapping observable signals to a rule from 01-core-rules.xml | ~700 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-applicability` | sonnet | Decision-tree application; bounded judgement. |
| `draft-ads-budget-optimization` | opus | Synthesis under output contract; final write-up. |
| `validate-output` | haiku | Mechanical schema check via scripts/validate-<slug>.py. |

## Templates

| File | Purpose |
|------|---------|
| `templates/spec.md` | Markdown spec skeleton |
| `templates/output.json` | JSON spec sidecar with __faion_header__ |
| `templates/_smoke-test.md` | Minimum viable filled spec |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ads-budget-optimization.py` | Validate the produced artefact against the JSON Schema in `content/02-output-contract.xml` | After subagent returns, before publish; pre-commit if artefact is git-tracked |

## Related

- [[ad-account-hygiene-checklist]]
- [[ads-attribution-models]]
- [[learnings-database-schema]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (inputs available, thresholds, gating prerequisites) to a concrete verdict, each leaf referencing a rule from `01-core-rules.xml`. Use it whenever multiple variants of the methodology look applicable, or when an upstream condition (e.g. positioning undefined, spend below threshold) makes the methodology a misfit.
