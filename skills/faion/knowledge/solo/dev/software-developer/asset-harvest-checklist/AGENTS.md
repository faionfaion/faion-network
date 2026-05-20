---
slug: asset-harvest-checklist
tier: solo
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "44778df2e57462f8"
summary: An indie-hacker checklist for harvesting reusable assets — code modules, copy, UI components, illustrations — from a sunset product into a starter kit that compounds across the portfolio.
tags: [indie-hacker, sunset, asset-harvest, starter-kit, solo, portfolio]
---
# Asset Harvest Checklist

## Summary

**One-sentence:** A 7-section checklist that an indie hacker runs immediately after sunsetting or pivoting a product — code modules, copy, UI components, illustrations, schema, deploy scripts, infra config — turning the dead product into reusable assets in a portfolio starter kit that compounds across future bets.

**One-paragraph:** When an indie hacker sunsets a product, they typically delete the repo, tell themselves "next time", and start the next bet from scratch. Six months later they realise the auth, billing, email pipeline, landing-page hero, FAQ block, and Stripe webhooks were 80% reusable. This methodology defines the post-sunset harvest pass: a 7-section checklist with what to extract, where to store it (a `~/portfolio/starter-kit/` repo), how to license it, and how to update it when the next bet finds a bug. Output: a `harvest-log.md` per sunset that records what was extracted and where, plus an updated starter-kit repo. Compounds across portfolio bets; the third bet ships in half the time of the first.

## Applies If (ALL must hold)

- Indie hacker is sunsetting OR pivoting OR shutting down a product.
- A `portfolio/starter-kit/` repo exists OR will be created within the harvest window.
- The dead product's code is still accessible (git history, archived repo, dev machine).
- Indie owns the IP (no client-work obligations preventing harvest).

## Skip If (ANY kills it)

- Indie has no plans to ship more products — harvest overhead exceeds the win.
- Code was written for a client / under NDA — extraction violates contract.
- Sunset is litigation-related — preserve evidence; do not edit.
- All assets are already in the starter kit from prior harvests — re-run is unnecessary.

## Prerequisites

- A `portfolio/starter-kit/` repo with directory conventions: `lib/`, `copy/`, `ui/`, `illustrations/`, `schema/`, `deploy/`, `infra/`.
- An SPDX license declaration in the starter kit (typically MIT or proprietary).
- A `harvest-log.md` template in the starter kit.
- A 1-2 day time window to do the harvest before context decays.

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/dev/software-developer/personal-portfolio-discipline` (or equivalent) | Background on indie-hacker portfolio mindset. |
| `solo/dev/software-developer/code-extraction-patterns` (or equivalent) | How to lift a module out of a project. |
| `solo/dev/software-developer/license-discipline-for-solos` (if exists) | License hygiene for reused assets. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: harvest within 14 days, license declared, no client code, schema before code, log every extraction | ~1100 |
| `content/02-output-contract.xml` | essential | Starter-kit layout, harvest-log fields, asset metadata | ~800 |
| `content/03-failure-modes.xml` | essential | 6 failure modes: stale harvest, license drift, accidental client code | ~1000 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `extract-module-candidates` | sonnet | Bounded judgement: which modules generalise vs which are bet-specific |
| `copy-extract-and-anonymise` | haiku | Mechanical: strip product names, leave structure |
| `license-check` | haiku | Mechanical: confirm SPDX header per file |
| `log-entry-compose` | haiku | Structured log fill |

## Templates

| File | Purpose |
|------|---------|
| `templates/starter-kit-layout.md` | Directory conventions and intended contents per folder |
| `templates/harvest-log.md` | Per-sunset harvest log template |
| `templates/asset-metadata.json` | Per-asset metadata schema (license, origin, version, generalisation level) |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/scan-source.py` | Walk the sunset repo; emit candidate extraction list per section | Day 1 of harvest |
| `scripts/license-scrub.sh` | Add SPDX headers, replace product names, confirm authorship | Per extracted asset |

## Related

- parent skill: `solo/dev/software-developer/`
- peer methodologies: `personal-portfolio-discipline`, `code-extraction-patterns`, `multi-product-portfolio-rotation`
- external: [Pieter Levels portfolio approach](https://twitter.com/levelsio) · [Arvid Kahl on portfolio compounding](https://embeddedentrepreneur.com/) · [SPDX license list](https://spdx.org/licenses/)
