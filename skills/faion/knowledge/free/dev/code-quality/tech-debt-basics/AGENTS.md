---
slug: tech-debt-basics
tier: free
group: dev
domain: dev
version: 1.1.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: Produces a 20-30 row TECH_DEBT_REGISTER.md classified by Fowler's quadrant (deliberate-reckless / deliberate-prudent / inadvertent-reckless / inadvertent-prudent) with severity, location, and interest cost.
content_id: "7bfdacf666a1952d"
complexity: light
produces: report
est_tokens: 3000
tags: [tech-debt, fowler-quadrant, debt-register, prioritisation]
---
# Tech Debt Basics

## Summary

**One-sentence:** Builds a capped tech-debt register (≤30 rows) classified by Fowler's quadrant with severity, evidence, and weekly interest cost per row.

**One-paragraph:** Untracked tech debt accrues silently; tracking everything turns the register into a graveyard. This methodology produces a TECH_DEBT_REGISTER.md capped at 20-30 active rows, each carrying: type (Fowler quadrant), severity, file location, evidence link (PR / postmortem), and a weekly interest cost estimate. Agents scan to surface candidates; humans approve before adding. Register is reviewed monthly: items past 90 days without action are escalated or closed.

**Ефективно для:**

- Команди, що 'знають що в нас борг', але не можуть назвати топ-3.
- Quarterly planning: register дає reasoning 'що рефакторити' замість gut feel.
- Onboarding senior: register показує 'тут небезпеки' за 5 хв замість трьох тижнів.
- AI-driven scan: агент пропонує кандидатів, людина approves.

## Applies If (ALL must hold)

- Codebase is &gt;6 months old.
- Team has authority to schedule refactor time.
- An owner is willing to maintain the register monthly.

## Skip If (ANY kills it)

- Pre-product-market-fit prototype — debt is mostly intentional and uniform.
- Codebase is end-of-life — register has no payoff.
- Team already has a working bug-tracker that handles debt — don't duplicate.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Repo + git history | path | git rev-parse |
| Postmortem archive | path or URL | team docs |
| Owner | string | team handbook |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| none | Standalone — no upstream artefacts required. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: register-cap, fowler-quadrant, evidence-link, monthly-review, agent-scan-human-approve | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema for debt register entries | 700 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns: graveyard, unclassified, no-owner | 600 |
| `content/05-examples.xml` | reference | Sample 3-row register | 500 |
| `content/06-decision-tree.xml` | essential | Quadrant picker tree | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scan_candidates` | haiku | Static scan + churn metrics. |
| `classify_quadrant` | sonnet | Per-item Fowler classification. |
| `estimate_interest` | sonnet | Per-item cost estimate. |

## Templates

| File | Purpose |
|------|---------|
| `templates/TECH_DEBT_REGISTER.md` | Skeleton register the team commits to repo |
| `templates/scan-debt.sh` | Shell scan that surfaces candidates |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-tech-debt-basics.py` | Validate register against schema | Before commit |

## Related

- - [[refactoring-patterns]] — register items in 'reckless' quadrant route here for fix.
- - [[code-decomposition-principles]] — register often surfaces decomposition candidates.

## Decision tree

See `content/06-decision-tree.xml`. Tree asks: was the debt incurred deliberately? was the team aware of the consequence? Combines the two into the four Fowler quadrants; each quadrant routes to a recommended action (refactor / accept / educate / monitor).
