# Agent Integration — AI Agent Design Patterns

## When to use
- Selecting the right architectural pattern before implementing any agentic system
- Replacing ad-hoc "call LLM in a loop" code with a structured, debuggable pattern
- Multi-step workflows where intermediate results determine next steps (ReAct, Plan-Execute)
- Quality-critical outputs where first-pass LLM output is insufficient (Reflection)
- Creative or optimization tasks where exploring multiple solution paths is worthwhile (Tree-of-Thoughts)
- Multi-agent coordination: decomposing complex tasks across specialized agents (Hierarchical, Supervisor)

## When NOT to use
- Single LLM call with deterministic output — patterns add latency and cost without benefit
- Tasks where the full input fits in one context window and requires no tool calls — just prompt directly
- Real-time inference under 200ms — ReAct, Reflection, and ToT all require multiple round-trips
- When you need reproducible outputs for auditing — agent non-determinism conflicts with strict reproducibility requirements

## Where it fails / limitations
- ReAct: thought-action-observation loops compound errors — a wrong observation at step 3 corrupts all subsequent reasoning
- Chain-of-Thought: self-consistency voting requires 3-10 LLM calls per question, multiplying cost proportionally
- Reflection: without a concrete checklist of criteria, the critique pass produces vague "could be better" feedback that does not improve output
- Tree-of-Thoughts: state-space explosion at depth 3+ makes it computationally infeasible without aggressive pruning
- Plan-Execute: the planner's task decomposition assumes tool outputs are deterministic — unexpected failures cascade through the entire plan
- Multi-agent Supervisor: if the supervisor prompt is underspecified, it reassigns the same task to the same worker repeatedly; infinite routing loops are possible

## Agentic workflow
Map Claude subagents directly to pattern roles: for ReAct, a single Claude subagent runs the Thought-Action-Observation loop with tools injected as functions; for Plan-Execute, spawn an Opus subagent as planner and Haiku subagents as executors; for Reflection, add a critic subagent that receives the draft and a structured critique rubric. Combine patterns by nesting: use ReAct for each step in a Plan-Execute workflow, and wrap the final output in a Reflection pass. Pattern selection should happen at system design time, not dynamically — switching patterns mid-execution adds complexity without gain.

### Recommended subagents
- `planner` — decomposes goal into ordered task list with dependencies (use Opus for complex domains)
- `executor` — handles a single atomic task given inputs and tools (use Haiku for mechanical steps)
- `critic` — evaluates output against explicit criteria list, returns structured pass/fail with specific defects
- `supervisor` — routes task to specialist worker agents, aggregates results, resolves conflicts
- `verifier` — binary check: does the output satisfy all success criteria? returns bool + reason

### Prompt pattern
```
# Reflection critic prompt
You are a strict quality reviewer. Evaluate this output against the criteria below.

Output to review:
{output}

Criteria (check each explicitly):
1. Accuracy: all factual claims are verifiable
2. Completeness: all required sections present
3. Tone: matches target audience ({audience})
4. Length: between {min_words} and {max_words} words

Return JSON: {"passed": bool, "defects": [{"criterion": str, "issue": str, "fix": str}]}
```

```python
# Plan-Execute skeleton with model tiering
def plan_execute(goal: str, tools: dict, max_tasks: int = 10) -> str:
    # Expensive model for planning
    plan = opus_call(f"Decompose into ordered tasks (max {max_tasks}): {goal}")
    tasks = parse_task_list(plan)

    results = []
    for task in tasks:
        # Cheap model for execution
        result = haiku_call(f"Execute: {task.description}\nContext: {results}\nTools: {list(tools)}")
        tool_result = run_tools_if_needed(result, tools)
        results.append({"task": task.description, "result": tool_result})

    return sonnet_call(f"Synthesize final answer from: {results}\nGoal: {goal}")
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `langgraph` | State machine implementation of agent patterns | `pip install langgraph` / https://langchain-ai.github.io/langgraph/ |
| `autogen` | Multi-agent conversation patterns (Microsoft) | `pip install pyautogen` / https://microsoft.github.io/autogen/ |
| `crewai` | Role-based agent teams (Supervisor pattern) | `pip install crewai` / https://docs.crewai.com/ |
| `dspy` | Programmatic prompt optimization for CoT patterns | `pip install dspy-ai` / https://dspy-docs.vercel.app/ |
| `agentops` | Pattern execution tracing and replay | `pip install agentops` / https://www.agentops.ai/ |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| LangSmith | SaaS | Yes | Visualize ReAct loops, Plan-Execute graphs, Reflection cycles as traces |
| Weights & Biases | SaaS | Partial | Log multi-agent runs as experiments; compare pattern variants |
| Arize Phoenix | OSS | Yes | Open-source alternative to LangSmith; no API key |
| LangGraph Cloud | SaaS | Yes | Managed LangGraph execution with checkpointing; native human-in-loop |
| Temporal | OSS | Yes | Durable workflow engine for Plan-Execute patterns with retry semantics |

## Templates & scripts
See `templates.md` for complete pattern implementations.

Minimal Reflection loop:
```python
def reflection_loop(
    generate_fn,
    critique_fn,
    task: str,
    max_cycles: int = 3,
) -> str:
    output = generate_fn(task)
    for cycle in range(max_cycles):
        critique = critique_fn(task, output)
        if critique["passed"]:
            return output
        revision_prompt = f"Revise output to fix these defects:\n{critique['defects']}\n\nOriginal:\n{output}"
        output = generate_fn(revision_prompt)
    return output  # return best effort after max cycles
```

## Best practices
- Choose the simplest pattern that solves the problem: ReAct before Plan-Execute, single-agent before multi-agent
- Always define explicit exit conditions for iterative patterns (Reflection, ReAct) — vague "stop when satisfied" creates unbounded loops
- Use model tiering across patterns: Opus for planning/critique, Sonnet for reasoning, Haiku for mechanical execution
- Log pattern metadata (pattern type, iteration count, tool calls, model used) alongside outputs — enables debugging and cost analysis
- In Plan-Execute, include a replanning step: if an executor task fails 3x, return to the planner to revise the task list
- For multi-agent Supervisor patterns, each worker must have a well-defined scope and return structured output — open-ended worker responses cause supervisor confusion

## AI-agent gotchas
- CoT self-consistency majority voting assumes 3+ independent samples — if the LLM has a systematic bias on the task, voting amplifies the bias rather than correcting it
- Tree-of-Thoughts requires a reliable evaluation function for branch pruning — using another LLM call as evaluator doubles cost per branch; define a cheap heuristic first
- Reflection critic prompted too harshly will always find defects — use a balanced rubric with a concrete "pass threshold" (≤1 minor defect = pass)
- Plan-Execute planners sometimes generate plans with circular dependencies — validate the task graph for cycles before executing
- Human-in-the-loop checkpoint: for Supervisor patterns managing external actions (API calls, emails, database writes), add a human approval step before the supervisor dispatches to workers — prevents cascading errors from misrouted tasks

## References
- ReAct paper: https://arxiv.org/abs/2210.03629
- Reflexion paper: https://arxiv.org/abs/2303.11366
- Tree-of-Thoughts paper: https://arxiv.org/abs/2305.10601
- Google Cloud agent patterns: https://cloud.google.com/architecture/choose-design-pattern-agentic-ai-system
- Anthropic multi-agent guide: https://docs.anthropic.com/en/docs/build-with-claude/agents
- DSPy for optimizing CoT: https://dspy-docs.vercel.app/
