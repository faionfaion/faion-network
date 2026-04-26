# Cognitive Walkthrough

## Summary

A structured expert-inspection method that evaluates interface learnability by stepping through
a known correct action sequence and answering four questions per step: does the user know what
to do, can they see how, does the label make sense, and do they get feedback that it worked?

## Why

Cognitive walkthrough finds learnability failures before any user is recruited — cheaper and
faster than moderated testing. It is especially sensitive to problems that block first-time
users: invisible actions, ambiguous labels, and missing progress feedback. A 2-4 person team
can cover a full onboarding flow in under two hours and produce a prioritized fix list.

## When To Use

- Evaluating learnability for first-time users: kiosks, sign-up flows, onboarding.
- Pre-launch sanity check before recruiting participants for usability testing.
- Auditing a defined task path (checkout, account setup) where the correct sequence is known.
- Government / public-service flows where novice users dominate.

## When NOT To Use

- Open-ended exploratory tasks (browsing) — no single correct sequence exists.
- Replacing real user research: walkthrough finds learnability issues, not preference or value.
- Subjective brand or aesthetic review — heuristic evaluation is the right method.
- Late-stage efficiency tuning for expert users — use keystroke-level model (KLM) or GOMS.

## Content

| File | What's inside |
|------|---------------|
| `content/01-protocol.xml` | Four CW questions, per-step procedure, evaluator setup, issue-documentation rules. |
| `content/02-rules.xml` | Evaluator calibration rules, agent-specific gotchas (charity bias, persona drift), severity rubric. |

## Templates

| File | Purpose |
|------|---------|
| `templates/walkthrough-plan.md` | Pre-session plan: persona, task, correct sequence table, interface link, scope. |
| `templates/evaluation-form.md` | Per-step evaluation: Q1-Q4 answers, issues table, screenshot slot. |
| `templates/summary-report.md` | Post-session report: executive summary, findings by step, priority recommendations. |
