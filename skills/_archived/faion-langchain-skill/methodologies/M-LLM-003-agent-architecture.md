# M-LLM-003: Agent Architecture

## Overview

AI agents are autonomous systems that use LLMs to reason, plan, and execute actions. Unlike simple chains, agents dynamically decide which tools to use and when. Key patterns include ReAct (Reasoning + Acting), Plan-and-Execute, and LATS (Language Agent Tree Search).

**When to use:** Complex tasks requiring dynamic decision-making, tool use, or multi-step problem solving.

## Core Concepts

### 1. Agent Components

```
┌─────────────────────────────────────────────┐
│                   AGENT                      │
├─────────────────────────────────────────────┤
│  ┌─────────┐  ┌─────────┐  ┌─────────────┐  │
│  │ Planner │→ │ Memory  │→ │ Tool Router │  │
│  └─────────┘  └─────────┘  └─────────────┘  │
│       ↓            ↓             ↓          │
│  ┌─────────┐  ┌─────────┐  ┌─────────────┐  │
│  │  LLM    │  │ Context │  │   Tools     │  │
│  └─────────┘  └─────────┘  └─────────────┘  │
└─────────────────────────────────────────────┘
```

| Component | Purpose | Implementation |
|-----------|---------|----------------|
| **Planner** | Decides next action | LLM with planning prompt |
| **Memory** | Stores conversation/actions | Vector DB or buffer |
| **Tools** | Execute actions | Functions, APIs, code |
| **Executor** | Runs tools | Function calling |
| **Reflector** | Evaluates progress | LLM self-critique |

### 2. Agent Types

| Type | Behavior | Use Case |
|------|----------|----------|
| **Reactive** | Respond to input | Simple Q&A |
| **Deliberative** | Plan before acting | Complex tasks |
| **Hybrid** | Mix of both | Production systems |

### 3. Reasoning Patterns

| Pattern | Description | Strengths |
|---------|-------------|-----------|
| **ReAct** | Thought → Action → Observation | Simple, interpretable |
| **Plan-Execute** | Full plan → Execute steps | Better for complex tasks |
| **LATS** | Tree search with backtracking | Handles uncertainty |
| **Reflexion** | Self-critique and improve | Higher quality |

## Best Practices

### 1. Define Clear Tool Interfaces

```python
from langchain.tools import StructuredTool
from pydantic import BaseModel, Field

class SearchInput(BaseModel):
    """Input for web search tool."""
    query: str = Field(description="Search query")
    max_results: int = Field(default=5, description="Max results")

def web_search(query: str, max_results: int = 5) -> str:
    """Search the web and return results."""
    # Implementation
    pass

search_tool = StructuredTool.from_function(
    func=web_search,
    name="web_search",
    description="Search the web for current information",
    args_schema=SearchInput
)
```

### 2. Implement Guardrails

```python
class SafeAgent:
    def __init__(self, agent, max_iterations=10, forbidden_actions=None):
        self.agent = agent
        self.max_iterations = max_iterations
        self.forbidden_actions = forbidden_actions or []

    def run(self, input):
        for i in range(self.max_iterations):
            action = self.agent.plan(input)

            # Check guardrails
            if action.tool in self.forbidden_actions:
                return "Action not permitted"

            if self.agent.is_complete(action):
                return action.result

        return "Max iterations reached"
```

### 3. Use Structured Outputs

```python
class AgentResponse(BaseModel):
    thought: str = Field(description="Agent's reasoning")
    action: str = Field(description="Tool to use or 'final_answer'")
    action_input: dict = Field(description="Input for the tool")

# In agent prompt
"""
Respond in this exact format:
{
  "thought": "I need to search for current data",
  "action": "web_search",
  "action_input": {"query": "latest AI news", "max_results": 3}
}
"""
```

## Common Patterns

### Pattern 1: ReAct Agent

```python
from langchain.agents import AgentExecutor, create_react_agent

react_prompt = """
Answer the following question using available tools.

Available tools:
{tools}

Use this format:
Thought: Consider what to do
Action: tool_name
Action Input: input for the tool
Observation: result from tool
... (repeat as needed)
Thought: I now know the answer
Final Answer: the final answer

Question: {input}
{agent_scratchpad}
"""

agent = create_react_agent(llm, tools, react_prompt)
executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
result = executor.invoke({"input": "What is the weather in Tokyo?"})
```

