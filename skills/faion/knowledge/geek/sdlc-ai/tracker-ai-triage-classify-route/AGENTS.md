# AI Triage, Classify, and Route Inbound Issues

## Summary

Pipe every inbound bug or request through a six-step triage agent before any human picks it up: classify type (bug/story/epic/task/spike), score severity with an attached SLA timer (blocker/critical/major/minor), dedupe against the last 1000 issues by title+body cosine similarity, apply `/area/*`, `/component/*`, `/lang/*` labels, route to the CODEOWNERS-derived team, and assign to the least-loaded engineer on that team. Severity = blocker MUST require an on-call confirmation before the SLA timer arms; everything else is auto-routed. The agent emits a single comment listing every classification it applied so the assignee can dispute any field with one reaction.

## Why

April 2026 reports from Linear's Triage Intelligence, Atlassian's AI Backlog, and bug-triage vendor case studies converge on the same finding: manual triage is the bottleneck above roughly 50 inbound issues per week, and bug-classification BERT-class models plus historical assignment data hit accuracy high enough to remove the manual step on everything except blockers. The mechanism is that classification, dedupe, and routing are independently cheap signals — running them all on the same input compresses minutes of human time per issue into seconds, and the single transparency comment lets the receiving engineer reject any field cheaper than re-triaging from scratch. Skipping the dedupe step is the most common failure mode and produces duplicate work the agent itself authored.

## When To Use

- High-volume inbound queues over ~50 issues per week where manual triage is the documented bottleneck.
- Linear's Triage Intelligence or Jira's AI Backlog can be the drop-in implementation rather than a custom build.
- Multi-team monorepos that already maintain CODEOWNERS — routing piggybacks on the same matrix.
- Teams with at least three months of historical issue + assignment data so the routing model has a non-cold-start.

## When NOT To Use

- Small teams (under five engineers) where the cost of triage agent setup exceeds manual work.
- Domains where misclassification has security or legal consequences without specialist review.
- Cold-start projects: under three months of history yields routing accuracy too low to act on without human review.
- Single-repo solo projects — every issue is self-routed by definition.

## Content

| File | What's inside |
|------|---------------|
| `content/01-six-step-pipeline.xml` | Mandatory step order: classify, severity+SLA, dedupe, label, route, assign — with the blocker confirmation gate. |
| `content/02-transparency-comment.xml` | The single comment shape that lists every classification field so the assignee can dispute with one reaction. |

## Templates

| File | Purpose |
|------|---------|
| `templates/triage-pipeline.yaml` | Pipeline config with the six steps, the blocker gate, and dedupe threshold. |

## Related

- https://www.webelight.com/blog/bug-triage-agents-ai-github-jira-automation
- https://bugpilot.io/2026/01/28/automated-bug-triage-ai-prioritization-reporting-guide/
- https://lobehub.com/skills/lobbi-docs-claude-triage
