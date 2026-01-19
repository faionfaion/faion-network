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

## M-ML-031: Multi-Agent Design Patterns

### Problem

Single all-purpose agents cannot handle complex enterprise workflows efficiently.

### Solution: Orchestrated Multi-Agent Systems

**Eight Essential Design Patterns (Google ADK):**

| Pattern | Description | Use Case |
|---------|-------------|----------|
| Sequential Pipeline | Assembly line, agent passes output to next | Linear workflows |
| Parallel Fan-Out/Gather | Spawn parallel agents, synthesize results | PR reviews, multi-aspect analysis |
| Hierarchical Decomposition | High-level agent delegates subtasks | Complex goal breakdown |
| Generator and Critic | One creates, another validates | Quality-critical content |
| Loop Pattern | Iterative refinement cycles | Self-improving outputs |
| Human-in-the-Loop | Checkpoints for human approval | High-stakes decisions |
| Router Pattern | Dynamic agent selection based on task | Multi-domain queries |
| Blackboard Pattern | Shared workspace for agent collaboration | Knowledge synthesis |

**Architecture Example:**
```
Orchestrator Agent
    ├── Researcher Agent → gather information
    ├── Coder Agent → implement solutions
    ├── Analyst Agent → validate results
    └── Documentation Agent → create reports
```

**Framework Comparison (2026):**

| Framework | Strengths | Setup Complexity |
|-----------|-----------|------------------|
| CrewAI | Role-based teams, real-time collaboration | Low |
| AutoGen | Multi-agent conversations, Microsoft backed | Medium |
| LangGraph | State machines, complex flows | Medium-High |
| AgentFlow | Low-code canvas, production-ready | Low |
| NVIDIA Nemotron | 4x throughput, hybrid MoE | High |

**Enterprise Adoption:**
- Gartner: 1,445% surge in multi-agent inquiries (Q1 2024 → Q2 2025)
- Prediction: 40% of enterprise apps include AI agents by 2026 (Gartner)
- IDC: 80% of workplace apps will have AI copilots by 2026

---

## M-ML-032: Graph RAG & Advanced Retrieval

### Problem

Standard RAG struggles with global questions requiring entity relationships.

### Solution: Graph-Based Retrieval

**Graph RAG Architecture:**
```
Documents → Entity Extraction → Knowledge Graph
                                    ↓
Query → Graph Traversal → Subgraph Selection → LLM Synthesis
```

**Key Techniques:**

| Technique | Description |
|-----------|-------------|
| Entity-Relationship Graphs | Build structured graph over corpus |
| Query-Focused Summarization | Move from local passages to global structure |
| Hybrid Retrieval | Combine vector + graph + keyword search |
| Multi-Vector Retrieval | Dense, sparse, and graph embeddings |
| Continuous Learning | Real-time index updates from streaming data |

**Microsoft GraphRAG Pipeline:**
1. Document chunking and entity extraction
2. Community detection for related concepts
3. Hierarchical summarization at multiple granularities
4. Query routing to appropriate retrieval strategy

**Context-Adaptive Models:**
- LLMs fine-tuned to handle retrieval noise gracefully
- Retrieval-Augmented Reasoning (RAR) patterns
- Agent-controlled retrieval decisions

**Performance:**
- Clinical RAG study: accuracy improved 68% → 73%
- Substantial hallucination reduction
- Better handling of complex multi-hop queries

---

## M-ML-033: LLM Observability Stack (2026)

### Problem

Production AI requires comprehensive monitoring beyond basic logging.

### Solution: Full-Stack LLM Observability

**Platform Comparison:**

| Platform | Focus | Self-Host | Pricing |
|----------|-------|-----------|---------|
| Langfuse | Tracing, prompts, evals | Yes (MIT) | Free / $29/mo |
| Helicone | Cost analytics, caching | Yes | Free (10K req) / $79/mo |
| Arize Phoenix | Evaluation, embeddings | Yes | Free / $50/mo managed |
| Braintrust | Multi-agent tracing | No | Enterprise |
| Portkey | Gateway, fallbacks | Limited | Usage-based |

**Essential Metrics:**

| Category | Metrics |
|----------|---------|
| Cost | Token usage, cost/conversation, cache hit rate |
| Quality | Relevance scores, hallucination rate, user feedback |
| Performance | Latency (P50/P95/P99), throughput, TTFT |
| Reliability | Error rate, retry rate, fallback triggers |
| Agent-specific | Tool call success, reasoning steps, iteration count |

**Integration Architecture:**
```
Application
    ↓
Observability SDK (OpenTelemetry/OpenInference)
    ↓
├── Tracing → Langfuse/Phoenix
├── Analytics → Helicone Dashboard
├── Evaluation → Automated quality gates
└── Alerting → Cost/quality thresholds
```

**Setup Times:**
- Helicone: 15 minutes (proxy-based)
- Langfuse: Few hours (SDK-based)
- Cost savings: 20-30% with caching

---

## M-ML-034: MCP Ecosystem (2025-2026)

### Problem

Fragmented tool integrations across LLM platforms.

### Solution: Model Context Protocol as Industry Standard

**MCP Timeline:**
| Date | Milestone |
|------|-----------|
| Nov 2024 | Anthropic launches MCP |
| Mar 2025 | OpenAI adopts MCP |
| Apr 2025 | Google DeepMind confirms Gemini support |
| May 2025 | Microsoft/GitHub join steering committee |
| Nov 2025 | MCP Apps Extension (SEP-1865) released |
| Dec 2025 | Donated to Linux Foundation (AAIF) |

