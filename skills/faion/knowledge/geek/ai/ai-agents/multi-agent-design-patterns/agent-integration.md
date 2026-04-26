# Agent Integration — Multi-Agent Design Patterns

## When to use
- Enterprise workflow automation where no single agent has all required expertise (use Hierarchical Decomposition)
- Content or code quality checks that must catch every error, not just obvious ones (use Generator-Critic)
- Multi-dimensional analysis tasks where independent perspectives reduce blind spots (use Parallel Fan-Out/Gather)
- Long-horizon tasks that require iterative refinement with feedback loops (use Loop Pattern)
- Workflows requiring human sign-off before irreversible steps (use Human-in-the-Loop)
- Dynamic routing across multiple knowledge domains based on query content (use Router Pattern)
- Knowledge synthesis tasks where agents share a common workspace (use Blackboard Pattern)

## When NOT to use
- Simple retrieval or single-step generation — pattern overhead adds cost with no quality gain
- Latency-critical paths where multiple sequential agent calls are unacceptable
- Tasks without clear decomposition axes — forcing patterns onto unstructured tasks creates artificial fragmentation
- Early prototyping phases where debugging orchestration complexity is not yet warranted
- Single-domain problems where one specialized agent is sufficient

## Where it fails / limitations
- **Sequential Pipeline**: each stage must handle partial or malformed output from the previous stage; no stage can "reach back" to request clarification
- **Parallel Fan-Out/Gather**: synthesis step is a single call — a weak synthesizer loses value from good parallel work
- **Hierarchical Decomposition**: plan quality determines everything; a poor planner produces subtasks that overlap or miss key work
- **Generator-Critic**: critic and generator from the same base model converge on shared blind spots; they may both miss the same class of errors
- **Loop Pattern**: without a verifiable exit criterion, loops run to the iteration cap and exit with partial quality
- **Router Pattern**: routing based on LLM classification introduces latency per-query; misrouting sends queries to the wrong expert with no automatic recovery
- **Blackboard Pattern**: concurrent writes to a shared workspace require locking or immutable append semantics to avoid data races
- **Framework dependency**: framework-specific DSLs (CrewAI, LangGraph) lock in orchestration logic; switching frameworks later is costly

## Agentic workflow
A Claude orchestrator subagent selects the appropriate pattern based on task properties (parallelizability, quality requirements, domain count), then instantiates specialized worker subagents. The orchestrator mediates all inter-agent communication and is the sole consumer of worker outputs. For the Human-in-the-Loop pattern, the orchestrator pauses execution, surfaces a decision point with full context, and only continues after receiving explicit human approval via a structured response. LangGraph is the recommended framework for patterns requiring persistent state and conditional branching.

### Recommended subagents
- `pattern-selector` — classifies task against the 8 patterns and returns recommended pattern + rationale; uses Sonnet
- `planner` — Hierarchical Decomposition: decomposes goal into subtask assignments; uses Opus
- `domain-expert-worker` — executes a focused subtask in a specific domain; uses Sonnet
- `critic` — Generator-Critic: validates output against quality rubric, returns structured feedback; uses Sonnet
- `router` — Router Pattern: classifies query and dispatches to correct specialist agent; uses Haiku

### Prompt pattern
Generator-Critic:
```xml
<role>Critic</role>
<quality_rubric>{{rubric_items}}</quality_rubric>
<generated_output>{{generator_output}}</generated_output>
<instruction>
Evaluate the output against each rubric item.
Return JSON: {"passed": ["item1"], "failed": [{"item": "item2", "reason": "...", "fix": "..."}]}
</instruction>
```

