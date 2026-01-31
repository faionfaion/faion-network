---
id: multi-agent-basics
name: "Multi-Agent Systems Basics"
domain: ML
skill: faion-ml-engineer
category: "ml-engineering"
---

# Multi-Agent Systems Basics

## Overview

Multi-agent systems coordinate multiple specialized AI agents to solve complex problems collaboratively. By dividing tasks among experts and enabling communication, these systems can tackle challenges beyond single-agent capabilities.

## When to Use

- Complex tasks requiring diverse expertise
- Problems with natural role divisions
- Debate and verification scenarios
- Creative collaboration
- Simulation and role-playing
- When single agents struggle with scope

## Key Concepts

### Coordination Patterns

| Pattern | Description | Use Case |
|---------|-------------|----------|
| Sequential | Agents work in order | Pipelines, workflows |
| Parallel | Agents work simultaneously | Independent subtasks |
| Hierarchical | Manager delegates to workers | Complex projects |
| Debate | Agents argue positions | Verification, decisions |
| Collaborative | Agents work together | Creative tasks |

### Multi-Agent Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    ORCHESTRATOR                              │
│  - Task distribution                                         │
│  - Communication routing                                     │
│  - Conflict resolution                                       │
└─────────────────────────────────────────────────────────────┘
            │                    │                    │
    ┌───────▼───────┐   ┌───────▼───────┐   ┌───────▼───────┐
    │   AGENT A     │   │   AGENT B     │   │   AGENT C     │
    │  (Researcher) │   │  (Developer)  │   │  (Reviewer)   │
    └───────────────┘   └───────────────┘   └───────────────┘
```

## Basic Implementation

### Agent Foundation

```python
from dataclasses import dataclass
from typing import List, Dict, Optional
from openai import OpenAI
import json

client = OpenAI()

@dataclass
class AgentConfig:
    name: str
    role: str
    system_prompt: str
    model: str = "gpt-4o"
    tools: List[Dict] = None

class Agent:
    """Individual agent in a multi-agent system."""

    def __init__(self, config: AgentConfig):
        self.config = config
        self.messages: List[Dict] = []
        self.reset()

    def reset(self):
        """Reset agent state."""
        self.messages = [
            {"role": "system", "content": self.config.system_prompt}
        ]

    def respond(self, message: str, context: Dict = None) -> str:
        """Generate a response to a message."""
        user_content = message
        if context:
            user_content = f"Context: {json.dumps(context)}\n\n{message}"

        self.messages.append({"role": "user", "content": user_content})

        response = client.chat.completions.create(
            model=self.config.model,
            messages=self.messages,
            tools=self.config.tools
        )

        assistant_message = response.choices[0].message.content
        self.messages.append({"role": "assistant", "content": assistant_message})

        return assistant_message

class MultiAgentOrchestrator:
    """Orchestrates communication between agents."""

    def __init__(self, agents: List[Agent]):
        self.agents = {a.config.name: a for a in agents}
        self.conversation_history: List[Dict] = []

    def send_message(
        self,
        from_agent: str,
        to_agent: str,
        message: str,
        context: Dict = None
    ) -> str:
        """Send message from one agent to another."""
        if to_agent not in self.agents:
            raise ValueError(f"Unknown agent: {to_agent}")

        prefixed_message = f"[From {from_agent}]: {message}"

        response = self.agents[to_agent].respond(prefixed_message, context)

        self.conversation_history.append({
            "from": from_agent,
            "to": to_agent,
            "message": message,
            "response": response
        })

        return response

    def broadcast(self, message: str, exclude: List[str] = None) -> Dict[str, str]:
        """Broadcast message to all agents."""
        exclude = exclude or []
        responses = {}

        for name, agent in self.agents.items():
            if name not in exclude:
                responses[name] = agent.respond(message)

        return responses

    def get_summary(self) -> str:
        """Get summary of conversation."""
        summary = "Conversation Summary:\n"
        for entry in self.conversation_history:
            summary += f"\n{entry['from']} -> {entry['to']}:\n"
            summary += f"  Message: {entry['message'][:100]}...\n"
            summary += f"  Response: {entry['response'][:100]}...\n"
        return summary
```

### Sequential Pipeline

```python
class SequentialPipeline:
    """Agents process tasks in sequence."""

    def __init__(self, agents: List[Agent]):
        self.agents = agents

    def run(self, initial_input: str) -> Dict:
        """Run the pipeline."""
        current_output = initial_input
        results = []

        for agent in self.agents:
            response = agent.respond(current_output)
            results.append({
                "agent": agent.config.name,
                "input": current_output[:200],
                "output": response
            })
            current_output = response

        return {
            "final_output": current_output,
            "pipeline_results": results
        }

