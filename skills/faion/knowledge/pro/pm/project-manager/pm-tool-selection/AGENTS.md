# PM Tool Selection

## Summary

A structured evaluation framework for selecting or replacing a project management tool: gather requirements via MoSCoW matrix, run a time-boxed 2-week POC on real project data, score tools against weighted criteria, compute 3-year TCO, and document the decision as an ADR. Human sign-off is mandatory at requirements, POC scoring, and final decision — agents must not pick the tool unilaterally.

## Why

PM tool switches fail when driven by single-person preference or novelty bias rather than documented requirements and evidence. Weighted scorecards with explicit criteria prevent rationalization theater; TCO models surface migration and training costs that per-seat pricing hides; and ADR documentation gives future teams the context to revisit without starting over.

## When To Use

- New team picking a first PM tool, or current tool causing documented friction
- Vendor renewal cycle where a price jump triggers re-evaluation
- Post-acquisition consolidation across two tool stacks
- Compliance shift (SOC2, HIPAA, EU data residency) forcing reassessment

## When NOT To Use

- Teams under 5 people with simple workflow — pick GitHub Projects or Linear free tier, skip the matrix
- Mid-project under deadline pressure — switching tools mid-flight burns more than it saves
- Single-issue gripe (e.g., "velocity report is ugly") — fix the report, do not migrate
- Decision already made by leadership — running a theater POC erodes trust

## Content

| File | What's inside |
|------|---------------|
| `content/01-evaluation-process.xml` | Requirements gathering, MoSCoW matrix, tool comparison framework, TCO model |
| `content/02-tool-profiles.xml` | Quick-reference profiles for Jira, Linear, ClickUp, Notion, GitHub, GitLab, Azure DevOps, others |
| `content/03-workflow.xml` | Agentic subagents, prompt patterns, AI-agent gotchas, best practices |

## Templates

| File | Purpose |
|------|---------|
| `templates/requirements.yaml` | MoSCoW requirements matrix with must/should/nice/constraints sections |
| `templates/tco.yaml` | 3-year TCO model: direct, indirect, hidden costs |
| `templates/adr.md` | ADR template for documenting the tool decision with evaluation summary |
| `templates/fetch-pricing.sh` | Snapshot vendor pricing pages for diff-review |
