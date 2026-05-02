---
name: agent-memory-architecture
description: Wire up a 3-tier agent memory system (working → episodic JSONL → semantic Qdrant) with threshold-triggered compaction and top-K retrieval injection.
tier: geek
group: ai-agents
status: active
owner: ruslan
last_verified: 2026-05-02
version: 1.0.0
---

## Goal

After this playbook you will have a Python agent that manages three memory tiers — working memory (current context window), episodic memory (JSONL sliding-window of recent sessions), and semantic memory (Qdrant vector store for persistent facts) — with automatic compaction at a token threshold and top-K retrieval injected into every new session prompt.

## Prerequisites

- Python 3.11+ with `uv` or `pip`.
- An Anthropic API key (`ANTHROPIC_API_KEY` in environment).
- Docker for running Qdrant locally (`docker pull qdrant/qdrant`).
- Packages: `anthropic>=0.40`, `qdrant-client>=1.9`, `sentence-transformers>=3.0`, `tiktoken>=0.7`.
- Familiarity with Claude tool-use / tool_result message format.
- Working knowledge of Python `dataclasses` and `pathlib`.

## Steps

1. **Start the Qdrant container.**

   ```bash
   docker run -d --name qdrant-memory -p 6333:6333 -p 6334:6334 \
     -v $(pwd)/qdrant_data:/qdrant/storage qdrant/qdrant
   ```

   Verify: `curl -s http://localhost:6333/collections` returns `{"result":{"collections":[]}}`.

2. **Install dependencies.**

   ```bash
   pip install "anthropic>=0.40" "qdrant-client>=1.9" \
               "sentence-transformers>=3.0" "tiktoken>=0.7"
   ```

3. **Define the three-tier memory schema.**

   ```python
   # memory/schema.py
   from __future__ import annotations
   from dataclasses import dataclass, field
   from pathlib import Path
   import json
   import time

   EPISODIC_PATH = Path("memory/episodic.jsonl")
   EPISODIC_WINDOW = 20          # keep last N turns in episodic store
   COMPACT_TOKEN_THRESHOLD = 6_000  # trigger compaction above this count
   EMBEDDING_MODEL = "all-MiniLM-L6-v2"
   QDRANT_COLLECTION = "agent-semantic"
   TOPK = 5                      # memories injected per prompt

   @dataclass
   class Turn:
       role: str                  # "user" | "assistant"
       content: str
       ts: float = field(default_factory=time.time)

       def to_msg(self) -> dict:
           return {"role": self.role, "content": self.content}

       def to_jsonl(self) -> str:
           return json.dumps({"role": self.role, "content": self.content, "ts": self.ts})
   ```

4. **Build the working-memory manager.**

   Working memory is the live `messages` list passed to every `client.messages.create` call. Count tokens with `tiktoken` and trigger compaction when the threshold is crossed.

   ```python
   # memory/working.py
   import tiktoken
   from memory.schema import Turn, COMPACT_TOKEN_THRESHOLD

   _enc = tiktoken.get_encoding("cl100k_base")

   def token_count(turns: list[Turn]) -> int:
       return sum(len(_enc.encode(t.content)) for t in turns)

   def needs_compaction(turns: list[Turn]) -> bool:
       return token_count(turns) > COMPACT_TOKEN_THRESHOLD
   ```

5. **Build the episodic-memory store (JSONL sliding window).**

   ```python
   # memory/episodic.py
   import json
   from pathlib import Path
   from memory.schema import Turn, EPISODIC_PATH, EPISODIC_WINDOW

   EPISODIC_PATH.parent.mkdir(parents=True, exist_ok=True)

   def append_turns(turns: list[Turn]) -> None:
       with EPISODIC_PATH.open("a") as fh:
           for t in turns:
               fh.write(t.to_jsonl() + "\n")
       _trim()

   def _trim() -> None:
       lines = EPISODIC_PATH.read_text().splitlines() if EPISODIC_PATH.exists() else []
       if len(lines) > EPISODIC_WINDOW:
           EPISODIC_PATH.write_text("\n".join(lines[-EPISODIC_WINDOW:]) + "\n")

   def load_recent() -> list[Turn]:
       if not EPISODIC_PATH.exists():
           return []
       turns = []
       for line in EPISODIC_PATH.read_text().splitlines():
           if not line.strip():
               continue
           d = json.loads(line)
           turns.append(Turn(role=d["role"], content=d["content"], ts=d.get("ts", 0.0)))
       return turns[-EPISODIC_WINDOW:]
   ```

