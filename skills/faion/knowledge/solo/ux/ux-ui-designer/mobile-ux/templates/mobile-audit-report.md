<!--
purpose: mobile UX audit report skeleton
consumes: mobile build URL or screen inventory + Lighthouse output
produces: a mobile-ux artefact validating against scripts/validate-mobile-ux.py
depends-on: content/01-core-rules.xml, content/02-output-contract.xml
token-budget-impact: ~600-1500 tokens once filled
-->
# Mobile UX Audit: [Product / Surface]

**Date:** [YYYY-MM-DD]
**Reviewer:** [Name <email>]
**Platforms:** iOS / Android / web
**Build URL:** [url]
**Lighthouse run:** [path / timestamp]

## Core Web Vitals

| Metric | Observed | Threshold | Verdict |
|--------|----------|-----------|---------|
| LCP | [s] | < 2.5s | pass/fail |
| FID | [ms] | < 100ms | pass/fail |
| CLS | [score] | < 0.1 | pass/fail |
| TTI | [s] | < 5s | pass/fail |

## Findings

| Screen | Element | Category | Observed | Threshold | Platform | Fix direction |
|--------|---------|----------|----------|-----------|----------|---------------|
| [route] | [element] | touch-target / thumb-zone / nav-pattern / input-type / vitals / platform | [value] | [value] | iOS / Android / web | [direction] |

## Action items

1. [highest-severity violation → owner → ETA]
2. [...]

## Open questions

- [ambiguous behaviour requiring product owner sign-off]
