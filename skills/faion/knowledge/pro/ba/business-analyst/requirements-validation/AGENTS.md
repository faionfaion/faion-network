# Requirements Validation

## Summary

A four-stage process that confirms requirements build the right thing (not that they are built right). A BA-led quality scorecard grades each requirement against eight attributes (correct, complete, unambiguous, consistent, testable, traceable, feasible, necessary), a technique is selected (walkthrough, inspection, prototype review, simulation), findings are captured in a structured issue log, and a human stakeholder provides an explicit sign-off before design begins.

## Why

Development built on unvalidated requirements produces software that is correct but wrong. Wiegers (Software Requirements, 3rd ed.) and BABOK v3 ch. 8 both cite requirements defects caught before development as 10-100x cheaper to fix than post-delivery rework. Agents amplify the risk by generating plausible but invented requirements; structured validation with human sign-off closes the loop on summarization drift.

## When To Use

- Before flipping an SDD feature from todo/ to in-progress/ — validate that spec.md AC matches what the stakeholder asked, not what the elicitation agent inferred.
- After a non-trivial elicitation session to catch summarization drift.
- When a major scope change arrives mid-flight, before resuming faion-feature-executor.
- Pre-baseline gate: locking a spec.md version before design starts.
- Prototype is available and users can perform task-based walkthroughs to expose gaps.

## When NOT To Use

- Throwaway spikes or research tasks — use a stop condition and brief, not a validation session.
- Pre-elicitation: validating empty or aspirational requirements is theatre.
- Pure operational runbook tweaks (cron edits, nginx vhost) — smoke tests, not validation.
- Strictly internal refactors with no behavior change.
- Post-launch: use Solution Evaluation and feedback loops instead.

## Content

| File | What's inside |
|------|---------------|
| `content/01-validation-process.xml` | Eight quality attributes, technique selection rules, session preparation, issue log structure, sign-off requirements. |
| `content/02-agent-workflow.xml` | Four-stage agentic chain, recommended subagents, prompt patterns (scorecard + session minutes), AI gotchas. |

## Templates

| File | Purpose |
|------|---------|
| `templates/review-checklist.md` | Per-requirement quality checklist covering all eight attributes plus completeness and issue log. |
| `templates/session-agenda.md` | Validation session agenda template with time slots, participant roles, and pre-work list. |
| `templates/sign-off-form.md` | Requirements sign-off form with scope, conditions, outstanding items, and signature table. |
| `templates/req-validate.sh` | Bash script: pre-validation lint of spec.md — detects placeholders, weasel words, untraced requirements. |
