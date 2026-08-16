# LangChain Chains: Patterns and Composition

## Summary

**One-sentence:** Composes LCEL chains using the four canonical patterns — Sequential, Router (RunnableBranch), MapReduce (asyncio.gather over ainvoke), and Fallback (with_fallbacks) — with explicit exception scoping, module-level definition, and pinned versions for production reliability.

**One-paragraph:** LCEL chain patterns, prompt templates, output parsers, error handling, and streaming for composing LLM pipelines with LangChain. Four patterns: Sequential (`prompt | model | parser`), Router (`RunnableBranch` with sequential conditions), MapReduce (real async fan-out via `asyncio.gather`), Fallback (`with_fallbacks` scoped to specific exception classes). Chains live at module level; `with_structured_output()` is preferred over `JsonOutputParser`; exception classes on fallbacks must be explicit to avoid masking config bugs.

**Ефективно для:** дискретних LLM-кроків у лінійному пайплайні, маршрутизації введення до спеціалізованих обробників, batch-обробки незалежних задач, стійких пайплайнів з gracefull degradation.

## Applies If (ALL must hold)

- Composing discrete LLM steps in a linear or routed pipeline.
- No need for stateful loops or branching (else use LangGraph).
- Output parsing is straightforward (else use `with_structured_output`).

## Skip If (ANY kills it)

- Need state, retries with modified state, or context between steps — use LangGraph.
- Single prompt + model call — use the model directly.
- Output parsing requires multiple fallback formats — function-calling structured output is more reliable.
- Visual workflow debugging is required — LangGraph is easier to inspect.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Prompt templates | `ChatPromptTemplate` | Application code |
| Model instance | `ChatAnthropic` or equivalent | Application code |
| Parser | `StrOutputParser` or `with_structured_output(Model)` | Application code |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|---|---|
| `langchain-basics` | Sets the foundation rules; this methodology extends them with pattern detail. |
| `gateway-fallback-chain` | `with_fallbacks` is the LangChain-native version of the gateway pattern. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Six rules: structured_output, module-level chains, scoped fallback exceptions, asyncio for parallel, retry-aware, no inline JsonOutputParser | ~1100 |
| `content/02-output-contract.xml` | essential | Sequential, Router, MapReduce, Fallback chain shapes | ~1100 |
| `content/03-failure-modes.xml` | essential | RunnableParallel sync misuse, with_fallbacks masking, JsonOutputParser drift | ~800 |
| `content/06-decision-tree.xml` | essential | Pick the right LCEL pattern | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Compose a sequential chain | haiku | Mechanical composition |
| Design a router | sonnet | Condition ordering needs judgement |
| Build a MapReduce pipeline | sonnet | Async + reduce-step design |

## Templates

| File | Purpose |
|------|---------|
| `templates/router-chain.py` | Router chain using RunnableBranch with explicit fallback default |
| `templates/_smoke-test.json` | Minimum valid chain config envelope |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-langchain-chains.py` | Validates a chain config envelope and confirms exceptions_to_handle is set | Pre-commit on chain changes |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[langchain-basics]]
- [[langchain-agents-architectures]]
- [[gateway-fallback-chain]]

## Decision tree

See `content/06-decision-tree.xml`. Root question is whether the pipeline branches by input. Branches route to Sequential, Router, MapReduce, or Fallback chain patterns.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/router-chain.py`

```python
"""Router chain template — sequential conditions + default fallback."""
from __future__ import annotations

from langchain_anthropic import ChatAnthropic
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableBranch

model = ChatAnthropic(model="claude-sonnet-4-7")
parser = StrOutputParser()

math_chain = ChatPromptTemplate.from_template("Solve this math problem: {input}") | model | parser
code_chain = ChatPromptTemplate.from_template("Write code for: {input}") | model | parser
general_chain = ChatPromptTemplate.from_template("Answer: {input}") | model | parser


def route(info: dict) -> str:
    topic = (info.get("topic") or "").lower()
    if "math" in topic:
        return "math"
    if "code" in topic:
        return "code"
    return "general"


branch = RunnableBranch(
    (lambda x: route(x) == "math", math_chain),
    (lambda x: route(x) == "code", code_chain),
    general_chain,  # default — required so unmatched inputs don't crash
).with_retry(stop_after_attempt=3, wait_exponential_jitter=True)
```

### `templates/_smoke-test.json`

```json
{
  "_purpose": "smallest valid chain config envelope for the validator",
  "_consumes": "nothing",
  "_produces": "example chain config matching content/02-output-contract.xml",
  "_depends_on": "content/01-core-rules.xml",
  "_token_budget_impact": "~40 tokens",
  "pattern": "fallback",
  "module_level": true,
  "exceptions_to_handle": [
    "openai.RateLimitError",
    "openai.APITimeoutError"
  ]
}
```
