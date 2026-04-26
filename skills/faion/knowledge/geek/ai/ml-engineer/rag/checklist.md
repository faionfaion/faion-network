# RAG Implementation Checklists

Comprehensive checklists for building, deploying, and maintaining RAG systems.

## Pre-Flight Checklist

### Before Starting RAG Development

- [ ] **Define success criteria**
  - What questions should the system answer?
  - What is acceptable response latency?
  - What accuracy/faithfulness targets?
  - How will you measure success?

- [ ] **Assess data readiness**
  - [ ] Documents are accessible and readable
  - [ ] Documents are in supported formats (PDF, MD, TXT, HTML, DOCX)
  - [ ] Document quality is sufficient (OCR quality, formatting)
  - [ ] Data volume estimated (number of docs, total size)
  - [ ] Update frequency determined (static vs dynamic)

- [ ] **Choose technology stack**
  - [ ] Framework selected (LlamaIndex, LangChain, custom)
  - [ ] Vector database selected (Qdrant, Pinecone, pgvector)
  - [ ] Embedding model selected (OpenAI, Cohere, local)
  - [ ] LLM selected for generation (GPT-4, Claude, Gemini)

- [ ] **Infrastructure planning**
  - [ ] Compute requirements estimated
  - [ ] Storage requirements estimated
  - [ ] API rate limits checked
  - [ ] Cost budget established

---

## Document Ingestion Checklist

### Phase 1: Document Collection

- [ ] **Gather source documents**
  - [ ] Identify all document sources
  - [ ] Establish access permissions
  - [ ] Create document inventory
  - [ ] Plan update schedule

- [ ] **Document preprocessing**
  - [ ] Remove duplicate documents
  - [ ] Filter out low-quality documents
  - [ ] Standardize file formats if needed
  - [ ] Extract text from PDFs/images (OCR if needed)

### Phase 2: Document Cleaning

- [ ] **Text cleaning**
  - [ ] Remove headers/footers/page numbers
  - [ ] Remove boilerplate text
  - [ ] Fix encoding issues
  - [ ] Normalize whitespace

- [ ] **Structure preservation**
  - [ ] Maintain heading hierarchy
  - [ ] Preserve lists and tables
  - [ ] Keep code blocks intact
  - [ ] Retain important formatting

### Phase 3: Metadata Extraction

- [ ] **Core metadata**
  - [ ] Source filename
  - [ ] Document title
  - [ ] Creation/modification date
  - [ ] Author (if available)

- [ ] **Custom metadata**
  - [ ] Document type/category
  - [ ] Department/team
  - [ ] Version number
  - [ ] Access level/permissions

---

## Chunking Strategy Checklist

### Choosing a Chunking Strategy

- [ ] **Assess document types**
  - [ ] Structured (Markdown, HTML) → Structure-aware chunking
  - [ ] Unstructured (plain text) → Recursive or semantic chunking
  - [ ] Technical docs → Preserve code blocks
  - [ ] Legal/formal → Preserve clauses and sections

- [ ] **Determine chunk parameters**
  - [ ] Chunk size (tokens): 256-512 for precision, 512-1024 for context
  - [ ] Chunk overlap: 10-20% of chunk size
  - [ ] Separator hierarchy (paragraphs → sentences → words)

### Chunking Quality Validation

- [ ] **Chunk coherence check**
  - [ ] Chunks contain complete thoughts
  - [ ] No sentences split mid-way
  - [ ] Code blocks not fragmented
  - [ ] Tables not split across chunks

- [ ] **Chunk size distribution**
  - [ ] Review size histogram
  - [ ] Check for outliers (too small/large)
  - [ ] Verify overlap is applied correctly

---

## Vector Index Checklist

### Index Creation

- [ ] **Embedding configuration**
  - [ ] Embedding model selected and tested
  - [ ] Batch size configured for efficiency
  - [ ] Embedding dimensions confirmed
  - [ ] Normalize embeddings if required

