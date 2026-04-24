# Python Async Patterns Examples

Real-world async code examples demonstrating production patterns.

---

## Basic Async/Await

### Simple HTTP Request

```python
import asyncio
import httpx


async def fetch_user(user_id: int) -> dict:
    """Fetch user data from API."""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://api.example.com/users/{user_id}",
            timeout=30.0
        )
        response.raise_for_status()
        return response.json()


async def main():
    user = await fetch_user(123)
    print(f"User: {user['name']}")


if __name__ == "__main__":
    asyncio.run(main())
```

### Multiple Sequential Requests

```python
import asyncio
import httpx


async def fetch_user_with_posts(user_id: int) -> dict:
    """Fetch user and their posts sequentially."""
    async with httpx.AsyncClient(base_url="https://api.example.com") as client:
        # First request
        user_response = await client.get(f"/users/{user_id}")
        user = user_response.json()

        # Second request (depends on first)
        posts_response = await client.get(f"/users/{user_id}/posts")
        posts = posts_response.json()

        return {"user": user, "posts": posts}
```

---

## Concurrent Execution with asyncio.gather()

### Fetch Multiple Resources Concurrently

```python
import asyncio
import httpx
from typing import Any


async def fetch_json(client: httpx.AsyncClient, url: str) -> dict[str, Any]:
    """Fetch JSON from URL."""
    response = await client.get(url, timeout=30.0)
    response.raise_for_status()
    return response.json()


async def fetch_all_users(user_ids: list[int]) -> list[dict]:
    """Fetch multiple users concurrently."""
    async with httpx.AsyncClient(base_url="https://api.example.com") as client:
        # Create coroutines for all requests
        coroutines = [
            fetch_json(client, f"/users/{uid}")
            for uid in user_ids
        ]

        # Execute all concurrently - returns list in same order
        results = await asyncio.gather(*coroutines, return_exceptions=True)

        # Filter out errors, keep successful results
        users = [
            result for result in results
            if not isinstance(result, Exception)
        ]

        # Log errors
        errors = [
            result for result in results
            if isinstance(result, Exception)
        ]
        for error in errors:
            print(f"Failed to fetch user: {error}")

        return users


async def main():
    # Sequential: 10 * 0.5s = 5 seconds
    # Concurrent: ~0.5 seconds total
    user_ids = list(range(1, 11))
    users = await fetch_all_users(user_ids)
    print(f"Fetched {len(users)} users")


if __name__ == "__main__":
    asyncio.run(main())
```

### Parallel API Calls with Different Endpoints

```python
import asyncio
import httpx


async def fetch_dashboard_data(user_id: int) -> dict:
    """Fetch all dashboard data in parallel."""
    async with httpx.AsyncClient(base_url="https://api.example.com") as client:
        # All independent - can run in parallel
        user_coro = client.get(f"/users/{user_id}")
        orders_coro = client.get(f"/users/{user_id}/orders")
        notifications_coro = client.get(f"/users/{user_id}/notifications")
        settings_coro = client.get(f"/users/{user_id}/settings")

        # Wait for all
        responses = await asyncio.gather(
            user_coro,
            orders_coro,
            notifications_coro,
            settings_coro
        )

        return {
            "user": responses[0].json(),
            "orders": responses[1].json(),
            "notifications": responses[2].json(),
            "settings": responses[3].json(),
        }
```

---

## TaskGroup (Python 3.11+)

### Basic TaskGroup Usage

```python
import asyncio


async def process_item(item_id: int) -> dict:
    """Process a single item."""
    await asyncio.sleep(0.1)  # Simulate I/O
    return {"id": item_id, "status": "processed"}


async def process_all_items(item_ids: list[int]) -> list[dict]:
    """Process items concurrently with TaskGroup."""
    tasks: list[asyncio.Task] = []

    async with asyncio.TaskGroup() as tg:
        for item_id in item_ids:
            task = tg.create_task(process_item(item_id))
            tasks.append(task)

    # All tasks completed when exiting context
    # If any task raised exception, others were cancelled
    return [task.result() for task in tasks]


async def main():
    item_ids = list(range(1, 21))
    results = await process_all_items(item_ids)
    print(f"Processed {len(results)} items")


if __name__ == "__main__":
    asyncio.run(main())
```

### TaskGroup with Exception Handling

