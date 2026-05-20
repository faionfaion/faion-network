---
slug: sprint-capacity-from-complexity-tags
tier: geek
group: sdd
domain: sdd
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-network]
summary: Time-estimate-free sprint capacity model that allocates a bi-weekly sprint slot budget from per-task complexity tags (XS/S/M/L/XL) and token-cost estimates, calibrated by a rolling completion ratio.
content_id: "a6ddc08c59e21743"
tags: [sdd, sprint-planning, capacity, complexity-tags, no-time-estimate, p6-product-dev-team]
---
# Sprint Capacity From Complexity Tags

## Summary

**One-sentence:** A sprint capacity model that takes per-task complexity tags (XS/S/M/L/XL) and token estimates, applies a rolling completion factor per developer, and emits a sprint slot budget — no hours, no story points, no time estimates.

**One-paragraph:** Faion bans time estimates in SDD work, which kills the usual sprint capacity math (velocity in story points / hours per developer). This methodology replaces it with a complexity-tag accounting scheme: every task in `tasks/todo/` carries a `complexity: XS|S|M|L|XL` tag and a `est_tokens` field. Each tag maps to a fixed slot weight (XS=1, S=2, M=3, L=5, XL=8). Per-developer capacity is computed from the prior 3 sprints' completion ratio (slots completed / slots committed) — a calibration constant, not a forecast. The output is a sprint commitment in slots, not hours. Sponsors and PMs get predictability without anyone lying about durations.

## Applies If (ALL must hold)

- Team uses SDD with `tasks/todo/TASK_*.md` files containing `complexity` and `est_tokens` frontmatter.
- Sprint cadence is fixed (typically bi-weekly).
- Team has at least 3 completed sprints of historical data per developer (or 1 sprint with explicit cold-start factor).
- Team has agreed to ban time estimates per the faion-network constitution.

## Skip If (ANY kills it)

- Team still uses hours or story-point velocity — adopt that workflow's playbook instead, do not run both.
- No SDD task files exist; tasks live only in Jira/Linear without `complexity` tags.
- Solo developer with no team coordination need — use `tiny-bets-quarterly-cadence` instead.
- Fewer than 3 sprints of history AND team unwilling to set a cold-start factor — capacity is not predictable enough.

## Prerequisites

- `tasks/todo/TASK_*.md` files for the candidate sprint, each with `complexity` and `est_tokens` frontmatter.
- Prior 3 sprints' completion log (slots committed vs slots completed per developer).
- Per-developer slot budget anchor (default: 10 slots per bi-weekly sprint at 100% completion factor).

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/sdd/sdd/` | SDD lifecycle and task frontmatter conventions. |
| `geek/sdd/definition-of-done-multi-role` | "Done" semantics that close out a slot. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Five rules for tag-to-slot mapping, rolling completion factor, and sprint commitment ceiling. | ~900 |

## Related

- parent skill: `geek/sdd/`
- peer: `definition-of-done-multi-role`, `pm-tech-lead-grooming-agenda`, `tech-debt-slot-quota-policy`
- external: faion-network constitution — "No Time Estimates" section
