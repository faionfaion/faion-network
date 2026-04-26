# Feature Prioritization (MoSCoW)

## Summary

Categorical prioritization technique that sorts requirements into Must Have (non-negotiable, ~60% effort), Should Have (important with workarounds, ~20%), Could Have (nice-to-have, ~20%), and Won't Have (explicitly out of scope for this release). Requires a fixed timebox and capacity number before categorization begins. Changing a Must post-lock requires explicit human escalation.

## Why

When every requirement is "high priority" — the default state without a shared vocabulary — teams cannot make trade-off decisions during planning, scope creep follows every sprint, and stakeholders argue instead of align. MoSCoW provides the shared vocabulary: four categories with crisp definitions and a capacity math check (Must + Should must not exceed 80% of capacity). The Won't Have category is the most valuable — it prevents scope creep by making exclusions explicit.

## When To Use

- Fixed-timebox release (sprint, MVP, launch deadline) where the question is "what fits and what gets cut".
- Stakeholder alignment workshop where the deliverable is a shared shortlist, not a numerical score.
- Pre-sales or contract-bound deliverables where Won't-Have must be documented to prevent scope creep.
- Pairing with MVP-scoping: MoSCoW gives the categorical lens, MVP-scoping gives the buildable cut.

## When NOT To Use

- Continuous backlog ranking across many items — RICE/WSJF give finer-grained sequence.
- Strategic portfolio decisions across multiple products — MoSCoW lacks effort math.
- Fast iteration / shipping daily — the ceremony cost is too high for sub-week cycles.

## Content

| File | What's inside |
|------|---------------|
| `content/01-moscow-categories.xml` | Four category definitions, test questions per category, effort proportion targets, and the locking rule. |
| `content/02-moscow-process.xml` | 6-step process, capacity validation rule, stakeholder alignment, agent workflow, prompt patterns, and gotchas. |

## Templates

| File | Purpose |
|------|---------|
| `templates/moscow-matrix.md` | Full release matrix: context, Must/Should/Could/Won't tables with effort per row, summary totals. |
| `templates/moscow-discussion-guide.md` | Single-requirement debate template: proposed category, arguments for each, questions to resolve, final decision. |

## Scripts

| File | Purpose |
|------|---------|
| `scripts/moscow-check.py` | Validates 60/20/20 budget split from JSON input; reports violations when Must is over/under-allocated. |
