# Agent Integration — LangChain Basics

## When to use
- Building sequential LLM pipelines where output of one step feeds the next (prompt → model → parser)
- You need rapid structured output with Pydantic validation via `with_structured_output()`
- The task is prompt engineering and chain composition, not stateful agent loops
- Streaming output to a user interface is required — LCEL chains support `.stream()` natively
- Team wants LangSmith observability out of the box with minimal configuration

## When NOT to use
- You need stateful multi-step agents with conditional branching — use LangGraph instead
- Pure document retrieval/RAG is the primary concern — LlamaIndex handles indexing better
- The pipeline has no LLM calls — plain Python functions with no framework overhead are simpler
- You need agentic memory, tool loops, or human-in-the-loop — all require LangGraph
- Latency is critical and you want to minimize abstraction layers; direct Anthropic SDK calls are faster

## Where it fails / limitations
- LCEL chains serialize as Runnables; complex branching with RunnableBranch becomes hard to read beyond 3 routes
- `JsonOutputParser` is unreliable with smaller models — use `with_structured_output()` with function calling instead
- `InMemoryCache` for LLMs is process-local; doesn't survive restarts or scale across workers
- LangChain version pinning is essential — breaking changes between 0.1, 0.2, 0.3 are common
- `get_openai_callback()` only tracks OpenAI costs; no built-in cost tracking for Anthropic
- MapReduce with `RunnableParallel` on large lists can exhaust API rate limits with no built-in backoff

## Agentic workflow
An orchestrating agent defines the task as a chain composition: prompt template, model call, output parser. It invokes the chain via a subagent, receives structured output, and continues its own reasoning loop. For repeated or templated generation tasks (email drafting, code review comments, data extraction), wrap the LCEL chain in a tool that the parent agent calls by name. The chain handles low-level LLM interaction; the agent handles task decomposition and state.

### Recommended subagents
- `faion-llm-cli-agent` — drives LangChain chains from CLI, handles prompt injection, returns structured JSON
- General code/content generation subagent — receives a task description, selects the appropriate prompt template and model, returns structured output

### Prompt pattern
```
You are a structured extraction agent. Use the following chain:
  prompt: extract_prompt | model: claude-opus-4-5 | parser: JsonOutputParser(schema=ExtractedData)
Input text: "{text}"
Return the parsed ExtractedData JSON only.
```

```
Run the router chain to classify this query as one of [research, code, write].
Query: "{input}"
Then invoke the matching specialist chain and return the result.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `langchain-cli` | Scaffold LangChain apps and serve chains | `pip install langchain-cli` / https://python.langchain.com/docs/langserve |
| `langsmith` | Trace, evaluate, monitor chains | `pip install langsmith` / https://smith.langchain.com |
| `langgraph-cli` | Local LangGraph dev server | `pip install langgraph-cli` / https://langchain-ai.github.io/langgraph |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| LangSmith | SaaS | Yes | Trace every chain call; set `LANGCHAIN_TRACING_V2=true` |
| LangServe | OSS | Yes | Serve LCEL chains as REST API endpoints |
| LangChain Hub | SaaS | Yes | Versioned prompt repository; pull prompts by commit hash |
| LangGraph Cloud | SaaS | Yes | Managed stateful agent runtime |
| Chroma | OSS | Yes | Vector store for few-shot example selector |
| Supabase pgvector | SaaS/OSS | Yes | Persistent vector store with `langchain-community` |

## Templates & scripts
See `templates.md` for chain composition templates. Inline structured extraction chain:

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_anthropic import ChatAnthropic
from pydantic import BaseModel, Field

class Extraction(BaseModel):
    entities: list[str] = Field(description="Named entities found")
    sentiment: str = Field(description="positive | neutral | negative")
    summary: str = Field(description="One sentence summary")

model = ChatAnthropic(model="claude-opus-4-5")
structured_model = model.with_structured_output(Extraction)

prompt = ChatPromptTemplate.from_messages([
    ("system", "Extract entities, sentiment, and summary from the text."),
    ("human", "{text}")
])

chain = prompt | structured_model

result = chain.invoke({"text": "Apple reported record Q1 profits despite market uncertainty."})
print(result.model_dump())
```

## Best practices
- Prefer `model.with_structured_output(PydanticModel)` over `JsonOutputParser` — function calling is more reliable than prompt-based JSON extraction
- Pin `langchain`, `langchain-core`, and provider packages to exact versions in `requirements.txt`; minor version bumps routinely change interfaces
- Use `RunnableParallel` for independent tasks in a pipeline step, not for parallel agent spawning — LangGraph is the right primitive for that
- Always configure LangSmith in non-production environments during development; traces are invaluable for debugging prompt failures
- Set `chain.with_retry(stop_after_attempt=3)` on any chain that calls an external API — transient network errors are common
- Prefer `chain.astream()` for user-facing outputs; streaming reduces perceived latency significantly even when total tokens are the same
- Use `partial()` on prompt templates to pre-fill static fields (system instructions, format specs) at definition time, not at call time
- Keep chains stateless — pass all context through `invoke()` input dict, not through closures or module-level state

## AI-agent gotchas
- LCEL `|` operator is eager at definition time — referencing a variable that's `None` at chain construction raises immediately, not at invocation
- `RunnableBranch` evaluates all conditions sequentially; the first `True` wins — order matters and is not obvious from code structure alone
- `with_structured_output()` requires function-calling support from the model; it silently falls back to prompt-based parsing with models that don't support it
- LangSmith traces are async; they may not appear instantly — don't rely on them for real-time decision making inside agent loops
- `StreamingStdOutCallbackHandler` conflicts with async chains — use `astream_events()` instead for async streaming
- Cost tracking via `get_openai_callback()` is a context manager — forgetting to wrap the call means no cost data; integrate cost checks as a post-step validation, not runtime guard

## References
- https://python.langchain.com/docs/
- https://python.langchain.com/docs/expression_language/ (LCEL)
- https://smith.langchain.com/
- https://github.com/langchain-ai/langchain
- LangChain changelog: https://github.com/langchain-ai/langchain/releases
