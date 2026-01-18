# M-PY-005: Asyncio Patterns

## Metadata
- **Category:** Development/Python
- **Difficulty:** Intermediate
- **Tags:** #dev, #python, #async, #methodology
- **Agent:** faion-code-agent

---

## Problem

Asyncio is powerful but confusing. Mixing sync and async code causes deadlocks. Unhandled exceptions crash programs silently. You need patterns that work reliably.

## Promise

After this methodology, you will write async Python code that is fast, correct, and maintainable. No more mysterious deadlocks or lost exceptions.

## Overview

Python asyncio enables concurrent I/O operations without threads. Key concepts: coroutines, event loop, tasks, and gathering.

---

## Framework

### Step 1: Basic Async/Await

```python
import asyncio

# Coroutine definition
async def fetch_data(url: str) -> dict:
    """Async function (coroutine)."""
    # Simulate I/O operation
    await asyncio.sleep(1)
    return {"url": url, "data": "..."}

# Running coroutines
async def main():
    # Sequential execution
    result1 = await fetch_data("url1")
    result2 = await fetch_data("url2")
    # Total time: 2 seconds

    # Concurrent execution
    results = await asyncio.gather(
        fetch_data("url1"),
        fetch_data("url2"),
    )
    # Total time: 1 second

# Entry point
if __name__ == "__main__":
    asyncio.run(main())
```

### Step 2: Task Management

```python
import asyncio

async def worker(name: str, duration: float):
    print(f"{name} starting")
    await asyncio.sleep(duration)
    print(f"{name} done")
    return f"{name} result"

async def main():
    # Create tasks for concurrent execution
    task1 = asyncio.create_task(worker("A", 2))
    task2 = asyncio.create_task(worker("B", 1))

    # Tasks start immediately after create_task
    # Do other work here...

    # Wait for completion
    result1 = await task1
    result2 = await task2

    # Or gather all at once
    tasks = [
        asyncio.create_task(worker(f"Worker-{i}", i * 0.1))
        for i in range(5)
    ]
    results = await asyncio.gather(*tasks)
```

### Step 3: Error Handling

```python
import asyncio

async def might_fail(success: bool):
    await asyncio.sleep(0.1)
    if not success:
        raise ValueError("Operation failed")
    return "Success"

async def main():
    # Individual exception handling
    try:
        result = await might_fail(False)
    except ValueError as e:
        print(f"Caught: {e}")

    # gather with return_exceptions
    results = await asyncio.gather(
        might_fail(True),
        might_fail(False),
        might_fail(True),
        return_exceptions=True,
    )

    for result in results:
        if isinstance(result, Exception):
            print(f"Error: {result}")
        else:
            print(f"Result: {result}")

# TaskGroup (Python 3.11+) - better exception handling
async def main_taskgroup():
    try:
        async with asyncio.TaskGroup() as tg:
            task1 = tg.create_task(might_fail(True))
            task2 = tg.create_task(might_fail(False))
            # If any task fails, all are cancelled
    except* ValueError as eg:
        for e in eg.exceptions:
            print(f"Error: {e}")
```

### Step 4: Timeouts

```python
import asyncio

async def slow_operation():
    await asyncio.sleep(10)
    return "Done"

async def main():
    # Timeout with asyncio.timeout (Python 3.11+)
    try:
        async with asyncio.timeout(2):
            result = await slow_operation()
    except asyncio.TimeoutError:
        print("Operation timed out")

    # wait_for for older Python
    try:
        result = await asyncio.wait_for(slow_operation(), timeout=2)
    except asyncio.TimeoutError:
        print("Operation timed out")

    # Timeout with default value
    async def with_timeout(coro, timeout: float, default=None):
        try:
            return await asyncio.wait_for(coro, timeout=timeout)
        except asyncio.TimeoutError:
            return default
```

### Step 5: Semaphores and Locks

```python
import asyncio

# Rate limiting with semaphore
async def fetch_with_limit(url: str, semaphore: asyncio.Semaphore):
    async with semaphore:
        # Only N concurrent requests
        return await fetch(url)

async def main():
    semaphore = asyncio.Semaphore(10)  # Max 10 concurrent

    urls = [f"https://api.example.com/{i}" for i in range(100)]
    tasks = [fetch_with_limit(url, semaphore) for url in urls]
    results = await asyncio.gather(*tasks)

# Mutex with Lock
class Counter:
    def __init__(self):
        self.value = 0
        self._lock = asyncio.Lock()

    async def increment(self):
        async with self._lock:
            current = self.value
            await asyncio.sleep(0.01)  # Simulate work
            self.value = current + 1
```

### Step 6: Queues

```python
import asyncio

async def producer(queue: asyncio.Queue, items: list):
    for item in items:
        await queue.put(item)
        print(f"Produced: {item}")
    # Signal completion
    await queue.put(None)

async def consumer(queue: asyncio.Queue, name: str):
    while True:
        item = await queue.get()
        if item is None:
            queue.task_done()
            break
        print(f"{name} processing: {item}")
        await asyncio.sleep(0.1)  # Simulate work
        queue.task_done()

async def main():
    queue = asyncio.Queue(maxsize=10)

    items = list(range(20))

    # Start producer and consumers
    producer_task = asyncio.create_task(producer(queue, items))
    consumer_tasks = [
        asyncio.create_task(consumer(queue, f"Consumer-{i}"))
        for i in range(3)
    ]

    await producer_task
    await queue.join()  # Wait until all items processed

    # Stop consumers
    for _ in consumer_tasks:
        await queue.put(None)
```

