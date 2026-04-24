# Claude API Basics - Checklist

## Authentication Setup

- [ ] Set ANTHROPIC_API_KEY environment variable
- [ ] Verify API key is valid (non-expired)
- [ ] Configure required headers (x-api-key, anthropic-version, content-type)
- [ ] Load credentials from ~/.secrets/anthropic if available
- [ ] Test authentication with a simple API call

## Model Configuration

- [ ] Review available Claude models (Opus 4.5, Sonnet 4, Haiku 3.5)
- [ ] Select appropriate model for task complexity
- [ ] Document model selection rationale
- [ ] Understand model context window limits (200K tokens)
- [ ] Configure max_tokens parameter

## Rate Limiting Implementation

- [ ] Check rate limits for your tier (requests/min, tokens/min, tokens/day)
- [ ] Implement rate limit header monitoring
- [ ] Implement exponential backoff retry strategy
- [ ] Test retry behavior with rate limit errors
- [ ] Configure tenacity or manual retry logic

## Error Handling

- [ ] Handle invalid_api_key errors (401)
- [ ] Handle rate_limit_error (429) with backoff
- [ ] Handle overloaded_error (529) with retry
- [ ] Handle invalid_request_error (400)
- [ ] Handle not_found_error (404 - bad model name)
- [ ] Handle generic api_error (500) with retry
- [ ] Parse error response structure (status code + message + type)

## Token Management

- [ ] Implement pre-count tokens before API call
- [ ] Count tokens including system prompt
- [ ] Include tools/functions in token count
- [ ] Track usage from API responses (input/output tokens)
- [ ] Monitor cache creation and read tokens if using caching

## Cost Tracking

- [ ] Create cost tracker class with model prices
- [ ] Define pricing for Opus 4.5, Sonnet 4, Haiku
- [ ] Include cache pricing (write/read costs)
- [ ] Calculate costs per API call
- [ ] Generate cost reports
- [ ] Consider batch API for 50% cost savings (if applicable)

## Verification & Testing

- [ ] Test authentication with curl
- [ ] Test message creation with Python SDK
- [ ] Verify model selection works
- [ ] Test rate limit handling
- [ ] Confirm cost calculations are accurate
- [ ] Document API version used (2023-06-01 or later)