```python
import asyncio
import random


async def risky_operation(operation_id: int) -> str:
    """Operation that might fail."""
    await asyncio.sleep(0.1)

    # Simulate random failures
    if random.random() < 0.3:
        raise ValueError(f"Operation {operation_id} failed")

    return f"Success: {operation_id}"


async def process_with_error_handling():
    """Process operations with proper error handling."""
    try:
        async with asyncio.TaskGroup() as tg:
            tasks = [
                tg.create_task(risky_operation(i), name=f"op-{i}")
                for i in range(10)
            ]
    except* ValueError as eg:
        # Handle all ValueErrors as a group
        print(f"Caught {len(eg.exceptions)} ValueErrors:")
        for exc in eg.exceptions:
            print(f"  - {exc}")
        # TaskGroup cancelled remaining tasks automatically
        return []
    except* TypeError as eg:
        print(f"Caught {len(eg.exceptions)} TypeErrors")
        return []

    # Only reached if ALL tasks succeeded
    return [task.result() for task in tasks]


async def main():
    results = await process_with_error_handling()
    print(f"Successful results: {len(results)}")


if __name__ == "__main__":
    asyncio.run(main())
```

### TaskGroup for Dependent Operations

```python
import asyncio
import httpx


async def fetch_and_process_orders(user_id: int) -> dict:
    """
    Fetch user orders and process each one.
    If any processing fails, cancel all other processing.
    """
    async with httpx.AsyncClient(base_url="https://api.example.com") as client:
        # First, fetch the orders list
        response = await client.get(f"/users/{user_id}/orders")
        orders = response.json()

        # Then process all orders concurrently
        async with asyncio.TaskGroup() as tg:
            tasks = [
                tg.create_task(
                    process_order(client, order["id"]),
                    name=f"order-{order['id']}"
                )
                for order in orders
            ]

        # All succeeded
        return {
            "user_id": user_id,
            "processed_orders": [task.result() for task in tasks]
        }


async def process_order(client: httpx.AsyncClient, order_id: int) -> dict:
    """Process a single order."""
    # Fetch order details
    response = await client.get(f"/orders/{order_id}")
    order = response.json()

    # Process it (e.g., validate, transform)
    return {
        "id": order_id,
        "total": order["total"],
        "status": "processed"
    }
```

---

## Rate Limiting with Semaphore

### Basic Rate Limiting

```python
import asyncio
import httpx


async def fetch_with_rate_limit(
    urls: list[str],
    max_concurrent: int = 5
) -> list[dict | None]:
    """Fetch URLs with concurrency limit."""
    semaphore = asyncio.Semaphore(max_concurrent)

    async def fetch_one(url: str) -> dict | None:
        async with semaphore:  # Only N concurrent at a time
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.get(url, timeout=30.0)
                    response.raise_for_status()
                    return response.json()
            except httpx.HTTPError as e:
                print(f"Error fetching {url}: {e}")
                return None

    # Create all tasks (they'll wait on semaphore)
    tasks = [fetch_one(url) for url in urls]
    results = await asyncio.gather(*tasks)

    return results


async def main():
    # 100 URLs, but only 10 concurrent requests
    urls = [f"https://api.example.com/items/{i}" for i in range(100)]
    results = await fetch_with_rate_limit(urls, max_concurrent=10)
    successful = [r for r in results if r is not None]
    print(f"Successfully fetched {len(successful)}/{len(urls)}")


if __name__ == "__main__":
    asyncio.run(main())
```

### Rate Limiting with TaskGroup

```python
import asyncio
import httpx


async def rate_limited_taskgroup(
    urls: list[str],
    max_concurrent: int = 5
) -> list[dict]:
    """Fetch URLs with TaskGroup and rate limiting."""
    semaphore = asyncio.Semaphore(max_concurrent)

    async def fetch_one(client: httpx.AsyncClient, url: str) -> dict:
        async with semaphore:
            response = await client.get(url, timeout=30.0)
            response.raise_for_status()
            return response.json()

    tasks: list[asyncio.Task] = []

    async with httpx.AsyncClient() as client:
        async with asyncio.TaskGroup() as tg:
            for url in urls:
                task = tg.create_task(fetch_one(client, url))
                tasks.append(task)

    return [task.result() for task in tasks]
```

---

## Timeouts

### Using asyncio.timeout() (Python 3.11+)

