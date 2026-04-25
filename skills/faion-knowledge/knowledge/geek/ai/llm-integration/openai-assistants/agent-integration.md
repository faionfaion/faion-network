# Agent Integration — OpenAI Assistants API

## When to use
- Multi-turn user-facing applications where conversation history must persist across sessions without custom storage
- RAG over uploaded documents without building a vector pipeline — File Search manages chunking, embedding, and retrieval automatically
- Data analysis workflows where the LLM needs to execute Python code on uploaded CSV/Excel files (Code Interpreter)
- Prototyping agent applications quickly when conversation state management overhead is not acceptable
- Use cases where users upload files mid-conversation and the assistant must immediately act on them

## When NOT to use
- High-throughput pipelines — Assistants API adds HTTP round-trips per turn (create message → create run → poll → retrieve); Chat Completions is faster for automated pipelines
- When you need deterministic, auditable tool execution — Assistants' internal tool calling is opaque compared to manual function calling
- Cost-sensitive workloads — Assistants API adds per-token overhead for file search + thread storage
- When your data must not be stored on OpenAI servers — threads and files persist; GDPR/HIPAA workloads need explicit cleanup or custom storage
- Streaming pipelines that need sub-100ms first-token latency — `create_and_poll` adds polling overhead

## Where it fails / limitations
- Run polling is required — no native webhook; `create_and_poll` blocks until completion, making async pipelines complex
- File Search retrieval quality is not auditable — you cannot inspect the embedding model, chunking strategy, or ranking algorithm
- Code Interpreter runs in an OpenAI-controlled sandbox — cannot install custom packages or access external network
- Vector store file processing can fail silently — always check `file.status` before assuming documents are indexed
- Thread messages accumulate indefinitely — long threads hit context limits and cost more per run
- Assistant configuration (instructions, tools) cannot be changed per-run — create a new assistant for significantly different configurations
- Rate limits apply per assistant, not just per account — parallel runs on the same assistant can conflict

## Agentic workflow
Assistants are best used as the conversational layer in a hybrid architecture: the Assistants API handles multi-turn state and file access while custom tools handle business logic. An agent creates a thread once per user session, adds messages, triggers runs, and polls for completion. For automated pipelines without user interaction, prefer Chat Completions with your own message array. Use File Search for document Q&A; use Code Interpreter for data analysis; avoid both for pure text generation.

### Recommended subagents
- no dedicated assistant management subagent exists in the current agent library; use `faion-sdd-executor-agent` to orchestrate assistant creation + cleanup lifecycle

### Prompt pattern
```python
from openai import OpenAI

client = OpenAI()

# One-shot assistant interaction with error handling
def query_assistant(assistant_id: str, thread_id: str, question: str) -> str:
    client.beta.threads.messages.create(
        thread_id=thread_id, role="user", content=question
    )
    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread_id, assistant_id=assistant_id
    )
    if run.status != "completed":
        raise RuntimeError(f"Run failed: {run.status} — {run.last_error}")
    msgs = client.beta.threads.messages.list(thread_id=thread_id, order="desc", limit=1)
    return msgs.data[0].content[0].text.value
```

```python
# File upload + RAG query
def upload_and_query(assistant_id: str, file_path: str, question: str) -> str:
    # Upload file
    with open(file_path, "rb") as f:
        file = client.files.create(file=f, purpose="assistants")

    # Create vector store and attach file
    vs = client.beta.vector_stores.create(name="session-docs")
    client.beta.vector_stores.files.create(vector_store_id=vs.id, file_id=file.id)
    client.beta.assistants.update(
        assistant_id=assistant_id,
        tool_resources={"file_search": {"vector_store_ids": [vs.id]}}
    )
    thread = client.beta.threads.create()
    result = query_assistant(assistant_id, thread.id, question)

    # Cleanup
    client.beta.threads.delete(thread.id)
    client.beta.vector_stores.delete(vs.id)
    client.files.delete(file.id)
    return result
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `openai` SDK | Assistants, threads, files, runs | `pip install openai` → https://github.com/openai/openai-python |
| `openai` CLI | List/delete assistants, files via CLI | `openai api assistants.list` |
| `tenacity` | Retry polling loops on rate limit errors | `pip install tenacity` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| OpenAI Platform | SaaS | Yes | Primary endpoint; Assistants v2 with vector stores |
| Helicone | SaaS | Yes | Proxy; logs thread/run costs alongside completions |
| Portkey | SaaS | Yes | Fallback routing; useful if Assistants endpoint degrades |
| LlamaIndex | OSS | Yes | Can use OpenAI Assistants as a retriever backend |

## Templates & scripts
See `templates.md` for streaming EventHandler pattern. Resource lifecycle manager (create → use → cleanup):

```python
from contextlib import contextmanager

@contextmanager
def managed_thread(assistant_id: str):
    """Create thread, yield for use, then delete."""
    thread = client.beta.threads.create()
    try:
        yield thread.id
    finally:
        client.beta.threads.delete(thread.id)

@contextmanager
def managed_vector_store(name: str, file_paths: list[str]):
    """Upload files, create vector store, yield id, then clean up."""
    files = [client.files.create(file=open(p, "rb"), purpose="assistants") for p in file_paths]
    vs = client.beta.vector_stores.create(name=name)
    for f in files:
        client.beta.vector_stores.files.create(vector_store_id=vs.id, file_id=f.id)
    try:
        yield vs.id
    finally:
        client.beta.vector_stores.delete(vs.id)
        for f in files:
            client.files.delete(f.id)
```

## Best practices
- Delete threads, vector stores, and files after use — orphaned resources accumulate and are billed
- Use `create_and_poll` only for synchronous flows; for async, use `runs.create` + poll manually with `asyncio.sleep`
- Check `run.status` explicitly: `completed`, `failed`, `cancelled`, `expired` all need different handling
- Limit thread length — archive old messages by creating a new thread with a summary message after N turns
- Use `metadata` on threads and assistants to tag with user IDs and session IDs for cost attribution
- For File Search, verify file processing status before querying — upload is async and may take seconds to minutes for large PDFs
- Set `max_prompt_tokens` and `max_completion_tokens` on runs to cap per-run costs in multi-user deployments

## AI-agent gotchas
- `run.status == "requires_action"` means the assistant called a custom function tool and is waiting — if your agent does not handle this, the run expires (10-minute timeout)
- Vector store file processing is asynchronous — querying immediately after `files.create` may return no results; poll `file.status == "completed"` first
- File Search citations in message annotations reference `file_id`, not file name — you must maintain a file_id → filename mapping yourself
- Thread message order: `messages.list` returns newest first by default — use `order="asc"` to get conversation order
- Code Interpreter-generated images are ephemeral `image_file` content blocks — download them immediately; they expire
- `create_and_poll` does not surface run step details (which tools were called) — use `run_steps.list` separately if you need auditability
- Assistants API v2 (vector stores) is different from v1 (file_ids on assistant) — mixing v1 and v2 patterns causes 400 errors

## References
- https://platform.openai.com/docs/assistants/overview
- https://platform.openai.com/docs/assistants/tools/file-search
- https://platform.openai.com/docs/assistants/tools/code-interpreter
- https://platform.openai.com/docs/api-reference/assistants
- https://github.com/openai/openai-python/tree/main/examples/assistants
