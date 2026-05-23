---
slug: ad-account-hygiene-checklist
tier: pro
group: marketing
domain: marketing
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Weekly + monthly ad-account hygiene checklist (naming, exclusions, learning-phase, budget pacing, audit-log) that catches drift before it eats spend.
content_id: "e6b8e3a5132a2b5e"
complexity: light
produces: checklist
est_tokens: 4100
tags: ["marketing", "ppc", "hygiene", "checklist", "account-structure", "pro"]
---
# Ad Account Hygiene Checklist

## Summary

**One-sentence:** Weekly + monthly ad-account hygiene checklist (naming, exclusions, learning-phase, budget pacing, audit-log) that catches drift before it eats spend.

**One-paragraph:** Ad-account hygiene is the most under-documented PPC discipline — naming conventions, exclusion lists, learning-phase respect, budget pacing alerts, and audit-log review. Drift here costs 10-25% of monthly spend silently. This methodology emits a 14-item weekly + 8-item monthly checklist tagged by platform (Google / Meta / LinkedIn), with owner + cycle + completion-evidence per row.

**Ефективно для:**

- PPC manager з >=$1k/mo spend і >=2 campaigns шукає standing weekly ritual.
- Onboarding нового account-owner: один cycle того ж checklist щоб виявити drift.
- Pre-quarter review: знайти що 'тихо протекло' за 90 днів.
- Audit-log discipline для multi-tenant agency accounts.

## Applies If (ALL must hold)

- Active paid-ads account with monthly spend >= $1k.
- Operator has admin or owner access to the account.
- Account has >=2 active campaigns (single-campaign accounts don't need hygiene).
- Account survives >=3 month window (one-off accounts don't accumulate drift).

## Skip If (ANY kills it)

- Spend < $500/mo — drift cost < checklist overhead.
- Single-campaign account — checklist mostly N/A.
- Account closing within 30 days — hygiene irrelevant.

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
| `content/06-decision-tree.xml` | essential | Decision tree mapping observable signals to a rule from 01-core-rules.xml | ~700 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-applicability` | sonnet | Decision-tree application; bounded judgement. |
| `draft-ad-account-hygiene-checklist` | opus | Synthesis under output contract; final write-up. |
| `validate-output` | haiku | Mechanical schema check via scripts/validate-<slug>.py. |

## Templates

| File | Purpose |
|------|---------|
| `templates/checklist.md` | Operating checklist skeleton with rows + owner + cadence |
| `templates/_smoke-test.md` | Minimum viable filled-in checklist |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ad-account-hygiene-checklist.py` | Validate the produced artefact against the JSON Schema in `content/02-output-contract.xml` | After subagent returns, before publish; pre-commit if artefact is git-tracked |

## Related

- [[ad-account-hygiene-checklist]]
- [[ads-attribution-models]]
- [[learnings-database-schema]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (inputs available, thresholds, gating prerequisites) to a concrete verdict, each leaf referencing a rule from `01-core-rules.xml`. Use it whenever multiple variants of the methodology look applicable, or when an upstream condition (e.g. positioning undefined, spend below threshold) makes the methodology a misfit.
