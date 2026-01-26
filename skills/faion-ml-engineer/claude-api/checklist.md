# Claude API Implementation Checklist

## Setup

- [ ] Install SDK: `pip install anthropic` or `npm install @anthropic-ai/sdk`
- [ ] Set `ANTHROPIC_API_KEY` environment variable
- [ ] Verify API access with test request
- [ ] Configure rate limit handling

## Messages API

- [ ] Choose appropriate model for task
- [ ] Set `max_tokens` based on expected output
- [ ] Define system prompt for behavior
- [ ] Handle multi-turn conversations correctly
- [ ] Parse response content blocks

## Tool Use

- [ ] Define tools with clear descriptions
- [ ] Use JSON Schema for `input_schema`
- [ ] Mark required parameters
- [ ] Implement tool execution logic
- [ ] Handle tool results (success and error)
- [ ] Support parallel tool calls
- [ ] Consider `tool_choice` for forcing tool use

## Extended Thinking

- [ ] Use Claude Opus 4.5 or Sonnet for thinking
- [ ] Set appropriate `budget_tokens` (min 1,024)
- [ ] Handle `thinking` content blocks
- [ ] Consider interleaved thinking with tools (beta)
- [ ] Stream thinking for user feedback

## Streaming

- [ ] Enable streaming with `stream=True`
- [ ] Handle all event types:
  - [ ] `message_start`
  - [ ] `content_block_start`
  - [ ] `content_block_delta`
  - [ ] `content_block_stop`
  - [ ] `message_stop`
- [ ] Process text deltas incrementally
- [ ] Handle tool use deltas
- [ ] Implement async streaming if needed

## Vision

- [ ] Encode images as base64
- [ ] Set correct `media_type`
- [ ] Place images before text in content
- [ ] Handle multiple images if needed
- [ ] Support PDFs (up to 100 pages)

## Prompt Caching

- [ ] Enable beta header: `prompt-caching-2024-07-31`
- [ ] Add `cache_control` to cacheable content
- [ ] Cache system prompts (most reused)
- [ ] Cache long documents for multi-turn
- [ ] Monitor cache hit rate

## Batch API

- [ ] Prepare batch requests with `custom_id`
- [ ] Submit batch via `messages.batches.create`
- [ ] Poll for completion status
- [ ] Process results on completion
- [ ] Handle errors per request

## Error Handling

- [ ] Catch `AuthenticationError` (401)
- [ ] Catch `RateLimitError` (429)
- [ ] Catch `BadRequestError` (400)
- [ ] Catch `APIStatusError` (500+)
- [ ] Implement exponential backoff
- [ ] Set appropriate retry limits

## Cost Management

- [ ] Pre-count tokens for large inputs
- [ ] Track usage from responses
- [ ] Calculate costs per request
- [ ] Use caching to reduce input costs
- [ ] Use Batch API for non-urgent work
- [ ] Choose model appropriate to task

## Security

- [ ] Never log API keys
- [ ] Use environment variables for secrets
- [ ] Validate user input before sending
- [ ] Implement content filtering if needed
- [ ] Review computer use safety guidelines

## Production

- [ ] Implement request logging
- [ ] Set up monitoring and alerts
- [ ] Configure rate limit dashboard
- [ ] Implement graceful degradation
- [ ] Test failover scenarios
- [ ] Document API usage patterns