- [ ] **Vector store setup**
  - [ ] Collection/index created
  - [ ] Schema defined with metadata fields
  - [ ] Distance metric selected (cosine, dot product, euclidean)
  - [ ] Index parameters configured (HNSW ef, m values)

- [ ] **Indexing execution**
  - [ ] Progress monitoring enabled
  - [ ] Error handling for failed embeddings
  - [ ] Batch processing for large datasets
  - [ ] Checkpointing for resumability

### Index Verification

- [ ] **Basic validation**
  - [ ] Total document count matches expected
  - [ ] Vector count matches chunk count
  - [ ] Metadata searchable and correct
  - [ ] Sample queries return relevant results

- [ ] **Performance testing**
  - [ ] Query latency acceptable (<100ms)
  - [ ] Memory usage within limits
  - [ ] Concurrent query handling works

---

## Retrieval Configuration Checklist

### Basic Retrieval Setup

- [ ] **Retriever configuration**
  - [ ] top-k value determined (start with 10, tune later)
  - [ ] Similarity threshold set if applicable
  - [ ] Metadata filters configured
  - [ ] Query preprocessing enabled

### Advanced Retrieval Setup

- [ ] **Hybrid search** (if needed)
  - [ ] BM25 retriever configured
  - [ ] Vector retriever configured
  - [ ] Fusion weights set (40% keyword, 60% semantic typical)
  - [ ] Reciprocal rank fusion or other fusion method selected

- [ ] **Reranking** (recommended for production)
  - [ ] Reranker model selected
  - [ ] Initial retrieval top-k increased (e.g., 20)
  - [ ] Final top-k after reranking set (e.g., 5)
  - [ ] Latency impact measured

- [ ] **Query enhancement** (optional)
  - [ ] Query expansion enabled
  - [ ] Multi-query generation configured
  - [ ] HyDE (Hypothetical Document Embeddings) considered

---

## Generation Configuration Checklist

### Prompt Engineering

- [ ] **System prompt defined**
  - [ ] Role and purpose clear
  - [ ] Source-only constraint included
  - [ ] Citation format specified
  - [ ] Uncertainty handling instructions

- [ ] **Context injection**
  - [ ] Context template created
  - [ ] Source metadata included
  - [ ] Max context length configured
  - [ ] Truncation strategy defined

### LLM Configuration

- [ ] **Model selection**
  - [ ] Model chosen for quality/cost balance
  - [ ] Temperature set (0-0.3 for factual RAG)
  - [ ] Max tokens configured
  - [ ] Stop sequences defined if needed

- [ ] **Response synthesis**
  - [ ] Synthesis mode selected (compact, refine, tree)
  - [ ] Streaming enabled if needed
  - [ ] Error handling for API failures

---

## Evaluation Checklist

### Test Dataset Creation

- [ ] **Query dataset**
  - [ ] Representative queries collected (50-100 minimum)
  - [ ] Query categories identified (simple, complex, multi-hop)
  - [ ] Edge cases included (out-of-scope, ambiguous)
  - [ ] Ground truth answers available

- [ ] **Relevance judgments**
  - [ ] Relevant documents identified per query
  - [ ] Relevance grades assigned (binary or graded)
  - [ ] Multiple annotators if possible

### Retrieval Evaluation

- [ ] **Metrics computed**
  - [ ] Recall@k (target: >0.8)
  - [ ] Precision@k
  - [ ] MRR (target: >0.7)
  - [ ] NDCG@k

- [ ] **Error analysis**
  - [ ] Failed retrievals reviewed
  - [ ] False positives analyzed
  - [ ] Query reformulation tested

### Generation Evaluation

- [ ] **Automated metrics**
  - [ ] Faithfulness (target: >0.9)
  - [ ] Answer relevancy (target: >0.8)
  - [ ] Context precision (target: >0.7)
  - [ ] Context recall (target: >0.8)

- [ ] **Human evaluation**
  - [ ] Correctness ratings collected
  - [ ] Helpfulness ratings collected
  - [ ] Citation accuracy verified

