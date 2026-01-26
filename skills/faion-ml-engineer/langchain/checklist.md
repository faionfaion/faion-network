# LangChain Checklists

Comprehensive checklists for LangChain/LangGraph project setup, design, deployment, and security.

---

## Project Setup Checklist

### Environment Setup

- [ ] **Python Environment**
  - [ ] Python 3.11+ installed
  - [ ] Virtual environment created (`venv`, `conda`, `poetry`)
  - [ ] pip/poetry configured

- [ ] **Core Packages Installed**
  ```bash
  pip install langchain langchain-core langchain-community
  pip install langgraph
  pip install langsmith
  ```

- [ ] **Provider Packages (as needed)**
  - [ ] `langchain-openai` for OpenAI
  - [ ] `langchain-anthropic` for Claude
  - [ ] `langchain-google-genai` for Gemini
  - [ ] `langchain-ollama` for local models

- [ ] **Vector Store Packages (for RAG)**
  - [ ] `langchain-chroma` for development
  - [ ] `langchain-qdrant` / `langchain-pinecone` / `langchain-weaviate` for production

### API Keys and Configuration

- [ ] **LLM API Keys**
  - [ ] `OPENAI_API_KEY` set (if using OpenAI)
  - [ ] `ANTHROPIC_API_KEY` set (if using Claude)
  - [ ] `GOOGLE_API_KEY` set (if using Gemini)

- [ ] **Observability**
  - [ ] `LANGCHAIN_TRACING_V2=true`
  - [ ] `LANGCHAIN_API_KEY` set (LangSmith)
  - [ ] `LANGCHAIN_PROJECT` named appropriately

- [ ] **Environment Management**
  - [ ] `.env` file created
  - [ ] `.env` added to `.gitignore`
  - [ ] `python-dotenv` installed for loading

### Project Structure

- [ ] **Directory Structure Created**
  ```
  project/
  ├── src/
  │   ├── chains/           # LCEL chains
  │   ├── agents/           # LangGraph agents
  │   ├── tools/            # Custom tools
  │   ├── prompts/          # Prompt templates
  │   └── utils/            # Helpers
  ├── tests/
  ├── .env
  └── requirements.txt
  ```

- [ ] **Configuration Files**
  - [ ] `pyproject.toml` or `setup.py`
  - [ ] `requirements.txt` or `poetry.lock`
  - [ ] `.env.example` with placeholder keys

### Development Tools

- [ ] **Code Quality**
  - [ ] Linter configured (ruff, flake8)
  - [ ] Formatter configured (black, ruff)
  - [ ] Type checker configured (mypy, pyright)

- [ ] **Testing**
  - [ ] pytest installed
  - [ ] Test structure created
  - [ ] Mock strategies planned

---

## Chain Design Checklist

### Requirements Analysis

- [ ] **Input/Output Definition**
  - [ ] Input schema defined (Pydantic model)
  - [ ] Output schema defined (Pydantic model)
  - [ ] Error cases identified

- [ ] **Flow Design**
  - [ ] Sequential vs parallel identified
  - [ ] Conditional logic mapped
  - [ ] Error handling planned

### Prompt Engineering

- [ ] **System Message**
  - [ ] Clear role defined
  - [ ] Constraints specified
  - [ ] Output format described

- [ ] **User Message Template**
  - [ ] All variables identified
  - [ ] Examples included (if few-shot)
  - [ ] Edge cases handled

- [ ] **Prompt Testing**
  - [ ] Tested with diverse inputs
  - [ ] Edge cases validated
  - [ ] Output consistency verified

### Chain Implementation

- [ ] **Components Selected**
  - [ ] Appropriate model chosen (cost vs quality)
  - [ ] Output parser selected (Str, JSON, Structured)
  - [ ] Memory type chosen (if needed)

- [ ] **LCEL Chain Built**
  - [ ] `prompt | model | parser` pattern used
  - [ ] Streaming supported (if needed)
  - [ ] Async supported (if needed)

- [ ] **Error Handling**
  - [ ] `.with_retry()` added for transient failures
  - [ ] `.with_fallbacks()` for model redundancy
  - [ ] Custom error handling where needed