**Current Scale (2026):**
- 97M+ monthly SDK downloads (Python + TypeScript)
- 8M+ MCP server downloads
- 5,800+ MCP servers available
- 300+ MCP clients

**Founding Members (Agentic AI Foundation):**
- Anthropic, OpenAI, Google, Microsoft, AWS, Cloudflare, Bloomberg

**MCP Apps Extension (SEP-1865):**
- Standardized UI capabilities for agents
- Interactive user interface components
- Cross-platform compatibility

**Implementation:**
```json
{
  "mcpServers": {
    "database": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres"],
      "env": {"DATABASE_URL": "postgresql://..."}
    }
  }
}
```

**2026 Predictions:**
- Multi-agent collaboration becomes standard
- Agent squads dynamically orchestrated
- MCP as common infrastructure layer

---

## M-ML-035: EU AI Act Compliance (2026)

### Problem

August 2026 marks major enforcement milestone for AI regulation.

### Solution: Comprehensive Compliance Framework

**Key Dates:**

| Date | Requirement |
|------|-------------|
| Aug 2025 | GPAI model compliance (transparency, copyright) |
| Aug 2026 | Full high-risk AI system compliance |
| Aug 2026 | Article 50 transparency obligations enforceable |
| Aug 2026 | Member states establish AI regulatory sandboxes |

**Risk Classification:**

| Risk Level | Examples | Requirements |
|------------|----------|--------------|
| Unacceptable | Social scoring, emotion recognition in workplace | Prohibited |
| High | Biometrics, critical infrastructure, employment AI | Full compliance |
| Limited | Chatbots, recommendation systems | Transparency |
| Minimal | Games, spam filters | None |

**High-Risk System Requirements:**
- Quality management systems
- Risk management frameworks
- Technical documentation
- Conformity assessments
- EU database registration
- Data protection impact assessments
- Human oversight mechanisms

**Transparency Obligations (Article 50):**
- AI chatbots must disclose artificial nature
- Emotion recognition requires user notification
- Deepfake content needs machine-readable watermarks
- Biometric categorization faces disclosure mandates
- Training data sources must be disclosed

**Penalties:**
| Violation | Maximum Fine |
|-----------|--------------|
| Unacceptable risk deployment | EUR 35M or 7% global turnover |
| Data governance violations | EUR 20M or 4% global turnover |
| Other non-compliance | EUR 10M or 2% global turnover |

**Compliance Checklist:**
- [ ] Risk classification of all AI systems
- [ ] Model cards and data sheets
- [ ] Bias detection (Fairlearn, AI Fairness 360)
- [ ] Explainability (SHAP, LIME)
- [ ] Human oversight procedures
- [ ] Incident reporting mechanisms
- [ ] Training data documentation
- [ ] Copyright opt-out respect

---

## M-ML-036: Reasoning-First Architectures

### Problem

Agents act before thinking, leading to suboptimal outcomes.

### Solution: Think-Before-Act Patterns

**Core Reasoning Patterns:**

| Pattern | Description |
|---------|-------------|
| ReAct | Interleaved reasoning and acting |
| Reflexion | Self-evaluation and improvement |
| Tree-of-Thought | Explore multiple reasoning paths |
| Planning Loops | Plan → Execute → Verify → Adjust |
| Critique & Revise | Generate → Critique → Improve |

**ReAct Implementation:**
```
Thought: I need to find the company's Q4 revenue
Action: search("Company X Q4 2025 revenue report")
Observation: [search results]
Thought: Found $4.2B revenue, but need YoY comparison
Action: search("Company X Q4 2024 revenue")
Observation: [search results showing $3.8B]
Thought: Can now calculate growth rate
Answer: Q4 2025 revenue was $4.2B, representing 10.5% YoY growth
```

**Tree-of-Thought:**
```
Query
├── Path A: Direct approach
│   ├── Evaluate: Score 0.6
│   └── Continue or prune
├── Path B: Step-by-step
│   ├── Evaluate: Score 0.8
│   └── Expand further
└── Path C: Tool-assisted
    ├── Evaluate: Score 0.9
    └── Select as best path
```

**Reflexion Loop:**
```
Generate response
    ↓
Self-evaluate quality
    ↓
Identify weaknesses
    ↓
Generate improved response
    ↓
Repeat until satisfactory
```

---

*AI/ML Best Practices 2026*
*Sources: Prompt Engineering Guide, CNCF, AI Engineer Roadmap, Google ADK, Microsoft GraphRAG, Anthropic MCP, EU AI Act*

**Research Sources (January 2026):**
- [Machine Learning Mastery - Agentic AI Trends](https://machinelearningmastery.com/7-agentic-ai-trends-to-watch-in-2026/)
- [InfoQ - Multi-Agent Design Patterns](https://www.infoq.com/news/2026/01/multi-agent-design-patterns/)
- [arxiv - Agentic RAG Survey](https://arxiv.org/abs/2501.09136)
- [Data Nucleus - RAG Enterprise Guide](https://datanucleus.dev/rag-and-agentic-ai/what-is-rag-enterprise-guide-2025)
- [LakeFS - LLM Observability Tools](https://lakefs.io/blog/llm-observability-tools/)
- [Langfuse Docs](https://langfuse.com/docs/observability/overview)
- [MCP Specification](https://modelcontextprotocol.io/specification/2025-11-25)
- [Anthropic - MCP Foundation](https://www.anthropic.com/news/donating-the-model-context-protocol-and-establishing-of-the-agentic-ai-foundation)
- [EU AI Act Official](https://artificialintelligenceact.eu/)
- [IAPP - AI Act Compliance Matrix](https://iapp.org/resources/article/eu-ai-act-compliance-matrix)
