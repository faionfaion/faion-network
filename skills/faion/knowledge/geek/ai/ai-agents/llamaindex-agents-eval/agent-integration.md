# Agent Integration — LlamaIndex Agents & Evaluation

## When to use
- Building autonomous agents that combine RAG retrieval with custom tool execution (calculators, APIs, code runners)
- Implementing automated evaluation gates: block response delivery if faithfulness score < threshold
- Production RAG system that requires measurable quality metrics reported per-deployment or per-query batch
- Multi-agent orchestration where a research agent and an analysis agent share context through LlamaIndex query engine tools
- LlamaCloud integration for organizations that need managed document parsing (LlamaParse) without running local extraction infra

## When NOT to use
- The agent's primary task is workflow orchestration with branching — LangGraph/LlamaIndex agents have no graph state; use LangGraph instead
- Evaluation is needed across heterogeneous LLM outputs (not RAG-specific) — Ragas or DeepEval are more flexible evaluation frameworks
- You need Anthropic-native structured tool use without RAG — direct Claude API with `tools` parameter is simpler
- `MultiAgentRunner` is needed at scale — it is experimental; for production multi-agent, prefer LangGraph supervisor pattern
- Cost is critical: LLM-based evaluators (faithfulness, relevancy) cost as much per evaluation as a retrieval query

## Where it fails / limitations
- `ReActAgent.chat()` loop can exceed `max_iterations` without resolving the task — agent returns empty result; must handle `AgentChatResponse` with no output gracefully
- `FunctionCallingAgentWorker` requires the underlying LLM to support function calling — fails silently with models that don't (returns prose instead of tool calls)
- `MultiAgentRunner` routing prompt is not deterministic — same query may route to different agents across invocations; not suitable for deterministic pipelines
- `BatchEvalRunner` with `workers=4` opens concurrent LLM calls — rate limits hit fast; no built-in semaphore
- `FaithfulnessEvaluator` uses LLM judgment, not grounded fact-checking — high faithfulness score does not mean the answer is factually correct, only that it's consistent with retrieved context
- `LlamaParse` requires network call to LlamaCloud API — adds latency and fails if API is down; no local fallback

## Agentic workflow
An LlamaIndex agent is wrapped as a tool-using module by the outer orchestrator. The orchestrator calls the agent's `chat()` method with a task description; the agent selects and invokes query engine tools, function tools, or calculation tools autonomously. After the agent returns, an evaluation subagent scores the response for faithfulness and relevancy; if both pass, the result is delivered. This pattern creates a quality gate without human review for routine queries. For complex tasks, the evaluation agent can trigger a second agent pass with a refined query.

### Recommended subagents
- `faion-rag-agent` — wraps LlamaIndex `ReActAgent` with query engine tools; handles multi-tool reasoning; returns structured response + source nodes
- Quality gate subagent — receives (query, response, context_nodes), runs faithfulness + relevancy evaluators, returns pass/fail + scores

### Prompt pattern
```
You are a document analysis agent with access to these tools:
  - knowledge_base: Search product documentation
  - financial_data: Query financial metrics index

Task: "{task}"
Use tools as needed. After each tool call, assess whether you have enough information.
Return: {"answer": str, "tools_used": [str], "confidence": float}
```

