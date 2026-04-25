# Agent Integration — LangChain Chains

## When to use
- Composing discrete LLM steps in a linear pipeline where each step transforms and passes output to the next
- Routing user input to specialized handlers (code, math, general) without maintaining state between requests
- Parallel execution of independent sub-tasks (summarize + extract + classify) in a single LLM call batch
- Building resilient pipelines where a primary model may fail and a fallback must take over transparently
- Prompt engineering iteration — LCEL chain composition makes it easy to swap prompt templates, models, or parsers without restructuring code

## When NOT to use
- The pipeline needs to loop, retry with modified state, or maintain context between steps — use LangGraph
- You need tool use (web search, database queries) inside the pipeline — LangGraph agent with tools is the right primitive
- The "chain" would consist of a single prompt + model call — use the model directly without LCEL overhead
- Output parsing is complex with multiple fallback formats — `with_structured_output()` with function calling is more reliable than chaining parsers
- The team needs visual workflow debugging — LangGraph's graph structure is far easier to inspect than nested LCEL chains

## Where it fails / limitations
- `RunnableBranch` does not support dynamic routing keys computed at runtime — all branch conditions must be lambda functions known at definition time
- MapReduce via `RunnableParallel` does not support true async fan-out; parallel dict keys execute synchronously in CPython without explicit async
- `chain.with_retry()` uses exponential backoff but does not distinguish between retryable errors (rate limit) and non-retryable ones (auth failure) — both trigger retry
- `FewShotChatMessagePromptTemplate` with `SemanticSimilarityExampleSelector` requires a vector store; this dependency is non-obvious for newcomers
- LCEL pipe operator `|` has no built-in timeout; a hung model call blocks indefinitely without explicit `asyncio.wait_for()` wrapping
- `StrOutputParser` does not validate output format — downstream steps that expect structured data fail with confusing errors if the model returns prose

## Agentic workflow
An agent uses LCEL chains as composable building blocks for individual task types. A routing subagent classifies the input and selects the appropriate chain; a specialist subagent runs the selected chain and returns structured output. For batch processing, an orchestrator agent fans out multiple chain invocations using `asyncio.gather()` and collects results for aggregation. Chain definitions live in a registry so the orchestrating agent can select by name without knowing the implementation.

### Recommended subagents
- `faion-llm-cli-agent` — invokes named LCEL chains via CLI interface, handles prompt injection and output parsing
- General extraction subagent — receives raw text, runs extraction chain with `with_structured_output()`, returns Pydantic object

### Prompt pattern
```
You are a chain orchestrator. Select and run the correct chain for this input:
- If input is code → run "code_review_chain"
- If input is prose → run "summarize_chain"
- Otherwise → run "general_chain"

Input: "{user_input}"
Run the selected chain and return its output verbatim.
```

```
Run the following MapReduce chain on these {count} documents:
  Map step: summarize each document in 2 sentences
  Reduce step: synthesize summaries into one coherent paragraph
Documents: {documents_json}
Return: {"individual_summaries": [...], "synthesis": str}
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `langchain-cli` | Scaffold chains, serve via LangServe | `pip install langchain-cli` |
| `langserve` | Expose LCEL chains as REST endpoints | `pip install langserve` / https://python.langchain.com/docs/langserve |
| `langsmith` | Trace and debug each chain step | `pip install langsmith` / https://smith.langchain.com |
| `tenacity` | Retry logic with fine-grained control | `pip install tenacity` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| LangSmith | SaaS | Yes | Per-step tracing; essential for debugging parser failures |
| LangServe | OSS | Yes | Serves any LCEL chain as `/invoke`, `/stream`, `/batch` endpoints |
| LangChain Hub | SaaS | Yes | Pull versioned prompts with `hub.pull("username/prompt-name")` |
| Chroma | OSS | Yes | Required for `SemanticSimilarityExampleSelector` in few-shot chains |
| Redis | OSS | Yes | `RedisCache` for LLM response caching across chain invocations |

## Templates & scripts
See `templates.md` for chain composition templates. Inline MapReduce chain with async fan-out:

```python
import asyncio
from langchain_core.prompts import ChatPromptTemplate
from langchain_anthropic import ChatAnthropic
from langchain_core.output_parsers import StrOutputParser

model = ChatAnthropic(model="claude-opus-4-5")
parser = StrOutputParser()

summarize_chain = (
    ChatPromptTemplate.from_template("Summarize in 2 sentences:\n\n{document}")
    | model | parser
)
combine_chain = (
    ChatPromptTemplate.from_template("Synthesize these summaries:\n\n{summaries}")
    | model | parser
)

async def map_reduce(documents: list[str]) -> str:
    tasks = [summarize_chain.ainvoke({"document": d}) for d in documents]
    summaries = await asyncio.gather(*tasks)
    return await combine_chain.ainvoke({"summaries": "\n\n".join(summaries)})
```

## Best practices
- Use `with_structured_output(PydanticModel)` for any chain where downstream code depends on specific fields — this eliminates an entire class of parser failure bugs
- Define chains at module level, not inside request handlers — chain compilation happens once at import time; recreating chains per request wastes CPU
- Use `hub.pull("username/prompt")` for production prompts; storing prompts in version control separately from code creates drift
- For router chains, put the most common route as the last `RunnableBranch` condition checked via the default fallback — avoids all conditions returning False for unrecognized inputs
- Enable `LANGCHAIN_TRACING_V2=true` during development but disable in production unless you are actively monitoring — tracing adds latency per chain call
- When chaining model calls, set explicit `max_tokens` on each model to prevent runaway generation that exceeds downstream parser expectations
- Test each chain component (prompt, model output format, parser) independently before testing the full chain — isolating failures to a single component is much faster

## AI-agent gotchas
- `RunnableParallel` with a dict of chains blocks on the slowest chain; there is no timeout-per-branch — one slow chain blocks the entire parallel step
- Piping into `JsonOutputParser` on streaming mode returns partial JSON dicts that are valid Python but not yet complete — downstream agents that consume streaming events must handle partial objects
- `chain.batch([...])` calls each chain element sequentially in Python; for true parallelism use `asyncio.gather` with `chain.ainvoke` per element
- `FewShotChatMessagePromptTemplate` injects examples before the user message; large example sets can push user content below the model's effective attention window
- `with_fallbacks()` catches all exceptions by default, including auth errors and invalid API key errors — set `exceptions_to_handle` explicitly to avoid masking configuration bugs
- Output from one chain piped into another via LCEL must match the expected input dict key exactly; a key mismatch raises a KeyError at invocation time, not at chain definition time

## References
- https://python.langchain.com/docs/expression_language/
- https://python.langchain.com/docs/how_to/routing/
- https://python.langchain.com/docs/how_to/parallel/
- https://python.langchain.com/docs/how_to/fallbacks/
- LangChain LCEL cookbook: https://python.langchain.com/docs/expression_language/cookbook/
