# Decision Analysis

## Summary

Structured 6-step process for evaluating options against weighted criteria: define decision → identify options → define and lock criteria with weights → score options with evidence URLs per cell → sensitivity analysis (±20% weight Monte Carlo) → document rationale. Weights are locked before scoring; sensitivity analysis determines whether the recommendation is robust or fragile (top option wins less than 70% of Monte Carlo trials → escalate to human).

## Why

Decisions made by gut feel cannot be audited, re-examined, or calibrated over time. Making criteria weights explicit collapses argument-by-anecdote into argument-by-number. The sensitivity analysis surface is the key step that the README omits: a 3.85 vs 3.70 weighted total is well within rater noise — without Monte Carlo you cannot distinguish a real winner from statistical noise. The decision artifact in `.aidocs/` lets future teams audit and improve calibration.

## When To Use

- Reversible-but-expensive choice with three or more candidate options where the team is sliding toward gut feel (CRM selection, build-vs-buy, LLM provider choice).
- Stakeholders disagree because they secretly weight criteria differently — making weights explicit collapses the argument.
- Decision will be re-litigated later (board review, audit, post-mortem) and a written rationale is needed.
- Comparing N options against a current baseline (Pugh matrix mode).
- A decision has long-tail risk that only surfaces when tabulated (vendor lock-in, regulatory exposure).
- Sequential / conditional decisions with probabilities — switch to decision tree with expected value.

## When NOT To Use

- Two-option, low-cost, easily reversible decisions — use a 5-minute pros/cons list.
- Decision is actually about strategy, not selection — run a brainstorm session first.
- Analysis is retrofitted to justify a decision already made (the #1 failure mode).
- Pure financial trade-offs with quantifiable cash flows — use NPV / discounted cash flow directly.
- Decisions under deep uncertainty where numbers have more than one order-of-magnitude error.

## Content

| File | What's inside |
|------|---------------|
| `content/01-process.xml` | 6-step process rules: criteria lock-before-scoring, evidence-URL requirement per cell, scoring-direction normalization, sensitivity-analysis trigger. |
| `content/02-examples.xml` | CRM selection worked example, build-vs-buy example, Pugh matrix mode explained. |
| `content/03-agentic-workflow.xml` | Three-pass pipeline: frame pass (sonnet) → score pass (parallel agents) → sensitivity/dissent pass (opus). Prompt patterns and anti-patterns. |

## Templates

| File | Purpose |
|------|---------|
| `templates/decision-analysis.md` | Full Decision Analysis Document: context, options, criteria/weights, evaluation matrix, sensitivity, recommendation, approval. |
| `templates/decision-matrix-simple.md` | Lightweight matrix template for lower-stakes decisions. |
| `templates/sensitivity.py` | Monte Carlo over ±20% weight perturbations; prints robustness % per option. Recommends escalation if winner is below 70%. |
| `templates/prompt-score-pass.txt` | LLM prompt for evidence-backed cell scoring: evidence URLs required, confidence field, no-marketing-copy rule. |