6. **Build the semantic-memory store (Qdrant + embeddings).**

   ```python
   # memory/semantic.py
   from __future__ import annotations
   from sentence_transformers import SentenceTransformer
   from qdrant_client import QdrantClient
   from qdrant_client.models import Distance, VectorParams, PointStruct
   import uuid
   from memory.schema import QDRANT_COLLECTION, EMBEDDING_MODEL, TOPK

   _model = SentenceTransformer(EMBEDDING_MODEL)
   _client = QdrantClient(host="localhost", port=6333)

   def _ensure_collection() -> None:
       existing = {c.name for c in _client.get_collections().collections}
       if QDRANT_COLLECTION not in existing:
           _client.create_collection(
               collection_name=QDRANT_COLLECTION,
               vectors_config=VectorParams(size=384, distance=Distance.COSINE),
           )

   def upsert_fact(text: str, metadata: dict | None = None) -> str:
       _ensure_collection()
       vec = _model.encode(text).tolist()
       point_id = str(uuid.uuid4())
       _client.upsert(
           collection_name=QDRANT_COLLECTION,
           points=[PointStruct(id=point_id, vector=vec, payload={"text": text, **(metadata or {})})],
       )
       return point_id

   def retrieve(query: str, top_k: int = TOPK) -> list[str]:
       _ensure_collection()
       vec = _model.encode(query).tolist()
       hits = _client.search(
           collection_name=QDRANT_COLLECTION,
           query_vector=vec,
           limit=top_k,
           with_payload=True,
       )
       return [h.payload["text"] for h in hits if h.payload]
   ```

7. **Implement compaction (episodic flush + semantic upsert).**

   Compaction extracts structured references — decisions, identifiers, key facts — from the current working-memory turns, upserts them into Qdrant, then flushes to episodic JSONL and resets the live list.

   ```python
   # memory/compact.py
   import anthropic
   from memory.schema import Turn, COMPACT_TOKEN_THRESHOLD
   from memory import episodic, semantic

   _anthro = anthropic.Anthropic()

   _COMPACT_PROMPT = """
   You are a memory compactor. Given the conversation below, extract a JSON list of facts.
   Each fact: {"text": "<one sentence>", "type": "decision|entity|error|url|preference"}.
   Include only information the agent will need to resume work:
   decisions made, identifiers (IDs, file paths, URLs), user preferences, error messages.
   Drop reasoning chains and tool output verbatim text.
   Return only the JSON array — no commentary.

   Conversation:
   {conversation}
   """

   def compact(turns: list[Turn]) -> list[Turn]:
       conversation = "\n".join(f"{t.role.upper()}: {t.content}" for t in turns)
       resp = _anthro.messages.create(
           model="claude-haiku-4-5-20251001",
           max_tokens=1024,
           messages=[{"role": "user", "content": _COMPACT_PROMPT.format(conversation=conversation)}],
       )
       import json, re
       raw = resp.content[0].text
       # extract JSON array even if model adds a preamble
       m = re.search(r"\[.*\]", raw, re.DOTALL)
       facts = json.loads(m.group()) if m else []
       for fact in facts:
           semantic.upsert_fact(fact["text"], {"type": fact.get("type", "general")})
       episodic.append_turns(turns)
       # reset to a single synthetic context turn summarising what was stored
       summary = f"[Compacted {len(turns)} turns. {len(facts)} facts stored to semantic memory.]"
       return [Turn(role="assistant", content=summary)]
   ```

8. **Wire everything into the main agent loop.**

   ```python
   # agent.py
   import anthropic
   from memory.schema import Turn
   from memory import working, semantic
   from memory.compact import compact

   _anthro = anthropic.Anthropic()
   MODEL = "claude-sonnet-4-6"

   def _build_system(query: str) -> str:
       retrieved = semantic.retrieve(query)
       if not retrieved:
           return "You are a helpful assistant."
       facts_block = "\n".join(f"- {f}" for f in retrieved)
       return (
           "You are a helpful assistant.\n\n"
           "## Relevant memories (retrieved)\n"
           f"{facts_block}"
       )

   def chat(turns: list[Turn], user_input: str) -> tuple[str, list[Turn]]:
       turns.append(Turn(role="user", content=user_input))
       if working.needs_compaction(turns):
           turns = compact(turns)

       response = _anthro.messages.create(
           model=MODEL,
           max_tokens=2048,
           system=_build_system(user_input),
           messages=[t.to_msg() for t in turns],
       )
       reply = response.content[0].text
       turns.append(Turn(role="assistant", content=reply))
       return reply, turns

   if __name__ == "__main__":
       history: list[Turn] = []
       while True:
           user_in = input("You: ").strip()
           if user_in.lower() in {"exit", "quit"}:
               break
           reply, history = chat(history, user_in)
           print(f"Agent: {reply}\n")
   ```

