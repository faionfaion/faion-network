# Python Async Patterns

## Overview

Asynchronous programming in Python enables efficient handling of I/O-bound operations like network requests, database queries, file operations, and real-time communication. This methodology covers modern asyncio patterns, structured concurrency with TaskGroup (Python 3.11+), HTTP client selection, and production-ready async code practices.

**Python Version:** 3.11+ recommended (for TaskGroup, timeout context managers, ExceptionGroups)

## When to Use Async

| Use Case | Async Benefit |
|----------|---------------|
| High-performance APIs (FastAPI, aiohttp) | Handle thousands of concurrent connections |
| Multiple concurrent HTTP requests | 10x+ speedup vs sequential |
| Database operations (asyncpg, aiosqlite) | Non-blocking queries |
| Real-time applications (WebSockets) | Bidirectional communication |
| Background task processing | Fire-and-forget without blocking |
| Streaming data processing | Memory-efficient iteration |

## When NOT to Use Async

| Scenario | Better Alternative |
|----------|-------------------|
| CPU-bound computations | `multiprocessing` or `ProcessPoolExecutor` |
| Simple scripts with few I/O calls | Synchronous code |
| Legacy codebases without async support | Threading or sync patterns |
| When all libraries are sync-only | `run_in_executor()` wrapper |

## Key Concepts

### Event Loop

The event loop is the core of asyncio - it manages and distributes execution of coroutines. In modern Python (3.10+), you rarely interact with it directly.

```python
# Modern approach - let asyncio manage the loop
asyncio.run(main())

# Only when needed
loop = asyncio.get_running_loop()  # Inside async context
```

### Coroutines

Functions defined with `async def` that can be paused and resumed:

```python
async def fetch_data() -> dict:
    # Can use await here
    return await some_async_operation()
```

### Tasks

Coroutines wrapped for concurrent execution:

```python
task = asyncio.create_task(fetch_data())  # Starts immediately
result = await task  # Wait for completion
```

### Structured Concurrency (Python 3.11+)

TaskGroup ensures all tasks complete or are cancelled together - no orphan tasks:

```python
async with asyncio.TaskGroup() as tg:
    task1 = tg.create_task(operation1())
    task2 = tg.create_task(operation2())
# All tasks guaranteed complete here
```

## Pattern Selection Guide

| Need | Pattern | Python Version |
|------|---------|----------------|
| Run N tasks, get all results | `asyncio.gather()` | 3.4+ |
| Run N tasks, cancel on first failure | `asyncio.TaskGroup()` | 3.11+ |
| Limit concurrent operations | `asyncio.Semaphore` | 3.4+ |
| Timeout single operation | `asyncio.timeout()` | 3.11+ |
| Timeout with deadline | `asyncio.timeout_at()` | 3.11+ |
| Stream large datasets | Async generators | 3.6+ |
| Manage connections | Async context managers | 3.5+ |
| Run sync code in async | `run_in_executor()` | 3.4+ |

## HTTP Client Selection: httpx vs aiohttp

| Criteria | httpx | aiohttp |
|----------|-------|---------|
| Sync + Async support | Yes | No (async only) |
| HTTP/2 support | Yes | No |
| Performance (high concurrency) | Good | Excellent |
| API similarity to requests | Very similar | Different |
| Type annotations | Full | Partial |
| WebSocket support | No | Yes |
| Server capabilities | No | Yes |

**Recommendation:**
- **httpx** - Modern projects, HTTP/2 needed, mixed sync/async code
- **aiohttp** - Maximum performance, WebSockets, high-concurrency scrapers

## gather() vs TaskGroup

| Aspect | `asyncio.gather()` | `asyncio.TaskGroup()` |
|--------|-------------------|----------------------|
| Python version | 3.4+ | 3.11+ |
| Cancellation on error | No (unless configured) | Yes (automatic) |
| Returns ordered results | Yes (list) | No (access via task.result()) |
| Exception handling | One at a time | ExceptionGroup |
| Structured concurrency | No | Yes |
| Best for | Independent tasks | Related/dependent tasks |

**Use gather() when:**
- Need results in order
- Tasks are independent
- Failure of one shouldn't cancel others
- Need `return_exceptions=True` behavior