Router Pattern:
```xml
<role>Router</role>
<available_experts>{{expert_list_with_domains}}</available_experts>
<query>{{user_query}}</query>
<instruction>Select the most appropriate expert. Return JSON: {"expert": "name", "rationale": "..."}</instruction>
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `langgraph` | State-machine graphs for loop, router, and blackboard patterns | `pip install langgraph` / langchain-ai.github.io/langgraph |
| `crewai` | Role-based teams for hierarchical and collaborative patterns | `pip install crewai` / crewai.com |
| `autogen` | Conversation-centric patterns (debate, collaborative) | `pip install pyautogen` / microsoft.github.io/autogen |
| `agentops` | Observability for all patterns — cost, latency, trace | `pip install agentops` / agentops.ai |
| `prefect` | Workflow orchestration with retries and scheduling | `pip install prefect` / docs.prefect.io |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| LangGraph Cloud | SaaS | Yes | Persistent state for loop and blackboard patterns; built-in human-in-loop |
| CrewAI Enterprise | SaaS | Yes | Managed hierarchical and collaborative crew execution |
| Google Vertex AI Agent Builder | SaaS | Yes | ADK-native; implements all 8 Google ADK patterns |
| AutoGen Studio | OSS | Yes | Visual builder for conversational and generator-critic patterns |
| LangSmith | SaaS | Yes | Full trace per pattern step; invaluable for debugging routing errors |

## Templates & scripts
See `templates.md` for pattern implementations.

Generator-Critic loop (≤30 lines):
```python
def generator_critic_loop(generator_fn, critic_fn, task, max_iterations=3):
    output = generator_fn(task)
    for _ in range(max_iterations):
        feedback = critic_fn(output)
        if not feedback.get("failed"):
            return output  # all rubric items passed
        output = generator_fn(f"{task}\n\nRevise based on feedback:\n{feedback['failed']}")
    return output  # best effort after max iterations
```

## Best practices
- Match pattern to task structure before writing any code — the wrong pattern costs more to fix than to prevent
- Generator-Critic: use a **different** base model or temperature for critic vs. generator to reduce shared blind spots
- Parallel Fan-Out: cap the number of parallel workers at 5-8; more workers rarely improve synthesis quality
- Human-in-the-Loop: surface the human gate with a complete action summary, not just a yes/no prompt
- Loop Pattern: define the exit criterion as a function that returns `True`/`False`, not an LLM judgment — deterministic exits prevent runaway loops
- Router Pattern: log every routing decision with the query, chosen expert, and rationale for monitoring routing accuracy over time
- Blackboard Pattern: use append-only writes to the shared workspace; never allow agents to delete or overwrite others' contributions

## AI-agent gotchas
- **Gartner adoption surge (1445% inquiries)**: means tooling is maturing rapidly, but production battle-testing is still limited. Treat framework docs as authoritative; blog tutorials may be outdated by months.
- **Critic shares training data with generator**: generator and critic from the same model will miss the same failure modes. Consider using Claude as critic for GPT-generated output or vice versa.
- **Loop exit without success**: the loop pattern exits at `max_iterations` regardless of quality. Always inspect the final output; do not assume max iterations implies a passing result.
- **Router misclassification**: if the router sends a query to the wrong expert, downstream errors are silent — the expert produces output for a task it was not designed for. Add a confidence score to routing decisions and fall back to a generalist agent below threshold.
- **Human-in-loop synchronization**: in async pipelines, the human approval step must block the workflow, not just log a request. Use LangGraph's `interrupt_before` or an explicit polling mechanism.
- **Blackboard concurrency**: if two agents write conflicting updates to the same blackboard key, the last write wins silently. Use named, agent-scoped keys or an explicit merge protocol.

## References
- Google ADK multi-agent patterns: https://google.github.io/adk-docs/multi-agents/
- LangGraph patterns: https://langchain-ai.github.io/langgraph/concepts/multi_agent/
- CrewAI: https://github.com/joaomdmoura/crewAI
- AutoGen: https://microsoft.github.io/autogen/
- Gartner AI agent forecast (2025): https://www.gartner.com/en/articles/intelligent-agent-in-ai
