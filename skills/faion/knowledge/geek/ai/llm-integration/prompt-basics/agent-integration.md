# Agent Integration — Prompt Basics

## When to use
- Any pipeline step where an LLM call needs consistent, parseable output
- Before investing in fine-tuning — prompt engineering resolves most output consistency issues
- When agent inner-loop outputs are unreliable or hallucinating
- Setting up few-shot examples to teach a model a new output schema
- Encoding role, constraints, and output format into a reusable `PromptTemplate`

## When NOT to use
- When task complexity genuinely requires multi-step reasoning (use Chain-of-Thought or ReAct instead)
- When output schema is critical and must be guaranteed (use Structured Outputs with Pydantic)
- When token budget is the bottleneck — elaborate system prompts eat context; prefer shorter system + structured output enforcement

## Where it fails / limitations
- Zero-shot fails on novel output schemas — model guesses format without examples
- Few-shot example quality matters more than quantity; bad examples poison output
- Prompt injection via user-controlled content can override system prompt constraints
- Long, nested system prompts degrade following accuracy on complex tasks (model "forgets" later constraints)
- Without versioning, prompt drift goes undetected — silent regression in output quality
- Chain-of-Thought adds latency and tokens; not appropriate for high-throughput pipelines

## Agentic workflow
Agents use `PromptTemplate` objects as the interface between task spec and LLM call. A subagent receives a structured task description, fills variables into a template, calls the LLM, and validates the output against the expected schema. System prompts should be stable and cached (Anthropic cache_control, OpenAI prompt caching); only the user turn varies per call. Prompt versions should be stored in code, not databases, for diff-ability.

### Recommended subagents
- `faion-sdd-executor-agent` — uses prompt templates per SDD phase (spec, design, impl); each phase has its own system prompt and output schema
- `nero-sdd-executor-agent` — same pattern for NERO tasks

### Prompt pattern
```python
# Minimal PromptTemplate for agent use
from dataclasses import dataclass, field
from typing import List, Dict

@dataclass
class PromptTemplate:
    system: str
    user_template: str
    examples: List[Dict] = field(default_factory=list)

    def render(self, **kwargs) -> List[Dict]:
        msgs = [{"role": "system", "content": self.system}]
        for ex in self.examples:
            msgs += [
                {"role": "user", "content": ex["input"]},
                {"role": "assistant", "content": ex["output"]}
            ]
        msgs.append({"role": "user", "content": self.user_template.format(**kwargs)})
        return msgs
```

```python
# Zero-shot with explicit output format
EXTRACT_TEMPLATE = PromptTemplate(
    system="Extract the requested fields. Return only valid JSON, no prose.",
    user_template="Text: {text}\n\nReturn: {{\"sentiment\": str, \"topics\": [str]}}"
)
msgs = EXTRACT_TEMPLATE.render(text="The product is great but shipping was slow!")
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `promptfoo` | Prompt evaluation, regression testing | `npm install -g promptfoo` → https://promptfoo.dev |
| `langfuse` CLI | Prompt versioning, tracing | `pip install langfuse` → https://langfuse.com |
| `tiktoken` | Count tokens before sending | `pip install tiktoken` |
| `dotenv` | Manage API keys per environment | `pip install python-dotenv` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Langfuse | OSS/SaaS | Yes | Prompt versioning, tracing, evaluation; self-hostable |
| PromptLayer | SaaS | Yes | Prompt history, A/B testing, cost tracking per template |
| Helicone | SaaS | Yes | Logs all calls with metadata; filter by prompt version |
| Anthropic Console | SaaS | Partial | Manual prompt playground, not scriptable directly |
| OpenAI Playground | SaaS | Partial | Good for iteration, not for automated testing |

## Templates & scripts
See `templates.md` for full PromptTemplate class with few-shot support. Short inline helper for system prompt construction:

```python
def build_system(role: str, constraints: list[str], output_format: str = "") -> str:
    parts = [f"You are {role}."]
    if constraints:
        parts.append("Constraints:\n" + "\n".join(f"- {c}" for c in constraints))
    if output_format:
        parts.append(f"Output format:\n{output_format}")
    return "\n\n".join(parts)

system = build_system(
    role="a JSON extraction agent",
    constraints=["Return only valid JSON", "Never add prose or markdown"],
    output_format='{"field1": "string", "field2": ["list"]}'
)
```

## Best practices
- Store prompt templates as code constants, not runtime strings — enables `git diff` on prompt changes
- Use delimiters (`"""`, `<text>`, `---`) to separate instructions from user-supplied content
- Limit few-shot examples to 3–5 high-quality pairs; more does not reliably improve accuracy
- Place the output format instruction last in the user message — models follow the most recent constraint
- Test prompts against adversarial inputs (empty, malformed, injection attempts) before shipping
- Separate extraction prompts (deterministic, `temperature=0`) from generation prompts (`temperature=0.7+`)
- Cache stable system prompts (Anthropic `cache_control`, OpenAI prompt cache) to cut costs on repetitive pipelines
- Version prompts with semantic IDs (`extract-v2`, `classify-v1`) logged alongside every LLM call

## AI-agent gotchas
- Prompt injection: user-supplied text in the user turn can contain "Ignore previous instructions" — sanitize or wrap in XML tags and instruct model to treat content as data, not instructions
- Model updates silently break prompts that rely on model-specific quirks — run regression tests after any model version change
- `system` prompt truncation at context limit: very long system prompts get cut first on some providers — keep system under 2K tokens for safety
- Few-shot order matters: last example has highest influence; put the most representative example last
- Asking the model to "return ONLY JSON" still fails occasionally — always `try/except json.loads` and retry with a corrective message
- Temperature 0 is not fully deterministic across providers or after model updates — do not assume identical outputs in production

## References
- https://platform.openai.com/docs/guides/prompt-engineering
- https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview
- https://www.promptingguide.ai/
- https://learnprompting.org/
- https://github.com/brexhq/prompt-injection
