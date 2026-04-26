# OpenAI Assistants API

## Summary

The Assistants API is a stateful layer over Chat Completions that manages conversation threads, file uploads, a built-in vector store (File Search), and a sandboxed Python runtime (Code Interpreter). It is designed for multi-turn user-facing applications where the caller should not manage message history, document indexing, or code execution infrastructure.

## Why

Building persistent conversation state, file-based RAG, and code execution from scratch requires significant infrastructure. Assistants API handles chunking, embedding, retrieval, and code sandboxing as managed services. The cost: every feature adds HTTP round-trips and per-token overhead, making it slower and more expensive than Chat Completions for automated pipelines. Use it when state management convenience outweighs throughput requirements.

## When To Use

- Multi-turn user-facing applications where conversation history must persist across sessions.
- RAG over uploaded documents without building a custom vector pipeline (File Search).
- Data analysis where the LLM needs to execute Python on uploaded CSV/Excel files (Code Interpreter).
- Prototyping agent applications when stateful conversation overhead is acceptable.
- Users upload files mid-conversation and the assistant must act on them immediately.

## When NOT To Use

- High-throughput automated pipelines — Assistants adds HTTP round-trips per turn; Chat Completions is faster.
- When deterministic, auditable tool execution is required — internal tool calling is opaque.
- Cost-sensitive workloads — file search + thread storage add per-token overhead.
- Data that must not be stored on OpenAI servers (GDPR/HIPAA) — threads and files persist.
- Sub-100ms first-token latency requirements — `create_and_poll` polling overhead is too high.

## Content

| File | What's inside |
|------|---------------|
| `content/01-threads-runs.xml` | Thread lifecycle, run creation, status handling, streaming, rate limit retry. |
| `content/02-file-search.xml` | Vector store creation, file upload, async indexing, citation handling. |
| `content/03-code-interpreter.xml` | File attachment, code execution, image output download, sandbox limits. |

## Templates

| File | Purpose |
|------|---------|
| `templates/query-assistant.py` | One-shot assistant interaction with error handling. |
| `templates/managed-resources.py` | Context managers for thread and vector store lifecycle (create → use → delete). |