```python
import asyncio


async def slow_operation() -> str:
    """Operation that takes too long."""
    await asyncio.sleep(10)
    return "Done"


async def with_timeout():
    """Execute with timeout context manager."""
    try:
        async with asyncio.timeout(2.0):
            result = await slow_operation()
            return result
    except asyncio.TimeoutError:
        print("Operation timed out after 2 seconds")
        return None


async def main():
    result = await with_timeout()
    print(f"Result: {result}")


if __name__ == "__main__":
    asyncio.run(main())
```

### Deadline-Based Timeout

```python
import asyncio


async def with_deadline():
    """Execute multiple operations with shared deadline."""
    loop = asyncio.get_running_loop()
    deadline = loop.time() + 5.0  # 5 seconds from now

    try:
        async with asyncio.timeout_at(deadline):
            # All operations share the same deadline
            result1 = await operation1()  # Takes 2s
            result2 = await operation2()  # Takes 2s
            result3 = await operation3()  # Would take 3s - will timeout!
            return [result1, result2, result3]
    except asyncio.TimeoutError:
        print("Deadline exceeded")
        return None


async def operation1():
    await asyncio.sleep(2)
    return "op1"


async def operation2():
    await asyncio.sleep(2)
    return "op2"


async def operation3():
    await asyncio.sleep(3)
    return "op3"
```

### Timeout with Fallback

```python
import asyncio
import httpx


async def fetch_with_fallback(
    primary_url: str,
    fallback_url: str,
    timeout: float = 5.0
) -> dict:
    """Try primary URL, fall back to secondary on timeout."""
    async with httpx.AsyncClient() as client:
        try:
            async with asyncio.timeout(timeout):
                response = await client.get(primary_url)
                return response.json()
        except asyncio.TimeoutError:
            print(f"Primary URL timed out, trying fallback")
            response = await client.get(fallback_url, timeout=timeout)
            return response.json()
```

---

## Async Context Managers

### Class-Based Context Manager

```python
import asyncio
import asyncpg


class AsyncDatabasePool:
    """Async context manager for database connection pool."""

    def __init__(self, dsn: str, min_size: int = 5, max_size: int = 20):
        self.dsn = dsn
        self.min_size = min_size
        self.max_size = max_size
        self.pool: asyncpg.Pool | None = None

    async def __aenter__(self) -> asyncpg.Pool:
        """Create pool when entering context."""
        self.pool = await asyncpg.create_pool(
            self.dsn,
            min_size=self.min_size,
            max_size=self.max_size
        )
        return self.pool

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> bool:
        """Close pool when exiting context."""
        if self.pool:
            await self.pool.close()
        return False  # Don't suppress exceptions


async def main():
    async with AsyncDatabasePool("postgresql://localhost/db") as pool:
        async with pool.acquire() as conn:
            result = await conn.fetch("SELECT * FROM users")
            print(f"Found {len(result)} users")
```

### Function-Based Context Manager

```python
import asyncio
from contextlib import asynccontextmanager
from typing import AsyncIterator


@asynccontextmanager
async def get_db_session() -> AsyncIterator:
    """Get database session with automatic commit/rollback."""
    session = await create_session()
    try:
        yield session
        await session.commit()
    except Exception:
        await session.rollback()
        raise
    finally:
        await session.close()


@asynccontextmanager
async def timed_operation(name: str) -> AsyncIterator[None]:
    """Context manager that logs operation duration."""
    start = asyncio.get_event_loop().time()
    try:
        yield
    finally:
        duration = asyncio.get_event_loop().time() - start
        print(f"{name} took {duration:.2f}s")


async def main():
    async with timed_operation("Database query"):
        async with get_db_session() as session:
            await session.execute("INSERT INTO logs VALUES ($1)", ["event"])
```

### Nested Context Managers

```python
import asyncio
from contextlib import asynccontextmanager
import httpx


@asynccontextmanager
async def managed_client(base_url: str):
    """HTTP client with logging."""
    print(f"Creating client for {base_url}")
    async with httpx.AsyncClient(base_url=base_url) as client:
        yield client
    print(f"Closed client for {base_url}")


async def main():
    async with managed_client("https://api.example.com") as client:
        async with asyncio.timeout(30.0):
            response = await client.get("/users")
            return response.json()
```

---

## Async Generators and Iterators

### Basic Async Generator

