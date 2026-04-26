# LLM Prompts for LangChain Development

Prompts for using LLMs to assist with LangChain/LangGraph development, debugging, and optimization.

---

## Table of Contents

1. [Chain Design Prompts](#chain-design-prompts)
2. [Agent Architecture Prompts](#agent-architecture-prompts)
3. [Debugging Prompts](#debugging-prompts)
4. [Optimization Prompts](#optimization-prompts)
5. [Code Review Prompts](#code-review-prompts)
6. [Migration Prompts](#migration-prompts)

---

## Chain Design Prompts

### Prompt 1: Design LCEL Chain from Requirements

```markdown
# LCEL Chain Design Assistant

I need to design a LangChain LCEL chain for the following use case:

## Requirements
[Describe what the chain should do]

## Input
- Input format: [JSON schema, text, etc.]
- Example input: [provide example]

## Expected Output
- Output format: [JSON schema, text, Pydantic model]
- Example output: [provide example]

## Constraints
- Model preferences: [gpt-4o-mini, claude-3, etc.]
- Latency requirements: [if any]
- Cost considerations: [if any]
- Error handling needs: [retry, fallback, etc.]

## Questions to Answer
1. What chain pattern best fits this use case? (sequential, router, parallel, map-reduce)
2. What components are needed? (prompts, parsers, retrievers)
3. How should errors be handled?
4. What's the recommended LCEL implementation?

Please provide:
1. Chain architecture diagram (text-based)
2. Complete LCEL implementation code
3. Example usage with test input
4. Potential edge cases to handle
```

### Prompt 2: Prompt Engineering for Chains

```markdown
# Prompt Engineering Assistant

I need to create an effective prompt for a LangChain chain.

## Chain Purpose
[Describe what the chain does]

## Current Prompt (if any)
```
[Current prompt text]
```

## Problems with Current Prompt
- [Issue 1]
- [Issue 2]

## Desired Behavior
- [Specific behavior 1]
- [Specific behavior 2]

## Output Requirements
- Format: [JSON, markdown, plain text]
- Structure: [Pydantic model if applicable]
- Constraints: [length, style, etc.]

Please provide:
1. Improved system prompt
2. User message template with variables
3. Few-shot examples if helpful
4. Output format instructions
5. Edge case handling in the prompt
```

### Prompt 3: RAG Chain Design

```markdown
# RAG Chain Design Assistant

I need to design a RAG (Retrieval Augmented Generation) chain.

## Document Corpus
- Type: [PDFs, web pages, code, etc.]
- Size: [number of documents, total size]
- Update frequency: [static, daily, real-time]

## Query Types
- [Type 1 example]
- [Type 2 example]

## Requirements
- Response format: [with sources, confidence, etc.]
- Retrieval accuracy priority: [precision vs recall]
- Latency constraints: [if any]

## Infrastructure
- Vector store preference: [Chroma, Pinecone, Qdrant, etc.]
- Embedding model: [OpenAI, Cohere, local]
- LLM for generation: [model name]

Please provide:
1. Chunking strategy recommendation
2. Retrieval strategy (basic, hybrid, reranking)
3. Complete RAG chain implementation
4. Evaluation approach for RAG quality
```

---

## Agent Architecture Prompts

### Prompt 4: Design Agent Architecture

```markdown
# Agent Architecture Design Assistant

I need to design a LangGraph agent for the following task:

## Task Description
[Describe the agent's purpose and goals]

## Available Tools/Capabilities
1. [Tool 1]: [description]
2. [Tool 2]: [description]
3. [Tool 3]: [description]

## Decision Making Requirements
- When to use each tool
- How to handle tool failures
- When to stop (success criteria)

## State Requirements
- What information needs to persist between steps
- What needs to be tracked (iterations, results, etc.)

## Constraints
- Maximum iterations: [number]
- Human-in-the-loop: [yes/no, when]
- Error budget: [how many failures allowed]

Please provide:
1. Agent architecture recommendation (ReAct, Plan-Execute, Supervisor, custom)
2. State schema (TypedDict)
3. Node definitions
4. Edge/routing logic
5. Complete LangGraph implementation
```

### Prompt 5: Multi-Agent System Design

```markdown
# Multi-Agent System Design Assistant

I need to design a multi-agent system with the following requirements:

## Agents Needed
1. [Agent 1]: [role and capabilities]
2. [Agent 2]: [role and capabilities]
3. [Agent 3]: [role and capabilities]

## Coordination Pattern
- [ ] Supervisor (one agent coordinates others)
- [ ] Peer-to-peer (agents communicate directly)
- [ ] Sequential (fixed order)
- [ ] Hierarchical (teams of teams)

## Communication Requirements
- How agents share information
- What information is passed between agents
- How conflicts are resolved

## Task Types
- [Example task 1]
- [Example task 2]

Please provide:
1. System architecture diagram
2. Agent role definitions
3. State schema for coordination
4. Routing/orchestration logic
5. Complete LangGraph implementation
6. Example execution trace
```

### Prompt 6: Tool Design for Agents

```markdown
# Agent Tool Design Assistant

I need to design tools for a LangGraph agent.

## Agent Purpose
[What the agent does]

## Required Capabilities
1. [Capability 1]
2. [Capability 2]
3. [Capability 3]

## External APIs/Services
- [Service 1]: [how it will be used]
- [Service 2]: [how it will be used]

## Tool Requirements
- Input validation needs
- Error handling approach
- Rate limiting considerations
- Authentication handling

Please provide:
1. Tool definitions with @tool decorator
2. Pydantic input schemas
3. Error handling implementation
4. Tool documentation (docstrings for LLM)
5. Test cases for each tool
```

---

## Debugging Prompts

### Prompt 7: Debug Chain Behavior

```markdown
# Chain Debugging Assistant

My LangChain chain is not working as expected.

## Chain Code
```python
[Paste your chain code here]
```

## Expected Behavior
[What should happen]

## Actual Behavior
[What is happening]

## Error Messages (if any)
```
[Error traceback]
```

## Sample Input
```python
[Input that causes the issue]
```

## Sample Output
```python
[Output received]
```

## LangSmith Trace (if available)
[Link or description of trace]

Please help me:
1. Identify the root cause
2. Explain why this is happening
3. Provide a fix
4. Suggest how to prevent similar issues
```

### Prompt 8: Debug Agent Loops

```markdown
# Agent Loop Debugging Assistant

My LangGraph agent is stuck in a loop or not terminating correctly.

## Agent Code
```python
[Paste agent implementation]
```

## Observed Behavior
- Number of iterations before timeout/stop: [number]
- Repeated actions: [yes/no, which ones]
- Tool call patterns: [describe]

## State at Loop Point
```python
[State values when loop detected]
```

## Expected Termination Condition
[When should the agent stop]

Please help me:
1. Identify why the agent is looping
2. Fix the termination condition
3. Add safeguards against infinite loops
4. Improve the agent's decision-making
```

### Prompt 9: Debug Tool Calling Issues

```markdown
# Tool Calling Debug Assistant

My agent is not calling tools correctly.

## Tool Definition
```python
[Tool code]
```

## Agent Setup
```python
[Agent configuration]
```

## Problem
- [ ] Tool not being called when it should
- [ ] Wrong tool being called
- [ ] Tool called with wrong arguments
- [ ] Tool results not being used correctly

## Example Interaction
User: [User message]
Expected tool call: [What should happen]
Actual behavior: [What happened]

## Model Used
[gpt-4o-mini, claude-3, etc.]

Please help me:
1. Diagnose the tool calling issue
2. Fix the tool definition or docstring
3. Improve the agent's tool selection
4. Add better error handling
```

---

## Optimization Prompts

### Prompt 10: Optimize Chain Latency

```markdown
# Chain Latency Optimization Assistant

My LangChain chain is too slow and I need to optimize it.

## Current Chain
```python
[Chain code]
```

## Current Performance
- Average latency: [X ms]
- P95 latency: [X ms]
- Bottleneck (if known): [component]

## Target Performance
- Target latency: [X ms]
- Acceptable tradeoffs: [quality, cost, etc.]

## Constraints
- Cannot change: [any fixed requirements]
- Must maintain: [any quality requirements]

Please provide:
1. Latency analysis of each component
2. Specific optimization recommendations
3. Parallelization opportunities
4. Caching strategies
5. Model selection recommendations
6. Optimized implementation
```

### Prompt 11: Optimize Token Usage and Cost

```markdown
# Cost Optimization Assistant

I need to reduce the token usage and cost of my LangChain application.

## Current Implementation
```python
[Code]
```

## Current Costs
- Tokens per request: [average]
- Cost per request: [$X.XX]
- Monthly volume: [requests]
- Current monthly cost: [$X]

## Budget
- Target cost per request: [$X.XX]
- Target monthly budget: [$X]

## Quality Requirements
- Minimum acceptable quality level: [describe]
- Critical features that cannot be degraded: [list]

Please provide:
1. Token usage analysis
2. Prompt optimization suggestions
3. Model tiering strategy
4. Caching opportunities
5. Context window management
6. Cost-optimized implementation
```

### Prompt 12: Optimize RAG Retrieval

```markdown
# RAG Retrieval Optimization Assistant

My RAG chain is not retrieving relevant documents effectively.

## Current Setup
- Vector store: [type]
- Embedding model: [model]
- Chunk size: [size]
- Retrieval k: [number]

## Problem Queries
1. Query: "[query]" - Expected: [doc], Got: [wrong docs]
2. Query: "[query]" - Expected: [doc], Got: [wrong docs]

## Metrics
- Current retrieval accuracy: [%]
- Target accuracy: [%]

## Constraints
- Latency budget: [ms]
- Cost constraints: [if any]

Please provide:
1. Analysis of retrieval issues
2. Chunking strategy improvements
3. Retrieval strategy recommendations (hybrid, reranking)
4. Query transformation suggestions
5. Optimized implementation
```

---

## Code Review Prompts

### Prompt 13: Review LangChain Code

```markdown
# LangChain Code Review Assistant

Please review my LangChain implementation for best practices.

## Code to Review
```python
[Paste code here]
```

## Context
- Purpose: [what the code does]
- Environment: [development/production]
- Scale: [expected load]

## Review Focus Areas
- [ ] Code structure and organization
- [ ] Error handling
- [ ] Performance
- [ ] Security
- [ ] Observability
- [ ] Testing approach
- [ ] Production readiness

Please provide:
1. Issues found (categorized by severity)
2. Best practice violations
3. Security concerns
4. Performance improvements
5. Refactored code with improvements
```

### Prompt 14: Security Review

```markdown
# LangChain Security Review Assistant

Please review my LangChain code for security vulnerabilities.

## Code
```python
[Code to review]
```

## Deployment Context
- Environment: [cloud, on-prem, etc.]
- Data sensitivity: [public, internal, confidential]
- User access: [authenticated, public]

## Security Concerns
- [ ] Prompt injection
- [ ] API key exposure
- [ ] Data leakage
- [ ] Output validation
- [ ] Tool execution safety

Please provide:
1. Security vulnerabilities found
2. Risk assessment for each
3. Remediation recommendations
4. Secure code patterns
5. Security testing suggestions
```

---

## Migration Prompts

### Prompt 15: Migrate Legacy LangChain Code

```markdown
# LangChain Migration Assistant

I need to migrate legacy LangChain code to modern patterns.

## Current Code (Legacy)
```python
[Old code using LLMChain, AgentExecutor, etc.]
```

## Current LangChain Version
[e.g., 0.1.x]

## Target Version
[e.g., 1.0+]

## Requirements
- Maintain same functionality
- Improve performance if possible
- Add better error handling

Please provide:
1. Mapping of old patterns to new patterns
2. Step-by-step migration guide
3. Migrated code using LCEL/LangGraph
4. Testing strategy to verify migration
5. Breaking changes to watch for
```

### Prompt 16: Migrate Agent to LangGraph

```markdown
# AgentExecutor to LangGraph Migration

I need to migrate from AgentExecutor to LangGraph.

## Current AgentExecutor Code
```python
[Current implementation]
```

## Agent Behavior
- Tools used: [list]
- Decision patterns: [describe]
- Memory/state: [if any]

## New Requirements
- Human-in-the-loop: [yes/no]
- Checkpointing: [yes/no]
- Custom control flow: [describe]

Please provide:
1. LangGraph state definition
2. Node implementations
3. Edge/routing logic
4. Complete migrated code
5. Feature comparison (old vs new)
6. Testing approach
```

---

## Prompt Templates for Common Tasks

### Quick Design Prompt

```markdown
Design a LangChain [chain/agent] that:
- Takes [input type] as input
- Does [action 1], [action 2], [action 3]
- Returns [output type]

Use [model] with [specific requirements].
Include error handling and [retry/fallback] logic.
```

### Quick Debug Prompt

```markdown
My LangChain [chain/agent] is [problem].

Code:
```python
[code]
```

Input: [input]
Expected: [expected]
Actual: [actual]

Why is this happening and how do I fix it?
```

### Quick Optimize Prompt

```markdown
Optimize this LangChain code for [latency/cost/accuracy]:

```python
[code]
```

Current performance: [metrics]
Target: [target metrics]
Constraints: [any constraints]
```

---

## Best Practices for LLM-Assisted Development

### When Using These Prompts

1. **Be Specific**: Include actual code, error messages, and examples
2. **Provide Context**: Explain the broader application and constraints
3. **Show Your Work**: Include what you've already tried
4. **Ask for Explanations**: Request reasoning, not just code
5. **Iterate**: Use follow-up prompts to refine solutions

### Prompt Structure Tips

```markdown
## Good Prompt Structure

1. Context/Background
   - What the system does
   - Current state/implementation

2. Specific Problem/Request
   - Clear, actionable ask
   - Success criteria

3. Constraints
   - Technical limitations
   - Requirements that must be met

4. Examples
   - Input/output examples
   - Edge cases to consider

5. Expected Output
   - Format of desired response
   - Level of detail needed
```

### Follow-Up Prompts

```markdown
# Clarification
"Can you explain why you chose [X] over [Y]?"

# Deeper Dive
"Show me how this handles [edge case]"

# Alternative
"What's another approach if [constraint] changes?"

# Simplification
"Can you simplify this while maintaining [requirement]?"

# Production Readiness
"What would need to change for production use?"
```

---

*LLM Prompts v2.0 - LangChain 1.0+ / LangGraph 1.0+*
