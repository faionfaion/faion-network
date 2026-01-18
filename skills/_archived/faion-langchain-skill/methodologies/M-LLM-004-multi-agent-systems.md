# M-LLM-004: Multi-Agent Systems

## Overview

Multi-agent systems coordinate multiple AI agents working together on complex tasks. Agents can have specialized roles, debate solutions, or work in hierarchies. Patterns include supervisor agents, hierarchical teams, and debate/critique systems.

**When to use:** Tasks too complex for single agents, requiring diverse expertise, or benefiting from multiple perspectives.

## Core Concepts

### 1. Multi-Agent Architectures

```
┌─────────────────────────────────────────────────────┐
│                  SUPERVISOR                          │
│            (orchestrates, delegates)                 │
└───────────┬───────────┬───────────┬────────────────┘
            ↓           ↓           ↓
     ┌──────────┐ ┌──────────┐ ┌──────────┐
     │ Agent A  │ │ Agent B  │ │ Agent C  │
     │(Research)│ │ (Code)   │ │ (Review) │
     └──────────┘ └──────────┘ └──────────┘
```

| Architecture | Description | Use Case |
|--------------|-------------|----------|
| **Supervisor** | One agent orchestrates others | Task delegation |
| **Hierarchical** | Multi-level management | Complex projects |
| **Peer-to-Peer** | Agents collaborate equally | Brainstorming |
| **Debate** | Agents argue positions | Decision making |
| **Pipeline** | Sequential handoffs | Workflow automation |

### 2. Communication Patterns

| Pattern | Description | Example |
|---------|-------------|---------|
| **Broadcast** | One-to-many | Supervisor assigns tasks |
| **Direct** | One-to-one | Agent requests help |
| **Blackboard** | Shared workspace | All agents read/write |
| **Message Queue** | Async messaging | Decoupled agents |

### 3. Agent Specialization

| Role | Responsibility | Skills |
|------|----------------|--------|
| **Planner** | Break down tasks | Strategic thinking |
| **Researcher** | Gather information | Web search, RAG |
| **Coder** | Write/edit code | Code generation |
| **Reviewer** | Quality check | Critique, testing |
| **Writer** | Create content | Language, style |

## Best Practices

### 1. Clear Role Definitions

```python
class AgentRole:
    def __init__(self, name: str, description: str, tools: list):
        self.name = name
        self.description = description
        self.tools = tools
        self.system_prompt = f"""
        You are {name}.
        {description}

        Your available tools: {[t.name for t in tools]}

        Focus on your specialty. Ask for help when needed.
        """

researcher = AgentRole(
    name="Research Specialist",
    description="Expert at finding and synthesizing information",
    tools=[web_search, document_reader, summarizer]
)
```

### 2. Structured Handoffs

```python
class TaskHandoff:
    from_agent: str
    to_agent: str
    task: str
    context: dict
    priority: int
    deadline: Optional[datetime]

# Clear handoff format
handoff = TaskHandoff(
    from_agent="planner",
    to_agent="researcher",
    task="Find statistics on AI adoption in healthcare",
    context={"project": "AI Report", "section": "Market Size"},
    priority=1,
    deadline=None
)
```

### 3. Conflict Resolution

```python
def resolve_conflict(opinions: list[AgentOpinion]) -> str:
    # If majority agrees
    if count_majority(opinions) > len(opinions) / 2:
        return majority_opinion(opinions)

    # Otherwise, escalate to senior agent
    return supervisor_decision(opinions)
```

## Common Patterns

### Pattern 1: Supervisor Agent

```python
from langgraph.graph import StateGraph, END

class TeamState(TypedDict):
    messages: list
    next_agent: str
    task_complete: bool

def supervisor_node(state: TeamState):
    """Supervisor decides which agent works next."""
    supervisor_prompt = """
    You are a team supervisor. Based on the conversation,
    decide which agent should work next:
    - researcher: For gathering information
    - coder: For writing/fixing code
    - reviewer: For checking quality
    - FINISH: If task is complete

    Current state: {state}

    Next agent:
    """

    response = llm.invoke(supervisor_prompt.format(state=state))
    return {"next_agent": response.content}

def researcher_node(state: TeamState):
    # Research agent does work
    pass

def coder_node(state: TeamState):
    # Coder agent does work
    pass

def reviewer_node(state: TeamState):
    # Reviewer agent does work
    pass

# Build workflow
workflow = StateGraph(TeamState)
workflow.add_node("supervisor", supervisor_node)
workflow.add_node("researcher", researcher_node)
workflow.add_node("coder", coder_node)
workflow.add_node("reviewer", reviewer_node)

# Supervisor routes to agents
workflow.add_conditional_edges(
    "supervisor",
    lambda s: s["next_agent"],
    {
        "researcher": "researcher",
        "coder": "coder",
        "reviewer": "reviewer",
        "FINISH": END
    }
)

# Agents return to supervisor
for agent in ["researcher", "coder", "reviewer"]:
    workflow.add_edge(agent, "supervisor")

workflow.set_entry_point("supervisor")
team = workflow.compile()
```

### Pattern 2: Hierarchical Team