```python
import asyncio
import httpx
from typing import AsyncIterator


async def fetch_pages(base_url: str) -> AsyncIterator[dict]:
    """Fetch paginated data as async generator."""
    page = 1

    async with httpx.AsyncClient() as client:
        while True:
            response = await client.get(
                base_url,
                params={"page": page, "per_page": 100}
            )
            data = response.json()

            if not data["items"]:
                break

            for item in data["items"]:
                yield item

            page += 1


async def process_all_items(base_url: str):
    """Process items as they arrive (memory efficient)."""
    count = 0
    async for item in fetch_pages(base_url):
        # Process each item without loading all into memory
        await process_item(item)
        count += 1

    print(f"Processed {count} items")


async def process_item(item: dict):
    """Process a single item."""
    await asyncio.sleep(0.01)  # Simulate processing
```

### Async Generator with Cleanup

```python
import asyncio
from typing import AsyncIterator


async def stream_with_cleanup() -> AsyncIterator[str]:
    """Async generator with proper cleanup."""
    resource = await acquire_resource()
    try:
        while True:
            data = await resource.read()
            if data is None:
                break
            yield data
    finally:
        # Always runs, even if generator is closed early
        await resource.close()
        print("Resource cleaned up")


async def consume_partially():
    """Consume only first few items."""
    async for i, item in enumerate(stream_with_cleanup()):
        print(item)
        if i >= 5:
            break  # Generator's finally block still runs
```

### Async Comprehensions

```python
import asyncio
from typing import AsyncIterator


async def get_numbers() -> AsyncIterator[int]:
    for i in range(10):
        await asyncio.sleep(0.1)
        yield i


async def main():
    # Async list comprehension
    numbers = [n async for n in get_numbers()]

    # Async list comprehension with filter
    evens = [n async for n in get_numbers() if n % 2 == 0]

    # Async set comprehension
    number_set = {n async for n in get_numbers()}

    # Async dict comprehension
    number_dict = {n: n**2 async for n in get_numbers()}

    print(f"Numbers: {numbers}")
    print(f"Evens: {evens}")
```

---

## Background Tasks

### Background Task Manager

```python
import asyncio
from typing import Awaitable, Callable
import logging

logger = logging.getLogger(__name__)


class BackgroundTaskManager:
    """Manage background tasks with proper lifecycle."""

    def __init__(self):
        self.tasks: set[asyncio.Task] = set()

    def add_task(
        self,
        coro: Awaitable,
        *,
        name: str | None = None,
        on_error: Callable[[Exception], None] | None = None
    ) -> asyncio.Task:
        """Add a background task."""
        task = asyncio.create_task(coro, name=name)
        self.tasks.add(task)

        def done_callback(t: asyncio.Task):
            self.tasks.discard(t)
            if t.cancelled():
                logger.info(f"Task {t.get_name()} was cancelled")
            elif t.exception():
                exc = t.exception()
                logger.error(f"Task {t.get_name()} failed: {exc}")
                if on_error:
                    on_error(exc)

        task.add_done_callback(done_callback)
        return task

    async def shutdown(self, timeout: float = 5.0):
        """Gracefully shutdown all background tasks."""
        if not self.tasks:
            return

        logger.info(f"Shutting down {len(self.tasks)} background tasks")

        # Cancel all tasks
        for task in self.tasks:
            task.cancel()

        # Wait for cancellation
        done, pending = await asyncio.wait(
            self.tasks,
            timeout=timeout,
            return_when=asyncio.ALL_COMPLETED
        )

        if pending:
            logger.warning(f"{len(pending)} tasks didn't complete in time")

    @property
    def active_count(self) -> int:
        return len(self.tasks)


# Global instance
background_tasks = BackgroundTaskManager()
```

### Usage with FastAPI

```python
from fastapi import FastAPI
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    yield
    # Shutdown
    await background_tasks.shutdown()


app = FastAPI(lifespan=lifespan)


@app.post("/orders")
async def create_order(order_data: dict):
    order = await order_service.create(order_data)

    # Fire-and-forget email
    background_tasks.add_task(
        send_order_confirmation(order.id),
        name=f"email-order-{order.id}",
        on_error=lambda e: logger.error(f"Failed to send email: {e}")
    )

    return order
```

---

## Running Sync Code in Async

### Using run_in_executor

