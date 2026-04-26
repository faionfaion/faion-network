# Competitor Analysis

## Summary

A 5-step framework for systematically studying businesses competing for the same customers: identify (direct / indirect / future), map on a positioning matrix, analyse across 8 dimensions, find gaps, then define differentiation. Output is `competitive-analysis.md` in `.aidocs/product_docs/`.

## Why

Entrepreneurs either ignore competitors ("we're unique") or copy them without strategy. Without a structured competitive scan you miss indirect competitors, build table-stakes features instead of differentiators, and produce pricing that fits no segment well. A gap-driven analysis converts a competitor landscape into a concrete positioning statement and feature roadmap.

## When To Use

- Pre-MVP: 5-10 candidate competitors identified, need structured scan before committing engineering time.
- Positioning sprint: landing page or pricing rewrite requiring a defensible differentiation statement.
- New feature greenlight: comparing how 3-7 incumbents implement a feature you plan to build.
- Quarterly market refresh: re-scoring known competitors on price, features, and traction.
- Investor / pitch deck: building a credible competitor matrix slide with named gaps.

## When NOT To Use

- Deep customer-pain discovery — competitors are a proxy, not a substitute for user interviews; use `pain-points` or `problem-validation` first.
- Pure brainstorming with no category defined yet — run `idea-generation-methods` first.
- Regulated / B2B-enterprise procurement where pricing is hidden behind sales — agents will hallucinate numbers.
- Real-time monitoring of a single competitor — use a change-tracking service (Visualping), not a one-shot agent run.
- "Should we build this?" gut checks — competitor count alone does not answer that.

## Content

| File | What's inside |
|------|---------------|
| `content/01-framework.xml` | 5-step analysis process with rules, the positioning matrix, and 8-dimension analysis table |
| `content/02-examples.xml` | Worked examples: note-taking app, email marketing; common mistakes table |
| `content/03-gotchas.xml` | Agent gotchas: hallucinated funding, pricing-page footnotes, stale data, context overflow |

## Templates

| File | Purpose |
|------|---------|
| `templates/competitor-report.md` | Full analysis report skeleton (market overview, per-competitor deep dive, gap analysis, differentiation) |
| `templates/competitor-snapshot.md` | Quick single-competitor snapshot template for fan-out sub-tasks |
| `templates/scrape-competitor.sh` | Bash scraper: fetches homepage, pricing page, G2, Wayback for one competitor |
