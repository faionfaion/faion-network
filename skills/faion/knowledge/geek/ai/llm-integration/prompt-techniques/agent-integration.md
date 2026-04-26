# Agent Integration — Advanced Prompt Techniques

## When to use
- A prompt is underperforming (wrong format, missing edge cases, hallucinating) and needs systematic improvement via meta-prompting or A/B testing
- A pipeline has multiple discrete LLM steps that should be decoupled into a PromptChain for maintainability
- The project needs a versioned PromptLibrary so prompts can be updated without code deployments
- You need to validate prompt accuracy against a known test set before releasing a new version
- Prompt injection or delimiter confusion is causing failures in production

## When NOT to use
- The prompt is simple (<50 words) and passes manual inspection — over-engineering with libraries adds maintenance cost
- The task changes frequently; a rigid PromptLibrary with versioning becomes a burden if prompts are iterated daily
- You need model-specific optimizations (e.g., Anthropic XML tags vs. OpenAI system messages) — a cross-provider library hides these differences and can regress quality
- Budget is tight and meta-prompting (using GPT-4o to generate prompts) doubles token cost on every iteration

## Where it fails / limitations
- Meta-prompting produces prompts that work on the generating model but underperform on a smaller/different target model
- PromptChain error propagation: an error in step N produces garbage that step N+1 silently accepts, making root cause analysis hard
- A/B testing requires a stable evaluator; LLM-as-evaluator is itself non-deterministic and can flip results between runs
- `PromptLibrary.format()` with `{variable}` in templates breaks if the input contains literal curly braces — must escape `{{` / `}}`
- Prompt versioning without a test suite is theater; bumping versions without accuracy tracking gives false confidence

## Agentic workflow
A subagent performing prompt optimization should: read the current prompt, run it against 5-10 representative test cases, identify the failure pattern, invoke meta-prompting to generate a candidate improvement, then A/B test the candidate against the original before replacing. The cycle runs as a loop until accuracy meets a defined threshold or a maximum iteration count is reached. For PromptChain, each step should be a named function — this makes the chain readable in code review and debuggable by logging `step.input` and `step.output` at each stage.

### Recommended subagents
- General-purpose subagent — execute meta-prompt generation and A/B evaluation cycles
- `faion-sdd-executor-agent` — implement PromptLibrary and PromptTester as SDD tasks with test coverage

### Prompt pattern
```
You are a prompt engineer. The following prompt produces these failure cases: {failures}.
Rewrite the prompt to address the failures while preserving the original intent.
Output only the improved prompt, no explanation.
Original: {original_prompt}
```

```
Evaluate if the LLM output matches the expected answer.
Output JSON: {"match": true/false, "reason": "<one sentence>"}
Output: {output}
Expected: {expected}
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `promptfoo` | Prompt testing and comparison CLI | `npm i -g promptfoo` / [promptfoo.dev](https://promptfoo.dev) |
| `python -m pytest` | Run PromptTester test cases | system |
| `langfuse` CLI | Trace prompt versions and A/B results | [langfuse.com/docs](https://langfuse.com/docs) |
| `weave` (Weights & Biases) | Log prompt experiments | `pip install weave` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Promptfoo | OSS | Yes | YAML-defined test cases, multi-provider; runs in CI |
| Langfuse | OSS/SaaS | Yes | Prompt versioning, tracing, A/B via SDK; self-hostable |
| Anthropic Prompt Console | SaaS | Partial | Browser-based; no API for running evaluations |
| PromptLayer | SaaS | Yes | Prompt versioning + analytics; proxy approach |
| Weights & Biases Weave | SaaS | Yes | Experiment tracking with prompt diff views |

## Templates & scripts
See `templates.md` for the PromptLibrary, PromptTester, and PromptABTest class templates.

Inline XML delimiter formatter (concise):
```python
def xml_prompt(instruction: str, **sections: str) -> str:
    """Format prompt with XML-style section tags."""
    body = "\n\n".join(f"<{k}>\n{v}\n</{k}>" for k, v in sections.items())
    return f"{instruction}\n\n{body}"
```

## Best practices
- Use XML tags (`<document>`, `<question>`) rather than triple-backtick delimiters for Anthropic models; backticks work better for OpenAI
- Version every prompt that reaches production; store name + version + accuracy score together, not just the prompt text
- Never use LLM-as-sole-evaluator in A/B tests; pair it with at least one deterministic check (regex, JSON schema validation)
- Prompt chaining: keep each step's output to the minimum needed for the next step — passing full verbatim outputs bloats context and costs
- When using meta-prompting to generate prompts, specify the target model in the meta-prompt; prompts optimized for GPT-4o degrade on Haiku

## AI-agent gotchas
- Variable substitution: PromptLibrary templates use Python `.format()`; if user input contains `{text}` literally, it raises `KeyError` — sanitize inputs before formatting
- Prompt injection via user data: XML tag injection (`</document><injection>`) in untrusted input can break structured prompts — wrap user content in a neutral delimiter and strip close-tags before insertion
- Human checkpoint needed before deploying a new prompt version to production without a passing test suite; automated meta-prompt improvements can introduce regressions that only appear on edge-case inputs
- Chained prompts accumulate latency; a 5-step chain with 2s average latency per step = 10s total — subagents should parallelize independent chain branches when possible
- PromptABTest winner selection is sensitive to test set size; with <20 test cases, random variance can declare a losing prompt as "winner" — use at least 50 diverse cases for reliable comparison

## References
- [OpenAI Prompt Engineering Guide](https://platform.openai.com/docs/guides/prompt-engineering)
- [Anthropic Prompt Engineering](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering)
- [Promptfoo docs](https://promptfoo.dev/docs/intro)
- [Promptingguide.ai](https://www.promptingguide.ai/)
- [Langfuse prompt management](https://langfuse.com/docs/prompts/get-started)
