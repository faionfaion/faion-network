# Code Review Process

## Summary

The operational process layer for code review: a PR description template that agents fill from diff and linked issue, a CI workflow (lint, test, coverage, PR-size guard), four canonical review scenario templates (bug, design, security, performance), and review health metrics (time to first review, cycle time, rework rate). Scenario classifiers must select from the four templates — unconstrained comments produce inconsistent output that reviewers ignore.

## Why

Inconsistent PR descriptions, missing checklists, and freeform review comments slow the review cycle and obscure what the author must act on. Standardized PR templates propagate cleanly into agent prompts; scenario templates ensure each bug/design/security/performance finding uses the same structure. Tracking rework rate (PRs needing more than one review iteration) is the primary signal that the process is or is not working.

## When To Use

- Standardizing PR-description quality: agent fills the template from commit messages, diff, and linked issue.
- Wiring CI checks so human and agent reviewer see the same signal before commenting.
- Generating reviewer comment scaffolding for the four canonical scenarios.
- Tracking weekly review health metrics and producing dashboard reports.

## When NOT To Use

- Replacing the human review verdict — process scaffolding only, not approval authority.
- Greenfield repos without established conventions — process amplifies existing bad habits.
- Tiny teams (1-2 developers) where overhead exceeds value — use lightweight inline review.
- Spike or throwaway branches — process overhead does not pay back.

## Content

| File | What's inside |
|------|---------------|
| `content/01-pr-template.xml` | PR description fields, checklist items, rules for agent filling vs leaving unchecked. |
| `content/02-scenarios.xml` | Four scenario templates: bug (wrong output), design (too many responsibilities), security (missing auth), performance (N+1 query). |
| `content/03-metrics.xml` | Review health metrics: time to first review, cycle time, rework rate, comment ratio, defect escape rate. |

## Templates

| File | Purpose |
|------|---------|
| `templates/pr-description.md` | Full PR description template with description, related issues, change type, test checklist. |
| `templates/pr-checks.yml` | GitHub Actions CI workflow: lint, test, coverage gate, PR-size warning. |
| `templates/pr-size-guard.sh` | Shell script: warns above 400 lines, blocks above 1500 lines, outputs ::warning and ::error annotations. |
