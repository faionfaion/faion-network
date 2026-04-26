# Competitive Positioning

## Summary

Competitive positioning defines how a product is uniquely valuable compared to alternatives —
answering "why should customers choose us?" using April Dunford's six-step framework: competitive
alternatives → unique attributes → value translation → best-fit customer → market category →
positioning statement. The output is a `positioning-canvas.md` and a one-page
`positioning-statement.md`. Cap unique attributes at 3; every attribute must have a time-to-copy
estimate; every value benefit must terminate in a measurable outcome.

## Why

Products that position as "like X but better" compete on features and lose to incumbents with
larger teams. Dunford's framework finds what is genuinely different — not superior — and binds
it to the customer who cares most. Without this, PMs default to comparative language ("faster",
"easier") that is both unprovable and easily matched. Positioning done once and versioned in git
prevents the drift that happens when landing page, pricing page, and sales deck each drift
independently.

## When To Use

- Pre-launch positioning sprint: product exists, 3–7 named alternatives exist, landing page
  is next
- Repositioning after a pivot or pricing change where existing copy no longer matches
- New segment entry: same product, new ICP, parallel positioning canvas needed
- Pitch deck "why us, why now" slide
- Category-creation decision: joining existing category vs. naming a new one
- Quarterly positioning audit to verify unique attributes are still defensible

## When NOT To Use

- Before competitor analysis exists — the canvas consumes `competitor-analysis.md`; without it
  the canvas is fiction
- Before 5–10 user interviews — "best-fit customer" cannot be filled honestly without discovery
- Pure copywriting / headline polish — that is landing-page-design, not positioning
- Internal tools, side projects, or anything with a single user
- B2B-enterprise positioning requiring analyst relations (Gartner, Forrester) — agents lack the
  relationships and the data

## Content

| File | What's inside |
|------|---------------|
| `content/01-framework.xml` | Dunford six-step process, positioning strategies, common mistakes |
| `content/02-examples.xml` | Two worked examples (project-management tool, email platform) |
| `content/03-agent-usage.xml` | Orchestrator pattern, value-laddering fan-out, gotchas |

## Templates

| File | Purpose |
|------|---------|
| `templates/positioning-canvas.md` | Positioning canvas: alternatives, attributes, value, customer, category, statement |
| `templates/positioning-lint.sh` | Linter: flags comparative language, checks six-clause statement structure |
