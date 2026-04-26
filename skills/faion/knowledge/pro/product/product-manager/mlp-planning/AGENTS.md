# MLP Planning

## Summary

Minimum Lovable Product planning: a four-layer audit framework (Functional → Reliable → Usable → Delightful) for evolving an MVP that users find "fine" into one they love and recommend. The process identifies delight gaps by clustering feedback where the core job is done but the emotion is missing, then generates a polish backlog ranked by Pain × Frequency × Visibility. MLP threshold: all core features score 4+ on all four layers.

## Why

MVP validates the core assumption but often fails to retain users in crowded categories where competitors already clear the "viable" bar. Users leave not because the product doesn't work, but because it lacks emotional connection. Adding delight (speed, simplicity, personality, anticipation, celebration) on top of a working foundation is the lowest-CAC retention investment because it converts activation to word-of-mouth.

## When To Use

- MVP shipped with measurable activation but Day-30 retention plateaus below 25-30%.
- NPS &lt; 30 or churn surveys show users finish the core job but describe the product as "fine" or "okay."
- Retention curve flattens after week 2 — function works, emotion missing.
- About to enter a paid acquisition phase: every dollar spent on a non-lovable product compounds CAC waste.
- Pre-launch in a category where competitors already cleared the "viable" bar.
- Refactor or redesign sprint with explicit budget for polish, copy, micro-interactions.

## When NOT To Use

- Pre-MVP — there is nothing to make lovable yet. Use `mvp-scoping` or `minimum-product-frameworks` first.
- Product-market fit not validated — adding delight before demand signal hides the real problem.
- Infrastructure or B2B plumbing where users only interact via API — delight surface is too small.
- Capacity-constrained team mid-incident — Layer 1 and 2 regressions trump delight work.
- Hard-deadline compliance or regulatory features — polish budget is zero until shipped.

## Content

| File | What's inside |
|------|---------------|
| `content/01-framework.xml` | Four-layer model, MVP vs. MLP comparison, delight categories, polish priority formula, five-step planning process. |
| `content/02-examples.xml` | Note-taking app and invoicing tool MVP-to-MLP transformations with before/after tables and retention outcomes. |

## Templates

| File | Purpose |
|------|---------|
| `templates/mlp-plan.md` | Full MLP planning document: current state, goal, feature audit, delight opportunities, polish backlog, completion criteria, measurement plan. |
| `templates/delight-sprint.md` | Single-workflow delight sprint: scope, current experience, target experience, tasks, success criteria. |
| `templates/audit-to-backlog.sh` | Bash: converts mlp-gap-finder JSON audit output into Linear issues with Pain×Freq×Vis priority scores. |

## Scripts

| File | Purpose |
|------|---------|
| `scripts/audit-to-backlog.sh` | Filters features scoring below 4 on usability or delight; creates Linear issues via GraphQL API. |
