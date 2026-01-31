# Python Async Patterns Checklist (Complete)

Complete checklist is already present in file - comprehensive coverage from Requirements Analysis through Production/Code Review checklists

### Environment Setup

- [ ] Install async HTTP client (`pip install httpx` or `pip install aiohttp`)
- [ ] Install async database driver if needed (`asyncpg`, `aiosqlite`, `motor`)
- [ ] Install testing tools (`pip install pytest-asyncio`)
- [ ] Configure IDE for async support

---

## Implementation Checklist

### Basic Async Function

- [ ] Define function with `async def`
- [ ] Use `await` for all async operations
- [ ] Return type hints include `Awaitable` context if needed
- [ ] No sync I/O calls inside async function

```python
async def fetch_user(user_id: int) -> User:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"/users/{user_id}")
        return User(**response.json())
```

### Concurrent Execution (gather)

- [ ] Create list of coroutines
- [ ] Use `asyncio.gather(*coroutines)`
- [ ] Consider `return_exceptions=True` for fault tolerance
- [ ] Filter out exceptions from results if needed

```python
results = await asyncio.gather(
    fetch_user(1),
    fetch_user(2),
    return_exceptions=True
)
```

### Concurrent Execution (TaskGroup - Python 3.11+)

- [ ] Use `async with asyncio.TaskGroup() as tg:`
- [ ] Create tasks with `tg.create_task()`
- [ ] Store task references to get results
- [ ] Handle `ExceptionGroup` with `except*`

```python
async with asyncio.TaskGroup() as tg:
    task1 = tg.create_task(fetch_user(1))
    task2 = tg.create_task(fetch_user(2))
# Access results: task1.result(), task2.result()
```

### Rate Limiting

- [ ] Create `asyncio.Semaphore(max_concurrent)`
- [ ] Wrap operations in `async with semaphore:`
- [ ] Set appropriate limit (consider API limits, connection pools)
- [ ] Test under load to verify limits work

```python
semaphore = asyncio.Semaphore(10)

async def rate_limited_fetch(url: str) -> dict:
    async with semaphore:
        return await fetch(url)
```

### Timeouts

- [ ] Use `asyncio.timeout(seconds)` context manager (3.11+)
- [ ] Or use `asyncio.wait_for(coro, timeout=seconds)` (older Python)
- [ ] Handle `asyncio.TimeoutError`
- [ ] Consider `timeout_at()` for absolute deadlines

```python
async with asyncio.timeout(30.0):
    result = await slow_operation()
```

### Async Context Managers

- [ ] Implement `__aenter__` and `__aexit__` methods
- [ ] Or use `@asynccontextmanager` decorator
- [ ] Ensure cleanup in `__aexit__` (close connections, release resources)
- [ ] Handle exceptions in `__aexit__` appropriately

```python
@asynccontextmanager
async def get_connection():
    conn = await connect()
    try:
        yield conn
    finally:
        await conn.close()
```

### Async Generators

- [ ] Use `async def` with `yield`
- [ ] Iterate with `async for`
- [ ] Handle cleanup with `try/finally` or `async with`
- [ ] Consider `asyncio.Queue` for producer/consumer patterns

```python
async def stream_items() -> AsyncIterator[Item]:
    async for page in paginate():
        for item in page:
            yield item
```

### Error Handling

- [ ] Use `try/except` inside coroutines for local handling
- [ ] Use `try/except*` for ExceptionGroups (TaskGroup)
- [ ] Don't swallow `asyncio.CancelledError` (let it propagate)
- [ ] Log errors with context (task name, parameters)
- [ ] Implement graceful degradation where appropriate

```python
try:
    async with asyncio.TaskGroup() as tg:
        tg.create_task(risky_operation())
except* ValueError as eg:
    for exc in eg.exceptions:
        logger.error(f"ValueError: {exc}")
except* TypeError as eg:
    for exc in eg.exceptions:
        logger.error(f"TypeError: {exc}")
```

### Background Tasks

