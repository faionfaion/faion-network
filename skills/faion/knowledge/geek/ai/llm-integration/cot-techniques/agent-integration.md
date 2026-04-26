# Agent Integration — Chain-of-Thought Advanced Techniques

## When to use
- Multi-step reasoning problems where zero-shot CoT still produces wrong answers
- Problems with branching solution paths (code architecture choices, algorithm selection) — use Tree of Thoughts
- Problems with sequential sub-dependencies (build system, migration path) — use Least-to-Most decomposition
- Verification pipelines where the model must self-check an answer before returning it
- Agent planning steps where you need the model to reason about which tool to call next

## When NOT to use
- Simple factual lookups — CoT inflates token usage without improving accuracy
- Classification tasks with 3–5 clear categories — few-shot without CoT is faster and cheaper
- High-throughput pipelines where latency matters — each ToT branch is a separate API call
- Tasks where the reasoning trace would itself be the output (e.g., essay writing) — standard prompting is sufficient
- When self-consistency requires 5–10 samples — cost multiplies linearly; benchmark accuracy gain vs. cost first

## Where it fails / limitations
- Tree of Thoughts with `num_branches=3, max_depth=3` makes up to 9+ API calls per problem — cost explodes for complex trees
- Self-consistency relies on majority vote; if all samples share the same bias, the wrong answer wins consistently
- Least-to-Most requires the LLM to decompose correctly — if decomposition is wrong, all downstream steps are wrong
- Models can produce confident, well-structured reasoning that is factually incorrect ("hallucination with steps")
- JSON response format is required for thought evaluation; models occasionally produce malformed JSON under the structured reasoning load

## Agentic workflow
Advanced CoT techniques are best encapsulated inside a reasoning subagent that exposes a single `reason(problem, strategy)` interface. The parent agent passes a problem description and a strategy hint (zero_shot / tree_of_thoughts / least_to_most); the reasoning subagent selects the implementation, runs it, and returns a structured result with the reasoning trace and final answer. The parent agent uses only the final answer, not the trace — this keeps context clean across multi-turn conversations.

### Recommended subagents
- `faion-sdd-executor-agent` — can invoke a CoT reasoning step as part of design/spec generation
- A dedicated `reasoning-agent` wrapping `ChainOfThoughtService` (see README.md) for complex decision tasks

### Prompt pattern
Zero-shot trigger (cheapest, try first):
```
Think step by step. Show your reasoning before giving the final answer.
```

Tree of Thoughts trigger for branching decisions:
```
Generate 3 distinct approaches to this problem, evaluate each, then choose the best and complete it.
```

Least-to-Most for sequential problems:
```
First list the subproblems from simplest to hardest. Then solve each in order, using previous solutions.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `openai` / `anthropic` (Python SDK) | LLM calls for CoT steps | `pip install openai anthropic` |
| `tenacity` | Retry on JSON parse failure from CoT output | `pip install tenacity` |
| `dspy` | Framework for programmatic CoT prompt optimization | `pip install dspy-ai` / https://dspy.ai |
| `guidance` | Constrained generation for structured CoT | `pip install guidance` / https://github.com/guidance-ai/guidance |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| OpenAI GPT-4o / o1 | SaaS | Yes | o1 has native CoT reasoning built in |
| Anthropic Claude (extended thinking) | SaaS | Yes | Extended thinking = native CoT; see claude-advanced-features |
| LangSmith | SaaS | Yes | Trace and visualize CoT reasoning chains |
| DSPy | OSS | Yes | Programmatically optimize CoT prompts |
| Weights & Biases | SaaS | Yes | Log reasoning traces and evaluate accuracy |

## Templates & scripts
See `templates.md` for `ChainOfThoughtService` and `TreeOfThoughts` class templates. Strategy selection heuristic:

```python
def select_cot_strategy(problem: str) -> str:
    """Heuristic: pick CoT strategy based on problem length and keywords."""
    kws_branching = {"choose", "compare", "which", "options", "alternative"}
    kws_sequential = {"step", "before", "depends", "order", "first", "then"}
    words = set(problem.lower().split())
    if kws_branching & words:
        return "tree_of_thoughts"
    if kws_sequential & words or len(problem) > 500:
        return "least_to_most"
    return "zero_shot"
```

## Best practices
- Always try zero-shot CoT first (`"Think step by step."`) — it solves 70–80% of cases at minimal cost
- Use `response_format={"type": "json_object"}` for thought evaluation in ToT to prevent parse failures
- Set a hard `max_depth` on Tree of Thoughts (2–3 levels max) to prevent runaway API call chains
- For self-consistency, sample at `temperature=0.7` and use the most common answer, not the first
- Cache the decomposition step output in Least-to-Most — if the LLM already decomposed the problem, don't re-decompose on retry
- Use `o1` / `o3` models for problems that natively benefit from extended reasoning — they handle CoT internally and are cheaper than explicit multi-call ToT

## AI-agent gotchas
- An agent running ToT must set a wall-clock timeout — a 9-branch tree with slow API responses can stall the pipeline for minutes
- JSON parse failures in thought evaluation (`_evaluate_thoughts`) are common — always wrap in try/except and assign score=0 on parse failure rather than crashing
- Self-consistency samples must be deduplicated before majority vote — identical outputs (low temperature) artificially inflate one answer's count
- Extended Thinking (Claude) and o1 reasoning tokens are billed but not visible in the response text — account for them in cost tracking
- Do NOT include the full CoT trace in the next turn's context — it bloats the context window rapidly in multi-turn agents; summarize or strip it

## References
- https://arxiv.org/abs/2201.11903 (Chain-of-Thought Prompting, Wei et al.)
- https://arxiv.org/abs/2305.10601 (Tree of Thoughts, Yao et al.)
- https://arxiv.org/abs/2205.10625 (Least-to-Most, Zhou et al.)
- https://arxiv.org/abs/2203.11171 (Self-Consistency, Wang et al.)
- https://platform.openai.com/docs/guides/reasoning (o1 reasoning guide)
