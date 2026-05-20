---
slug: performance-budget-design
tier: pro
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Performance budgets (Core Web Vitals, p95 latency, payload size, cold-start) wired as CI gates with reasoned thresholds — what QA engineers own in P6 product teams.
content_id: "149160a4c239cb81"
tags: [performance-budget-design, dev, pro]
---

# Performance Budget Design

## Summary

**One-sentence:** Performance budgets (Core Web Vitals, p95 latency, payload size, cold-start) wired as CI gates with reasoned thresholds — what QA engineers own in P6 product teams.

**One-paragraph:** solo/dev/automation-tooling/perf-test-basics + perf-test-tools exist as tool tutorials; no methodology for setting budgets + CI-gating. Output: budget table + CI gate config + reasoned thresholds.

## Applies If (ALL must hold)

- web product OR API surface with perf SLO
- CI pipeline exists
- team can block merges on perf regressions

## Skip If (ANY kills it)

- internal tools with no users — budgets are theater
- research / experimentation phase — premature optimization
- team lacks CI maturity — set up CI first

## Prerequisites

- current Core Web Vitals or API latency baseline
- CI tool (GitHub Actions, GitLab CI, Buildkite, CircleCI)
- perf measurement tool (Lighthouse CI, WebPageTest, Datadog Synthetics)

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/dev/backend-systems` | parent skill — provides operating context for this methodology |
| `pro/dev/perf-test-basics` | peer methodology — produces inputs or consumes outputs |
| `pro/dev/perf-test-tools` | peer methodology — produces inputs or consumes outputs |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules | ~900 |
| `content/02-output-contract.xml` | essential | required fields, forbidden patterns, allowed transformations | ~700 |
| `content/03-failure-modes.xml` | essential | 5 failure modes with detector + repair | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft_inputs_summary` | haiku | template fill, bounded transformation |
| `synthesize_decision` | sonnet | per-instance judgment; bounded inputs |
| `review_for_compliance` | opus | cross-input synthesis when stakes are high |

## Related

- parent skill: `pro/dev/backend-systems/`
- peer methodology: `pro/dev/perf-test-basics`
- peer methodology: `pro/dev/perf-test-tools`
- peer methodology: `geek/ai/agent-observability-stack-blueprint`
- external: https://web.dev/articles/use-lighthouse-for-performance-budgets; https://web.dev/articles/vitals (CWV)
