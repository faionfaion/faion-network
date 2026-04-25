# Agent Integration — Reasoning-First Architectures

## When to use
- Tasks where acting without a plan produces low-quality output (complex coding, multi-step math, strategic decisions)
- Research synthesis where the agent must reconcile conflicting sources before concluding
- Any agentic pipeline where premature tool calls cause cascading errors (e.g. writing code before understanding the full spec)
- Quality-critical generation where a Critique-and-Revise loop demonstrably improves output
- Problems with multiple viable solution paths where Tree-of-Thought search yields better solutions than greedy selection

## When NOT to use
- Simple factual retrieval where reasoning adds latency with no quality gain
- Latency-sensitive paths (<500ms budget) — extended thinking and multi-path search are expensive
- Tasks where the domain is so narrow that chain-of-thought adds no signal (e.g. regex matching, format conversion)
- Reflexion loops on tasks with no verifiable exit criterion — the loop runs to the cap and exits with no quality guarantee
- Streaming response use cases where intermediate reasoning steps must not be shown to the user

## Where it fails / limitations
- **ReAct verbose reasoning**: models produce plausible-sounding reasoning steps that are wrong; the reasoning trace is not causally connected to the output
- **Tree-of-Thought cost**: exploring N paths × M evaluation steps multiplies LLM calls; even a 3-path ToT with 5 evaluation rounds costs 15 calls per query
- **Reflexion without a verifier**: self-evaluation by the same model that generated the output has low recall for the model's own failure modes
- **Planning Loops with stale plans**: the plan is correct at creation time but becomes invalid after unexpected tool results mid-execution
- **Critique-and-Revise anchoring**: the generator is anchored to its first output; revisions tend to be surface-level rather than structural
- **Extended thinking token cost**: Claude's extended thinking mode uses thinking tokens that count against the context window and are billed; naive use on every request is expensive

## Agentic workflow
A Claude subagent with reasoning-first architecture separates a planning/thinking phase from an execution phase. For ReAct, the subagent's system prompt enforces explicit Thought → Action → Observation formatting before any tool call. For Reflexion, an outer loop invokes the subagent, passes its output to a critic, and re-invokes with the critique appended. For Tree-of-Thought, a branching subagent generates N candidates, a scoring subagent evaluates each, and a selector picks the best path to expand — all orchestrated by a parent coordinator.

### Recommended subagents
- `thinker` — ReAct agent with explicit reasoning steps before each tool call; uses extended thinking (Claude) or chain-of-thought prompt; uses Sonnet or Opus
- `tree-explorer` — generates 3 candidate approaches for a problem; uses Sonnet
- `path-evaluator` — scores each candidate approach against a rubric (0-10); uses Haiku for efficiency
- `reflexion-critic` — evaluates output quality and returns structured improvement suggestions; uses Sonnet
- `plan-and-act` — produces a full plan before any execution step, then executes sequentially; uses Opus for planning, Sonnet for execution

### Prompt pattern
ReAct with enforced reasoning:
```xml
<instruction>
Before taking any action, write your reasoning under <thought>.
Then specify your action under <action>.
After observing the result, write your next thought.
Continue until you have enough information to answer.
</thought>
<action>tool_name(args)</action>
<observation>{{tool_result}}</observation>
```

Critique-and-Revise:
```xml
<role>Critic</role>
<original_task>{{task}}</original_task>
<generated_output>{{output}}</generated_output>
<instruction>
Identify specific weaknesses. For each weakness, provide:
1. What is wrong
2. Why it matters
3. Concrete suggestion to fix it
Do not provide a revised version — only the critique.
</instruction>
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `langchain` | ReAct agent scaffolding via `create_react_agent` | `pip install langchain` / python.langchain.com |
| `langgraph` | State graphs for Reflexion loops and Tree-of-Thought branches | `pip install langgraph` / langchain-ai.github.io/langgraph |
| `litellm` | Unified API for extended thinking across model providers | `pip install litellm` / docs.litellm.ai |
| `dspy` | Declarative LM programming with automatic prompt optimization | `pip install dspy-ai` / dspy-docs.readthedocs.io |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Anthropic Claude (extended thinking) | SaaS | Yes | Native `thinking` parameter for structured pre-action reasoning |
| OpenAI o1 / o3 | SaaS | Yes | Built-in chain-of-thought reasoning before output; no explicit Thought step needed |
| LangSmith | SaaS | Yes | Traces Thought/Action/Observation steps; essential for debugging ReAct loops |
| Weights & Biases Weave | SaaS | Yes | Tracks reasoning path length, cost, and quality across Reflexion iterations |

## Templates & scripts
See `templates.md` for ReAct, Reflexion, and Planning Loop implementations.

Tree-of-Thought selector (≤25 lines):
```python
def tree_of_thought(problem: str, generate_fn, score_fn, n_paths=3, max_depth=3):
    candidates = generate_fn(problem, n=n_paths)
    for depth in range(max_depth):
        scored = [(c, score_fn(problem, c)) for c in candidates]
        best = max(scored, key=lambda x: x[1])
        if best[1] >= 8:  # threshold: good enough
            return best[0]
        # Expand best candidate
        candidates = generate_fn(f"{problem}\nBest so far:\n{best[0]}", n=n_paths)
    return max(scored, key=lambda x: x[1])[0]
```

## Best practices
- For ReAct, add a hard max on reasoning steps per turn (e.g. 5 Thought/Action cycles) to prevent over-reasoning before acting
- For Reflexion, make the critic prompt list **specific failure modes** to check rather than asking for general feedback; specificity catches more issues
- For Tree-of-Thought, use Haiku to score candidates and reserve Sonnet/Opus for generating and expanding paths — cost drops 60-80%
- For Planning Loops, validate the plan against a schema before execution; catch malformed plans before they cascade into bad tool calls
- Log the full reasoning trace (all Thought steps) to an audit store — reasoning steps are the primary debugging tool for agent failures
- Use extended thinking (Claude) or o1 (OpenAI) for the planning phase; use a cheaper model for each individual execution step

## AI-agent gotchas
- **Confident wrong reasoning**: models produce syntactically valid Thought steps that are factually wrong. Reasoning text is not ground truth — always verify final outputs against an external check when possible.
- **Reasoning length explosion**: in ReAct, models can produce multi-paragraph Thought blocks that consume most of the context window before taking any action. Cap reasoning length with `max_tokens` on the thinking portion.
- **Tree-of-Thought cost spiral**: ToT with backtracking can explore exponentially many paths. Set a hard cap on total nodes (e.g. 20) and prune aggressively below the score threshold.
- **Reflexion critic anchoring**: asking the same model to critique its own output has low recall for its own failure modes. Use a second model or a rule-based verifier as critic when possible.
- **Human-in-loop at plan step**: for Planning Loops that will take irreversible actions (writes, sends, deploys), surface the plan to a human for review before execution begins. The reasoning-first architecture makes this natural — the plan is an artifact that can be inspected before any action.
- **Extended thinking billing**: Claude's thinking tokens are billed at the same rate as output tokens. A naive "think before every step" prompt on a high-traffic agent can double costs. Gate extended thinking to complex subtasks only.

## References
- ReAct paper: https://arxiv.org/abs/2210.03629
- Tree of Thoughts paper: https://arxiv.org/abs/2305.10601
- Reflexion paper: https://arxiv.org/abs/2303.11366
- Claude extended thinking docs: https://docs.anthropic.com/en/docs/build-with-claude/extended-thinking
- "Reasoning models" — OpenAI docs: https://platform.openai.com/docs/guides/reasoning