### Chain Validation

- [ ] **Functionality Testing**
  - [ ] Happy path works
  - [ ] Edge cases handled
  - [ ] Error cases graceful

- [ ] **Performance Testing**
  - [ ] Latency acceptable
  - [ ] Token usage reasonable
  - [ ] Cost within budget

- [ ] **Observability**
  - [ ] Traces appear in LangSmith
  - [ ] Metadata tags added
  - [ ] Custom callbacks (if needed)

---

## Agent Design Checklist

### Architecture Selection

- [ ] **Agent Type Determined**
  - [ ] ReAct for simple tool use
  - [ ] Plan-and-Execute for multi-step
  - [ ] Supervisor for multi-agent
  - [ ] Custom LangGraph for complex flows

- [ ] **Control Flow Designed**
  - [ ] State schema defined (TypedDict)
  - [ ] Nodes identified
  - [ ] Edges mapped (conditional vs direct)
  - [ ] Entry/exit points defined

### Tool Design

- [ ] **Tools Identified**
  - [ ] Required capabilities listed
  - [ ] Existing tools reviewed
  - [ ] Custom tools planned

- [ ] **Tool Implementation**
  - [ ] `@tool` decorator used
  - [ ] Docstring describes function (LLM reads this!)
  - [ ] Input validation included
  - [ ] Error handling implemented
  - [ ] Return types are strings (for LLM consumption)

- [ ] **Tool Testing**
  - [ ] Each tool tested independently
  - [ ] Error cases handled
  - [ ] Response format verified

### LangGraph Implementation

- [ ] **State Definition**
  - [ ] TypedDict with all fields
  - [ ] Annotated fields for accumulators
  - [ ] Optional fields marked

- [ ] **Nodes Implemented**
  - [ ] Each node returns partial state update
  - [ ] Node functions are pure (no side effects on state)
  - [ ] Error handling in each node

- [ ] **Edges Configured**
  - [ ] Entry point set
  - [ ] Direct edges added
  - [ ] Conditional edges with routing functions
  - [ ] END node reachable from all paths

- [ ] **Checkpointing (if needed)**
  - [ ] MemorySaver for development
  - [ ] Production checkpointer selected (PostgreSQL, Redis)
  - [ ] Thread ID strategy defined

### Agent Validation

- [ ] **Flow Testing**
  - [ ] All paths exercised
  - [ ] Tool calls verified
  - [ ] State transitions correct

- [ ] **Edge Case Testing**
  - [ ] Tool failures handled
  - [ ] Max iterations enforced
  - [ ] Infinite loops prevented

- [ ] **Human-in-the-Loop (if needed)**
  - [ ] Interrupt points defined
  - [ ] Resume logic tested
  - [ ] State persistence verified

---

## RAG Implementation Checklist

### Document Processing

- [ ] **Document Loading**
  - [ ] Loaders selected (PDF, web, etc.)
  - [ ] Metadata extraction planned
  - [ ] Error handling for corrupt files

- [ ] **Chunking Strategy**
  - [ ] Chunk size determined (500-1000 tokens typical)
  - [ ] Overlap size set (10-20% typical)
  - [ ] Splitter selected (recursive, semantic, etc.)

- [ ] **Metadata**
  - [ ] Source tracking implemented
  - [ ] Document ID assigned
  - [ ] Custom metadata added

### Vector Store

- [ ] **Store Selection**
  - [ ] Chroma for development
  - [ ] Production store selected
  - [ ] Hosting/self-hosted decided

- [ ] **Embedding Model**
  - [ ] Model selected (OpenAI, Cohere, local)
  - [ ] Dimension size noted
  - [ ] Batch processing configured

- [ ] **Index Configuration**
  - [ ] Index created
  - [ ] Similarity metric chosen (cosine typical)
  - [ ] HNSW parameters tuned (if applicable)

### Retrieval

- [ ] **Retriever Configuration**
  - [ ] k (top results) set appropriately
  - [ ] Score threshold considered
  - [ ] Filters configured

