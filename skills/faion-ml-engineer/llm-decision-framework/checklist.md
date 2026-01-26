# LLM Decision Checklist

Step-by-step checklist for selecting the right LLM enhancement approach.

## Phase 1: Requirements Analysis

### Data Requirements

- [ ] **Data freshness:** How often does knowledge change?
  - Daily/hourly: RAG required
  - Monthly: RAG or periodic fine-tuning
  - Rarely/never: Fine-tuning viable

- [ ] **Data volume:** How much domain data?
  - <100 documents: Prompt engineering with context
  - 100-10K documents: RAG
  - 10K+ documents: RAG with advanced retrieval

- [ ] **Data sensitivity:** Where can data be processed?
  - Public cloud OK: Any approach
  - Private cloud only: Self-hosted models + RAG
  - On-premise only: Local models, on-prem vector DB

### Performance Requirements

- [ ] **Latency requirements:**
  - <500ms: Prompt engineering or cached RAG
  - 500ms-2s: RAG acceptable
  - >2s acceptable: Any approach

- [ ] **Accuracy requirements:**
  - General quality: Prompt engineering
  - High accuracy with sources: RAG
  - Domain-specific precision: Fine-tuning
  - Maximum accuracy: RAFT (hybrid)

- [ ] **Scale requirements:**
  - <1K queries/day: Any approach
  - 1K-100K queries/day: Cost-optimize with caching
  - >100K queries/day: Consider fine-tuned smaller models

### Functional Requirements

- [ ] **Citation needed:** Source attribution required?
  - Yes: RAG (provides source documents)
  - No: Any approach

- [ ] **Output format:** Strict format requirements?
  - Flexible: Prompt engineering
  - Consistent JSON/XML: Structured output
  - Domain-specific format: Fine-tuning

- [ ] **Reasoning complexity:** Type of reasoning?
  - Simple Q&A: Prompt engineering
  - Multi-step reasoning: CoT prompting or reasoning models
  - Complex analysis: Fine-tuning or agents

## Phase 2: Constraint Evaluation

### Budget Constraints

- [ ] **Setup budget:**
  - <$1K: Prompt engineering only
  - $1K-10K: RAG viable
  - $10K-50K: Fine-tuning viable
  - >$50K: Full stack including RAFT

- [ ] **Monthly operational budget:**
  - <$100: Prompt engineering, caching
  - $100-1K: Basic RAG
  - $1K-10K: Production RAG or fine-tuning
  - >$10K: Enterprise RAG + fine-tuning

### Team Constraints

- [ ] **ML expertise available:**
  - None: Prompt engineering, managed services
  - Basic: RAG with existing tools
  - Advanced: Fine-tuning, custom architectures

- [ ] **Infrastructure expertise:**
  - None: Fully managed (Pinecone, OpenAI)
  - Basic: Semi-managed (Qdrant Cloud, Weaviate Cloud)
  - Advanced: Self-hosted (Qdrant, pgvector)

### Timeline Constraints

- [ ] **Time to production:**
  - Days: Prompt engineering only
  - Weeks: RAG
  - Months: Fine-tuning

## Phase 3: Approach Selection

### Decision Tree

```
Q1: Need real-time/dynamic data?
    YES -> RAG (continue to Q2)
    NO  -> Continue to Q2

Q2: Need specialized domain behavior?
    YES -> Fine-tuning (or RAFT if Q1=YES)
    NO  -> Prompt engineering (or RAG if Q1=YES)

Q3: Need strict output format?
    YES -> Add structured output
    NO  -> Standard output

Q4: High volume (>10K queries/day)?
    YES -> Consider model distillation, caching
    NO  -> Direct API calls OK
```

### Selected Approach

- [ ] **Primary approach:** ________________
- [ ] **Secondary techniques:** ________________
- [ ] **Fallback strategy:** ________________

## Phase 4: Implementation Checklist

### Prompt Engineering

- [ ] Define system prompt with clear instructions
- [ ] Add few-shot examples (3-5)
- [ ] Test with edge cases
- [ ] Implement structured output if needed
- [ ] Set up prompt versioning

### RAG Implementation

- [ ] Select vector database (see [vector-databases/](../vector-databases/README.md))
- [ ] Choose embedding model
- [ ] Define chunking strategy
- [ ] Implement retrieval pipeline
- [ ] Add reranking (optional)
- [ ] Set up hybrid search (optional)
- [ ] Configure caching layer
- [ ] Implement evaluation metrics

### Fine-tuning Implementation

- [ ] Prepare training dataset (min 100-1000 examples)
- [ ] Validate data quality
- [ ] Select base model
- [ ] Choose fine-tuning method (SFT, LoRA, QLoRA)
- [ ] Set up training infrastructure
- [ ] Run training
- [ ] Evaluate on held-out test set
- [ ] Deploy fine-tuned model
- [ ] Monitor for drift

### RAFT (Hybrid) Implementation

- [ ] Complete fine-tuning checklist
- [ ] Complete RAG checklist
- [ ] Synchronize knowledge base with fine-tuning data
- [ ] Test combined pipeline
- [ ] Set up monitoring for both components

## Phase 5: Validation

### Pre-Launch

- [ ] Accuracy meets requirements
- [ ] Latency within bounds
- [ ] Cost per query acceptable
- [ ] Hallucination rate measured and acceptable
- [ ] Edge cases handled
- [ ] Fallback behavior defined

### Post-Launch

- [ ] Monitoring in place
- [ ] Alerting configured
- [ ] User feedback collection enabled
- [ ] Regular evaluation scheduled
- [ ] Update/retraining plan documented

---

*LLM Decision Checklist v2.0*
