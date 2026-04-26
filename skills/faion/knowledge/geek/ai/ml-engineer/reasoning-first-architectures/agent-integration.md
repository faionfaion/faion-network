# Agent Integration — Reasoning-First Architectures

## When to use
- Task requires multi-step math, logic, or formal proofs where intermediate steps matter
- Code generation with edge cases requiring self-verification before returning
- Research synthesis where the agent must explore competing hypotheses before concluding
- Planning tasks with dependencies — agent must validate ordering before execution
- Any workflow where the cost of a wrong answer outweighs the cost of extra tokens

## When NOT to use
- Simple retrieval or lookup tasks where CoT adds latency with no quality gain
- High-throughput classification or routing (thousands of calls per minute)
- Creative writing where deliberate reasoning constrains output quality
- Cost-sensitive pipelines where standard models already meet the bar (verified by eval)
- Real-time streaming responses where users see partial output — reasoning tokens break the UX

## Where it fails / limitations
- Reasoning tokens are billed as output tokens; o3 + long reasoning budget can cost 10-50x a standard call
- "Thinking" is not always correct — models can hallucinate confident-sounding reasoning chains
- Extended Thinking on Claude cannot be interrupted mid-thought; no streaming of reasoning tokens to the user
- DeepSeek R1 visible `<think>` blocks leak internal monologue — not appropriate when confidentiality of reasoning is required
- Test-time compute scaling hits diminishing returns on tasks that require factual recall (knowledge cutoffs still apply)
- o3/o4 tool-use with extended reasoning has higher latency per tool call due to interleaved thinking

## Agentic workflow
A subagent receives a complex task (planning, debugging, theorem proving). It invokes a reasoning model with a tuned thinking budget — low budget (1K-4K tokens) for structural tasks, high budget (32K-128K) for math/code. The reasoning output is then passed to a cheaper model for summarization or formatting. Human review checkpoints should gate any destructive downstream actions that follow from the reasoning.

### Recommended subagents
- `faion-sdd-executor-agent` — wraps reasoning calls for architecture design and spec validation tasks
- `nero-sdd-executor-agent` — same pattern for NERO-internal planning loops

### Prompt pattern
```
# System
You are a careful reasoning agent. Think step by step before answering.
Never skip verification steps. Output only your final conclusion after thinking.

# User
<task>
Verify that the proposed database schema handles the following edge cases: ...
</task>
```

```python
# Claude Extended Thinking — minimal invocation
import anthropic
client = anthropic.Anthropic()
response = client.messages.create(
    model="claude-opus-4-5",
    max_tokens=16000,
    thinking={"type": "enabled", "budget_tokens": 8000},
    messages=[{"role": "user", "content": task}]
)
# response.content[0] is ThinkingBlock, [1] is TextBlock
answer = response.content[1].text
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `openai` Python SDK | Call o3/o4-mini with reasoning_effort param | `pip install openai` / platform.openai.com |
| `anthropic` Python SDK | Claude Extended Thinking via `thinking=` param | `pip install anthropic` / docs.anthropic.com |
| `litellm` | Unified interface: switch models without code changes | `pip install litellm` / litellm.ai |
| `promptfoo` | Eval harness to compare reasoning vs standard models | `npx promptfoo` / promptfoo.dev |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| OpenAI API (o3, o4-mini) | SaaS | Yes | `reasoning_effort`: low/medium/high; returns usage.reasoning_tokens |
| Anthropic API (Claude 3.7/4) | SaaS | Yes | `thinking.budget_tokens` 1K-128K; streaming supported for text block |
| DeepSeek API (R1) | SaaS | Yes | Returns `<think>` block in content; cheap ($0.55/M input) |
| Replicate (QwQ-32B) | SaaS | Yes | Open-weight; good for batch offline reasoning |
| Together AI | SaaS | Yes | Hosts DeepSeek R1, QwQ; supports streaming |
| Ollama (local) | OSS | Partial | QwQ-32B, DeepSeek-R1-distilled; no API key; limited context |

## Templates & scripts
See `templates.md` for reasoning pipeline templates. Inline budget-selector:

```python
def reasoning_budget(task_type: str) -> int:
    """Return thinking budget tokens by task complexity."""
    budgets = {
        "format": 1024,       # Reformatting, extraction
        "analysis": 4096,     # Code review, logic check
        "planning": 8192,     # Architecture, multi-step plan
        "research": 32768,    # Deep synthesis, theorem proving
    }
    return budgets.get(task_type, 4096)
```

## Best practices
- Always measure: run eval on a sample before committing to a reasoning model in production
- Route by task: use a cheap model to classify task complexity, then dispatch to reasoning model only when warranted
- Set `max_tokens` high enough to accommodate reasoning tokens + answer; undershoot causes truncated thinking
- For Claude: `budget_tokens` does not guarantee usage — model decides; set it as an upper bound
- Strip `<think>` blocks before passing DeepSeek R1 output downstream or to users
- Cache reasoning outputs for identical inputs (same hash) to avoid re-billing reasoning tokens
- When using o3 tool use, batch tool calls per reasoning step to reduce round-trips

## AI-agent gotchas
- Reasoning tokens are non-deterministic even with temperature=0 on some providers; don't compare raw reasoning text between runs
- Extended Thinking cannot be used with `system` prompt caching on Claude in the same request (as of 2026-01); check API changelog
- `reasoning_effort=high` on o3 can spike a single call to $5-15; add per-call cost guards in agent loops
- Human-in-loop checkpoint required before any irreversible action (deploy, delete, send) that follows from reasoning output
- DeepSeek R1 `<think>` blocks may contain PII echoed from input — scrub before logging
- Tool calls interleaved with Extended Thinking (Claude) extend latency nonlinearly; set timeout > 120s in agent harness

## References
- https://platform.openai.com/docs/guides/reasoning
- https://docs.anthropic.com/en/docs/build-with-claude/extended-thinking
- https://arxiv.org/abs/2501.12948 (DeepSeek R1 paper)
- https://arxiv.org/abs/2210.03629 (ReAct)
- https://www.anthropic.com/engineering/claude-think-tool