- [ ] **Advanced Retrieval (if needed)**
  - [ ] Hybrid search (keyword + semantic)
  - [ ] Reranking model
  - [ ] Multi-query retrieval
  - [ ] Contextual compression

### RAG Chain

- [ ] **Prompt Design**
  - [ ] Context injection template
  - [ ] Source attribution instructions
  - [ ] "I don't know" handling

- [ ] **Chain Assembly**
  - [ ] Retriever -> Format -> LLM -> Parse
  - [ ] Streaming supported
  - [ ] Sources returned with answer

---

## Production Deployment Checklist

### Pre-Deployment

- [ ] **Code Review**
  - [ ] All prompts reviewed for injection risks
  - [ ] API keys not hardcoded
  - [ ] Error handling comprehensive

- [ ] **Testing Complete**
  - [ ] Unit tests passing
  - [ ] Integration tests passing
  - [ ] Load testing performed

- [ ] **Documentation**
  - [ ] API documentation complete
  - [ ] Prompt documentation updated
  - [ ] Runbook created

### Infrastructure

- [ ] **Compute**
  - [ ] Server/serverless selected
  - [ ] Memory requirements met
  - [ ] CPU/GPU requirements met

- [ ] **Scaling**
  - [ ] Horizontal scaling configured
  - [ ] Rate limiting implemented
  - [ ] Queue for async tasks (if needed)

- [ ] **Storage**
  - [ ] Vector store provisioned
  - [ ] Checkpointer storage provisioned
  - [ ] Cache storage provisioned

### Configuration

- [ ] **Environment Variables**
  - [ ] All secrets in environment/secrets manager
  - [ ] No defaults for sensitive values
  - [ ] Validation on startup

- [ ] **Model Configuration**
  - [ ] Production model selected
  - [ ] Fallback models configured
  - [ ] Temperature/parameters finalized

- [ ] **Limits and Quotas**
  - [ ] Max tokens per request set
  - [ ] Max concurrent requests set
  - [ ] Rate limits configured

### Observability

- [ ] **Logging**
  - [ ] Structured logging configured
  - [ ] Log levels appropriate
  - [ ] Sensitive data not logged

- [ ] **Tracing**
  - [ ] LangSmith connected (or alternative)
  - [ ] Project/tags configured
  - [ ] Sampling for high-volume

- [ ] **Metrics**
  - [ ] Latency tracked
  - [ ] Token usage tracked
  - [ ] Cost tracked
  - [ ] Error rates tracked

- [ ] **Alerting**
  - [ ] Error rate alerts
  - [ ] Latency alerts
  - [ ] Cost alerts
  - [ ] API quota alerts

### Post-Deployment

- [ ] **Smoke Tests**
  - [ ] Basic functionality verified
  - [ ] All integrations working
  - [ ] Monitoring receiving data

- [ ] **Rollback Plan**
  - [ ] Previous version available
  - [ ] Rollback procedure documented
  - [ ] Team trained on rollback

---

## Security Checklist

### API Key Security

- [ ] **Storage**
  - [ ] Keys in secrets manager (not env files in production)
  - [ ] Keys rotated regularly
  - [ ] Separate keys for dev/staging/prod

- [ ] **Access Control**
  - [ ] Principle of least privilege
  - [ ] Keys scoped to necessary permissions
  - [ ] Usage monitored

### Prompt Injection Prevention

- [ ] **Input Validation**
  - [ ] User input sanitized
  - [ ] Length limits enforced
  - [ ] Special characters handled

- [ ] **Prompt Design**
  - [ ] System/user message separation
  - [ ] Instructions in system message
  - [ ] Clear delimiters for user content

- [ ] **Output Validation**
  - [ ] Structured output when possible
  - [ ] Output sanitized before use
  - [ ] No direct execution of LLM output

### Data Security

- [ ] **PII Handling**
  - [ ] PII identified and classified
  - [ ] PII masked/removed before LLM
  - [ ] Retention policies applied

- [ ] **Data in Transit**
  - [ ] HTTPS enforced
  - [ ] TLS 1.2+ required
  - [ ] Certificate validation enabled

