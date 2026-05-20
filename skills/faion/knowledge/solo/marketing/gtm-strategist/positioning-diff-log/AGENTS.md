---
slug: positioning-diff-log
tier: solo
group: marketing
domain: gtm-strategist
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "84d2e0b54e18f65f"
summary: An ADR-style positioning diff log that captures every change to a product's positioning statement with the trigger, the old wording, the new wording, the expected effect, and the metric to check 30 / 90 days later — so positioning iterations stop disappearing into git history without rationale.
tags: [positioning, marketing, adr-style, log, indie-hacker, decisions]
---

# Positioning Diff Log

## Summary

**One-sentence:** Treat every positioning-statement change like an ADR: record the trigger, the old wording, the new wording, the expected effect, and the metric to check at 30/90 days, in a single `positioning.diff.md` file that lives in the marketing repo.

**One-paragraph:** Solo SaaS builders iterate positioning constantly — competitor scans, persona recalibrations, accidental insights from a customer call. The iterations vanish into git history (or worse, into landing-page-only edits) without rationale, so 6 months later nobody remembers why the current positioning is the one in production or whether the prior one performed better. The positioning-diff-log applies ADR discipline to positioning: each change is an entry with header (date, trigger, expected effect, success metric), an old/new diff with at least one verbatim source quote, and a 30/90-day check section that gets populated after the data is in. Primary output: `positioning.diff.md` with append-only entries, plus a monthly review that surfaces entries whose expected effect was not observed.

## Applies If (ALL must hold)

- product is past MVP launch (positioning statement actually exists on a live landing page)
- founder iterates positioning at least once per quarter (changes hero, value prop, audience description)
- founder has at least one quantitative signal that responds to positioning: visit-to-trial, trial-to-paid, demo-conversion, headline-click-through
- positioning lives in a versioned location (landing repo, MDX file, CMS export) not a hand-edited live page

## Skip If (ANY kills it)

- pre-MVP — positioning is still in discovery, write hypotheses not a diff log
- founder changes positioning impulsively and is not ready for the ADR discipline — start with a 1-sentence "trigger + change" log before adopting the full template
- positioning is contractually locked (brand-licensed product) — diff log adds friction without flexibility benefit
- single landing page with no analytics — no metric to validate the diff against

## Prerequisites

- a single canonical location for the current positioning (`POSITIONING.md` or equivalent) referenced by the landing page
- analytics + funnel metrics available at 30-day granularity
- a calendar habit: positioning review on the first Monday of each month

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/marketing/gtm-strategist/growth-brand-positioning` | The positioning framework itself (segment, alternatives, differentiation) |
| `solo/marketing/seo-manager/zero-click-search-adaptation` | Landing-section structure where positioning surfaces |
| `solo/marketing/gtm-strategist/objection-bank` | Objection-bank entries are a common trigger for positioning iteration |

## Content

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: ADR header, trigger required, 30/90-day check, verbatim source quote, monthly review | ~800 |
| `content/02-output-contract.xml` | essential | positioning.diff.md entry schema, monthly review schema | ~600 |
| `content/03-failure-modes.xml` | essential | 6 failure modes: no trigger, missing 30/90 check, edit-without-entry, etc. | ~800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `extract_trigger_from_recent_signals` | sonnet | Cross-source synthesis: customer calls, support tickets, competitor scans |
| `draft_positioning_change_proposal` | opus | Cross-input creative work on positioning copy |
| `populate_30_90_day_check_results` | sonnet | Read analytics, compare to predicted effect |

## Templates

| File | Purpose |
|------|---------|
| `templates/positioning-entry.md` | Single-entry skeleton with header, old/new, expected effect, success metric, check sections |
| `templates/monthly-review.md` | Monthly review post: entries due for check, entries whose effect was not observed |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/due-checks.py` | Walks positioning.diff.md, surfaces entries past their 30-day or 90-day check date and not yet checked | Monthly |
| `scripts/positioning-vs-landing-diff.py` | Diffs canonical POSITIONING.md against the live landing page; flags drift | Weekly |

## Related

- parent skill: `solo/marketing/gtm-strategist/SKILL.md`
- peer methodologies: `pro/marketing/gtm-strategist/growth-brand-positioning`, `solo/marketing/gtm-strategist/objection-bank`
- external: [April Dunford, Obviously Awesome (Ambient Press, 2019)] · [Michael Nygard, Documenting Architecture Decisions (2011) — the ADR pattern this borrows from] · [Patrick Campbell, ProfitWell positioning research notes]