---

## Production Readiness Checklist

### Performance Requirements

- [ ] **Latency**
  - [ ] End-to-end latency <3 seconds
  - [ ] Retrieval latency <500ms
  - [ ] Generation streaming enabled
  - [ ] Cold start time acceptable

- [ ] **Throughput**
  - [ ] Concurrent request handling tested
  - [ ] Rate limiting implemented
  - [ ] Queue management for spikes

### Reliability Requirements

- [ ] **Error handling**
  - [ ] API failure recovery
  - [ ] Timeout handling
  - [ ] Graceful degradation
  - [ ] Retry logic with backoff

- [ ] **Monitoring**
  - [ ] Latency metrics tracked
  - [ ] Error rates monitored
  - [ ] Usage patterns logged
  - [ ] Anomaly detection configured

### Security Requirements

- [ ] **Data protection**
  - [ ] No sensitive data in logs
  - [ ] API keys secured
  - [ ] Access controls implemented
  - [ ] Data encryption at rest and in transit

- [ ] **Input validation**
  - [ ] Query sanitization
  - [ ] Injection prevention
  - [ ] Length limits enforced

### Operational Requirements

- [ ] **Documentation**
  - [ ] Architecture documented
  - [ ] Runbooks created
  - [ ] Troubleshooting guides written
  - [ ] API documentation complete

- [ ] **Maintenance plan**
  - [ ] Index update strategy defined
  - [ ] Backup and recovery tested
  - [ ] Rollback procedure documented
  - [ ] On-call rotation established

---

## Index Update Checklist

### Incremental Updates

- [ ] **Document change detection**
  - [ ] New documents identified
  - [ ] Modified documents identified
  - [ ] Deleted documents identified
  - [ ] Change timestamps tracked

- [ ] **Update execution**
  - [ ] New documents chunked and embedded
  - [ ] Modified documents re-chunked
  - [ ] Old chunks deleted
  - [ ] Metadata updated

- [ ] **Verification**
  - [ ] Document counts verified
  - [ ] Sample queries tested
  - [ ] No regression in quality

### Full Re-indexing

- [ ] **Preparation**
  - [ ] New index created (parallel to production)
  - [ ] All documents re-processed
  - [ ] Quality validated on new index

- [ ] **Cutover**
  - [ ] Index alias updated
  - [ ] Old index retained temporarily
  - [ ] Rollback tested
  - [ ] Old index deleted after validation

---

## Troubleshooting Checklist

### Poor Retrieval Quality

- [ ] Check chunk size (too large dilutes, too small loses context)
- [ ] Check chunk overlap (missing context at boundaries)
- [ ] Verify embedding model quality
- [ ] Test hybrid search if not enabled
- [ ] Enable reranking
- [ ] Check for data quality issues

### Poor Generation Quality

- [ ] Check if relevant context is retrieved (retrieval vs generation issue)
- [ ] Review prompt engineering
- [ ] Lower temperature for more factual responses
- [ ] Increase top-k for more context
- [ ] Check for conflicting information in context
- [ ] Verify LLM model choice

### High Latency

- [ ] Profile each pipeline stage
- [ ] Reduce top-k if over-retrieving
- [ ] Enable caching for embeddings
- [ ] Use faster embedding model
- [ ] Pre-filter with metadata
- [ ] Optimize vector index (HNSW parameters)

### High Costs

- [ ] Reduce embedding dimensions
- [ ] Use cheaper embedding model
- [ ] Cache embeddings and query results
- [ ] Batch embedding requests
- [ ] Use smaller LLM for simple queries
- [ ] Implement query result caching

---

## Weekly Maintenance Checklist

- [ ] Review error logs
- [ ] Check latency metrics
- [ ] Validate retrieval quality on sample queries
- [ ] Update documents if needed
- [ ] Review and address user feedback
- [ ] Check for framework/model updates
- [ ] Verify backup integrity
- [ ] Update evaluation dataset if needed
