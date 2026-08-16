# Filesystem as Working Memory — Offload Before Summarize

## Summary

**One-sentence:** Equips long-running agents with write_file/read_file/ls/grep tools backed by a real or virtual FS, offloads every tool output above ~2K tokens to disk, and reserves lossy LLM-based summarisation for context >85% utilisation only after no offload remains.

**One-paragraph:** Give every long-running agent a `write_file` / `read_file` / `ls` / `grep` tool surface backed by real disk, S3, or a state-dict virtual FS. Whenever a tool produces a large blob, write it to the FS and pass back only a filename plus a short snippet. Reserve LLM-based context summarisation for the moment context hits ~85% AND nothing remains to offload — file offload preserves information losslessly, summarisation does not.

**Ефективно для:** дослідницьких агентів, codegen-агентів, будь-якого циклу понад 20 ходів, що мусить зберігати інформацію між процесами.

## Applies If (ALL must hold)

- Research agents reading more than 5 documents per task.
- Codegen across many files (Claude Code, Aider, OpenHands, Cursor).
- Tasks expected to run more than ~20 turns.
- Pipelines where step N's output feeds step N+1 — paths flow, not blobs.
- Agents must survive process restart (FS persists, conversation does not).

## Skip If (ANY kills it)

- Short chat sessions under ~10 turns.
- Single-document QA — the document already fits in context.
- Hard real-time loops where every disk write adds unacceptable latency.
- Untrusted code execution where a writable FS is a security problem.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| FS backend | Real disk path, S3 bucket, or in-memory dict | Agent config |
| Checkpointer | Postgres/Redis/SQLite store for conversation state | Orchestrator config |
| Path taxonomy | search/ docs/ plan/ scratch/ | SKILL or system prompt |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|---|---|
| `file-reference-passing` | The offloaded files are passed by reference, not content. |
| `compaction-preserve-refs` | When summarisation finally triggers, refs in the compaction point at offloaded files. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Five testable rules: offload-2k, four-tool surface, taxonomy, atomic-checkpoint, compact-last | ~1000 |
| `content/02-output-contract.xml` | essential | Tool definitions JSON; offloaded-envelope schema | ~900 |
| `content/03-failure-modes.xml` | essential | Premature compaction, round-trip blobs, dangling paths | ~800 |
| `content/06-decision-tree.xml` | essential | Per-tool-call: inline or offload? Per-turn: offload or compact? | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Decide inline vs offload per tool result | code | Pure size check; no LLM needed |
| Choose path taxonomy for new agent | sonnet | One-shot design |
| Audit existing agent for premature compaction | sonnet | Pattern detection |

## Templates

| File | Purpose |
|------|---------|
| `templates/fs-tools.json` | OpenAI/Anthropic tool definitions for the four FS primitives |
| `templates/_smoke-test.json` | Minimum valid offloaded-envelope for self-test |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-filesystem-as-working-memory.py` | Validates an offloaded-envelope against the schema | After every tool wrapper that may offload |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[file-reference-passing]]
- [[compaction-preserve-refs]]
- [[handoff-id-payload]]

## Decision tree

See `content/06-decision-tree.xml`. The root question per tool call is whether the result exceeds the ~2K token threshold. The root question per turn is whether utilisation passed 85%. The tree routes to inline-return, offload-with-snippet, or LLM-based compaction depending on what is still available.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/fs-tools.json`

```json
{
  "items": [
    {
      "_header": {
        "_purpose": "OpenAI/Anthropic tool definitions for the four FS primitives",
        "_consumes": "agent tool-binding step",
        "_produces": "registered tool surface (write_file/read_file/ls/grep)",
        "_depends_on": "content/01-core-rules.xml (r2-four-tools)",
        "_token_budget_impact": "~400 tokens when injected into the model"
      }
    },
    {
      "name": "write_file",
      "description": "Write content to the agent's working-memory filesystem. Creates parent directories. Returns the path on success. Use this for any tool result over ~2000 tokens that you want to keep but not pin in context.",
      "input_schema": {
        "type": "object",
        "required": [
          "path",
          "content"
        ],
        "properties": {
          "path": {
            "type": "string",
            "description": "Relative path under search/, docs/, plan/, or scratch/."
          },
          "content": {
            "type": "string"
          }
        }
      }
    },
    {
      "name": "read_file",
      "description": "Read a file previously written. Use offset+limit to stream large files. Default limit is 2000 tokens; ask for more only when you need it.",
      "input_schema": {
        "type": "object",
        "required": [
          "path"
        ],
        "properties": {
          "path": {
            "type": "string"
          },
          "offset": {
            "type": "integer",
            "default": 0
          },
          "limit": {
            "type": "integer",
            "default": 2000
          }
        }
      }
    },
    {
      "name": "ls",
      "description": "List files under a working-memory directory. Returns names + sizes only. Use to navigate the FS without reading content.",
      "input_schema": {
        "type": "object",
        "properties": {
          "path": {
            "type": "string",
            "default": "."
          }
        }
      }
    },
    {
      "name": "grep",
      "description": "Search for a regex pattern across working-memory files. Returns matching path:line:snippet entries. Use this BEFORE read_file when scanning for specific content.",
      "input_schema": {
        "type": "object",
        "required": [
          "pattern"
        ],
        "properties": {
          "pattern": {
            "type": "string"
          },
          "path": {
            "type": "string",
            "default": "."
          }
        }
      }
    }
  ]
}
```

### `templates/_smoke-test.json`

```json
{
  "_purpose": "smallest valid offloaded-envelope for the validator",
  "_consumes": "nothing",
  "_produces": "example envelope matching content/02-output-contract.xml",
  "_depends_on": "content/01-core-rules.xml",
  "_token_budget_impact": "~60 tokens",
  "kind": "offloaded",
  "path": "search/refund-policy.json",
  "head": "Refund policy v3.2 \u2014 30-day window, exceptions for digital goods..."
}
```
