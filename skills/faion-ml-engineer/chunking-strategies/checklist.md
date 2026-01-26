# Chunking Strategy Checklists

Practical checklists for selecting, implementing, and evaluating chunking strategies.

---

## 1. Strategy Selection Checklist

Use this checklist to choose the right chunking strategy for your use case.

### Document Analysis

- [ ] **Document length assessment**
  - [ ] Short (<1000 tokens): Consider no chunking
  - [ ] Medium (1000-10000 tokens): Standard chunking
  - [ ] Long (>10000 tokens): Hierarchical or multi-pass chunking

- [ ] **Content type identification**
  - [ ] Plain text (articles, blog posts)
  - [ ] Structured text (Markdown, HTML)
  - [ ] Code (Python, JavaScript, etc.)
  - [ ] Mixed content (PDFs with tables, images)
  - [ ] Legal/medical/financial documents

- [ ] **Structure evaluation**
  - [ ] Has clear headers/sections
  - [ ] Has tables and lists
  - [ ] Has code blocks
  - [ ] Has embedded metadata
  - [ ] Uniform density vs. variable density

### Use Case Requirements

- [ ] **Query pattern analysis**
  - [ ] Factual questions (specific answers)
  - [ ] Summarization (broader context needed)
  - [ ] Comparison queries (multiple chunks)
  - [ ] Multi-hop reasoning (cross-references)

- [ ] **Performance requirements**
  - [ ] Latency constraints (real-time vs. batch)
  - [ ] Cost budget (embedding API calls)
  - [ ] Accuracy threshold (precision requirements)

- [ ] **Retrieval setup**
  - [ ] Top-K value (how many chunks retrieved)
  - [ ] Model context window size
  - [ ] Hybrid search requirements

### Strategy Decision Matrix

| Criterion | Fixed | Recursive | Semantic | Structure | Code | Late | Agentic |
|-----------|-------|-----------|----------|-----------|------|------|---------|
| Speed priority | Yes | Yes | - | Yes | - | - | - |
| Cost sensitive | Yes | Yes | - | Yes | - | - | - |
| Quality priority | - | - | Yes | - | - | Yes | Yes |
| Structured docs | - | - | - | Yes | - | - | - |
| Code content | - | - | - | - | Yes | - | - |
| Context critical | - | - | Yes | - | - | Yes | Yes |
| Variable content | - | - | - | - | - | - | Yes |

### Final Selection Checklist

- [ ] Selected strategy matches document type
- [ ] Selected strategy meets performance requirements
- [ ] Have embedding model compatible with strategy
- [ ] Have compute budget for selected strategy
- [ ] Have fallback strategy for edge cases

---

## 2. Implementation Checklist

### Pre-Implementation

- [ ] **Environment setup**
  - [ ] Python 3.10+ installed
  - [ ] Required libraries installed (chonkie, langchain, or llamaindex)
  - [ ] Embedding model API keys configured
  - [ ] Vector database connection verified

- [ ] **Data preparation**
  - [ ] Documents collected and accessible
  - [ ] Document formats validated
  - [ ] Encoding issues addressed (UTF-8)
  - [ ] Special characters handled
  - [ ] Metadata schema defined

- [ ] **Configuration planning**
  - [ ] Chunk size determined (default: 512 tokens)
  - [ ] Overlap percentage set (default: 15%)
  - [ ] Min/max chunk size constraints defined
  - [ ] Separator hierarchy configured (for recursive)
  - [ ] Similarity threshold set (for semantic)

### Implementation Steps

#### Fixed-Size Chunking

- [ ] Define chunk size in tokens (not characters)
- [ ] Set overlap size (10-20% of chunk size)
- [ ] Handle last chunk padding/truncation
- [ ] Test with sample documents
- [ ] Verify token counts are accurate

#### Recursive Chunking

- [ ] Define separator hierarchy
  ```python
  separators = ["\n\n", "\n", ". ", " "]
  ```
- [ ] Set chunk size and overlap
- [ ] Configure length function (token-based recommended)
- [ ] Test with nested content
- [ ] Verify no sentences are cut mid-word

