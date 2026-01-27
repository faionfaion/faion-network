# LLM Prompts for Python Async Development

Effective prompts for LLM-assisted async Python development. Use these prompts with Claude, GPT, Cursor, or other AI coding assistants.

---

## Context Setting Prompts

### Initial Context

Use this at the start of a conversation to establish context:

```
I'm working on a Python async project with:
- Python version: 3.11+ (TaskGroup available)
- Framework: FastAPI / Django / standalone script
- HTTP client: httpx / aiohttp
- Database: asyncpg / aiosqlite / motor
- Testing: pytest-asyncio

Code should follow:
- Type hints everywhere
- Proper error handling with try/except*
- Structured concurrency with TaskGroup
- No fire-and-forget tasks without tracking
```

---

## Conversion Prompts

### Convert Sync to Async

```
Convert this synchronous function to async:
- Use httpx.AsyncClient instead of requests
- Use asyncpg/aiosqlite instead of sync database drivers
- Preserve the same interface and return types
- Add proper type hints
- Handle errors appropriately

[paste your sync code here]
```

### Convert requests to httpx

```
Convert this code from requests to httpx async:
- Replace requests.get/post with httpx.AsyncClient
- Make the function async def
- Add await to all HTTP calls
- Reuse the client (don't create per request)
- Add timeout parameter

[paste your requests code here]
```

### Convert gather() to TaskGroup

```
Convert this asyncio.gather() code to use TaskGroup (Python 3.11+):
- Replace gather() with async with asyncio.TaskGroup()
- Store task references to get results
- Add except* handling for ExceptionGroups
- Ensure proper cancellation on failure

[paste your gather code here]
```

---

## Implementation Prompts

### Concurrent HTTP Requests

```
Write an async function to fetch data from multiple URLs concurrently:
- Input: list of URLs
- Output: list of JSON responses (same order as input)
- Use httpx.AsyncClient (reuse for all requests)
- Add rate limiting with Semaphore (max 10 concurrent)
- Handle failures gracefully (return None for failed requests)
- Add timeout (30 seconds per request)
- Python 3.11+ (use TaskGroup)
```

### Paginated API Consumer

```
Write an async generator to consume a paginated REST API:
- API returns: {"items": [...], "next_page": "..."}
- Yield individual items (not pages)
- Stop when no more pages
- Handle rate limits (429 status)
- Add retry with exponential backoff
- Memory efficient (don't load all pages at once)
```

### Background Task System

```
Create a background task manager class:
- Store task references (prevent GC)
- Add done callbacks for cleanup
- Track success/failure counts
- Support graceful shutdown with timeout
- Log task lifecycle events
- Thread-safe task management
- Compatible with FastAPI lifespan
```

### Database Connection Pool

```
Create an async context manager for database connection pool:
- Initialize pool on enter
- Close pool on exit
- Handle connection errors
- Support configurable pool size
- Add health check method
- Work with asyncpg
```

### Retry with Backoff

```
Write a retry decorator/function for async operations:
- Configurable max retries
- Exponential backoff with jitter
- Configurable exceptions to retry on
- Timeout for entire operation
- Log retry attempts
- Return last exception if all retries fail
```

---

## Error Handling Prompts

### Add Exception Handling

```
Add proper error handling to this async code:
- Use try/except* for ExceptionGroups (if using TaskGroup)
- Handle specific exceptions (httpx.HTTPError, asyncio.TimeoutError)
- Don't swallow asyncio.CancelledError
- Log errors with context
- Implement graceful degradation where possible
- Return sensible defaults on failure

[paste your code here]
```

### Handle Partial Failures

```
Modify this code to handle partial failures:
- Some operations can fail without failing the whole batch
- Return successful results + list of errors
- Don't cancel other tasks on single failure
- Add error aggregation and reporting
- Maintain result ordering

[paste your code here]
```

---

## Testing Prompts

### Write Async Tests

```
Write pytest-asyncio tests for this async function:
- Test happy path
- Test error handling (network errors, timeouts)
- Test edge cases (empty input, single item)
- Mock external HTTP calls with AsyncMock
- Test cancellation behavior
- Use async fixtures for setup/teardown

[paste your function here]
```

### Mock Async Dependencies

```
Create mocks for testing this async code:
- Mock httpx.AsyncClient with AsyncMock
- Configure return values for different endpoints
- Simulate errors (timeout, HTTP 500)
- Verify correct calls were made
- Reset mocks between tests

[paste your code here]
```

### Test TaskGroup Cancellation

