# Agent Integration — LangChain Patterns

## When to use
- Building LLM applications that need composable, swappable components (prompt templates, parsers, retrievers)
- Implementing RAG pipelines where documents must be loaded, split, embedded, and retrieved
- Creating agents that need session-aware conversation memory across multiple turns
- Projects that require LLM provider flexibility (swap OpenAI for Anthropic without rewriting the chain)
- When LangSmith tracing is required for production observability

## When NOT to use
- Simple single-call LLM tasks — LCEL pipe syntax adds complexity with no benefit over a direct API call
- When you control the model exclusively (Claude-only) — the Anthropic SDK directly is simpler and cheaper
- Projects with strict latency SLAs where LCEL's serialization overhead matters
- When the team is unfamiliar with LangChain's abstraction layers — debugging failures requires deep framework knowledge
- When avoiding dependency bloat: `langchain` + `langchain-openai` + `langchain-community` adds ~200 transitive dependencies

## Where it fails / limitations
- LCEL's `RunnableParallel` is not truly parallel for I/O-bound tasks unless explicitly async; synchronous parallel calls still block
- `RunnableWithMessageHistory` stores session history in-memory by default; this is lost on process restart unless backed by a persistent store
- The `hub.pull()` pattern fetches prompts from LangSmith Hub at runtime — this fails silently in air-gapped or restricted network environments
- LangChain's community integrations (`langchain-community`) are maintained by contributors, not LangChain core; quality varies significantly
- Pydantic v1/v2 conflicts: LangChain's internal models use Pydantic v1 patterns; mixing with v2-native code in the same project causes type errors
- LangSmith tracing is opt-in but easy to forget; production agents running without tracing are nearly impossible to debug retrospectively

## Agentic workflow
A Claude subagent uses LCEL chains as composable building blocks: the orchestrator defines the chain topology (prompt → model → parser), the subagent executes it per task, and LangSmith captures the full execution trace. For RAG agents, the retriever runs as a parallel branch alongside the main chain. For multi-step agents, `AgentExecutor` with a `max_iterations` cap is the standard pattern. Haiku handles straightforward LCEL chain execution; Sonnet reviews chain outputs and detects reasoning errors; Opus handles chain architecture design when trade-offs between branching strategies are non-obvious.

### Recommended subagents
- `faion-sdd-executor-agent` — implements LangChain-based pipelines from SDD design specs

### Prompt pattern
```xml
<langchain_task>
  <goal>Build a RAG chain that answers questions about competitor pricing from uploaded PDFs</goal>
  <components>
    <loader>PyPDFLoader</loader>
    <splitter>RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)</splitter>
    <embeddings>OpenAIEmbeddings(model="text-embedding-3-small")</embeddings>
    <vectorstore>Chroma</vectorstore>
    <llm>ChatOpenAI(model="gpt-4o", temperature=0)</llm>
    <parser>StrOutputParser</parser>
  </components>
  <output>Working Python code. Include error handling. Use LCEL pipe syntax.</output>
</langchain_task>
```

```xml
<chain_review>
  <chain_code>{{chain_python}}</chain_code>
  <criteria>
    - Uses LCEL (not legacy Chain classes)
    - Memory cleared between sessions
    - Fallback configured for model calls
    - LangSmith tracing enabled
    - No blocking sync calls in async context
  </criteria>
  <output>Pass/fail per criterion with fix if failed</output>
</chain_review>
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `langchain` | Core LCEL framework | `pip install langchain` |
| `langchain-openai` | OpenAI model bindings | `pip install langchain-openai` |
| `langchain-anthropic` | Anthropic/Claude bindings | `pip install langchain-anthropic` |
| `langchain-community` | Community loaders, stores | `pip install langchain-community` |
| `langsmith` | Tracing and evaluation | `pip install langsmith` |
| `chromadb` | Local vector store for RAG | `pip install chromadb` |
| `pypdf` | PDF loading | `pip install pypdf` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| LangSmith | SaaS | Yes — SDK | Production tracing; required for debugging agents |
| LangChain Hub | SaaS | Yes — `hub.pull()` | Community prompt templates; network-dependent |
| Chroma | OSS | Yes | Local vector store; stateless by default |
| Pinecone | SaaS | Yes — REST | Hosted vector store for RAG in production |
| OpenAI API | SaaS | Yes | Primary model target in LangChain ecosystem |
| Anthropic API | SaaS | Yes — `langchain-anthropic` | Claude via LangChain; use `ChatAnthropic` |

## Templates & scripts
See `templates.md` for full chain templates including RAG, conversational, and branching patterns. Minimal production-ready chain with fallback and tracing:

```python
import os
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "my-project"

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a concise research assistant."),
    ("user", "{question}")
])

primary = ChatOpenAI(model="gpt-4o", temperature=0)
fallback = ChatAnthropic(model="claude-sonnet-4-5")
robust_llm = primary.with_fallbacks([fallback])

chain = prompt | robust_llm | StrOutputParser()
chain_with_retry = chain.with_retry(stop_after_attempt=3, wait_exponential_jitter=True)

answer = chain_with_retry.invoke({"question": "What is LCEL?"})
```

## Best practices
- Always use LCEL (`|` pipe syntax) instead of legacy `LLMChain`, `ConversationalChain` classes — they are deprecated and will be removed
- Enable LangSmith tracing from the start, not retroactively; adding it after deployment misses the history needed for debugging
- Back conversation memory with a persistent store (Redis, Postgres) via `RedisChatMessageHistory`; in-memory history is lost on restart
- Use `with_fallbacks()` on every production LLM call; model outages are common and chain failures propagate silently without it
- Pin `langchain`, `langchain-openai`, and `langchain-community` versions together; they have tight version coupling and mismatched versions cause hard-to-diagnose errors
- Test each chain component in isolation before composing; LCEL makes composition easy but debugging a composed chain from scratch is hard

## AI-agent gotchas
- `hub.pull()` fetches prompts at runtime from LangSmith Hub; if the Hub is down or the prompt is deleted, the chain fails with an unclear error
- `RunnableParallel` runs branches concurrently only in the async variant (`ainvoke`, `astream`); sync `invoke` runs branches sequentially despite the name
- `AgentExecutor` with `verbose=True` prints internal reasoning to stdout; in production this leaks intermediate state — disable it
- Pydantic validation errors in `PydanticOutputParser` are raised as exceptions, not returned as structured errors; the chain must catch and handle them explicitly
- `langchain-community` loaders (WebBaseLoader, PyPDFLoader) depend on external libraries that may not be installed; add explicit `try/except ImportError` guards
- Session IDs for `RunnableWithMessageHistory` must be unique per user session; reusing session IDs across users merges conversation histories

## References
- [LangChain LCEL Docs](https://python.langchain.com/docs/expression_language/)
- [LangSmith](https://smith.langchain.com/)
- [LangChain Hub](https://smith.langchain.com/hub)
- [LangChain Anthropic Integration](https://python.langchain.com/docs/integrations/chat/anthropic/)
- [LangGraph for Agents](https://langchain-ai.github.io/langgraph/)
- [Chroma Docs](https://docs.trychroma.com/)