- [ ] **Data at Rest**
  - [ ] Vector store encrypted
  - [ ] Checkpoints encrypted
  - [ ] Logs don't contain sensitive data

### Access Control

- [ ] **Authentication**
  - [ ] API authentication required
  - [ ] Token validation implemented
  - [ ] Session management secure

- [ ] **Authorization**
  - [ ] Role-based access implemented
  - [ ] Resource-level permissions
  - [ ] Audit logging enabled

### Compliance (if applicable)

- [ ] **Data Residency**
  - [ ] LLM API region known
  - [ ] Vector store region appropriate
  - [ ] Data doesn't cross restricted boundaries

- [ ] **Audit Trail**
  - [ ] All queries logged
  - [ ] User actions attributed
  - [ ] Retention period defined

- [ ] **Third-Party Assessment**
  - [ ] LLM provider compliance reviewed
  - [ ] Vector store provider compliance reviewed
  - [ ] DPA signed (if required)

---

## Performance Optimization Checklist

### Latency Optimization

- [ ] **Model Selection**
  - [ ] Smallest effective model used
  - [ ] Streaming enabled for UX
  - [ ] Response caching implemented

- [ ] **Parallel Execution**
  - [ ] Independent operations parallelized
  - [ ] RunnableParallel used appropriately
  - [ ] Batch operations where possible

- [ ] **Network**
  - [ ] Closest API region selected
  - [ ] Connection pooling enabled
  - [ ] Keep-alive configured

### Cost Optimization

- [ ] **Token Management**
  - [ ] Prompt length minimized
  - [ ] Context window managed
  - [ ] Conversation history summarized

- [ ] **Model Tiering**
  - [ ] Simple tasks -> cheap models
  - [ ] Complex tasks -> capable models
  - [ ] Router pattern implemented

- [ ] **Caching**
  - [ ] Semantic cache for common queries
  - [ ] Embedding cache for documents
  - [ ] Response cache for deterministic queries

### Reliability Optimization

- [ ] **Retry Configuration**
  - [ ] Exponential backoff
  - [ ] Jitter added
  - [ ] Max retries limited

- [ ] **Fallback Strategy**
  - [ ] Primary model selected
  - [ ] Fallback models configured
  - [ ] Graceful degradation designed

- [ ] **Circuit Breaker**
  - [ ] Failure threshold set
  - [ ] Recovery time defined
  - [ ] Alternative path available

---

## Testing Checklist

### Unit Testing

- [ ] **Prompt Tests**
  - [ ] Template rendering verified
  - [ ] Variable injection correct
  - [ ] Format instructions present

- [ ] **Tool Tests**
  - [ ] Each tool tested in isolation
  - [ ] Input validation tested
  - [ ] Error handling tested

- [ ] **Parser Tests**
  - [ ] Valid output parsed correctly
  - [ ] Invalid output handled gracefully
  - [ ] Edge cases covered

### Integration Testing

- [ ] **Chain Integration**
  - [ ] Full chain executes
  - [ ] Components interact correctly
  - [ ] Error propagation works

- [ ] **Agent Integration**
  - [ ] Tool calls execute
  - [ ] State transitions work
  - [ ] Checkpointing works

- [ ] **External Services**
  - [ ] Vector store operations work
  - [ ] LLM API calls work
  - [ ] Memory persistence works

### End-to-End Testing

- [ ] **Happy Path**
  - [ ] Common use cases work
  - [ ] Expected output produced
  - [ ] Performance acceptable

- [ ] **Edge Cases**
  - [ ] Empty input handled
  - [ ] Long input handled
  - [ ] Malformed input handled

- [ ] **Failure Scenarios**
  - [ ] API timeout handled
  - [ ] Rate limit handled
  - [ ] Invalid response handled

### Mocking Strategy

- [ ] **LLM Mocking**
  - [ ] Deterministic responses for tests
  - [ ] Tool call mocking
  - [ ] Streaming mocking

- [ ] **External Service Mocking**
  - [ ] Vector store mocked
  - [ ] External APIs mocked
  - [ ] File system mocked

---

*Checklists v2.0 - LangChain 1.0+ / LangGraph 1.0+*
