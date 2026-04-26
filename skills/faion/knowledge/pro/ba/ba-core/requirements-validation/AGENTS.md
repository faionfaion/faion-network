# Requirements Validation

## Summary

BABOK Task 7.6: confirms that requirements accurately represent the business need and deliver expected value before any downstream commitment. Five steps: review quality attributes, choose validation technique, conduct session, address findings, obtain sign-off. Distinct from Verification (BABOK 7.5), which checks form/ambiguity/testability — Validation asks "are we building the right thing?"

## Why

Requirements are documented but nobody confirms they are correct. When stakeholders sign off without truly understanding, development builds what is written rather than what is meant. The gap between stated and intended requirements is the most expensive defect category — caught at validation it costs a session; caught post-deployment it costs a rework sprint.

## When To Use

- BABOK Task 7.6 trigger: a requirement or design is ready to be confirmed against business need before downstream commitment.
- Before requirements are baselined in a Requirements Repository — validation is the gate.
- When a stakeholder need is restated by an agent (summary, paraphrase, transcription) — close the loop on representational drift.
- When an existing baselined requirement is challenged by new information (regulation, market signal, data result).
- Capstone gate before transitioning from Requirements Analysis to Solution Evaluation.

## When NOT To Use

- Pre-elicitation: nothing to validate yet — run elicitation-techniques and requirements-documentation first.
- Pure technical-quality concerns (form, style, consistency) — that is Verification, not Validation.
- Throwaway prototypes meant to provoke a reaction — the prototype is the elicitation tool, not a sign-off candidate.
- Operational/maintenance changes with no new business need (dependency bumps, refactors).
- After delivery — use Solution Evaluation (BABOK ch. 8) and feedback-loop measurement instead.

## Content

| File | What's inside |
|------|---------------|
| `content/01-validation-framework.xml` | Validation vs verification distinction, eight quality attributes, five-step process, technique selection by requirement type. |
| `content/02-validation-antipatterns.xml` | Rubber-stamp approval, wrong participants, single-technique reliance, validation confused with UAT. |

## Templates

| File | Purpose |
|------|---------|
| `templates/review-checklist.md` | Requirements review checklist covering general quality and individual requirement checks. |
| `templates/sign-off-form.md` | Formal requirements sign-off with scope, conditions, outstanding items, and signature table. |
| `templates/req-value-trace.sh` | Bash script that fails pre-commit when a requirement in spec.md lacks a value-trace block. |