#### Semantic Chunking

- [ ] Select embedding model
- [ ] Configure similarity threshold (0.75-0.85)
- [ ] Set min/max chunk constraints
- [ ] Enable breakpoint detection (percentile or gradient)
- [ ] Consider buffer sentences for context
- [ ] Test with multi-topic documents

#### Document Structure Chunking

- [ ] **For Markdown:**
  - [ ] Define header levels to split on
  - [ ] Configure header inheritance
  - [ ] Handle code blocks separately

- [ ] **For HTML:**
  - [ ] Define tags to split on (section, article, div)
  - [ ] Handle nested structures
  - [ ] Strip unwanted tags

- [ ] **For PDF:**
  - [ ] Use proper PDF parser (unstructured, PyMuPDF)
  - [ ] Handle page boundaries
  - [ ] Extract table content separately

#### Code Chunking

- [ ] Select parsing method (AST, treesitter, regex)
- [ ] Configure language-specific parser
- [ ] Handle import statements (include vs. separate)
- [ ] Preserve docstrings with functions
- [ ] Handle class methods (with or without class context)
- [ ] Set max function size limit

#### Late Chunking

- [ ] Use compatible embedding model (jina-embeddings-v3)
- [ ] Document fits in model context window
- [ ] Configure span boundaries for chunking
- [ ] Set pooling strategy (mean pooling)
- [ ] Test with pronoun-heavy documents

#### Agentic Chunking

- [ ] Select LLM for decisions (GPT-4, Claude)
- [ ] Design decision prompt
- [ ] Configure strategy options
- [ ] Set metadata enrichment rules
- [ ] Implement fallback for LLM failures
- [ ] Set rate limiting for API calls
- [ ] Calculate cost estimates

### Post-Implementation

- [ ] **Validation**
  - [ ] Chunks are within size limits
  - [ ] No empty chunks generated
  - [ ] Metadata attached correctly
  - [ ] Special characters preserved
  - [ ] Encoding is consistent

- [ ] **Logging and monitoring**
  - [ ] Chunk count per document logged
  - [ ] Token distribution tracked
  - [ ] Error handling for edge cases
  - [ ] Processing time recorded

---

## 3. Evaluation Checklist

### Test Dataset Preparation

- [ ] **Create evaluation dataset**
  - [ ] 50-100 representative documents
  - [ ] 100-200 test queries with ground truth
  - [ ] Mix of query types (factual, summary, comparison)
  - [ ] Include edge cases (very long, very short, mixed content)

- [ ] **Define ground truth**
  - [ ] Relevant chunks marked for each query
  - [ ] Expected answer documented
  - [ ] Relevance levels defined (highly relevant, somewhat relevant, not relevant)

### Retrieval Metrics

- [ ] **Precision@K**
  ```
  Precision@K = (Relevant chunks in top-K) / K
  Target: > 0.7 for most use cases
  ```

- [ ] **Recall@K**
  ```
  Recall@K = (Relevant chunks in top-K) / (Total relevant chunks)
  Target: > 0.8 for critical applications
  ```

- [ ] **Mean Reciprocal Rank (MRR)**
  ```
  MRR = Average of (1 / rank of first relevant result)
  Target: > 0.6
  ```

- [ ] **Normalized Discounted Cumulative Gain (NDCG)**
  ```
  NDCG = Measures ranking quality with relevance scores
  Target: > 0.7
  ```

### Chunk Quality Metrics

- [ ] **Chunk size distribution**
  - [ ] Mean chunk size within target range
  - [ ] Standard deviation not too high
  - [ ] No chunks below minimum threshold
  - [ ] No chunks above maximum threshold

- [ ] **Semantic coherence**
  - [ ] Chunks represent complete thoughts
  - [ ] No mid-sentence splits
  - [ ] Topic consistency within chunks

- [ ] **Context preservation**
  - [ ] Pronouns resolvable within chunk
  - [ ] References make sense
  - [ ] No orphaned continuations

