---
slug: daily-ads-anomaly-checklist
tier: pro
group: marketing
domain: marketing
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Daily Ads Anomaly Checklist: codified marketing practice that turns the recurring 'role-growth-marketing/Daily paid-ads spend + CPA check (15 min)' decision into a repeatable, auditable artefact.
content_id: "ca213b987e064c93"
tags: [daily-ads-anomaly-checklist, marketing, pro]
---
# Daily Ads Anomaly Checklist

## Summary

**One-sentence:** Daily Ads Anomaly Checklist: codified marketing practice that turns the recurring 'role-growth-marketing/Daily paid-ads spend + CPA check (15 min)' decision into a repeatable, auditable artefact.

**One-paragraph:** Daily Ads Anomaly Checklist addresses the gap surfaced by 'role-growth-marketing/Daily paid-ads spend + CPA check (15 min)'. ppc-manager has plenty of setup content but no daily 15-min triage routine; this is where money is actively lost. Mechanism: typed input → bounded transformation → contract-checked output. Primary output: a versioned artefact (decision record, checklist, score, or report) that downstream tasks can consume without re-deriving the rationale.

## Applies If (ALL must hold)

- task is an instance of 'role-growth-marketing/Daily paid-ads spend + CPA check (15 min)' OR a closely-adjacent variant
- the operator has the artefacts named in Prerequisites available before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == pro or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working artefact for this gap — replace, do not duplicate
- the change being decided is a greenfield prototype with no production users
- regulatory / compliance context overrides any in-methodology guidance (defer to legal)
- single-use throwaway task — overhead of the contract is not justified

## Prerequisites

- recent context for the 'role-growth-marketing/Daily paid-ads spend + CPA check (15 min)' task (last 30 days of activity)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream
- baseline conventions documented (CLAUDE.md / AGENTS.md / CONVENTIONS.md)

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/marketing/growth-marketer` | parent role skill — provides the operating context for this methodology |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: r1-bound-scope, r2-typed-input, r3-named-owner, r4-versioned, r5-traceable-decision | ~900 |
| `content/02-output-contract.xml` | essential | Required fields, forbidden patterns, allowed transformations | ~700 |
| `content/03-failure-modes.xml` | essential | 5 failure modes with detector + repair | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft_inputs_summary` | haiku | Template fill, bounded transformation |
| `synthesize_decision` | sonnet | Per-instance judgment with bounded inputs |
| `review_for_compliance` | opus | Cross-input synthesis when stakes are high |

## Templates

| File | Purpose |
|------|---------|
| `templates/daily-ads-anomaly-checklist.json` | JSON schema for the Daily Ads Anomaly Checklist output contract |
| `templates/daily-ads-anomaly-checklist.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-daily-ads-anomaly-checklist.py` | Enforce Daily Ads Anomaly Checklist output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `pro/marketing/growth-marketer/`
- upstream playbook: `role-growth-marketing/Daily paid-ads spend + CPA check (15 min)`
- methodology family: `pro/marketing/` (gap-p2 batch, F-059-063)
