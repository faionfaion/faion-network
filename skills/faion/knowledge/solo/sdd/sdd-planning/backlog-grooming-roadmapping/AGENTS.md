# Backlog Grooming & Roadmapping

## Summary

A structured process for prioritizing backlogs (using RICE scoring and MoSCoW categorization) and translating the top-priority items into a Now/Next/Later roadmap. The grooming loop runs weekly (triage new ideas, re-score top 20, refine upcoming items, archive stale entries). Roadmaps are theme-based for solo projects and time-based for teams with committed delivery windows.

## Why

Projects lose direction when feature requests accumulate without systematic triage. Unscored backlogs cause teams to default to recency bias or vocal stakeholder pressure rather than impact-adjusted effort. RICE scoring (Reach × Impact × Confidence / Effort) gives a reproducible ranking signal; combining it with MoSCoW classification ensures the "Must" bucket never exceeds 60% of scope, which is the primary driver of missed milestones.

## When To Use

- Sprint kickoff: need to pick top N items from backlog for next cycle.
- Quarterly planning: produce a theme-based roadmap from raw backlog data.
- Backlog has grown past 20 unscored items.
- Product review: prioritize incoming requests from users or stakeholders.

## When NOT To Use

- Single-task execution sessions where direction is already clear.
- Greenfield projects with no backlog yet — use `spec-requirements` or write the first spec directly.
- When RICE inputs (Reach, Impact, Confidence) are pure guesses with no data — flag as "estimate-needed" and do not rank.
- Real-time stakeholder negotiations — async agent output does not substitute for live discussion.

## Content

| File | What's inside |
|------|---------------|
| `content/01-grooming-process.xml` | Backlog structure (ideas/validated/specified/designed/ready); weekly grooming 4-part process; RICE formula and scoring example; MoSCoW scope percentages. |
| `content/02-roadmap-structure.xml` | Time-based vs theme-based roadmap tradeoffs; Now/Next/Later structure with confidence levels; quarterly roadmap example; antipatterns (too many P0s, roadmap as commitment). |

## Templates

| File | Purpose |
|------|---------|
| `templates/backlog-item.md` | Backlog item skeleton with RICE score table, MoSCoW checkboxes, dependencies, and next steps. |
| `templates/grooming-session.md` | Grooming session record: ideas reviewed, priority changes, items refined, archived, next sprint candidates. |
| `templates/roadmap.md` | Product roadmap skeleton with Now/Next/Later sections, "Not Planned" list, dependencies, change log. |
| `templates/gh-backlog-export.sh` | Bash script: exports GitHub Issues labeled "backlog" to RICE-ready CSV using gh CLI and jq. |
