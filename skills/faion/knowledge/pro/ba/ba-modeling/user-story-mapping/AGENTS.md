# User Story Mapping

## Summary

Arranges user stories along two dimensions: horizontal (user journey activities and tasks in narrative verb-phrases) and vertical (priority from essential to nice-to-have). The result shows the complete user experience and enables release slicing into a walking skeleton (R1) plus enhancement releases. Map lives as YAML-in-git; renderers produce Markdown, Mermaid, and Miro outputs from that single source.

## Why

A flat backlog has no journey context: release planning is arbitrary, important stories get lost, and the UX is fragmented because no one can see what a complete experience looks like. Story mapping forces a backbone (activities) before stories, and forces release lines (capacity-feasibility checked) before sprint planning. The walking skeleton discipline ensures R1 delivers a degraded-but-complete user journey rather than half of one activity done perfectly.

## When To Use

- Flat backlog of 50-500 items with no journey context — agents reverse-engineer activities from titles.
- New product or module kick-off with personas and goals but no scope yet.
- Release planning for a 3-6 month roadmap that needs a walking-skeleton cut with thin-slice defense.
- Migration or replatforming — current journey mapped first, target journey overlaid to surface gaps.
- Stakeholder workshop prep — agents pre-populate a draft map so the workshop debates cuts, not vocabulary.
- Auditing an existing Jira backlog for journey coverage gaps.

## When NOT To Use

- Single-feature work (one screen, one form) — write 3 stories with AC and ship; mapping overhead exceeds value.
- Pure platform / API-only services with no end-user journey — use `interface-analysis` and `use-case-modeling`.
- Hard-deadline regulated work where scope is already defined by regulation.
- Pre-PMF zero-to-one where the journey changes weekly — prototype + customer development instead.
- Pure infrastructure / DevOps backlogs — non-user activities do not belong on a story map.

## Content

| File | What's inside |
|------|---------------|
| `content/01-map-structure.xml` | Two-axis structure, backbone/task/story definitions, walking-skeleton contract, vertical slicing vs horizontal slicing rules. |
| `content/02-agentic-workflow.xml` | 6-subagent pipeline (backlog-ingester → persona-resolver → activity-extractor → task-grouper → story-rewriter → release-slicer), model selection rationale, prompt pattern. |
| `content/03-antipatterns.xml` | Activity-as-feature-name, vertical priority collapse, multi-persona merge, stale maps, walking-skeleton inflation, dependency blindness. |

## Templates

| File | Purpose |
|------|---------|
| `templates/map.yaml` | YAML schema for story map: backbone, tasks, stories with release/size/depends_on/enabler fields. |
| `templates/map_to_jira.py` | Syncs map.yaml to Jira: creates epics per activity, stories per leaf, labels per release and task. |
| `templates/prompt-usm.xml` | Structured XML agent prompt covering backbone rules, orphan handling, capacity feasibility, diff-only output. |