# Example: Research -> Write -> Edit pipeline
researcher = Agent(AgentConfig(
    name="Researcher",
    role="Research Specialist",
    system_prompt="You are a research specialist. Gather and summarize relevant information."
))

writer = Agent(AgentConfig(
    name="Writer",
    role="Content Writer",
    system_prompt="You are a content writer. Create engaging content from research findings."
))

editor = Agent(AgentConfig(
    name="Editor",
    role="Editor",
    system_prompt="You are an editor. Improve clarity, fix errors, and polish the content."
))

pipeline = SequentialPipeline([researcher, writer, editor])
result = pipeline.run("Write an article about AI agents")
```

### Debate System

```python
class DebateSystem:
    """Two agents debate a topic to reach better conclusions."""

    def __init__(
        self,
        proponent: Agent,
        opponent: Agent,
        judge: Agent,
        max_rounds: int = 3
    ):
        self.proponent = proponent
        self.opponent = opponent
        self.judge = judge
        self.max_rounds = max_rounds

    def debate(self, topic: str) -> Dict:
        """Run a debate on the topic."""
        debate_history = []

        # Initial positions
        pro_position = self.proponent.respond(
            f"Argue IN FAVOR of: {topic}\nProvide your strongest arguments."
        )
        con_position = self.opponent.respond(
            f"Argue AGAINST: {topic}\nProvide your strongest arguments."
        )

        debate_history.append({
            "round": 0,
            "proponent": pro_position,
            "opponent": con_position
        })

        # Debate rounds
        for round_num in range(1, self.max_rounds + 1):
            # Opponent responds to proponent
            con_response = self.opponent.respond(
                f"Counter the following argument:\n{pro_position}"
            )

            # Proponent responds to opponent
            pro_response = self.proponent.respond(
                f"Defend against and counter:\n{con_response}"
            )

            debate_history.append({
                "round": round_num,
                "proponent": pro_response,
                "opponent": con_response
            })

            pro_position = pro_response

        # Judge evaluates
        debate_summary = json.dumps(debate_history, indent=2)
        judgment = self.judge.respond(
            f"""Evaluate this debate and determine the stronger position.

Topic: {topic}

Debate:
{debate_summary}

Provide:
1. Summary of key arguments
2. Strengths and weaknesses of each side
3. Your judgment on which side argued more effectively
4. A synthesized conclusion incorporating the best points"""
        )

        return {
            "topic": topic,
            "debate_history": debate_history,
            "judgment": judgment
        }

# Example
debate = DebateSystem(
    proponent=Agent(AgentConfig(
        name="Proponent",
        role="Advocate",
        system_prompt="You are a skilled debater arguing in favor of positions. Be persuasive and logical."
    )),
    opponent=Agent(AgentConfig(
        name="Opponent",
        role="Critic",
        system_prompt="You are a skilled debater arguing against positions. Find weaknesses and counter-arguments."
    )),
    judge=Agent(AgentConfig(
        name="Judge",
        role="Impartial Judge",
        system_prompt="You are an impartial judge. Evaluate arguments fairly and provide balanced conclusions."
    ))
)

result = debate.debate("AI will create more jobs than it eliminates")
```

## Best Practices

1. **Agent Specialization**
   - Clear, focused roles
   - Non-overlapping responsibilities
   - Appropriate expertise levels

2. **Communication Design**
   - Clear message protocols
   - Structured information exchange
   - Conflict resolution mechanisms

3. **Coordination**
   - Choose appropriate pattern for task
   - Minimize unnecessary communication
   - Handle failures gracefully

4. **Monitoring**
   - Log all inter-agent messages
   - Track individual agent performance
   - Monitor for deadlocks

5. **Testing**
   - Test agents individually
   - Test coordination logic
   - Simulate edge cases

## Common Pitfalls

1. **Role Confusion** - Overlapping agent responsibilities
2. **Communication Overhead** - Too much back-and-forth
3. **Deadlocks** - Agents waiting on each other
4. **Echo Chambers** - Agents reinforcing mistakes
5. **Coordination Failure** - No clear decision making
6. **Resource Waste** - Redundant agent work

## References

- [AutoGen](https://microsoft.github.io/autogen/)
- [CrewAI](https://github.com/joaomdmoura/crewAI)
- [MetaGPT](https://github.com/geekan/MetaGPT)
- [Multi-Agent Survey](https://arxiv.org/abs/2308.08155)
