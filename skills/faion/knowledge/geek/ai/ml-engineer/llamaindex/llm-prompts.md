# LlamaIndex LLM Prompts

Prompts for LLM-assisted LlamaIndex development, debugging, and optimization.

---

## Table of Contents

1. [Index Design Prompts](#index-design-prompts)
2. [Chunking Strategy Prompts](#chunking-strategy-prompts)
3. [Query Engine Prompts](#query-engine-prompts)
4. [Debugging Prompts](#debugging-prompts)
5. [Optimization Prompts](#optimization-prompts)
6. [Workflow Design Prompts](#workflow-design-prompts)
7. [Agent Design Prompts](#agent-design-prompts)
8. [Evaluation Prompts](#evaluation-prompts)

---

## Index Design Prompts

### Analyze Document Corpus for Index Design

```
Analyze my document corpus to recommend the best LlamaIndex index type and configuration.

**Document Corpus Details:**
- Document types: [PDFs, Markdown, HTML, etc.]
- Total documents: [number]
- Average document size: [pages/words/chars]
- Content domain: [technical docs, legal, medical, etc.]
- Update frequency: [static, daily, real-time]
- Query patterns: [Q&A, summarization, comparison, etc.]

**Requirements:**
- Response latency: [<1s, <5s, etc.]
- Accuracy priority: [high, medium]
- Cost constraints: [budget/month for API calls]

**Questions to Answer:**
1. Which index type should I use? (VectorStoreIndex, PropertyGraphIndex, etc.)
2. What chunking strategy is optimal?
3. Which vector store is recommended?
4. Should I use hybrid search (vector + BM25)?
5. Do I need metadata extraction?

Please provide specific LlamaIndex code configuration.
```

### Design Multi-Index Architecture

```
Design a multi-index architecture for my RAG application.

**Data Sources:**
1. [Source 1]: [description, size, query types]
2. [Source 2]: [description, size, query types]
3. [Source 3]: [description, size, query types]

**Query Patterns:**
- [Pattern 1]: [description, frequency]
- [Pattern 2]: [description, frequency]

**Requirements:**
- Some queries need data from multiple sources
- Different sources have different update schedules
- Cost optimization is important

**Provide:**
1. Index architecture diagram
2. Routing strategy (RouterQueryEngine vs SubQuestionQueryEngine)
3. Code template for the architecture
4. Pros and cons of the design
```

### Recommend Vector Store

```
Help me choose the right vector store for my LlamaIndex application.

**Application Context:**
- Environment: [local dev, cloud, hybrid]
- Expected documents: [number]
- Expected queries/day: [number]
- Team size: [number]
- Existing infrastructure: [PostgreSQL, K8s, etc.]

**Requirements:**
- Metadata filtering: [required/optional]
- Hybrid search: [required/optional]
- Managed service: [preferred/not required]
- Self-hosted: [required/acceptable/not preferred]
- Budget: [range]

**Compare:**
1. Qdrant vs Pinecone vs Weaviate vs Chroma vs pgvector

For each, provide:
- Pros/cons for my use case
- Estimated cost
- LlamaIndex integration code
- Migration complexity
```

---

## Chunking Strategy Prompts

### Optimize Chunking for Document Type

```
Recommend optimal chunking strategy for my documents.

**Document Details:**
- Type: [technical documentation / legal contracts / research papers / etc.]
- Structure: [headers/sections / continuous text / tables / code blocks]
- Average length: [pages/words]
- Languages: [English, multilingual]

**Current Chunking:**
- Strategy: [SentenceSplitter / etc.]
- Chunk size: [X tokens]
- Overlap: [Y tokens]

**Problems Observed:**
- [Problem 1]: [e.g., "context lost between chunks"]
- [Problem 2]: [e.g., "code blocks split incorrectly"]

**Goals:**
- Improve retrieval precision
- Maintain context
- Handle [specific structure]

Provide:
1. Recommended splitter (SentenceSplitter, SemanticSplitter, MarkdownNodeParser, etc.)
2. Optimal chunk_size and chunk_overlap
3. Metadata extraction recommendations
4. Code example with before/after comparison
```

### Design Hierarchical Chunking

```
Help me implement hierarchical chunking for better context retrieval.

**Document Characteristics:**
- Documents have clear section hierarchy
- Some questions need broad context, others need specifics
- Average document: [X pages]

**Current Issues:**
- Small chunks lose context
- Large chunks reduce precision
- [Other issues]

**Provide:**
1. HierarchicalNodeParser configuration
2. AutoMergingRetriever setup
3. Optimal chunk sizes for each level
4. Trade-offs and when to use this approach
5. Complete code example
```

---

## Query Engine Prompts

### Design Custom Query Pipeline

```
Design a custom query pipeline for my RAG application.

**Query Types:**
1. [Type 1]: [description, example]
2. [Type 2]: [description, example]
3. [Type 3]: [description, example]

**Current Setup:**
- Index type: [VectorStoreIndex]
- Basic query engine with top_k=5

**Problems:**
- [Problem 1]: [description]
- [Problem 2]: [description]

**Requirements:**
- Handle [query type] differently
- Include [specific processing step]
- Return [specific output format]

**Provide:**
1. Query pipeline architecture
2. Custom retriever configuration
3. Reranking strategy
4. Response synthesis customization
5. Complete code implementation
```

### Implement Query Routing

```
Help me implement intelligent query routing.

**Indexes Available:**
1. [Index 1]: [content type, when to use]
2. [Index 2]: [content type, when to use]
3. [Index 3]: [content type, when to use]

**Example Queries:**
- "[Query A]" -> should route to [Index X]
- "[Query B]" -> should route to [Index Y]
- "[Query C]" -> should use multiple indexes

**Requirements:**
- Automatic routing based on query content
- Fallback handling
- Logging for debugging

**Provide:**
1. RouterQueryEngine vs SubQuestionQueryEngine decision
2. Tool descriptions for optimal routing
3. Code implementation
4. Testing strategy
```

---

## Debugging Prompts

### Diagnose Poor Retrieval Quality

```
Help me debug poor retrieval quality in my RAG system.

**Symptoms:**
- Retrieved chunks are not relevant to the query
- Correct information exists in the index but isn't retrieved
- [Other symptoms]

**Current Configuration:**
```python
# Paste your current configuration
```

**Example Failing Query:**
- Query: "[query text]"
- Expected to retrieve: [what should be found]
- Actually retrieved: [what was found]

**Information Needed:**
1. Are embeddings capturing the right semantics?
2. Is chunking splitting important context?
3. Is the query being interpreted correctly?

**Provide:**
1. Diagnostic steps to identify the root cause
2. Specific tests to run
3. Configuration changes to try
4. Code for debugging (similarity scores, embedding visualization, etc.)
```

### Debug Response Hallucinations

```
Help me fix hallucination issues in my RAG responses.

**Problem:**
The LLM is generating information not present in the retrieved context.

**Example:**
- Query: "[query]"
- Retrieved context: "[context]"
- Response: "[response with hallucinated info]"
- Hallucinated part: "[specific hallucinated content]"

**Current Configuration:**
- LLM: [model]
- Temperature: [value]
- Response mode: [mode]
- Prompt template: [if custom]

**Provide:**
1. Root cause analysis
2. Prompt engineering fixes
3. Configuration changes
4. Evaluation strategy to measure hallucination rate
5. Code implementation
```

### Troubleshoot Performance Issues

```
Help me diagnose and fix performance issues.

**Symptoms:**
- Query latency: [current] (target: [target])
- Memory usage: [current]
- [Other issues]

**Current Setup:**
- Documents: [number]
- Index type: [type]
- Vector store: [store]
- Hosting: [local/cloud]

**Profiling Results (if available):**
- Embedding time: [X]ms
- Retrieval time: [X]ms
- LLM time: [X]ms

**Provide:**
1. Performance profiling code
2. Bottleneck identification
3. Optimization recommendations
4. Trade-offs for each optimization
5. Implementation priority
```

---

## Optimization Prompts

### Optimize for Cost

```
Help me reduce API costs while maintaining quality.

**Current Usage:**
- Queries/day: [number]
- Avg tokens/query: [number]
- Monthly cost: [amount]
- LLM: [model]
- Embedding model: [model]

**Quality Requirements:**
- Cannot compromise on: [specific aspects]
- Can accept trade-offs on: [specific aspects]

**Provide:**
1. Cost breakdown analysis
2. Model selection recommendations (smaller models, local options)
3. Caching strategy
4. Batch processing opportunities
5. Estimated savings for each optimization
6. Implementation code
```

### Optimize Retrieval Accuracy

```
Help me improve retrieval accuracy for my RAG system.

**Current Metrics:**
- MRR: [value]
- Hit Rate: [value]
- [Other metrics]

**Target Metrics:**
- MRR: [target]
- Hit Rate: [target]

**Current Configuration:**
```python
# Paste configuration
```

**Evaluation Dataset:**
- Size: [number] question-answer pairs
- Domain: [domain]

**Constraints:**
- Latency budget: [max ms]
- Cost budget: [max $/query]

**Provide:**
1. Analysis of current weaknesses
2. Prioritized list of improvements
3. Expected impact of each improvement
4. A/B testing strategy
5. Implementation code for top 3 recommendations
```

---

## Workflow Design Prompts

### Design Event-Driven Workflow

```
Help me design a LlamaIndex Workflow for my use case.

**Use Case:**
[Describe the overall goal]

**Steps Required:**
1. [Step 1]: [input] -> [output]
2. [Step 2]: [input] -> [output]
3. [Step 3]: [input] -> [output]

**Special Requirements:**
- Parallel processing: [where needed]
- Conditional branching: [conditions]
- Error handling: [requirements]
- State persistence: [requirements]

**Provide:**
1. Event definitions (Pydantic models)
2. Step implementations
3. Context/state management
4. Error handling
5. Complete workflow code
6. Testing approach
```

### Convert Sequential to Event-Driven

```
Help me convert my sequential RAG code to a LlamaIndex Workflow.

**Current Code:**
```python
# Paste current sequential code
```

**Goals:**
- Better error handling
- Observability
- Ability to pause/resume
- [Other goals]

**Provide:**
1. Workflow architecture design
2. Event definitions
3. Step breakdown
4. Migration strategy
5. Complete workflow code
6. Comparison of before/after
```

---

## Agent Design Prompts

### Design Tool-Using Agent

```
Help me design an agent with custom tools.

**Agent Purpose:**
[Describe what the agent should do]

**Required Capabilities:**
1. [Capability 1]: [description]
2. [Capability 2]: [description]
3. [Capability 3]: [description]

**Available Resources:**
- Knowledge bases: [list]
- APIs: [list]
- Databases: [list]

**Constraints:**
- Max iterations: [number]
- Timeout: [seconds]
- Cost per interaction: [limit]

**Provide:**
1. Tool design (name, description, parameters)
2. Agent type selection (ReAct, OpenAI, etc.)
3. System prompt
4. Memory configuration
5. Complete implementation
6. Example interactions
```

### Design Multi-Agent System

```
Help me design a multi-agent system using AgentWorkflow.

**Agents Needed:**
1. [Agent 1]: [role, capabilities]
2. [Agent 2]: [role, capabilities]
3. [Agent 3]: [role, capabilities]

**Interaction Patterns:**
- [Scenario 1]: Agent 1 -> Agent 2 -> Agent 3
- [Scenario 2]: Agent 1 -> Agent 3
- [Scenario 3]: [description]

**Handoff Conditions:**
- Agent 1 hands off when: [condition]
- Agent 2 hands off when: [condition]

**Shared State:**
- [State item 1]: accessed by [which agents]
- [State item 2]: accessed by [which agents]

**Provide:**
1. Agent definitions with tools
2. Handoff logic
3. State management
4. Orchestration pattern (AgentWorkflow vs custom)
5. Complete implementation
6. Debugging/monitoring approach
```

---

## Evaluation Prompts

### Create Evaluation Dataset

```
Help me create an evaluation dataset for my RAG system.

**Document Corpus:**
- Domain: [domain]
- Size: [documents]
- Sample content: [paste sample]

**Evaluation Goals:**
- Test retrieval quality
- Test response quality
- Test [specific aspect]

**Question Types Needed:**
1. Factual questions: [number]
2. Comparison questions: [number]
3. Summarization questions: [number]
4. [Other types]: [number]

**Provide:**
1. Question generation approach
2. Ground truth annotation guidelines
3. Code for generating questions using LlamaIndex
4. Dataset format and storage
5. Quality validation approach
```

### Design Evaluation Pipeline

```
Help me design a comprehensive evaluation pipeline.

**Components to Evaluate:**
- Retrieval: MRR, Hit Rate, NDCG
- Response: Faithfulness, Relevancy, Correctness
- End-to-end: User satisfaction proxy

**Current Setup:**
- Index: [type]
- Query engine: [configuration]
- Evaluation dataset: [size, format]

**Requirements:**
- Automated pipeline
- CI/CD integration
- Historical tracking
- Alerting on regression

**Provide:**
1. Evaluation metrics selection
2. LlamaIndex evaluator configuration
3. Batch evaluation code
4. Results visualization
5. CI/CD integration script
6. Alerting thresholds
```

### Compare Configurations

```
Help me set up A/B testing for RAG configurations.

**Configuration A:**
```python
# Paste config A
```

**Configuration B:**
```python
# Paste config B
```

**Evaluation Questions:**
[List of questions]

**Metrics to Compare:**
- Latency
- Retrieval quality (MRR, Hit Rate)
- Response quality (Faithfulness, Relevancy)
- Cost

**Provide:**
1. Comparison framework code
2. Statistical significance testing
3. Results visualization
4. Recommendation criteria
5. Complete implementation
```

---

## Quick Reference Prompts

### Architecture Decision

```
I need to decide between [Option A] and [Option B] for my LlamaIndex application.

**Context:** [brief context]
**Constraints:** [constraints]
**Priority:** [what matters most]

Provide a decision matrix and recommendation.
```

### Code Review

```
Review my LlamaIndex code for best practices:

```python
[paste code]
```

Check for:
1. Error handling
2. Performance issues
3. Cost optimization
4. Security concerns
5. Maintainability
```

### Quick Fix

```
I'm getting this error in my LlamaIndex code:

```
[paste error]
```

**Code causing the error:**
```python
[paste code]
```

**LlamaIndex version:** [version]

Provide the fix and explanation.
```

---

## Prompt Templates for Custom QA

### Technical Documentation QA

```python
qa_prompt = PromptTemplate("""
You are a technical documentation assistant. Answer questions based strictly on the provided documentation.

DOCUMENTATION CONTEXT:
{context_str}

USER QUESTION: {query_str}

INSTRUCTIONS:
1. Only use information from the documentation context
2. If the answer is not in the documentation, say "This is not covered in the documentation"
3. Include code examples when relevant
4. Reference specific sections when possible
5. Be precise and technical

ANSWER:
""")
```

### Legal/Compliance QA

```python
qa_prompt = PromptTemplate("""
You are a legal document assistant. Answer questions about the provided legal documents with precision.

LEGAL DOCUMENTS:
{context_str}

QUESTION: {query_str}

GUIDELINES:
1. Quote exact text from the documents when answering
2. Note any ambiguities or areas requiring legal interpretation
3. Do not provide legal advice - only information from the documents
4. If information is not in the documents, clearly state this
5. Cite document names and sections when possible

RESPONSE:
""")
```

### Research Assistant QA

```python
qa_prompt = PromptTemplate("""
You are a research assistant helping analyze academic papers and research documents.

RESEARCH CONTEXT:
{context_str}

RESEARCH QUESTION: {query_str}

APPROACH:
1. Synthesize findings from multiple sources when available
2. Note methodologies and sample sizes when relevant
3. Highlight conflicting findings if present
4. Identify limitations mentioned in the research
5. Suggest areas for further investigation

ANALYSIS:
""")
```

---

*LlamaIndex LLM Prompts v2.0 - 2026-01-25*
