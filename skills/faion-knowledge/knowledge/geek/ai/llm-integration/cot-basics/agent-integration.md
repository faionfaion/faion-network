# Agent Integration — Chain-of-Thought Basics

## When to use
- Task requires multi-step reasoning: math, logic, code debugging, root cause analysis.
- Agent must explain its reasoning to a downstream consumer or auditor.
- Accuracy matters more than latency (self-consistency requires multiple calls).
- Structured decomposition is needed before calling external tools (plan before act).

## When NOT to use
- Simple lookup or classification tasks — CoT adds tokens with no accuracy gain.
- Latency-critical paths where a single token answer suffices.
- Tasks whose "steps" cannot be verified (e.g., pure creative generation) — overhead without benefit.
- High-volume pipelines where cost dominates; use zero-shot direct answering instead.

## Where it fails / limitations
- CoT improves but does not guarantee correctness; confident wrong reasoning chains still occur.
- Self-consistency requires N=3–7 LLM calls; cost scales linearly.
- On very long reasoning chains the model can drift from the original question ("lost in thought").
- Extracting the final answer reliably from free-form CoT text requires a second parsing step or a forced answer marker.
- Few-shot examples that contain domain errors propagate those errors to outputs.
- Claude's extended thinking (`budget_tokens`) is non-deterministic; budget undershoot can truncate reasoning mid-chain.

## Agentic workflow
A subagent receives the task and a CoT trigger in its system prompt. It emits a reasoning block followed by a structured answer. A second, lightweight judge subagent checks the reasoning for internal consistency and flags anomalies. For high-stakes decisions the orchestrator runs self-consistency: spawns N=5 parallel reasoner calls, extracts the answer token from each, and takes the majority vote. The final answer plus the winning reasoning chain are passed downstream.

### Recommended subagents
- `reasoner` — Runs the CoT prompt; emits `<reasoning>` + `<answer>` XML blocks.
- `consistency-judge` — Receives N answers, votes on majority, returns confidence score.
- `answer-extractor` — Parses free-form CoT output to extract the final answer reliably.

### Prompt pattern
```xml
<system>
You are a reasoning engine. Think step by step before answering.
Structure output as:
<reasoning>step-by-step analysis</reasoning>
<answer>final answer only</answer>
</system>
```

Self-consistency extraction:
```python
# After N calls, extract answer tokens and vote
answers = [extract_answer(resp) for resp in responses]
winner = Counter(answers).most_common(1)[0]
confidence = winner[1] / len(answers)
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `llm` (Simon Willison) | Run CoT prompts against any model from CLI | `pip install llm` / github.com/simonw/llm |
| `guidance` | Constrained generation with step delimiters | `pip install guidance` / github.com/guidance-ai/guidance |
| `dspy` | Compile + optimize CoT prompts automatically | `pip install dspy-ai` / dspy.ai |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Anthropic Messages API (`thinking` param) | SaaS | Yes | Native extended thinking; returns `thinking` blocks separately |
| OpenAI o1/o3 series | SaaS | Yes | Reasoning done server-side; no explicit CoT in response |
| DSPy Teleprompter | OSS | Yes | Auto-optimizes CoT few-shot examples via labeled data |
| Weights & Biases Prompts | SaaS | Partial | Logs CoT traces for debugging; no agent control plane |

## Templates & scripts
See `templates.md` for zero-shot, few-shot, and self-consistency templates.

Self-consistency loop (under 50 lines):
```python
from collections import Counter
import anthropic

client = anthropic.Anthropic()

def self_consistency(problem: str, n: int = 5) -> tuple[str, float]:
    answers = []
    for _ in range(n):
        msg = client.messages.create(
            model="claude-opus-4-5-20251101",
            max_tokens=2048,
            messages=[{
                "role": "user",
                "content": f"{problem}\n\nThink step by step. End with 'Answer: <value>'"
            }]
        )
        text = msg.content[0].text
        if "Answer:" in text:
            answers.append(text.split("Answer:")[-1].strip().split()[0])
    if not answers:
        return "", 0.0
    top, count = Counter(answers).most_common(1)[0]
    return top, count / len(answers)
```

## Best practices
- Append the CoT trigger (`Let's think step by step.`) at the end of the user turn, not in the system prompt — it activates reasoning for that specific message only.
- Always request an explicit answer marker (`Answer: X`) to decouple reasoning from extraction.
- Cache the system prompt + few-shot examples with `cache_control: ephemeral`; only the problem varies.
- For Claude, prefer `extended thinking` over manual CoT when accuracy is paramount — it uses a private scratchpad and avoids the parsing overhead.
- Limit few-shot examples to 2–3 high-quality chains; more examples do not always improve accuracy and inflate input tokens.
- Never embed CoT examples that contain arithmetic errors — models imitate the style including mistakes.

## AI-agent gotchas
- Answer extraction can fail if the model ends with prose instead of the marker — always validate the extracted answer matches the expected format before propagating it downstream.
- Extended thinking (`budget_tokens`) consumed cannot be cached; budget overruns increase cost silently — set explicit `max_tokens` guard above the budget.
- Self-consistency with `temperature=0` collapses to a single deterministic path — set `temperature >= 0.6` to get meaningful diversity across samples.
- LLM reasoning chains are not auditable facts; never pass them to external tools as verified inputs without a validation step.
- Human-in-loop checkpoint: when confidence from self-consistency is below 0.6, route to human review rather than proceeding with the majority answer.

## References
- https://arxiv.org/abs/2201.11903 — Chain-of-Thought Prompting Elicits Reasoning in Large Language Models
- https://arxiv.org/abs/2203.11171 — Self-Consistency Improves Chain of Thought Reasoning
- https://docs.anthropic.com/en/docs/build-with-claude/extended-thinking — Claude Extended Thinking
- https://dspy.ai — DSPy: automatic prompt optimization including CoT chains
