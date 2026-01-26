# OpenAI API Implementation Checklists

Step-by-step checklists for production-ready OpenAI API integration.

## Pre-Integration Checklist

Before writing any code, verify these requirements.

### Project Setup

- [ ] **API key obtained** - Project key (`sk-proj-*`) from OpenAI dashboard
- [ ] **Environment variable configured** - `OPENAI_API_KEY` set securely
- [ ] **SDK installed** - `pip install openai` (Python) or `npm install openai` (Node.js)
- [ ] **Organization/project IDs** - Configure if using team accounts
- [ ] **Billing enabled** - Credits added for production usage
- [ ] **Rate limits known** - Understand tier limits for your account

### Requirements Analysis

- [ ] **Use case defined** - What problem does the API solve?
- [ ] **Model selected** - gpt-4o vs gpt-4o-mini vs o1 based on task complexity
- [ ] **Cost estimated** - Expected tokens/day and budget
- [ ] **Latency requirements** - Streaming vs non-streaming decision
- [ ] **Output format** - JSON schema defined if using structured output
- [ ] **Error handling** - Strategy for rate limits, failures, timeouts

---

## Chat Completions Checklist

### Basic Implementation

- [ ] **Client initialized** - `OpenAI()` with automatic env var pickup
- [ ] **Model specified** - Use versioned model ID for production
- [ ] **Messages formatted** - Proper role/content structure
- [ ] **System prompt defined** - Clear instructions and persona
- [ ] **Temperature set** - 0 for deterministic, 0.7+ for creative
- [ ] **Max tokens configured** - Prevent runaway generation

### Production Hardening

- [ ] **Error handling** - Catch `RateLimitError`, `APIError`, `AuthenticationError`
- [ ] **Retry logic** - Exponential backoff for transient failures
- [ ] **Timeout configured** - `client.timeout` for slow responses
- [ ] **Usage tracking** - Log `response.usage` for cost monitoring
- [ ] **Model pinned** - Use `gpt-4o-2024-08-06` not `gpt-4o`
- [ ] **Input validation** - Sanitize user input before including in prompts
- [ ] **Output validation** - Verify response format before processing

### Message Roles

| Role | Checklist Items |
|------|-----------------|
| **system** | [ ] Clear persona, [ ] Explicit constraints, [ ] Output format |
| **user** | [ ] Sanitized input, [ ] Delimited with tags, [ ] Length limited |
| **assistant** | [ ] Previous responses for context, [ ] Consistent format |
| **tool** | [ ] Valid tool_call_id, [ ] JSON-serialized result |

---

## Streaming Checklist

### Implementation

- [ ] **Stream enabled** - `stream=True` in request
- [ ] **Chunk handling** - Process `delta.content` for each chunk
- [ ] **End detection** - Check `finish_reason` for completion
- [ ] **Flush output** - `flush=True` for real-time display
- [ ] **Error recovery** - Handle connection drops mid-stream

### UI Integration

- [ ] **Loading state** - Show indicator before first token
- [ ] **Progressive display** - Render tokens as received
- [ ] **Cancel support** - Allow user to stop generation
- [ ] **Reconnection** - Retry on network failure
- [ ] **Accessibility** - Announce streaming status to screen readers

### Streaming with Tools

- [ ] **Tool call detection** - Check `delta.tool_calls`
- [ ] **Argument accumulation** - Build arguments across chunks
- [ ] **Complete tool call** - Only execute when fully received
- [ ] **Result streaming** - Handle tool results in conversation

---

## Structured Output Checklist

### Schema Definition

- [ ] **Pydantic model created** - Type-safe schema definition
- [ ] **Field descriptions added** - Help model understand fields
- [ ] **Required fields marked** - No `Optional` for mandatory data
- [ ] **Enum constraints** - Use `Literal` or `Enum` for fixed values
- [ ] **Validation rules** - Add `Field(ge=0, le=1)` etc. for constraints
- [ ] **Nested models** - Proper structure for complex data

### Implementation

- [ ] **Parse method used** - `client.beta.chat.completions.parse()`
- [ ] **Response format set** - `response_format=YourModel`
- [ ] **Parsed result accessed** - `response.choices[0].message.parsed`
- [ ] **Refusal handling** - Check `message.refusal` for content policy

