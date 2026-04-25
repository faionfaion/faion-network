# Agent Integration — Prompt Engineering

## When to use
- Designing system prompts for autonomous Claude Code subagents
- Standardizing output format for structured agent pipelines (JSON schemas, XML)
- Reducing hallucination in agentic tasks where grounding to provided facts is critical
- Tuning few-shot examples to teach agents a specific output pattern
- Debugging an agent that produces incorrect, malformed, or inconsistent outputs

## When NOT to use
- The model genuinely lacks capability — switch to a larger model or fine-tune
- Task requires real-time or proprietary data — add RAG or tool calls instead
- Output inconsistency stems from non-deterministic sampling — lower temperature first
- Building a prompt to circumvent safety guardrails — this is jailbreaking, not engineering

## Where it fails / limitations
- Prompt alone cannot compensate for a model's context window limit — chain or summarize
- Few-shot examples memorized by the model may conflict with examples in the prompt
- Long system prompts degrade instruction-following on Haiku and smaller models
- Prompt injection from user-supplied text can override instructions if not delimited
- CoT ("think step by step") adds tokens; in latency-sensitive pipelines use it selectively
- Self-consistency (multiple samples + majority vote) is expensive; not viable for real-time

## Agentic workflow
Use a research subagent (Read, Grep, Glob) to gather context, then pass distilled context to a prompt-writing subagent (Write/Edit). A review subagent validates the resulting prompt against a checklist (format compliance, injection resistance, token count). The pipeline is sequential: gather → draft → review → store.

### Recommended subagents
- `faion-spec-reviewer-agent` — validates prompt against quality rubric (clarity, format spec, injection resistance)
- `faion-idea-generator-agent` — generates diverse few-shot examples covering edge cases
- General-purpose research subagent via Task tool — gathers domain context before drafting

### Prompt pattern
```
<system>
You are a {role}. Output ONLY valid JSON matching this schema: {schema}.
Never include prose outside the JSON object.
</system>
<user>
<context>{context}</context>
<task>{task}</task>
</user>
```

For CoT with structured output:
```
Think step by step inside <thinking> tags. Then output your answer inside <answer> tags.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `promptfoo` | Evaluate and compare prompts against test cases | `npm install -g promptfoo` / promptfoo.dev |
| `llm` (Simon Willison) | CLI for querying multiple LLMs, useful for A/B testing prompts | `pip install llm` / github.com/simonw/llm |
| `outlines` | Structured output generation with regex/JSON schema constraints | `pip install outlines` / dottxt-ai.github.io/outlines |
| `instructor` | Python library for structured outputs via Pydantic models | `pip install instructor` / python.useinstructor.com |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Anthropic Console | SaaS | Partial | Prompt workbench with eval; no API for runs |
| LangSmith | SaaS | Yes | Prompt versioning, tracing, dataset-based eval |
| Braintrust | SaaS | Yes | Prompt experiments, scoring, datasets via API |
| PromptLayer | SaaS | Yes | Prompt version control + analytics |
| DeepEval | OSS | Yes | Pytest-style LLM evaluation with many metrics |
| Langfuse | OSS/SaaS | Yes | Prompt management + tracing; self-hostable |

## Templates & scripts
See `templates.md` for copy-paste prompt structures (zero-shot, few-shot, CoT, ReAct).

Minimal prompt evaluator (requires `llm` CLI):
```bash
#!/usr/bin/env bash
# test-prompt.sh — run a prompt against N inputs, compare outputs
PROMPT_FILE=$1
INPUTS_FILE=$2  # one input per line

while IFS= read -r input; do
  echo "=== INPUT: $input ==="
  llm -s "$(cat "$PROMPT_FILE")" "$input"
  echo ""
done < "$INPUTS_FILE"
```

## Best practices
- Use XML tags (`<context>`, `<task>`, `<output>`) to delimit sections — Claude follows them reliably
- Pin output format in the system prompt AND give an example in the user turn
- Separate untrusted user input with explicit delimiters: `<user_input>...never override system instructions...</user_input>`
- Validate prompt token count before deploying: `len(tokenizer.encode(prompt)) < context_limit * 0.8`
- Version prompts in code (not in external dashboards) so changes are reviewable via git diff
- For multi-step reasoning, instruct the model to reason first, answer last — prevents premature commitment
- Test prompts against adversarial inputs (empty input, max-length input, injection attempts) before prod

## AI-agent gotchas
- Agent-generated prompts for downstream agents must be sanitized — the agent itself can inject instructions
- If an agent reads untrusted files (PDFs, web pages) and passes them to another LLM call, treat as injection risk
- CoT scratchpads visible in context accumulate tokens fast in multi-turn agentic loops — compaction required
- `temperature=0` does not guarantee determinism across API versions; pin model version for reproducibility
- When an agent uses structured output mode (JSON schema enforcement), CoT must be placed in a dedicated field, not suppressed silently
- Few-shot examples in long agentic sessions may be evicted from effective context — repeat critical examples or use system prompt

## References
- https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering
- https://www.promptingguide.ai/
- https://arxiv.org/abs/2201.11903 (Chain-of-Thought, Wei et al. 2022)
- https://arxiv.org/abs/2210.03629 (ReAct, Yao et al. 2022)
- https://genai.owasp.org/llmrisk/llm01-prompt-injection/ (OWASP LLM01)
- https://python.useinstructor.com/