```python
# Multi-level hierarchy
class HierarchicalTeam:
    def __init__(self):
        # Level 1: Executive (strategic)
        self.executive = Agent(
            name="Executive",
            role="Strategic decisions and final approval"
        )

        # Level 2: Managers (tactical)
        self.dev_manager = Agent(
            name="Dev Manager",
            role="Oversee development team"
        )
        self.research_manager = Agent(
            name="Research Manager",
            role="Oversee research team"
        )

        # Level 3: Workers (operational)
        self.developers = [
            Agent(name="Frontend Dev"),
            Agent(name="Backend Dev"),
            Agent(name="QA Engineer")
        ]
        self.researchers = [
            Agent(name="Data Analyst"),
            Agent(name="Market Researcher")
        ]

    def execute(self, task: str):
        # Top-down: Executive breaks down task
        plan = self.executive.plan(task)

        # Managers get sub-tasks
        dev_tasks = self.dev_manager.plan(plan.dev_requirements)
        research_tasks = self.research_manager.plan(plan.research_needs)

        # Workers execute
        dev_results = [d.execute(t) for d, t in zip(self.developers, dev_tasks)]
        research_results = [r.execute(t) for r, t in zip(self.researchers, research_tasks)]

        # Bottom-up: Aggregate results
        dev_summary = self.dev_manager.summarize(dev_results)
        research_summary = self.research_manager.summarize(research_results)

        # Final approval
        return self.executive.finalize(dev_summary, research_summary)
```

### Pattern 3: Debate System

```python
def debate_agents(topic: str, rounds: int = 3) -> str:
    """Two agents debate, third judges."""

    pro_agent = Agent(role="Argue in favor")
    con_agent = Agent(role="Argue against")
    judge = Agent(role="Evaluate arguments, decide winner")

    debate_history = []

    for round in range(rounds):
        # Pro argument
        pro_arg = pro_agent.respond(
            topic=topic,
            history=debate_history,
            instruction="Make your strongest argument"
        )
        debate_history.append(("PRO", pro_arg))

        # Con argument
        con_arg = con_agent.respond(
            topic=topic,
            history=debate_history,
            instruction="Counter the argument and present your case"
        )
        debate_history.append(("CON", con_arg))

    # Judge decides
    decision = judge.evaluate(
        topic=topic,
        debate=debate_history,
        instruction="Based on argument quality, which position is stronger?"
    )

    return decision
```

### Pattern 4: Critique and Revise

```python
def critique_and_revise(task: str, max_iterations: int = 3) -> str:
    """One agent creates, another critiques, first revises."""

    creator = Agent(role="Generate solution")
    critic = Agent(role="Find issues and suggest improvements")

    solution = creator.generate(task)

    for i in range(max_iterations):
        # Critic evaluates
        critique = critic.evaluate(
            solution=solution,
            instruction="Find weaknesses. Be specific and constructive."
        )

        # Check if good enough
        if critique.score >= 0.9:
            break

        # Revise based on feedback
        solution = creator.revise(
            current=solution,
            feedback=critique.feedback,
            instruction="Address all feedback points"
        )

    return solution
```

## Anti-patterns

| Anti-pattern | Problem | Solution |
|--------------|---------|----------|
| No clear roles | Agents duplicate work | Define distinct responsibilities |
| Infinite delegation | Tasks never complete | Set depth limits |
| No consensus mechanism | Conflicting outputs | Add voting/judge |
| Single point of failure | Supervisor bottleneck | Add redundancy |
| Overly complex hierarchies | Coordination overhead | Keep it simple |

## Design Checklist

### Architecture
- [ ] Agent roles clearly defined
- [ ] Communication pattern selected
- [ ] Hierarchy depth appropriate
- [ ] Handoff format standardized

### Coordination
- [ ] Supervisor logic implemented
- [ ] Conflict resolution defined
- [ ] Task routing clear
- [ ] Completion criteria set

### Reliability
- [ ] Agent failures handled
- [ ] Timeout mechanisms
- [ ] State recovery possible
- [ ] Logging comprehensive

### Performance
- [ ] Parallel execution where possible
- [ ] Minimal coordination overhead
- [ ] Resource limits per agent
- [ ] Cost monitoring enabled

## Tools & References

### Related Skills
- faion-langchain-skill
- faion-llamaindex-skill

### Related Agents
- faion-autonomous-agent-builder-agent

### External Resources
- [LangGraph Multi-Agent](https://langchain-ai.github.io/langgraph/tutorials/multi_agent/)
- [AutoGen Multi-Agent](https://microsoft.github.io/autogen/)
- [CrewAI Framework](https://www.crewai.com/)
- [Multi-Agent Debate Paper](https://arxiv.org/abs/2305.19118)

## Checklist

- [ ] Identified need for multi-agent system
- [ ] Selected appropriate architecture
- [ ] Defined agent roles and tools
- [ ] Implemented coordination logic
- [ ] Added conflict resolution
- [ ] Set up monitoring
- [ ] Tested with complex scenarios
- [ ] Documented agent interactions

---

*Methodology: M-LLM-004 | Category: LLM/Orchestration*
*Related: faion-autonomous-agent-builder-agent, faion-langchain-skill*
