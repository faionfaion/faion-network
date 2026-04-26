# Workflow: Specification Phase

## Summary

Step-by-step procedures for the SDD specification phase: writing constitutions (two modes:
existing codebase analysis vs. Socratic dialogue for new projects), writing specifications
(Brainstorm → Research → Clarify → Draft → Review → Save), backlog grooming with
Definition of Ready, and roadmapping with confidence levels (90/70/50%). All workflows
have human-in-loop checkpoints at section boundaries.

## Why

Agents writing specs without Socratic dialogue produce assumption-driven requirements that
fail AC validation. Without constitution analysis, new code contradicts implicit standards.
Without a backlog grooming Definition of Ready, features enter execution with unapproved
specs and missing dependencies. The structured procedures enforce incremental validation
(show each section, get approval) before proceeding.

## When To Use

- Starting a new feature where requirements are unclear or only partially defined
- Existing codebase needs a constitution — tech decisions are implicit and undocumented
- Backlog grooming session where features need prioritization and DoR verification
- Roadmap needs a reality check against current feature status

## When NOT To Use

- Feature is a bugfix with a single clear root cause — skip spec, go straight to task
- Requirements fully documented elsewhere (existing PRD) — extract, don't re-elicit
- Constitution already exists and team agrees — skip Mode 1 discovery
- Rapid prototype/spike where requirements will change after seeing output

## Content

| File | What's inside |
|------|---------------|
| `content/01-constitution-workflow.xml` | Mode 1 (existing project) and Mode 2 (new project) constitution workflows; anti-patterns |
| `content/02-spec-workflow.xml` | 6-phase spec writing: brainstorming (Five Whys, alternatives), codebase research, clarify, draft section-by-section, review, save |
| `content/03-grooming-roadmap.xml` | Backlog grooming phases, Definition of Ready checklist, roadmapping with confidence levels |

## Templates

none

## Scripts

| File | Purpose |
|------|---------|
| `scripts/backlog-audit.sh` | Print feature status table (spec/design/plan existence) across all lifecycle stages |
