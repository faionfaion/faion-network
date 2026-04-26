# Backlog Management

## Summary

Maintain a prioritized, healthy list of work connected to product goals using the DEEP principle (Detailed at top, Emergent at bottom, Estimated, Prioritized) and four buckets: Ready, Upcoming, Backlog, Icebox. Every item must have a type tag (feature/bug/tech_debt/research), a user story in As-a/I-want/So-that format, and Given/When/Then acceptance criteria before it can enter the Ready bucket. Run weekly grooming; archive items with 180+ days of inactivity.

## Why

Backlogs become dumping grounds when treated as storage rather than strategic tools. Without type tags and explicit promotion criteria, every item looks equal and planning degrades into opinion contests. The 180-day archive rule and the 2-sprint cap on Ready items keep the signal-to-noise ratio high and prevent refinement work from being wasted on low-probability items.

## When To Use

- Backlog has crossed ~80 items and signal is degrading; weekly grooming has lapsed.
- Multiple input streams (support, sales, eng, ideas) need triaging into a single ranked list.
- Refining the top of backlog into Ready items before sprint planning.
- Auditing backlog health (DEEP/INVEST compliance) before a quarterly review.

## When NOT To Use

- Pre-PMF prototype phase with fewer than 20 items — a simple Trello/Notion list is sufficient.
- One-off project with fixed scope and end date — use a WBS or kanban board instead.
- When the team will not run weekly grooming; an unmaintained managed backlog is a longer dumping ground.
- Replacing prioritization frameworks — backlog management organizes items; RICE/MoSCoW prioritizes them. Run prioritization first.

## Content

| File | What's inside |
|------|---------------|
| `content/01-principles.xml` | DEEP/INVEST rules, bucket definitions, and item quality criteria. |
| `content/02-process.xml` | Five-step management process (capture, groom, prioritize, refine, cleanup) with antipatterns. |

## Templates

| File | Purpose |
|------|---------|
| `templates/health-check.md` | Backlog health check: snapshot, counts by status and type, health metrics table, actions. |
| `templates/grooming-agenda.md` | Weekly grooming session agenda with triage table, refinement section, and cleanup log. |
| `templates/backlog-item.md` | Full backlog item template with story, Given/When/Then criteria, estimate, and priority. |
| `templates/validate-backlog.py` | Python linter: checks ready items for AC, size, and INVEST shape; flags stale ratio. |
