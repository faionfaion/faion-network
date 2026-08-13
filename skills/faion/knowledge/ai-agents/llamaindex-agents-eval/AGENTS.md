# Llamaindex Agents Eval

## Summary

**One-sentence:** Picks a LlamaIndex agent style (ReAct vs OpenAI) and an eval suite (faithfulness/relevancy/correctness) and emits an agent-eval-spec.

**One-paragraph:** LlamaIndex agents need the right style for the task and a real eval suite — running an agent without measuring faithfulness, relevancy, and correctness is hope, not engineering. This methodology turns an agent profile (tools, reasoning style, eval budget) into a deterministic spec: agent class, tool list, eval metrics, cost cap, streaming on/off.

**Ефективно для:** solopreneur shipping a LlamaIndex-based agent who needs numbers on quality before launch.

## Applies If (ALL must hold)

- Using LlamaIndex (not LangChain) for an agent.
- Agent has ≥1 tool call per turn (otherwise it's a query engine).
- You have a labeled set or can generate one with LlamaCloud/another agent.
- Eval budget is bounded; you can't run 10k samples per build.
- Production target measures answer correctness, not just availability.

## Skip If (ANY kills it)

- Agent is throwaway / exploratory.
- Framework is LangChain — use langchain-observability + langchain-production-patterns instead.
- No tools — use a plain query engine + relevancy eval.
- Eval budget zero — write at least 5 manual test cases or stop calling it production.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| `agent-profile.yaml` | YAML: tools, reasoning_style, eval_budget_usd, latency_target_ms, streaming_required | author writes |
| `Labeled set` | JSONL with question + ground-truth answer | manual or LlamaCloud-generated |
| `Tools list` | callable functions or LlamaIndex Tools | code |

## Assumes Loaded

| Methodology | Why |
|---|---|
| [[llamaindex-basics]] | Index + query engine foundations. |
| [[llamaindex-production-gotchas]] | Common LlamaIndex failure modes. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | Rules for agent style, eval metrics, streaming, caching. | ~1000 |
| `content/02-output-contract.xml` | essential | agent-eval-spec schema + examples. | ~800 |
| `content/03-failure-modes.xml` | essential | No eval at all, single-metric eval, eval set leaks into prompt. | ~700 |
| `content/04-procedure.xml` | recommended | 6-step procedure. | ~800 |
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
| `templates/agent-profile.yaml` | Input. |
| `templates/agent-eval-spec.md` | Output. |
| `templates/agent.py` | Working LlamaIndex agent wiring. |
| `templates/_smoke-test.yaml` | Minimum profile. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-llamaindex-agents-eval.py` | Validates output against the JSON schema. | Pre-commit. |

## Related

- [[llamaindex-basics]]
- [[llm-judge-rubric-evidence-first]]
- [[llamaindex-production-gotchas]]

## Decision tree

Lives at `content/06-decision-tree.xml`. Branches on reasoning_style (openai → OpenAIAgent; react → ReActAgent), then on eval_budget (high → full faithfulness+relevancy+correctness; low → relevancy only), then on streaming. Each leaf cites a rule id in 01-core-rules.xml so the agent always cites which rule drove the choice — and can be replayed for audit.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/agent-profile.yaml`

```yaml
reasoning_style: TODO          # fill with concrete value per the driver definition
tools_count: TODO          # fill with concrete value per the driver definition
eval_budget_usd: TODO          # fill with concrete value per the driver definition
latency_target_ms: TODO          # fill with concrete value per the driver definition
```

### `templates/agent.py`

```python
"""Reference artefact for llamaindex-agents-eval. Self-test only verifies the scaffold compiles."""
from __future__ import annotations


def build(decision: dict):
    """Build the runtime object from a validated decision-record."""
    if not isinstance(decision, dict):
        raise TypeError("decision must be dict from validated decision-record")
    return decision  # placeholder: real implementations wire here


def _self_test() -> int:
    out = build({"slug": "llamaindex-agents-eval", "version": "2.0.0"})
    return 0 if out["slug"] == "llamaindex-agents-eval" else 1


if __name__ == "__main__":
    import sys
    if "--self-test" in sys.argv:
        raise SystemExit(_self_test())
    if "--help" in sys.argv:
        print(__doc__)
```

### `templates/_smoke-test.yaml`

```yaml
reasoning_style: low
tools_count: low
eval_budget_usd: low
latency_target_ms: low
```
