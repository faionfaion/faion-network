# SDD Document Templates

## Summary

A collection of canonical templates for every SDD artifact: Constitution, Spec, Design, Implementation Plan, Task, Roadmap, Backlog Item, Confidence Check, Pattern Record, and Mistake Record. Use these as output schemas — provide a template in the system prompt, instruct the agent to fill each section, and enforce that no non-standard sections are added.

## Why

Without fixed schemas, agents invent non-standard sections, omit required fields, and produce inconsistent output across sessions. Templates constrain output structure and ensure executor agents can parse task files predictably. The Confidence Check template enforces explicit quality gates at phase transitions; the Pattern/Mistake Record templates enable agent self-logging and cross-session learning.

## When To Use

- Starting any SDD artifact from scratch — always start from the relevant template.
- Onboarding a new project: the Constitution template captures tech stack and standards before feature work begins.
- When a subagent must produce a spec, design, task, or implementation plan with consistent structure.
- Generating backlog items, roadmap entries, or confidence-check reports during planning sessions.

## When NOT To Use

- When an SDD artifact already exists and only needs incremental updates — edit in place.
- For one-off notes or research spikes that do not feed into task execution.
- Generating freeform documentation not part of the SDD lifecycle.

## Content

| File | What's inside |
|------|---------------|
| `content/01-artifact-templates.xml` | Constitution, Spec, Design, Task, and Impl Plan template bodies with field descriptions. |
| `content/02-planning-templates.xml` | Roadmap, Backlog Item, Grooming Session, Confidence Check, Pattern/Mistake Record templates. |
| `content/03-usage-rules.xml` | Rules for template usage: do not add sections, run Confidence Check at four gates, token estimation guide, agent self-logging pattern. |

## Templates

| File | Purpose |
|------|---------|
| `templates/constitution.md` | Project Constitution skeleton (vision, tech stack, patterns, standards, quality gates). |
| `templates/implementation-plan.md` | Implementation Plan skeleton (overview, task table, dependency graph, waves, quality gates). |
| `templates/backlog-item.md` | Backlog item skeleton (priority, RICE score, problem, AC, dependencies). |
| `templates/confidence-check.md` | Confidence Check skeleton (score table, verdict, gaps). |
| `templates/pattern-record.json` | JSON schema for agent-logged successful patterns. |
| `templates/mistake-record.json` | JSON schema for agent-logged errors and solutions. |
| `templates/new-feature.sh` | Shell script to scaffold a new feature directory with stub spec and impl plan. |
