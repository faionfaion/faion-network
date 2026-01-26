# LLM Prompts for Gemini API

Prompts for AI assistants to help with Gemini API implementation.

---

## Table of Contents

1. [Setup & Configuration](#setup--configuration)
2. [Chat Implementation](#chat-implementation)
3. [Multimodal Processing](#multimodal-processing)
4. [Function Calling](#function-calling)
5. [Live API Integration](#live-api-integration)
6. [RAG Implementation](#rag-implementation)
7. [Optimization](#optimization)
8. [Troubleshooting](#troubleshooting)

---

## Setup & Configuration

### Initialize Gemini Project

```
I need to set up a Gemini API project with:

Requirements:
- Model: [gemini-3-pro / gemini-2.0-flash / gemini-1.5-pro]
- Features: [chat / multimodal / function calling / streaming]
- Environment: [Python / Node.js / FastAPI / Next.js]

Please provide:
1. Required dependencies (pip/npm)
2. Environment variable setup
3. Basic initialization code
4. Error handling setup
5. Rate limiting configuration
```

### Choose Model

```
Help me choose the right Gemini model for my use case:

Use case: [describe your application]
Requirements:
- Latency: [low / medium / not critical]
- Context length needed: [short / medium / long / very long]
- Reasoning complexity: [simple / moderate / complex]
- Budget: [low / medium / high]
- Multimodal: [yes / no]

Please recommend the best model and configuration.
```

### Configure Generation Parameters

```
Configure Gemini generation parameters for my use case:

Task type: [creative writing / code generation / data extraction / chat / analysis]
Output requirements:
- Format: [text / JSON / structured]
- Length: [short / medium / long]
- Creativity level: [deterministic / balanced / creative]

Provide the optimal generation_config settings with explanations.
```

---

## Chat Implementation

### Build Chatbot

```
Build a Gemini-powered chatbot with:

Requirements:
- System instruction: [describe persona/behavior]
- Memory: [in-memory / Redis / database]
- Streaming: [yes / no]
- Framework: [standalone / FastAPI / Flask / Express]

Features needed:
- [ ] Conversation history
- [ ] Session management
- [ ] Streaming responses
- [ ] Error recovery
- [ ] Rate limiting

Provide complete implementation with best practices.
```

### Add System Instruction

```
Create an effective system instruction for Gemini:

Chatbot purpose: [describe what the bot should do]
Personality: [professional / friendly / technical / casual]
Constraints:
- Topics to focus on: [list]
- Topics to avoid: [list]
- Response style: [concise / detailed / structured]
- Languages: [list]

Generate the system_instruction string and explain the design choices.
```

### Implement Chat Memory

```
Implement chat memory/history management for Gemini:

Requirements:
- Storage: [in-memory / Redis / PostgreSQL / MongoDB]
- Context window management: [truncate / summarize / sliding window]
- Multi-session support: [yes / no]
- Persistence: [session-only / permanent]

Provide implementation with:
1. History storage/retrieval
2. Context window management
3. Session cleanup
4. Thread-safe operations (if applicable)
```

---

## Multimodal Processing

### Image Analysis System

```
Build an image analysis system with Gemini:

Use case: [product recognition / OCR / medical / general analysis]
Input sources:
- [ ] Local files
- [ ] URLs
- [ ] Base64 encoded
- [ ] Live camera

Output requirements:
- [ ] Description
- [ ] Object detection
- [ ] Text extraction
- [ ] Custom attributes

Provide complete implementation with error handling.
```

### Video Processing Pipeline

```
Create a video processing pipeline with Gemini:

Requirements:
- Video sources: [local files / URLs / streaming]
- Processing tasks:
  - [ ] Summarization
  - [ ] Transcription
  - [ ] Scene detection
  - [ ] Timestamp queries
- Output format: [text / JSON / structured]

Include:
1. Upload and processing status handling
2. Chunking for long videos
3. Error recovery
4. Progress tracking
```

### Document Processing

```
Build a document processing system:

Document types:
- [ ] PDFs
- [ ] Images (scanned docs)
- [ ] Presentations
- [ ] Spreadsheets

Processing tasks:
- [ ] Summarization
- [ ] Information extraction
- [ ] Q&A
- [ ] Structured data extraction

Output: [text / JSON schema / database records]

Provide implementation with caching for repeated queries.
```

---

## Function Calling

### Define Function Schema

```
Create Gemini function declarations for these capabilities:

Functions needed:
1. [function_name]: [description]
   - Input: [parameters]
   - Output: [expected return]

2. [function_name]: [description]
   - Input: [parameters]
   - Output: [expected return]

Requirements:
- Tool config mode: [AUTO / ANY / VALIDATED]
- Parallel calling: [yes / no]
- Error handling: [describe]

Generate:
1. Function declarations with proper schemas
2. Implementation stubs
3. Response handling code
4. Error handling patterns
```

### Build Agent with Tools

```
Build an AI agent with the following tools:

Tools:
1. [tool_name]: [what it does]
2. [tool_name]: [what it does]
3. [tool_name]: [what it does]

Agent requirements:
- Max iterations: [number]
- Fallback behavior: [describe]
- Logging: [yes / no]
- Human-in-the-loop: [yes / no]

Provide:
1. Complete agent implementation
2. Tool registry
3. Execution loop
4. Error handling and recovery
```

### Multimodal Function Responses (Gemini 3)

```
Implement function calling with multimodal responses for Gemini 3:

Use case: [describe scenario where function returns images/files]

Requirements:
- Function output includes: [images / PDFs / charts]
- Response format: [base64 / file reference]
- Error handling for media processing

Provide implementation showing:
1. Function definition
2. Execution with media return
3. Sending multimodal response to Gemini
4. Processing model's interpretation
```

---

## Live API Integration

### Real-time Voice Chat

```
Implement real-time voice chat with Gemini Live API:

Requirements:
- Audio input: [microphone / file / stream]
- Audio output: [speaker / file / stream]
- Platform: [desktop / web / mobile]
- Language: [Python / JavaScript]

Features:
- [ ] Voice activity detection
- [ ] Interrupt handling
- [ ] Session persistence
- [ ] Function calling during conversation

Provide complete implementation with audio handling.
```

### Live API with Video

```
Implement video streaming with Gemini Live API:

Requirements:
- Video source: [webcam / screen share / file]
- Audio: [microphone / none]
- Use case: [describe what you want to analyze]

Include:
1. Video capture setup
2. Frame processing
3. Bidirectional communication
4. Response handling
```

### Ephemeral Tokens for Client-side

```
Implement secure client-side Live API access:

Architecture:
- Server: [Node.js / Python / Go]
- Client: [browser / mobile app]

Requirements:
- Token refresh strategy
- Error handling for token expiry
- Fallback to server-side if needed

Provide:
1. Server endpoint for token generation
2. Client-side token management
3. Reconnection logic
```

---

## RAG Implementation

### Build RAG System

```
Build a RAG system with Gemini:

Requirements:
- Document types: [PDF / text / web pages]
- Vector store: [Chroma / Pinecone / Qdrant / pgvector]
- Embedding model: text-embedding-004
- Chunking strategy: [fixed / semantic / recursive]

Features:
- [ ] Hybrid search (vector + keyword)
- [ ] Reranking
- [ ] Context caching
- [ ] Citation generation

Provide complete implementation with:
1. Document processing pipeline
2. Indexing logic
3. Query handling
4. Response generation with citations
```

### Optimize RAG Retrieval

```
Optimize my RAG retrieval for Gemini:

Current issues:
- [describe problems: irrelevant results, missing context, etc.]

Current setup:
- Chunk size: [number]
- Overlap: [number]
- Top-k: [number]
- Vector DB: [name]

Provide optimizations for:
1. Chunking strategy
2. Embedding configuration
3. Search parameters
4. Prompt engineering for RAG
```

### Context Caching for RAG

```
Implement context caching for my RAG system:

Scenario:
- Knowledge base size: [estimate tokens]
- Query frequency: [high / medium / low]
- Update frequency: [daily / weekly / rarely]

Requirements:
- Cache TTL strategy
- Cache invalidation
- Cost optimization

Provide implementation with:
1. Cache creation
2. Query using cached context
3. Cache management (update, delete)
4. Cost comparison analysis
```

---

## Optimization

### Cost Optimization

```
Optimize Gemini API costs for my application:

Current usage:
- Model: [name]
- Monthly requests: [number]
- Average input tokens: [number]
- Average output tokens: [number]
- Use case: [description]

Constraints:
- Quality requirements: [high / medium / flexible]
- Latency requirements: [strict / flexible]

Provide optimization strategies for:
1. Model selection
2. Prompt optimization
3. Caching strategy
4. Batching opportunities
5. Cost projections
```

### Performance Optimization

```
Optimize Gemini API performance:

Current bottlenecks:
- [describe: latency, throughput, etc.]

Application type: [real-time chat / batch processing / API]
Scale: [requests/minute]

Optimize for:
1. Latency reduction
2. Throughput improvement
3. Concurrent request handling
4. Streaming implementation
```

### Prompt Engineering

```
Optimize my Gemini prompts:

Current prompt:
```
[paste your current prompt]
```

Issues:
- [describe problems]

Goals:
- [what you want to achieve]

Output format requirements:
- [describe expected format]

Provide:
1. Optimized prompt
2. Explanation of changes
3. Few-shot examples if helpful
4. Testing suggestions
```

---

## Troubleshooting

### Debug Generation Issues

```
Help me debug Gemini generation issues:

Problem:
- [describe the issue: unexpected output, errors, safety blocks, etc.]

Current code:
```python
[paste relevant code]
```

Error message (if any):
```
[paste error]
```

Model: [name]
Parameters: [list your generation_config]

Help me:
1. Identify the root cause
2. Suggest fixes
3. Add proper error handling
```

### Handle Rate Limits

```
Implement robust rate limit handling for Gemini:

Current usage:
- Requests per minute: [number]
- Model tier: [free / pay-as-you-go]
- Peak traffic patterns: [describe]

Requirements:
- Graceful degradation
- Queue management
- User feedback
- Monitoring

Provide implementation with:
1. Retry logic with exponential backoff
2. Request queuing
3. Circuit breaker pattern
4. Alerting setup
```

### Safety Blocking Issues

```
Resolve Gemini safety blocking issues:

Problem:
- Legitimate content being blocked
- Use case: [describe your use case]

Current safety settings:
```python
[paste current settings]
```

Blocked content example:
```
[describe what's being blocked, without including harmful content]
```

Help me:
1. Understand why blocking occurs
2. Adjust safety settings appropriately
3. Reframe prompts to avoid false positives
4. Handle blocked responses gracefully
```

### Token Limit Issues

```
Handle Gemini token limit issues:

Problem:
- [context too long / output truncated / etc.]

Current setup:
- Model: [name]
- Context window: [size]
- Input size: [estimate]
- Output needs: [estimate]

Help me:
1. Measure actual token usage
2. Implement context management
3. Use context caching if appropriate
4. Split long content effectively
```

---

## Meta Prompts

### Generate Project Scaffold

```
Generate a complete Gemini API project scaffold:

Project type: [chatbot / RAG / agent / multimodal / API]
Tech stack:
- Backend: [Python/FastAPI, Node/Express, etc.]
- Frontend: [if applicable]
- Database: [if applicable]

Features:
- [ ] [list features]

Provide:
1. Project structure
2. Configuration files
3. Core modules
4. Example usage
5. Tests
6. Docker setup
```

### Review Implementation

```
Review my Gemini API implementation:

```python
[paste your code]
```

Check for:
1. Best practices adherence
2. Error handling completeness
3. Security issues
4. Performance optimizations
5. Cost efficiency
6. Code quality

Provide specific recommendations with code examples.
```

### Migrate from Other LLM

```
Help me migrate from [OpenAI / Claude / other] to Gemini:

Current implementation:
```python
[paste current code]
```

Features used:
- [ ] [list features]

Requirements:
- Maintain feature parity
- Optimize for Gemini's strengths
- Handle API differences

Provide:
1. Migration plan
2. Equivalent Gemini code
3. Feature mapping table
4. Optimization opportunities specific to Gemini
```

---

*Last updated: 2026-01-25*
