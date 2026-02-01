---
id: ai-agent-patterns
name: "AI Agent Patterns"
domain: ML
skill: faion-ml-engineer
category: "best-practices-2026"
version: "2.0.0"
---

# AI Agent Design Patterns

Comprehensive guide to agentic AI design patterns for building intelligent, autonomous systems.

## Overview

Simple prompt-response workflows are insufficient for complex, multi-step tasks. Agent design patterns provide structured approaches for reasoning, planning, tool use, and self-improvement.

## Core Patterns

| Pattern | Description | Best For |
|---------|-------------|----------|
| [ReAct](#react-reasoning--acting) | Thought-Action-Observation loop | Dynamic tasks requiring adaptation |
| [Chain-of-Thought](#chain-of-thought-cot) | Step-by-step reasoning | Complex reasoning, math, logic |
| [Tool Use](#tool-use) | External capability invocation | Real-world data, API access |
| [Plan-Execute](#plan-execute) | Upfront planning + execution | Multi-step workflows |
| [Reflection](#reflection) | Self-critique and revision | Quality-critical outputs |
| [Tree-of-Thoughts](#tree-of-thoughts-tot) | Multi-path exploration | Creative/puzzle tasks |

## Pattern Selection Guide

```
Task Analysis
├── Simple, single-step?
│   └── Direct prompting (no agent needed)
│
├── Requires external data/actions?
│   └── Tool Use pattern
│
├── Complex reasoning needed?
│   ├── Single path sufficient → Chain-of-Thought
│   └── Multiple paths to explore → Tree-of-Thoughts
│
├── Dynamic, adaptive workflow?
│   └── ReAct pattern
│
├── Multi-step with dependencies?
│   └── Plan-Execute pattern
│
├── Quality-critical output?
│   └── Add Reflection layer
│
└── Multiple specialized capabilities?
    └── Multi-Agent pattern
```

## ReAct (Reasoning + Acting)

Introduced by Yao et al. (2023), ReAct synergizes reasoning and acting in language models.

**Loop Structure:**
```
Thought → Action → Observation → (repeat until done)
```

**When to Use:**
- Tasks requiring dynamic adaptation
- Complex information retrieval
- Multi-step problem solving
- When actions depend on intermediate results

**Trade-offs:**
- Higher latency (multiple model calls)
- Increased token consumption
- Better accuracy for complex tasks

## Chain-of-Thought (CoT)

Explicit step-by-step reasoning that shows intermediate work.

**Variants:**
| Variant | Approach |
|---------|----------|
| Zero-shot CoT | "Let's think step by step..." |
| Few-shot CoT | Examples with reasoning traces |
| Self-consistency | Multiple paths, majority vote |

**When to Use:**
- Mathematical reasoning
- Logical deduction
- Multi-step problem solving
- Explanation generation

## Tool Use

Bridge between reasoning and reality through external capabilities.

**Tool Categories:**
| Category | Examples |
|----------|----------|
| Information | Web search, database queries |
| Computation | Calculators, code execution |
| Integration | APIs, file systems |
| Communication | Email, messaging |

**When to Use:**
- Current information needed
- Precise calculations required
- External system interaction
- Beyond training data scope

## Plan-Execute

Separate planning from execution for complex workflows.

**Structure:**
```
1. Planner creates task decomposition
2. Executor handles each subtask
3. Verifier checks results
4. Replanner adjusts if needed
```

**When to Use:**
- Multi-phase projects
- Resource constraints exist
- Dependencies between steps
- Parallel execution possible

**Optimization:** Use larger model for planning, smaller for execution.

## Reflection

Self-evaluation layer for output improvement.

**Critique Dimensions:**
- Accuracy verification
- Constraint adherence
- Logical consistency
- Quality standards

**When to Use:**
- High-stakes outputs
- Quality-critical content
- Code generation
- Complex document creation

**Trade-offs:**
- Each cycle increases latency
- Additional token consumption
- Requires clear exit conditions

## Tree-of-Thoughts (ToT)

Explores multiple reasoning branches simultaneously.

**When to Use:**
- Creative ideation
- Puzzle-like problems
- Strategic planning
- When single path may fail

## Multi-Agent Patterns

| Pattern | Description | Complexity |
|---------|-------------|------------|
| Sequential | Linear agent chain | Low |
| Parallel | Concurrent execution | Medium |
| Coordinator | Central routing agent | Medium |
| Hierarchical | Multi-level decomposition | High |
| Swarm | All-to-all collaboration | Highest |

## Frameworks

| Framework | Strengths | Use Case |
|-----------|-----------|----------|
| LangGraph | State machines, complex flows | Production agents |
| AutoGen | Multi-agent conversations | Collaborative agents |
| CrewAI | Role-based teams | Specialized agents |
| OpenAI Agents SDK | Native OpenAI support | OpenAI-first projects |
| LlamaIndex | RAG-focused agents | Knowledge-heavy tasks |

## Best Practices (2026)

1. **Start Simple:** Single agent with ReAct handles most tasks
2. **Add Complexity Gradually:** Only when hitting clear limitations
3. **Combine Patterns:** Tool use + Reflection + Planning work together
4. **Design for Observability:** Log thoughts, actions, decisions
5. **Set Exit Conditions:** Prevent infinite loops in iterative patterns
6. **Cost Awareness:** Track token usage across agent calls

## Files in This Folder

| File | Purpose |
|------|---------|
| [README.md](README.md) | Overview and pattern summaries |
| [checklist.md](checklist.md) | Implementation checklists |
| [examples.md](examples.md) | Code examples for each pattern |
| [templates.md](templates.md) | Reusable prompt templates |
| [llm-prompts.md](llm-prompts.md) | LLM prompts for agent creation |


## Agent Selection

| Task | Model | Rationale |
|------|-------|----------|
| Agent loop design | sonnet | Pattern expertise |
| Agent state management | sonnet | State design |
| Error handling in agents | sonnet | Robustness |

## Sources

- [Google Cloud: Choose a design pattern for agentic AI](https://docs.cloud.google.com/architecture/choose-design-pattern-agentic-ai-system)
- [ByteByteGo: Top AI Agentic Workflow Patterns](https://blog.bytebytego.com/p/top-ai-agentic-workflow-patterns)
- [IBM: What is a ReAct Agent?](https://www.ibm.com/think/topics/react-agent)
- [Agentic Design Patterns Reference](https://medium.com/@random.droid/agentic-design-pattern-quick-reference-d4d434972069)
- [Skywork: 20 Agentic AI Workflow Patterns](https://skywork.ai/blog/agentic-ai-examples-workflow-patterns-2025/)
