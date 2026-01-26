# Multi-Agent Design Patterns

> **Entry point:** `/faion-net` — invoke for automatic routing.

Design patterns for orchestrating multiple AI agents in production systems.

## Overview

Single all-purpose agents cannot handle complex enterprise workflows efficiently. Multi-agent systems (MAS) apply the microservices principle to AI: specialized agents collaborate through defined communication patterns.

**Enterprise Adoption (2025-2026):**
- Gartner: 1,445% surge in multi-agent inquiries (Q1 2024 → Q2 2025)
- Prediction: 40% of enterprise apps include AI agents by 2026
- IDC: 80% of workplace apps will have AI copilots by 2026

## Core Patterns

| Pattern | Type | Use Case |
|---------|------|----------|
| [Supervisor](#supervisor-pattern) | Centralized | Request routing, orchestration |
| [Hierarchical](#hierarchical-pattern) | Multi-level | Complex goal decomposition |
| [Sequential](#sequential-pattern) | Pipeline | Linear workflows, data processing |
| [Peer-to-Peer](#peer-to-peer-pattern) | Decentralized | Resilient, adaptive systems |

## Supervisor Pattern

**Description:** A central coordinator agent routes requests to specialized worker agents based on task type. The supervisor uses LLM reasoning to decide delegation.

**Architecture:**
```
User Query
    ↓
┌─────────────┐
│  Supervisor │  ← LLM-driven routing
└─────────────┘
    ↓     ↓     ↓
┌─────┐ ┌─────┐ ┌─────┐
│ A1  │ │ A2  │ │ A3  │  ← Specialized workers
└─────┘ └─────┘ └─────┘
```

**When to Use:**
- Multi-domain systems (help desks, customer service)
- Intelligent request routing needed
- Workers have distinct, non-overlapping expertise
- Need centralized control and monitoring

**Key Characteristics:**
- Single point of coordination
- LLM-driven or rule-based routing
- Workers are specialized agents with distinct tools
- Supervisor aggregates worker outputs

**Advantages:**
- Clear responsibility separation
- Easy to add new workers
- Centralized logging and monitoring
- Predictable control flow

**Disadvantages:**
- Single point of failure
- Supervisor can become bottleneck
- Requires good task classification

**Framework Support:**
| Framework | Implementation |
|-----------|----------------|
| LangGraph | `StateGraph` with supervisor node |
| CrewAI | Manager agent with crew |
| AutoGen | `GroupChat` with speaker selection |
| Google ADK | `transfer_to_agent()` mechanism |

## Hierarchical Pattern

**Description:** Multi-level agent tree where higher-level agents decompose complex goals into sub-tasks delegated to lower-level agents. Results propagate back up the hierarchy.

**Architecture:**
```
┌─────────────────┐
│  Top Supervisor │  ← Strategic planning
└─────────────────┘
    ↓           ↓
┌────────┐  ┌────────┐
│ Mid-1  │  │ Mid-2  │  ← Tactical coordination
└────────┘  └────────┘
  ↓    ↓      ↓    ↓
┌──┐ ┌──┐  ┌──┐ ┌──┐
│W1│ │W2│  │W3│ │W4│  ← Task execution
└──┘ └──┘  └──┘ └──┘
```

**When to Use:**
- Complex problems requiring recursive breakdown
- Large cross-functional domains
- Need for task isolation and specialization
- Enterprise workflows with multiple departments

**Key Characteristics:**
- Multi-level parent/sub-agent structure
- Decisions cascade down, results bubble up
- Each level abstracts complexity for level above
- Can combine with other patterns at each level

**Advantages:**
- Scales to complex workflows
- Highly modular
- Natural for organizational structures
- Supports team specialization

**Disadvantages:**
- Complex orchestration
- Harder to debug across levels
- Coordination overhead between levels
- "Middle management" latency problem

**Real-World Example:**
```
Report Generator (Top)
├── Research Team (Mid)
│   ├── Web Searcher (Worker)
│   └── Data Analyst (Worker)
└── Writing Team (Mid)
    ├── Draft Writer (Worker)
    └── Editor (Worker)
```

## Sequential Pattern

**Description:** Assembly-line pipeline where agents execute in fixed order. Each agent's output feeds the next agent's input through shared state.

**Architecture:**
```
Input → [Agent A] → [Agent B] → [Agent C] → Output
           ↓            ↓            ↓
        state[a]     state[b]     state[c]
```

**When to Use:**
- Linear workflows with clear stages
- Data processing pipelines
- Document transformation chains
- Validation → Processing → Reporting workflows

**Key Characteristics:**
- Fixed execution order
- State passed via shared session
- Each agent has `output_key` for state writing
- Deterministic and easy to debug

**Advantages:**
- Simple to understand and implement
- Easy to debug (clear data lineage)
- Predictable execution
- Good for ETL-like workflows

**Disadvantages:**
- No parallelism (slower for independent tasks)
- Single failure stops pipeline
- Limited flexibility for dynamic workflows

**Example Pipeline:**
```
Document Processing:
Parser → Extractor → Summarizer → Formatter

Code Review:
Linter → Security Scanner → Style Checker → Report Generator
```

**Framework Support:**
| Framework | Implementation |
|-----------|----------------|
| Google ADK | `SequentialAgent` |
| LangGraph | Linear graph edges |
| CrewAI | Sequential process |

## Peer-to-Peer Pattern

**Description:** Decentralized architecture where agents communicate directly without central orchestrator. Each agent has routing strategy and can evolve independently.

**Architecture:**
```
┌─────┐ ←→ ┌─────┐
│ A1  │    │ A2  │
└─────┘ ↘  └─────┘
    ↕    ↘   ↕
┌─────┐ ←→ ┌─────┐
│ A3  │    │ A4  │
└─────┘    └─────┘
```

**When to Use:**
- Resilience is critical (no single point of failure)
- Cross-organizational collaboration
- Privacy-preserving systems
- Adaptive, evolving agent networks

**Key Characteristics:**
- No central coordinator
- Dynamic agent discovery
- Local routing decisions
- Can form DAG (Directed Acyclic Graph) structures

**Advantages:**
- High resilience and fault tolerance
- Scales horizontally
- Privacy-preserving (no central data collection)
- Agents can specialize independently

**Disadvantages:**
- Complex coordination mechanisms needed
- Harder to monitor globally
- Potential for circular dependencies
- Consensus overhead

**Notable Implementation: AgentNet (NeurIPS 2025)**
- Decentralized DAG structure
- RAG-enhanced memory per agent
- Dynamic task routing
- Agent evolution capability

## Pattern Comparison

| Aspect | Supervisor | Hierarchical | Sequential | Peer-to-Peer |
|--------|------------|--------------|------------|--------------|
| Control | Centralized | Multi-level | Linear | Distributed |
| Complexity | Low-Medium | High | Low | High |
| Scalability | Medium | High | Low | Very High |
| Fault Tolerance | Low | Medium | Low | High |
| Debugging | Easy | Hard | Very Easy | Hard |
| Latency | Medium | High | Predictable | Variable |
| Best For | Routing | Decomposition | Pipelines | Resilience |

## Hybrid Patterns

Real-world systems often combine patterns:

**Hierarchical + Sequential:**
```
Supervisor
├── Team A (Sequential)
│   └── A1 → A2 → A3
└── Team B (Sequential)
    └── B1 → B2
```

**Supervisor + Parallel:**
```
Supervisor
├── [Parallel Workers]
│   ├── W1 (concurrent)
│   ├── W2 (concurrent)
│   └── W3 (concurrent)
└── Aggregator
```

## Additional Patterns

### Parallel Fan-Out/Gather
Spawn parallel agents for concurrent execution, then synthesize results.

### Generator-Critic
One agent creates content, another validates/critiques it.

### Loop (Iterative Refinement)
Repeated improvement cycles until criteria met.

### Human-in-the-Loop
Checkpoints for human approval in high-stakes decisions.

### Router
Dynamic agent selection based on input classification.

### Blackboard
Shared workspace for collaborative knowledge synthesis.

## Framework Comparison (2026)

| Framework | Patterns | Strengths | Complexity |
|-----------|----------|-----------|------------|
| LangGraph | All | State machines, graph-based | Medium-High |
| CrewAI | Supervisor, Sequential | Role-based teams | Low |
| AutoGen | Supervisor, P2P | Multi-agent conversations | Medium |
| Google ADK | All | Native primitives | Medium |
| AgentNet | P2P | Decentralized, evolving | High |

## Files in This Directory

| File | Purpose |
|------|---------|
| [checklist.md](checklist.md) | Implementation checklists per pattern |
| [examples.md](examples.md) | Code examples for each pattern |
| [templates.md](templates.md) | Reusable templates and scaffolds |
| [llm-prompts.md](llm-prompts.md) | Prompts for agent roles |

## Sources

- [Google ADK Multi-Agent Documentation](https://google.github.io/adk-docs/agents/multi-agents/)
- [Databricks Agent System Design Patterns](https://docs.databricks.com/aws/en/generative-ai/guide/agent-system-design-patterns)
- [LangGraph Hierarchical Agent Teams](https://langchain-ai.github.io/langgraph/tutorials/multi_agent/hierarchical_agent_teams/)
- [AgentNet: Decentralized Multi-Agent Systems (NeurIPS 2025)](https://arxiv.org/abs/2504.00587)
- [Multi-Agent Collaboration Mechanisms Survey](https://arxiv.org/html/2501.06322v1)

## Related

- [faion-ai-agents](../../faion-ai-agents/CLAUDE.md) - Agent frameworks (LangChain, MCP)
- [faion-llm-integration](../../faion-llm-integration/CLAUDE.md) - LLM API integration
