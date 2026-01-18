# M-LLM-002: LLM Chain Patterns

## Overview

LLM chains connect multiple LLM calls in sequence, where each step's output feeds the next step's input. This enables complex workflows that single prompts cannot achieve. Patterns include sequential chains, router chains, and MapReduce chains.

**When to use:** Tasks requiring multiple reasoning steps, dynamic routing, or processing multiple documents.

## Core Concepts

### 1. Chain Types

| Type | Description | Use Case |
|------|-------------|----------|
| **Sequential** | Steps run in order | Multi-step analysis |
| **Router** | Dynamic path selection | Intent classification |
| **MapReduce** | Parallel then aggregate | Document summarization |
| **Branching** | Conditional paths | Decision trees |
| **Reflexion** | Self-correction loops | Quality improvement |

### 2. Chain Components

```
Input → Preprocessor → LLM Call 1 → Parser → LLM Call 2 → Output
          ↓               ↓            ↓           ↓
       Validate        Format       Extract     Format
```

### 3. State Management

Chains maintain state between steps:
- **Accumulated context** - Previous outputs available
- **Variables** - Extracted values passed forward
- **Memory** - Conversation history (if needed)

## Best Practices

### 1. Design for Failure

Each chain step should:
- Validate input before processing
- Handle parsing errors gracefully
- Have fallback behavior
- Log intermediate results

### 2. Minimize Chain Length

```
# Bad: 5-step chain for simple task
Input → Extract → Validate → Transform → Format → Output

# Good: 2-step chain with clear purpose
Input → Analyze + Extract → Format + Validate → Output
```

### 3. Use Typed Outputs

```python
from pydantic import BaseModel

class AnalysisResult(BaseModel):
    sentiment: str
    confidence: float
    topics: list[str]

# Chain step outputs structured data
```

## Common Patterns

### Pattern 1: Sequential Chain

```python
# LangChain example
from langchain.chains import SequentialChain
from langchain.prompts import PromptTemplate

# Step 1: Analyze
analyze_prompt = PromptTemplate(
    input_variables=["text"],
    template="Analyze this text for key themes: {text}"
)

# Step 2: Summarize based on analysis
summarize_prompt = PromptTemplate(
    input_variables=["analysis"],
    template="Create a summary focusing on: {analysis}"
)

# Chain them
chain = SequentialChain(
    chains=[analyze_chain, summarize_chain],
    input_variables=["text"],
    output_variables=["summary"]
)
```

### Pattern 2: Router Chain

```python
# Route to specialized handlers
from langchain.chains.router import MultiPromptChain

# Define routes
routes = {
    "technical": technical_chain,
    "business": business_chain,
    "creative": creative_chain
}

# Router prompt
router_prompt = """
Classify this request into one category:
- technical: Code, debugging, architecture
- business: Strategy, pricing, marketing
- creative: Writing, design, brainstorming

Request: {input}
Category:"""

# Dynamic routing based on classification
router_chain = MultiPromptChain.from_prompts(
    llm=llm,
    prompt_infos=routes,
    default_chain=general_chain
)
```

### Pattern 3: MapReduce Chain

```python
# Process multiple documents, then combine
from langchain.chains import MapReduceDocumentsChain

# Map: Process each document independently
map_prompt = PromptTemplate(
    template="Summarize this document in 3 bullet points:\n{doc}"
)

# Reduce: Combine all summaries
reduce_prompt = PromptTemplate(
    template="Combine these summaries into one coherent summary:\n{summaries}"
)

chain = MapReduceDocumentsChain(
    llm_chain=map_chain,
    combine_document_chain=reduce_chain
)

# Process 100 documents in parallel, then combine
result = chain.run(documents)
```

### Pattern 4: Branching Chain

```python
# Conditional execution based on previous output
def branching_chain(input_data):
    # Step 1: Classify
    classification = classify_chain.run(input_data)

    # Step 2: Branch based on classification
    if classification == "urgent":
        return urgent_handler.run(input_data)
    elif classification == "routine":
        return routine_handler.run(input_data)
    else:
        return escalation_handler.run(input_data)
```

### Pattern 5: Reflexion Chain

```python
# Self-improvement loop
def reflexion_chain(input_data, max_iterations=3):
    result = initial_chain.run(input_data)

    for i in range(max_iterations):
        # Evaluate quality
        evaluation = evaluate_chain.run(result)

        if evaluation["score"] >= 0.9:
            break

        # Improve based on feedback
        result = improve_chain.run({
            "original": result,
            "feedback": evaluation["feedback"]
        })

    return result
```

## Anti-patterns

| Anti-pattern | Problem | Solution |
|--------------|---------|----------|
| Monolithic chains | Hard to debug, maintain | Break into reusable components |
| No intermediate validation | Errors propagate | Validate at each step |
| Ignoring token limits | Truncated context | Summarize long contexts |
| Synchronous MapReduce | Slow for many docs | Use async/parallel processing |
| No caching | Redundant API calls | Cache intermediate results |

## Chain Design Checklist

### Architecture
- [ ] Each step has single responsibility
- [ ] Outputs are typed and validated
- [ ] Error handling at each step
- [ ] Reasonable chain length (2-4 steps typical)

### Performance
- [ ] Parallel processing where possible
- [ ] Caching for repeated inputs
- [ ] Token budgets per step
- [ ] Timeout handling

### Debugging
- [ ] Intermediate outputs logged
- [ ] Clear step naming
- [ ] Metrics collection
- [ ] Replay capability

## Tools & References

### Related Skills
- faion-langchain-skill
- faion-llamaindex-skill

### Related Agents
- faion-autonomous-agent-builder-agent
- faion-prompt-engineer-agent

### External Resources
- [LangChain Chains](https://python.langchain.com/docs/concepts/chains/)
- [LlamaIndex Pipelines](https://docs.llamaindex.ai/en/stable/module_guides/querying/pipeline/)
- [LangGraph for Complex Chains](https://langchain-ai.github.io/langgraph/)

## Checklist

- [ ] Identified chain type needed
- [ ] Designed step-by-step flow
- [ ] Defined input/output schemas
- [ ] Added validation between steps
- [ ] Implemented error handling
- [ ] Set up logging/monitoring
- [ ] Tested with edge cases
- [ ] Optimized for performance

---

*Methodology: M-LLM-002 | Category: LLM/Orchestration*
*Related: faion-langchain-skill, faion-llamaindex-skill*
