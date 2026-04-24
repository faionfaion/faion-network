# LLM Decision Examples

Real-world examples of LLM architecture decisions.

## Example 1: Customer Support Chatbot

### Requirements

- Answer questions about company products
- Use internal knowledge base (500 articles)
- Cite sources for answers
- <2s response time
- 10K queries/day

### Analysis

| Factor | Value | Implication |
|--------|-------|-------------|
| Data freshness | Weekly updates | RAG viable |
| Data volume | 500 documents | RAG appropriate |
| Citations needed | Yes | RAG required |
| Latency | <2s | RAG acceptable |
| Volume | 10K/day | Caching recommended |

### Decision: RAG

**Architecture:**
```
User Query
    |
    v
Embedding (OpenAI ada-002)
    |
    v
Vector Search (Qdrant)
    |
    v
Reranker (Cohere)
    |
    v
LLM (GPT-4o) + Context
    |
    v
Response with Citations
```

**Cost estimate:**
- Vector DB: $200/month (Qdrant Cloud)
- Embeddings: $50/month (10K queries * 500 tokens avg)
- Reranker: $100/month
- LLM: $500/month (GPT-4o)
- **Total: ~$850/month**

---

## Example 2: Legal Document Analyzer

### Requirements

- Extract clauses from contracts
- Strict JSON output format
- Domain-specific legal terminology
- High accuracy (>98%)
- 100 documents/day

### Analysis

| Factor | Value | Implication |
|--------|-------|-------------|
| Data freshness | Static contracts | Fine-tuning OK |
| Output format | Strict JSON | Structured output + fine-tuning |
| Domain expertise | High | Fine-tuning beneficial |
| Accuracy | >98% | Fine-tuning + evaluation |
| Volume | 100/day | Cost not primary concern |

### Decision: Fine-tuning + Structured Output

**Architecture:**
```
Contract PDF
    |
    v
PDF Parser (PyMuPDF)
    |
    v
Fine-tuned GPT-4o
    |
    v
Structured Output (JSON Schema)
    |
    v
Validation Layer
    |
    v
Extracted Clauses
```

**Implementation:**
- Base model: GPT-4o
- Training data: 1,000 annotated contracts
- Fine-tuning method: OpenAI SFT
- Output: JSON with function calling

**Cost estimate:**
- Fine-tuning: $5,000 (one-time)
- Inference: $300/month (100 docs * 10K tokens * $0.01/1K)
- **Total: $5,000 setup + $300/month**

---

## Example 3: Real-time Financial Assistant

### Requirements

- Answer questions about current market data
- Access company financial database
- Sub-second responses for critical queries
- 24/7 availability
- Regulatory compliance (audit trail)

### Analysis

| Factor | Value | Implication |
|--------|-------|-------------|
| Data freshness | Real-time | RAG with live feeds |
| Latency | <1s for critical | Caching + fast retrieval |
| Compliance | Audit required | Full observability |
| Availability | 24/7 | Redundant architecture |

### Decision: RAG with Caching + Observability

**Architecture:**
```
User Query
    |
    +---> Cache Check (Redis)
    |         |
    |    HIT: Return cached
    |         |
    |    MISS: Continue
    |
    v
Query Router
    |
    +---> Static Knowledge (Vector DB)
    |
    +---> Live Market Data (API)
    |
    +---> Company Database (SQL)
    |
    v
Context Assembly
    |
    v
LLM (Claude 3.5) + Observability
    |
    v
Response + Audit Log
```

**Key components:**
- Vector DB: Qdrant (self-hosted for compliance)
- Cache: Redis with 5-minute TTL for market data
- Observability: Langfuse for full trace logging
- Fallback: Secondary LLM provider

**Cost estimate:**
- Infrastructure: $2,000/month
- LLM: $1,500/month
- Observability: $300/month
- **Total: ~$3,800/month**

---

## Example 4: E-commerce Product Description Generator

### Requirements

- Generate product descriptions from specs
- Consistent brand voice
- Multiple languages
- 50K products
- Batch processing OK

### Analysis

