# LLM Prompts for Reranking

Prompts for model selection, optimization, debugging, and evaluation of reranking systems.

---

## Table of Contents

- [Model Selection Prompts](#model-selection-prompts)
- [Implementation Prompts](#implementation-prompts)
- [Optimization Prompts](#optimization-prompts)
- [Debugging Prompts](#debugging-prompts)
- [Evaluation Prompts](#evaluation-prompts)
- [Documentation Prompts](#documentation-prompts)

---

## Model Selection Prompts

### Requirements Analysis

```markdown
# Prompt: Analyze Reranking Requirements

Analyze my reranking requirements and recommend the best model.

## My Use Case
- Application type: [e.g., RAG chatbot, document search, e-commerce]
- Domain: [e.g., legal, medical, general, technical documentation]
- Query types: [e.g., questions, keywords, natural language]

## Technical Constraints
- Infrastructure: [e.g., GPU available, CPU only, serverless]
- Latency budget: [e.g., < 200ms p99]
- Throughput: [e.g., 100 QPS]
- Deployment: [e.g., self-hosted, API OK, air-gapped]

## Data Characteristics
- Languages: [e.g., English only, multilingual]
- Document length: [e.g., short passages, long documents]
- Candidate pool size: [e.g., 50-100 documents per query]

## Budget
- API budget: [e.g., $X per 1M requests]
- Infrastructure budget: [e.g., $X per month]

---

Based on these requirements, recommend:
1. Primary model choice with justification
2. Alternative options for different trade-offs
3. Configuration recommendations (batch size, top-k, etc.)
4. Estimated costs and performance expectations
```

### Model Comparison

```markdown
# Prompt: Compare Reranking Models

Compare these reranking models for my use case:

## Models to Compare
1. [Model A, e.g., Cohere Rerank 3]
2. [Model B, e.g., BGE Reranker v2-M3]
3. [Model C, e.g., Jina Reranker v3]

## Evaluation Criteria
- Accuracy (BEIR benchmark scores)
- Latency (p50, p99)
- Cost (per 1M requests)
- Language support
- Ease of integration
- License/terms of use

## My Priorities (rank 1-5)
- Accuracy: [X]
- Speed: [X]
- Cost: [X]
- Multilingual: [X]
- Self-hosting: [X]

---

Provide a detailed comparison table and final recommendation with reasoning.
```

### Migration Assessment

```markdown
# Prompt: Assess Reranker Migration

I want to migrate from [Current Model] to [New Model].

## Current Setup
- Model: [e.g., cross-encoder/ms-marco-MiniLM-L-12-v2]
- Integration: [e.g., sentence-transformers, custom API]
- Performance: [e.g., 150ms p50, 85% nDCG@5]
- Daily volume: [e.g., 100K requests]

## Target Model
- Model: [e.g., BAAI/bge-reranker-v2-m3]
- Expected benefits: [e.g., better multilingual support]

---

Analyze:
1. Expected performance changes (latency, accuracy)
2. Code changes required
3. Migration risks and mitigation
4. A/B testing strategy
5. Rollback plan
```

---

## Implementation Prompts

### Pipeline Architecture

```markdown
# Prompt: Design Reranking Pipeline

Design a reranking pipeline for my RAG system.

## Current Architecture
```
[Describe your current retrieval flow]
```

## Requirements
- First stage: [e.g., Qdrant vector search]
- Reranking model: [e.g., BGE Reranker v2-M3]
- Final top-k: [e.g., 5 documents for LLM context]
- Additional features needed:
  - [ ] Diversity (MMR)
  - [ ] Hybrid search fusion
  - [ ] Multi-stage reranking
  - [ ] Caching
  - [ ] Fallback handling

## Constraints
- Language: [e.g., Python]
- Framework: [e.g., LangChain, LlamaIndex, custom]
- Async required: [yes/no]

---

Provide:
1. Architecture diagram (text-based)
2. Component responsibilities
3. Data flow description
4. Error handling strategy
5. Sample code structure
```

### Integration Code

```markdown
# Prompt: Generate Reranking Integration Code

Generate production-ready code for reranking integration.

## Specifications
- Reranker: [e.g., Cohere Rerank API]
- Retriever: [e.g., Pinecone]
- Framework: [e.g., FastAPI]
- Language: Python 3.11

## Features Required
- [ ] Retry logic with exponential backoff
- [ ] Timeout handling
- [ ] Error fallback to initial results
- [ ] Metrics collection
- [ ] Async support
- [ ] Batch processing
- [ ] Result caching

## Input/Output Format
Input:
```json
{
  "query": "string",
  "documents": [{"id": "string", "content": "string", "metadata": {}}],
  "top_k": 5
}
```

Output:
```json
{
  "results": [{"id": "string", "content": "string", "score": 0.95}],
  "latency_ms": 150
}
```

---

Generate complete, documented, type-annotated Python code.
```

### Configuration Setup

```markdown
# Prompt: Generate Reranking Configuration

Generate configuration for reranking deployment.

## Environment
- Deployment: [e.g., Kubernetes, Docker Compose, serverless]
- Model: [e.g., self-hosted BGE, Cohere API]
- Scale: [e.g., 3 replicas, auto-scaling]

## Requirements
- Environment-based configuration
- Secret management
- Health checks
- Resource limits
- Logging configuration
- Metrics endpoints

---

Generate:
1. YAML configuration file
2. Environment variables template
3. Docker/K8s manifests (if applicable)
4. Startup validation code
```

---

## Optimization Prompts

### Latency Optimization

```markdown
# Prompt: Optimize Reranking Latency

My reranking is too slow. Help me optimize.

## Current Performance
- Model: [e.g., BGE Reranker v2-M3]
- Hardware: [e.g., NVIDIA T4 GPU]
- Current latency:
  - p50: [e.g., 250ms]
  - p99: [e.g., 800ms]
- Batch size: [e.g., 32]
- Documents per request: [e.g., 50]
- Document length: [e.g., avg 500 tokens]

## Target
- p50: [e.g., < 100ms]
- p99: [e.g., < 300ms]

## Constraints
- Cannot change model
- Cannot reduce document count significantly
- Budget for additional hardware: [e.g., $X/month]

---

Provide optimization strategies with expected impact:
1. Inference optimizations (batching, precision, etc.)
2. Caching strategies
3. Architectural changes
4. Hardware recommendations
5. Code-level optimizations
```

### Cost Optimization

```markdown
# Prompt: Reduce Reranking Costs

Help me reduce reranking costs while maintaining quality.

## Current State
- Model: [e.g., Cohere Rerank 3]
- Monthly volume: [e.g., 10M requests]
- Current cost: [e.g., $X/month]
- Documents per request: [e.g., 100]
- Quality metrics: [e.g., 85% nDCG@5]

## Quality Threshold
- Minimum acceptable: [e.g., 80% nDCG@5]
- Critical use cases that need full quality: [describe]

## Flexibility
- Can reduce doc count: [yes/no]
- Can use different model for some traffic: [yes/no]
- Can implement caching: [yes/no]
- Can switch to self-hosted: [yes/no]

---

Provide cost reduction strategies with trade-offs:
1. Immediate optimizations (no quality loss)
2. Trade-off optimizations (some quality loss)
3. Architecture changes for long-term savings
4. Expected cost after each optimization
```

### Throughput Optimization

```markdown
# Prompt: Scale Reranking Throughput

I need to scale reranking to handle more traffic.

## Current State
- Model: [e.g., self-hosted cross-encoder]
- Infrastructure: [e.g., 2x NVIDIA T4]
- Current throughput: [e.g., 50 QPS]
- Latency at current load: [e.g., 100ms p50]

## Target
- Required throughput: [e.g., 500 QPS]
- Latency requirement: [e.g., < 200ms p99]
- Budget: [e.g., $X/month additional]

## Constraints
- Must maintain current accuracy
- Prefer horizontal scaling
- [Any other constraints]

---

Provide scaling strategy:
1. Immediate changes (software optimization)
2. Horizontal scaling plan
3. Load balancing configuration
4. Auto-scaling rules
5. Cost projections at target scale
```

---

## Debugging Prompts

### Quality Issues

```markdown
# Prompt: Debug Reranking Quality Issues

My reranking isn't improving results as expected.

## Symptoms
- [e.g., Relevant documents ranked lower than irrelevant ones]
- [e.g., Quality worse than without reranking]
- [e.g., Inconsistent results for similar queries]

## Current Setup
- Model: [model name]
- First stage retrieval: [method]
- Candidate pool size: [N]
- Document preprocessing: [describe]

## Sample Failing Case
Query: "[example query]"

Retrieved documents (before reranking):
1. [doc 1 - relevant/irrelevant]
2. [doc 2 - relevant/irrelevant]
...

After reranking:
1. [doc X - should be lower]
2. [doc Y - should be higher]
...

Expected ranking:
1. [what should be first]
...

---

Diagnose the issue and provide:
1. Likely root causes
2. Diagnostic steps to confirm
3. Fixes for each potential cause
4. How to verify the fix worked
```

### Latency Issues

```markdown
# Prompt: Debug Reranking Latency Spike

Reranking latency is spiking unexpectedly.

## Normal Performance
- p50: [e.g., 100ms]
- p99: [e.g., 200ms]

## Current Performance (during issues)
- p50: [e.g., 500ms]
- p99: [e.g., 2000ms]

## Context
- When did it start: [time/event]
- Any recent changes: [describe]
- Traffic pattern: [normal/spike/changed]
- Infrastructure changes: [any]

## Observations
- CPU usage: [%]
- GPU usage: [%]
- Memory usage: [%]
- Request queue depth: [N]
- Error rate: [%]

---

Provide:
1. Diagnostic checklist
2. Most likely causes
3. Immediate mitigation steps
4. Long-term fixes
5. Monitoring to prevent recurrence
```

### Integration Issues

```markdown
# Prompt: Debug Reranking Integration

Reranking integration isn't working correctly.

## Error/Symptom
```
[paste error message or describe unexpected behavior]
```

## Code
```python
[paste relevant code]
```

## Environment
- Python version: [X.X]
- Package versions:
  - sentence-transformers: [X.X.X]
  - torch: [X.X.X]
  - [other relevant packages]
- OS: [e.g., Ubuntu 22.04]
- Hardware: [e.g., CPU only, GPU model]

## What I've Tried
1. [attempt 1]
2. [attempt 2]

---

Diagnose the issue and provide:
1. Root cause explanation
2. Step-by-step fix
3. Verification steps
4. How to prevent similar issues
```

### Memory Issues

```markdown
# Prompt: Debug Reranking Memory Issues

Reranking service is experiencing memory problems.

## Symptoms
- [e.g., OOM errors]
- [e.g., Memory gradually increasing]
- [e.g., Slow garbage collection]

## Environment
- Model: [model name]
- Model size: [e.g., 600M params]
- Available memory: [e.g., 8GB]
- GPU memory: [e.g., 16GB]
- Batch size: [N]
- Max documents: [N]
- Max document length: [N tokens]

## Memory Usage Pattern
- Startup: [X GB]
- After warmup: [X GB]
- Under load: [X GB]
- Peak: [X GB]

---

Provide:
1. Memory analysis
2. Optimization strategies
3. Configuration changes
4. Code changes if needed
5. Monitoring setup
```

---

## Evaluation Prompts

### Benchmark Design

```markdown
# Prompt: Design Reranking Evaluation

Help me design a comprehensive evaluation for my reranking system.

## Application Context
- Domain: [e.g., legal document search]
- Query types: [e.g., natural language questions]
- Success criteria: [e.g., users find answer in top 3]

## Available Data
- Existing relevance judgments: [yes/no, how many]
- Query logs: [yes/no]
- Click data: [yes/no]
- Expert annotators: [yes/no]

## Evaluation Goals
- Compare models: [list models]
- Measure production impact: [yes/no]
- Track over time: [yes/no]

---

Provide:
1. Evaluation dataset design
2. Metrics to track (with justification)
3. Baseline definitions
4. Statistical significance approach
5. Evaluation pipeline code
6. Reporting template
```

### A/B Test Design

```markdown
# Prompt: Design Reranking A/B Test

Design an A/B test for comparing reranking approaches.

## Variants
- Control: [current approach]
- Treatment: [new approach]

## Hypothesis
[What improvement do you expect and why]

## Metrics
- Primary: [e.g., click-through rate on top result]
- Secondary: [e.g., time to find answer]
- Guardrails: [e.g., latency p99]

## Traffic
- Daily users: [N]
- Queries per day: [N]
- Test duration flexibility: [min/max days]

## Constraints
- Minimum detectable effect: [e.g., 5% improvement]
- Statistical significance: [e.g., 95%]
- Cannot show to [any user segments]

---

Provide:
1. Sample size calculation
2. Randomization strategy
3. Test duration recommendation
4. Analysis plan
5. Success/failure criteria
6. Rollout plan if successful
```

### Quality Assessment

```markdown
# Prompt: Assess Reranking Quality

Assess the quality of my reranking system.

## Current Metrics
- nDCG@5: [X]
- MRR: [X]
- Precision@3: [X]

## Evaluation Dataset
- Size: [N queries]
- Domain: [describe]
- Relevance scale: [binary / graded]

## Comparison
- Without reranking: [metrics]
- With reranking: [metrics]
- Improvement: [%]

## Sample Results (5 queries)
[Provide 5 example queries with retrieved and reranked results]

---

Assess:
1. Are the metrics appropriate for this use case?
2. Is the improvement statistically significant?
3. Are there concerning patterns in the examples?
4. What additional evaluation would you recommend?
5. Where might the system be failing?
```

---

## Documentation Prompts

### Technical Documentation

```markdown
# Prompt: Generate Reranking Documentation

Generate technical documentation for our reranking system.

## System Overview
- Purpose: [describe]
- Architecture: [describe]
- Model: [name and version]
- Integration points: [list]

## Target Audience
- [ ] New developers onboarding
- [ ] Operations team
- [ ] ML engineers
- [ ] External API consumers

## Documentation Sections Needed
- [ ] Architecture overview
- [ ] API reference
- [ ] Configuration guide
- [ ] Deployment guide
- [ ] Troubleshooting guide
- [ ] Performance tuning guide

---

Generate comprehensive documentation with:
1. Clear structure and navigation
2. Code examples
3. Configuration examples
4. Common issues and solutions
5. Performance expectations
```

### Runbook

```markdown
# Prompt: Create Reranking Runbook

Create an operational runbook for the reranking service.

## Service Details
- Service name: [name]
- Owner team: [team]
- On-call rotation: [details]
- Dependencies: [list]

## SLOs
- Availability: [e.g., 99.9%]
- Latency p99: [e.g., < 500ms]
- Error rate: [e.g., < 0.1%]

## Common Incidents
1. [Incident type 1]
2. [Incident type 2]
3. [Incident type 3]

## Monitoring
- Dashboard URL: [URL]
- Alert channels: [list]
- Logs location: [location]

---

Generate runbook with:
1. Service overview
2. Architecture diagram
3. Dependency map
4. Alert response procedures
5. Common issue resolution
6. Escalation paths
7. Recovery procedures
8. Post-incident checklist
```

### Decision Record

```markdown
# Prompt: Create Reranking ADR

Create an Architecture Decision Record for reranking choice.

## Decision
[What decision was made]

## Context
- Problem: [what problem are we solving]
- Constraints: [technical, business, time]
- Options considered: [list]

## Evaluation
[How were options evaluated]

## Consequences
- Positive: [list]
- Negative: [list]
- Risks: [list]

---

Generate ADR with:
1. Title
2. Status (proposed/accepted/deprecated)
3. Context
4. Decision
5. Consequences
6. Alternatives considered with trade-offs
7. Related decisions
```

---

## Prompt Templates for Specific Scenarios

### LLM-as-Reranker Prompt

```markdown
# Prompt for LLM to act as a reranker

You are a document relevance expert. Given a query and a list of documents, score each document's relevance to the query.

## Instructions
1. Read the query carefully to understand the user's information need
2. For each document, assess:
   - Does it directly answer the query?
   - Does it contain relevant information?
   - How specific and accurate is the information?
3. Assign a relevance score from 0-10:
   - 0-2: Irrelevant
   - 3-4: Marginally relevant
   - 5-6: Somewhat relevant
   - 7-8: Relevant
   - 9-10: Highly relevant, directly answers query

## Query
{query}

## Documents
{documents_formatted}

## Output Format
Return a JSON object:
```json
{
  "rankings": [
    {"index": 0, "score": 8.5, "reasoning": "brief explanation"},
    {"index": 2, "score": 7.0, "reasoning": "brief explanation"},
    ...
  ]
}
```

Return only the top {top_k} most relevant documents, sorted by score descending.
```

### Listwise Reranking Prompt

```markdown
# Listwise reranking prompt (more efficient)

Rank these documents by relevance to the query. Consider all documents together and compare them.

Query: {query}

Documents:
[0] {doc_0}
[1] {doc_1}
[2] {doc_2}
...

Return ONLY a JSON object with the indices of the {top_k} most relevant documents in order from most to least relevant:

{"ranking": [index1, index2, ...]}

The first index is most relevant.
```

### Pairwise Comparison Prompt

```markdown
# Pairwise comparison prompt (most accurate, most expensive)

Compare these two documents for relevance to the query.

Query: {query}

Document A:
{doc_a}

Document B:
{doc_b}

Which document is MORE relevant to answering the query?

Return ONLY: "A" if Document A is more relevant, "B" if Document B is more relevant, or "EQUAL" if equally relevant.
```

### Domain-Specific Reranking Prompt

```markdown
# Domain-specific reranking (e.g., legal)

You are a legal document relevance expert. Rank documents for a legal research query.

## Special Considerations
- Prioritize binding authority over persuasive authority
- Consider jurisdiction relevance
- Weight recent cases higher for evolving areas of law
- Distinguish between holdings and dicta

## Query
{query}

## Jurisdiction (if specified)
{jurisdiction}

## Documents
{documents}

## Scoring Criteria
- 10: Directly on point, binding authority, recent
- 8-9: Highly relevant, may be persuasive authority
- 6-7: Relevant legal principle, different jurisdiction
- 4-5: Tangentially related
- 1-3: Marginally relevant
- 0: Irrelevant

Return JSON with rankings and legal reasoning.
```
