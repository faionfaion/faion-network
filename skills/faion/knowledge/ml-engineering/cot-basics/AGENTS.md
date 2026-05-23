# Chain-of-Thought (CoT) Basics

## Summary

**One-sentence:** Produces a chain-of-thought-enabled prompt that elicits explicit reasoning before answer — zero-shot CoT trigger, structured reasoning tag, parsed answer, fallback for non-CoT models.

**One-paragraph:** Chain-of-thought prompting asks the model to show its work before committing to an answer. Two basic moves: (1) zero-shot "let's think step by step" triggers; (2) structured `<reasoning>...</reasoning><answer>...</answer>` tag separation that lets the runtime parse only the answer for downstream consumers. CoT improves arithmetic, logical, and multi-step planning tasks; it is overkill (and a cost amplifier) for direct lookup or pattern-completion tasks. Modern reasoning models (Claude with Extended Thinking, o-series) embed CoT — explicit prompt-side CoT is a no-op there.

**Ефективно для:** multi-step word problems, multi-hop QA, constraint-satisfaction, code-translation, classification with rubric.

## Applies If (ALL must hold)

- Task involves ≥2 reasoning steps before the final answer.
- Caller can parse the model output to extract the final answer.
- Latency budget tolerates ≥30% longer responses.
- Cost budget tolerates ≥2-3x output tokens vs direct answer.

## Skip If (ANY kills it)

- Task is direct lookup or single-step pattern-completion.
- Using a reasoning model (Claude Extended Thinking, o-series) — CoT already happens internally.
- Streaming UX where partial reasoning leaks to the user.
- Output must be valid JSON only — wrap CoT outside the JSON or use forced tool call.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Task description | string | application logic |
| Output schema or expected answer shape | doc | spec |
| Sample inputs | text | eval set |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `[[cot-techniques]]` | Advanced CoT variants (few-shot CoT, self-consistency, tree-of-thought). |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 5 rules: tag the reasoning, parse the answer, cost cap, skip on reasoning models, eval the lift | ~600 |
| `content/02-output-contract.xml` | essential | Output schema: `<reasoning>...</reasoning><answer>...</answer>` + parser regex | ~500 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: unparseable output, reasoning leaks to user, CoT on lookup tasks, no eval, double-CoT with reasoning model | ~500 |
| `content/06-decision-tree.xml` | essential | Root: "≥2 reasoning steps AND not on a reasoning model?" | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| Choose CoT trigger | sonnet | Mechanical. |
| Author parser regex | haiku | Pure regex. |
| Eval lift measurement | haiku | Numerical. |

## Templates

| File | Purpose |
|---|---|
| `templates/cot-prompt.md` | Zero-shot CoT prompt skeleton with structured tags. |
| `templates/parser.py` | Regex parser extracting answer from `<answer>...</answer>`. |
| `templates/_smoke-test.txt` | Example CoT output for the parser test. |

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-cot-basics.py` | Validates a sample CoT output contains both `<reasoning>` and `<answer>` blocks and the answer is non-empty. | Pre-commit on fixtures; eval CI. |

## Related

- parent skill: `geek/ai/llm-integration/`
- `[[cot-techniques]]` — next step (few-shot, self-consistency)
- `[[claude-tool-use]]` — forced-tool extraction is an alternative to CoT for JSON

## Decision tree

The decision tree at `content/06-decision-tree.xml` decides whether CoT helps: single-step tasks → skip; reasoning model → skip (already internal); ≥2 steps + non-reasoning model + cost budget OK → run-the-checklist.