| Factor | Value | Implication |
|--------|-------|-------------|
| Consistency | Brand voice | Fine-tuning for style |
| Volume | 50K products | Cost optimization critical |
| Latency | Batch OK | Can use slower/cheaper models |
| Languages | Multiple | Multilingual fine-tuning |

### Decision: Fine-tuned Smaller Model

**Architecture:**
```
Product Specs (CSV/JSON)
    |
    v
Batch Processor
    |
    v
Fine-tuned GPT-4o-mini (or Llama 3.2)
    |
    v
Quality Check (LLM-as-Judge)
    |
    v
Translation Layer (if needed)
    |
    v
Product Descriptions
```

**Implementation:**
- Base model: GPT-4o-mini (cost-effective)
- Training data: 500 high-quality descriptions
- Fine-tuning: OpenAI SFT
- Quality gate: 10% human review

**Cost estimate:**
- Fine-tuning: $1,000 (one-time)
- Batch inference: $200/month (50K * 500 tokens)
- **Total: $1,000 setup + $200/month**

---

## Example 5: Medical Diagnosis Support

### Requirements

- Assist doctors with differential diagnosis
- Access medical literature (10M+ papers)
- Must cite sources
- Maximum accuracy critical
- Regulatory (FDA considerations)

### Analysis

| Factor | Value | Implication |
|--------|-------|-------------|
| Data volume | 10M+ papers | Advanced RAG |
| Citations | Required | RAG essential |
| Accuracy | Maximum | RAFT (hybrid) |
| Regulation | FDA | Full documentation |

### Decision: RAFT (Hybrid RAG + Fine-tuning)

**Architecture:**
```
Symptom Input
    |
    v
Medical NER (fine-tuned)
    |
    v
Multi-index RAG
    |
    +---> Medical Literature (PubMed)
    |
    +---> Clinical Guidelines
    |
    +---> Drug Interactions DB
    |
    v
Context Assembly + Reranking
    |
    v
Fine-tuned Medical LLM
    |
    v
Differential Diagnosis + Citations
    |
    v
Human Expert Review
```

**Key components:**
- Base model: Claude 3.5 (long context)
- Fine-tuning: Domain-adapted on medical texts
- Vector DB: Weaviate (supports knowledge graphs)
- Compliance: Full HIPAA logging

**Cost estimate:**
- Fine-tuning: $50,000 (including data prep)
- Infrastructure: $5,000/month
- LLM: $3,000/month
- Compliance/auditing: $2,000/month
- **Total: $50,000 setup + $10,000/month**

---

## Example 6: Internal Documentation Q&A

### Requirements

- Answer questions about internal docs
- 2,000 Confluence pages
- Employees only (private)
- Simple deployment
- Low budget

### Analysis

| Factor | Value | Implication |
|--------|-------|-------------|
| Data volume | 2,000 pages | Basic RAG |
| Privacy | Internal only | Self-hosted or private cloud |
| Budget | Low | Open-source stack |
| Complexity | Simple | Managed solutions |

### Decision: Simple RAG with Open-Source Stack

**Architecture:**
```
Confluence Sync
    |
    v
Chunking + Embedding (OpenAI or local)
    |
    v
Vector Storage (Chroma or pgvector)
    |
    v
Simple RAG Pipeline (LangChain)
    |
    v
LLM (GPT-4o-mini or Claude Haiku)
    |
    v
Slack/Teams Bot
```

**Implementation:**
- Embeddings: OpenAI ada-002 or local (e5-small)
- Vector DB: Chroma (file-based, simple)
- Framework: LangChain
- Interface: Slack bot

**Cost estimate:**
- Infrastructure: $50/month (cloud VM)
- LLM: $100/month
- **Total: ~$150/month**

---

## Decision Summary Table

| Use Case | Approach | Setup Cost | Monthly Cost |
|----------|----------|------------|--------------|
| Customer Support | RAG | $2K | $850 |
| Legal Analyzer | Fine-tuning | $5K | $300 |
| Financial Assistant | RAG + Cache | $10K | $3,800 |
| Product Descriptions | Fine-tuned small | $1K | $200 |
| Medical Diagnosis | RAFT (hybrid) | $50K | $10,000 |
| Internal Docs Q&A | Simple RAG | $0.5K | $150 |

---

*LLM Decision Examples v2.0*