### Step 7: HTTP Requests with aiohttp

```python
import asyncio
import aiohttp

async def fetch(session: aiohttp.ClientSession, url: str) -> dict:
    async with session.get(url) as response:
        return await response.json()

async def fetch_all(urls: list[str]) -> list[dict]:
    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, url) for url in urls]
        return await asyncio.gather(*tasks)

# With rate limiting
async def fetch_with_rate_limit(urls: list[str], rate: int = 10) -> list[dict]:
    semaphore = asyncio.Semaphore(rate)

    async def limited_fetch(session: aiohttp.ClientSession, url: str):
        async with semaphore:
            async with session.get(url) as response:
                return await response.json()

    async with aiohttp.ClientSession() as session:
        tasks = [limited_fetch(session, url) for url in urls]
        return await asyncio.gather(*tasks, return_exceptions=True)
```

### Step 8: Running Sync Code

```python
import asyncio
from concurrent.futures import ThreadPoolExecutor

# CPU-bound or blocking I/O
def blocking_operation(data: str) -> str:
    # Heavy computation or blocking I/O
    import time
    time.sleep(1)
    return data.upper()

async def main():
    loop = asyncio.get_event_loop()

    # Run in thread pool (default executor)
    result = await loop.run_in_executor(None, blocking_operation, "hello")

    # Custom executor for more control
    with ThreadPoolExecutor(max_workers=4) as executor:
        results = await asyncio.gather(
            loop.run_in_executor(executor, blocking_operation, "a"),
            loop.run_in_executor(executor, blocking_operation, "b"),
        )
```

---

## Templates

### Async Context Manager

```python
class AsyncResource:
    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def connect(self):
        print("Connected")

    async def close(self):
        print("Closed")

# Usage
async with AsyncResource() as resource:
    await resource.do_something()
```

### Async Iterator

```python
class AsyncRange:
    def __init__(self, start: int, end: int):
        self.start = start
        self.end = end

    def __aiter__(self):
        self.current = self.start
        return self

    async def __anext__(self):
        if self.current >= self.end:
            raise StopAsyncIteration
        await asyncio.sleep(0.1)  # Simulate async work
        value = self.current
        self.current += 1
        return value

# Usage
async for num in AsyncRange(0, 5):
    print(num)
```

### Retry Pattern

```python
import asyncio
from functools import wraps

def async_retry(retries: int = 3, delay: float = 1.0, backoff: float = 2.0):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            last_exception = None
            current_delay = delay

            for attempt in range(retries):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < retries - 1:
                        await asyncio.sleep(current_delay)
                        current_delay *= backoff

            raise last_exception
        return wrapper
    return decorator

@async_retry(retries=3, delay=1.0)
async def flaky_api_call():
    # Might fail randomly
    pass
```

---

## Examples

### Batch Processing

```python
async def process_batch(items: list, batch_size: int = 10):
    """Process items in batches with concurrency limit."""
    results = []

    for i in range(0, len(items), batch_size):
        batch = items[i:i + batch_size]
        batch_results = await asyncio.gather(
            *[process_item(item) for item in batch]
        )
        results.extend(batch_results)

    return results
```

### Graceful Shutdown

```python
import asyncio
import signal

async def main():
    tasks = set()
    shutdown_event = asyncio.Event()

    def signal_handler():
        shutdown_event.set()

    loop = asyncio.get_event_loop()
    loop.add_signal_handler(signal.SIGTERM, signal_handler)
    loop.add_signal_handler(signal.SIGINT, signal_handler)

    # Start workers
    for i in range(5):
        task = asyncio.create_task(worker(i, shutdown_event))
        tasks.add(task)

    # Wait for shutdown
    await shutdown_event.wait()

    # Cancel all tasks
    for task in tasks:
        task.cancel()

    await asyncio.gather(*tasks, return_exceptions=True)
```

---

## Common Mistakes

1. **Blocking the event loop** - Never use `time.sleep()`, use `asyncio.sleep()`
2. **Missing await** - Forgetting `await` silently creates coroutine object
3. **Fire and forget** - Untracked tasks can be garbage collected
4. **Nested asyncio.run()** - Cannot nest event loops
5. **Shared mutable state** - Race conditions without locks

---

## Checklist

- [ ] No blocking calls in async code
- [ ] All coroutines awaited
- [ ] Tasks tracked properly
- [ ] Exceptions handled
- [ ] Timeouts configured
- [ ] Graceful shutdown implemented
- [ ] Rate limiting for external APIs
- [ ] Thread pool for CPU-bound work

---

## Next Steps

- M-PY-003: FastAPI Patterns
- M-PY-004: Pytest Testing

---

*Methodology M-PY-005 v1.0*
