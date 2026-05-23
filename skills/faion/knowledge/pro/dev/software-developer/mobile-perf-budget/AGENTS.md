---
slug: mobile-perf-budget
tier: pro
group: dev
domain: dev
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Establish a per-route mobile performance budget covering bundle size, LCP/INP/CLS, image weight, and JS execution time — enforced in CI.
content_id: "482a8c46550d7d25"
complexity: medium
produces: spec
est_tokens: 5200
tags: [mobile, performance, budget, lighthouse, core-web-vitals]
---
# Mobile Performance Budget

## Summary

**One-sentence:** Establish a per-route mobile performance budget covering bundle size, LCP/INP/CLS, image weight, and JS execution time — enforced in CI.

**One-paragraph:** Mobile perf is a budget, not a hope. Define a per-route budget for: total transfer size, gzipped JS size, Largest Contentful Paint, Interaction-to-Next-Paint, Cumulative Layout Shift, image weight, and main-thread blocking time. Enforce in CI via Lighthouse CI / WebPageTest / bundle-size action. Regressions block merges; budgets adjust quarterly with explicit rationale. Without a budget, every PR slowly degrades the experience.

**Ефективно для:**

- Greenfield SPA / SSR / native mobile проєкти з expected scale (organic traffic, paid acquisition).
- Refactor існуючих сайтів які почали втрачати конверсію через slow LCP.
- Visible CI gates — щоб ніхто не прокачав 800 KB JS у нормі.
- Quarterly perf review: тренди + rationale за зміни в budget.

## Applies If (ALL must hold)

- Product served to mobile users on cellular connections (>20% mobile traffic).
- Conversion / engagement / SEO ranking is meaningful to the business.
- CI/CD pipeline has a step where Lighthouse / WebPageTest can run.
- Frontend stack supports bundle analysis (webpack-bundle-analyzer, Rollup visualizer).

## Skip If (ANY kills it)

- Internal admin tool with <50 users on desktop — budget is overhead.
- Native app released only on a fixed device profile — different methodology.
- PoC / throwaway project with no production lifetime — perf gates slow iteration.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Route inventory | URL list | router config |
| Current metrics | Lighthouse / RUM baseline | WebPageTest / CrUX |
| Business KPI | conversion / bounce / SEO position | product/marketing |

## Assumes Loaded

none — methodology is self-contained.

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: budget-per-route, core-web-vitals-included, ci-enforcement, mobile-3g-baseline, quarterly-review | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for spec + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix | 900 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | 900 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `measure-baseline` | sonnet | Templated Lighthouse run + parse. |
| `set-budgets` | opus | Business-tradeoff judgment per route. |
| `lint-budget-file` | haiku | Mechanical schema check. |

## Templates

| File | Purpose |
|------|---------|
| `templates/budgets.json` | Lighthouse CI budgets.json for per-route thresholds |
| `templates/lhci-config.json` | Lighthouse CI config wiring mobile preset + budgets |
| `templates/perf-budget.md` | Human-readable budget doc with rationale + change process |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-mobile-perf-budget.py` | Validate the budget artefact against the schema | Pre-commit + CI |

## Related

- [[api-monitoring-metrics]]
- [[microservices-observability]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, stack, runtime, scale, etc.) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
