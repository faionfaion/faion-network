# Gemini API Implementation Checklist

## Setup

- [ ] Install SDK: `pip install google-generativeai`
- [ ] Get API key from [Google AI Studio](https://aistudio.google.com/)
- [ ] Set environment variable: `export GOOGLE_API_KEY="..."`
- [ ] Test basic generation works

## Model Selection

- [ ] Identify task complexity (simple/moderate/complex)
- [ ] Choose appropriate model:
  - [ ] Gemini 3 Pro - complex reasoning, multi-step tasks
  - [ ] Gemini 3 Flash - balanced speed + intelligence
  - [ ] Gemini 2.0 Flash - fastest, real-time apps
  - [ ] Gemini 1.5 Pro - very long context (2M tokens)
  - [ ] Gemini 1.5 Flash - high-volume, cost-sensitive
- [ ] Configure thinking level (Gemini 3):
  - [ ] `high` for complex tasks (default)
  - [ ] `low` for simple tasks
  - [ ] `minimal` for speed-critical (Flash only)

## Basic Generation

- [ ] Configure generation parameters:
  - [ ] `temperature` (default 1.0 for Gemini 3)
  - [ ] `top_p`, `top_k` if needed
  - [ ] `max_output_tokens`
  - [ ] `response_mime_type` for structured output
- [ ] Set system instruction for consistent behavior
- [ ] Test with sample prompts

## Chat Implementation

- [ ] Initialize chat session with `model.start_chat()`
- [ ] Handle conversation history
- [ ] Implement streaming for better UX
- [ ] Add system instruction for persona/behavior

## Multimodal

### Images
- [ ] Test image upload with `PIL.Image`
- [ ] Test file upload with `genai.upload_file()`
- [ ] Handle multiple images in single request
- [ ] Set appropriate `media_resolution` (Gemini 3)

### Video
- [ ] Upload video with `genai.upload_file()`
- [ ] Wait for processing (check `state.name`)
- [ ] Test timestamp-based queries
- [ ] Handle long videos appropriately

### Audio
- [ ] Upload audio files (MP3, WAV, etc.)
- [ ] Test transcription
- [ ] Test audio analysis/summarization

### PDFs
- [ ] Upload PDF with `genai.upload_file()`
- [ ] Test document summarization
- [ ] Test Q&A over document content

## Streaming

- [ ] Implement text streaming with `stream=True`
- [ ] Handle streaming in chat sessions
- [ ] Implement async streaming if needed
- [ ] Test chunk processing

## Function Calling

- [ ] Define function declarations with proper schema
- [ ] Include clear descriptions for each function
- [ ] Configure `tool_config` mode:
  - [ ] `AUTO` - model decides
  - [ ] `ANY` - must call function
  - [ ] `NONE` - no function calling
  - [ ] `VALIDATED` - schema adherence
- [ ] Implement function execution handler
- [ ] Handle parallel function calls
- [ ] Implement multimodal function responses (Gemini 3)
- [ ] Enable automatic function calling if appropriate

## Live API (Real-time)

- [ ] Install audio libraries (PyAudio/mic/speaker)
- [ ] Configure WebSocket connection
- [ ] Set up audio streaming (16kHz input, 24kHz output)
- [ ] Handle voice activity detection
- [ ] Implement session management
- [ ] Use ephemeral tokens for client-side auth
- [ ] Test bidirectional audio flow

## Context Caching

- [ ] Identify cacheable content (>32K tokens)
- [ ] Create cache with `caching.CachedContent.create()`
- [ ] Set appropriate TTL
- [ ] Use `GenerativeModel.from_cached_content()`
- [ ] Monitor cache usage and costs
- [ ] Clean up expired caches

## Embeddings

- [ ] Choose appropriate task type:
  - [ ] `RETRIEVAL_DOCUMENT` for indexing
  - [ ] `RETRIEVAL_QUERY` for search
  - [ ] `SEMANTIC_SIMILARITY` for comparison
- [ ] Implement batch embedding for efficiency
- [ ] Store embeddings in vector database
- [ ] Implement similarity search

## Safety & Error Handling

- [ ] Configure safety settings per category
- [ ] Handle `BlockedPromptException`
- [ ] Handle `StopCandidateException`
- [ ] Implement rate limit handling with backoff
- [ ] Check safety ratings in responses
- [ ] Log blocked content for analysis

## Grounding

- [ ] Enable Google Search grounding
- [ ] Configure dynamic retrieval threshold
- [ ] Access grounding metadata (sources)
- [ ] Combine search with function calling

## Code Execution

- [ ] Enable with `tools=["code_execution"]`
- [ ] Handle executed code output
- [ ] Test data analysis workflows
- [ ] Test chart generation

## Production Readiness

- [ ] Move to Vertex AI for enterprise features
- [ ] Implement proper logging/monitoring
- [ ] Set up error alerting
- [ ] Configure VPC/IAM if needed
- [ ] Implement cost tracking
- [ ] Set up usage quotas
- [ ] Test fallback strategies
- [ ] Document API key rotation process

## Cost Optimization

- [ ] Use Flash models where possible
- [ ] Enable context caching for repeated contexts
- [ ] Limit output tokens appropriately
- [ ] Compress prompts without losing meaning
- [ ] Monitor token usage
- [ ] Set up cost alerts

## Testing

- [ ] Unit tests for function declarations
- [ ] Integration tests for API calls
- [ ] Test error handling paths
- [ ] Test rate limiting behavior
- [ ] Test streaming interruption
- [ ] Load testing for production volume
