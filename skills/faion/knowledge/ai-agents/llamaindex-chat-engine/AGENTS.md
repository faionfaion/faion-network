# Llamaindex Chat Engine

## Summary

**One-sentence:** Selects a LlamaIndex chat-engine mode (condense_plus_context, context, react) and bounded memory + streaming and emits a chat-engine-spec.

**One-paragraph:** LlamaIndex chat engines wrap a VectorStoreIndex with conversation memory. Choosing the wrong mode (react when condense+context would do) wastes tokens; unbounded memory blows the context window. This methodology turns a chat profile (follow-up complexity, doc corpus, latency) into a deterministic chat-engine-spec.

**Ефективно для:** solopreneur building a doc-Q&A chatbot on LlamaIndex who needs follow-up questions to work.

## Applies If (ALL must hold)

- Using LlamaIndex as the framework.
- Bot needs follow-up question handling (multi-turn).
- Index already exists or will be built next.
- Latency budget allows ≥1 LLM call per turn.
- You can pin token_limit on the memory buffer.

## Skip If (ANY kills it)

- Single-turn Q&A — use plain query_engine.
- Tool-using agent — use ReActAgent + [[llamaindex-agents-eval]].
- LangChain-based — use [[langchain-memory]].
- Chat needs SQL — use [[llamaindex-sql-query]] then wrap.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| `chat-profile.yaml` | follow_up_complexity, latency_target_ms, streaming_required, token_limit | author |
| `VectorStoreIndex` | existing or to-build | ingestion |
| `LLM client` | instantiated | creds |

## Assumes Loaded

| Methodology | Why |
|---|---|
| [[llamaindex-basics]] | Index foundations. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | Rules for chat modes, ChatMemoryBuffer, streaming. | ~1000 |
| `content/02-output-contract.xml` | essential | chat-engine-spec schema + examples. | ~800 |
| `content/03-failure-modes.xml` | essential | Unbounded buffer, wrong mode for follow-ups, streaming UX broken. | ~700 |
| `content/04-procedure.xml` | recommended | 5-step selection procedure. | ~800 |
| `content/06-decision-tree.xml` | essential | Decision tree | ~700 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| Profile parsing | haiku | Mechanical. |
| Decision drafting | sonnet | Tradeoffs require sound reasoning. |
| Code/config emission | sonnet | Mechanical but must compile. |
| Failure-mode cross-check | opus | Catches subtle gaps. |

## Templates

| File | Purpose |
|---|---|
| `templates/chat-profile.yaml` | Input. |
| `templates/chat-engine-spec.md.j2` | Output. |
| `templates/chat-engine-spec.md` | Output. Generated from `templates/chat-engine-spec.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/chat.py` | Working chat-engine wiring. |
| `templates/_smoke-test.yaml` | Minimum. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-llamaindex-chat-engine.py` | Validates output against the JSON schema. | Pre-commit. |

## Related

- [[llamaindex-basics]]
- [[langchain-memory]]

## Decision tree

Lives at `content/06-decision-tree.xml`. Branches on tool_use (true → react; false → condense_plus_context default), then on follow_up_complexity (high → condense_plus_context; trivial → context). Each leaf cites a rule id in 01-core-rules.xml so the agent always cites which rule drove the choice — and can be replayed for audit.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/chat-profile.yaml`

```yaml
follow_up_complexity: TODO          # fill with concrete value per the driver definition
tool_use: TODO          # fill with concrete value per the driver definition
latency_target_ms: TODO          # fill with concrete value per the driver definition
```

### `templates/chat.py`

```python
"""Reference artefact for llamaindex-chat-engine. Self-test only verifies the scaffold compiles."""
from __future__ import annotations


def build(decision: dict):
    """Build the runtime object from a validated decision-record."""
    if not isinstance(decision, dict):
        raise TypeError("decision must be dict from validated decision-record")
    return decision  # placeholder: real implementations wire here


def _self_test() -> int:
    out = build({"slug": "llamaindex-chat-engine", "version": "2.0.0"})
    return 0 if out["slug"] == "llamaindex-chat-engine" else 1


if __name__ == "__main__":
    import sys
    if "--self-test" in sys.argv:
        raise SystemExit(_self_test())
    if "--help" in sys.argv:
        print(__doc__)
```

### `templates/_smoke-test.yaml`

```yaml
follow_up_complexity: low
tool_use: low
latency_target_ms: low
```