### Validation

- [ ] **Schema validation** - Pydantic validates automatically
- [ ] **Type checking** - Verify types at runtime
- [ ] **Business rules** - Additional validation beyond schema
- [ ] **Error recovery** - Retry with modified prompt on validation failure

### Streaming with Structured Output

- [ ] **SDK streaming helpers** - Use SDK's streaming with parse
- [ ] **Partial validation** - Validate complete fields as received
- [ ] **Error boundaries** - Handle malformed streaming JSON

---

## Function Calling / Tool Use Checklist

### Tool Definition

- [ ] **Function schema defined** - JSON Schema for parameters
- [ ] **Description clear** - When to use this tool
- [ ] **Parameters typed** - Proper types for all arguments
- [ ] **Required params marked** - In `required` array
- [ ] **Enum values listed** - For constrained parameters

### Implementation Loop

- [ ] **Initial request** - Include `tools` parameter
- [ ] **Tool choice configured** - `auto`, `required`, or specific function
- [ ] **Check for tool calls** - `message.tool_calls` presence
- [ ] **Execute tools** - Call your functions with parsed arguments
- [ ] **Add tool results** - Append `tool` role messages with results
- [ ] **Continue conversation** - Request next response with tool results
- [ ] **Detect completion** - No more tool calls = final response

### Parallel Tool Calls

- [ ] **Multiple calls handled** - Process all tool calls in single response
- [ ] **Order preserved** - Match results to call IDs
- [ ] **Concurrent execution** - Run independent tools in parallel
- [ ] **Error isolation** - Individual tool failures don't break loop

### Tool Result Messages

```python
# Checklist for tool result message
{
    "role": "tool",                    # [ ] Correct role
    "tool_call_id": tool_call.id,      # [ ] Matches call ID
    "content": json.dumps(result)      # [ ] JSON-serialized result
}
```

---

## Error Handling Checklist

### Exception Types

| Exception | Handling |
|-----------|----------|
| `AuthenticationError` | [ ] Check API key, [ ] Verify not expired |
| `RateLimitError` | [ ] Implement backoff, [ ] Queue requests |
| `APIError` (5xx) | [ ] Retry with backoff, [ ] Log for monitoring |
| `BadRequestError` | [ ] Validate input, [ ] Check token limits |
| `APITimeoutError` | [ ] Increase timeout, [ ] Implement retry |

### Retry Implementation

- [ ] **Exponential backoff** - `delay = base * (2 ** attempt)`
- [ ] **Max retries set** - Prevent infinite loops (3-5 attempts)
- [ ] **Jitter added** - Random delay to avoid thundering herd
- [ ] **Idempotency considered** - Safe to retry the request?
- [ ] **Logging** - Record retry attempts for debugging

### Circuit Breaker

- [ ] **Failure threshold** - Open circuit after N failures
- [ ] **Reset timeout** - Try again after cooling period
- [ ] **Half-open state** - Test with single request
- [ ] **Fallback behavior** - Graceful degradation when open

---

## Cost Management Checklist

### Token Tracking

- [ ] **Input tokens logged** - `response.usage.prompt_tokens`
- [ ] **Output tokens logged** - `response.usage.completion_tokens`
- [ ] **Cost calculated** - Apply per-model pricing
- [ ] **Budget alerts** - Notify when approaching limits
- [ ] **Daily/monthly reports** - Track spending trends

### Optimization

- [ ] **Model tiering** - Route simple tasks to gpt-4o-mini
- [ ] **Prompt caching** - Reuse system prompts for shared prefix
- [ ] **Batch API used** - 50% savings for async workloads
- [ ] **Max tokens set** - Prevent excessive generation
- [ ] **Stop sequences** - End generation early when possible
- [ ] **Embedding dimensions** - Reduce if quality permits

### Token Counting

- [ ] **tiktoken installed** - For accurate pre-request counting
- [ ] **Context tracked** - Know when approaching limits
- [ ] **Truncation strategy** - How to handle long inputs
- [ ] **Message priority** - Which messages to keep when truncating

---

## Security Checklist

### API Key Protection