```
Evaluate this RAG response for quality:
  query: "{query}"
  response: "{response}"
  context_nodes: {nodes_json}

Run faithfulness_evaluator and relevancy_evaluator.
Return: {"faithfulness": float, "relevancy": float, "pass": bool, "flags": [str]}
Threshold: faithfulness >= 0.75, relevancy >= 0.70
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `llama-index` | Agent framework + evaluation primitives | `pip install llama-index` |
| `llama-parse` | Cloud document parser (LlamaParse) | `pip install llama-parse` |
| `llama-index-agent-openai` | OpenAI function-calling agent | `pip install llama-index-agent-openai` |
| `llama-index-instrumentation-langfuse` | Langfuse observability integration | `pip install llama-index-instrumentation-langfuse` |
| `ragas` | Alternative evaluation framework (faithfulness, answer relevancy, context recall) | `pip install ragas` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| LlamaCloud | SaaS | Yes | Managed parsing + indexing; LlamaParse for complex PDFs |
| Langfuse | OSS/SaaS | Yes | Per-agent-step tracing; native LlamaIndex instrumentation |
| Arize Phoenix | OSS | Yes | LLM observability with RAG evaluation metrics |
| Weights & Biases (W&B) | SaaS | Partial | Log evaluation results as W&B tables for trend analysis |
| Cohere Rerank | SaaS | Yes | API-based reranking callable from custom function tool |
| Qdrant | OSS | Yes | Vector store for agent query engine tools |

## Templates & scripts
See `templates.md` for agent and evaluation templates. Inline agent with quality gate:

```python
import asyncio
from llama_index.core.agent import ReActAgent
from llama_index.core.tools import QueryEngineTool, FunctionTool
from llama_index.core.evaluation import FaithfulnessEvaluator, RelevancyEvaluator
from llama_index.llms.anthropic import Anthropic

llm = Anthropic(model="claude-opus-4-5")

# Tool from existing index
kb_tool = QueryEngineTool.from_defaults(
    query_engine=index.as_query_engine(),
    name="knowledge_base",
    description="Search product knowledge base"
)

agent = ReActAgent.from_tools([kb_tool], llm=llm, max_iterations=8)

async def query_with_eval(task: str) -> dict:
    response = agent.chat(task)
    faith_eval = FaithfulnessEvaluator(llm=llm)
    rel_eval = RelevancyEvaluator(llm=llm)

    faith_result, rel_result = await asyncio.gather(
        faith_eval.aevaluate_response(query=task, response=response),
        rel_eval.aevaluate_response(query=task, response=response)
    )

    return {
        "answer": str(response),
        "faithfulness": faith_result.score,
        "relevancy": rel_result.score,
        "pass": faith_result.passing and rel_result.passing
    }
```

## Best practices
- Set `max_iterations=8` on `ReActAgent` explicitly — the default allows too many steps and increases cost on runaway tasks
- Run `FaithfulnessEvaluator` and `RelevancyEvaluator` with `aevaluate_response()` in parallel using `asyncio.gather()` — sequential evaluation doubles the evaluation latency
- Generate evaluation datasets offline with `generate_question_context_pairs()` before deployment; evaluate new index versions against the same dataset to track quality over time
- Use `LlamaParse` for any PDF with tables, columns, or scanned content; default `SimpleDirectoryReader` PDF parsing strips table structure
- In `MultiAgentRunner`, write the orchestrator prompt to explicitly list agent names and their domains — vague orchestrator prompts cause consistent routing errors
- Cache `BatchEvalRunner` results to disk (JSON) so re-evaluation after minor index changes can reuse unchanged question results
- Monitor `agent.chat()` latency per tool call — if a single tool call exceeds 5 seconds, the agent should time out and return partial results rather than blocking

## AI-agent gotchas
- `ReActAgent` stops calling tools when the LLM generates a final answer tag without completing the task — add explicit output validation in a post-processing step
- `OpenAIAgent` and `ReActAgent` use different internal prompting strategies; switching agent type for the same tools changes behavior in non-obvious ways
- `FunctionTool.from_defaults(fn=calculate)` uses `eval()` internally in some examples — never pass user-controlled input directly to eval-based function tools
- `BatchEvalRunner` with default `workers=1` processes sequentially; increase `workers` cautiously — each worker opens a new LLM call concurrently and exhausts rate limits fast
- `LlamaCloudIndex` silently falls back to an empty index if the project/index name is wrong — always validate response count before trusting results
- `ChatMemoryBuffer` in agent memory is not persisted by default — agent loses conversation history on process restart; serialize memory to disk or use external memory store

## References
- https://docs.llamaindex.ai/en/stable/examples/agent/
- https://docs.llamaindex.ai/en/stable/examples/evaluation/
- https://cloud.llamaindex.ai/
- https://docs.llamaindex.ai/en/stable/module_guides/deploying/agents/
- Ragas evaluation framework: https://docs.ragas.io/
