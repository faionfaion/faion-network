# Feature Prioritization (RICE)

## Summary

Quantitative scoring model that ranks features by `(Reach × Impact × Confidence) / Effort`. Reach is users per quarter from analytics; Impact uses a fixed 5-point scale (3/2/1/0.5/0.25); Confidence is capped at 50% without cited evidence; Effort is total person-months including design, dev, QA, and docs. Higher score = higher priority. Re-score quarterly; archive prior scoring files with date stamps.

## Why

Feature prioritization driven by gut feeling or the HiPPO (Highest Paid Person's Opinion) produces inconsistent, unstable roadmaps. RICE replaces negotiation with a shared math artifact: every stakeholder can challenge the inputs, but the formula is neutral. The Effort denominator corrects for scope creep — large high-impact features that take a quarter still lose to small quick wins that unlock the same users.

## When To Use

- Backlog has 10+ candidates needing an objective, repeatable rank for the next quarter or release.
- Stakeholders disagree on priority and you need a math-based artifact to defuse HiPPO.
- A subagent drafts a roadmap from a raw idea list and needs a defensible default ordering.
- You have at least funnel/MAU data plus an effort estimate per item.

## When NOT To Use

- Single-feature decisions — RICE adds noise versus a one-liner rationale.
- Pre-PMF / 0-to-1 products where Reach is unknowable — use opportunity solution trees or Kano.
- Compliance, security, or contractual must-haves — they bypass RICE and go straight into the plan.
- Cross-portfolio bets where strategic fit dominates the score (RICE has no strategy term).

## Content

| File | What's inside |
|------|---------------|
| `content/01-rice-formula.xml` | Formula definition, factor scales (R/I/C/E), calculation example, scoring process, and constraints. |
| `content/02-rice-examples.xml` | Two worked examples (e-commerce, SaaS dashboard), antipatterns, and agent gotchas. |

## Templates

| File | Purpose |
|------|---------|
| `templates/rice-scoring-table.md` | Multi-feature scoring table with R/I/C/E columns, RICE score, rank, and per-feature notes. |
| `templates/rice-decision-record.md` | Single-feature record: factor scores with rationale, calculation, rank, decision, dependencies, strategic alignment. |

## Scripts

| File | Purpose |
|------|---------|
| `scripts/rice.py` | Minimal Python scorer: reads JSON list with reach/impact/confidence/effort fields, computes scores, returns ranked output. |