```python
import asyncio
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from functools import partial


def cpu_intensive_task(data: bytes) -> bytes:
    """CPU-bound synchronous task."""
    # Heavy computation (e.g., image processing)
    import hashlib
    for _ in range(1000):
        data = hashlib.sha256(data).digest()
    return data


def blocking_io_task(filepath: str) -> str:
    """Blocking I/O that can't be made async."""
    with open(filepath, 'r') as f:
        return f.read()


# Thread pool for blocking I/O
io_executor = ThreadPoolExecutor(max_workers=10)

# Process pool for CPU-bound
cpu_executor = ProcessPoolExecutor(max_workers=4)


async def process_file_async(filepath: str) -> str:
    """Run blocking I/O in thread pool."""
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(
        io_executor,
        blocking_io_task,
        filepath
    )


async def cpu_bound_async(data: bytes) -> bytes:
    """Run CPU-bound in process pool."""
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(
        cpu_executor,
        cpu_intensive_task,
        data
    )


async def main():
    # I/O-bound in threads
    content = await process_file_async("/path/to/file.txt")

    # CPU-bound in processes
    result = await cpu_bound_async(b"data")

    print(f"File content length: {len(content)}")
    print(f"Hash result: {result.hex()}")


if __name__ == "__main__":
    asyncio.run(main())
```

---

## Testing Async Code

### Basic pytest-asyncio Test

```python
import pytest
import httpx
from unittest.mock import AsyncMock, patch


@pytest.mark.asyncio
async def test_fetch_user():
    """Test async function."""
    user = await fetch_user(1)
    assert user["id"] == 1
    assert "name" in user


@pytest.mark.asyncio
async def test_fetch_user_not_found():
    """Test error handling."""
    with pytest.raises(httpx.HTTPStatusError):
        await fetch_user(99999)


@pytest.mark.asyncio
async def test_with_mock():
    """Test with mocked HTTP client."""
    mock_response = AsyncMock()
    mock_response.json.return_value = {"id": 1, "name": "Test User"}
    mock_response.raise_for_status = AsyncMock()

    with patch("httpx.AsyncClient.get", return_value=mock_response):
        result = await fetch_user(1)
        assert result["name"] == "Test User"


@pytest.mark.asyncio
async def test_timeout():
    """Test timeout behavior."""
    with pytest.raises(asyncio.TimeoutError):
        async with asyncio.timeout(0.1):
            await asyncio.sleep(1.0)
```

### Async Fixtures

```python
import pytest
import asyncpg


@pytest.fixture
async def db_pool():
    """Async fixture for database pool."""
    pool = await asyncpg.create_pool("postgresql://localhost/test_db")
    yield pool
    await pool.close()


@pytest.fixture
async def test_user(db_pool):
    """Create test user, cleanup after test."""
    async with db_pool.acquire() as conn:
        user_id = await conn.fetchval(
            "INSERT INTO users (name) VALUES ($1) RETURNING id",
            "Test User"
        )

    yield {"id": user_id, "name": "Test User"}

    # Cleanup
    async with db_pool.acquire() as conn:
        await conn.execute("DELETE FROM users WHERE id = $1", user_id)


@pytest.mark.asyncio
async def test_with_fixtures(db_pool, test_user):
    """Test using async fixtures."""
    async with db_pool.acquire() as conn:
        row = await conn.fetchrow(
            "SELECT * FROM users WHERE id = $1",
            test_user["id"]
        )
        assert row["name"] == "Test User"
```

### Testing TaskGroup Exception Handling

```python
import pytest


@pytest.mark.asyncio
async def test_taskgroup_cancellation():
    """Test that TaskGroup cancels remaining tasks on error."""
    completed = []

    async def slow_task(name: str):
        await asyncio.sleep(1.0)
        completed.append(name)

    async def failing_task():
        await asyncio.sleep(0.1)
        raise ValueError("Intentional failure")

    with pytest.raises(ExceptionGroup) as exc_info:
        async with asyncio.TaskGroup() as tg:
            tg.create_task(slow_task("task1"))
            tg.create_task(slow_task("task2"))
            tg.create_task(failing_task())

    # Verify slow tasks were cancelled (not completed)
    assert len(completed) == 0

    # Verify exception group contains our error
    assert len(exc_info.value.exceptions) == 1
    assert isinstance(exc_info.value.exceptions[0], ValueError)
```
