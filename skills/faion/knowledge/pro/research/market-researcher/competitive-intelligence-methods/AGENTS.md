# Competitive Intelligence Methods

## Summary

A two-sub-methodology bundle — competitor landscape mapping and competitive-intelligence feature analysis — run as a sequential pipeline: landscape first (2x2 positioning + whitespace identification across 15-20 competitors covering all four types), then feature-matrix drill-down (Y/P/N + 0-3 quality score with evidence URL per cell, gap-validation critic with forced skip budget).

## Why

Teams default to the 3-5 obvious head-on competitors and miss substitutes (spreadsheets, email, "do nothing") — the actual churn cause. A feature matrix with only Y/N hides quality differences; without a gap-validator critic forcing ≥40% skips, pursuit-bias turns every empty cell into a roadmap item. The four-type taxonomy and adversarial critic together produce a defensible gap shortlist.

## When To Use

- Pre-MVP wedge selection: need the 2x2 + gap list before writing a spec.
- Quarterly competitive review: deltas in funding, pricing, positioning, hiring across top 15-20 competitors.
- New-feature go/no-go: deciding whether feature X is table-stakes, opportunity, or moat-building.
- Pricing repositioning: anchoring price tier on a fresh per-competitor pricing scrape.
- Pitch deck or investor update: defensible "competitive landscape" slide with sourced rows.

## When NOT To Use

- Sub-week tactical decisions (single ad copy, single landing-page test) — matrices are too coarse.
- True greenfield with fewer than 3 competitors — feature matrix collapses to 1 column; use jobs-to-be-done.
- Highly regulated B2B (defense, banking core) where competitor data is private and any public pull is misleading.
- Late-stage scaling where customer-success and retention data dominate — feature matrix produces feature-bloat backlog.
- After product-market fit — optimizing on feature matrix is how startups become "Salesforce-but-cheaper" forever.

## Content

| File | What's inside |
|------|---------------|
| `content/01-landscape-mapping.xml` | Four competitor types, 2x2 positioning matrix, whitespace identification, orchestrator prompt pattern |
| `content/02-feature-matrix.xml` | Feature inventory, Y/P/N + quality-score matrix, gap-validation critic (three questions, skip budget), evidence-URL rule |
| `content/03-rules-and-antipatterns.xml` | Evidence-per-cell rule, direct-only blindness, static-snapshot decay, whitespace fallacy, agent gotchas |

## Templates

| File | Purpose |
|------|---------|
| `templates/landscape-table.md` | Competitor landscape table: direct/indirect/substitute/potential with founding/funding/pricing/positioning |
| `templates/feature-matrix.md` | Feature matrix with Y/P/N, 0-3 quality score, evidence_url, and gap-validation block |
| `templates/competitor-signals.py` | Multi-source per-competitor signal collector: HN, GitHub, ProductHunt, Wayback Machine |
