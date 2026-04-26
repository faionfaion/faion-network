# RACI Matrix

## Summary

A RACI matrix assigns exactly one of four roles — Responsible, Accountable, Consulted, Informed — to each stakeholder for each task or deliverable. The single testable rule: every task row must have exactly one Accountable and at least one Responsible. Multiple Accountables on a single task is the most common failure mode and re-creates the "no clear owner" problem the matrix was designed to solve.

## Why

Projects fail from unclear ownership: "I thought you were handling that," duplicate effort, and approval bottlenecks from undefined decision-makers. RACI externalizes the implicit contract between roles before work starts. The PMI PMBOK 7th edition Team Performance Domain identifies role clarity as a prerequisite for high-performing teams.

## When To Use

- Multi-role projects with more than 3 roles and more than 10 deliverables.
- Solopreneur engagements with contractors or agencies where one human plus outsourced parties need clear per-task ownership.
- Onboarding a new hire or contractor — encodes "who owns what" in one readable table.
- Pre-mortem or kickoff for cross-functional features (PM + Eng + Design + QA + DevOps) before sprint zero.
- Incident response retros where "no one owned X" was a root cause — bake the new RACI into the runbook.

## When NOT To Use

- Solo work with no external collaborators — overhead with zero return.
- Self-organizing Scrum teams where Definition of Done plus collective code ownership already covers accountability — RACI can undermine team agency.
- Hyper-dynamic discovery work where tasks change weekly — the matrix goes stale faster than it can be maintained.
- Senior autonomous teams operating under DACI, Advice Process, or RAPID — those frameworks fit decision rights better.

## Content

| File | What's inside |
|------|---------------|
| `content/01-raci-rules.xml` | The four roles, validation rules (one A, one+ R, C-limit, I-generosity), common mistakes. |
| `content/02-raci-examples.xml` | Feature development RACI, solopreneur-with-contractors RACI, agent-driven project RACI. |
| `content/03-agent-usage.xml` | Agentic workflows: raci-drafter, raci-validator, raci-diff. Prompt patterns. Gotchas. |

## Templates

| File | Purpose |
|------|---------|
| `templates/raci-lint.py` | Lint a Markdown RACI table on stdin; exit 1 on violations (missing A, missing R, too many C). |
| `templates/raci-template.md` | Blank RACI matrix with role columns and task rows ready to fill. |
