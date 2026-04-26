# Agent Integration — LangChain Memory

## When to use
- Building conversational AI where users reference earlier turns ("as I mentioned before…")
- Long-running multi-session assistants that must recall user preferences, entities, or prior decisions
- Stateful LangGraph workflows where each node must read and update shared state
- Human-in-the-loop approval workflows that must persist state across a pause-and-resume cycle
- Content pipelines where upstream node output must be accessible to downstream nodes without full re-processing

## When NOT to use
- Single-turn, stateless question-answering — memory adds latency and cost with no benefit
- Tasks where conversation history is irrelevant or where fresh context is preferred each turn
- Extremely long sessions (thousands of turns) where even vector memory retrieval becomes a bottleneck
- High-security contexts where persisting conversation history creates unacceptable data retention risk
- Serverless functions with no persistent storage — buffer and summary memory require a store backend

## Where it fails / limitations
- **Buffer Memory**: grows linearly; a 200-turn conversation can easily exceed a 128k context window
- **Summary Memory**: summarization compresses and may lose details that were not salient to the summarizer but matter later; irreversible loss
- **Vector Memory**: embedding a query and retrieving top-K returns semantically similar, not necessarily causally relevant, past interactions; can surface unrelated turns
- **Entity Memory**: LLM extraction of entities is imperfect; rare or ambiguous entity names are merged or lost
- **LangGraph state**: complex `TypedDict` schemas with many accumulating fields bloat the checkpoint store and slow persistence
- **In-memory stores**: `InMemoryChatMessageHistory` and `MemorySaver` do not survive process restarts; production use requires Redis, PostgreSQL, or equivalent
- **Session ID collisions**: sharing a session ID across users leaks conversation history between them; a critical security failure

## Agentic workflow
A Claude subagent uses LangChain memory wrappers to maintain conversation context across invocations within a session. For multi-session persistence, the subagent connects to a Redis or PostgreSQL backend via `RedisChatMessageHistory` or `SQLChatMessageHistory`. For complex state machines, LangGraph wraps the agent in a `StateGraph` with typed state, conditional routing, and `MemorySaver` checkpointing so workflows survive interruptions and resume exactly where they paused.

### Recommended subagents
- `conversational-agent` — uses `RunnableWithMessageHistory` + buffer or summary memory for ongoing user conversations; uses Sonnet
- `entity-tracker` — extracts and maintains entity knowledge from conversation turns; uses Haiku for extraction, Sonnet for reasoning
- `workflow-node` — individual LangGraph node that reads/writes typed `WorkflowState`; uses appropriate model for its task
- `hitl-approver` — LangGraph node that pauses at `interrupt_before` and waits for human input before resuming; uses Sonnet

### Prompt pattern
Conversational agent with memory:
```xml
<system>You are a helpful assistant. Use the conversation history to maintain context.</system>
<history>{{history_messages}}</history>
<user_input>{{current_message}}</user_input>
<instruction>Respond using prior context where relevant. Be concise.</instruction>
```

Entity-aware response:
```xml
<known_entities>{{entity_store_json}}</known_entities>
<user_input>{{message}}</user_input>
<instruction>Use the known entities to personalize your response. Update entities if new information is provided.</instruction>
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `langchain` | Core memory abstractions and `RunnableWithMessageHistory` | `pip install langchain` / python.langchain.com |
| `langgraph` | State machine graphs with checkpointing and human-in-loop | `pip install langgraph` / langchain-ai.github.io/langgraph |
| `langchain-community` | Community backends: Redis, PostgreSQL, MongoDB message history | `pip install langchain-community` / pypi |
| `langchain-openai` | OpenAI chat models and embeddings for memory retrieval | `pip install langchain-openai` / pypi |
| `redis` (Python) | Fast in-memory store for `RedisChatMessageHistory` | `pip install redis` / redis.io/docs |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Redis Cloud | SaaS | Yes | Managed Redis for `RedisChatMessageHistory`; sub-ms reads |
| Upstash | SaaS | Yes | Serverless Redis; per-request pricing, good for low-volume agents |
| LangGraph Cloud | SaaS | Yes | Managed LangGraph with `MemorySaver` backed by persistent store |
| Supabase (PostgreSQL) | SaaS/OSS | Yes | `SQLChatMessageHistory` backend; row-level security for session isolation |
| Chroma | OSS | Yes | Embedded vector store for `VectorMemory`; zero-config local setup |
| Pinecone | SaaS | Yes | Managed vector store for production-scale `VectorMemory` |

## Templates & scripts
See `templates.md` for `SummaryMemory`, `VectorMemory`, `EntityMemory`, and LangGraph workflow implementations.

Session-safe Redis memory setup (≤20 lines):
```python
from langchain_community.chat_message_histories import RedisChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

def get_session_history(session_id: str):
    # Use unique session_id per user — never share across users
    return RedisChatMessageHistory(
        session_id=session_id,
        url="redis://localhost:6379",
        ttl=3600  # expire after 1 hour of inactivity
    )

chain_with_memory = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history"
)
```

## Best practices
- Always use user-scoped session IDs — never a shared or static string
- Set TTL on all session history stores; conversation data should not persist indefinitely by default
- For conversations >10 turns, switch from buffer to summary memory to cap token cost
- For conversations >50 turns or where semantic retrieval matters, switch to vector memory
- In LangGraph workflows, keep `WorkflowState` schemas flat — deeply nested dicts are hard to checkpoint and debug
- Use `interrupt_before` at destructive LangGraph nodes; never rely on in-graph checks to substitute for human approval of irreversible actions
- Log memory reads and writes with session ID, timestamp, and token count; memory is the most common source of cost surprises in production conversational agents
- Purge or anonymize session histories according to your data retention policy before storing in external backends

## AI-agent gotchas
- **Session ID leakage**: if session IDs are predictable (e.g. user's email), an attacker can retrieve another user's history. Use UUIDs, not user-readable identifiers.
- **InMemoryChatMessageHistory in production**: works in dev, loses all sessions on process restart. Replace with Redis or PostgreSQL before deploying.
- **Summary Memory irreversibility**: once old messages are summarized, the original text is gone. If an agent needs to re-examine a specific past message, it cannot. Archive raw history to a separate log if auditability matters.
- **LangGraph state size growth**: `Annotated[List[str], operator.add]` fields accumulate forever. Add a compaction step every N messages to prevent checkpoint bloat.
- **Human-in-loop resume**: after an `interrupt_before` pause, resuming with `workflow.invoke(None, config)` re-reads from checkpoint. Ensure the checkpoint store is durable; if it fails, the workflow cannot resume.
- **Context contamination**: vector memory retrieves past interactions across sessions if you use a shared collection without filtering by session ID. Always filter retrievals by `session_id` metadata.

## References
- LangChain memory docs: https://python.langchain.com/docs/modules/memory/
- LangGraph concepts: https://langchain-ai.github.io/langgraph/concepts/
- LangGraph human-in-the-loop: https://langchain-ai.github.io/langgraph/how-tos/human_in_the_loop/
- RedisChatMessageHistory: https://python.langchain.com/docs/integrations/memory/redis_chat_message_history/
- LangChain 0.3.x migration: https://python.langchain.com/docs/versions/v0_3/
