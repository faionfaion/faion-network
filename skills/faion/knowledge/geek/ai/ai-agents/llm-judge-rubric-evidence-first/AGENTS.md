# LLM-as-Judge — Rubric, Evidence-First, Bias-Mitigated

## Summary

When you cannot use exact-match or unit-test checks (open-ended outputs: summaries, code review, plans, agent transcripts), use another LLM as a judge — but only with a structured rubric, JSON output, evidence cited BEFORE the score, per-criterion scoring, and explicit mitigation of position/verbosity/self-preference/authority bias. "Rate 1-10" prompts are not evals; they are noise generators.

## Why

Galileo's 2026 review of 12 production judge stacks plus Anthropic's eval guidance both show that vanilla "score this 1-10" judges have inter-rater reliability below Cronbach's alpha 0.5, which is worse than coin-flip on borderline cases. Adding a named rubric, requiring evidence quotes from the candidate output before scoring, and randomising candidate order pushes alpha to 0.8+ and removes the four canonical biases. Without this discipline, you ship a judge that simply prefers longer, GPT-4-flavoured responses regardless of correctness.

## When To Use

- Evaluating open-ended agent outputs where exact-match is impossible (summaries, plans, multi-turn dialogue).
- Grading code review comments, refactor plans, or other reasoning artifacts.
- Pairwise comparison of two agent variants on the same task set.
- Building a regression suite for prompt or model changes that touch generation quality.

## When NOT To Use

- Output is verifiable deterministically (compiles, passes tests, matches schema) — judges add cost and noise; use the deterministic check first.
- Single-LLM stack on borderline cases — self-preference bias is unfixable; bring in a second model family for cross-judging.
- Privacy-sensitive outputs you cannot send to a third-party judge — keep evals local or skip.
- Throwaway prototypes — overhead of rubric design is not justified before the agent is real.

## Content

| File | What's inside |
|------|---------------|
| `content/01-rubric-shape.xml` | The required rubric shape: named criteria, weights, evidence-before-score, JSON output schema. |
| `content/02-bias-mitigation.xml` | The four canonical biases (position, verbosity, self-preference, authority) and the concrete countermeasure for each. |

## Templates

| File | Purpose |
|------|---------|
| `templates/rubric.json` | Reusable rubric template with criteria, weights, output schema, and judge-prompt slots. |
| `templates/judge-prompt.txt` | Plain-text judge prompt with bias-mitigation instructions and evidence-first ordering. |
