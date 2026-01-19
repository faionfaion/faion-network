# AI/ML Best Practices 2026

## M-ML-025: Agentic RAG (RAG 2.0)

### Problem

Traditional RAG: single retrieval, no verification, limited reasoning.

### Solution: Agentic RAG

**Key Differences:**

| Traditional RAG | Agentic RAG |
|-----------------|-------------|
| Single retrieval | Multi-hop retrieval |
| Fixed pipeline | Dynamic reasoning |
| No self-correction | Iterative refinement |
| Context stuffing | Selective retrieval |

**Agentic RAG Loop:**
```
Query → Think → Retrieve → Evaluate sufficiency
                              ↓
                    Insufficient? → Re-query/Different source
                              ↓
                    Sufficient → Generate answer → Verify → Output
```

**Implementation:**
```python
# Agentic RAG pattern
class AgenticRAG:
    def answer(self, query):
        context = []
        for attempt in range(max_attempts):
            retrieved = self.retrieve(query, context)
            context.extend(retrieved)

            if self.is_sufficient(query, context):
                break

            query = self.refine_query(query, context)

        answer = self.generate(query, context)
        return self.verify(answer, context)
```

**Use Cases:**
- Complex multi-step questions
- Research synthesis
- Compliance verification
- Multi-source fact-checking

---

## M-ML-026: AI Agent Patterns

### Problem

Simple prompt→response insufficient for complex tasks.

### Solution: Agent Design Patterns

**1. Chain of Thought (CoT)**
```
Prompt: "Let's think step by step..."
Output: Reasoning → Intermediate steps → Final answer
```

**2. ReAct (Reason + Act)**
```
Thought: What do I need to find out?
Action: search(query)
Observation: [search results]
Thought: Now I know X, but need Y
Action: lookup(Y)
...
Answer: [final response]
```

**3. Plan-and-Execute**
```
1. Create plan with subtasks
2. Execute each subtask
3. Verify results
4. Adjust plan if needed
5. Synthesize final output
```

**4. Tool Use Pattern**
```python
tools = [
    {"name": "search", "description": "Search the web"},
    {"name": "calculate", "description": "Math operations"},
    {"name": "code_exec", "description": "Run Python code"}
]

# Agent decides which tool to use based on task
```

**Frameworks:**
| Framework | Strengths |
|-----------|-----------|
| LangGraph | State machines, complex flows |
| AutoGen | Multi-agent conversations |
| CrewAI | Role-based agent teams |
| OpenAI Agents SDK | Official OpenAI support |

---

## M-ML-027: LLM Management & Observability

### Problem

No visibility into LLM cost, quality, and reliability.

### Solution: LLMOps Platform

**Key Metrics:**

| Category | Metrics |
|----------|---------|
| Cost | Tokens/request, cost/conversation, budget tracking |
| Quality | Response relevance, hallucination rate, user satisfaction |
| Performance | Latency (P50, P95, P99), throughput |
| Reliability | Error rate, retry rate, fallback frequency |

**Observability Stack:**
```
Application → Tracing (Langfuse/Helicone) → Dashboard
                    ↓
              Prompt Registry → Version Control
                    ↓
              Evaluation Suite → Quality Gates
```

**Tools:**
| Tool | Focus |
|------|-------|
| Langfuse | Open-source tracing, prompts |
| Helicone | Cost analytics, caching |
| Weights & Biases | Experiment tracking |
| Arize Phoenix | Evaluation, embeddings |
| Portkey | Gateway, fallbacks |

**Best Practices:**
- Track every LLM call
- Version control prompts
- Set up cost alerts
- A/B test prompt changes
- Monitor for drift

---

## M-ML-028: Decision Framework

### Problem

When to use prompting vs RAG vs fine-tuning?

### Solution: Progressive Enhancement

```
Start: Prompt Engineering (hours/days, $0)
         ↓
Need external data? → RAG ($70-1000/month)
         ↓
Need specialized behavior? → Fine-tuning (months, 6x inference cost)
```

**Decision Matrix:**

| Need | Solution |
|------|----------|
| Better instructions | Prompt engineering |
| Real-time/private data | RAG |
| Specific output format | Structured output |
| Domain expertise | Fine-tuning |
| Cost reduction | Smaller model + fine-tuning |

**Cost Comparison:**

| Approach | Setup Cost | Ongoing Cost | Time to Deploy |
|----------|------------|--------------|----------------|
| Prompting | Low | Per-token | Hours |
| RAG | Medium | Infrastructure + tokens | Days-weeks |
| Fine-tuning | High | Higher per-token | Weeks-months |

---

## M-ML-029: MCP (Model Context Protocol)

### Problem

No standard way to connect LLMs to external tools/data.

### Solution: Model Context Protocol

**What is MCP?**
- Open protocol for LLM-tool communication
- Standardized tool definitions
- Secure context sharing
- Developed by Anthropic

**Components:**
```
MCP Server (tools/data) ←→ MCP Client (Claude Code, etc.)
                              ↓
                           LLM Request
```

**Example MCP Server:**
```json
{
  "name": "database",
  "description": "Query company database",
  "input_schema": {
    "type": "object",
    "properties": {
      "query": {"type": "string"}
    }
  }
}
```

**Benefits:**
- Reusable tool definitions
- Security through protocol
- Composable capabilities
- Standard across clients

---

## M-ML-030: AI Governance & Compliance

### Problem

EU AI Act and regulations require compliance.

### Solution: AI Governance Framework

**EU AI Act Requirements (2026):**
- Risk classification
- Transparency requirements
- Human oversight
- Bias mitigation
- Data governance

**Implementation Checklist:**

| Area | Requirement |
|------|-------------|
| Documentation | Model cards, data sheets |
| Monitoring | Bias detection, drift monitoring |
| Explainability | SHAP/LIME for decisions |
| Human oversight | Review queues, escalation |
| Data governance | Consent, retention, deletion |

**Tools:**
- Model cards: Hugging Face format
- Bias detection: Fairlearn, AI Fairness 360
- Explainability: SHAP, LIME, Captum

---

*AI/ML Best Practices 2026*
*Sources: Prompt Engineering Guide, CNCF, AI Engineer Roadmap*
