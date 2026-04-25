# Agent Integration — AI Agent Patterns

## When to use
- Choosing a control flow pattern (CoT, ReAct, Plan-and-Execute) for a new agent task
- Explaining why a single prompt-response fails and what pattern would address the gap
- Selecting a framework (LangGraph, AutoGen, CrewAI, OpenAI Agents SDK) for a new agent project
- Debugging an agent that loops, hallucinates, or fails to use tools correctly — pattern mismatch is often the root cause

## When NOT to use
- Tasks solvable in a single LLM call — adding an agent pattern introduces latency and token overhead with no benefit
- Creative generation tasks where strict control flow degrades output quality
- When the framework dependency cost exceeds the project lifetime (e.g., a one-off script using LangGraph)
- Hard real-time tasks where multi-iteration loops are too slow (< 500ms SLA)

## Where it fails / limitations
- Chain of Thought (CoT) degrades on tasks requiring factual recall; the model reasons confidently to wrong conclusions
- ReAct (Reason + Act) loops can get stuck in circular Thought → Action → Observation cycles without progress if the tool returns ambiguous results
- Plan-and-Execute breaks when the initial plan is wrong and the replanning step is not implemented — agents proceed to execute an invalid plan to completion
- Framework abstractions (LangGraph state machines, AutoGen conversations) add debugging complexity; errors manifest several layers below the business logic
- Tool Use Pattern requires precise tool descriptions; vague descriptions cause the agent to select the wrong tool or pass malformed arguments

## Agentic workflow
Use Claude Haiku to generate initial tool definitions from an API schema (mechanical transformation). Use Claude Sonnet to review agent reasoning chains (requires logic analysis across multiple steps). Use Claude Opus only when designing multi-agent orchestration where coordination patterns are genuinely complex. For production NERO pipelines, ReAct is the default pattern; Plan-and-Execute is used when a task has more than 5 sequential steps requiring inter-step dependencies.

### Recommended subagents
- `faion-sdd-executor-agent` — implements agent patterns as defined in SDD design docs
- `nero-sdd-executor-agent` — NERO-side agent pattern implementation

### Prompt pattern
```xml
<agent_pattern_selection>
  <task>Gather competitor pricing data for 10 SaaS tools, synthesize into a comparison table</task>
  <constraints>
    <tools_available>web_search, file_write</tools_available>
    <max_steps>15</max_steps>
  </constraints>
  <candidate_patterns>CoT, ReAct, Plan-and-Execute</candidate_patterns>
  <output>Selected pattern with rationale. If Plan-and-Execute: output initial plan as numbered steps.</output>
</agent_pattern_selection>
```

```xml
<react_loop>
  <system>You are a research agent. For each step, output:
Thought: <reasoning>
Action: <tool_name>(<args>)
Then wait for Observation before continuing.
Only output Final Answer when the task is complete.</system>
  <task>{{research_task}}</task>
</react_loop>
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `anthropic` SDK | Core LLM calls for all patterns | `pip install anthropic` |
| `langgraph` | State machine for Plan-and-Execute and complex ReAct | `pip install langgraph` / [docs](https://langchain-ai.github.io/langgraph/) |
| `autogen` | Multi-agent conversation pattern | `pip install pyautogen` / [docs](https://microsoft.github.io/autogen/) |
| `crewai` | Role-based agent teams | `pip install crewai` / [docs](https://docs.crewai.com/) |
| `openai` SDK | OpenAI Agents SDK (tool use pattern reference) | `pip install openai` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| LangGraph | OSS | Yes | Best for stateful Plan-and-Execute; steep learning curve |
| AutoGen | OSS (Microsoft) | Yes | Multi-agent conversation; good for role specialization |
| CrewAI | OSS | Yes | Role-based teams; simpler API than AutoGen |
| OpenAI Agents SDK | SaaS/OSS | Yes | Official OpenAI; tightly coupled to OpenAI models |
| LangSmith | SaaS | Yes — SDK | Pattern execution tracing; essential for ReAct debugging |
| Modal | SaaS | Yes | Sandboxed tool execution for Tool Use Pattern |

## Templates & scripts
See `templates.md` for full pattern templates. Minimal ReAct implementation for Claude:

```python
import anthropic, re

client = anthropic.Anthropic()

SYSTEM = """You are a ReAct agent. Format each step as:
Thought: <your reasoning>
Action: <tool_name>(<json_args>)

When done, output:
Final Answer: <answer>"""

def run_react(task: str, tool_fns: dict, max_steps: int = 10) -> str:
    messages = [{"role": "user", "content": task}]
    for _ in range(max_steps):
        r = client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=1024,
            system=SYSTEM,
            messages=messages
        )
        text = r.content[0].text
        messages.append({"role": "assistant", "content": text})
        if "Final Answer:" in text:
            return text.split("Final Answer:")[-1].strip()
        action_match = re.search(r"Action: (\w+)\((.+?)\)", text, re.DOTALL)
        if action_match:
            tool_name, args_str = action_match.groups()
            import json
            args = json.loads(args_str) if args_str.strip().startswith("{") else {"input": args_str}
            fn = tool_fns.get(tool_name)
            observation = fn(**args) if fn else f"Unknown tool: {tool_name}"
            messages.append({"role": "user", "content": f"Observation: {observation}"})
    return "Max steps reached without final answer"
```

## Best practices
- Match pattern to task structure before selecting a framework: CoT for pure reasoning, ReAct for tool-dependent research, Plan-and-Execute for multi-step workflows with dependencies
- Implement explicit loop-detection: if the last 3 Thought→Action cycles are identical, break and return an error rather than continuing
- Use structured output (JSON schema) for Plan-and-Execute plan steps; free-text plans degrade execution reliability
- Test each pattern on a known-answer benchmark before production deployment; patterns that work on toy examples often fail on real tasks
- For multi-agent patterns (AutoGen, CrewAI), assign exactly one responsibility per agent; agents with overlapping roles produce contradictory outputs

## AI-agent gotchas
- ReAct agents with access to a general web-search tool will spend iterations searching for information they already have in context — set a `no_redundant_search` rule in the system prompt
- Plan-and-Execute agents that don't replan after a failed step will complete all remaining steps against an invalid intermediate state
- CoT prompting ("Let's think step by step") works on Claude and GPT-4 class models but degrades on smaller models; don't assume it transfers
- Framework abstractions (LangGraph, CrewAI) hide token costs; always instrument token usage per agent call, not per framework invocation
- The Tool Use Pattern requires tools to return deterministic, parseable output; tools that return HTML, markdown, or unstructured text cause the agent to hallucinate parsed results

## References
- [ReAct Paper](https://arxiv.org/abs/2210.03629)
- [LangGraph Docs](https://langchain-ai.github.io/langgraph/)
- [AutoGen Docs](https://microsoft.github.io/autogen/)
- [CrewAI Docs](https://docs.crewai.com/)
- [OpenAI Agents SDK](https://platform.openai.com/docs/guides/agents)
- [Anthropic Tool Use](https://docs.anthropic.com/en/docs/tool-use)
