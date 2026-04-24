# LLM Prompts for RAG Development

Prompts for building, debugging, and optimizing RAG systems with AI assistance.

## Table of Contents

1. [Architecture Design Prompts](#architecture-design-prompts)
2. [Implementation Prompts](#implementation-prompts)
3. [Debugging Prompts](#debugging-prompts)
4. [Optimization Prompts](#optimization-prompts)
5. [Evaluation Prompts](#evaluation-prompts)
6. [Documentation Prompts](#documentation-prompts)

---

## Architecture Design Prompts

### RAG Architecture Design

```
Design a RAG (Retrieval-Augmented Generation) architecture for the following use case:

**Use Case:** [Describe your use case]
**Data Sources:** [List document types and sources]
**Scale:** [Number of documents, users, queries per day]
**Requirements:**
- Latency: [Target response time]
- Accuracy: [Accuracy requirements]
- Budget: [Cost constraints]

Please provide:
1. High-level architecture diagram (text-based)
2. Component selection recommendations:
   - Vector database
   - Embedding model
   - LLM for generation
   - Reranking approach
3. Data flow from ingestion to response
4. Scaling considerations
5. Key trade-offs and recommendations
```

### Vector Database Selection

```
Help me select a vector database for my RAG system:

**Requirements:**
- Document count: [Number]
- Query volume: [Queries per second]
- Deployment: [Self-hosted / Managed cloud]
- Budget: [Monthly budget]
- Existing infrastructure: [PostgreSQL, AWS, etc.]
- Required features: [Filtering, hybrid search, etc.]

Compare the following options for my use case:
1. Qdrant
2. Pinecone
3. Weaviate
4. pgvector
5. Chroma
6. Milvus

For each, provide:
- Pros/cons for my use case
- Cost estimate
- Scaling capabilities
- Ease of operations
- Final recommendation with reasoning
```

### Chunking Strategy Design

```
Recommend a chunking strategy for my documents:

**Document Types:**
[List your document types: PDFs, Markdown, HTML, etc.]

**Document Characteristics:**
- Average document length: [Pages/words]
- Structure: [Headings, sections, tables, code blocks]
- Content type: [Technical, legal, conversational, etc.]

**Query Patterns:**
- Typical queries: [Examples of user queries]
- Query complexity: [Simple lookups / Complex reasoning]

Recommend:
1. Chunking method (fixed, recursive, semantic, structure-aware)
2. Optimal chunk size with reasoning
3. Overlap strategy
4. Special handling for tables, code, images
5. Metadata to extract and preserve
6. Example implementation code
```

### Retrieval Strategy Selection

```
Design a retrieval strategy for my RAG application:

**Context:**
- Domain: [Your domain]
- Query types: [Examples]
- Current issues: [If migrating from existing system]

**Evaluate these strategies:**
1. Pure vector search
2. Hybrid (BM25 + Vector)
3. Multi-query retrieval
4. Hierarchical retrieval
5. Agentic retrieval

For my use case, recommend:
1. Primary retrieval strategy
2. Whether to use reranking (and which model)
3. Optimal top-k values at each stage
4. Fusion weights (if hybrid)
5. Query preprocessing steps
6. Implementation approach
```

---

## Implementation Prompts

### RAG Pipeline Implementation

```
Implement a RAG pipeline with the following specifications:

**Framework:** [LlamaIndex / LangChain / Custom]
**Vector Store:** [Qdrant / Pinecone / Chroma / etc.]
**Embedding Model:** [text-embedding-3-large / etc.]
**LLM:** [GPT-4o / Claude / etc.]

**Features Required:**
- [ ] Document ingestion from [source types]
- [ ] Semantic chunking
- [ ] Hybrid search
- [ ] Reranking
- [ ] Source citations
- [ ] Streaming responses
- [ ] Caching
- [ ] Error handling

**Constraints:**
- Must run on [infrastructure]
- Budget: [API costs]
- Latency target: [ms]

Provide:
1. Complete implementation code
2. Configuration file
3. Dependencies (requirements.txt)
4. Usage examples
5. Error handling patterns
```

### Custom Chunker Implementation

```
Implement a custom document chunker with these requirements:

**Requirements:**
1. Preserve document structure (headings, lists)
2. Keep code blocks intact
3. Handle tables appropriately
4. Extract and attach metadata:
   - Document title
   - Section headers
   - Page numbers (for PDFs)
5. Support for: [list file types]

**Chunk Parameters:**
- Target chunk size: [tokens]
- Overlap: [tokens]

Provide:
1. Python implementation
2. Unit tests
3. Usage example
4. Performance considerations
```

### Metadata Filtering Implementation

```
Implement metadata filtering for my RAG system:

**Metadata Fields:**
- category: [list of categories]
- date: datetime
- author: string
- access_level: [public, internal, confidential]
- department: [list of departments]

**Requirements:**
1. Filter by single field
2. Filter by multiple fields (AND/OR)
3. Date range queries
4. Access control enforcement

**Vector Store:** [Your vector store]

Provide:
1. Schema design for metadata
2. Indexing configuration
3. Query implementation
4. Access control middleware
5. Example queries
```

### Caching Layer Implementation

```
Implement a caching layer for my RAG pipeline:

**Requirements:**
1. Cache embeddings for documents (avoid re-embedding)
2. Cache query results (frequent queries)
3. Cache intermediate retrieval results
4. TTL-based expiration
5. Cache invalidation on document updates

**Infrastructure:**
- Cache backend: [Redis / Memcached / In-memory]
- Deployment: [Local / Cloud]

Provide:
1. Cache key design
2. Implementation code
3. Cache warming strategy
4. Invalidation logic
5. Monitoring/metrics
6. Memory management
```

---

## Debugging Prompts

### Poor Retrieval Quality

```
Debug poor retrieval quality in my RAG system:

**Symptoms:**
[Describe what's happening]
- Relevant documents not retrieved
- Irrelevant documents ranked high
- Missing context for answers

**Current Configuration:**
- Embedding model: [model]
- Chunk size: [size]
- Chunk overlap: [overlap]
- Top-k: [value]
- Similarity threshold: [if any]

**Example Failing Query:**
Query: "[Your query]"
Expected: "[What should be retrieved]"
Actual: "[What was retrieved]"

Please:
1. Identify likely causes
2. Provide diagnostic steps
3. Suggest specific fixes
4. Recommend experiments to run
5. Provide code for debugging/analysis
```

### Hallucination Issues

```
My RAG system is hallucinating despite retrieving relevant context:

**Problem:**
Query: "[Query that causes hallucination]"
Retrieved Context: "[Relevant context that was retrieved]"
Generated Answer: "[Hallucinated answer]"
Expected Answer: "[Correct answer]"

**Current Configuration:**
- LLM: [model]
- Temperature: [value]
- System prompt: [your prompt]
- Context injection method: [how you inject context]

Analyze:
1. Why is the model hallucinating?
2. Is it a prompt issue, context issue, or model issue?
3. Specific fixes to try
4. How to validate the fix
5. Guardrails to add
```

### Latency Issues

```
Debug high latency in my RAG pipeline:

**Current Latency:** [X] seconds
**Target Latency:** [Y] seconds

**Pipeline Stages (with measured times):**
1. Query preprocessing: [X] ms
2. Embedding generation: [X] ms
3. Vector search: [X] ms
4. Reranking: [X] ms
5. LLM generation: [X] ms
6. Post-processing: [X] ms

**Infrastructure:**
- Vector DB: [type, location]
- Embedding: [local/API]
- LLM: [local/API]

Identify:
1. Main bottleneck(s)
2. Quick wins for each stage
3. Architecture changes needed
4. Caching opportunities
5. Parallelization opportunities
```

### Memory Issues

```
Debug memory issues in my RAG system:

**Problem:**
[Describe: OOM errors, high memory usage, etc.]

**Context:**
- Document count: [number]
- Average document size: [size]
- Chunk count: [number]
- Batch processing size: [size]
- Available memory: [GB]

**Current Implementation:**
[Describe how you load/process documents]

Provide:
1. Root cause analysis
2. Memory optimization techniques
3. Streaming/batching implementation
4. Memory monitoring code
5. Recommended memory allocation
```

### Inconsistent Results

```
My RAG system returns inconsistent results for similar queries:

**Examples:**
Query 1: "[query]" → "[result A]"
Query 2 (similar): "[query]" → "[result B, different]"

**Configuration:**
- Temperature: [value]
- Seed: [if set]
- Top-k: [value]
- Retrieval method: [method]

Investigate:
1. Source of non-determinism
2. How to ensure consistency
3. Whether variation is acceptable
4. Fixes for each source of randomness
5. Testing approach for consistency
```

---

## Optimization Prompts

### Retrieval Quality Optimization

```
Optimize retrieval quality for my RAG system:

**Current Metrics:**
- Recall@5: [X]
- MRR: [X]
- Precision@5: [X]

**Target Metrics:**
- Recall@5: [Y]
- MRR: [Y]

**Current Configuration:**
- Embedding: [model]
- Chunk size: [size]
- Retrieval: [method]
- Reranking: [yes/no]

**Evaluation Dataset:**
[Describe: size, query types, ground truth availability]

Provide optimization plan:
1. Quick wins (no architecture change)
2. Medium effort improvements
3. Major changes if needed
4. A/B testing approach
5. Monitoring for regression
```

### Cost Optimization

```
Optimize costs for my RAG system:

**Current Costs:**
- Embedding API: $[X]/month
- LLM API: $[X]/month
- Vector DB: $[X]/month
- Infrastructure: $[X]/month
- Total: $[X]/month

**Usage Patterns:**
- Queries per day: [number]
- Tokens per query (avg): [number]
- Index size: [number of vectors]
- Active users: [number]

**Quality Requirements:**
- Minimum acceptable quality: [describe]
- Critical use cases: [list]

Optimize by:
1. Reducing embedding costs
2. Reducing LLM costs
3. Caching strategies
4. Model selection alternatives
5. Architecture changes
6. Expected savings and trade-offs
```

### Latency Optimization

```
Optimize latency for my RAG system:

**Current State:**
- P50 latency: [X] ms
- P95 latency: [X] ms
- P99 latency: [X] ms

**Target:**
- P95 latency: [Y] ms

**Breakdown:**
[List each pipeline stage with timing]

**Constraints:**
- Cannot sacrifice quality for speed
- Budget for infrastructure: [X]
- Must work with [existing infrastructure]

Provide:
1. Immediate optimizations (no infra change)
2. Caching strategy
3. Parallelization opportunities
4. Infrastructure upgrades if needed
5. CDN/edge deployment options
6. Expected latency after each optimization
```

### Scaling Optimization

```
Scale my RAG system to handle increased load:

**Current Capacity:**
- Max queries/second: [X]
- Document count: [X]
- Response time at max load: [X] ms

**Target Capacity:**
- Required queries/second: [Y]
- Expected document count: [Y]
- Target response time: [Y] ms

**Current Architecture:**
[Describe current setup]

Provide scaling plan:
1. Horizontal vs vertical scaling recommendations
2. Database scaling approach
3. Load balancing strategy
4. Caching layer design
5. Async processing where applicable
6. Cost implications
7. Implementation priority order
```

---

## Evaluation Prompts

### Evaluation Dataset Creation

```
Help me create an evaluation dataset for my RAG system:

**Domain:** [Your domain]
**Document Types:** [Types of docs in your knowledge base]
**Query Patterns:** [Typical user queries]

Requirements:
1. Generate [N] diverse test queries
2. Include:
   - Simple factual queries
   - Complex multi-hop queries
   - Edge cases (out of scope, ambiguous)
   - Queries requiring synthesis across documents
3. For each query, provide:
   - Expected answer
   - Relevant source documents (if known)
   - Query category/difficulty

Provide:
1. Query generation methodology
2. Sample queries across categories
3. Answer annotation guidelines
4. Quality assurance process
5. Dataset format (JSON/CSV)
```

### Evaluation Framework Setup

```
Set up comprehensive evaluation for my RAG system:

**Evaluation Goals:**
- Track quality over time
- Compare configuration changes
- Identify regressions early

**Current Stack:**
- Framework: [LlamaIndex/LangChain]
- Vector DB: [type]
- LLM: [model]

Implement:
1. Retrieval metrics (Recall@k, MRR, NDCG)
2. Generation metrics (Faithfulness, Relevancy)
3. End-to-end metrics (Answer correctness)
4. Automated evaluation pipeline
5. Reporting dashboard
6. CI/CD integration
7. Alerting on regression
```

### A/B Testing Setup

```
Design A/B testing for RAG configuration changes:

**Change to Test:**
[Describe the change: new embedding model, different chunk size, etc.]

**Success Metrics:**
1. Primary: [e.g., answer correctness]
2. Secondary: [e.g., latency, user satisfaction]

**Constraints:**
- Minimum sample size: [number]
- Test duration: [days]
- Risk tolerance: [low/medium/high]

Provide:
1. Experiment design
2. Traffic splitting implementation
3. Statistical significance calculation
4. Rollback criteria
5. Monitoring setup
6. Analysis template
```

---

## Documentation Prompts

### API Documentation

```
Generate API documentation for my RAG service:

**Endpoints:**
1. POST /index - Index documents
2. POST /query - Query the knowledge base
3. GET /health - Health check
4. DELETE /documents/{id} - Delete document

**For Each Endpoint, Provide:**
- Description
- Request format (with examples)
- Response format (with examples)
- Error codes and handling
- Rate limits
- Authentication

**Format:** OpenAPI 3.0 specification
```

### Architecture Documentation

```
Document my RAG system architecture:

**Components:**
[List your components]

**Generate:**
1. Architecture overview
2. Component descriptions
3. Data flow diagrams (text-based)
4. API contracts
5. Configuration reference
6. Deployment guide
7. Monitoring and alerting guide
8. Troubleshooting runbook
9. Capacity planning guide
```

### Runbook Generation

```
Create an operations runbook for my RAG system:

**System Components:**
- Vector DB: [type]
- API Service: [framework]
- Cache: [type]
- LLM Provider: [provider]

**Cover These Scenarios:**
1. High latency alerts
2. Error rate spikes
3. Vector DB issues
4. LLM API failures
5. Cache failures
6. Memory pressure
7. Disk space issues
8. Index corruption

For each scenario:
1. Detection (what alerts fire)
2. Initial diagnosis steps
3. Resolution steps
4. Escalation criteria
5. Post-incident review checklist
```

---

## Quick Reference Prompts

### Quick Fix Prompts

```
# Empty retrieval results
"My RAG query returns no results. Query: [X]. Help debug."

# Low relevance scores
"Retrieved docs have low scores (all <0.3). How to improve?"

# Slow embedding
"Embedding [N] documents takes [X] hours. How to speed up?"

# High memory usage
"My RAG index uses [X] GB memory for [N] docs. How to reduce?"

# Inconsistent answers
"Same query gives different answers. How to fix?"
```

### Code Generation Prompts

```
# Streaming response
"Implement streaming RAG response with [framework]."

# Async processing
"Convert my RAG pipeline to async for better throughput."

# Batch indexing
"Implement efficient batch document indexing with progress tracking."

# Multi-tenant
"Add multi-tenancy to my RAG system (separate knowledge bases per org)."

# Access control
"Implement document-level access control in RAG retrieval."
```

### Analysis Prompts

```
# Compare configurations
"Compare these two RAG configs and recommend which to use: [A] vs [B]"

# Analyze failure modes
"Analyze this failed RAG response and suggest fixes: Query: [X], Answer: [Y], Expected: [Z]"

# Benchmark interpretation
"Interpret these RAG benchmarks and suggest next steps: [metrics]"

# Cost analysis
"Analyze my RAG costs and identify optimization opportunities: [usage data]"
```
