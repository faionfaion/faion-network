# Risk Assessment

## Summary

A structured 5-category (market/product/team/financial/operational) risk identification
and scoring process using probability x impact matrices. Each risk gets one owner,
one measurable trigger, and a concrete mitigation action (not "monitor + diversify").
Run as a multi-pass agent pipeline: enumerate → red-team pre-mortem → score → human
review → convert high-priority risks into SDD tasks.

## Why

Entrepreneurs are either blindly optimistic or paralyzed by fear because there is
no structured process for identifying and managing business risks. H/M/L scoring is
useful only for relative ranking — absolute probabilities are wrong by an order of
magnitude. The pre-mortem template is the highest-leverage artifact: a 30-minute
exercise surfaces omissions that a solo risk review misses due to optimism bias.

## When To Use

- Pre-launch go/no-go review for a new product, feature, or market entry
- Investor or due-diligence ask requiring a credible risk register plus mitigations
- Quarterly business review where assumptions need re-validation
- After a near-miss incident — formalizing what almost killed the business
- Pivot decision comparing risk profiles of two strategic options
- New regulatory exposure appears on the roadmap (GDPR, AI Act, SOC2, payment rails)

## When NOT To Use

- Idea-stage with fewer than 3 customer conversations — risk theater is procrastination
- Tactical sprint planning — use an issue tracker, not a risk register
- One-person side projects with under $1k at stake — overhead exceeds value
- When the team will not assign owners or revisit monthly — a static register is worse than none

## Content

| File | What's inside |
|------|---------------|
| `content/01-framework.xml` | 5 risk categories, prob x impact scoring, response strategies |
| `content/02-agentic-patterns.xml` | Multi-pass pipeline, prompt patterns, gotchas |
| `content/03-examples.xml` | SaaS startup and content business risk register examples |

## Templates

none

## Scripts

| File | Purpose |
|------|---------|
| `scripts/riskreg.sh` | Sort risk register by score, lint missing fields and mitigations |
