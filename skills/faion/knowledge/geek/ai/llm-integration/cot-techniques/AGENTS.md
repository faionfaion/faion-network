# Chain-of-Thought Advanced Techniques

## Summary

Advanced reasoning patterns beyond zero-shot CoT: Tree of Thoughts (ToT) for branching decisions, Least-to-Most for sequential sub-dependencies, and Self-Consistency for high-stakes answers. Always start with zero-shot CoT ("Think step by step.") — it solves 70–80% of cases. Escalate to advanced techniques only when zero-shot fails.

## Why

Zero-shot CoT improves model accuracy on multi-step reasoning by 20–40% with zero token overhead beyond the trigger phrase. Advanced techniques (ToT, Least-to-Most) can further improve accuracy for specific problem structures but multiply API call count linearly — they should be used judiciously after zero-shot fails.

## When To Use

- Multi-step reasoning where zero-shot CoT still produces wrong answers
- Branching solution paths (architecture choices, algorithm selection) — use Tree of Thoughts
- Sequential sub-dependencies (build order, migration path) — use Least-to-Most decomposition
- Verification pipelines where the model must self-check before returning
- Agent planning steps requiring reasoning about which tool to call next

## When NOT To Use

- Simple factual lookups — CoT inflates token usage without improving accuracy
- Classification tasks with 3–5 clear categories — few-shot without CoT is cheaper
- High-throughput pipelines where latency matters — each ToT branch is a separate API call
- When self-consistency requires 5–10 samples — cost multiplies linearly; benchmark gain vs. cost first

## Content

| File | What's inside |
|------|---------------|
| `content/01-tot-least-to-most.xml` | Tree of Thoughts implementation, Least-to-Most decomposition, depth limits |
| `content/02-strategy-selection.xml` | Strategy heuristic, self-consistency, CoT trace handling in multi-turn agents |

## Templates

| File | Purpose |
|------|---------|
| `templates/strategy-selector.py` | Keyword-based strategy selection heuristic |
| `templates/cot-prompts.txt` | Zero-shot, ToT, and Least-to-Most trigger phrases |
