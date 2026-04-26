# Cognitive Walkthrough: Process

## Summary

The full structured process for running a cognitive walkthrough: defining prerequisites (persona, task, correct action sequence, interface), assembling 2-4 evaluators, completing per-step evaluation forms for all four questions, documenting issues with concrete fixes, and synthesizing findings into a prioritized summary report. Lock the action sequence before any evaluation begins — mid-walk changes invalidate per-step JSON.

## Why

Ad-hoc walkthrough without consistent templates produces inconsistent outputs that cannot be merged across evaluators or tracked across releases. The structured process — planner → per-step evaluation forms → summary report — ensures every issue cites a step number, a question (Q1-Q4), and a one-line fix. Tracking resolved/new/regressed issues per release proves whether the walk is paying off.

## When To Use

- Multi-evaluator walkthroughs where outputs must be consistent and mergeable.
- CI-integrated walkthroughs: every preview deploy of a critical flow gets an automated walk and report attached to the PR.
- Re-evaluation after fixes — agent re-runs the full process and produces a delta report vs the prior run.
- Cross-evaluator aggregation: two human evaluators plus one agent fill forms independently; a reconciler merges results.

## When NOT To Use

- Ad-hoc single-screen reviews — use cog-walk-basics without the full process overhead.
- Unstable task sequences changing daily — lock the action sequence first, then walk.
- When stakeholders need real user voice — inspection findings are not user evidence.
- Multi-app journeys spanning systems the agent cannot render without orchestration.

## Content

| File | What's inside |
|------|---------------|
| `content/01-process-steps.xml` | Five-step process: prerequisites, evaluator assembly, per-step walk, issue documentation, findings summary. |
| `content/02-reporting.xml` | Summary report structure, severity calibration rules, exec-summary constraints, delta tracking across releases. |

## Templates

| File | Purpose |
|------|---------|
| `templates/walkthrough-plan.md` | Planning template: persona, task, correct action sequence table, interface link, scope. |
| `templates/evaluation-form.md` | Per-step form: Q1-Q4 with Yes/No/Partial + notes, issues table with severity and suggestion. |
| `templates/cw-findings.md` | Walkthrough findings: executive summary, step issues, issues table, priority recommendations, positive findings. |
| `templates/run-cog-walk.sh` | Shell pipeline driver: planner → Playwright captures → evaluators → reporter. |
