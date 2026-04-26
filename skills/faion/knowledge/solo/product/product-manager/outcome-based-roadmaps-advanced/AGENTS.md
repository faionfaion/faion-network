# Outcome-Based Roadmaps Advanced

## Summary

Decompose a top-line business goal into 2-4 product outcomes, each with a leading indicator measurable within 4 weeks, a confidence level (low/med/high) backed by evidence, and 2-3 candidate experiments. Maintain one source-of-truth roadmap, then generate four audience views from it: theme-based (customers, no dates), outcome-metric (board, quarterly targets), outcome-plus-options (engineering, sprint-level when known), and problem-solution (sales, only confirmed items get timing). Confidence inflation — defaulting to "medium" without evidence — is the primary failure mode.

## Why

Stakeholders who demand feature timelines despite an outcome-first culture are solving a communication problem, not a roadmap-format problem. Audience-tailored views from a single source of truth provide the narrative each audience needs without creating four diverging documents. Breaking a business goal into product outcomes with leading indicators is the highest-leverage PM skill for 2026: it forces explicit evidence requirements and surfaced "what we still need to learn" before committing to solutions.

## When To Use

- Stakeholders keep demanding feature timelines; you need audience-tailored views per cohort (board, sales, eng, customers).
- Translating a top-line business goal into a tree of product outcomes with leading indicators.
- Quarterly re-planning where confidence levels shift and the same roadmap must be presented to different audiences.
- A PM transitioning from feature owner to "architect of impact" who needs scaffolding for the new role.

## When NOT To Use

- Early-stage product (pre-PMF) where outcomes are unstable and discovery dominates — use a "now/next/later" theme list.
- Single-stakeholder context (just you and your co-founder) — the audience-matrix overhead has zero ROI.
- Enterprise with hard-deadline contractual commitments — use a hybrid (outcome theme plus dated milestones).
- Org with no metrics infrastructure — you cannot operate confidence levels without measurement.

## Content

| File | What's inside |
|------|---------------|
| `content/01-decomposition.xml` | Goal-to-outcome decomposition rules, leading indicator requirements, confidence levels, and audience view rules. |
| `content/02-antipatterns.xml` | Confidence inflation, outcome count explosion, view drift from source, and sales over-commitment. |

## Templates

| File | Purpose |
|------|---------|
| `templates/validate-outcome-tree.py` | Python validator: fails outcomes missing leading indicators, high confidence without evidence, or fewer than 2 experiments. |
