# Agent Integration — Chain-of-Thought Prompting

## When to use
- Task requires multi-step reasoning: math problems, logic puzzles, code debugging, complex decisions
- The LLM is making errors on a problem that it should theoretically be able to solve — CoT often surfaces where the reasoning breaks
- Output needs to be explainable/auditable: visible reasoning steps allow users or reviewers to verify the path to an answer
- Agent must plan a sequence of actions before executing — CoT acts as a scratchpad before tool calls
- High-stakes single responses where Self-Consistency (multiple samples + voting) is justified by the cost of an error

## When NOT to use
- Simple classification, extraction, or translation tasks — CoT adds token cost (and latency) with no quality gain for tasks that don't require reasoning
- Latency is critical (< 1s response) — CoT adds tokens and turns; use a direct prompt instead
- Using o1/o3/DeepSeek-R1 style reasoning models — they have built-in chain-of-thought; adding explicit CoT prompting can interfere with their internal reasoning
- High-volume, low-complexity pipelines — the 2-5x token overhead multiplies into significant cost at scale

## Where it fails / limitations
- CoT can produce confident-sounding wrong reasoning: the model may generate a plausible-looking but incorrect chain that leads to a wrong answer
- For strong modern models (GPT-4+, Claude Sonnet 4+), simple zero-shot CoT often works as well as few-shot CoT — few-shot primarily enforces output format, not reasoning quality (2025 research finding)
- Self-Consistency requires 5-20 samples per query: effective but expensive; only use for mission-critical decisions
- Tree-of-Thoughts is expensive and requires a search algorithm (BFS/DFS) over candidate thoughts — impractical as a general-purpose technique; only for narrow planning/exploration tasks
- CoT reasoning is not verifiable by default: even visible reasoning steps can be post-hoc rationalizations rather than true causal chains — Typed CoT (ICLR 2026) addresses this but requires special model support

## Agentic workflow
A reasoning agent uses CoT implicitly via Claude's extended thinking (for Opus) or explicitly by structuring the prompt with `<thinking>` tags (for Sonnet). For planning tasks, the agent prompts Claude to output a plan in structured steps before executing any tool calls, then executes the plan step by step, checking intermediate results. For high-stakes decisions, the agent runs Self-Consistency: generates 5 independent reasoning paths and selects the answer that appears in the majority.

### Recommended subagents
- Reasoning agent with `<thinking>` — structured CoT for complex analysis tasks; returns `{thinking: ..., answer: ...}`
- Self-consistency voting subagent — runs N parallel Claude calls with temperature=0.7, collects answers, returns majority vote with confidence score

### Prompt pattern
```
# Zero-Shot CoT (most common)
Solve the following problem. Think step by step before giving your final answer.

Problem: {problem}

Reasoning:
```

```
# Structured CoT with XML tags (Claude-specific)
<task>
{task_description}
</task>

Think through this carefully in <thinking> tags, then provide your answer in <answer> tags.
```

```python
# Self-Consistency with Claude (3 samples)
import anthropic
from collections import Counter

def self_consistency(problem: str, n_samples: int = 5) -> str:
    client = anthropic.Anthropic()
    answers = []
    for _ in range(n_samples):
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            temperature=0.7,
            messages=[{
                "role": "user",
                "content": f"Think step by step and solve: {problem}\nFinal answer:",
            }],
        )
        answers.append(response.content[0].text.strip().split("\n")[-1])
    return Counter(answers).most_common(1)[0][0]
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `anthropic` | Claude API with Extended Thinking support | `pip install anthropic` — [docs.anthropic.com](https://docs.anthropic.com/) |
| `openai` | GPT-4 CoT via structured prompts | `pip install openai` |
| `dspy` | Programmatic CoT pipeline composition | `pip install dspy-ai` — [dspy.ai](https://dspy.ai/) |
| `guidance` | Constrained generation for structured CoT output | `pip install guidance` — [github.com/guidance-ai/guidance](https://github.com/guidance-ai/guidance) |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Anthropic API (Extended Thinking) | SaaS | Yes — Python/TS SDK | Built-in CoT for Opus; streamed thinking tokens |
| OpenAI (o1/o3/o4-mini) | SaaS | Yes — REST SDK | Built-in reasoning; don't add explicit CoT |
| DSPy | OSS | Yes — Python | Programmatic CoT; automatic few-shot optimization |
| Langfuse | SaaS + OSS | Yes | Trace and compare CoT vs direct prompts; cost per trace |

## Templates & scripts
See `templates.md` for copy-paste CoT prompt templates per task type.

Inline: Claude Extended Thinking call (< 20 lines):

```python
import anthropic

