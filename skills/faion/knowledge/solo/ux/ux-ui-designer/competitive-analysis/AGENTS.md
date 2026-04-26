# Competitive Analysis

## Summary

A structured method for examining 3-5 direct competitors, 2-3 indirect, and 1-2 aspirational examples against consistent evaluation criteria (features, user flows, UI patterns, IA, error handling, mobile experience). Output is a feature comparison matrix, per-competitor profiles, and recommendations bucketed into: must-have (table stakes), parity (match), and differentiation (opportunity). Analysis requires actually using the products through key user flows, not just looking at screenshots.

## Why

Designing without competitive context means reinventing existing solutions, missing user expectations set by other products, and failing to see differentiation opportunities. Competitors' UX patterns represent accumulated product decisions — understanding them reveals what users now expect as baseline behavior, what problems are unsolved across the market, and what mistakes to avoid.

## When To Use

- Before a new feature spec is written — understand what exists before designing something that already exists
- Quarterly product reviews — market and competitor UI patterns shift faster than annual reviews capture
- When a stakeholder asks "what do others do?" — answer with evidence, not opinion
- Before a positioning or pricing decision — competitor UX quality is part of the market landscape
- When user research reveals users compare your product to specific competitors — study those products

## When NOT To Use

- As a substitute for user research — tells you what others built, not what users actually need
- When all target competitors are behind closed paywalls inaccessible for legal analysis
- For internal tooling with no external market — no competitors means no competitive analysis
- When the product intentionally defies conventions — conventional analysis anchors you to patterns you're breaking

## Content

| File | What's inside |
|------|---------------|
| `content/01-process.xml` | 6-step process (scope, criteria, gather, document, patterns, insights), competitor type taxonomy, analysis dimensions |
| `content/02-examples.xml` | Worked examples (e-commerce checkout, SaaS onboarding), gap analysis framework, antipatterns (surface-level review, copying without understanding) |

## Templates

| File | Purpose |
|------|---------|
| `templates/analysis-plan.md` | Analysis plan: objective, competitor list (type + rationale), criteria, flows to analyze, deliverables |
| `templates/comparison-matrix.md` | Feature comparison matrix with legend (Yes/No/Partial + ratings) |
| `templates/competitor-profile.md` | Per-competitor profile: overview, target users, key screens, flows, friction points, strengths/weaknesses, opportunities |
| `templates/summary-report.md` | Executive summary report: key findings, industry standards, best practices, opportunities, recommendations (must/should/could/avoid) |
| `templates/scrape-reviews.js` | Node.js script: scrape App Store critical reviews for competitor sentiment analysis |