```
Write a test to verify TaskGroup cancellation behavior:
- Create TaskGroup with multiple tasks
- One task should fail
- Verify other tasks were cancelled
- Verify ExceptionGroup contains correct exception
- Verify no resource leaks
```

---

## Performance Prompts

### Optimize Concurrent Code

```
Optimize this async code for better performance:
- Identify opportunities for parallelization
- Add connection pooling
- Reduce unnecessary awaits
- Batch operations where possible
- Add caching if appropriate
- Profile and identify bottlenecks

[paste your code here]
```

### Add Rate Limiting

```
Add rate limiting to this async code:
- Limit to N concurrent operations
- Use asyncio.Semaphore
- Consider per-host limits for HTTP
- Add queue depth monitoring
- Handle backpressure gracefully

[paste your code here]
```

---

## Architecture Prompts

### Design Async Service

```
Design an async service class for [describe purpose]:
- Initialize resources in startup method
- Clean up in shutdown method
- Use dependency injection
- Support health checks
- Handle configuration
- Thread-safe operations
- Graceful degradation
- Logging and metrics

Requirements:
[list requirements]
```

### Design Event-Driven System

```
Design an async event-driven system with:
- Event publisher (async)
- Event subscribers (async handlers)
- Event queue (asyncio.Queue)
- Multiple worker consumers
- Graceful shutdown
- Error handling per event
- Retry failed events
- Dead letter queue for failures
```

---

## Debugging Prompts

### Fix Async Bug

```
This async code has a bug - help me find and fix it:
- [describe the symptoms]
- [paste the code]
- [paste any error messages]

Check for:
- Missing await
- Fire-and-forget without tracking
- Blocking sync calls
- Event loop issues
- Resource leaks
- Race conditions
```

### Explain Async Behavior

```
Explain what this async code does step by step:
- Trace the execution flow
- Identify concurrency points
- Note when event loop can switch
- Identify potential issues
- Suggest improvements

[paste your code here]
```

---

## Review Prompts

### Code Review

```
Review this async code for:
- Correct async/await usage
- Proper error handling
- Resource management (no leaks)
- Concurrency safety
- Performance issues
- Testing coverage gaps
- Documentation needs

[paste your code here]
```

### Security Review

```
Review this async code for security issues:
- Input validation
- Timeout handling (DoS prevention)
- Resource limits
- Error information leakage
- Injection vulnerabilities
- Authentication/authorization

[paste your code here]
```

---

## Migration Prompts

### Migrate to Python 3.11+

```
Update this async code to use Python 3.11+ features:
- Replace gather() with TaskGroup where appropriate
- Use asyncio.timeout() context manager
- Use except* for ExceptionGroups
- Use asyncio.timeout_at() for deadlines
- Update type hints to modern syntax

[paste your code here]
```

### Migrate to Structured Concurrency

```
Refactor this async code to use structured concurrency:
- Replace fire-and-forget tasks with tracked tasks
- Use TaskGroup for related tasks
- Ensure all tasks complete before function returns
- Add proper cancellation propagation
- No orphan tasks possible

[paste your code here]
```

---

## Tips for Better Results

### Provide Context

Always include:
- Python version (3.11+ for TaskGroup)
- Framework (FastAPI, Django, etc.)
- Libraries used (httpx, aiohttp, asyncpg)
- Error messages if debugging

### Be Specific

Instead of:
> "Write async code to fetch data"

Use:
> "Write async function to fetch user data from REST API, handling pagination, with max 5 concurrent requests, 30s timeout, using httpx and Python 3.11 TaskGroup"

### Request Explanations

Add to prompts:
- "Explain why you chose this approach"
- "What are the tradeoffs?"
- "What could go wrong?"
- "How would this behave under load?"

### Iterative Refinement

1. Start with basic implementation
2. Ask for error handling additions
3. Ask for performance optimizations
4. Ask for tests
5. Ask for documentation

---

## Common LLM Mistakes to Watch For

When reviewing LLM-generated async code, check for:

| Mistake | What to Look For |
|---------|-----------------|
| Using `requests` | Should use `httpx` or `aiohttp` |
| Missing `await` | Coroutines must be awaited |
| Creating event loop | Use `asyncio.run()` or framework |
| Fire-and-forget | Tasks need references stored |
| Swallowing CancelledError | Should propagate |
| New client per request | Should reuse `AsyncClient` |
| Blocking file I/O | Should use `aiofiles` or executor |
| No timeout | External calls need timeouts |
| Old event_loop fixture | pytest-asyncio 1.0 removed it |