client = anthropic.Anthropic()

def extended_thinking(problem: str, thinking_budget: int = 4096) -> dict:
    response = client.messages.create(
        model="claude-opus-4-5-20251101",
        max_tokens=thinking_budget + 2048,
        thinking={"type": "enabled", "budget_tokens": thinking_budget},
        messages=[{"role": "user", "content": problem}],
    )
    thinking_text = next((b.thinking for b in response.content if b.type == "thinking"), "")
    answer_text = next((b.text for b in response.content if b.type == "text"), "")
    return {"thinking": thinking_text, "answer": answer_text}
```

## Best practices
- Start with zero-shot CoT ("Think step by step") for Claude Sonnet 4 and GPT-4+ — it works as well as few-shot for most tasks and saves tokens
- Use few-shot CoT only when you need a specific output format, not to improve reasoning quality on modern models
- For Claude: use `<thinking>` XML tags in the prompt to signal where the model should externalize its reasoning; this is more reliable than free-form "think step by step"
- Use Extended Thinking (Opus + `thinking` parameter) for math, formal logic, code correctness proofs, and multi-constraint optimization — it provides verifiable reasoning traces, not just CoT scaffolding
- Keep thinking budget proportional to task complexity: start at 1,024 tokens (minimum), increase by 1,024 until quality plateaus; diminishing returns appear quickly for most tasks
- Reserve Self-Consistency for truly high-stakes single decisions (not conversational); at 5 samples per query, it costs 5x tokens — budget explicitly

## AI-agent gotchas
- Reasoning tokens cost money: Extended Thinking tokens are billed at the same rate as output tokens — a 4,096-token thinking budget adds ~$0.30 per Opus call at current pricing; multiply by query volume
- CoT in agentic loops: if an agent generates a CoT plan before each tool call, token costs compound across turns — use CoT for the initial planning step, then switch to direct prompts for execution steps
- Thinking tokens are not cached: Prompt Caching applies to input tokens, not to Extended Thinking output — cannot amortize thinking cost across requests
- Human-in-loop checkpoint: for automated pipelines using Self-Consistency on high-stakes decisions (financial calculations, legal interpretations), log the disagreement rate across samples; if > 40% of samples disagree, escalate to human review rather than taking the majority vote
- Zero-Shot CoT can produce confidently wrong reasoning: always validate the final answer independently for numerical or verifiable claims — do not trust the reasoning trace alone

## References
- [Chain-of-Thought Prompting (Wei et al., 2022)](https://arxiv.org/abs/2201.11903)
- [Self-Consistency (Wang et al., 2022)](https://arxiv.org/abs/2203.11171)
- [Tree of Thoughts (Yao et al., 2023)](https://arxiv.org/abs/2305.10601)
- [Revisiting CoT Prompting (2025)](https://arxiv.org/abs/2506.14641)
- [Typed Chain-of-Thought (ICLR 2026)](https://arxiv.org/pdf/2510.01069)
- [Anthropic Extended Thinking guide](https://docs.anthropic.com/en/docs/build-with-claude/extended-thinking)
- [Prompt Engineering Guide - CoT](https://www.promptingguide.ai/techniques/cot)