**Use TaskGroup when:**
- All tasks must succeed or none
- Want automatic cleanup on failure
- Need structured concurrency guarantees
- Modern Python 3.11+ codebase

## Anti-Patterns to Avoid

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| Sync I/O in async code | Blocks event loop | Use async libraries (httpx, asyncpg) |
| Not awaiting coroutines | Coroutine never executes | Always `await` or create task |
| Fire-and-forget without tracking | Tasks may be garbage collected | Store task references |
| Swallowing CancelledError | Breaks cancellation propagation | Let it propagate |
| Creating tasks outside context | Orphan tasks possible | Use TaskGroup |

## LLM Usage Tips

When using this methodology with LLMs (Claude, GPT, etc.):

### Effective Prompts

1. **For basic async conversion:**
   > "Convert this sync function to async using httpx. Keep the same interface."

2. **For concurrent operations:**
   > "I need to fetch data from 100 URLs concurrently with max 10 simultaneous requests. Use TaskGroup and Semaphore."

3. **For error handling:**
   > "Add proper error handling to this async code using try/except* for ExceptionGroups."

4. **For testing:**
   > "Write pytest-asyncio tests for this async service with mocked HTTP calls."

### Context to Provide

- Python version (3.11+ for TaskGroup)
- Framework (FastAPI, Django, standalone)
- Error handling requirements
- Performance constraints
- Testing framework preference

### Common Mistakes LLMs Make

1. Using `requests` instead of `httpx` in async code
2. Forgetting `await` on coroutines
3. Using old `event_loop.run_until_complete()` pattern
4. Not handling `CancelledError` properly
5. Creating event loops inside async functions

## Agent Selection

| Task | Model | Rationale |
|------|-------|----------|
| Analyze and assess | sonnet | Evaluation and planning |
| Execute implementation | haiku | Apply established patterns |
| Review and validate | sonnet | Quality assurance |
| Strategic decision | opus | Novel scenarios |
| Optimize and refine | haiku | Performance tuning |
| Document approach | haiku | Create documentation |

## External Resources

### Official Documentation
- [Python asyncio Documentation](https://docs.python.org/3/library/asyncio.html)
- [Python 3.11 TaskGroup](https://docs.python.org/3/library/asyncio-task.html#task-groups)
- [PEP 654 - Exception Groups](https://peps.python.org/pep-0654/)
- [PEP 525 - Async Generators](https://peps.python.org/pep-0525/)

### Libraries
- [HTTPX Documentation](https://www.python-httpx.org/)
- [aiohttp Documentation](https://docs.aiohttp.org/)
- [asyncpg Documentation](https://magicstack.github.io/asyncpg/)
- [pytest-asyncio Documentation](https://pytest-asyncio.readthedocs.io/)

### Tutorials & Guides
- [Real Python - Async IO in Python](https://realpython.com/async-io-python/)
- [Real Python - Exception Groups](https://realpython.com/python311-exception-groups/)
- [Python Structured Concurrency Guide](https://applifting.io/blog/python-structured-concurrency)

### Best Practices Articles
- [Async Python 2025: Fast, Safe, and Under Control](https://medium.com/@hadiyolworld007/async-python-2025-fast-safe-and-under-control-ee2c0e2b2bf6)
- [Structured Concurrency with TaskGroup](https://billypoon.com/insights/structured-concurrency-in-python-with-taskgroup-writing-async-code-that-doesn-t-break)
- [Why TaskGroup and Timeout Are Crucial](https://www.dataleadsfuture.com/why-taskgroup-and-timeout-are-so-crucial-in-python-3-11-asyncio/)
- [HTTPX vs Requests vs AIOHTTP](https://oxylabs.io/blog/httpx-vs-requests-vs-aiohttp)

## Related Files

| File | Description |
|------|-------------|
| [checklist.md](checklist.md) | Step-by-step async implementation checklist |
| [examples.md](examples.md) | Real async code examples |
| [templates.md](templates.md) | Copy-paste async patterns |
| [llm-prompts.md](llm-prompts.md) | Effective prompts for LLM-assisted development |

## Related Skills

- [faion-backend-developer](../faion-backend-developer/CLAUDE.md) - Database async patterns
- [faion-api-developer](../faion-api-developer/CLAUDE.md) - Async API design
- [faion-testing-developer](../faion-testing-developer/CLAUDE.md) - Async testing strategies
