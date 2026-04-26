---
name: faion-langchain-agents-multi-agent
user-invocable: false
description: "LangChain multi-agent systems: Supervisor, Debate, Hierarchical patterns, testing"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(python:*), Bash(pip:*)
---

# LangChain Multi-Agent Systems

**Communication: User's language. Docs/code: English.**

## Purpose

Multi-agent collaboration patterns and testing strategies using LangChain and LangGraph.

## When to Use

- Building multi-agent collaboration systems
- Implementing agent supervision and routing
- Creating debate and consensus systems
- Hierarchical team coordination
- Testing agent systems

---

# Section 1: Multi-Agent Patterns

## Pattern 1: Supervisor Architecture

One agent routes to specialized workers.

```python
from langgraph.graph import StateGraph, END
from typing import TypedDict, Literal

class TeamState(TypedDict):
    input: str
    next_agent: str
    messages: list
    final_answer: str

def supervisor(state: TeamState) -> TeamState:
    """Route to appropriate specialist."""
    prompt = f"""You are a supervisor. Route this query to the right agent.
    Options: researcher, coder, writer

    Query: {state['input']}

    Respond with just the agent name."""

    response = model.invoke(prompt)
    return {"next_agent": response.content.strip().lower()}

def researcher(state: TeamState) -> TeamState:
    """Research specialist."""
    response = model.invoke(f"Research this: {state['input']}")
    return {"messages": [f"Researcher: {response.content}"]}

def coder(state: TeamState) -> TeamState:
    """Coding specialist."""
    response = model.invoke(f"Write code for: {state['input']}")
    return {"messages": [f"Coder: {response.content}"]}

def writer(state: TeamState) -> TeamState:
    """Writing specialist."""
    response = model.invoke(f"Write content for: {state['input']}")
    return {"messages": [f"Writer: {response.content}"]}

def route_to_agent(state: TeamState) -> str:
    return state["next_agent"]

# Build
graph = StateGraph(TeamState)
graph.add_node("supervisor", supervisor)
graph.add_node("researcher", researcher)
graph.add_node("coder", coder)
graph.add_node("writer", writer)

graph.set_entry_point("supervisor")
graph.add_conditional_edges(
    "supervisor",
    route_to_agent,
    {"researcher": "researcher", "coder": "coder", "writer": "writer"}
)
graph.add_edge("researcher", END)
graph.add_edge("coder", END)
graph.add_edge("writer", END)

team = graph.compile()
```

## Pattern 2: Debate Architecture

Agents debate to reach consensus.

```python
class DebateState(TypedDict):
    topic: str
    positions: list[dict]
    round: int
    consensus: str | None

def agent_a(state: DebateState) -> DebateState:
    """First debater."""
    context = "\n".join([f"{p['agent']}: {p['argument']}" for p in state["positions"]])

    prompt = f"""You are Agent A in a debate.
    Topic: {state['topic']}
    Previous arguments: {context}

    Present your position."""

    response = model.invoke(prompt)
    return {
        "positions": [{"agent": "A", "argument": response.content}],
        "round": state["round"] + 1
    }

def agent_b(state: DebateState) -> DebateState:
    """Second debater."""
    context = "\n".join([f"{p['agent']}: {p['argument']}" for p in state["positions"]])

    prompt = f"""You are Agent B in a debate.
    Topic: {state['topic']}
    Previous arguments: {context}

    Present your counterargument."""

    response = model.invoke(prompt)
    return {"positions": [{"agent": "B", "argument": response.content}]}

def judge(state: DebateState) -> DebateState:
    """Judge the debate."""
    context = "\n".join([f"{p['agent']}: {p['argument']}" for p in state["positions"]])

    prompt = f"""You are a judge.
    Topic: {state['topic']}
    Arguments: {context}

    Determine if consensus is reached. If yes, summarize it.
    If no, say "No consensus"."""

    response = model.invoke(prompt)
    consensus = None if "No consensus" in response.content else response.content
    return {"consensus": consensus}

def should_continue_debate(state: DebateState) -> str:
    if state.get("consensus"):
        return END
    if state["round"] >= 5:
        return END
    return "agent_a"

# Build
graph = StateGraph(DebateState)
graph.add_node("agent_a", agent_a)
graph.add_node("agent_b", agent_b)
graph.add_node("judge", judge)

graph.set_entry_point("agent_a")
graph.add_edge("agent_a", "agent_b")
graph.add_edge("agent_b", "judge")
graph.add_conditional_edges("judge", should_continue_debate)

debate = graph.compile()
```

