# Synthetic Users

## Summary

AI-generated user profiles that simulate survey and interview responses for directional, pre-validation research. Always labeled as synthetic; always followed by real-user validation before any product decision. The methodology's primary value is hypothesis triage — identifying what is worth investing in real-user research time.

## Why

Real user research is slow and expensive. Synthetic users provide fast directional signal for early ideation and hypothesis filtering. The single greatest adoption barrier is a "crisis of trust" from data quality concerns; the methodology addresses this with mandatory governance rules and explicit use-case constraints.

## When To Use

- Early ideation: generating directional signal before real users can be recruited.
- Hypothesis stress-testing as a fast pre-filter ("Would this persona care about X?").
- Low-stakes concept validation where the cost of being wrong is recoverable.
- Generating adversarial edge-case responses to find blind spots in a survey instrument.

## When NOT To Use

- Go/no-go product decisions — synthetic data cannot replace real demand signal.
- Demand forecasting or pricing research — synthetic willingness-to-pay is systematically biased high.
- Legal, medical, or safety research — any domain where findings have real consequences.
- Stakeholder-facing deliverables presented as real research without disclosure.

## Content

| File | What's inside |
|------|---------------|
| `content/01-method-and-limits.xml` | What synthetic users are, valid/invalid use cases, tool landscape, governance rules. |
| `content/02-agent-workflow.xml` | Profile generation + response simulation pipeline, prompt patterns, gotchas. |

## Templates

| File | Purpose |
|------|---------|
| `templates/synthetic-interview.py` | Python: profile generation + simulated interview via Anthropic SDK. |
| `templates/profile-prompt.txt` | Prompt template for generating synthetic user profiles with anti-uniformity constraints. |