- [ ] Store task references (prevent garbage collection)
- [ ] Add done callback for cleanup: `task.add_done_callback(tasks.discard)`
- [ ] Implement graceful shutdown
- [ ] Handle exceptions in background tasks

```python
tasks: set[asyncio.Task] = set()

def add_background_task(coro):
    task = asyncio.create_task(coro)
    tasks.add(task)
    task.add_done_callback(tasks.discard)
    return task
```

### Running Sync Code in Async

- [ ] Identify blocking sync operations
- [ ] Use `loop.run_in_executor()` to offload
- [ ] Use `ThreadPoolExecutor` for I/O-bound sync
- [ ] Use `ProcessPoolExecutor` for CPU-bound
- [ ] Don't create executor per call (reuse)

```python
loop = asyncio.get_running_loop()
result = await loop.run_in_executor(None, sync_function, arg1, arg2)
```

---

## Testing Checklist

### pytest-asyncio Setup

- [ ] Install: `pip install pytest-asyncio`
- [ ] Add `pytest.mark.asyncio` to async tests
- [ ] Configure `loop_scope` in pytest.ini if needed
- [ ] Use async fixtures for async setup

```python
@pytest.mark.asyncio
async def test_fetch_user():
    user = await fetch_user(1)
    assert user.id == 1
```

### Mocking Async Code

- [ ] Use `AsyncMock` for async function mocks
- [ ] Configure return values with `return_value` (for sync) or as coroutine
- [ ] Use `side_effect` for exceptions or multiple returns
- [ ] Patch at correct location

```python
@pytest.mark.asyncio
async def test_with_mock():
    with patch("module.fetch_data", new_callable=AsyncMock) as mock:
        mock.return_value = {"id": 1}
        result = await function_under_test()
        assert result["id"] == 1
```

### Testing Timeouts

- [ ] Test timeout behavior triggers correctly
- [ ] Verify cleanup happens on timeout
- [ ] Test recovery from timeout
- [ ] Use shorter timeouts in tests than production

### Testing Cancellation

- [ ] Test task cancellation propagates
- [ ] Verify cleanup on cancellation
- [ ] Test partial completion scenarios
- [ ] Ensure no resource leaks on cancel

---

## Production Checklist

### Performance

- [ ] Set appropriate concurrency limits
- [ ] Reuse HTTP clients (don't create per request)
- [ ] Use connection pooling
- [ ] Profile with async profilers
- [ ] Monitor event loop lag

### Reliability

- [ ] Implement retry logic with exponential backoff
- [ ] Set appropriate timeouts on all operations
- [ ] Handle partial failures gracefully
- [ ] Implement circuit breakers for external services

### Observability

- [ ] Log async task lifecycle (start, complete, error)
- [ ] Track concurrent task count
- [ ] Monitor queue depths
- [ ] Set up alerting for event loop blocking

### Graceful Shutdown

- [ ] Cancel pending tasks on shutdown
- [ ] Wait for in-progress tasks with timeout
- [ ] Close connections and resources
- [ ] Log incomplete tasks

```python
async def shutdown(tasks: set[asyncio.Task], timeout: float = 5.0):
    for task in tasks:
        task.cancel()
    await asyncio.wait(tasks, timeout=timeout)
```

---

## Code Review Checklist

### Common Issues to Check

- [ ] No sync I/O in async code (requests, time.sleep, open())
- [ ] All coroutines are awaited
- [ ] Task references stored (no fire-and-forget without tracking)
- [ ] CancelledError not swallowed
- [ ] Semaphores used for rate limiting
- [ ] Timeouts on all external calls
- [ ] Proper cleanup in context managers
- [ ] Exception handling doesn't hide errors
- [ ] Tests cover async behavior

### Performance Issues

- [ ] HTTP client reused (not created per request)
- [ ] Database connections pooled
- [ ] No unnecessary serialization
- [ ] Appropriate concurrency limits
- [ ] No CPU-bound work blocking event loop
