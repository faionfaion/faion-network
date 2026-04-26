# Filesystem as Working Memory — Offload Before Summarize

## Summary

Give every long-running agent a `write_file` / `read_file` / `ls` tool surface backed by real disk, S3, or a state-dict virtual FS. Whenever a tool produces a large blob (search dump, full document, raw API response), write it to the FS and pass back only a filename plus a short snippet. Reserve LLM-based context summarization for the moment context hits ~85% AND there is nothing left to offload — file offload preserves information losslessly, summarization does not.

## Why

LangChain's "Deep Agents" pattern and the "Anatomy of an Agent Harness" report converge on a single observation: agents that summarize prematurely lose facts they will need three turns later, while agents that offload to a filesystem keep every fact recoverable on demand. Treating the FS as working memory turns every tool result into a referenceable artifact: cheap to keep, cheap to skip, cheap to re-read at the precision the next step actually needs. The result is a hard upper bound on context size that does not require lossy compression.

## When To Use

- Research agents reading more than 5 documents per task.
- Codegen across many files (Claude Code, Aider, OpenHands, Cursor agents).
- Any task expected to run more than ~20 turns.
- Pipelines where step N's output is consumed by step N+1 — paths flow, not blobs.
- Agents that must survive process restart (FS persists, conversation does not).

## When NOT To Use

- Short chat sessions under ~10 turns — the FS abstraction adds ceremony with no payoff.
- Single-document QA — the document already fits in context once.
- Hard real-time loops where every disk write adds unacceptable latency.
- Untrusted code execution where a writable FS is itself a security problem.

## Content

| File | What's inside |
|------|---------------|
| `content/01-rule.xml` | The offload-before-summarize rule and the 85% threshold. |
| `content/02-tool-surface.xml` | Minimum FS tool surface (write_file, read_file, ls, grep) and naming conventions. |
| `content/03-anti-patterns.xml` | Common failures: summarize-too-early, blob round-trips, lost-state on restart. |

## Templates

| File | Purpose |
|------|---------|
| `templates/fs-tools.json` | OpenAI/Anthropic tool definitions for the four FS primitives. |