## Pattern 3: Hierarchical Teams

Teams of teams with delegation.

```python
class HierarchicalState(TypedDict):
    task: str
    team: str
    subtasks: list[str]
    results: list[str]
    final_output: str

# Research team
def research_lead(state: HierarchicalState) -> HierarchicalState:
    """Research team lead - delegates to researchers."""
    return {"subtasks": ["search web", "analyze papers", "summarize"]}

research_team = StateGraph(HierarchicalState)
research_team.add_node("lead", research_lead)
research_team.add_node("searcher", searcher_node)
research_team.add_node("analyzer", analyzer_node)
# ... build team

# Engineering team
def eng_lead(state: HierarchicalState) -> HierarchicalState:
    """Engineering team lead."""
    return {"subtasks": ["design", "implement", "test"]}

eng_team = StateGraph(HierarchicalState)
eng_team.add_node("lead", eng_lead)
# ... build team

# Top-level coordinator
def coordinator(state: HierarchicalState) -> HierarchicalState:
    """Coordinate between teams."""
    prompt = f"Which team should handle: {state['task']}? research or engineering"
    response = model.invoke(prompt)
    return {"team": response.content.strip().lower()}

def route_team(state: HierarchicalState) -> str:
    return state["team"]

main = StateGraph(HierarchicalState)
main.add_node("coordinator", coordinator)
main.add_node("research", research_team.compile())
main.add_node("engineering", eng_team.compile())

main.set_entry_point("coordinator")
main.add_conditional_edges(
    "coordinator",
    route_team,
    {"research": "research", "engineering": "engineering"}
)

organization = main.compile()
```

---

# Section 2: Testing Agents

```python
import pytest
from unittest.mock import Mock, patch

def test_agent_tool_selection():
    """Test that agent selects correct tool."""
    with patch("langchain_openai.ChatOpenAI") as mock_llm:
        mock_llm.return_value.invoke.return_value = Mock(
            tool_calls=[{"name": "search", "args": {"query": "test"}}]
        )

        result = agent.invoke({"messages": [("human", "Search for test")]})

        assert "search" in str(result)

def test_chain_output_format():
    """Test chain returns expected format."""
    result = chain.invoke({"input": "test"})

    assert isinstance(result, str)
    assert len(result) > 0

# Integration test with real LLM
@pytest.mark.integration
def test_full_workflow():
    """Test complete workflow end-to-end."""
    result = workflow.invoke({"input": "Analyze this data"})

    assert result["final_answer"] is not None
    assert "error" not in result
```

---

# Quick Reference

## Multi-Agent Patterns

| Pattern | Description | Use Case |
|---------|-------------|----------|
| Supervisor | Route to specialists | Task delegation |
| Debate | Collaborative reasoning | Decision making |
| Hierarchical | Nested teams | Complex organizations |

## Testing Strategies

| Strategy | Purpose |
|----------|---------|
| Mock LLM calls | Unit test logic |
| Check output format | Validate structure |
| Integration tests | End-to-end validation |
| Tool selection tests | Verify correct tool usage |

---

# Related

| File | Purpose |
|------|---------|
| [langchain-agents-architectures.md](langchain-agents-architectures.md) | Agent architectures and tools |
| [multi-agent-systems.md](multi-agent-systems.md) | Multi-agent coordination |
| [multi-agent-design-patterns.md](multi-agent-design-patterns.md) | Advanced patterns |

| Agent | Purpose |
|-------|---------|
| faion-autonomous-agent-builder-agent | Build custom LangGraph agents |
| faion-llm-cli-agent | CLI interactions with LangChain |
| faion-rag-agent | RAG with LangChain/LlamaIndex |

---

*faion-langchain-agents-multi-agent v1.0*
*LangChain 0.3.x / LangGraph 0.2.x*
*Covers: Supervisor, Debate, Hierarchical patterns, testing*
## Agent Selection

| Task | Model | Rationale |
|------|-------|-----------|
| Generate tool definitions from API | haiku | Mechanical transformation |
| Review agent reasoning chains | sonnet | Requires logic analysis |
| Design multi-agent orchestration | opus | Complex coordination patterns |

