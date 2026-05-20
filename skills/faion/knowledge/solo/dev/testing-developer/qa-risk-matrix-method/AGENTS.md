---
slug: qa-risk-matrix-method
tier: solo
group: dev
domain: testing-developer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "e69cf9d1a77d38f4"
summary: A maintained QA risk matrix that scores every product area on impact × likelihood, drives test-investment allocation (unit / integration / e2e / exploratory), and updates per release so testing strategy stays in sync with what is actually risky.
tags: [risk-based-testing, qa, test-strategy, risk-matrix, prioritization]
---

# QA Risk Matrix Method

## Summary

**One-sentence:** Maintain a 2-dimensional risk matrix (impact × likelihood) per product area, score it before every release cycle, and use the scores to allocate test-investment across unit / integration / e2e / exploratory — replacing "test everything equally" with explicit, defensible priorities.

**One-paragraph:** Risk-based testing is the meta-decision that drives every other QA choice (where unit-test depth, where to invest in e2e, where to schedule exploratory sessions, what to leave to monitoring). Faion has no methodology for building and maintaining the risk matrix itself. Mechanism: enumerate product areas at a useful granularity (typically 8-20 areas — auth, billing, search, onboarding, search, etc.), score each on impact (customer-money-or-trust at stake if it breaks) and likelihood (frequency of change × complexity × novelty), produce a heatmap, then map the four quadrants to four test-investment patterns (heavy automation + exploratory, automation only, light, monitor-only). Update the matrix before every release cycle. Primary output: a `risk-matrix.yaml` per project plus a quarterly heatmap + investment plan posted to the team channel.

## Applies If (ALL must hold)

- product has ≥ 5 distinct user-facing or business-critical areas
- team has bounded testing capacity (always; the matrix is for allocation)
- there is a release cycle (sprint, monthly, continuous) where investment decisions can be reconsidered
- team can articulate the worst customer-impact for at least 3 product areas without prompts

## Skip If (ANY kills it)

- single-feature product with one user flow — risk is uniform, matrix overhead exceeds benefit
- pre-MVP — risk landscape is unknown, build the matrix after the first 90 days of real usage
- compliance environment where every area is "high risk" by mandate — risk-tier the inside of compliance buckets but defer to the regulator on the outside
- team has no test-investment to allocate (everything is exploratory) — adopt automation first

## Prerequisites

- a list of product areas at consistent granularity (post-MVP product, with a domain model)
- access to recent incident data (which areas have actually broken; how often)
- access to recent change data (commits per area, churn)
- a definition of impact tiers (typically: revenue loss, data loss, customer-trust, regulatory exposure)

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/dev/testing-developer/qa-test-pyramid-vs-trophy-decision` | Risk matrix drives the pyramid-vs-trophy choice per area |
| `solo/dev/testing-developer/qa-exploratory-charter-template` | High-risk areas with high uncertainty get exploratory sessions |
| `pro/infra/devops-engineer/dora-metrics` | Incident data is the load-bearing input |

## Content

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: explicit area enumeration, impact-from-customer-effect, likelihood-data-anchored, quadrant-to-investment map, per-release refresh | ~900 |
| `content/02-output-contract.xml` | essential | risk-matrix.yaml schema, investment-plan schema | ~600 |
| `content/03-failure-modes.xml` | essential | 6 failure modes: all-areas-high, areas-stale, no-refresh, etc. | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `enumerate_product_areas_from_codebase` | sonnet | Bounded extraction from module / route map |
| `propose_impact_score_per_area` | sonnet | Per-area judgment from customer-effect framing |
| `compute_likelihood_from_data` | haiku | Mechanical computation from incident + commit data |
| `generate_investment_plan` | opus | Cross-area synthesis: balance capacity vs risk |

## Templates

| File | Purpose |
|------|---------|
| `templates/risk-matrix.yaml` | Per-area scores with impact / likelihood / quadrant / investment |
| `templates/heatmap.svg` | Render template for the 4-quadrant visualisation |
| `templates/investment-plan.md` | Quarterly investment plan: what each quadrant gets, with rationale |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/likelihood-from-incidents.py` | Reads incident log + git history, computes likelihood scores per area | Pre-quarterly review |
| `scripts/render-heatmap.py` | Generates the heatmap SVG from risk-matrix.yaml | Quarterly review prep |

## Related

- parent skill: `solo/dev/testing-developer/SKILL.md`
- peer methodologies: `solo/dev/testing-developer/qa-test-pyramid-vs-trophy-decision`, `solo/dev/testing-developer/qa-exploratory-charter-template`
- external: [Bach Heuristic Risk-Based Testing (2003)] · [Erik van Veenendaal Risk-Based Testing book (UTN, 2017)] · [ISTQB Foundation Level syllabus, risk-based testing section]
