# LangChain and LangGraph: Building Production AI Agents

## Summary

**One-sentence:** Produces a production agent built on LangChain (LCEL pipe syntax) for chains and LangGraph (state-machine framework) for durable multi-step orchestration with checkpoints and human-in-the-loop interrupts.

**One-paragraph:** Produces a production agent built on LangChain + LangGraph. LangChain handles standard tool-calling agents (`create_react_agent`) and composable pipelines via LCEL (`prompt | model | parser`). LangGraph adds durable state, checkpointing, human-in-the-loop interrupts, and Supervisor multi-agent patterns. Choose LangGraph when the workflow has loops, retries, human approval steps, or independent agent nodes; choose LangChain LCEL when it is a linear pipeline.

**Ефективно для:** Бекенд-розробник для agent з human-approval — fixed graph з durable state + interrupt + supervisor.

## Applies If (ALL must hold)

- Multi-step LLM workflow with tools, retries, branches, or human approval steps.
- Python stack — LangChain is Python (and JS, but Python is canonical).
- Need durable state across long-running sessions (checkpointing).
- Have or can stand up a checkpoint backend (PostgreSQL, Redis, SQLite for dev).
- Familiar with the LangChain/LangGraph paradigm or willing to learn it.

## Skip If (ANY kills it)

- Single-turn LLM call with no tools / state — use the provider SDK directly.
- Workflow has no branching, retries, or human steps — LCEL chain is sufficient.
- Team rejects the framework lock-in — consider a thinner agent loop.
- Performance budget cannot absorb LangGraph state overhead.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Workflow diagram (nodes + edges) | markdown / mermaid | ML lead |
| Tool specifications | py functions / json | ML team |
| Checkpoint backend | url + creds | infra |
| Provider choice | string | decision record |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/ai/ml-engineer/llm-decision-framework` | Provider + agent-pattern choice. |
| `geek/ai/ml-engineer/llm-observability-stack` | LangSmith / OTel integration. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules each with rationale + source. | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples + self-check. | ~800 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix. | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure: model-workflow → declare-nodes → wire-edges → add-checkpoint → wire-interrupt. | ~800 |
| `content/06-decision-tree.xml` | essential | Branch: LCEL vs LangGraph + supervisor vs router. | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-graph` | haiku | Fill langgraph-supervisor.py / router-node.py from workflow diagram. |
| `design-state-schema` | sonnet | Declare State TypedDict with reducers. |
| `debug-non-terminating` | opus | Trace loops that fail to terminate; cross-node debug. |

## Templates

| File | Purpose |
|------|---------|
| `templates/langgraph-router-node.py` | Router-node template for branching. |
| `templates/lcel-chain.py` | LCEL pipe-syntax chain skeleton. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-langchain.py` | Validate the graph config (nodes, edges, checkpointer, interrupts). | Pre-merge of every agent PR. |

## Related

- [[llamaindex]] — alternative agent framework.
- [[llm-decision-framework]] — provider/framework choice.
- [[llm-observability-stack]] — LangSmith tracing.

## Decision tree

Decision tree at `content/06-decision-tree.xml` decides LCEL vs LangGraph and within LangGraph: supervisor vs router vs single-agent.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/langgraph-router-node.py`

```python
"""

# LangGraph routing node using structured output
from langchain_core.prompts import ChatPromptTemplate
from langchain_anthropic import ChatAnthropic
from pydantic import BaseModel

class RouteDecision(BaseModel):
    next_node: str  # "executor" | "critic" | "done"
    reasoning: str

def router_node(state: dict) -> dict:
    model = ChatAnthropic(model="claude-sonnet-4-20250514")
    chain = (
        ChatPromptTemplate.from_template(
            "Given state: {state}\nDecide next step. Options: executor, critic, done."
        )
        | model.with_structured_output(RouteDecision)
    )
    decision = chain.invoke({"state": str(state)})
    return {"next": decision.next_node}
```

### `templates/lcel-chain.py`

```python
"""

# Stub — see methodology AGENTS.md ## Templates table.
```
