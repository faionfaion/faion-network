# Cognitive Walkthrough: Basics

## Summary

A usability inspection method where evaluators step through a task from a first-time user's perspective, answering four questions per step: (1) Will the user try to achieve the right effect? (2) Will they notice the correct action? (3) Will they associate the action with the desired effect? (4) Will they see that progress is being made? Designed specifically to expose learnability failures before user testing.

## Why

Onboarding failures and first-use drop-off occur because teams evaluate their own interfaces as experts, not as first-time users. The four-question framework forces evaluators to separate motivation, visibility, labeling, and feedback — four distinct mechanisms that fail independently. It is cheap (no participants needed), fast, and works on prototypes before any code ships.

## When To Use

- Early prototypes and clickable mockups before investing in moderated usability testing.
- Onboarding flows, sign-up, first-run experiences where learnability is the primary concern.
- New feature launches where the interaction model is unfamiliar.
- CI-integrated review: a vision-capable agent walks each preview build of a critical flow and flags Q1-Q4 failures.
- Reviewing AI-generated UI before merging to main.

## When NOT To Use

- Expert-user efficiency tasks (dashboards, keyboard shortcuts) — use heuristic evaluation or quantitative testing instead.
- Purely aesthetic or visual hierarchy decisions — the four questions do not cover those.
- When real users are available — moderated usability testing always produces more reliable findings.
- Static brand/marketing pages with no task flow — there are no steps to walk through.

## Content

| File | What's inside |
|------|---------------|
| `content/01-framework.xml` | The four questions defined, what each checks, common failure modes per question, contrast with heuristic evaluation. |
| `content/02-examples.xml` | Two worked examples (sign-up flow, file upload) showing Q1-Q4 table per step with issue and fix. |
| `content/03-antipatterns.xml` | Five failure modes: power-user bias, skipping steps, omitting "Yes" findings, vague issue statements, missing fix recommendations. |

## Templates

| File | Purpose |
|------|---------|
| `templates/walk.py` | Playwright harness: drives browser, captures per-step screenshots, emits step JSON for evaluator agent. |