### End-to-End Evaluation

- [ ] **Answer quality metrics**
  - [ ] Faithfulness: Answer grounded in retrieved chunks
  - [ ] Relevance: Answer addresses the question
  - [ ] Completeness: Answer includes all necessary info
  - [ ] Conciseness: No unnecessary information

- [ ] **LLM evaluation (RAGAS framework)**
  - [ ] Context precision: Retrieved context is relevant
  - [ ] Context recall: Retrieved context covers answer
  - [ ] Faithfulness: Answer doesn't hallucinate
  - [ ] Answer relevancy: Answer addresses query

### Performance Benchmarks

- [ ] **Latency metrics**
  - [ ] Document chunking time per MB
  - [ ] Embedding generation time per chunk
  - [ ] Retrieval latency per query
  - [ ] End-to-end response time

- [ ] **Cost metrics**
  - [ ] Embedding API calls per document
  - [ ] Storage requirements (vectors + metadata)
  - [ ] LLM calls (for agentic chunking)
  - [ ] Monthly cost projection

### A/B Testing Checklist

- [ ] **Test design**
  - [ ] Define hypothesis (e.g., "Semantic chunking improves precision by 10%")
  - [ ] Select test and control strategies
  - [ ] Determine sample size for significance
  - [ ] Define success metrics

- [ ] **Execution**
  - [ ] Same documents used for both strategies
  - [ ] Same test queries used
  - [ ] Same embedding model used
  - [ ] Same retrieval parameters (top-K)

- [ ] **Analysis**
  - [ ] Statistical significance calculated
  - [ ] Edge cases analyzed
  - [ ] Winner determined with confidence interval
  - [ ] Trade-offs documented

---

## 4. Production Checklist

### Pre-Deployment

- [ ] **Code quality**
  - [ ] Unit tests for chunking functions
  - [ ] Integration tests with vector DB
  - [ ] Error handling for all edge cases
  - [ ] Logging at appropriate levels

- [ ] **Configuration management**
  - [ ] Chunk parameters in config file
  - [ ] Environment-specific settings
  - [ ] Feature flags for strategy switching

- [ ] **Documentation**
  - [ ] API documentation updated
  - [ ] Runbook for common issues
  - [ ] Strategy rationale documented

### Deployment

- [ ] **Infrastructure**
  - [ ] Sufficient compute for chunking load
  - [ ] Vector DB scaled appropriately
  - [ ] Rate limiting on embedding APIs
  - [ ] Caching layer configured

- [ ] **Monitoring**
  - [ ] Chunk size distribution dashboard
  - [ ] Chunking latency alerts
  - [ ] Error rate tracking
  - [ ] Cost tracking per document type

### Post-Deployment

- [ ] **Ongoing evaluation**
  - [ ] Weekly retrieval quality checks
  - [ ] Monthly strategy review
  - [ ] User feedback integration
  - [ ] New document type handling

- [ ] **Maintenance**
  - [ ] Re-chunk documents when strategy changes
  - [ ] Update embeddings when model changes
  - [ ] Archive old chunks appropriately
  - [ ] Version control for chunk configurations

---

## Quick Reference Cards

### Chunk Size Cheat Sheet

| Use Case | Chunk Size | Overlap |
|----------|-----------|---------|
| FAQs | 256 | 0% |
| Technical docs | 512 | 15% |
| Legal documents | 1024 | 20% |
| Code files | Function-based | 0% |
| Research papers | 512-1024 | 15% |

### Strategy Selection Quick Guide

| Speed | Quality | Cost | Strategy |
|-------|---------|------|----------|
| High | Low | Low | Fixed-size |
| High | Medium | Low | Recursive |
| Medium | High | Medium | Semantic |
| Low | Highest | High | Agentic |

### Red Flags During Evaluation

- Precision@5 < 0.5: Strategy too coarse
- Many empty chunks: Parsing issues
- High chunk size variance: Inconsistent splitting
- Low coherence scores: Semantic boundaries not respected
- High latency: Strategy too complex for load