- [ ] **Environment variables** - Never hardcode keys
- [ ] **Server-side only** - Keys never in client code
- [ ] **Rotation plan** - Regular key rotation schedule
- [ ] **Scope minimization** - Project keys over user keys
- [ ] **Secrets manager** - Use HashiCorp Vault, AWS Secrets, etc.
- [ ] **Audit logging** - Track key usage

### Input Sanitization

- [ ] **Length limits** - Prevent context overflow
- [ ] **Injection patterns** - Filter "ignore instructions" attempts
- [ ] **Special tokens** - Remove `<|im_start|>` etc.
- [ ] **Content validation** - Check for malicious content
- [ ] **User identification** - Pass `user` param for abuse tracking

### Output Safety

- [ ] **Content filtering** - Check response for harmful content
- [ ] **Moderation API** - Use for user-facing applications
- [ ] **PII detection** - Prevent sensitive data in outputs
- [ ] **Logging sanitized** - Don't log full prompts/responses

---

## Monitoring Checklist

### Metrics to Track

- [ ] **Latency** - Time to first token and total time
- [ ] **Error rate** - By error type and model
- [ ] **Token usage** - Input and output separately
- [ ] **Cost** - Daily, weekly, monthly trends
- [ ] **Request volume** - Requests per second/minute
- [ ] **Model performance** - Quality metrics for your use case

### Alerting

- [ ] **Error rate threshold** - Alert on spike in errors
- [ ] **Latency threshold** - Alert on slow responses
- [ ] **Cost threshold** - Alert on budget approach
- [ ] **Rate limit proximity** - Alert before hitting limits

### Observability

- [ ] **Request ID tracking** - Correlate logs across system
- [ ] **Distributed tracing** - Follow request through services
- [ ] **Log aggregation** - Centralized log storage
- [ ] **Dashboard** - Real-time visibility into API usage

---

## Testing Checklist

### Unit Tests

- [ ] **Mock API responses** - Don't call real API in tests
- [ ] **Error scenarios** - Test all error handling paths
- [ ] **Input validation** - Test sanitization logic
- [ ] **Output parsing** - Test structured output handling

### Integration Tests

- [ ] **Real API calls** - With test prompts and low token limits
- [ ] **Rate limit handling** - Verify backoff works
- [ ] **Timeout handling** - Test with slow responses
- [ ] **End-to-end flow** - Full user journey testing

### Load Tests

- [ ] **Concurrent requests** - Test parallel request handling
- [ ] **Rate limit behavior** - Verify queue/backoff under load
- [ ] **Memory usage** - Check for leaks with streaming
- [ ] **Cost projection** - Estimate production costs from load test

---

## Deployment Checklist

### Pre-Deployment

- [ ] **Environment config** - API keys in production secrets
- [ ] **Model version pinned** - Specific version, not alias
- [ ] **Timeouts configured** - Appropriate for expected latency
- [ ] **Error handling tested** - All failure modes covered
- [ ] **Monitoring enabled** - Metrics and logging ready

### Post-Deployment

- [ ] **Smoke tests passed** - Basic functionality verified
- [ ] **Metrics baseline** - Record normal operation metrics
- [ ] **Alerts configured** - Notify on anomalies
- [ ] **Runbook created** - How to handle common issues
- [ ] **Rollback plan** - How to revert if needed

### Scaling

- [ ] **Connection pooling** - Reuse HTTP connections
- [ ] **Rate limit management** - Distribute across time
- [ ] **Caching layer** - Cache identical requests
- [ ] **Queue system** - Buffer requests during spikes
- [ ] **Multi-region** - Consider latency for global users

---

## Quick Reference Card

### Common Issues and Fixes

| Issue | Quick Fix |
|-------|-----------|
| Rate limited | Implement exponential backoff |
| Slow responses | Enable streaming, reduce max_tokens |
| Inconsistent output | Lower temperature, add examples |
| Wrong format | Use structured output |
| High costs | Use gpt-4o-mini, batch API |
| Context too long | Truncate with tiktoken |

### Production Readiness Score

Rate your implementation (0-5 for each):

| Category | Score |
|----------|-------|
| Error handling | /5 |
| Security | /5 |
| Cost management | /5 |
| Monitoring | /5 |
| Testing | /5 |
| **Total** | /25 |

- 20-25: Production ready
- 15-19: Needs improvement
- <15: Not ready for production