9. **Teach the agent to store explicit facts via a tool.**

   Add a `store_memory` tool so the agent can proactively upsert facts during a session without waiting for compaction.

   ```python
   # tools.py
   STORE_MEMORY_TOOL = {
       "name": "store_memory",
       "description": "Save an important fact to long-term semantic memory.",
       "input_schema": {
           "type": "object",
           "properties": {
               "text":     {"type": "string", "description": "Fact to store (one sentence)."},
               "mem_type": {"type": "string", "enum": ["decision", "entity", "error", "url", "preference"]},
           },
           "required": ["text", "mem_type"],
       },
   }
   ```

   In `chat()`, pass `tools=[STORE_MEMORY_TOOL]` and handle `tool_use` stop reason by calling `semantic.upsert_fact(inp["text"], {"type": inp["mem_type"]})` then continuing the loop with a `tool_result` message.

## Verify

Run the agent and confirm all three tiers are active:

```bash
python agent.py
# Enter a few turns. Then:
python - <<'EOF'
from memory import episodic, semantic
print("Episodic turns:", len(episodic.load_recent()))
print("Semantic hits:", semantic.retrieve("user preferences"))
EOF
```

Expected: episodic returns ≥1 `Turn` object; semantic returns a list of strings (may be empty on first run). After triggering compaction (paste a long conversation), `qdrant_data/` grows and `episodic.jsonl` stays trimmed to ≤20 lines.

Also confirm Qdrant has received points:

```bash
curl -s http://localhost:6333/collections/agent-semantic | python3 -m json.tool | grep vectors_count
```

Returns `"vectors_count": <N>` where N > 0 after at least one compaction cycle.

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `qdrant_client.http.exceptions.ResponseHandlingException: Connection refused` | Qdrant container not running | `docker start qdrant-memory`; confirm `curl localhost:6333` responds |
| Compaction fires every turn | `COMPACT_TOKEN_THRESHOLD` too low for model output size | Raise `COMPACT_TOKEN_THRESHOLD` to 10 000–15 000; check `tiktoken` encoding matches the model (use `cl100k_base` for all Claude models) |
| `json.JSONDecodeError` in `compact()` | Haiku returned prose instead of JSON array | Add `assert resp.stop_reason == "end_turn"` guard; wrap extraction in `try/except` and fall back to storing the raw summary as a single fact |
| Semantic retrieval returns irrelevant facts | `all-MiniLM-L6-v2` domain mismatch | Switch to `multi-qa-mpnet-base-dot-v1` (stronger retrieval) or use Qdrant's sparse-vector hybrid mode with a domain-tuned model |
| `EPISODIC_PATH` grows unbounded between restarts | `_trim()` not called on load | Call `_trim()` once at import time by adding `_trim()` at the bottom of `episodic.py` |
| `store_memory` tool call silently dropped | `tool_result` block missing from message loop | After any `tool_use` in response, always append a `tool_result` message before the next `messages.create` call |

## Next

- Add the `store_memory` tool loop from Step 9 and test with a multi-turn session that explicitly saves decisions.
- Extend semantic retrieval to use Qdrant's hybrid sparse+dense mode for better recall on short keywords; see `knowledge/geek/ai/rag-engineer/db-qdrant`.
- Add cross-session identity by tagging every fact with `session_id`; filter retrieval to `current_user` via Qdrant payload filters.

## References

- [knowledge/geek/ai/ai-agents/langchain-memory](../../../knowledge/geek/ai/ai-agents/langchain-memory) — buffer, summary, vector, and entity memory patterns that directly map to the 3 tiers implemented here; Step 4 (working) and Step 5 (episodic) derive from buffer and summary memory shapes respectively
- [knowledge/geek/ai/ai-agents/compaction-preserve-refs](../../../knowledge/geek/ai/ai-agents/compaction-preserve-refs) — schema-driven compaction preserving file paths, decisions, and IDs; Step 7's `_COMPACT_PROMPT` and keep/drop logic are a direct application of this pattern
- [knowledge/geek/ai/ai-agents/filesystem-as-working-memory](../../../knowledge/geek/ai/ai-agents/filesystem-as-working-memory) — offload-before-summarize discipline that informs the compaction trigger order: flush to episodic JSONL (lossless) before calling the LLM to extract semantic facts (lossy)
- [knowledge/geek/ai/rag-engineer/db-qdrant](../../../knowledge/geek/ai/rag-engineer/db-qdrant) — Qdrant HNSW tuning, payload filtering, and quantization options used in Step 6's collection setup and the hybrid-mode upgrade path in Next
