---
slug: ads-conversion-tracking
tier: pro
group: marketing
domain: marketing
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Configures multi-platform conversion tracking (events with $ values, browser pixels, server-side APIs, attribution windows, dedup) so smart bidding optimizes on complete data.
content_id: "2075321e9282e31e"
complexity: deep
produces: config
est_tokens: 6500
tags: ["marketing", "conversion-tracking", "pixel", "capi", "server-side", "ppc", "pro"]
---
# Ads Conversion Tracking

## Summary

**One-sentence:** Configures multi-platform conversion tracking (events with $ values, browser pixels, server-side APIs, attribution windows, dedup) so smart bidding optimizes on complete data.

**One-paragraph:** Browser-side conversion tracking loses 20-40% of events to ad blockers, iOS privacy, and cookie restrictions. This methodology configures the full multi-platform stack: macro + micro events with $ values, browser pixels (Meta Pixel, Google Tag, LinkedIn Insight Tag), server-side APIs (Meta CAPI, Google enhanced conversions, LinkedIn API), attribution-window matching to sales-cycle, and dedup keys. Output: tracking config + event spec + server-side mapping + verification checklist.

**Ефективно для:**

- New campaign-tracking implementation з server-side від day one.
- Audit: CRM покаже 500 sales, ads показують 800 conversions — пошук дубля.
- iOS17 / cookie-deprecation refit: CAPI + dedup key + enhanced match.
- Offline-conversion upload з CRM для long-cycle deals.

## Applies If (ALL must hold)

- New ads-tracking implementation OR audit when reported conversions don't match CRM.
- Server-side API available (CAPI / Google enhanced / LinkedIn API).
- Sales-cycle defined (drives attribution window).
- Operator can implement dataLayer or has dev support.

## Skip If (ANY kills it)

- Browser-only fallback acceptable (low-spend, low-stakes) — methodology overhead exceeds value.
- No CRM source-of-truth — dedup impossible.
- Sales-cycle undefined — attribution window arbitrary.

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
| `content/03-failure-modes.xml` | essential | >=4 antipatterns (symptom/root-cause/fix) | ~900 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with inputs / actions / outputs / decision-gates | ~1100 |
| `content/06-decision-tree.xml` | essential | Decision tree mapping observable signals to a rule from 01-core-rules.xml | ~700 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-applicability` | sonnet | Decision-tree application; bounded judgement. |
| `draft-ads-conversion-tracking` | opus | Synthesis under output contract; final write-up. |
| `validate-output` | haiku | Mechanical schema check via scripts/validate-<slug>.py. |

## Templates

| File | Purpose |
|------|---------|
| `templates/config.yaml` | YAML config skeleton with 5-line header |
| `templates/output.json` | JSON sidecar with __faion_header__ |
| `templates/_smoke-test.yaml` | Minimum viable filled config |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ads-conversion-tracking.py` | Validate the produced artefact against the JSON Schema in `content/02-output-contract.xml` | After subagent returns, before publish; pre-commit if artefact is git-tracked |

## Related

- [[ad-account-hygiene-checklist]]
- [[ads-attribution-models]]
- [[learnings-database-schema]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (inputs available, thresholds, gating prerequisites) to a concrete verdict, each leaf referencing a rule from `01-core-rules.xml`. Use it whenever multiple variants of the methodology look applicable, or when an upstream condition (e.g. positioning undefined, spend below threshold) makes the methodology a misfit.
