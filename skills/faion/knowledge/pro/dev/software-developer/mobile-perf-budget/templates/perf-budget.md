<!-- purpose: Human-readable budget doc with rationale + change process -->
<!-- consumes: see content/02-output-contract.xml inputs -->
<!-- produces: artefact conforming to content/02-output-contract.xml -->
<!-- depends-on: content/01-core-rules.xml -->
<!-- token-budget-impact: ~300 tokens when loaded as context -->

# Mobile Performance Budget

Validated in CI via Lighthouse CI on the **mobile** preset (Slow 4G + 4x CPU). PRs exceeding budget fail the build.

## Per-route budgets

| Route | LCP | INP | CLS | Total | JS gz | Image |
|-------|-----|-----|-----|-------|-------|-------|
| `/` | 2500ms | 200ms | 0.1 | 1500KB | 200KB | 800KB |
| `/product/[slug]` | 2500ms | 200ms | 0.1 | 1500KB | 180KB | 900KB |
| `/checkout` | 2200ms | 150ms | 0.05 | 900KB | 120KB | n/a |

## Process

1. Every PR runs `lhci autorun` against the three routes.
2. PR comment shows diff vs main; build fails if any threshold exceeded.
3. To request a budget increase, open a Notion ticket with: rationale, business impact, target metric, mitigations attempted.
4. Quarterly review: compile CrUX p75 + adjust budgets with written rationale.

## Review log

- {{2026-Q1}}: initial budget set.
- {{2026-Q2}}: /product image budget raised 800→900KB; rationale: video preview feature.