### Pattern 2: Plan-and-Execute Agent

```python
from langchain_experimental.plan_and_execute import (
    PlanAndExecute,
    load_agent_executor,
    load_chat_planner
)

# Planner creates full plan upfront
planner = load_chat_planner(llm)

# Executor runs each step
executor = load_agent_executor(llm, tools, verbose=True)

# Combined agent
agent = PlanAndExecute(
    planner=planner,
    executor=executor,
    verbose=True
)

result = agent.run("Research and summarize the top 3 AI frameworks")
```

### Pattern 3: LangGraph Agent (Stateful)

```python
from langgraph.graph import StateGraph, END
from typing import TypedDict

class AgentState(TypedDict):
    messages: list
    current_step: str
    tool_results: dict

def reasoning_node(state: AgentState):
    # LLM decides next action
    response = llm.invoke(state["messages"])
    return {"messages": state["messages"] + [response]}

def tool_node(state: AgentState):
    # Execute selected tool
    tool_call = state["messages"][-1].tool_calls[0]
    result = tools[tool_call["name"]].invoke(tool_call["args"])
    return {"tool_results": {tool_call["name"]: result}}

def should_continue(state: AgentState):
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        return "tools"
    return END

# Build graph
workflow = StateGraph(AgentState)
workflow.add_node("reason", reasoning_node)
workflow.add_node("tools", tool_node)
workflow.add_conditional_edges("reason", should_continue)
workflow.add_edge("tools", "reason")
workflow.set_entry_point("reason")

agent = workflow.compile()
```

### Pattern 4: Multi-Tool Agent

```python
tools = [
    web_search_tool,
    calculator_tool,
    code_executor_tool,
    file_reader_tool,
    database_query_tool
]

# Agent automatically selects appropriate tool
agent_prompt = """
You have access to these tools:
- web_search: Search the internet
- calculator: Perform calculations
- code_executor: Run Python code
- file_reader: Read local files
- database_query: Query the database

For each step, choose the most appropriate tool.
If no tool is needed, provide the final answer.

Task: {input}
"""
```

## Anti-patterns

| Anti-pattern | Problem | Solution |
|--------------|---------|----------|
| Unbounded loops | Agent runs forever | Set max_iterations |
| No error recovery | Single failure stops agent | Add retry logic |
| Missing tool descriptions | Poor tool selection | Detailed, clear descriptions |
| No memory management | Context overflow | Summarize long histories |
| Unsafe tool access | Security risks | Sandbox and validate |

## Agent Design Checklist

### Planning
- [ ] Clear task decomposition
- [ ] Appropriate reasoning pattern selected
- [ ] Tool set defined with descriptions
- [ ] Success criteria established

### Implementation
- [ ] Max iterations set
- [ ] Error handling for each tool
- [ ] Memory/context management
- [ ] Structured outputs defined

### Safety
- [ ] Guardrails implemented
- [ ] Dangerous actions blocked
- [ ] Human-in-the-loop for critical actions
- [ ] Audit logging enabled

### Testing
- [ ] Unit tests for tools
- [ ] Integration tests for agent flow
- [ ] Edge case handling
- [ ] Performance benchmarks

## Tools & References

### Related Skills
- faion-langchain-skill
- faion-llamaindex-skill

### Related Agents
- faion-autonomous-agent-builder-agent
- faion-rag-agent

### External Resources
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [ReAct Paper](https://arxiv.org/abs/2210.03629)
- [Plan-and-Solve Paper](https://arxiv.org/abs/2305.04091)
- [LATS Paper](https://arxiv.org/abs/2310.04406)

## Checklist

- [ ] Selected appropriate agent pattern
- [ ] Defined all required tools
- [ ] Implemented memory strategy
- [ ] Added guardrails and limits
- [ ] Set up error handling
- [ ] Created evaluation metrics
- [ ] Tested with varied inputs
- [ ] Documented agent behavior

---

*Methodology: M-LLM-003 | Category: LLM/Orchestration*
*Related: faion-autonomous-agent-builder-agent, faion-langchain-skill*
